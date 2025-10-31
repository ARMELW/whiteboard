#!/usr/bin/env python3
"""Test to reproduce the bug where config variables are undefined."""

import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from whiteboard_animator import compose_layers

def test_text_layer_after_image_layer():
    """Test that text layer works even when it comes after an image layer."""
    print("Testing text layer after image layer...")
    
    # Create a configuration with an image layer first, then a text layer
    layers_config = [
        {
            'type': 'image',
            'z_index': 1,
            'image_path': '1.jpg',  # Use an existing image from the repo
            'scale': 0.5
        },
        {
            'type': 'text',
            'z_index': 2,
            'text_config': {
                'text': 'Test Text',
                'font': 'DejaVuSans',
                'size': 48,
                'color': [255, 0, 0],  # RGB
                'position': {'x': 100, 'y': 100}
            }
        }
    ]
    
    try:
        result = compose_layers(layers_config, 800, 600)
        print("✓ Text layer after image layer works")
        return True
    except NameError as e:
        print(f"✗ NameError occurred: {e}")
        return False
    except Exception as e:
        print(f"✗ Other error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_shape_layer_first():
    """Test that shape layer description works when it's the first layer."""
    print("\nTesting shape layer as first layer...")
    
    layers_config = [
        {
            'type': 'shape',
            'z_index': 1,
            'shape_config': {
                'shape': 'circle',
                'radius': 50,
                'color': [255, 0, 0],
                'position': {'x': 400, 'y': 300}
            }
        }
    ]
    
    try:
        result = compose_layers(layers_config, 800, 600)
        print("✓ Shape layer as first layer works")
        return True
    except NameError as e:
        print(f"✗ NameError occurred: {e}")
        return False
    except Exception as e:
        print(f"✗ Other error: {e}")
        return False

def test_text_layer_first():
    """Test that text layer works when it's the first layer."""
    print("\nTesting text layer as first layer...")
    
    layers_config = [
        {
            'type': 'text',
            'z_index': 1,
            'text_config': {
                'text': 'First Text',
                'font': 'DejaVuSans',
                'size': 48,
                'color': [255, 0, 0]
            }
        }
    ]
    
    try:
        result = compose_layers(layers_config, 800, 600)
        print("✓ Text layer as first layer works")
        return True
    except NameError as e:
        print(f"✗ NameError occurred: {e}")
        return False
    except Exception as e:
        print(f"✗ Other error: {e}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("Config Variable Scope Bug Tests")
    print("=" * 60)
    
    tests = [
        test_text_layer_first,
        test_shape_layer_first,
        test_text_layer_after_image_layer
    ]
    
    results = []
    for test in tests:
        try:
            results.append(test())
        except Exception as e:
            print(f"✗ Test crashed: {e}")
            results.append(False)
        print()
    
    print("=" * 60)
    passed = sum(results)
    total = len(results)
    print(f"Results: {passed}/{total} tests passed")
    print("=" * 60)
    
    sys.exit(0 if all(results) else 1)
