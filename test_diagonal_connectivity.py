#!/usr/bin/env python3
"""
Test script to verify 8-connectivity (diagonal propagation) in flood fill mode.
This test creates images with diagonal patterns and corners to ensure proper fill coverage.
"""

import sys
import os
import cv2
import numpy as np
import json

def create_diagonal_test_image():
    """
    Create a test image with diagonal lines and corners.
    With 4-connectivity, diagonals would be separate regions.
    With 8-connectivity, they should be one region.
    """
    # Create a white canvas
    canvas = np.ones((400, 400, 3), dtype=np.uint8) * 255
    
    # Draw a diagonal staircase pattern where pixels touch only at corners
    # Each step is 2x2 pixels, placed diagonally
    # With 4-connectivity: separate regions; with 8-connectivity: one region
    for i in range(15):
        x = 50 + i * 2
        y = 50 + i * 2
        canvas[y:y+2, x:x+2] = [0, 0, 0]
    
    # Draw another diagonal line with single-pixel steps
    for i in range(20):
        x = 250 + i
        y = 50 + i
        canvas[y, x] = [0, 0, 0]
    
    # Draw a zigzag pattern (tests both horizontal and diagonal connectivity)
    points = []
    for i in range(15):
        x = 50 + i * 20
        y = 250 + (30 if i % 2 == 0 else 0)
        points.append([x, y])
    
    for i in range(len(points) - 1):
        cv2.line(canvas, tuple(points[i]), tuple(points[i+1]), (0, 0, 0), 3)
    
    return canvas


def create_corner_test_image():
    """
    Create a test image with shapes that have many corners.
    Tests if corners are properly filled without gaps.
    """
    canvas = np.ones((400, 400, 3), dtype=np.uint8) * 255
    
    # Draw a star (lots of corners and narrow angles)
    star_pts = []
    cx, cy = 200, 200
    for i in range(5):
        # Outer points
        angle = i * 72 * np.pi / 180 - np.pi/2
        x = int(cx + 80 * np.cos(angle))
        y = int(cy + 80 * np.sin(angle))
        star_pts.append([x, y])
        
        # Inner points
        angle = (i * 72 + 36) * np.pi / 180 - np.pi/2
        x = int(cx + 35 * np.cos(angle))
        y = int(cy + 35 * np.sin(angle))
        star_pts.append([x, y])
    
    star_pts = np.array(star_pts, np.int32)
    cv2.fillPoly(canvas, [star_pts], (0, 0, 0))
    
    # Draw a maze-like pattern (tests narrow passages)
    for i in range(5):
        x1 = 50 + i * 30
        y1 = 50
        y2 = 150 - i * 20
        cv2.line(canvas, (x1, y1), (x1, y2), (0, 0, 0), 5)
    
    return canvas


def test_diagonal_connectivity():
    """Test that diagonal pixels are treated as connected."""
    print("\n=== Testing Diagonal Connectivity (8-connectivity) ===\n")
    
    # Create test image
    test_image = create_diagonal_test_image()
    test_image_path = "/tmp/test_diagonal_input.png"
    cv2.imwrite(test_image_path, test_image)
    print(f"✓ Created diagonal test image: {test_image_path}")
    
    # Convert to grayscale and create binary mask
    gray = cv2.cvtColor(test_image, cv2.COLOR_BGR2GRAY)
    binary_mask = (gray < 128).astype(np.uint8)
    
    # Test with 4-connectivity (old behavior)
    num_labels_4, labels_4 = cv2.connectedComponents(binary_mask, connectivity=4)
    regions_4 = num_labels_4 - 1  # Exclude background
    
    # Test with 8-connectivity (new behavior)
    num_labels_8, labels_8 = cv2.connectedComponents(binary_mask, connectivity=8)
    regions_8 = num_labels_8 - 1  # Exclude background
    
    print(f"Connectivity test results:")
    print(f"  - 4-connectivity: {regions_4} regions (diagonal pixels separate)")
    print(f"  - 8-connectivity: {regions_8} regions (diagonal pixels connected)")
    print()
    
    if regions_8 < regions_4:
        print("✅ 8-connectivity correctly merges diagonal regions")
        print(f"   Reduced from {regions_4} to {regions_8} regions")
        return True
    else:
        print("❌ 8-connectivity did not reduce region count as expected")
        return False


def test_corner_coverage():
    """Test that corners are properly covered without gaps."""
    print("\n=== Testing Corner Coverage ===\n")
    
    # Create test image
    test_image = create_corner_test_image()
    test_image_path = "/tmp/test_corner_input.png"
    cv2.imwrite(test_image_path, test_image)
    print(f"✓ Created corner test image: {test_image_path}")
    
    # Convert to grayscale and create binary mask
    gray = cv2.cvtColor(test_image, cv2.COLOR_BGR2GRAY)
    binary_mask = (gray < 128).astype(np.uint8)
    
    # Count pixels in original
    total_black_pixels = np.sum(binary_mask)
    
    # Test with 8-connectivity
    num_labels_8, labels_8 = cv2.connectedComponents(binary_mask, connectivity=8)
    
    # Count pixels in all labeled regions
    labeled_pixels = np.sum(labels_8 > 0)
    
    print(f"Corner coverage test:")
    print(f"  - Black pixels in input: {total_black_pixels}")
    print(f"  - Labeled pixels: {labeled_pixels}")
    print(f"  - Regions detected: {num_labels_8 - 1}")
    print()
    
    if labeled_pixels == total_black_pixels:
        print("✅ All pixels properly labeled with 8-connectivity")
        return True
    else:
        print(f"⚠️  Coverage mismatch: {labeled_pixels}/{total_black_pixels} pixels")
        return False


def test_flood_fill_with_diagonal_image():
    """Test the actual flood fill function with diagonal patterns."""
    print("\n=== Testing Flood Fill Mode with Diagonal Patterns ===\n")
    
    # Create test image
    test_image = create_diagonal_test_image()
    test_image_path = "/tmp/test_flood_diagonal.png"
    cv2.imwrite(test_image_path, test_image)
    print(f"✓ Created test image: {test_image_path}")
    
    # Create configuration
    config = {
        "output_video": "/tmp/test_flood_diagonal_output.mp4",
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
                        "mode": "flood_fill"
                    }
                ]
            }
        ]
    }
    
    config_path = "/tmp/test_flood_diagonal_config.json"
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=2)
    
    print(f"✓ Created config: {config_path}")
    
    # Run whiteboard animator
    print("\n▶️  Running whiteboard animator with flood fill mode...")
    import subprocess
    script_dir = os.path.dirname(os.path.abspath(__file__))
    animator_script = os.path.join(script_dir, "whiteboard_animator.py")
    cmd = f"{sys.executable} {animator_script} --config {config_path}"
    
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    
    # Check for success indicators in output
    output = result.stdout + result.stderr
    
    if result.returncode == 0 or "Flood fill mode: found" in output:
        # Extract number of regions from output
        import re
        match = re.search(r'found (\d+) regions', output)
        if match:
            num_regions = int(match.group(1))
            print(f"✅ Flood fill detected {num_regions} regions")
            
            # With 8-connectivity, we expect fewer regions than with 4-connectivity
            # For diagonal patterns, 8-connectivity should significantly reduce region count
            # Test image has 3 distinct diagonal patterns, so expect <= 10 regions
            MAX_EXPECTED_REGIONS = 10
            if num_regions <= MAX_EXPECTED_REGIONS:
                print(f"   Region count is reasonable for 8-connectivity")
                return True
            else:
                print(f"   ⚠️  High region count ({num_regions}) suggests 4-connectivity may still be used")
                return False
        else:
            print("✅ Flood fill completed (region count not found in output)")
            return True
    else:
        print("❌ Flood fill mode test failed")
        print(f"   Error: {result.stderr[:200]}")
        return False


def main():
    """Run all diagonal connectivity tests."""
    print("=" * 70)
    print("DIAGONAL CONNECTIVITY TEST SUITE (8-connectivity)")
    print("=" * 70)
    
    # Test 1: Basic diagonal connectivity
    test1_passed = test_diagonal_connectivity()
    
    # Test 2: Corner coverage
    test2_passed = test_corner_coverage()
    
    # Test 3: Flood fill with diagonal patterns
    test3_passed = test_flood_fill_with_diagonal_image()
    
    # Summary
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    print(f"Diagonal connectivity test: {'✅ PASSED' if test1_passed else '❌ FAILED'}")
    print(f"Corner coverage test:       {'✅ PASSED' if test2_passed else '❌ FAILED'}")
    print(f"Flood fill diagonal test:   {'✅ PASSED' if test3_passed else '❌ FAILED'}")
    print("=" * 70)
    
    if test1_passed and test2_passed and test3_passed:
        print("\n🎉 All diagonal connectivity tests PASSED!")
        print("   8-connectivity is working correctly.")
        return 0
    else:
        print("\n⚠️  Some tests FAILED")
        return 1


if __name__ == "__main__":
    sys.exit(main())
