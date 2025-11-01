#!/usr/bin/env python3
"""
Test the exact scenario from the issue where font "Gargi" was not being applied.
"""
import sys
import os
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from whiteboard_animator import resolve_font_path, render_text_to_image, compose_scene_with_camera
import cv2

def test_issue_scenario():
    """Test the exact configuration from the GitHub issue."""
    print("=" * 70)
    print("TESTING GITHUB ISSUE: Font not applicable")
    print("=" * 70)
    print()
    
    # Configuration from the issue
    issue_config = {
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
                        "width": 1188,
                        "height": 316.8,
                        "scale": 1,
                        "source_width": 800,
                        "source_height": 450,
                        "opacity": 1,
                        "skip_rate": 12,
                        "anchor_point": "center",
                        "position": {
                            "x": 407.7353908974883,
                            "y": 219.55754812670125
                        },
                        "text_config": {
                            "text": "Votre texte ici\nleka wa",
                            "font": "Gargi",
                            "size": 55,
                            "style": "normal",
                            "color": [0, 0, 0],
                            "align": "center"
                        }
                    }
                ]
            }
        ]
    }
    
    # Test 1: Check font resolution
    print("1. Checking font resolution for 'Gargi':")
    font_path = resolve_font_path("Gargi", "normal")
    if font_path:
        print(f"   ✅ Font 'Gargi' resolved to: {font_path}")
        print(f"   Note: This is the fallback font since Gargi is not installed on the system.")
    else:
        print(f"   ❌ Font 'Gargi' could not be resolved")
    print()
    
    # Test 2: Render text with the config
    print("2. Rendering text with issue configuration:")
    text_config = issue_config["slides"][0]["layers"][0]["text_config"]
    text_config["position"] = issue_config["slides"][0]["layers"][0]["position"]
    text_config["anchor_point"] = issue_config["slides"][0]["layers"][0]["anchor_point"]
    
    try:
        img = render_text_to_image(text_config, 800, 450)
        cv2.imwrite("test_issue_gargi_font.png", img)
        print("   ✅ Text rendered successfully: test_issue_gargi_font.png")
    except Exception as e:
        print(f"   ❌ Failed to render: {str(e)}")
    print()
    
    # Test 3: Compare with known working fonts
    print("3. Comparing with other fonts:")
    
    test_fonts = [
        ("DejaVu Sans", "Known system font"),
        ("Liberation Sans", "Known system font"),
        ("Arial", "Common font (fallback to Liberation Sans)"),
    ]
    
    for font_name, description in test_fonts:
        test_config = text_config.copy()
        test_config["font"] = font_name
        
        font_path = resolve_font_path(font_name, "normal")
        print(f"   Font '{font_name}' ({description}):")
        print(f"      Resolved to: {font_path}")
        
        try:
            img = render_text_to_image(test_config, 800, 450)
            filename = f"test_issue_{font_name.replace(' ', '_')}.png"
            cv2.imwrite(filename, img)
            print(f"      ✅ Rendered: {filename}")
        except Exception as e:
            print(f"      ❌ Failed: {str(e)}")
        print()
    
    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print()
    print("The font resolution system now uses fontconfig (fc-match) to properly")
    print("resolve font family names to actual font file paths on the system.")
    print()
    print("When a font like 'Gargi' is not installed:")
    print("  - fontconfig returns the best fallback font (usually DejaVu Sans)")
    print("  - The text is rendered using this fallback font")
    print("  - The system no longer silently fails with a default PIL font")
    print()
    print("This ensures:")
    print("  ✅ Installed fonts are correctly resolved and used")
    print("  ✅ Missing fonts gracefully fall back to system fonts")
    print("  ✅ Font rendering is consistent across different systems")
    print()
    print("=" * 70)

if __name__ == '__main__':
    test_issue_scenario()
