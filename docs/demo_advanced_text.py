#!/usr/bin/env python3
"""
Quick demonstration of advanced text animation features.
Creates a short video showing the new capabilities.
"""

import os
import sys
import json
import tempfile

# Create a simple test configuration
test_config = {
    "slides": [{
        "index": 0,
        "duration": 8,
        "layers": [
            {
                "type": "text",
                "z_index": 1,
                "skip_rate": 5,
                "text_config": {
                    "text": "Character Animation",
                    "font": "DejaVuSans",
                    "size": 48,
                    "color": "#0066CC",
                    "style": "bold",
                    "align": "center",
                    "animation_type": "character_by_character",
                    "char_duration_frames": 3,
                    "pause_after_word": 8,
                    "position": {"x": 0, "y": 150}
                }
            },
            {
                "type": "text",
                "z_index": 2,
                "skip_rate": 8,
                "text_config": {
                    "text": "With Effects!",
                    "font": "DejaVuSans",
                    "size": 56,
                    "color": "#FF0066",
                    "style": "bold",
                    "align": "center",
                    "animation_type": "word_by_word",
                    "word_duration_frames": 10,
                    "text_effects": {
                        "shadow": {
                            "offset": [3, 3],
                            "color": "#888888"
                        }
                    },
                    "position": {"x": 0, "y": 320}
                }
            }
        ]
    }]
}

# Save config to temporary file
with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
    json.dump(test_config, f, indent=2)
    config_path = f.name

print("=" * 60)
print("Advanced Text Animation Demo")
print("=" * 60)
print(f"\nTest configuration saved to: {config_path}")
print("\nTo generate the demo video, run:")
print(f"  python3 whiteboard_animator.py --config {config_path} --output demo_advanced_text.mp4")
print("\nFeatures demonstrated:")
print("  ✓ Character-by-character animation with pauses")
print("  ✓ Word-by-word animation")
print("  ✓ Text shadow effects")
print("  ✓ Multiple text layers with different animations")
print("\n" + "=" * 60)

# Keep the config file for user to run
print(f"\nConfig file: {config_path}")
print("(File will be kept for you to use)")
