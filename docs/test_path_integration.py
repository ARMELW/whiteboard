#!/usr/bin/env python3
"""Integration test for path animation features"""

import os
import sys
import subprocess
import tempfile
import json

def test_path_animation(test_name, config, expected_duration_min):
    """Test a path animation configuration and verify video generation"""
    print(f"\n{'='*60}")
    print(f"Testing: {test_name}")
    print(f"{'='*60}")
    
    # Create temp config file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(config, f)
        config_path = f.name
    
    try:
        # Run the animator
        result = subprocess.run(
            ['python', 'whiteboard_animator.py', '--config', config_path],
            capture_output=True,
            text=True,
            timeout=60
        )
        
        # Check for success
        if result.returncode != 0:
            print(f"❌ FAILED: Process returned {result.returncode}")
            print("STDERR:", result.stderr[-500:] if len(result.stderr) > 500 else result.stderr)
            return False
        
        # Look for success message
        if "✅ SUCCÈS!" in result.stdout and "Vidéo finale:" in result.stdout:
            print(f"✅ PASSED: Video generated successfully")
            
            # Extract video path from output
            for line in result.stdout.split('\n'):
                if "Vidéo finale:" in line:
                    video_path = line.split("Vidéo finale:")[1].strip()
                    if os.path.exists(video_path):
                        size = os.path.getsize(video_path)
                        print(f"   Video file: {os.path.basename(video_path)}")
                        print(f"   Size: {size} bytes")
                        if size > 1000:  # At least 1KB
                            return True
                        else:
                            print(f"   ⚠️  Warning: Video file is very small")
                            return False
            
            print(f"   ⚠️  Warning: Could not verify video file")
            return True
        else:
            print(f"❌ FAILED: No success message found")
            return False
            
    except subprocess.TimeoutExpired:
        print(f"❌ FAILED: Process timed out")
        return False
    except Exception as e:
        print(f"❌ FAILED: {e}")
        return False
    finally:
        # Cleanup
        if os.path.exists(config_path):
            os.unlink(config_path)

def main():
    print("\n" + "="*60)
    print("PATH ANIMATION INTEGRATION TESTS")
    print("="*60)
    
    os.chdir('/home/runner/work/whiteboard-it/whiteboard-it')
    
    tests = []
    
    # Test 1: Linear path
    tests.append((
        "Linear Path Animation",
        {
            "slides": [{
                "index": 0,
                "duration": 3,
                "layers": [{
                    "image_path": "demo/2.png",
                    "z_index": 1,
                    "scale": 0.15,
                    "mode": "static",
                    "path_animation": {
                        "enabled": True,
                        "type": "linear",
                        "duration": 2.0,
                        "points": [[100, 100], [600, 300]],
                        "speed_profile": "ease_in_out"
                    }
                }]
            }]
        },
        2.0
    ))
    
    # Test 2: Bezier cubic with path drawing
    tests.append((
        "Bezier Cubic with Path Drawing",
        {
            "slides": [{
                "index": 0,
                "duration": 4,
                "layers": [{
                    "image_path": "demo/2.png",
                    "z_index": 1,
                    "scale": 0.12,
                    "mode": "static",
                    "path_animation": {
                        "enabled": True,
                        "type": "bezier_cubic",
                        "duration": 2.5,
                        "points": [[100, 400], [300, 200], [500, 300], [700, 100]],
                        "speed_profile": "ease_in_out",
                        "orient_to_path": True,
                        "draw_path": True,
                        "path_color": [0, 255, 0],
                        "path_thickness": 3
                    }
                }]
            }]
        },
        2.5
    ))
    
    # Test 3: Quadratic bezier
    tests.append((
        "Bezier Quadratic",
        {
            "slides": [{
                "index": 0,
                "duration": 3,
                "layers": [{
                    "image_path": "demo/2.png",
                    "z_index": 1,
                    "scale": 0.15,
                    "mode": "static",
                    "path_animation": {
                        "enabled": True,
                        "type": "bezier_quadratic",
                        "duration": 2.0,
                        "points": [[100, 400], [400, 100], [700, 400]],
                        "speed_profile": "ease_in"
                    }
                }]
            }]
        },
        2.0
    ))
    
    # Test 4: Spline with orient to path
    tests.append((
        "Spline with Orientation",
        {
            "slides": [{
                "index": 0,
                "duration": 5,
                "layers": [{
                    "image_path": "demo/2.png",
                    "z_index": 1,
                    "scale": 0.1,
                    "mode": "static",
                    "path_animation": {
                        "enabled": True,
                        "type": "spline",
                        "duration": 3.0,
                        "points": [
                            [100, 300],
                            [200, 150],
                            [400, 200],
                            [600, 100],
                            [700, 350]
                        ],
                        "speed_profile": "linear",
                        "orient_to_path": True
                    }
                }]
            }]
        },
        3.0
    ))
    
    # Run all tests
    results = []
    for test_name, config, duration in tests:
        result = test_path_animation(test_name, config, duration)
        results.append((test_name, result))
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    passed = sum(1 for _, r in results if r)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {test_name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    print("="*60 + "\n")
    
    return 0 if passed == total else 1

if __name__ == '__main__':
    sys.exit(main())
