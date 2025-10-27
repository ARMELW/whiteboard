#!/usr/bin/env python3
"""Simple test to verify arrow type layer is correctly processed."""

import sys
import json
import tempfile
import subprocess

def test_arrow_type_cli():
    """Test arrow type via CLI."""
    print("Testing arrow type via CLI...")
    
    # Create a simple test config
    config = {
        "slides": [
            {
                "index": 0,
                "duration": 2,
                "layers": [
                    {
                        "type": "arrow",
                        "arrow_config": {
                            "start": [200, 300],
                            "end": [600, 300],
                            "color": "#FF0000",
                            "fill_color": "#FFAAAA",
                            "stroke_width": 5,
                            "arrow_size": 40,
                            "duration": 1.5
                        },
                        "z_index": 1,
                        "mode": "draw"
                    }
                ]
            }
        ]
    }
    
    # Write to temp file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(config, f, indent=2)
        config_path = f.name
    
    print(f"  Config file: {config_path}")
    
    # Run whiteboard_animator
    cmd = [
        'python', 'whiteboard_animator.py',
        '--config', config_path,
        '--split-len', '15',
        '--frame-rate', '10'  # Low frame rate for fast test
    ]
    
    print(f"  Running: {' '.join(cmd)}")
    try:
        result = subprocess.run(
            cmd,
            cwd='/home/runner/work/whiteboard/whiteboard',
            capture_output=True,
            text=True,
            timeout=60
        )
        
        print("\n  STDOUT:")
        print("  " + "\n  ".join(result.stdout.split('\n')[-30:]))
        
        if result.returncode == 0:
            print("\n  ✓ CLI test passed!")
            return True
        else:
            print(f"\n  ✗ CLI test failed with return code {result.returncode}")
            if result.stderr:
                print("  STDERR:")
                print("  " + "\n  ".join(result.stderr.split('\n')))
            return False
    except subprocess.TimeoutExpired:
        print("  ✗ CLI test timed out")
        return False
    except Exception as e:
        print(f"  ✗ CLI test failed with exception: {e}")
        return False


def main():
    """Run CLI test."""
    print("=== Arrow Type CLI Test ===\n")
    
    result = test_arrow_type_cli()
    
    print("\n=== Test Result ===")
    if result:
        print("✓ CLI test passed!")
        return 0
    else:
        print("✗ CLI test failed")
        return 1


if __name__ == '__main__':
    sys.exit(main())
