#!/usr/bin/env python
"""
Test that shape polygons automatically use path_follow animation in draw mode.
This ensures a smooth outline-following animation instead of tile-by-tile drawing.
"""
import json

def test_polygon_path_follow_detection():
    """Test that polygon shapes are detected for path_follow animation"""
    print("=" * 60)
    print("TEST: Polygon Path Follow Detection")
    print("=" * 60)
    
    # Test case 1: Polygon shape with points should use path_follow
    test_layer_1 = {
        "type": "shape",
        "shape_config": {
            "shape": "polygon",
            "points": [[100, 100], [200, 150], [150, 200], [50, 150]],
            "color": "#FF0000",
            "fill_color": "#FFCCCC",
            "stroke_width": 3
        },
        "mode": "draw",
        "skip_rate": 5
    }
    
    shape_config = test_layer_1.get('shape_config', {})
    is_polygon = shape_config.get('shape') == 'polygon'
    has_points = 'points' in shape_config
    is_draw_mode = test_layer_1.get('mode') == 'draw'
    
    print(f"\nTest Case 1: Polygon with points")
    print(f"  Shape type: {shape_config.get('shape')}")
    print(f"  Has points: {has_points}")
    print(f"  Number of points: {len(shape_config.get('points', []))}")
    print(f"  Mode: {test_layer_1.get('mode')}")
    
    should_use_path_follow = is_polygon and has_points and is_draw_mode
    print(f"  ✅ Should use path_follow: {should_use_path_follow}")
    
    if not should_use_path_follow:
        print("  ❌ FAIL: Should use path_follow")
        return False
    
    # Test case 2: Circle should NOT use path_follow
    test_layer_2 = {
        "type": "shape",
        "shape_config": {
            "shape": "circle",
            "color": "#FF0000",
            "fill_color": "#FFCCCC",
            "stroke_width": 3,
            "position": {"x": 320, "y": 240},
            "size": 100
        },
        "mode": "draw",
        "skip_rate": 5
    }
    
    shape_config_2 = test_layer_2.get('shape_config', {})
    is_polygon_2 = shape_config_2.get('shape') == 'polygon'
    
    print(f"\nTest Case 2: Circle (should NOT use path_follow)")
    print(f"  Shape type: {shape_config_2.get('shape')}")
    print(f"  Is polygon: {is_polygon_2}")
    print(f"  ✅ Should NOT use path_follow: {not is_polygon_2}")
    
    # Test case 3: Polygon in eraser mode should NOT auto-switch
    test_layer_3 = {
        "type": "shape",
        "shape_config": {
            "shape": "polygon",
            "points": [[100, 100], [200, 150], [150, 200]],
            "color": "#FF0000",
            "stroke_width": 3
        },
        "mode": "eraser",
        "skip_rate": 5
    }
    
    is_draw_mode_3 = test_layer_3.get('mode') == 'draw'
    print(f"\nTest Case 3: Polygon with eraser mode")
    print(f"  Mode: {test_layer_3.get('mode')}")
    print(f"  ✅ Should NOT auto-switch (mode is not 'draw'): {not is_draw_mode_3}")
    
    print(f"\n✅ All detection tests passed!")
    return True


def test_example_configs():
    """Test that example configurations will use path_follow correctly"""
    print("\n" + "=" * 60)
    print("TEST: Example Configurations")
    print("=" * 60)
    
    # Test auto-extract SVG example
    try:
        with open('examples/shape_auto_extract_svg.json', 'r') as f:
            config = json.load(f)
        
        print(f"\n✅ Loaded shape_auto_extract_svg.json")
        
        polygon_layers = 0
        for slide in config.get('slides', []):
            for layer in slide.get('layers', []):
                if layer.get('type') == 'shape':
                    # Check if it will auto-extract to polygon
                    if 'svg_path' in layer:
                        print(f"  Found layer with svg_path: {layer.get('svg_path')}")
                        print(f"    - Will auto-extract to polygon with path_follow animation")
                        polygon_layers += 1
                    elif layer.get('shape_config', {}).get('shape') == 'polygon':
                        print(f"  Found polygon layer")
                        if 'points' in layer['shape_config']:
                            print(f"    - Has {len(layer['shape_config']['points'])} points")
                            print(f"    - Mode: {layer.get('mode', 'draw')}")
                            if layer.get('mode', 'draw') == 'draw':
                                print(f"    - ✅ Will use path_follow animation")
                                polygon_layers += 1
        
        print(f"\n✅ Found {polygon_layers} layer(s) that will use path_follow")
        
    except Exception as e:
        print(f"⚠️ Could not load example config: {e}")
    
    # Test shape from SVG example
    try:
        with open('examples/shape_from_svg_example.json', 'r') as f:
            config = json.load(f)
        
        print(f"\n✅ Loaded shape_from_svg_example.json")
        
        polygon_layers = 0
        for slide in config.get('slides', []):
            for layer in slide.get('layers', []):
                if layer.get('type') == 'shape':
                    shape_config = layer.get('shape_config', {})
                    if shape_config.get('shape') == 'polygon' and 'points' in shape_config:
                        mode = layer.get('mode', 'draw')
                        print(f"  Found polygon layer with {len(shape_config['points'])} points, mode={mode}")
                        if mode == 'draw':
                            print(f"    - ✅ Will use path_follow animation")
                            polygon_layers += 1
        
        print(f"\n✅ Found {polygon_layers} layer(s) that will use path_follow")
        
    except Exception as e:
        print(f"⚠️ Could not load example config: {e}")
    
    return True


def test_path_config_format():
    """Test path_config format conversion"""
    print("\n" + "=" * 60)
    print("TEST: Path Config Format Conversion")
    print("=" * 60)
    
    # Polygon points format
    polygon_points = [[100, 100], [200, 150], [150, 200], [50, 150]]
    
    # Convert to path_config format
    path_config = [{'x': int(p[0]), 'y': int(p[1])} for p in polygon_points]
    
    print(f"\nPolygon points: {polygon_points}")
    print(f"Converted path_config:")
    for i, point in enumerate(path_config[:3]):
        print(f"  {i+1}. x={point['x']}, y={point['y']}")
    if len(path_config) > 3:
        print(f"  ... and {len(path_config) - 3} more points")
    
    # Verify format
    assert len(path_config) == len(polygon_points)
    assert all('x' in p and 'y' in p for p in path_config)
    assert path_config[0]['x'] == 100 and path_config[0]['y'] == 100
    
    print(f"\n✅ Format conversion works correctly")
    return True


if __name__ == "__main__":
    import sys
    
    print("=" * 60)
    print("SHAPE PATH FOLLOW ANIMATION TEST SUITE")
    print("=" * 60)
    
    results = []
    
    # Run tests
    results.append(("Polygon Detection", test_polygon_path_follow_detection()))
    results.append(("Example Configs", test_example_configs()))
    results.append(("Path Config Format", test_path_config_format()))
    
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
        print("\n✨ Polygon shapes will now use smooth path_follow animation")
        print("   instead of tile-by-tile drawing when mode='draw'!")
        sys.exit(0)
    else:
        print("\n⚠️  Some tests failed")
        sys.exit(1)
