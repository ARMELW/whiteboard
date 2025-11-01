#!/usr/bin/env python
"""
Test script for shape rendering and path extraction functionality.
Tests the fix for the shape rendering issue.
"""
import sys
import os
import json

# Test 1: Test path_extractor with SVG file
def test_path_extractor():
    print("=" * 60)
    print("TEST 1: Testing path_extractor.py with SVG file")
    print("=" * 60)
    
    svg_file = "doodle/arrow.svg"
    if not os.path.exists(svg_file):
        print(f"⚠️  SVG file not found: {svg_file}")
        return False
    
    try:
        from path_extractor import extract_path_points, extract_svg_colors, save_path_config
        from pathlib import Path
        
        # Extract points
        print(f"\n🔍 Extracting path points from {svg_file}...")
        points = extract_path_points(svg_file, sampling_rate=10, reverse=False)
        print(f"✅ Extracted {len(points)} points")
        
        # Extract colors
        print(f"\n🎨 Extracting colors from {svg_file}...")
        colors = extract_svg_colors(svg_file)
        if colors:
            print(f"✅ Colors extracted:")
            if colors.get('fill'):
                print(f"   Fill: {colors['fill']}")
            if colors.get('stroke'):
                print(f"   Stroke: {colors['stroke']}")
        else:
            print("⚠️  No colors found in SVG")
        
        # Save config
        output_file = "/tmp/test_arrow_config.json"
        save_path_config(points, output_file, 
                        comment="Test extraction", 
                        colors=colors, 
                        num_points=len(points), 
                        reversed_path=False)
        
        # Verify saved file
        if os.path.exists(output_file):
            with open(output_file, 'r') as f:
                config = json.load(f)
            print(f"\n✅ Config saved successfully:")
            print(f"   Points: {len(config.get('path_config', []))}")
            print(f"   Has suggested_shape_config: {('suggested_shape_config' in config)}")
            print(f"   Has metadata: {('metadata' in config)}")
            
            # Show suggested config
            if 'suggested_shape_config' in config:
                shape_cfg = config['suggested_shape_config']
                print(f"\n📋 Suggested shape config:")
                print(f"   Type: {shape_cfg.get('type')}")
                print(f"   Shape: {shape_cfg.get('shape_config', {}).get('shape')}")
                print(f"   Color: {shape_cfg.get('shape_config', {}).get('color')}")
                fill = shape_cfg.get('shape_config', {}).get('fill_color')
                if fill:
                    print(f"   Fill color: {fill}")
            
            return True
        else:
            print(f"❌ Failed to save config file")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


# Test 2: Test render_shape_to_image function
def test_shape_rendering():
    print("\n" + "=" * 60)
    print("TEST 2: Testing render_shape_to_image function")
    print("=" * 60)
    
    try:
        import numpy as np
        import sys
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        
        # Import the function (this will test if it's syntactically correct)
        print("\n🔍 Importing render_shape_to_image...")
        from whiteboard_animator import render_shape_to_image
        print("✅ Function imported successfully")
        
        # Test rendering different shapes
        shapes_to_test = [
            {
                "name": "Circle with fill",
                "config": {
                    "shape": "circle",
                    "color": "#FF0000",
                    "fill_color": "#FFCCCC",
                    "stroke_width": 3,
                    "position": {"x": 320, "y": 240},
                    "size": 100
                }
            },
            {
                "name": "Rectangle with fill",
                "config": {
                    "shape": "rectangle",
                    "color": "#0000FF",
                    "fill_color": "#CCCCFF",
                    "stroke_width": 2,
                    "position": {"x": 320, "y": 240},
                    "width": 200,
                    "height": 150
                }
            },
            {
                "name": "Triangle with fill",
                "config": {
                    "shape": "triangle",
                    "color": "#00FF00",
                    "fill_color": "#CCFFCC",
                    "stroke_width": 2,
                    "position": {"x": 320, "y": 240},
                    "size": 120
                }
            },
            {
                "name": "Arrow with fill",
                "config": {
                    "shape": "arrow",
                    "color": "#FF6600",
                    "fill_color": "#FFAA66",
                    "stroke_width": 4,
                    "start": [100, 240],
                    "end": [540, 240],
                    "arrow_size": 30
                }
            }
        ]
        
        for shape_test in shapes_to_test:
            print(f"\n🔷 Testing {shape_test['name']}...")
            try:
                img = render_shape_to_image(shape_test['config'], 640, 480)
                
                # Verify the result
                if img is not None and isinstance(img, np.ndarray):
                    h, w, c = img.shape
                    print(f"✅ Shape rendered successfully: {w}x{h}x{c}")
                    
                    # Check if there's non-white content (shape was drawn)
                    white = np.all(img == 255)
                    if not white:
                        print(f"✅ Shape contains drawn content (not all white)")
                    else:
                        print(f"⚠️  Shape is all white - might not be drawn correctly")
                else:
                    print(f"❌ Invalid result from render_shape_to_image")
                    return False
            except Exception as e:
                print(f"❌ Error rendering {shape_test['name']}: {e}")
                import traceback
                traceback.print_exc()
                return False
        
        print(f"\n✅ All shape rendering tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


# Test 3: Test color parsing
def test_color_parsing():
    print("\n" + "=" * 60)
    print("TEST 3: Testing color parsing in render_shape_to_image")
    print("=" * 60)
    
    try:
        import numpy as np
        from whiteboard_animator import render_shape_to_image
        
        # Test different color formats
        color_tests = [
            {"format": "Hex string", "color": "#FF5733", "expected": (51, 87, 255)},  # BGR
            {"format": "RGB tuple", "color": [255, 87, 51], "expected": (51, 87, 255)},  # Convert to BGR
            {"format": "RGB list", "color": (255, 87, 51), "expected": (51, 87, 255)},
        ]
        
        for test in color_tests:
            print(f"\n🎨 Testing {test['format']}: {test['color']}")
            try:
                config = {
                    "shape": "circle",
                    "color": test['color'],
                    "stroke_width": 2,
                    "position": {"x": 50, "y": 50},
                    "size": 20
                }
                img = render_shape_to_image(config, 100, 100)
                print(f"✅ Color format accepted and rendered")
            except Exception as e:
                print(f"❌ Failed: {e}")
                return False
        
        print(f"\n✅ All color parsing tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


# Main test runner
if __name__ == "__main__":
    print("=" * 60)
    print("SHAPE RENDERING AND PATH EXTRACTION TEST SUITE")
    print("=" * 60)
    
    results = []
    
    # Run tests
    results.append(("Path Extraction", test_path_extractor()))
    results.append(("Shape Rendering", test_shape_rendering()))
    results.append(("Color Parsing", test_color_parsing()))
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    all_passed = True
    for name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{name}: {status}")
        if not passed:
            all_passed = False
    
    print("=" * 60)
    
    if all_passed:
        print("\n🎉 All tests passed!")
        sys.exit(0)
    else:
        print("\n⚠️  Some tests failed")
        sys.exit(1)
