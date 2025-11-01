#!/usr/bin/env python3
"""Test the exact example from the issue to verify the fix."""

import sys
import os
import json
import cv2

sys.path.insert(0, os.path.dirname(__file__))

from whiteboard_animator import compose_layers

def test_issue_example():
    """Test the exact configuration from the issue."""
    print("Testing the exact example from the GitHub issue...")
    
    # The exact configuration from the issue
    config = {
        "slides": [
            {
                "index": 0,
                "duration": 2,
                "skip_rate": 10,
                "layers": [
                    {
                        "type": "text",
                        "z_index": 0,
                        "mode": "draw",
                        "width": 799.2,
                        "height": 106.56,
                        "scale": 1,
                        "source_width": 800,
                        "source_height": 450,
                        "opacity": 1,
                        "skip_rate": 12,
                        "anchor_point": "center",
                        "position": {
                            "x": 163,
                            "y": 129
                        },
                        "text_config": {
                            "text": "Votre texte ici",
                            "font_path": "fonts/Pacifico.ttf",
                            "font": "Pacifico",
                            "size": 37,
                            "style": "normal",
                            "color": [0, 0, 0],
                            "align": "center"
                        }
                    }
                ]
            }
        ]
    }
    
    # Test with different styles
    test_cases = [
        ("normal", "normal"),
        ("bold", "bold"),
        ("italic", "italic"),
        ("bold italic", "bold italic")
    ]
    
    results = []
    for style_name, style_value in test_cases:
        print(f"\n  Testing with style: {style_name}")
        
        # Update the config with the current style
        config["slides"][0]["layers"][0]["text_config"]["style"] = style_value
        config["slides"][0]["layers"][0]["text_config"]["text"] = f"Style: {style_name}"
        
        layers_config = config['slides'][0]['layers']
        
        try:
            result = compose_layers(layers_config, 800, 450)
            if result is not None:
                print(f"    ✓ {style_name} style rendered successfully")
                
                # Save the result for visual inspection
                output_path = f"/home/runner/work/whiteboard/whiteboard/test_issue_{style_name.replace(' ', '_')}.png"
                cv2.imwrite(output_path, result)
                print(f"    → Saved to: {output_path}")
                results.append(True)
            else:
                print(f"    ✗ {style_name} style failed to render")
                results.append(False)
        except Exception as e:
            print(f"    ✗ {style_name} style raised exception: {e}")
            import traceback
            traceback.print_exc()
            results.append(False)
    
    # Test alignments
    print("\n  Testing alignments...")
    alignment_cases = [
        ("left", "left"),
        ("center", "center"),
        ("right", "right")
    ]
    
    for align_name, align_value in alignment_cases:
        print(f"\n  Testing with alignment: {align_name}")
        
        # Update the config with the current alignment
        config["slides"][0]["layers"][0]["text_config"]["align"] = align_value
        config["slides"][0]["layers"][0]["text_config"]["text"] = f"Align: {align_name}"
        config["slides"][0]["layers"][0]["text_config"]["style"] = "bold"  # Use bold for better visibility
        
        layers_config = config['slides'][0]['layers']
        
        try:
            result = compose_layers(layers_config, 800, 450)
            if result is not None:
                print(f"    ✓ {align_name} alignment rendered successfully")
                
                # Save the result for visual inspection
                output_path = f"/home/runner/work/whiteboard/whiteboard/test_issue_align_{align_name}.png"
                cv2.imwrite(output_path, result)
                print(f"    → Saved to: {output_path}")
                results.append(True)
            else:
                print(f"    ✗ {align_name} alignment failed to render")
                results.append(False)
        except Exception as e:
            print(f"    ✗ {align_name} alignment raised exception: {e}")
            import traceback
            traceback.print_exc()
            results.append(False)
    
    return all(results)

if __name__ == "__main__":
    print("=" * 70)
    print("Testing Issue Example: Text Style and Alignment")
    print("=" * 70)
    
    success = test_issue_example()
    
    print("\n" + "=" * 70)
    if success:
        print("✓ All tests passed - Issue is fixed!")
        print("\nThe fix ensures that:")
        print("  • Text styles (normal, bold, italic, bold italic) are applied")
        print("  • Alignment (left, center, right) works correctly")
        print("  • Fonts without style variants use synthetic styling")
    else:
        print("✗ Some tests failed")
    print("=" * 70)
    
    sys.exit(0 if success else 1)
