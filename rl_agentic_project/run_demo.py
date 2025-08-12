# run_demo.py
"""
Launch script for RL Agentic System
Provides options to run Python or HTML demo
"""

import os
import webbrowser
import sys

def main():
    print("="*60)
    print("🚀 RL AGENTIC SYSTEM - ADAPTIVE TUTORIAL AGENT")
    print("="*60)
    print("\nSelect Demo Option:")
    print("1. Run HTML Interactive Demo (Browser)")
    print("2. Run Python Implementation")
    print("3. Run Both Demos")
    print("4. View Results Folder")
    print("5. Exit")
    
    choice = input("\nEnter choice (1-5): ")
    
    if choice == "1":
        # Launch HTML demo
        html_path = os.path.join(os.getcwd(), "web_demo", "rl_demo.html")
        if os.path.exists(html_path):
            webbrowser.open(f"file:///{html_path}")
            print("✅ HTML Demo launched in browser!")
        else:
            print("❌ HTML file not found. Please ensure rl_demo.html is in web_demo folder")
    
    elif choice == "2":
        # Run Python implementation
        print("\n" + "="*40)
        print("Starting Python Implementation...")
        print("="*40)
        os.system("python main.py")
    
    elif choice == "3":
        # Run both
        html_path = os.path.join(os.getcwd(), "web_demo", "rl_demo.html")
        webbrowser.open(f"file:///{html_path}")
        print("✅ HTML Demo launched in browser!")
        print("\nNow starting Python implementation...\n")
        os.system("python main.py")
    
    elif choice == "4":
        # Open results folder
        results_path = os.path.join(os.getcwd(), "results")
        os.makedirs(results_path, exist_ok=True)
        os.startfile(results_path)
        print("✅ Results folder opened!")
    
    elif choice == "5":
        print("Goodbye!")
        sys.exit()
    
    else:
        print("Invalid choice. Please try again.")
        main()

if __name__ == "__main__":
    main()