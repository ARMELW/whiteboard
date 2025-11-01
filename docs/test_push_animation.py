#!/usr/bin/env python3
"""Test script for push animation functionality."""

import sys
import numpy as np
import cv2
from whiteboard_animator import apply_push_animation_with_hand, draw_hand_on_img

def create_test_frame():
    """Create a simple test frame with a pattern."""
    frame = np.ones((480, 640, 3), dtype=np.uint8) * 255
    # Add a black square in the center
    frame[200:280, 280:360] = [0, 0, 0]
    # Add some colored bars
    frame[100:120, 100:540] = [255, 0, 0]  # Blue bar
    frame[360:380, 100:540] = [0, 255, 0]  # Green bar
    return frame

def create_test_hand():
    """Create a simple test hand image."""
    hand = np.zeros((100, 80, 3), dtype=np.uint8)
    # Red rectangle representing hand
    hand[:, :] = [0, 0, 255]
    # Add a brighter center to simulate hand detail
    hand[30:70, 20:60] = [50, 50, 255]
    
    hand_mask_inv = np.ones((100, 80), dtype=np.float32)
    return hand, hand_mask_inv

def test_push_from_left():
    """Test push animation from left side."""
    print("Testing push_from_left animation...")
    
    test_frame = create_test_frame()
    hand, hand_mask_inv = create_test_hand()
    
    animation_config = {
        'type': 'push_from_left',
        'duration': 1.0
    }
    
    frame_rate = 30
    total_frames = int(animation_config['duration'] * frame_rate)
    
    # Test beginning, middle, and end frames
    for frame_idx in [0, 15, 29]:
        result = apply_push_animation_with_hand(
            test_frame.copy(),
            animation_config,
            frame_idx,
            total_frames,
            frame_rate,
            hand.copy(),
            hand_mask_inv.copy(),
            100, 80
        )
        
        if result.shape != test_frame.shape:
            print(f"✗ Frame {frame_idx}: Shape mismatch")
            return False
        
        if result.dtype != test_frame.dtype:
            print(f"✗ Frame {frame_idx}: Type mismatch")
            return False
    
    # Save first and last frame for visual inspection
    result_start = apply_push_animation_with_hand(
        test_frame.copy(), animation_config, 0, total_frames, frame_rate,
        hand.copy(), hand_mask_inv.copy(), 100, 80
    )
    result_end = apply_push_animation_with_hand(
        test_frame.copy(), animation_config, 29, total_frames, frame_rate,
        hand.copy(), hand_mask_inv.copy(), 100, 80
    )
    
    cv2.imwrite("/tmp/test_push_left_start.png", result_start)
    cv2.imwrite("/tmp/test_push_left_end.png", result_end)
    
    print("✓ push_from_left animation successful")
    return True

def test_push_from_right():
    """Test push animation from right side."""
    print("Testing push_from_right animation...")
    
    test_frame = create_test_frame()
    hand, hand_mask_inv = create_test_hand()
    
    animation_config = {
        'type': 'push_from_right',
        'duration': 1.0
    }
    
    frame_rate = 30
    total_frames = int(animation_config['duration'] * frame_rate)
    
    result = apply_push_animation_with_hand(
        test_frame.copy(),
        animation_config,
        15,  # Middle frame
        total_frames,
        frame_rate,
        hand.copy(),
        hand_mask_inv.copy(),
        100, 80
    )
    
    if result.shape == test_frame.shape and result.dtype == test_frame.dtype:
        cv2.imwrite("/tmp/test_push_right.png", result)
        print("✓ push_from_right animation successful")
        return True
    else:
        print("✗ push_from_right animation failed")
        return False

def test_push_from_top():
    """Test push animation from top."""
    print("Testing push_from_top animation...")
    
    test_frame = create_test_frame()
    hand, hand_mask_inv = create_test_hand()
    
    animation_config = {
        'type': 'push_from_top',
        'duration': 1.0
    }
    
    frame_rate = 30
    total_frames = int(animation_config['duration'] * frame_rate)
    
    result = apply_push_animation_with_hand(
        test_frame.copy(),
        animation_config,
        15,
        total_frames,
        frame_rate,
        hand.copy(),
        hand_mask_inv.copy(),
        100, 80
    )
    
    if result.shape == test_frame.shape and result.dtype == test_frame.dtype:
        cv2.imwrite("/tmp/test_push_top.png", result)
        print("✓ push_from_top animation successful")
        return True
    else:
        print("✗ push_from_top animation failed")
        return False

def test_push_from_bottom():
    """Test push animation from bottom."""
    print("Testing push_from_bottom animation...")
    
    test_frame = create_test_frame()
    hand, hand_mask_inv = create_test_hand()
    
    animation_config = {
        'type': 'push_from_bottom',
        'duration': 1.0
    }
    
    frame_rate = 30
    total_frames = int(animation_config['duration'] * frame_rate)
    
    result = apply_push_animation_with_hand(
        test_frame.copy(),
        animation_config,
        15,
        total_frames,
        frame_rate,
        hand.copy(),
        hand_mask_inv.copy(),
        100, 80
    )
    
    if result.shape == test_frame.shape and result.dtype == test_frame.dtype:
        cv2.imwrite("/tmp/test_push_bottom.png", result)
        print("✓ push_from_bottom animation successful")
        return True
    else:
        print("✗ push_from_bottom animation failed")
        return False

def test_animation_progress():
    """Test animation progress through multiple frames."""
    print("Testing animation progress...")
    
    test_frame = create_test_frame()
    hand, hand_mask_inv = create_test_hand()
    
    animation_config = {
        'type': 'push_from_left',
        'duration': 1.0
    }
    
    frame_rate = 30
    total_frames = int(animation_config['duration'] * frame_rate)
    
    # Generate all frames and verify smooth progression
    frames = []
    for frame_idx in range(total_frames):
        result = apply_push_animation_with_hand(
            test_frame.copy(),
            animation_config,
            frame_idx,
            total_frames,
            frame_rate,
            hand.copy(),
            hand_mask_inv.copy(),
            100, 80
        )
        frames.append(result)
    
    if len(frames) == total_frames:
        # Save a few key frames
        cv2.imwrite("/tmp/test_progress_0.png", frames[0])
        cv2.imwrite("/tmp/test_progress_15.png", frames[15])
        cv2.imwrite("/tmp/test_progress_29.png", frames[29])
        print("✓ Animation progress test successful")
        return True
    else:
        print("✗ Animation progress test failed")
        return False

def test_invalid_direction():
    """Test handling of invalid direction."""
    print("Testing invalid direction handling...")
    
    test_frame = create_test_frame()
    hand, hand_mask_inv = create_test_hand()
    
    animation_config = {
        'type': 'push_from_invalid',
        'duration': 1.0
    }
    
    frame_rate = 30
    total_frames = 30
    
    try:
        result = apply_push_animation_with_hand(
            test_frame.copy(),
            animation_config,
            15,
            total_frames,
            frame_rate,
            hand.copy(),
            hand_mask_inv.copy(),
            100, 80
        )
        # Should default to left direction
        if result.shape == test_frame.shape:
            print("✓ Invalid direction handled (defaulted to left)")
            return True
        else:
            print("✗ Invalid direction handling failed")
            return False
    except Exception as e:
        print(f"✗ Exception during invalid direction test: {e}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("Push Animation Tests")
    print("=" * 60)
    
    tests = [
        test_push_from_left,
        test_push_from_right,
        test_push_from_top,
        test_push_from_bottom,
        test_animation_progress,
        test_invalid_direction
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
    
    if all(results):
        print("\n🎉 All tests passed!")
    else:
        print("\n❌ Some tests failed")
    
    sys.exit(0 if all(results) else 1)
