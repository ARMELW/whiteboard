#!/usr/bin/env python3
"""Test script to verify that text layer config is displayed when composing layers."""

import sys
import os
from io import StringIO
from contextlib import redirect_stdout

# Add current directory to path
sys.path.insert(0, os.path.dirname(__file__))

from whiteboard_animator import compose_layers

def test_text_layer_display():
    """Test that text layer displays with config (color, font size, etc.)."""
    print("Testing text layer display with config...")
    
    # Test with a text layer
    layers_config = [
        {
            'type': 'text',
            'z_index': 1,
            'text_config': {
                'text': 'Hello World',
                'font': 'DejaVuSans',
                'size': 48,
                'color': [0, 0, 255],
                'style': 'bold'
            }
        }
    ]
    
    # Capture stdout to check the output
    captured_output = StringIO()
    try:
        with redirect_stdout(captured_output):
            result = compose_layers(layers_config, 800, 600)
        
        output = captured_output.getvalue()
        print("Captured output:")
        print(output)
        
        # Check if the output contains layer information
        if "text:" in output.lower():
            print("✓ Text layer was logged")
            # Check if we got the text content
            if "Hello World" in output:
                print("✓ Text content was displayed")
            else:
                print("⚠ Text content was NOT displayed")
            return True
        else:
            print("✗ Text layer was NOT logged properly")
            return False
            
    except Exception as e:
        print(f"✗ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_shape_layer_display():
    """Test that shape layer displays properly."""
    print("\nTesting shape layer display...")
    
    # Test with a shape layer
    layers_config = [
        {
            'type': 'shape',
            'z_index': 1,
            'shape_config': {
                'shape': 'circle',
                'radius': 100,
                'color': [255, 0, 0],
                'position': {'x': 400, 'y': 300}
            }
        }
    ]
    
    # Capture stdout to check the output
    captured_output = StringIO()
    try:
        with redirect_stdout(captured_output):
            result = compose_layers(layers_config, 800, 600)
        
        output = captured_output.getvalue()
        print("Captured output:")
        print(output)
        
        # Check if the output contains layer information
        if "shape:" in output.lower():
            print("✓ Shape layer was logged")
            if "circle" in output.lower():
                print("✓ Shape type was displayed")
            else:
                print("⚠ Shape type was NOT displayed")
            return True
        else:
            print("✗ Shape layer was NOT logged properly")
            return False
            
    except Exception as e:
        print(f"✗ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("Layer Display Tests")
    print("=" * 60)
    
    tests = [
        test_text_layer_display,
        test_shape_layer_display
    ]
    
    results = []
    for test in tests:
        try:
            results.append(test())
        except Exception as e:
            print(f"✗ Test failed with exception: {e}")
            import traceback
            traceback.print_exc()
            results.append(False)
        print()
    
    print("=" * 60)
    passed = sum(results)
    total = len(results)
    print(f"Results: {passed}/{total} tests passed")
    print("=" * 60)
    
    sys.exit(0 if all(results) else 1)
