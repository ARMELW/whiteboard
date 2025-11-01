#!/usr/bin/env python3
"""Test script for flood fill mode feature."""

import sys
import os
import cv2
import numpy as np
import json

def create_test_image():
    """Create a simple test image with distinct regions."""
    # Create a white canvas
    canvas = np.ones((600, 800, 3), dtype=np.uint8) * 255
    
    # Draw some shapes to create distinct regions
    # Circle
    cv2.circle(canvas, (200, 200), 80, (0, 0, 0), -1)
    
    # Rectangle
    cv2.rectangle(canvas, (400, 100), (600, 300), (0, 0, 0), -1)
    
    # Triangle (filled polygon)
    pts = np.array([[300, 400], [400, 550], [200, 550]], np.int32)
    cv2.fillPoly(canvas, [pts], (0, 0, 0))
    
    # Star shape
    star_pts = []
    for i in range(5):
        angle = i * 144 * np.pi / 180
        outer_x = int(600 + 60 * np.cos(angle - np.pi/2))
        outer_y = int(450 + 60 * np.sin(angle - np.pi/2))
        star_pts.append([outer_x, outer_y])
        
        angle2 = (i * 144 + 72) * np.pi / 180
        inner_x = int(600 + 30 * np.cos(angle2 - np.pi/2))
        inner_y = int(450 + 30 * np.sin(angle2 - np.pi/2))
        star_pts.append([inner_x, inner_y])
    
    star_pts = np.array(star_pts, np.int32)
    cv2.fillPoly(canvas, [star_pts], (0, 0, 0))
    
    # Save the test image
    test_image_path = "/tmp/test_flood_fill_input.png"
    cv2.imwrite(test_image_path, canvas)
    print(f"✓ Created test image: {test_image_path}")
    
    return test_image_path


def create_test_config(image_path, output_video):
    """Create a test configuration JSON for flood fill mode."""
    config = {
        "output_video": output_video,
        "fps": 30,
        "slides": [
            {
                "index": 0,
                "duration": 5,
                "skip_rate": 8,
                "layers": [
                    {
                        "image_path": image_path,
                        "position": {"x": 0, "y": 0},
                        "z_index": 1,
                        "skip_rate": 5,
                        "mode": "flood_fill"
                    }
                ]
            }
        ]
    }
    
    config_path = "/tmp/test_flood_fill_config.json"
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=2)
    
    print(f"✓ Created test config: {config_path}")
    return config_path


def test_flood_fill_mode():
    """Test flood fill mode with a simple configuration."""
    print("\n=== Testing Flood Fill Mode ===\n")
    
    # Create test image with distinct regions
    test_image_path = create_test_image()
    
    # Create test configuration
    output_video = "/tmp/test_flood_fill_output.mp4"
    config_path = create_test_config(test_image_path, output_video)
    
    # Run whiteboard animator with the test config
    print("\n▶️  Running whiteboard animator with flood fill mode...")
    cmd = f"python3 /home/runner/work/whiteboard/whiteboard/whiteboard_animator.py --config {config_path}"
    
    import subprocess
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    
    if result.returncode == 0:
        print("\n✅ Flood fill mode test PASSED")
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
        print("\n❌ Flood fill mode test FAILED")
        print(f"   Error: {result.stderr}")
        return False


def test_flood_fill_vs_draw_mode():
    """Test flood fill mode compared to draw mode."""
    print("\n=== Testing Flood Fill vs Draw Mode ===\n")
    
    # Create test image
    test_image_path = create_test_image()
    
    # Test with draw mode
    print("\n1️⃣  Testing with draw mode...")
    output_draw = "/tmp/test_draw_mode_output.mp4"
    config_draw = create_test_config(test_image_path, output_draw)
    
    # Modify config to use draw mode
    with open(config_draw, 'r') as f:
        config = json.load(f)
    config['slides'][0]['layers'][0]['mode'] = 'draw'
    with open(config_draw, 'w') as f:
        json.dump(config, f, indent=2)
    
    cmd_draw = f"python3 /home/runner/work/whiteboard/whiteboard/whiteboard_animator.py --config {config_draw}"
    result_draw = subprocess.run(cmd_draw, shell=True, capture_output=True, text=True)
    
    # Test with flood_fill mode
    print("\n2️⃣  Testing with flood_fill mode...")
    output_flood = "/tmp/test_flood_fill_mode_output.mp4"
    config_flood = create_test_config(test_image_path, output_flood)
    
    cmd_flood = f"python3 /home/runner/work/whiteboard/whiteboard/whiteboard_animator.py --config {config_flood}"
    result_flood = subprocess.run(cmd_flood, shell=True, capture_output=True, text=True)
    
    # Compare results
    draw_success = result_draw.returncode == 0 and os.path.exists(output_draw)
    flood_success = result_flood.returncode == 0 and os.path.exists(output_flood)
    
    if draw_success and flood_success:
        print("\n✅ Both modes completed successfully")
        print(f"   Draw mode output: {output_draw}")
        print(f"   Flood fill output: {output_flood}")
        return True
    else:
        print("\n❌ Comparison test FAILED")
        if not draw_success:
            print(f"   Draw mode failed: {result_draw.stderr}")
        if not flood_success:
            print(f"   Flood fill mode failed: {result_flood.stderr}")
        return False


def main():
    """Run all flood fill tests."""
    print("=" * 60)
    print("FLOOD FILL MODE TEST SUITE")
    print("=" * 60)
    
    import subprocess
    
    # Test 1: Basic flood fill mode
    test1_passed = test_flood_fill_mode()
    
    # Test 2: Compare with draw mode
    test2_passed = test_flood_fill_vs_draw_mode()
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    print(f"Basic flood fill test: {'✅ PASSED' if test1_passed else '❌ FAILED'}")
    print(f"Flood fill vs draw test: {'✅ PASSED' if test2_passed else '❌ FAILED'}")
    print("=" * 60)
    
    if test1_passed and test2_passed:
        print("\n🎉 All tests PASSED!")
        return 0
    else:
        print("\n⚠️  Some tests FAILED")
        return 1


if __name__ == "__main__":
    sys.exit(main())
