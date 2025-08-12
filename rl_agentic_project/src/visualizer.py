"""
Visualization module for experiment results
"""

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, Optional
import os

# Set style
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

class Visualizer:
    """Create visualizations for RL experiments"""
    
    def __init__(self, metrics: Dict):
        """Initialize with experiment metrics"""
        self.metrics = metrics
        
    def create_all_plots(self, save_path: Optional[str] = None):
        """Create all visualization plots"""
        fig, axes = plt.subplots(2, 3, figsize=(18, 10))
        fig.suptitle('Reinforcement Learning Experiment Results', fontsize=16, fontweight='bold')
        
        # 1. Learning Curve
        self.plot_learning_curve(axes[0, 0])
        
        # 2. Success Rate
        self.plot_success_rate(axes[0, 1])
        
        # 3. Action Distribution
        self.plot_action_distribution(axes[0, 2])
        
        # 4. Performance Evolution
        self.plot_performance_evolution(axes[1, 0])
        
        # 5. Q-Table Growth
        self.plot_q_table_growth(axes[1, 1])
        
        # 6. Reward Distribution
        self.plot_reward_distribution(axes[1, 2])
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=100, bbox_inches='tight')
            print(f"Plots saved to: {save_path}")
        
        plt.show()
        
    def plot_learning_curve(self, ax):
        """Plot episode rewards with moving average"""
        episodes = range(len(self.metrics["episode_rewards"]))
        rewards = self.metrics["episode_rewards"]
        
        # Plot raw rewards
        ax.plot(episodes, rewards, alpha=0.3, color='blue', label='Episode Reward')
        
        # Plot moving average
        window = min(10, len(rewards) // 4)
        if len(rewards) >= window:
            moving_avg = np.convolve(rewards, np.ones(window)/window, mode='valid')
            ax.plot(range(window-1, len(rewards)), moving_avg, 
                   color='red', linewidth=2, label=f'{window}-Episode Average')
        
        ax.set_xlabel('Episode')
        ax.set_ylabel('Reward')
        ax.set_title('Learning Curve')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
    def plot_success_rate(self, ax):
        """Plot success rate over episodes"""
        episodes = range(len(self.metrics["success_rates"]))
        success_rates = [sr * 100 for sr in self.metrics["success_rates"]]
        
        ax.plot(episodes, success_rates, alpha=0.3, color='green', label='Success Rate')
        
        # Moving average
        window = min(10, len(success_rates) // 4)
        if len(success_rates) >= window:
            moving_avg = np.convolve(success_rates, np.ones(window)/window, mode='valid')
            ax.plot(range(window-1, len(success_rates)), moving_avg,
                   color='darkgreen', linewidth=2, label=f'{window}-Episode Average')
        
        ax.set_xlabel('Episode')
        ax.set_ylabel('Success Rate (%)')
        ax.set_title('Success Rate Evolution')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
    def plot_action_distribution(self, ax):
        """Plot distribution of selected actions"""
        actions = ['Easy', 'Medium', 'Hard', 'Expert']
        counts = self.metrics["action_distribution"]
        colors = ['#2ecc71', '#3498db', '#f39c12', '#e74c3c']
        
        bars = ax.bar(actions, counts, color=colors)
        
        # Add percentage labels
        total = sum(counts)
        for bar, count in zip(bars, counts):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{count:.0f}\n({count/total*100:.1f}%)',
                   ha='center', va='bottom')
        
        ax.set_xlabel('Difficulty Level')
        ax.set_ylabel('Selection Count')
        ax.set_title('Action Distribution')
        ax.grid(True, alpha=0.3, axis='y')
        
    def plot_performance_evolution(self, ax):
        """Plot learner performance over episodes"""
        episodes = range(len(self.metrics["performance_history"]))
        performance = [p * 100 for p in self.metrics["performance_history"]]
        
        ax.plot(episodes, performance, color='purple', linewidth=2)
        ax.fill_between(episodes, 0, performance, alpha=0.3, color='purple')
        
        ax.set_xlabel('Episode')
        ax.set_ylabel('Performance Level (%)')
        ax.set_title('Learner Performance Evolution')
        ax.set_ylim([0, 105])
        ax.grid(True, alpha=0.3)
        
        # Add horizontal line at 70% (good performance)
        ax.axhline(y=70, color='green', linestyle='--', alpha=0.5, label='Good Performance')
        ax.legend()
        
    def plot_q_table_growth(self, ax):
        """Plot Q-table size growth"""
        if not self.metrics["q_table_sizes"] or all(s == 0 for s in self.metrics["q_table_sizes"]):
            ax.text(0.5, 0.5, 'N/A for this agent type', 
                   ha='center', va='center', transform=ax.transAxes, fontsize=12)
            ax.set_title('Q-Table Growth')
            return
        
        episodes = range(len(self.metrics["q_table_sizes"]))
        sizes = self.metrics["q_table_sizes"]
        
        ax.plot(episodes, sizes, color='orange', linewidth=2)
        ax.fill_between(episodes, 0, sizes, alpha=0.3, color='orange')
        
        ax.set_xlabel('Episode')
        ax.set_ylabel('Number of States')
        ax.set_title('Q-Table Growth')
        ax.grid(True, alpha=0.3)
        
    def plot_reward_distribution(self, ax):
        """Plot histogram of rewards"""
        rewards = self.metrics["episode_rewards"]
        
        ax.hist(rewards, bins=20, color='teal', alpha=0.7, edgecolor='black')
        ax.axvline(np.mean(rewards), color='red', linestyle='--', 
                  linewidth=2, label=f'Mean: {np.mean(rewards):.2f}')
        ax.axvline(np.median(rewards), color='orange', linestyle='--',
                  linewidth=2, label=f'Median: {np.median(rewards):.2f}')
        
        ax.set_xlabel('Episode Reward')
        ax.set_ylabel('Frequency')
        ax.set_title('Reward Distribution')
        ax.legend()
        ax.grid(True, alpha=0.3, axis='y')
        
    def generate_html_report(self, results: Dict, save_path: str):
        """Generate HTML report with results"""
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>RL Experiment Report</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    margin: 40px;
                    background-color: #f5f5f5;
                }}
                h1 {{
                    color: #333;
                    border-bottom: 3px solid #4CAF50;
                    padding-bottom: 10px;
                }}
                .metrics {{
                    display: grid;
                    grid-template-columns: repeat(3, 1fr);
                    gap: 20px;
                    margin: 30px 0;
                }}
                .metric-card {{
                    background: white;
                    padding: 20px;
                    border-radius: 8px;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                }}
                .metric-label {{
                    color: #666;
                    font-size: 14px;
                    margin-bottom: 5px;
                }}
                .metric-value {{
                    color: #333;
                    font-size: 24px;
                    font-weight: bold;
                }}
                .success {{
                    color: #4CAF50;
                }}
                .warning {{
                    color: #FF9800;
                }}
            </style>
        </head>
        <body>
            <h1>🚀 Reinforcement Learning Experiment Report</h1>
            
            <h2>Configuration</h2>
            <p><strong>Algorithm:</strong> {results['agent_type'].upper()}</p>
            <p><strong>Episodes:</strong> {results['total_episodes']}</p>
            <p><strong>Execution Time:</strong> {results['execution_time']:.2f} seconds</p>
            
            <h2>Performance Metrics</h2>
            <div class="metrics">
                <div class="metric-card">
                    <div class="metric-label">Average Reward</div>
                    <div class="metric-value">{results['avg_reward']:.2f}</div>
                </div>
                <div class="metric-card">
                    <div class="metric-label">Final Success Rate</div>
                    <div class="metric-value success">{results['final_success_rate']:.1%}</div>
                </div>
                <div class="metric-card">
                    <div class="metric-label">Performance Improvement</div>
                    <div class="metric-value">{results.get('improvement', 0):.1f}%</div>
                </div>
                <div class="metric-card">
                    <div class="metric-label">Max Reward</div>
                    <div class="metric-value">{results['max_reward']:.2f}</div>
                </div>
                <div class="metric-card">
                    <div class="metric-label">Convergence</div>
                    <div class="metric-value">{results['convergence_episode'] or 'N/A'}</div>
                </div>
                <div class="metric-card">
                    <div class="metric-label">Q-Table Size</div>
                    <div class="metric-value">{results['final_q_table_size']}</div>
                </div>
            </div>
            
            <h2>Action Distribution</h2>
            <p>Easy: {results['action_distribution'][0]:.0f} selections</p>
            <p>Medium: {results['action_distribution'][1]:.0f} selections</p>
            <p>Hard: {results['action_distribution'][2]:.0f} selections</p>
            <p>Expert: {results['action_distribution'][3]:.0f} selections</p>
            
            <p style="margin-top: 40px; color: #666; font-size: 12px;">
                Generated: {import_datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
            </p>
        </body>
        </html>
        """
        
        # Fix the datetime import issue
        from datetime import datetime as import_datetime
        
        with open(save_path, 'w') as f:
            f.write(html_content)