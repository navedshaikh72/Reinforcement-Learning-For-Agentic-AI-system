"""
Tutorial Environment for RL Agent
"""

import numpy as np
from typing import Tuple, Dict
from rl_agent import State

class TutorialEnvironment:
    """Simulated adaptive tutorial environment"""
    
    def __init__(self, learner_type: str = "average"):
        """Initialize environment with learner profile"""
        self.learner_profiles = {
            "fast": {
                "base_prob": 0.8,
                "learn_rate": 0.15,
                "fatigue_rate": 0.01
            },
            "average": {
                "base_prob": 0.6,
                "learn_rate": 0.08,
                "fatigue_rate": 0.02
            },
            "slow": {
                "base_prob": 0.4,
                "learn_rate": 0.04,
                "fatigue_rate": 0.03
            }
        }
        
        self.profile = self.learner_profiles[learner_type]
        self.difficulties = ["Easy", "Medium", "Hard", "Expert"]
        self.reset()
        
    def reset(self) -> State:
        """Reset environment to initial state"""
        self.state = State(
            performance=0.5,
            streak=0,
            questions_answered=0,
            difficulty=1  # Start with medium
        )
        self.fatigue = 0
        return self.state
    
    def step(self, action: int) -> Tuple[State, float, bool, Dict]:
        """
        Execute action and return new state, reward, done flag, and info
        
        Args:
            action: Difficulty level (0=Easy, 1=Medium, 2=Hard, 3=Expert)
        """
        # Calculate success probability
        success_prob = self._calculate_success_probability(action)
        success = np.random.random() < success_prob
        
        # Calculate reward
        reward = self._calculate_reward(action, success)
        
        # Update state
        old_performance = self.state.performance
        
        if success:
            # Improve performance
            self.state.performance = min(1.0, 
                self.state.performance + self.profile["learn_rate"])
            self.state.streak += 1
        else:
            # Decrease performance
            self.state.performance = max(0.0, 
                self.state.performance - self.profile["learn_rate"] / 2)
            self.state.streak = 0
        
        # Update fatigue
        self.fatigue = min(0.5, self.fatigue + self.profile["fatigue_rate"])
        
        # Update counters
        self.state.questions_answered += 1
        self.state.difficulty = action
        
        # Check if episode is done (20 questions per episode)
        done = self.state.questions_answered >= 20
        
        # Prepare info dictionary
        info = {
            "success": success,
            "difficulty": self.difficulties[action],
            "performance_change": self.state.performance - old_performance,
            "success_probability": success_prob
        }
        
        return self.state, reward, done, info
    
    def _calculate_success_probability(self, difficulty: int) -> float:
        """Calculate probability of correct answer based on difficulty and state"""
        # Base difficulty factors
        difficulty_factors = [1.3, 1.0, 0.7, 0.5]  # Easy to Expert
        
        # Calculate base probability
        base_prob = self.profile["base_prob"] * self.state.performance
        
        # Apply difficulty factor
        prob = base_prob * difficulty_factors[difficulty]
        
        # Apply fatigue penalty
        prob *= (1 - self.fatigue)
        
        # Add streak bonus (max 10% bonus)
        streak_bonus = min(0.1, self.state.streak * 0.02)
        prob += streak_bonus
        
        # Ensure probability is between 0 and 0.95
        return np.clip(prob, 0.05, 0.95)
    
    def _calculate_reward(self, difficulty: int, success: bool) -> float:
        """
        Calculate reward based on action and outcome
        
        Reward design principles:
        - Encourage appropriate difficulty selection
        - Higher rewards for harder successful questions
        - Penalties for failures (less severe for harder questions)
        - Bonus for optimal challenge level
        """
        reward = 0
        
        if success:
            # Base reward for success (higher for harder questions)
            reward = (difficulty + 1) * 2  # 2, 4, 6, 8
            
            # Streak bonus
            if self.state.streak > 3:
                reward += 1
            if self.state.streak > 5:
                reward += 1
                
        else:
            # Penalty for failure (less severe for harder questions)
            reward = -(4 - difficulty)  # -4, -3, -2, -1
        
        # Bonus for optimal difficulty
        # (where success probability is between 0.4 and 0.7)
        success_prob = self._calculate_success_probability(difficulty)
        if 0.4 <= success_prob <= 0.7:
            reward += 0.5  # Optimal challenge bonus
        
        # Penalty for too easy questions when performance is high
        if self.state.performance > 0.7 and difficulty == 0:
            reward -= 1
        
        # Penalty for too hard questions when performance is low
        if self.state.performance < 0.3 and difficulty == 3:
            reward -= 1
        
        return reward 