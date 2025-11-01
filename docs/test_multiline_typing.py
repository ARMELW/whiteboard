#!/usr/bin/env python3
"""Test script to verify multiline text typing behavior."""

import sys
import json
import os
import tempfile
import shutil

# Create a test config with multiline text
test_config = {
    "slides": [
        {
            "index": 0,
            "duration": 3,
            "skip_rate": 8,
            "layers": [
                {
                    "type": "text",
                    "z_index": 1,
                    "skip_rate": 5,
                    "mode": "draw",
                    "text_config": {
                        "text": "Armel Wanes\\nProject",
                        "font": "DejaVuSans",
                        "size": 72,
                        "color": [0, 0, 0],
                        "style": "bold",
                        "line_height": 1.5,
                        "align": "left"
                    }
                }
            ]
        }
    ]
}

# Create temp directory
temp_dir = tempfile.mkdtemp()
config_path = os.path.join(temp_dir, "test_multiline.json")
output_path = os.path.join(temp_dir, "output.mp4")

try:
    # Write config
    with open(config_path, 'w') as f:
        json.dump(test_config, f, indent=2)
    
    print("=" * 70)
    print("Testing Multiline Text Typing")
    print("=" * 70)
    print()
    print("Test text: 'Armel Wanes\\nProject'")
    print()
    print("Expected behavior:")
    print("  1. Write 'Armel Wanes' completely from left to right")
    print("  2. Then write 'Project' from left to right")
    print()
    print("Config saved to:", config_path)
    print()
    print("To test manually, run:")
    print(f"  python3 whiteboard_animator.py --config {config_path}")
    print()
    print("=" * 70)
    
finally:
    # Cleanup
    if os.path.exists(config_path):
        print(f"Note: Temp files in {temp_dir}")
        print("Clean up when done with: rm -rf", temp_dir)
