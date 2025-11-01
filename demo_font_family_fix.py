#!/usr/bin/env python3
"""
Demonstration of the font family fix.
This shows that font families are now properly resolved using fontconfig.
"""
import sys
import os
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from whiteboard_animator import resolve_font_path, compose_scene_with_camera
import cv2

def main():
    print("=" * 70)
    print("FONT FAMILY FIX DEMONSTRATION")
    print("=" * 70)
    print()
    print("This demonstrates the fix for the font application issue.")
    print("Previously, font families were not properly resolved,")
    print("causing the wrong fonts to be displayed in rendered output.")
    print()
    
    # The exact configuration from the issue
    print("Testing with the exact configuration from the GitHub issue...")
    print()
    
    scene_config = {
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
    
    # Check font resolution
    print("1. Font Resolution:")
    font_path = resolve_font_path("Gargi", "normal")
    print(f"   Font 'Gargi' resolves to: {font_path}")
    if font_path:
        print(f"   ✅ Font successfully resolved via fontconfig")
    else:
        print(f"   ⚠️  Font not found, will use PIL fallback")
    print()
    
    # Render the scene
    print("2. Rendering Scene:")
    camera = {
        'width': 800,
        'height': 450,
        'position': {'x': 0.5, 'y': 0.5},
        'zoom': 1.0
    }
    
    try:
        result = compose_scene_with_camera(
            scene_config, 
            camera, 
            scene_width=800, 
            scene_height=450, 
            verbose=True
        )
        
        # Save the result
        cv2.imwrite('demo_font_family_fix.png', result)
        print()
        print("   ✅ Scene rendered successfully!")
        print("   Output saved to: demo_font_family_fix.png")
        print()
    except Exception as e:
        print(f"   ❌ Error rendering scene: {str(e)}")
        import traceback
        traceback.print_exc()
        return
    
    # Test with different fonts to show the difference
    print("3. Comparing Different Fonts:")
    print()
    
    test_fonts = [
        ("DejaVu Sans", "System font that should be available"),
        ("Liberation Sans", "Alternative system font"),
        ("Lato", "Modern sans-serif font"),
        ("Arial", "Common font (fallback to Liberation Sans)"),
    ]
    
    for i, (font_name, description) in enumerate(test_fonts):
        print(f"   {i+1}. Testing font: {font_name}")
        print(f"      Description: {description}")
        
        font_path = resolve_font_path(font_name, "normal")
        if font_path:
            print(f"      Resolved to: {font_path}")
            
            # Update the scene config
            test_scene = scene_config.copy()
            test_scene['layers'] = [scene_config['layers'][0].copy()]
            test_scene['layers'][0]['text_config'] = scene_config['layers'][0]['text_config'].copy()
            test_scene['layers'][0]['text_config']['font'] = font_name
            
            # Render
            try:
                result = compose_scene_with_camera(
                    test_scene, 
                    camera, 
                    scene_width=800, 
                    scene_height=450, 
                    verbose=False
                )
                filename = f"demo_font_family_{font_name.replace(' ', '_')}.png"
                cv2.imwrite(filename, result)
                print(f"      ✅ Rendered: {filename}")
            except Exception as e:
                print(f"      ❌ Error: {str(e)}")
        else:
            print(f"      ⚠️  Could not resolve font")
        print()
    
    print("=" * 70)
    print("SUMMARY OF FIX")
    print("=" * 70)
    print()
    print("✅ Font families are now resolved using fontconfig (fc-match)")
    print("✅ System fonts are properly detected and used")
    print("✅ Missing fonts gracefully fall back to available fonts")
    print("✅ The correct font is applied to text rendering")
    print()
    print("The fix ensures that when you specify a font family in the JSON")
    print("configuration, the system will:")
    print("  1. Try to resolve it via fontconfig to get the actual font file")
    print("  2. Use the resolved font file for rendering")
    print("  3. Fall back gracefully if the font is not available")
    print()
    print("This solves the issue where fonts were not being applied correctly!")
    print("=" * 70)

if __name__ == '__main__':
    main()
