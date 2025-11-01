#!/usr/bin/env python3
"""Test script for coloriage (coloring) mode feature."""

import sys
import os
import cv2
import numpy as np
import json
import subprocess

def create_colorful_test_image():
    """Create a colorful test image for coloriage demo."""
    # Create a white canvas
    canvas = np.ones((400, 600, 3), dtype=np.uint8) * 255
    
    # Draw colorful shapes
    # Red circle
    cv2.circle(canvas, (150, 150), 60, (0, 0, 255), -1)
    
    # Blue rectangle
    cv2.rectangle(canvas, (300, 80), (500, 220), (255, 0, 0), -1)
    
    # Green triangle
    pts = np.array([[250, 250], [350, 380], [150, 380]], np.int32)
    cv2.fillPoly(canvas, [pts], (0, 255, 0))
    
    # Yellow star
    star_pts = []
    for i in range(5):
        angle = i * 144 * np.pi / 180
        outer_x = int(480 + 50 * np.cos(angle - np.pi/2))
        outer_y = int(320 + 50 * np.sin(angle - np.pi/2))
        star_pts.append([outer_x, outer_y])
        
        angle2 = (i * 144 + 72) * np.pi / 180
        inner_x = int(480 + 25 * np.cos(angle2 - np.pi/2))
        inner_y = int(320 + 25 * np.sin(angle2 - np.pi/2))
        star_pts.append([inner_x, inner_y])
    
    star_pts = np.array(star_pts, np.int32)
    cv2.fillPoly(canvas, [star_pts], (0, 255, 255))
    
    # Save the test image
    test_image_path = "/tmp/test_coloriage_input.png"
    cv2.imwrite(test_image_path, canvas)
    print(f"✓ Created colorful test image: {test_image_path}")
    
    return test_image_path


def test_coloriage_mode():
    """Test coloriage mode with a colorful configuration."""
    print("\n=== Testing Coloriage Mode ===\n")
    
    # Create colorful test image
    test_image_path = create_colorful_test_image()
    
    # Create test configuration
    config = {
        "output_video": "/tmp/test_coloriage_output.mp4",
        "fps": 30,
        "slides": [
            {
                "index": 0,
                "duration": 4,
                "skip_rate": 5,
                "layers": [
                    {
                        "image_path": test_image_path,
                        "position": {"x": 0, "y": 0},
                        "z_index": 1,
                        "skip_rate": 3,
                        "mode": "coloriage"
                    }
                ]
            }
        ]
    }
    
    config_path = "/tmp/test_coloriage_config.json"
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=2)
    
    print(f"✓ Created test config: {config_path}")
    
    # Run whiteboard animator with the test config
    print("\n▶️  Running whiteboard animator with coloriage mode...")
    # Get the script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    animator_script = os.path.join(script_dir, "whiteboard_animator.py")
    cmd = f"{sys.executable} {animator_script} --config {config_path}"
    
    import subprocess
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    
    if result.returncode == 0:
        output_video = "/tmp/test_coloriage_output.mp4"
        print("\n✅ Coloriage mode test PASSED")
        print(f"   Output video: {output_video}")
        
        # Check if output video exists
        if os.path.exists(output_video):
            # Get video info
            cap = cv2.VideoCapture(output_video)
            frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            fps = int(cap.get(cv2.CAP_PROP_FPS))
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            cap.release()
            
            print(f"   Video info: {width}x{height}, {fps} FPS, {frame_count} frames")
            return True
        else:
            print(f"   ⚠️  Output video not found")
            return False
    else:
        print("\n❌ Coloriage mode test FAILED")
        print(f"   Error: {result.stderr}")
        return False


def test_all_modes_comparison():
    """Test all four modes: draw, erase, flood_fill, coloriage."""
    print("\n=== Testing All Modes Comparison ===\n")
    
    # Create test image
    test_image_path = create_colorful_test_image()
    
    modes = ['draw', 'erase', 'flood_fill', 'coloriage']
    results = {}
    
    for mode in modes:
        print(f"\n▶️  Testing {mode} mode...")
        
        config = {
            "output_video": f"/tmp/test_{mode}_output.mp4",
            "fps": 30,
            "slides": [
                {
                    "index": 0,
                    "duration": 3,
                    "skip_rate": 5,
                    "layers": [
                        {
                            "image_path": test_image_path,
                            "position": {"x": 0, "y": 0},
                            "z_index": 1,
                            "skip_rate": 3,
                            "mode": mode
                        }
                    ]
                }
            ]
        }
        
        config_path = f"/tmp/test_{mode}_config.json"
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=2)
        
        import subprocess
        script_dir = os.path.dirname(os.path.abspath(__file__))
        animator_script = os.path.join(script_dir, "whiteboard_animator.py")
        cmd = f"{sys.executable} {animator_script} --config {config_path}"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        
        output_video = f"/tmp/test_{mode}_output.mp4"
        success = result.returncode == 0 and os.path.exists(output_video)
        
        if success:
            cap = cv2.VideoCapture(output_video)
            frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            cap.release()
            results[mode] = {'success': True, 'frames': frame_count}
            print(f"   ✅ {mode}: {frame_count} frames")
        else:
            results[mode] = {'success': False, 'frames': 0}
            print(f"   ❌ {mode}: FAILED")
    
    # Summary
    print("\n" + "=" * 60)
    print("MODE COMPARISON SUMMARY")
    print("=" * 60)
    for mode, result in results.items():
        status = '✅' if result['success'] else '❌'
        print(f"{status} {mode:12s}: {result['frames']} frames")
    print("=" * 60)
    
    all_passed = all(r['success'] for r in results.values())
    return all_passed


def main():
    """Run all coloriage tests."""
    print("=" * 60)
    print("COLORIAGE MODE TEST SUITE")
    print("=" * 60)
    
    # Test 1: Basic coloriage mode
    test1_passed = test_coloriage_mode()
    
    # Test 2: Compare all modes
    test2_passed = test_all_modes_comparison()
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    print(f"Basic coloriage test: {'✅ PASSED' if test1_passed else '❌ FAILED'}")
    print(f"All modes comparison: {'✅ PASSED' if test2_passed else '❌ FAILED'}")
    print("=" * 60)
    
    if test1_passed and test2_passed:
        print("\n🎉 All tests PASSED!")
        return 0
    else:
        print("\n⚠️  Some tests FAILED")
        return 1


if __name__ == "__main__":
    sys.exit(main())
