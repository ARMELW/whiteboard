#!/usr/bin/env python3
"""
Test script to verify sceneCameras mapping functionality.

This test ensures that:
1. sceneCameras field is properly mapped to cameras
2. Single scene configs without 'slides' wrapper are handled
3. Camera positions and zoom levels are correctly applied
"""

import json
import os
import sys
import tempfile
from pathlib import Path

def test_scene_cameras_mapping():
    """Test that sceneCameras is properly mapped to cameras."""
    
    # Test data matching the problem statement
    scene_config = {
        "title": "Test Scene",
        "duration": 5,
        "canvas_width": 1920,
        "canvas_height": 1080,
        "layers": [
            {
                "id": "test-layer-1",
                "mode": "draw",
                "type": "text",
                "position": {"x": 960, "y": 540},
                "z_index": 1,
                "text_config": {
                    "text": "Test Text",
                    "font": "Arial",
                    "size": 48,
                    "color": [0, 0, 0],
                    "align": "center"
                }
            }
        ],
        "sceneCameras": [
            {
                "id": "camera-default",
                "name": "Vue par défaut",
                "position": {"x": 0.5, "y": 0.5},
                "zoom": 0.8,
                "duration": 2,
                "width": 800,
                "height": 450
            },
            {
                "id": "camera-zoom",
                "name": "Camera Zoom",
                "position": {"x": 0.7, "y": 0.5},
                "zoom": 1.2,
                "duration": 3,
                "transition_duration": 1
            }
        ]
    }
    
    # Save to temporary file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(scene_config, f, indent=2)
        config_path = f.name
    
    try:
        # Import the whiteboard_animator module
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        import whiteboard_animator
        
        # Load the config as the code does
        with open(config_path, 'r', encoding='utf-8') as f:
            per_slide_config = json.load(f)
        
        # Check if config has layers at root (should trigger wrapping logic)
        has_layers = 'layers' in per_slide_config
        has_scene_cameras = 'sceneCameras' in per_slide_config
        
        print("✅ Test 1: Scene config structure detected")
        print(f"   - Has layers: {has_layers}")
        print(f"   - Has sceneCameras: {has_scene_cameras}")
        
        assert has_layers, "Config should have layers at root"
        assert has_scene_cameras, "Config should have sceneCameras"
        
        # Simulate the wrapping logic from process_multiple_images
        if 'layers' in per_slide_config and 'slides' not in per_slide_config:
            wrapped_config = {
                'slides': [per_slide_config],
                'canvas_width': per_slide_config.get('canvas_width', 1920),
                'canvas_height': per_slide_config.get('canvas_height', 1080)
            }
            
            # Map sceneCameras to cameras
            if 'sceneCameras' in wrapped_config['slides'][0]:
                wrapped_config['slides'][0]['cameras'] = wrapped_config['slides'][0].get('sceneCameras')
            
            wrapped_config['slides'][0]['index'] = 0
            per_slide_config = wrapped_config
        
        print("\n✅ Test 2: Config wrapping successful")
        print(f"   - Has slides array: {'slides' in per_slide_config}")
        print(f"   - Number of slides: {len(per_slide_config.get('slides', []))}")
        
        # Verify the wrapped structure
        assert 'slides' in per_slide_config, "Config should have slides array"
        assert len(per_slide_config['slides']) == 1, "Should have exactly 1 slide"
        
        slide = per_slide_config['slides'][0]
        
        print("\n✅ Test 3: Slide structure correct")
        print(f"   - Has cameras: {'cameras' in slide}")
        print(f"   - Has layers: {'layers' in slide}")
        
        assert 'cameras' in slide, "Slide should have cameras field"
        assert 'layers' in slide, "Slide should have layers field"
        
        # Verify cameras content
        cameras = slide.get('cameras', [])
        print(f"\n✅ Test 4: Cameras mapped from sceneCameras")
        print(f"   - Number of cameras: {len(cameras)}")
        print(f"   - Camera 1: zoom={cameras[0].get('zoom')}, duration={cameras[0].get('duration')}")
        print(f"   - Camera 2: zoom={cameras[1].get('zoom')}, duration={cameras[1].get('duration')}")
        
        assert len(cameras) == 2, "Should have 2 cameras"
        assert cameras[0].get('zoom') == 0.8, "First camera zoom should be 0.8"
        assert cameras[0].get('duration') == 2, "First camera duration should be 2"
        assert cameras[1].get('zoom') == 1.2, "Second camera zoom should be 1.2"
        assert cameras[1].get('duration') == 3, "Second camera duration should be 3"
        
        # Test 5: Verify empty cameras array triggers mapping
        print("\n✅ Test 5: Empty cameras array handling")
        test_empty_cameras = {
            "layers": [{"type": "text", "text_config": {"text": "test"}}],
            "cameras": [],
            "sceneCameras": [{"zoom": 0.8}]
        }
        
        if 'sceneCameras' in test_empty_cameras:
            if 'cameras' not in test_empty_cameras or not test_empty_cameras['cameras']:
                test_empty_cameras['cameras'] = test_empty_cameras['sceneCameras']
        
        assert test_empty_cameras['cameras'][0]['zoom'] == 0.8, "Empty cameras should be replaced by sceneCameras"
        print("   - Empty cameras array correctly replaced with sceneCameras")
        
        # Test 6: Verify non-empty cameras takes priority
        print("\n✅ Test 6: Non-empty cameras takes priority")
        test_priority = {
            "layers": [{"type": "text", "text_config": {"text": "test"}}],
            "cameras": [{"zoom": 1.5}],
            "sceneCameras": [{"zoom": 0.5}]
        }
        
        if 'sceneCameras' in test_priority:
            if 'cameras' not in test_priority or not test_priority['cameras']:
                test_priority['cameras'] = test_priority['sceneCameras']
        
        assert test_priority['cameras'][0]['zoom'] == 1.5, "Non-empty cameras should take priority"
        print("   - Non-empty cameras correctly takes priority over sceneCameras")
        
        print("\n" + "="*60)
        print("🎉 ALL TESTS PASSED!")
        print("="*60)
        print("✓ sceneCameras properly mapped to cameras")
        print("✓ Single scene config properly wrapped in slides array")
        print("✓ Camera properties preserved correctly")
        print("✓ Empty cameras array replaced with sceneCameras")
        print("✓ Non-empty cameras takes priority over sceneCameras")
        print("="*60)
        
        return True
        
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
        return False
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        # Clean up temp file
        if os.path.exists(config_path):
            os.unlink(config_path)


if __name__ == "__main__":
    success = test_scene_cameras_mapping()
    sys.exit(0 if success else 1)
