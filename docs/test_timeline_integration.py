#!/usr/bin/env python3
"""
Integration test demonstrating timeline system with config files.

This test shows how the timeline system integrates with the existing
whiteboard animator configuration format.
"""

import json
import sys
from timeline_system import GlobalTimeline


def test_load_crossfade_config():
    """Test loading and using the crossfade example config."""
    print("Testing crossfade config integration...")
    
    with open('example_timeline_crossfade.json', 'r') as f:
        config = json.load(f)
    
    # Extract timeline from config
    timeline_data = config.get('timeline', {})
    
    # Create timeline from config
    timeline = GlobalTimeline.from_dict(timeline_data)
    
    # Verify timeline properties
    assert timeline.duration == 10.0
    assert timeline.frame_rate == 30
    
    # Verify keyframes exist
    assert 'layer.0.opacity' in timeline.property_tracks
    assert 'layer.1.opacity' in timeline.property_tracks
    
    # Test opacity values at key times
    # At t=0: layer 0 fully visible (1.0), layer 1 hidden (0.0)
    assert timeline.get_property_value('layer.0.opacity', 0.0) == 1.0
    assert timeline.get_property_value('layer.1.opacity', 0.0) == 0.0
    
    # At t=5 (middle of crossfade): both should be fading
    opacity_0_at_5 = timeline.get_property_value('layer.0.opacity', 5.0)
    opacity_1_at_5 = timeline.get_property_value('layer.1.opacity', 5.0)
    # With easing, values may not be exactly 0.5, but should be between 0 and 1
    assert 0.0 < opacity_0_at_5 < 1.0
    assert 0.0 < opacity_1_at_5 < 1.0
    # At this point, one should be fading out and one fading in
    assert opacity_0_at_5 < 1.0 and opacity_1_at_5 > 0.0
    
    # At t=6: layer 0 hidden (0.0), layer 1 fully visible (1.0)
    assert timeline.get_property_value('layer.0.opacity', 6.0) == 0.0
    assert timeline.get_property_value('layer.1.opacity', 6.0) == 1.0
    
    # Verify markers
    assert len(timeline.markers) == 4
    assert timeline.markers[0].time == 0.0
    assert timeline.markers[0].label == "Start"
    
    # Verify sync points
    assert len(timeline.sync_points) == 1
    assert timeline.sync_points[0].time == 4.0
    assert len(timeline.sync_points[0].elements) == 2
    
    print("✅ Crossfade config integration test passed")


def test_load_advanced_config():
    """Test loading the advanced config with loops and remapping."""
    print("Testing advanced config integration...")
    
    with open('example_timeline_advanced.json', 'r') as f:
        config = json.load(f)
    
    timeline = GlobalTimeline.from_dict(config['timeline'])
    
    # Verify timeline properties
    assert timeline.duration == 20.0
    
    # Verify loop segment
    assert len(timeline.loop_segments) == 1
    loop = timeline.loop_segments[0]
    assert loop.start_time == 0.0
    assert loop.end_time == 4.0
    assert loop.loop_count == 3
    
    # Verify time remapping
    assert len(timeline.time_remappings) == 1
    remap = timeline.time_remappings[0]
    assert remap.original_start == 12.0
    assert remap.original_end == 14.0
    assert remap.remapped_start == 12.0
    assert remap.remapped_end == 18.0
    
    # Test remapped time
    remapped = timeline.get_remapped_time(13.0)
    assert remapped == 15.0  # Middle of original maps to middle of remapped
    
    # Verify markers
    assert len(timeline.markers) == 5
    
    print("✅ Advanced config integration test passed")


def test_load_sequence_config():
    """Test loading the sequence config with multiple elements."""
    print("Testing sequence config integration...")
    
    with open('example_timeline_sequence.json', 'r') as f:
        config = json.load(f)
    
    timeline = GlobalTimeline.from_dict(config['timeline'])
    
    # Verify timeline properties
    assert timeline.duration == 15.0
    
    # Verify multiple property tracks
    assert len(timeline.property_tracks) >= 6  # Multiple properties animated
    
    # Check layer 0 animations
    layer0_opacity = timeline.get_property_value('layer.0.opacity', 0.0)
    assert layer0_opacity == 0.0
    
    layer0_opacity = timeline.get_property_value('layer.0.opacity', 1.0)
    assert layer0_opacity == 1.0
    
    # Check layer 0 position animation
    layer0_pos_start = timeline.get_property_value('layer.0.position', 0.0)
    assert layer0_pos_start['x'] == -100
    assert layer0_pos_start['y'] == 0
    
    layer0_pos_end = timeline.get_property_value('layer.0.position', 1.0)
    assert layer0_pos_end['x'] == 0
    assert layer0_pos_end['y'] == 0
    
    # Verify sync points
    assert len(timeline.sync_points) == 4
    
    # Check "All elements visible" sync point
    all_visible_sync = [s for s in timeline.sync_points if "All elements visible" in s.label][0]
    assert len(all_visible_sync.elements) == 3
    
    # Verify markers
    assert len(timeline.markers) == 6
    
    print("✅ Sequence config integration test passed")


def test_frame_by_frame_animation():
    """Test generating frame-by-frame animation data."""
    print("Testing frame-by-frame animation generation...")
    
    with open('example_timeline_crossfade.json', 'r') as f:
        config = json.load(f)
    
    timeline = GlobalTimeline.from_dict(config['timeline'])
    
    # Generate animation data for each frame
    duration = timeline.duration
    frame_rate = timeline.frame_rate
    total_frames = int(duration * frame_rate)
    
    animation_frames = []
    
    for frame in range(total_frames):
        time = frame / frame_rate
        
        frame_data = {
            'frame': frame,
            'time': time,
            'layer_0_opacity': timeline.get_property_value('layer.0.opacity', time),
            'layer_1_opacity': timeline.get_property_value('layer.1.opacity', time),
        }
        
        animation_frames.append(frame_data)
    
    # Verify we generated the right number of frames
    assert len(animation_frames) == total_frames
    
    # Verify first frame
    assert animation_frames[0]['layer_0_opacity'] == 1.0
    assert animation_frames[0]['layer_1_opacity'] == 0.0
    
    # Verify last frame (frame 299 at 9.966s)
    assert animation_frames[-1]['layer_0_opacity'] == 0.0
    assert animation_frames[-1]['layer_1_opacity'] == 1.0
    
    # Verify middle transition frames exist
    middle_frame = animation_frames[int(5.0 * frame_rate)]  # Frame at t=5.0
    assert 0.0 < middle_frame['layer_0_opacity'] < 1.0
    assert 0.0 < middle_frame['layer_1_opacity'] < 1.0
    
    print(f"✅ Generated {total_frames} frames of animation data")
    print(f"   First frame: opacity ({animation_frames[0]['layer_0_opacity']:.2f}, {animation_frames[0]['layer_1_opacity']:.2f})")
    print(f"   Middle frame (t=5s): opacity ({middle_frame['layer_0_opacity']:.2f}, {middle_frame['layer_1_opacity']:.2f})")
    print(f"   Last frame: opacity ({animation_frames[-1]['layer_0_opacity']:.2f}, {animation_frames[-1]['layer_1_opacity']:.2f})")


def test_export_timeline_to_json():
    """Test exporting timeline back to JSON."""
    print("Testing timeline export to JSON...")
    
    # Load a config
    with open('example_timeline_crossfade.json', 'r') as f:
        original_config = json.load(f)
    
    # Create timeline
    timeline = GlobalTimeline.from_dict(original_config['timeline'])
    
    # Export back to dict
    exported = timeline.to_dict()
    
    # Verify structure preserved
    assert 'duration' in exported
    assert 'frame_rate' in exported
    assert 'property_tracks' in exported
    assert 'markers' in exported
    assert 'sync_points' in exported
    
    # Verify property tracks preserved
    assert 'layer.0.opacity' in exported['property_tracks']
    assert 'layer.1.opacity' in exported['property_tracks']
    
    # Create new timeline from exported data
    timeline2 = GlobalTimeline.from_dict(exported)
    
    # Verify values match
    for time in [0.0, 2.5, 5.0, 7.5, 10.0]:
        v1 = timeline.get_property_value('layer.0.opacity', time)
        v2 = timeline2.get_property_value('layer.0.opacity', time)
        assert v1 == v2, f"Values don't match at t={time}: {v1} != {v2}"
    
    print("✅ Timeline export/import test passed")


def test_timeline_with_slides():
    """Test how timeline integrates with slide configuration."""
    print("Testing timeline integration with slides...")
    
    # Create a config with both slides and timeline
    config = {
        "slides": [
            {
                "index": 0,
                "duration": 10,
                "layers": [
                    {"image_path": "demo/1.jpg", "z_index": 1},
                    {"image_path": "demo/2.jpg", "z_index": 2}
                ]
            }
        ],
        "timeline": {
            "duration": 10.0,
            "frame_rate": 30,
            "property_tracks": {
                "layer.0.opacity": {
                    "keyframes": [
                        {"time": 0.0, "value": 1.0},
                        {"time": 5.0, "value": 0.0}
                    ]
                }
            }
        }
    }
    
    # Extract slide info
    slide = config['slides'][0]
    assert slide['duration'] == 10
    assert len(slide['layers']) == 2
    
    # Extract and use timeline
    timeline = GlobalTimeline.from_dict(config['timeline'])
    
    # Verify timeline works with slide duration
    assert timeline.duration == slide['duration']
    
    # Generate frames for the slide
    frame_rate = timeline.frame_rate
    frames_per_slide = int(slide['duration'] * frame_rate)
    
    print(f"   Slide duration: {slide['duration']}s")
    print(f"   Frames to generate: {frames_per_slide}")
    print(f"   Layers in slide: {len(slide['layers'])}")
    
    # Simulate rendering each frame
    for frame in range(min(5, frames_per_slide)):  # Just test first 5 frames
        time = frame / frame_rate
        opacity = timeline.get_property_value('layer.0.opacity', time)
        print(f"   Frame {frame} (t={time:.2f}s): layer.0.opacity = {opacity:.3f}")
    
    print("✅ Timeline/slide integration test passed")


def run_all_integration_tests():
    """Run all integration tests."""
    print("="*60)
    print("Running Timeline Integration Tests")
    print("="*60)
    print()
    
    tests = [
        test_load_crossfade_config,
        test_load_advanced_config,
        test_load_sequence_config,
        test_frame_by_frame_animation,
        test_export_timeline_to_json,
        test_timeline_with_slides
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            print()
            passed += 1
        except FileNotFoundError as e:
            print(f"⚠️  {test.__name__} skipped: Config file not found: {e}")
            print()
        except AssertionError as e:
            print(f"❌ {test.__name__} failed: {e}")
            print()
            failed += 1
        except Exception as e:
            print(f"❌ {test.__name__} error: {e}")
            print()
            failed += 1
    
    print("="*60)
    print(f"Integration Test Results: {passed} passed, {failed} failed")
    print("="*60)
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_integration_tests()
    sys.exit(0 if success else 1)
