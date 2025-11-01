# Timeline System - Quick Start Guide

Get started with the Timeline and Synchronization system in 5 minutes!

## 📋 What You'll Learn

- How to create simple keyframe animations
- How to add time markers
- How to synchronize multiple elements
- Basic examples you can run immediately

---

## 🚀 Quick Example 1: Fade Transition

**Goal:** Create a smooth crossfade between two images.

### 1. Create your config file: `timeline_fade.json`

```json
{
  "slides": [
    {
      "index": 0,
      "duration": 10,
      "layers": [
        {
          "image_path": "demo/1.jpg",
          "z_index": 1
        },
        {
          "image_path": "demo/2.jpg",
          "z_index": 2
        }
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
          {"time": 4.0, "value": 1.0},
          {"time": 6.0, "value": 0.0, "interpolation": "ease_out"}
        ]
      },
      "layer.1.opacity": {
        "keyframes": [
          {"time": 0.0, "value": 0.0},
          {"time": 4.0, "value": 0.0},
          {"time": 6.0, "value": 1.0, "interpolation": "ease_in"}
        ]
      }
    }
  }
}
```

### 2. Run it

```bash
python whiteboard_animator.py --config timeline_fade.json
```

### 3. What happens?

- **0-4 seconds**: First image visible, second image hidden
- **4-6 seconds**: Smooth crossfade transition
- **6-10 seconds**: Second image visible, first image hidden

---

## 🎯 Quick Example 2: Add Time Markers

**Goal:** Add visual markers to organize your timeline.

Just add a `markers` section to your timeline:

```json
{
  "timeline": {
    "markers": [
      {"time": 0.0, "label": "Start", "color": "#00FF00"},
      {"time": 4.0, "label": "Crossfade", "color": "#FFFF00"},
      {"time": 10.0, "label": "End", "color": "#FF0000"}
    ]
  }
}
```

Markers help you:
- Visualize important moments
- Document your timeline
- Plan complex sequences

---

## 🔄 Quick Example 3: Synchronized Animation

**Goal:** Make multiple elements appear at the same time.

```json
{
  "slides": [
    {
      "index": 0,
      "duration": 10,
      "layers": [
        {"image_path": "demo/1.jpg", "z_index": 1},
        {"image_path": "demo/2.jpg", "z_index": 2},
        {"image_path": "demo/3.jpeg", "z_index": 3}
      ]
    }
  ],
  "timeline": {
    "duration": 10.0,
    "property_tracks": {
      "layer.0.opacity": {
        "keyframes": [
          {"time": 0.0, "value": 0.0},
          {"time": 2.0, "value": 1.0, "interpolation": "ease_in"}
        ]
      },
      "layer.1.opacity": {
        "keyframes": [
          {"time": 0.0, "value": 0.0},
          {"time": 2.0, "value": 1.0, "interpolation": "ease_in"}
        ]
      },
      "layer.2.opacity": {
        "keyframes": [
          {"time": 0.0, "value": 0.0},
          {"time": 2.0, "value": 1.0, "interpolation": "ease_in"}
        ]
      }
    },
    "sync_points": [
      {
        "time": 2.0,
        "elements": ["layer.0", "layer.1", "layer.2"],
        "label": "All appear together"
      }
    ]
  }
}
```

All three layers fade in perfectly synchronized!

---

## 🎨 Interpolation Types Cheat Sheet

| Type | When to Use | Effect |
|------|-------------|--------|
| `linear` | Default, steady motion | Constant speed |
| `ease_in` | Elements appearing | Slow start, fast end |
| `ease_out` | Elements stopping | Fast start, slow end |
| `ease_in_out` | Natural movement | Slow start and end |

Example:
```json
{
  "keyframes": [
    {"time": 0.0, "value": 0.0},
    {"time": 2.0, "value": 1.0, "interpolation": "ease_in_out"}
  ]
}
```

---

## 🔁 Quick Example 4: Loop Animation

**Goal:** Repeat an animation 3 times.

```json
{
  "timeline": {
    "duration": 15.0,
    "property_tracks": {
      "layer.0.position": {
        "keyframes": [
          {"time": 0.0, "value": {"x": 0, "y": 0}},
          {"time": 2.0, "value": {"x": 100, "y": 0}},
          {"time": 4.0, "value": {"x": 0, "y": 0}}
        ]
      }
    },
    "loop_segments": [
      {
        "start_time": 0.0,
        "end_time": 4.0,
        "loop_count": 3,
        "label": "Bounce loop"
      }
    ]
  }
}
```

The animation from 0-4 seconds repeats 3 times!

---

## ⚡ Quick Example 5: Slow Motion

**Goal:** Slow down a 2-second segment to 4 seconds.

```json
{
  "timeline": {
    "time_remappings": [
      {
        "original_start": 5.0,
        "original_end": 7.0,
        "remapped_start": 5.0,
        "remapped_end": 9.0,
        "curve": "ease_in_out"
      }
    ]
  }
}
```

The 2-second segment now plays in slow motion over 4 seconds!

---

## 📝 Property Paths Reference

Common property paths you can animate:

### Layer Properties
- `layer.0.opacity` - Transparency (0.0 to 1.0)
- `layer.0.position` - Position `{"x": 0, "y": 0}`
- `layer.0.scale` - Size (1.0 = original)

### Numbers
Just use numbers: `0.0`, `1.0`, `0.5`

### Positions
Use objects: `{"x": 100, "y": 50}`

### Colors (future)
Use tuples: `[255, 0, 0]` for RGB

---

## ✅ Testing Your Timeline

### Option 1: Python API Test

```python
from timeline_system import GlobalTimeline, KeyframeInterpolation

# Create timeline
timeline = GlobalTimeline(duration=10.0, frame_rate=30)

# Add keyframes
timeline.add_keyframe("layer.0.opacity", 0.0, 0.0)
timeline.add_keyframe("layer.0.opacity", 2.0, 1.0)

# Test a value
opacity_at_1s = timeline.get_property_value("layer.0.opacity", 1.0)
print(f"Opacity at 1.0s: {opacity_at_1s}")  # Should be 0.5
```

### Option 2: Run Unit Tests

```bash
python test_timeline.py
```

---

## 🎓 Next Steps

Ready for more? Check out:

1. **[TIMELINE_GUIDE.md](TIMELINE_GUIDE.md)** - Complete feature documentation
2. **Example configs**:
   - `example_timeline_crossfade.json` - Simple crossfade
   - `example_timeline_sequence.json` - Multi-element sequence
   - `example_timeline_advanced.json` - Loops and time remapping

3. **Integration** - See how to integrate timeline with whiteboard animator

---

## 💡 Tips for Beginners

1. **Start Simple**: Begin with opacity animations before complex movements
2. **Use Round Numbers**: Use 1.0, 2.0, 3.0 for easier calculation
3. **Add Markers Early**: Mark important points as you build
4. **Test Incrementally**: Test each keyframe before adding more
5. **Check Your JSON**: Use a JSON validator if you get errors

---

## 🐛 Common Issues

### "Property not found"
✅ Check spelling: `layer.0.opacity` not `layer[0].opacity`

### "Keyframe outside timeline"
✅ Ensure keyframe time < timeline duration

### "Invalid JSON"
✅ Check for missing commas, brackets, quotes

### "No animation happening"
✅ Verify keyframe times are different
✅ Check values actually change between keyframes

---

## 📞 Need Help?

- Check test examples in `test_timeline.py`
- Review complete guide in `TIMELINE_GUIDE.md`
- Look at provided example configs

**Happy animating!** 🎬
