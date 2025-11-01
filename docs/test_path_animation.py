#!/usr/bin/env python3
"""Test path animation functions"""

import sys
import math
import numpy as np

# Import the functions we want to test
from whiteboard_animator import (
    evaluate_bezier_cubic,
    evaluate_bezier_quadratic,
    evaluate_path_at_time,
    apply_speed_curve
)

def test_bezier_cubic():
    """Test cubic Bezier curve evaluation"""
    print("Testing cubic Bezier curve...")
    p0 = (0, 0)
    p1 = (100, 0)
    p2 = (100, 100)
    p3 = (200, 100)
    
    # Test at t=0 (should be p0)
    result = evaluate_bezier_cubic(p0, p1, p2, p3, 0.0)
    assert abs(result[0] - p0[0]) < 0.01 and abs(result[1] - p0[1]) < 0.01, "t=0 failed"
    
    # Test at t=1 (should be p3)
    result = evaluate_bezier_cubic(p0, p1, p2, p3, 1.0)
    assert abs(result[0] - p3[0]) < 0.01 and abs(result[1] - p3[1]) < 0.01, "t=1 failed"
    
    # Test at t=0.5 (should be somewhere in the middle)
    result = evaluate_bezier_cubic(p0, p1, p2, p3, 0.5)
    assert 0 < result[0] < 200 and 0 < result[1] < 100, "t=0.5 failed"
    
    print("  ✓ Cubic Bezier tests passed")

def test_bezier_quadratic():
    """Test quadratic Bezier curve evaluation"""
    print("Testing quadratic Bezier curve...")
    p0 = (0, 0)
    p1 = (100, 100)
    p2 = (200, 0)
    
    # Test at t=0 (should be p0)
    result = evaluate_bezier_quadratic(p0, p1, p2, 0.0)
    assert abs(result[0] - p0[0]) < 0.01 and abs(result[1] - p0[1]) < 0.01, "t=0 failed"
    
    # Test at t=1 (should be p2)
    result = evaluate_bezier_quadratic(p0, p1, p2, 1.0)
    assert abs(result[0] - p2[0]) < 0.01 and abs(result[1] - p2[1]) < 0.01, "t=1 failed"
    
    print("  ✓ Quadratic Bezier tests passed")

def test_path_evaluation():
    """Test path evaluation with different types"""
    print("Testing path evaluation...")
    
    # Test linear path
    linear_config = {
        'type': 'linear',
        'points': [(0, 0), (100, 100)]
    }
    x, y, angle = evaluate_path_at_time(linear_config, 0.5)
    assert abs(x - 50) < 0.01 and abs(y - 50) < 0.01, "Linear path failed"
    assert abs(angle - 45) < 0.1, f"Linear angle failed: expected ~45, got {angle}"
    
    # Test cubic bezier path
    cubic_config = {
        'type': 'bezier_cubic',
        'points': [(0, 0), (50, 0), (50, 100), (100, 100)]
    }
    x, y, angle = evaluate_path_at_time(cubic_config, 0.0)
    assert abs(x - 0) < 0.01 and abs(y - 0) < 0.01, "Cubic bezier start failed"
    
    x, y, angle = evaluate_path_at_time(cubic_config, 1.0)
    assert abs(x - 100) < 0.01 and abs(y - 100) < 0.01, "Cubic bezier end failed"
    
    # Test quadratic bezier path
    quad_config = {
        'type': 'bezier_quadratic',
        'points': [(0, 0), (50, 100), (100, 0)]
    }
    x, y, angle = evaluate_path_at_time(quad_config, 0.0)
    assert abs(x - 0) < 0.01 and abs(y - 0) < 0.01, "Quadratic bezier start failed"
    
    # Test spline path
    spline_config = {
        'type': 'spline',
        'points': [(0, 0), (50, 50), (100, 50), (150, 0)]
    }
    x, y, angle = evaluate_path_at_time(spline_config, 0.0)
    # Spline may not pass exactly through first point, but should be close
    assert 0 <= x <= 150 and 0 <= y <= 100, "Spline evaluation failed"
    
    print("  ✓ Path evaluation tests passed")

def test_speed_curves():
    """Test speed curve application"""
    print("Testing speed curves...")
    
    # Linear should be unchanged
    assert abs(apply_speed_curve(0.5, 'linear') - 0.5) < 0.01, "Linear speed curve failed"
    
    # Ease in should be slower at start
    ease_in_mid = apply_speed_curve(0.5, 'ease_in')
    assert ease_in_mid < 0.5, f"Ease in should be < 0.5 at t=0.5, got {ease_in_mid}"
    
    # Ease out should be faster at start  
    ease_out_mid = apply_speed_curve(0.5, 'ease_out')
    assert ease_out_mid > 0.5, f"Ease out should be > 0.5 at t=0.5, got {ease_out_mid}"
    
    # All should map 0 to 0 and 1 to 1
    for profile in ['linear', 'ease_in', 'ease_out', 'ease_in_out']:
        assert abs(apply_speed_curve(0.0, profile) - 0.0) < 0.01, f"{profile} failed at t=0"
        assert abs(apply_speed_curve(1.0, profile) - 1.0) < 0.01, f"{profile} failed at t=1"
    
    print("  ✓ Speed curve tests passed")

if __name__ == '__main__':
    print("\n=== Path Animation Function Tests ===\n")
    
    try:
        test_bezier_cubic()
        test_bezier_quadratic()
        test_path_evaluation()
        test_speed_curves()
        
        print("\n✅ All tests passed!\n")
        sys.exit(0)
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}\n")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}\n")
        import traceback
        traceback.print_exc()
        sys.exit(1)
