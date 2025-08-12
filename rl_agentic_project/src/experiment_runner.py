"""
Experiment Runner for RL Agents
"""

import numpy as np
import time
from typing import Dict, List
from rl_agent import QLearningAgent, ThompsonSamplingAgent, HybridAgent
from environment import TutorialEnvironment

class ExperimentRunner:
    """Manages experiments and collects metrics"""
    
    def __init__(self, agent_type: str = "hybrid", env_type: str = "average"):
        """
        Initialize experiment runner
        
        Args:
            agent_type: One of "qlearning", "thompson", or "hybrid"
            env_type: One of "fast", "average", or "slow"
        """
        self.agent_type = agent_type
        self.env = TutorialEnvironment(env_type)
        
        # Initialize agent based on type
        if agent_type == "qlearning":
            self.agent = QLearningAgent()
        elif agent_type == "thompson":
            self.agent = ThompsonSamplingAgent()
        else:  # hybrid
            self.agent = HybridAgent()
        
        # Initialize metrics storage
        self.metrics = {
            "episode_rewards": [],
            "success_rates": [],
            "action_distribution": np.zeros(4),
            "performance_history": [],
            "difficulty_history": [],
            "convergence_episode": None,
            "q_table_sizes": []
        }
        
    def run_episode(self, episode_num: int) -> float:
        """Run a single episode"""
        state = self.env.reset()
        episode_reward = 0
        successes = 0
        actions_taken = []
        
        while True:
            # Select action
            action = self.agent.select_action(state)
            
            # Execute action in environment
            next_state, reward, done, info = self.env.step(action)
            
            # Update agent
            self.agent.update(state, action, reward, next_state, done)
            
            # Track metrics
            episode_reward += reward
            if info["success"]:
                successes += 1
            actions_taken.append(action)
            self.metrics["action_distribution"][action] += 1
            
            # Move to next state
            state = next_state
            
            if done:
                break
        
        # Calculate episode metrics
        success_rate = successes / len(actions_taken) if actions_taken else 0
        self.metrics["success_rates"].append(success_rate)
        self.metrics["performance_history"].append(state.performance)
        self.metrics["difficulty_history"].append(actions_taken)
        self.metrics["q_table_sizes"].append(self.agent.get_q_table_size())
        
        return episode_reward
    
    def run_experiment(self, n_episodes: int = 100, verbose: bool = True) -> Dict:
        """
        Run full experiment
        
        Args:
            n_episodes: Number of episodes to run
            verbose: Whether to print progress updates
        """
        start_time = time.time()
        
        for episode in range(n_episodes):
            # Run episode
            reward = self.run_episode(episode)
            self.metrics["episode_rewards"].append(reward)
            
            # Check for convergence
            if self._check_convergence() and self.metrics["convergence_episode"] is None:
                self.metrics["convergence_episode"] = episode
            
            # Progress updates
            if verbose and (episode + 1) % 10 == 0:
                self._print_progress(episode + 1, n_episodes)
        
        # Calculate final metrics
        execution_time = time.time() - start_time
        
        return self._generate_report(execution_time)
    
    def _print_progress(self, current_episode: int, total_episodes: int):
        """Print progress update"""
        avg_reward = np.mean(self.metrics["episode_rewards"][-10:])
        avg_success = np.mean(self.metrics["success_rates"][-10:])
        progress = current_episode / total_episodes
        
        bar_length = 30
        filled = int(bar_length * progress)
        bar = '█' * filled + '░' * (bar_length - filled)
        
        print(f"Progress: [{bar}] {progress:.0%} | "
              f"Episode {current_episode}/{total_episodes} | "
              f"Avg Reward: {avg_reward:.2f} | "
              f"Success Rate: {avg_success:.2%}")
    
    def _check_convergence(self, window: int = 10, threshold: float = 0.5) -> bool:
        """Check if learning has converged"""
        if len(self.metrics["episode_rewards"]) < window * 2:
            return False
        
        recent = self.metrics["episode_rewards"][-window:]
        previous = self.metrics["episode_rewards"][-window*2:-window]
        
        recent_mean = np.mean(recent)
        previous_mean = np.mean(previous)
        
        return abs(recent_mean - previous_mean) < threshold
    
    def _generate_report(self, execution_time: float) -> Dict:
        """Generate comprehensive experiment report"""
        rewards = self.metrics["episode_rewards"]
        success_rates = self.metrics["success_rates"]
        
        report = {
            "agent_type": self.agent_type,
            "total_episodes": len(rewards),
            "execution_time": execution_time,
            "total_reward": sum(rewards),
            "avg_reward": np.mean(rewards),
            "std_reward": np.std(rewards),
            "max_reward": max(rewards),
            "min_reward": min(rewards),
            "final_10_avg_reward": np.mean(rewards[-10:]) if len(rewards) >= 10 else np.mean(rewards),
            "final_success_rate": np.mean(success_rates[-10:]) if len(success_rates) >= 10 else np.mean(success_rates),
            "overall_success_rate": np.mean(success_rates),
            "convergence_episode": self.metrics["convergence_episode"],
            "action_distribution": self.metrics["action_distribution"].tolist(),
            "final_performance": self.metrics["performance_history"][-1] if self.metrics["performance_history"] else 0,
            "final_q_table_size": self.metrics["q_table_sizes"][-1] if self.metrics["q_table_sizes"] else 0
        }
        
        # Calculate improvement
        if len(rewards) >= 20:
            initial_avg = np.mean(rewards[:10])
            final_avg = np.mean(rewards[-10:])
            report["improvement"] = ((final_avg - initial_avg) / abs(initial_avg)) * 100 if initial_avg != 0 else 0
        else:
            report["improvement"] = 0
        
        return report