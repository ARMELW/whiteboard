#!/usr/bin/env python3
"""
Demonstration of the new path_follow animation mode.
Creates a simple animation using point-by-point path following.
"""

import os
import sys
import json
import tempfile
from pathlib import Path

# Test configuration with path_follow mode
def create_demo_config():
    """Create a demo configuration using the new path_follow mode"""
    
    config = {
        "output": {
            "path": "demo_path_follow_output.mp4",
            "fps": 30,
            "format": "16:9",
            "quality": 23
        },
        "slides": [
            {
                "duration": 5,
                "layers": [
                    {
                        "image_path": "doodle/1.jpg",
                        "mode": "path_follow",
                        "skip_rate": 3,
                        "position": "center"
                    }
                ]
            }
        ]
    }
    
    return config

def main():
    """Create and save demo configuration"""
    config = create_demo_config()
    
    # Save config to file
    config_path = "demo_path_follow_config.json"
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=2)
    
    print("✅ Created demo configuration for path_follow mode")
    print(f"📄 Configuration saved to: {config_path}")
    print("\nTo run the demo, execute:")
    print(f"  python3 whiteboard_animator.py --from-json {config_path}")
    print("\nExample layer configuration for path_follow mode:")
    print(json.dumps(config['slides'][0]['layers'][0], indent=2))
    print("\nPath follow mode features:")
    print("  • Point-by-point path following animation")
    print("  • Natural hand jitter for realistic movement")
    print("  • Variable speed for human-like effect")
    print("  • Configurable via 'mode': 'path_follow' in layer config")

if __name__ == "__main__":
    main()
