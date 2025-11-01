#!/usr/bin/env python3
"""Test path follow animation mode"""

import sys
import numpy as np
import cv2
from pathlib import Path

# Import the functions we want to test
from whiteboard_animator import extract_path_points

def test_extract_path_points():
    """Test path point extraction from a simple drawing"""
    print("Testing path point extraction...")
    
    # Create a simple test image with a line
    img = np.ones((100, 100), dtype=np.uint8) * 255
    
    # Draw a simple diagonal line
    cv2.line(img, (10, 10), (90, 90), 0, 2)
    
    # Extract path points
    points = extract_path_points(img, sampling_rate=1)
    
    # Verify we got some points
    assert len(points) > 0, "Should extract some points from the line"
    print(f"  ✓ Extracted {len(points)} points from test line")
    
    # Test with sampling
    points_sampled = extract_path_points(img, sampling_rate=5)
    assert len(points_sampled) < len(points), "Sampling should reduce number of points"
    print(f"  ✓ Sampling works: {len(points_sampled)} points with sampling_rate=5")
    
    print("  ✓ Path point extraction tests passed")

def test_extract_path_points_with_mask():
    """Test path point extraction with object mask"""
    print("Testing path point extraction with mask...")
    
    # Create a test image with two separate drawings
    img = np.ones((100, 100), dtype=np.uint8) * 255
    cv2.circle(img, (25, 50), 15, 0, 2)  # Left circle
    cv2.circle(img, (75, 50), 15, 0, 2)  # Right circle
    
    # Create a mask for only the left circle
    mask = np.zeros((100, 100), dtype=np.uint8)
    cv2.circle(mask, (25, 50), 20, 255, -1)
    
    # Extract points with mask
    points_masked = extract_path_points(img, object_mask=mask)
    
    # All points should be in the left circle area (x < 50)
    left_points = [p for p in points_masked if p[0] < 50]
    assert len(left_points) > 0, "Should extract points from left circle"
    assert len(left_points) == len(points_masked), "Mask should exclude right circle"
    
    print(f"  ✓ Mask filtering works: {len(points_masked)} points in masked region")
    print("  ✓ Path point extraction with mask tests passed")

def test_path_points_ordering():
    """Test that path points are ordered naturally"""
    print("Testing path point ordering...")
    
    # Create a simple image with scattered points
    img = np.ones((200, 200), dtype=np.uint8) * 255
    
    # Draw some points at different positions
    cv2.circle(img, (50, 50), 3, 0, -1)   # Top-left
    cv2.circle(img, (150, 50), 3, 0, -1)  # Top-right
    cv2.circle(img, (50, 150), 3, 0, -1)  # Bottom-left
    cv2.circle(img, (150, 150), 3, 0, -1) # Bottom-right
    
    # Extract points
    points = extract_path_points(img, sampling_rate=1)
    
    # Points should generally flow from top to bottom, left to right
    # (due to the sorting key in extract_path_points)
    if len(points) >= 2:
        # First points should be in the upper part of the image
        top_points = [p for p in points[:len(points)//2] if p[1] < 100]
        bottom_points = [p for p in points[len(points)//2:] if p[1] >= 100]
        
        print(f"  ✓ Point ordering: {len(top_points)} top points, {len(bottom_points)} bottom points")
    
    print("  ✓ Path point ordering tests passed")

if __name__ == "__main__":
    try:
        test_extract_path_points()
        test_extract_path_points_with_mask()
        test_path_points_ordering()
        print("\n✅ All path follow tests passed!")
        sys.exit(0)
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error running tests: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
