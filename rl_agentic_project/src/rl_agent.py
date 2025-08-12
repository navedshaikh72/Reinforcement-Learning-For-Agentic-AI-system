"""
Reinforcement Learning Agents Implementation
"""

import numpy as np
from collections import defaultdict
from typing import Dict, Optional

class State:
    """Represents the state of a learner"""
    def __init__(self, performance=0.5, streak=0, questions_answered=0, difficulty=1):
        self.performance = performance
        self.streak = streak
        self.questions_answered = questions_answered
        self.difficulty = difficulty
    
    def to_key(self) -> str:
        """Convert state to hashable key for Q-table"""
        perf_bucket = int(self.performance * 10)
        streak_bucket = min(self.streak, 5)
        return f"{perf_bucket}_{streak_bucket}_{self.difficulty}"

class QLearningAgent:
    """Q-Learning implementation"""
    
    def __init__(self, action_space: int = 4, learning_rate: float = 0.1,
                 discount_factor: float = 0.95, epsilon: float = 0.2):
        self.action_space = action_space
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.epsilon = epsilon
        self.q_table = defaultdict(lambda: np.zeros(action_space))
        
    def select_action(self, state: State) -> int:
        """Epsilon-greedy action selection"""
        if np.random.random() < self.epsilon:
            return np.random.randint(self.action_space)
        
        state_key = state.to_key()
        q_values = self.q_table[state_key]
        
        # Handle ties randomly
        max_q = np.max(q_values)
        best_actions = np.where(q_values == max_q)[0]
        return np.random.choice(best_actions)
    
    def update(self, state: State, action: int, reward: float, 
               next_state: State, done: bool):
        """Q-Learning update rule"""
        state_key = state.to_key()
        next_state_key = next_state.to_key()
        
        current_q = self.q_table[state_key][action]
        
        if done:
            target = reward
        else:
            target = reward + self.discount_factor * np.max(self.q_table[next_state_key])
        
        # Q-learning update
        self.q_table[state_key][action] += self.learning_rate * (target - current_q)
    
    def get_q_table_size(self) -> int:
        """Return the number of states in Q-table"""
        return len(self.q_table)

class ThompsonSamplingAgent:
    """Thompson Sampling for exploration"""
    
    def __init__(self, action_space: int = 4):
        self.action_space = action_space
        self.alpha = np.ones(action_space)  # Success counts + 1
        self.beta = np.ones(action_space)   # Failure counts + 1
        
    def select_action(self, state: State = None) -> int:
        """Sample from Beta distributions"""
        samples = np.random.beta(self.alpha, self.beta)
        return np.argmax(samples)
    
    def update(self, state: State, action: int, reward: float, 
               next_state: State, done: bool):
        """Update Beta distribution parameters"""
        # Update based on reward
        if reward > 0:
            self.alpha[action] += 1
        else:
            self.beta[action] += 1
    
    def get_q_table_size(self) -> int:
        """Return 0 as Thompson doesn't use Q-table"""
        return 0

class HybridAgent:
    """Combines Q-Learning with Thompson Sampling"""
    
    def __init__(self, action_space: int = 4, exploration_rate: float = 0.3):
        self.q_agent = QLearningAgent(action_space, epsilon=0)  # No epsilon for Q-agent
        self.thompson_agent = ThompsonSamplingAgent(action_space)
        self.exploration_rate = exploration_rate
        self.action_space = action_space
        
    def select_action(self, state: State) -> int:
        """Hybrid action selection"""
        if np.random.random() < self.exploration_rate:
            # Use Thompson Sampling for exploration
            return self.thompson_agent.select_action(state)
        else:
            # Use Q-learning for exploitation
            return self.q_agent.select_action(state)
    
    def update(self, state: State, action: int, reward: float, 
               next_state: State, done: bool):
        """Update both agents"""
        self.q_agent.update(state, action, reward, next_state, done)
        self.thompson_agent.update(state, action, reward, next_state, done)
    
    def get_q_table_size(self) -> int:
        """Return Q-table size from Q-agent"""
        return self.q_agent.get_q_table_size()