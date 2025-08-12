# compare_implementations.py
"""
Compare HTML and Python implementations
Generate unified report
"""

import json
import time
import os
from datetime import datetime

def create_comparison_report():
    """Create a comparison report between implementations"""
    
    report = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "implementations": {
            "HTML Demo": {
                "type": "Interactive Browser-based",
                "algorithms": ["Q-Learning", "Thompson Sampling", "Hybrid"],
                "features": [
                    "Real-time visualization",
                    "Interactive controls",
                    "Live metrics",
                    "Immediate feedback"
                ],
                "best_for": "Demonstration and visualization"
            },
            "Python Implementation": {
                "type": "Command-line based",
                "algorithms": ["Q-Learning", "Thompson Sampling", "Hybrid"],
                "features": [
                    "Batch processing",
                    "Statistical analysis",
                    "Data export",
                    "Reproducible experiments"
                ],
                "best_for": "Detailed analysis and research"
            }
        }
    }
    
    # Save report
    os.makedirs("results", exist_ok=True)
    report_file = f"results/comparison_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    with open(report_file, 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"✅ Comparison report saved to: {report_file}")
    
    # Create summary markdown
    summary_file = "results/implementation_summary.md"
    with open(summary_file, 'w') as f:
        f.write("# Implementation Comparison\n\n")
        f.write("## HTML Demo\n")
        f.write("- **Location**: `web_demo/rl_demo.html`\n")
        f.write("- **Run**: Open in browser or VS Code Live Server\n")
        f.write("- **Best for**: Interactive exploration and visualization\n\n")
        f.write("## Python Implementation\n")
        f.write("- **Location**: `main.py` and `src/` folder\n")
        f.write("- **Run**: `python main.py`\n")
        f.write("- **Best for**: Batch experiments and data analysis\n\n")
        f.write("## Key Differences\n")
        f.write("| Feature | HTML Demo | Python Implementation |\n")
        f.write("|---------|-----------|----------------------|\n")
        f.write("| Interactivity | High | Low |\n")
        f.write("| Visualization | Real-time | Post-processing |\n")
        f.write("| Data Export | Limited | Comprehensive |\n")
        f.write("| Reproducibility | Low | High |\n")
    
    print(f"✅ Summary saved to: {summary_file}")

if __name__ == "__main__":
    create_comparison_report()