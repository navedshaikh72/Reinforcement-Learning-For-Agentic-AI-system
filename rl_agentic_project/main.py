"""
Main Runner for RL Agentic System
Run this file to start experiments
"""

import os
import sys
import time
from datetime import datetime

# Add src to path
sys.path.append('src')

from rl_agent import QLearningAgent, ThompsonSamplingAgent, HybridAgent
from environment import TutorialEnvironment
from experiment_runner import ExperimentRunner
from visualizer import Visualizer

def print_header():
    """Print welcome header"""
    print("="*60)
    print("🚀 REINFORCEMENT LEARNING FOR AGENTIC AI SYSTEMS")
    print("    Adaptive Tutorial Agent Implementation")
    print("="*60)
    print()

def get_user_choice(prompt, options):
    """Get user input with validation"""
    print(prompt)
    for i, option in enumerate(options, 1):
        print(f"  {i}. {option}")
    
    while True:
        try:
            choice = int(input("Enter your choice (number): "))
            if 1 <= choice <= len(options):
                return choice - 1
            else:
                print("Invalid choice. Please try again.")
        except ValueError:
            print("Please enter a number.")

def main():
    """Main execution function"""
    print_header()
    
    # Get configuration from user
    print("STEP 1: Choose RL Algorithm")
    algorithms = ["Q-Learning", "Thompson Sampling", "Hybrid (Q-Learning + Thompson)"]
    algo_choice = get_user_choice("Select algorithm:", algorithms)
    algo_map = ["qlearning", "thompson", "hybrid"]
    algorithm = algo_map[algo_choice]
    
    print("\nSTEP 2: Choose Learner Profile")
    profiles = ["Fast Learner", "Average Learner", "Slow Learner"]
    profile_choice = get_user_choice("Select learner profile:", profiles)
    profile_map = ["fast", "average", "slow"]
    profile = profile_map[profile_choice]
    
    print("\nSTEP 3: Set Number of Episodes")
    while True:
        try:
            n_episodes = int(input("Enter number of episodes (10-500, recommended: 100): "))
            if 10 <= n_episodes <= 500:
                break
            else:
                print("Please enter a number between 10 and 500.")
        except ValueError:
            print("Please enter a valid number.")
    
    print("\n" + "="*60)
    print(f"Configuration:")
    print(f"  Algorithm: {algorithms[algo_choice]}")
    print(f"  Learner: {profiles[profile_choice]}")
    print(f"  Episodes: {n_episodes}")
    print("="*60)
    
    input("\nPress Enter to start the experiment...")
    
    # Run experiment
    print("\n🔬 Starting Experiment...\n")
    
    runner = ExperimentRunner(
        agent_type=algorithm,
        env_type=profile
    )
    
    # Run with progress updates
    results = runner.run_experiment(n_episodes=n_episodes, verbose=True)
    
    # Display results
    print("\n📊 EXPERIMENT RESULTS")
    print("="*60)
    print(f"Total Reward: {results['total_reward']:.2f}")
    print(f"Average Reward: {results['avg_reward']:.2f}")
    print(f"Final Success Rate: {results['final_success_rate']:.2%}")
    print(f"Convergence: {results['convergence_episode'] or 'Not achieved'}")
    print(f"Final Performance Level: {results['final_performance']:.2%}")
    
    # Save results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    results_file = f"results/experiment_{algorithm}_{timestamp}.txt"
    
    os.makedirs("results", exist_ok=True)
    with open(results_file, 'w') as f:
        f.write(f"Experiment Results - {timestamp}\n")
        f.write("="*50 + "\n")
        for key, value in results.items():
            f.write(f"{key}: {value}\n")
    
    print(f"\n✅ Results saved to: {results_file}")
    
    # Generate visualizations
    print("\n📈 Generating visualizations...")
    visualizer = Visualizer(runner.metrics)
    
    # Create and save plots
    plot_file = f"results/plots_{algorithm}_{timestamp}.png"
    visualizer.create_all_plots(save_path=plot_file)
    print(f"✅ Plots saved to: {plot_file}")
    
    # Generate HTML report
    html_file = f"results/report_{algorithm}_{timestamp}.html"
    visualizer.generate_html_report(results, html_file)
    print(f"✅ HTML report saved to: {html_file}")
    
    print("\n🎉 Experiment Complete!")
    print("\nWould you like to:")
    print("  1. Run another experiment")
    print("  2. Open results folder")
    print("  3. Exit")
    
    choice = input("Enter choice (1/2/3): ")
    
    if choice == "1":
        print("\n" + "="*60 + "\n")
        main()
    elif choice == "2":
        os.startfile("results")
    else:
        print("\nThank you for using the RL Agentic System!")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nExperiment interrupted by user.")
    except Exception as e:
        print(f"\n❌ Error occurred: {e}")
        input("Press Enter to exit...")