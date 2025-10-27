#!/usr/bin/env python3
"""Integration test for arrow type layer feature."""

import sys
import os
import json
import cv2
from pathlib import Path

def create_test_config():
    """Create a minimal test configuration."""
    config = {
        "slides": [
            {
                "index": 0,
                "duration": 3,
                "layers": [
                    {
                        "type": "arrow",
                        "arrow_config": {
                            "start": [200, 400],
                            "end": [1400, 400],
                            "color": "#E74C3C",
                            "fill_color": "#F1948A",
                            "stroke_width": 5,
                            "arrow_size": 40,
                            "duration": 2.0
                        },
                        "z_index": 1,
                        "mode": "draw"
                    }
                ]
            }
        ]
    }
    return config


def test_arrow_type_integration():
    """Test arrow type with whiteboard animator."""
    print("Testing arrow type integration with whiteboard animator...")
    
    # Create test config
    config = create_test_config()
    config_path = "/tmp/test_arrow_integration.json"
    
    # Write config to file
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=2)
    
    print(f"  Created test config: {config_path}")
    
    # Try to import and run
    try:
        from whiteboard_animator import process_config_file
        
        output_path = "/tmp/test_arrow_output.mp4"
        
        # Run the animation
        print("  Running animation generation...")
        result = process_config_file(
            config_path,
            split_len=15,
            frame_rate=30,
            object_skip_rate=8,
            bg_object_skip_rate=20,
            which_platform="linux"
        )
        
        # Check if output was created
        if os.path.exists(output_path):
            # Get video info
            cap = cv2.VideoCapture(output_path)
            frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            fps = int(cap.get(cv2.CAP_PROP_FPS))
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            cap.release()
            
            print(f"  ✓ Video created successfully:")
            print(f"    - Path: {output_path}")
            print(f"    - Frames: {frame_count}")
            print(f"    - FPS: {fps}")
            print(f"    - Resolution: {width}x{height}")
            
            # Extract a few sample frames
            cap = cv2.VideoCapture(output_path)
            for i, frame_num in enumerate([0, frame_count // 3, frame_count * 2 // 3, frame_count - 1]):
                cap.set(cv2.CAP_PROP_POS_FRAMES, frame_num)
                ret, frame = cap.read()
                if ret:
                    sample_path = f"/tmp/test_arrow_frame_{i}.png"
                    cv2.imwrite(sample_path, frame)
                    print(f"    - Sample frame {i}: {sample_path}")
            cap.release()
            
            return True
        else:
            print(f"  ✗ Video not created at {output_path}")
            return False
            
    except Exception as e:
        print(f"  ✗ Integration test failed with exception: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run integration test."""
    print("=== Arrow Type Integration Test ===\n")
    
    result = test_arrow_type_integration()
    
    print("\n=== Test Result ===")
    if result:
        print("✓ Integration test passed!")
        return 0
    else:
        print("✗ Integration test failed")
        return 1


if __name__ == '__main__':
    sys.exit(main())
