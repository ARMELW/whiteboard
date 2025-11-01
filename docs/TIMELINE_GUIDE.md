# Timeline and Synchronization System - User Guide

## Overview

The Timeline and Synchronization system provides advanced control over timing and animation synchronization in your whiteboard videos. This guide covers all features:

1. **Global Timeline** - Timeline spanning multiple slides
2. **Keyframe System** - Universal keyframe-based animations
3. **Time Markers** - Visual markers for navigation
4. **Sync Points** - Synchronization between multiple elements
5. **Animation Curves** - Advanced easing functions
6. **Time Remapping** - Speed up or slow down time segments
7. **Loop Segments** - Repeat portions of your animation

## 📖 Table of Contents

- [Configuration Format](#configuration-format)
- [Keyframe System](#keyframe-system)
- [Time Markers](#time-markers)
- [Sync Points](#sync-points)
- [Animation Curves](#animation-curves)
- [Time Remapping](#time-remapping)
- [Loop Segments](#loop-segments)
- [Complete Examples](#complete-examples)

---

## Configuration Format

Timeline features are configured through a `timeline` section in your JSON config:

```json
{
  "slides": [...],
  "timeline": {
    "duration": 30.0,
    "frame_rate": 30,
    "property_tracks": {...},
    "markers": [...],
    "sync_points": [...],
    "loop_segments": [...],
    "time_remappings": [...]
  }
}
```

---

## Keyframe System

### What are Keyframes?

Keyframes define the value of a property at specific points in time. The system automatically interpolates between keyframes.

### Supported Properties

You can animate any property using keyframes:

- **Layer properties**: `layer.0.opacity`, `layer.0.position`, `layer.0.scale`
- **Camera properties**: `camera.zoom`, `camera.position`
- **Text properties**: `text.0.opacity`, `text.0.color`
- **Custom properties**: Any property path you define

### Basic Keyframe Example

```json
{
  "timeline": {
    "property_tracks": {
      "layer.0.opacity": {
        "keyframes": [
          {"time": 0.0, "value": 0.0, "interpolation": "ease_in"},
          {"time": 2.0, "value": 1.0, "interpolation": "linear"},
          {"time": 5.0, "value": 1.0, "interpolation": "ease_out"},
          {"time": 7.0, "value": 0.0, "interpolation": "linear"}
        ]
      }
    }
  }
}
```

### Interpolation Types

| Type | Description | Use Case |
|------|-------------|----------|
| `linear` | Constant speed | Default, smooth transitions |
| `ease_in` | Slow start | Elements appearing |
| `ease_out` | Slow end | Elements stopping |
| `ease_in_out` | Slow start and end | Natural motion |
| `ease_in_cubic` | Very slow start | Dramatic appearances |
| `ease_out_cubic` | Very slow end | Dramatic stops |
| `step` | No interpolation, instant jump | State changes |
| `bezier` | Custom cubic bezier curve | Advanced control |

### Position Keyframes

Animate x,y coordinates:

```json
{
  "property_tracks": {
    "layer.0.position": {
      "keyframes": [
        {"time": 0.0, "value": {"x": 0, "y": 0}, "interpolation": "ease_out"},
        {"time": 2.0, "value": {"x": 100, "y": 50}, "interpolation": "ease_in"},
        {"time": 4.0, "value": {"x": 200, "y": 100}, "interpolation": "linear"}
      ]
    }
  }
}
```

### Multiple Property Animation

Animate multiple properties simultaneously:

```json
{
  "property_tracks": {
    "layer.0.opacity": {
      "keyframes": [
        {"time": 0.0, "value": 0.0},
        {"time": 1.0, "value": 1.0}
      ]
    },
    "layer.0.scale": {
      "keyframes": [
        {"time": 0.0, "value": 0.5},
        {"time": 1.0, "value": 1.0}
      ]
    },
    "layer.0.position": {
      "keyframes": [
        {"time": 0.0, "value": {"x": 0, "y": 0}},
        {"time": 1.0, "value": {"x": 50, "y": 25}}
      ]
    }
  }
}
```

### Bezier Curves (Advanced)

For ultimate control, use custom bezier curves:

```json
{
  "keyframes": [
    {
      "time": 0.0, 
      "value": 0.0, 
      "interpolation": "bezier",
      "bezier_handles": [0.42, 0.0, 0.58, 1.0]
    },
    {
      "time": 2.0,
      "value": 1.0
    }
  ]
}
```

Bezier handles format: `[cp1x, cp1y, cp2x, cp2y]` where:
- `cp1x, cp1y`: First control point (0-1 range)
- `cp2x, cp2y`: Second control point (0-1 range)

Common bezier presets:
- **Ease**: `[0.25, 0.1, 0.25, 1.0]`
- **Ease-in**: `[0.42, 0.0, 1.0, 1.0]`
- **Ease-out**: `[0.0, 0.0, 0.58, 1.0]`
- **Ease-in-out**: `[0.42, 0.0, 0.58, 1.0]`

---

## Time Markers

### Purpose

Time markers help you navigate and organize your timeline visually.

### Configuration

```json
{
  "timeline": {
    "markers": [
      {
        "time": 2.0,
        "label": "Scene 1",
        "color": "#FF0000",
        "metadata": {
          "description": "Introduction sequence"
        }
      },
      {
        "time": 5.0,
        "label": "Scene 2",
        "color": "#00FF00",
        "metadata": {
          "description": "Main content"
        }
      },
      {
        "time": 8.0,
        "label": "Scene 3",
        "color": "#0000FF",
        "metadata": {
          "description": "Conclusion"
        }
      }
    ]
  }
}
```

### Properties

- **time**: Position on timeline in seconds
- **label**: Human-readable name
- **color**: Hex color for UI (optional)
- **metadata**: Additional data (optional)

### Use Cases

- **Scene boundaries**: Mark where scenes start/end
- **Important events**: Highlight key moments
- **Navigation**: Jump to specific points in long videos
- **Notes**: Add comments for collaboration

---

## Sync Points

### Purpose

Sync points ensure multiple elements start, stop, or change at exactly the same time.

### Configuration

```json
{
  "timeline": {
    "sync_points": [
      {
        "time": 3.0,
        "elements": ["layer.0", "layer.1", "text.0"],
        "label": "All appear together",
        "metadata": {
          "action": "appear"
        }
      },
      {
        "time": 6.0,
        "elements": ["layer.0", "layer.1"],
        "label": "Both fade out",
        "metadata": {
          "action": "fade_out"
        }
      }
    ]
  }
}
```

### Properties

- **time**: Synchronization point in seconds
- **elements**: List of element IDs to synchronize
- **label**: Description of sync point
- **metadata**: Additional context

### Use Cases

- **Coordinated appearance**: Multiple elements appear together
- **Synchronized transitions**: Elements change state together
- **Timing reference**: Ensure animations stay in sync
- **Complex choreography**: Multi-element sequences

---

## Animation Curves

### Visual Comparison

```
LINEAR:        EASE_IN:       EASE_OUT:      EASE_IN_OUT:
│     /        │    /         │  /            │   ___/
│   /          │   /          │ /             │  /
│ /            │ /            │/              │ /
│/             │/             /               │/
────────       ────────       ────────        ────────
```

### Choosing the Right Curve

| Animation Type | Recommended Curve | Reason |
|----------------|-------------------|--------|
| Fade in | `ease_in` | Gradual appearance feels natural |
| Fade out | `ease_out` | Smooth disappearance |
| Slide in | `ease_out` | Deceleration at end position |
| Slide out | `ease_in` | Acceleration away |
| Zoom in | `ease_in_out` | Smooth start and stop |
| Position change | `ease_out` | Natural movement |
| State toggle | `step` | Instant change |

### Examples

#### Fade In with Ease

```json
{
  "layer.0.opacity": {
    "keyframes": [
      {"time": 0.0, "value": 0.0, "interpolation": "ease_in"},
      {"time": 1.5, "value": 1.0}
    ]
  }
}
```

#### Bouncy Scale Animation

```json
{
  "layer.0.scale": {
    "keyframes": [
      {"time": 0.0, "value": 0.0, "interpolation": "ease_out_cubic"},
      {"time": 0.8, "value": 1.2, "interpolation": "ease_in_out"},
      {"time": 1.5, "value": 1.0}
    ]
  }
}
```

---

## Time Remapping

### Purpose

Time remapping allows you to speed up, slow down, or reverse time in specific segments.

### Configuration

```json
{
  "timeline": {
    "time_remappings": [
      {
        "original_start": 2.0,
        "original_end": 4.0,
        "remapped_start": 2.0,
        "remapped_end": 6.0,
        "curve": "ease_in_out"
      }
    ]
  }
}
```

### How It Works

In this example:
- Original segment: 2.0s → 4.0s (2 seconds duration)
- Remapped segment: 2.0s → 6.0s (4 seconds duration)
- **Effect**: This segment plays at 50% speed (slow motion)

### Use Cases

#### Slow Motion

Make a 2-second segment last 6 seconds:

```json
{
  "original_start": 5.0,
  "original_end": 7.0,
  "remapped_start": 5.0,
  "remapped_end": 11.0,
  "curve": "linear"
}
```

#### Fast Forward

Make a 4-second segment last 1 second:

```json
{
  "original_start": 10.0,
  "original_end": 14.0,
  "remapped_start": 10.0,
  "remapped_end": 11.0,
  "curve": "linear"
}
```

#### Reverse Time (Conceptual)

```json
{
  "original_start": 15.0,
  "original_end": 18.0,
  "remapped_start": 18.0,
  "remapped_end": 15.0,
  "curve": "linear"
}
```

### Curves with Time Remapping

Apply easing to the speed change itself:

- `linear`: Constant speed change
- `ease_in_out`: Gradually speed up/slow down
- `ease_in`: Gradually enter slow/fast motion
- `ease_out`: Gradually exit slow/fast motion

---

## Loop Segments

### Purpose

Loop segments repeat a portion of your animation multiple times.

### Configuration

```json
{
  "timeline": {
    "loop_segments": [
      {
        "start_time": 2.0,
        "end_time": 4.0,
        "loop_count": 3,
        "label": "Intro loop"
      }
    ]
  }
}
```

### Properties

- **start_time**: Loop start in seconds
- **end_time**: Loop end in seconds
- **loop_count**: Number of times to loop
- **label**: Description (optional)

### Use Cases

#### Background Animation Loop

Loop a background animation while foreground progresses:

```json
{
  "start_time": 0.0,
  "end_time": 2.0,
  "loop_count": 5,
  "label": "Background pattern"
}
```

#### Waiting State

Loop an idle animation:

```json
{
  "start_time": 5.0,
  "end_time": 6.0,
  "loop_count": 4,
  "label": "Character idle"
}
```

#### Emphasis

Repeat an action for emphasis:

```json
{
  "start_time": 10.0,
  "end_time": 11.0,
  "loop_count": 3,
  "label": "Attention grabber"
}
```

---

## Complete Examples

### Example 1: Simple Fade Sequence

```json
{
  "slides": [
    {
      "index": 0,
      "duration": 10,
      "layers": [
        {"image_path": "image1.png", "z_index": 1},
        {"image_path": "image2.png", "z_index": 2}
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
          {"time": 4.0, "value": 0.0, "interpolation": "ease_out"}
        ]
      },
      "layer.1.opacity": {
        "keyframes": [
          {"time": 0.0, "value": 0.0},
          {"time": 4.0, "value": 1.0, "interpolation": "ease_in"}
        ]
      }
    },
    "markers": [
      {"time": 0.0, "label": "Start"},
      {"time": 4.0, "label": "Crossfade"},
      {"time": 10.0, "label": "End"}
    ]
  }
}
```

### Example 2: Complex Multi-Element Animation

```json
{
  "slides": [
    {
      "index": 0,
      "duration": 15,
      "layers": [
        {"image_path": "background.png", "z_index": 1},
        {"image_path": "element1.png", "z_index": 2},
        {"image_path": "element2.png", "z_index": 3},
        {"image_path": "element3.png", "z_index": 4}
      ]
    }
  ],
  "timeline": {
    "duration": 15.0,
    "frame_rate": 30,
    "property_tracks": {
      "layer.1.opacity": {
        "keyframes": [
          {"time": 0.0, "value": 0.0},
          {"time": 1.0, "value": 1.0, "interpolation": "ease_in"}
        ]
      },
      "layer.1.position": {
        "keyframes": [
          {"time": 0.0, "value": {"x": -100, "y": 0}},
          {"time": 1.0, "value": {"x": 0, "y": 0}, "interpolation": "ease_out"}
        ]
      },
      "layer.2.opacity": {
        "keyframes": [
          {"time": 2.0, "value": 0.0},
          {"time": 3.0, "value": 1.0, "interpolation": "ease_in"}
        ]
      },
      "layer.2.scale": {
        "keyframes": [
          {"time": 2.0, "value": 0.5},
          {"time": 3.0, "value": 1.0, "interpolation": "ease_out"}
        ]
      },
      "layer.3.opacity": {
        "keyframes": [
          {"time": 4.0, "value": 0.0},
          {"time": 5.0, "value": 1.0, "interpolation": "ease_in"}
        ]
      }
    },
    "sync_points": [
      {
        "time": 1.0,
        "elements": ["layer.1"],
        "label": "Element 1 appears"
      },
      {
        "time": 3.0,
        "elements": ["layer.2"],
        "label": "Element 2 appears"
      },
      {
        "time": 5.0,
        "elements": ["layer.3"],
        "label": "Element 3 appears"
      }
    ],
    "markers": [
      {"time": 0.0, "label": "Start", "color": "#00FF00"},
      {"time": 5.0, "label": "All visible", "color": "#FFFF00"},
      {"time": 15.0, "label": "End", "color": "#FF0000"}
    ]
  }
}
```

### Example 3: Loop and Time Remap

```json
{
  "timeline": {
    "duration": 20.0,
    "frame_rate": 30,
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
        "label": "Bouncing loop"
      }
    ],
    "time_remappings": [
      {
        "original_start": 12.0,
        "original_end": 14.0,
        "remapped_start": 12.0,
        "remapped_end": 18.0,
        "curve": "ease_in_out"
      }
    ],
    "markers": [
      {"time": 0.0, "label": "Loop start"},
      {"time": 12.0, "label": "Slow motion start"},
      {"time": 18.0, "label": "Normal speed resume"}
    ]
  }
}
```

---

## Best Practices

### 1. **Keep it Simple**
Start with basic keyframes before adding complex features.

### 2. **Use Markers**
Always add markers at important points for easier editing.

### 3. **Test Interpolation**
Preview different easing curves to find what feels right.

### 4. **Sync Points for Coordination**
Use sync points instead of trying to match times manually.

### 5. **Consistent Timing**
Use round numbers (1.0, 2.0, 3.0) for easier calculation.

### 6. **Comment Your Config**
While JSON doesn't support comments, use descriptive labels in markers and sync points.

### 7. **Incremental Development**
Build your timeline step by step, testing as you go.

---

## Troubleshooting

### Keyframes Not Working

- ✅ Check property path is correct (e.g., `layer.0.opacity` not `layer[0].opacity`)
- ✅ Ensure keyframe times are within timeline duration
- ✅ Verify JSON syntax is valid

### Unexpected Interpolation

- ✅ Check interpolation type on the **first** keyframe of each pair
- ✅ Remember: interpolation applies from that keyframe to the next

### Elements Not Syncing

- ✅ Verify element IDs in sync points match actual elements
- ✅ Check that sync point time is within timeline duration

### Loops Not Playing

- ✅ Ensure loop segment times are within timeline bounds
- ✅ Check loop_count is > 1

---

## API Reference

For programmatic use, see `timeline_system.py`:

```python
from timeline_system import GlobalTimeline, KeyframeInterpolation

# Create timeline
timeline = GlobalTimeline(duration=10.0, frame_rate=30)

# Add keyframe
timeline.add_keyframe(
    property_path="layer.0.opacity",
    time=0.0,
    value=0.0,
    interpolation=KeyframeInterpolation.EASE_IN
)

# Add marker
timeline.add_marker(time=2.0, label="Scene 1", color="#FF0000")

# Get value at time
opacity = timeline.get_property_value("layer.0.opacity", 1.5)

# Export to dict
data = timeline.to_dict()

# Import from dict
timeline2 = GlobalTimeline.from_dict(data)
```

---

## Additional Resources

- See `test_timeline.py` for usage examples
- Check `timeline_system.py` for implementation details
- Refer to main documentation for integration with whiteboard animator

---

**Happy animating!** 🎬
