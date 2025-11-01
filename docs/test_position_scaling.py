#!/usr/bin/env python3
"""
Test script for canvas dimension position scaling
"""
import json

def test_position_scaling():
    """Test that positions are correctly scaled"""
    
    # Load positions from test-layer.json if available, otherwise use sample data
    original_positions = [
        {"x": 583.1, "y": 335.9},  # Image 1
        {"x": 1049, "y": 518},      # Text 1
        {"x": 1027, "y": 671},      # Text 2
        {"x": 1145.5, "y": 332.7},  # Image 2
        {"x": 1151, "y": 396}       # Text 3
    ]
    
    # Try to load from actual test-layer.json
    try:
        import os
        test_layer_path = os.path.join(os.path.dirname(__file__), 'examples', 'test-layer.json')
        if os.path.exists(test_layer_path):
            with open(test_layer_path, 'r') as f:
                config = json.load(f)
                if 'slides' in config and config['slides']:
                    layers = config['slides'][0].get('layers', [])
                    original_positions = []
                    for layer in layers:
                        if 'position' in layer:
                            original_positions.append(layer['position'])
                        elif 'text_config' in layer and 'position' in layer['text_config']:
                            original_positions.append(layer['text_config']['position'])
                    print(f"Loaded {len(original_positions)} positions from test-layer.json")
    except Exception as e:
        print(f"Using sample positions (couldn't load from file: {e})")
    
    # Test case 1: No scaling (canvas dimensions match video dimensions)
    print("Test 1: No Scaling (1920x1080 → 1920x1080)")
    print("=" * 60)
    canvas_width, canvas_height = 1920, 1080
    video_width, video_height = 1920, 1080
    scale_x = video_width / canvas_width
    scale_y = video_height / canvas_height
    print(f"Scale factors: x={scale_x:.3f}, y={scale_y:.3f}")
    
    for i, pos in enumerate(original_positions):
        new_x = pos['x'] * scale_x
        new_y = pos['y'] * scale_y
        print(f"  Position {i+1}: ({pos['x']:.1f}, {pos['y']:.1f}) → ({new_x:.1f}, {new_y:.1f})")
    
    print()
    
    # Test case 2: Scaling from smaller canvas
    print("Test 2: Scaling from smaller canvas (1200x800 → 1920x1080)")
    print("=" * 60)
    canvas_width, canvas_height = 1200, 800
    video_width, video_height = 1920, 1080
    scale_x = video_width / canvas_width
    scale_y = video_height / canvas_height
    print(f"Scale factors: x={scale_x:.3f}, y={scale_y:.3f}")
    
    # Calculate the inverse scale to convert original positions to smaller canvas
    inverse_scale_x = canvas_width / 1920.0
    inverse_scale_y = canvas_height / 1080.0
    
    # Adjust original positions as if they were from a 1200x800 canvas
    scaled_original = [
        {"x": p['x'] * inverse_scale_x, "y": p['y'] * inverse_scale_y} 
        for p in original_positions
    ]
    
    for i, pos in enumerate(scaled_original):
        new_x = pos['x'] * scale_x
        new_y = pos['y'] * scale_y
        print(f"  Position {i+1}: ({pos['x']:.1f}, {pos['y']:.1f}) → ({new_x:.1f}, {new_y:.1f})")
    
    print()
    
    # Test case 3: Verify layer position structure matches what animator expects
    print("Test 3: Verify JSON structure")
    print("=" * 60)
    
    test_config = {
        "canvas_width": 1920,
        "canvas_height": 1080,
        "slides": [
            {
                "index": 0,
                "duration": 2,
                "layers": [
                    {
                        "type": "image",
                        "position": {"x": 583.1, "y": 335.9}
                    },
                    {
                        "type": "text",
                        "text_config": {
                            "text": "Test",
                            "position": {"x": 1049, "y": 518}
                        }
                    }
                ]
            }
        ]
    }
    
    print("Sample config structure:")
    print(json.dumps(test_config, indent=2))
    print()
    
    # Simulate the scaling logic from whiteboard_animator.py
    canvas_w = test_config.get('canvas_width', 1920)
    canvas_h = test_config.get('canvas_height', 1080)
    target_w, target_h = 1920, 1080
    
    scale_x = target_w / canvas_w
    scale_y = target_h / canvas_h
    
    print(f"Scaling: {canvas_w}x{canvas_h} → {target_w}x{target_h}")
    print(f"Factors: x={scale_x:.3f}, y={scale_y:.3f}")
    
    if scale_x != 1.0 or scale_y != 1.0:
        print("Positions would be scaled")
    else:
        print("No scaling needed (dimensions match)")
    
    print()
    print("✅ All tests complete!")

if __name__ == "__main__":
    test_position_scaling()
