#!/usr/bin/env python3
"""
Visual demonstration of the timeline system capabilities.

This script demonstrates all timeline features with visual ASCII output
showing how animations progress over time.
"""

import json
from timeline_system import GlobalTimeline, KeyframeInterpolation


def print_header(title):
    """Print a section header."""
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70)


def visualize_value(value, min_val=0.0, max_val=1.0, width=40):
    """Create a visual bar representation of a value."""
    if value < min_val:
        value = min_val
    if value > max_val:
        value = max_val
    
    normalized = (value - min_val) / (max_val - min_val)
    bar_length = int(normalized * width)
    bar = "█" * bar_length + "░" * (width - bar_length)
    return f"{bar} {value:.3f}"


def demo_keyframe_interpolation():
    """Demonstrate keyframe interpolation with different easing curves."""
    print_header("Demo 1: Keyframe Interpolation with Different Curves")
    
    timeline = GlobalTimeline(duration=2.0, frame_rate=10)
    
    # Add keyframes with different interpolation types
    timeline.add_keyframe("linear", 0.0, 0.0, KeyframeInterpolation.LINEAR)
    timeline.add_keyframe("linear", 2.0, 1.0, KeyframeInterpolation.LINEAR)
    
    timeline.add_keyframe("ease_in", 0.0, 0.0, KeyframeInterpolation.EASE_IN)
    timeline.add_keyframe("ease_in", 2.0, 1.0, KeyframeInterpolation.EASE_IN)
    
    timeline.add_keyframe("ease_out", 0.0, 0.0, KeyframeInterpolation.EASE_OUT)
    timeline.add_keyframe("ease_out", 2.0, 1.0, KeyframeInterpolation.EASE_OUT)
    
    timeline.add_keyframe("ease_in_out", 0.0, 0.0, KeyframeInterpolation.EASE_IN_OUT)
    timeline.add_keyframe("ease_in_out", 2.0, 1.0, KeyframeInterpolation.EASE_IN_OUT)
    
    print("\nAnimating from 0.0 to 1.0 over 2 seconds:")
    print("\nTime   | Linear              | Ease In             | Ease Out            | Ease In-Out")
    print("-" * 100)
    
    for frame in range(21):  # 0 to 2 seconds, 0.1s intervals
        time = frame * 0.1
        
        linear = timeline.get_property_value("linear", time)
        ease_in = timeline.get_property_value("ease_in", time)
        ease_out = timeline.get_property_value("ease_out", time)
        ease_in_out = timeline.get_property_value("ease_in_out", time)
        
        print(f"{time:4.1f}s | {visualize_value(linear, width=15)} | "
              f"{visualize_value(ease_in, width=15)} | "
              f"{visualize_value(ease_out, width=15)} | "
              f"{visualize_value(ease_in_out, width=15)}")
    
    print("\n📊 Observation:")
    print("   • Linear: Constant speed throughout")
    print("   • Ease In: Starts slow, speeds up (good for appearances)")
    print("   • Ease Out: Starts fast, slows down (good for stops)")
    print("   • Ease In-Out: Slow at both ends (natural motion)")


def demo_position_animation():
    """Demonstrate animating position (x, y coordinates)."""
    print_header("Demo 2: Position Animation (2D Movement)")
    
    timeline = GlobalTimeline(duration=4.0, frame_rate=10)
    
    # Animate object moving in a path
    timeline.add_keyframe("position", 0.0, {"x": 0, "y": 0}, KeyframeInterpolation.EASE_OUT)
    timeline.add_keyframe("position", 1.0, {"x": 10, "y": 5}, KeyframeInterpolation.LINEAR)
    timeline.add_keyframe("position", 2.0, {"x": 20, "y": 0}, KeyframeInterpolation.LINEAR)
    timeline.add_keyframe("position", 3.0, {"x": 10, "y": -5}, KeyframeInterpolation.EASE_IN)
    timeline.add_keyframe("position", 4.0, {"x": 0, "y": 0}, KeyframeInterpolation.LINEAR)
    
    print("\nObject moving in a diamond pattern:")
    print()
    
    # Create a simple ASCII visualization
    for t in [0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0]:
        pos = timeline.get_property_value("position", t)
        x, y = int(pos['x']), int(pos['y'])
        
        # Create 11x21 grid (y: -5 to 5, x: 0 to 20)
        grid = [[' ' for _ in range(21)] for _ in range(11)]
        
        # Place marker
        grid_y = 5 - y  # Flip y axis for display
        if 0 <= grid_y < 11 and 0 <= x < 21:
            grid[grid_y][x] = '●'
        
        # Draw grid
        print(f"t={t:.1f}s: x={pos['x']:.1f}, y={pos['y']:.1f}")
        print("  " + "-" * 21)
        for row in grid:
            print("  " + ''.join(row) + "|")
        print("  " + "-" * 21)
        print()


def demo_crossfade():
    """Demonstrate crossfade effect."""
    print_header("Demo 3: Crossfade Between Two Layers")
    
    # Load the crossfade example
    with open('example_timeline_crossfade.json', 'r') as f:
        config = json.load(f)
    
    timeline = GlobalTimeline.from_dict(config['timeline'])
    
    print("\nCrossfading from Layer 0 to Layer 1:")
    print("\nTime  | Layer 0 Opacity     | Layer 1 Opacity     | Visual Representation")
    print("-" * 100)
    
    for t in [0.0, 2.0, 4.0, 4.5, 5.0, 5.5, 6.0, 8.0, 10.0]:
        opacity_0 = timeline.get_property_value('layer.0.opacity', t)
        opacity_1 = timeline.get_property_value('layer.1.opacity', t)
        
        # Visual representation
        visual = ""
        if opacity_0 > 0.8:
            visual = "[Layer 0 ████████]"
        elif opacity_1 > 0.8:
            visual = "[Layer 1 ████████]"
        elif 0.2 < opacity_0 < 0.8 or 0.2 < opacity_1 < 0.8:
            visual = "[Transitioning...]"
        
        print(f"{t:4.1f}s| {visualize_value(opacity_0, width=15)} | "
              f"{visualize_value(opacity_1, width=15)} | {visual}")
    
    # Show markers
    print("\n📍 Timeline Markers:")
    for marker in timeline.markers:
        print(f"   {marker.time:4.1f}s - {marker.label} {marker.color}")


def demo_sync_points():
    """Demonstrate synchronized animations."""
    print_header("Demo 4: Synchronized Multi-Element Animation")
    
    timeline = GlobalTimeline(duration=6.0, frame_rate=10)
    
    # Three elements appearing in sync
    for i in range(3):
        timeline.add_keyframe(f"element{i}.opacity", 0.0, 0.0)
        timeline.add_keyframe(f"element{i}.opacity", 2.0, 1.0, KeyframeInterpolation.EASE_IN)
        timeline.add_keyframe(f"element{i}.opacity", 4.0, 1.0)
        timeline.add_keyframe(f"element{i}.opacity", 6.0, 0.0, KeyframeInterpolation.EASE_OUT)
    
    # Add sync points
    timeline.add_sync_point(2.0, ["element0", "element1", "element2"], "All appear")
    timeline.add_sync_point(6.0, ["element0", "element1", "element2"], "All disappear")
    
    print("\nThree elements synchronized:")
    print("\nTime  | Element 0           | Element 1           | Element 2           | Status")
    print("-" * 110)
    
    for t in [0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0]:
        e0 = timeline.get_property_value("element0.opacity", t)
        e1 = timeline.get_property_value("element1.opacity", t)
        e2 = timeline.get_property_value("element2.opacity", t)
        
        status = ""
        if t == 2.0:
            status = "⭐ SYNC: All fully visible"
        elif t == 6.0:
            status = "⭐ SYNC: All hidden"
        
        print(f"{t:4.1f}s| {visualize_value(e0, width=15)} | "
              f"{visualize_value(e1, width=15)} | "
              f"{visualize_value(e2, width=15)} | {status}")


def demo_loop_segment():
    """Demonstrate loop segments."""
    print_header("Demo 5: Loop Segment (Repeating Animation)")
    
    timeline = GlobalTimeline(duration=10.0, frame_rate=10)
    
    # Simple bounce animation
    timeline.add_keyframe("bounce", 0.0, 0.0, KeyframeInterpolation.EASE_OUT)
    timeline.add_keyframe("bounce", 1.0, 1.0, KeyframeInterpolation.EASE_IN)
    timeline.add_keyframe("bounce", 2.0, 0.0, KeyframeInterpolation.LINEAR)
    
    # Add loop
    timeline.add_loop_segment(0.0, 2.0, 3, "Bounce loop")
    
    print("\nBounce animation looping 3 times:")
    print("\nTime  | Value               | Loop Info")
    print("-" * 60)
    
    loop_count = 1
    last_effective_time = -1
    
    for t in range(0, 70, 5):  # 0 to 7 seconds
        time_sec = t / 10.0
        value = timeline.get_property_value("bounce", time_sec)
        effective_time = timeline._apply_loops(time_sec)
        
        # Detect loop boundary
        if effective_time < last_effective_time:
            loop_count += 1
        last_effective_time = effective_time
        
        loop_info = f"Loop #{loop_count}" if time_sec < 6.0 else "After loops"
        
        print(f"{time_sec:4.1f}s| {visualize_value(value, width=15)} | {loop_info}")


def demo_time_remapping():
    """Demonstrate time remapping (slow motion)."""
    print_header("Demo 6: Time Remapping (Slow Motion Effect)")
    
    timeline = GlobalTimeline(duration=10.0, frame_rate=10)
    
    # Simple linear animation
    timeline.add_keyframe("value", 0.0, 0.0)
    timeline.add_keyframe("value", 10.0, 10.0)
    
    # Add slow motion from 4s to 6s (stretched to 8s)
    timeline.add_time_remapping(4.0, 6.0, 4.0, 8.0, KeyframeInterpolation.LINEAR)
    
    print("\nLinear animation with slow motion from 4-6s:")
    print("\nReal Time | Remapped Time | Value               | Effect")
    print("-" * 70)
    
    for t in [0.0, 2.0, 4.0, 5.0, 6.0, 7.0, 8.0, 10.0]:
        remapped = timeline.get_remapped_time(t)
        value = timeline.get_property_value("value", remapped)
        
        effect = ""
        if 4.0 <= t <= 8.0:
            effect = "🐌 SLOW MOTION"
        
        print(f"{t:8.1f}s | {remapped:11.1f}s | {visualize_value(value, 0, 10, width=15)} | {effect}")
    
    print("\n📊 Notice: Between 4-8s real time, animation only progresses from 4-6 (slower)")


def main():
    """Run all demonstrations."""
    print("\n" + "="*70)
    print("  TIMELINE SYSTEM - VISUAL DEMONSTRATIONS")
    print("="*70)
    print("\nThis demo shows all timeline features in action with ASCII visualizations.")
    
    try:
        demo_keyframe_interpolation()
        input("\n[Press Enter to continue...]")
        
        demo_position_animation()
        input("\n[Press Enter to continue...]")
        
        demo_crossfade()
        input("\n[Press Enter to continue...]")
        
        demo_sync_points()
        input("\n[Press Enter to continue...]")
        
        demo_loop_segment()
        input("\n[Press Enter to continue...]")
        
        demo_time_remapping()
        
        print("\n" + "="*70)
        print("  DEMO COMPLETE!")
        print("="*70)
        print("\n✨ All timeline features demonstrated successfully!")
        print("\n📚 For more information:")
        print("   • Quick Start: TIMELINE_QUICKSTART.md")
        print("   • Complete Guide: TIMELINE_GUIDE.md")
        print("   • Implementation: TIMELINE_IMPLEMENTATION_SUMMARY.md")
        print("\n🎬 Ready to create amazing animations!")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Demo interrupted by user.")
    except Exception as e:
        print(f"\n\n❌ Error during demo: {e}")


if __name__ == "__main__":
    main()
