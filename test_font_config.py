#!/usr/bin/env python3
"""
Test the font configuration system that maps font names to .ttf files.
"""
import sys
import os
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from whiteboard_animator import load_font_config, resolve_font_path, render_text_to_image
import cv2

def test_font_config_loading():
    """Test loading the fonts.json configuration file."""
    print("=" * 70)
    print("TEST 1: Loading fonts.json configuration")
    print("=" * 70)
    print()
    
    font_config = load_font_config()
    
    if font_config:
        print(f"✅ Font configuration loaded successfully")
        print(f"   Found {len(font_config)} font(s) in configuration:")
        for font_name, styles in font_config.items():
            print(f"   - {font_name}:")
            for style, path in styles.items():
                print(f"     - {style}: {path}")
    else:
        print("⚠️ No fonts found in configuration (fonts.json may not exist)")
    
    print()
    return font_config

def test_font_resolution():
    """Test that fonts from config are resolved correctly."""
    print("=" * 70)
    print("TEST 2: Font resolution from configuration")
    print("=" * 70)
    print()
    
    # Test Pacifico font (should be in fonts.json)
    print("Testing 'Pacifico' font:")
    font_path = resolve_font_path("Pacifico", "normal")
    if font_path:
        print(f"   ✅ Font resolved to: {font_path}")
        if os.path.exists(font_path):
            print(f"   ✅ Font file exists")
        else:
            print(f"   ❌ Font file does not exist!")
    else:
        print(f"   ❌ Font could not be resolved")
    print()
    
    # Test a font that should use fallback (not in config)
    print("Testing 'DejaVu Sans' font (should use fontconfig fallback):")
    font_path = resolve_font_path("DejaVu Sans", "normal")
    if font_path:
        print(f"   ✅ Font resolved to: {font_path}")
    else:
        print(f"   ⚠️ Font could not be resolved (fontconfig may not be available)")
    print()

def test_text_rendering_without_font_path():
    """Test rendering text using only font name (no font_path in config)."""
    print("=" * 70)
    print("TEST 3: Text rendering without font_path in config")
    print("=" * 70)
    print()
    
    # Test configuration similar to the issue
    text_config = {
        "text": "Test Font Config\nPacifico Font",
        "font": "Pacifico",  # Only font name, no font_path
        "size": 55,
        "style": "normal",
        "color": [0, 0, 0],
        "align": "center"
    }
    
    print("Rendering text with Pacifico font (from fonts.json):")
    print(f"  Config: font='{text_config['font']}', size={text_config['size']}")
    
    try:
        img = render_text_to_image(text_config, 800, 450)
        output_file = "test_font_config_pacifico.png"
        cv2.imwrite(output_file, img)
        print(f"   ✅ Text rendered successfully: {output_file}")
    except Exception as e:
        print(f"   ❌ Failed to render: {str(e)}")
    
    print()

def test_complete_slide_config():
    """Test a complete slide configuration without font_path."""
    print("=" * 70)
    print("TEST 4: Complete slide configuration (like the issue)")
    print("=" * 70)
    print()
    
    # Configuration from the issue, but without font_path
    slide_config = {
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
                            "font": "Pacifico",  # No font_path needed!
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
    
    print("Configuration (without font_path):")
    print(json.dumps(slide_config["slides"][0]["layers"][0]["text_config"], indent=2))
    print()
    
    text_config = slide_config["slides"][0]["layers"][0]["text_config"].copy()
    text_config["position"] = slide_config["slides"][0]["layers"][0]["position"]
    text_config["anchor_point"] = slide_config["slides"][0]["layers"][0]["anchor_point"]
    
    try:
        img = render_text_to_image(text_config, 800, 450)
        output_file = "test_font_config_complete.png"
        cv2.imwrite(output_file, img)
        print(f"✅ Slide rendered successfully: {output_file}")
        print("✅ No need to specify font_path in the configuration!")
    except Exception as e:
        print(f"❌ Failed to render: {str(e)}")
    
    print()

def print_summary():
    """Print summary of the font configuration system."""
    print("=" * 70)
    print("SUMMARY: Font Configuration System")
    print("=" * 70)
    print()
    print("The font configuration system allows you to:")
    print()
    print("1. ✅ Define font mappings in fonts.json")
    print("   - Map font names to .ttf file paths")
    print("   - Support multiple styles (normal, bold, italic, bold italic)")
    print()
    print("2. ✅ Use fonts without specifying font_path in configs")
    print("   - Just specify the font name: 'font': 'Pacifico'")
    print("   - No need to specify: 'font_path': '../fonts/Pacifico/...'")
    print()
    print("3. ✅ Easy to add new fonts")
    print("   - Add entry to fonts.json")
    print("   - No need to modify whiteboard_animator.py")
    print()
    print("4. ✅ Automatic fallback to system fonts")
    print("   - If font not in fonts.json, uses fontconfig")
    print("   - Graceful degradation if fontconfig unavailable")
    print()
    print("Example fonts.json:")
    print('  {')
    print('    "fonts": {')
    print('      "Pacifico": {')
    print('        "normal": "fonts/Pacifico/Pacifico-Regular.ttf"')
    print('      },')
    print('      "Roboto": {')
    print('        "normal": "fonts/Roboto/Roboto-Regular.ttf",')
    print('        "bold": "fonts/Roboto/Roboto-Bold.ttf"')
    print('      }')
    print('    }')
    print('  }')
    print()
    print("=" * 70)

if __name__ == '__main__':
    test_font_config_loading()
    test_font_resolution()
    test_text_rendering_without_font_path()
    test_complete_slide_config()
    print_summary()
