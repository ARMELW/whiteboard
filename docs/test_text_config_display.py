#!/usr/bin/env python3
"""Test that text layer config is displayed in console output."""

import sys
import os
from io import StringIO
from contextlib import redirect_stdout

sys.path.insert(0, os.path.dirname(__file__))

from whiteboard_animator import compose_layers

def test_text_config_display_in_output():
    """Test that text config details are shown in console output."""
    print("Testing text config display in console output...")
    
    # Create a text layer with specific config
    layers_config = [
        {
            'type': 'text',
            'z_index': 1,
            'text_config': {
                'text': 'Hello World',
                'font': 'DejaVuSans',
                'size': 48,
                'color': [255, 0, 0],  # RGB Red
                'style': 'bold',
                'align': 'center'
            }
        }
    ]
    
    # Capture stdout
    captured_output = StringIO()
    try:
        with redirect_stdout(captured_output):
            result = compose_layers(layers_config, 800, 600)
        
        output = captured_output.getvalue()
        print("Captured output:")
        print(output)
        print()
        
        # Check that all config details are in the output
        checks = {
            'font:DejaVuSans': 'font name' in output and 'DejaVuSans' in output,
            'size:48': 'size:48' in output or 'size: 48' in output,
            'color': 'color' in output.lower(),
            'style:bold': 'bold' in output.lower(),
            'align:center': 'center' in output.lower()
        }
        
        print("Config details check:")
        all_passed = True
        for check_name, passed in checks.items():
            status = "✓" if passed else "✗"
            print(f"  {status} {check_name}")
            if not passed:
                all_passed = False
        
        if all_passed:
            print("\n✓ All text config details are displayed")
            return True
        else:
            print("\n✗ Some text config details are missing")
            return False
            
    except Exception as e:
        print(f"✗ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_multiple_text_layers_config_display():
    """Test that multiple text layers show their individual configs."""
    print("Testing multiple text layers with different configs...")
    
    layers_config = [
        {
            'type': 'text',
            'z_index': 1,
            'text_config': {
                'text': 'Red Text',
                'font': 'Arial',
                'size': 36,
                'color': [255, 0, 0],
                'style': 'normal'
            }
        },
        {
            'type': 'text',
            'z_index': 2,
            'text_config': {
                'text': 'Blue Text',
                'font': 'DejaVuSans',
                'size': 52,
                'color': [0, 0, 255],
                'style': 'bold'
            }
        }
    ]
    
    # Capture stdout
    captured_output = StringIO()
    try:
        with redirect_stdout(captured_output):
            result = compose_layers(layers_config, 800, 600)
        
        output = captured_output.getvalue()
        print("Captured output:")
        print(output)
        print()
        
        # Check that both configs are shown
        has_arial = 'Arial' in output
        has_dejavu = 'DejaVuSans' in output
        has_size_36 = '36' in output
        has_size_52 = '52' in output
        
        print("Multiple layer check:")
        print(f"  {'✓' if has_arial else '✗'} Arial font mentioned")
        print(f"  {'✓' if has_dejavu else '✗'} DejaVuSans font mentioned")
        print(f"  {'✓' if has_size_36 else '✗'} Size 36 mentioned")
        print(f"  {'✓' if has_size_52 else '✗'} Size 52 mentioned")
        
        if has_arial and has_dejavu and has_size_36 and has_size_52:
            print("\n✓ Both text layers show their individual configs")
            return True
        else:
            print("\n✗ Not all layer configs are shown")
            return False
            
    except Exception as e:
        print(f"✗ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("Text Config Display Tests")
    print("=" * 60)
    print()
    
    tests = [
        test_text_config_display_in_output,
        test_multiple_text_layers_config_display
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
