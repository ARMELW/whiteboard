#!/usr/bin/env python3
"""
Test suite for the timeline system.

Tests cover:
- Keyframe system
- Time markers
- Sync points
- Animation curves
- Time remapping
- Loop segments
- Global timeline
"""

import json
import sys
from timeline_system import (
    GlobalTimeline, Keyframe, TimeMarker, SyncPoint, LoopSegment,
    KeyframeInterpolation, PropertyTrack, TimeRemapping,
    apply_easing, interpolate_values
)


def test_keyframe_creation():
    """Test creating keyframes."""
    print("Testing keyframe creation...")
    
    kf = Keyframe(time=0.0, value=0, interpolation=KeyframeInterpolation.LINEAR)
    assert kf.time == 0.0
    assert kf.value == 0
    assert kf.interpolation == KeyframeInterpolation.LINEAR
    
    kf2 = Keyframe(time=1.0, value=100, interpolation="ease_in_out")
    assert kf2.interpolation == KeyframeInterpolation.EASE_IN_OUT
    
    print("✅ Keyframe creation test passed")


def test_property_track():
    """Test property track with keyframes."""
    print("Testing property track...")
    
    track = PropertyTrack("opacity")
    track.add_keyframe(0.0, 0.0, KeyframeInterpolation.LINEAR)
    track.add_keyframe(1.0, 1.0, KeyframeInterpolation.LINEAR)
    
    # Test interpolation at various points
    assert track.get_value_at_time(0.0) == 0.0
    assert track.get_value_at_time(0.5) == 0.5
    assert track.get_value_at_time(1.0) == 1.0
    
    # Test before first keyframe
    assert track.get_value_at_time(-1.0) == 0.0
    
    # Test after last keyframe
    assert track.get_value_at_time(2.0) == 1.0
    
    print("✅ Property track test passed")


def test_easing_functions():
    """Test easing functions."""
    print("Testing easing functions...")
    
    # Linear
    assert apply_easing(0.5, KeyframeInterpolation.LINEAR) == 0.5
    
    # Ease in
    ease_in = apply_easing(0.5, KeyframeInterpolation.EASE_IN)
    assert ease_in == 0.25  # 0.5^2
    
    # Ease out
    ease_out = apply_easing(0.5, KeyframeInterpolation.EASE_OUT)
    assert ease_out == 0.75  # 0.5 * (2 - 0.5)
    
    # Ease in-out
    ease_in_out_early = apply_easing(0.25, KeyframeInterpolation.EASE_IN_OUT)
    assert ease_in_out_early == 0.125  # 2 * 0.25^2
    
    ease_in_out_late = apply_easing(0.75, KeyframeInterpolation.EASE_IN_OUT)
    expected = -1 + (4 - 2 * 0.75) * 0.75
    assert abs(ease_in_out_late - expected) < 0.001
    
    print("✅ Easing functions test passed")


def test_interpolate_values():
    """Test value interpolation."""
    print("Testing value interpolation...")
    
    # Numeric interpolation
    assert interpolate_values(0, 100, 0.5) == 50
    assert interpolate_values(0.0, 1.0, 0.25) == 0.25
    
    # Tuple interpolation (e.g., RGB colors)
    color1 = (0, 0, 0)
    color2 = (255, 255, 255)
    result = interpolate_values(color1, color2, 0.5)
    assert result == (127.5, 127.5, 127.5)
    
    # Dict interpolation (e.g., position)
    pos1 = {'x': 0, 'y': 0}
    pos2 = {'x': 100, 'y': 50}
    result = interpolate_values(pos1, pos2, 0.5)
    assert result == {'x': 50, 'y': 25}
    
    print("✅ Value interpolation test passed")


def test_global_timeline():
    """Test global timeline with keyframes."""
    print("Testing global timeline...")
    
    timeline = GlobalTimeline(duration=10.0, frame_rate=30)
    
    # Add keyframes for opacity
    timeline.add_keyframe("layer.0.opacity", 0.0, 0.0)
    timeline.add_keyframe("layer.0.opacity", 2.0, 1.0)
    timeline.add_keyframe("layer.0.opacity", 5.0, 1.0)
    timeline.add_keyframe("layer.0.opacity", 7.0, 0.0)
    
    # Test values at different times
    assert timeline.get_property_value("layer.0.opacity", 0.0) == 0.0
    assert timeline.get_property_value("layer.0.opacity", 1.0) == 0.5
    assert timeline.get_property_value("layer.0.opacity", 2.0) == 1.0
    assert timeline.get_property_value("layer.0.opacity", 3.5) == 1.0
    assert timeline.get_property_value("layer.0.opacity", 6.0) == 0.5
    
    print("✅ Global timeline test passed")


def test_time_markers():
    """Test time markers."""
    print("Testing time markers...")
    
    timeline = GlobalTimeline(duration=10.0)
    
    timeline.add_marker(2.0, "Scene 1", color="#FF0000")
    timeline.add_marker(5.0, "Scene 2", color="#00FF00")
    timeline.add_marker(8.0, "Scene 3", color="#0000FF")
    
    assert len(timeline.markers) == 3
    assert timeline.markers[0].time == 2.0
    assert timeline.markers[0].label == "Scene 1"
    assert timeline.markers[1].time == 5.0
    
    print("✅ Time markers test passed")


def test_sync_points():
    """Test synchronization points."""
    print("Testing sync points...")
    
    timeline = GlobalTimeline(duration=10.0)
    
    timeline.add_sync_point(3.0, ["layer1", "layer2", "text1"], "All appear together")
    timeline.add_sync_point(6.0, ["layer1", "layer2"], "Both fade out")
    
    assert len(timeline.sync_points) == 2
    assert timeline.sync_points[0].time == 3.0
    assert len(timeline.sync_points[0].elements) == 3
    assert "layer1" in timeline.sync_points[0].elements
    
    print("✅ Sync points test passed")


def test_loop_segments():
    """Test loop segments."""
    print("Testing loop segments...")
    
    timeline = GlobalTimeline(duration=10.0)
    
    # Add a loop from 2s to 4s that loops 3 times
    timeline.add_loop_segment(2.0, 4.0, 3, "Intro loop")
    
    assert len(timeline.loop_segments) == 1
    assert timeline.loop_segments[0].start_time == 2.0
    assert timeline.loop_segments[0].end_time == 4.0
    assert timeline.loop_segments[0].loop_count == 3
    
    # Test loop application
    # Time 2.5 is in the loop
    effective_time = timeline._apply_loops(2.5)
    assert effective_time == 2.5
    
    # Time 3.0 is in the loop
    effective_time = timeline._apply_loops(3.0)
    assert effective_time == 3.0
    
    # Total duration should account for loops
    total_duration = timeline.get_total_duration_with_loops()
    loop_duration = 4.0 - 2.0  # 2 seconds
    expected = 10.0 + loop_duration * (3 - 1)  # Original + 2 extra loops
    assert total_duration == expected
    
    print("✅ Loop segments test passed")


def test_time_remapping():
    """Test time remapping."""
    print("Testing time remapping...")
    
    timeline = GlobalTimeline(duration=10.0)
    
    # Slow down time from 2s to 4s, making it 4 seconds instead of 2
    timeline.add_time_remapping(2.0, 4.0, 2.0, 6.0, KeyframeInterpolation.LINEAR)
    
    # Time before remapping range
    assert timeline.get_remapped_time(1.0) == 1.0
    
    # Time at start of remapping
    assert timeline.get_remapped_time(2.0) == 2.0
    
    # Time in middle of remapping (should be stretched)
    remapped = timeline.get_remapped_time(3.0)
    # 3.0 is 50% through original range (2.0-4.0)
    # Should map to 50% through remapped range (2.0-6.0) = 4.0
    assert remapped == 4.0
    
    # Time at end of remapping
    assert timeline.get_remapped_time(4.0) == 6.0
    
    # Time after remapping range
    assert timeline.get_remapped_time(5.0) == 5.0
    
    print("✅ Time remapping test passed")


def test_timeline_serialization():
    """Test timeline to/from dict conversion."""
    print("Testing timeline serialization...")
    
    # Create a timeline with various features
    timeline = GlobalTimeline(duration=10.0, frame_rate=30)
    
    # Add keyframes
    timeline.add_keyframe("opacity", 0.0, 0.0, KeyframeInterpolation.EASE_IN)
    timeline.add_keyframe("opacity", 2.0, 1.0, KeyframeInterpolation.EASE_OUT)
    
    # Add markers
    timeline.add_marker(1.0, "Marker 1", "#FF0000")
    
    # Add sync point
    timeline.add_sync_point(2.0, ["layer1", "layer2"], "Sync 1")
    
    # Add loop
    timeline.add_loop_segment(3.0, 5.0, 2, "Loop 1")
    
    # Add time remapping
    timeline.add_time_remapping(6.0, 8.0, 6.0, 10.0)
    
    # Convert to dict
    data = timeline.to_dict()
    
    # Verify structure
    assert 'duration' in data
    assert 'frame_rate' in data
    assert 'property_tracks' in data
    assert 'markers' in data
    assert 'sync_points' in data
    assert 'loop_segments' in data
    assert 'time_remappings' in data
    
    # Convert back to timeline
    timeline2 = GlobalTimeline.from_dict(data)
    
    # Verify data preserved
    assert timeline2.duration == timeline.duration
    assert timeline2.frame_rate == timeline.frame_rate
    assert len(timeline2.property_tracks) == len(timeline.property_tracks)
    assert len(timeline2.markers) == len(timeline.markers)
    assert len(timeline2.sync_points) == len(timeline.sync_points)
    assert len(timeline2.loop_segments) == len(timeline.loop_segments)
    assert len(timeline2.time_remappings) == len(timeline.time_remappings)
    
    # Test keyframe values
    assert timeline2.get_property_value("opacity", 1.0) == timeline.get_property_value("opacity", 1.0)
    
    print("✅ Timeline serialization test passed")


def test_complex_animation_curve():
    """Test complex animation with multiple properties."""
    print("Testing complex animation curve...")
    
    timeline = GlobalTimeline(duration=10.0, frame_rate=30)
    
    # Animate position, scale, and opacity together
    # Position animation
    timeline.add_keyframe("element.position", 0.0, {'x': 0, 'y': 0}, KeyframeInterpolation.EASE_OUT)
    timeline.add_keyframe("element.position", 2.0, {'x': 100, 'y': 50}, KeyframeInterpolation.EASE_IN)
    timeline.add_keyframe("element.position", 4.0, {'x': 200, 'y': 0}, KeyframeInterpolation.EASE_OUT)
    
    # Scale animation
    timeline.add_keyframe("element.scale", 0.0, 0.5, KeyframeInterpolation.LINEAR)
    timeline.add_keyframe("element.scale", 2.0, 1.5, KeyframeInterpolation.LINEAR)
    timeline.add_keyframe("element.scale", 4.0, 1.0, KeyframeInterpolation.LINEAR)
    
    # Opacity animation
    timeline.add_keyframe("element.opacity", 0.0, 0.0, KeyframeInterpolation.EASE_IN)
    timeline.add_keyframe("element.opacity", 1.0, 1.0, KeyframeInterpolation.LINEAR)
    timeline.add_keyframe("element.opacity", 3.0, 1.0, KeyframeInterpolation.LINEAR)
    timeline.add_keyframe("element.opacity", 4.0, 0.0, KeyframeInterpolation.EASE_OUT)
    
    # Test values at t=1.0
    pos = timeline.get_property_value("element.position", 1.0)
    scale = timeline.get_property_value("element.scale", 1.0)
    opacity = timeline.get_property_value("element.opacity", 1.0)
    
    assert isinstance(pos, dict)
    assert 'x' in pos and 'y' in pos
    assert isinstance(scale, (int, float))
    assert isinstance(opacity, (int, float))
    assert opacity == 1.0  # Should be at full opacity at t=1.0
    
    print("✅ Complex animation curve test passed")


def test_step_interpolation():
    """Test step interpolation (no smooth transition)."""
    print("Testing step interpolation...")
    
    track = PropertyTrack("state")
    track.add_keyframe(0.0, "idle", KeyframeInterpolation.STEP)
    track.add_keyframe(2.0, "running", KeyframeInterpolation.STEP)
    track.add_keyframe(4.0, "jumping", KeyframeInterpolation.STEP)
    
    # Should hold first value until next keyframe
    assert track.get_value_at_time(0.0) == "idle"
    assert track.get_value_at_time(1.0) == "idle"
    assert track.get_value_at_time(1.999) == "idle"
    assert track.get_value_at_time(2.0) == "running"
    assert track.get_value_at_time(3.0) == "running"
    
    print("✅ Step interpolation test passed")


def run_all_tests():
    """Run all timeline tests."""
    print("="*60)
    print("Running Timeline System Tests")
    print("="*60)
    print()
    
    tests = [
        test_keyframe_creation,
        test_property_track,
        test_easing_functions,
        test_interpolate_values,
        test_global_timeline,
        test_time_markers,
        test_sync_points,
        test_loop_segments,
        test_time_remapping,
        test_timeline_serialization,
        test_complex_animation_curve,
        test_step_interpolation
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"❌ {test.__name__} failed: {e}")
            failed += 1
        except Exception as e:
            print(f"❌ {test.__name__} error: {e}")
            failed += 1
    
    print()
    print("="*60)
    print(f"Test Results: {passed} passed, {failed} failed")
    print("="*60)
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
