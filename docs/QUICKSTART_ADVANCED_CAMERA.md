# Quick Start: Advanced Camera System

## Basic Concept

The advanced camera system allows you to define multiple camera views on a single slide, creating cinematic movements similar to the example shown in the issue.

## Visual Example

```
┌─────────────────────────────────────────────┐
│          SLIDE CONTENT (Full Image)          │
│                                               │
│   ┌─────────────┐                            │
│   │  Camera 1   │  ← Start: Overview         │
│   │  (zoom 1.0) │                            │
│   └─────────────┘                            │
│                                               │
│        ┌──────────┐                          │
│        │ Camera 2 │  ← Zoom to detail       │
│        │(zoom 1.8)│    with transition       │
│        └──────────┘                          │
│                                               │
│                     ┌──────────┐             │
│                     │ Camera 3 │  ← Pan to   │
│                     │(zoom 1.8)│    another  │
│                     └──────────┘    detail   │
│                                               │
│   ┌─────────────┐                            │
│   │  Camera 4   │  ← Return to overview      │
│   │  (zoom 1.0) │                            │
│   └─────────────┘                            │
│                                               │
└─────────────────────────────────────────────┘
```

## Minimal Example

```json
{
  "slides": [
    {
      "index": 0,
      "duration": 10,
      "layers": [
        {
          "image_path": "your_image.png",
          "position": {"x": 0, "y": 0},
          "z_index": 1,
          "skip_rate": 10
        }
      ],
      "cameras": [
        {
          "zoom": 1.0,
          "position": {"x": 0.5, "y": 0.5},
          "duration": 2.0
        },
        {
          "zoom": 2.0,
          "position": {"x": 0.7, "y": 0.3},
          "duration": 2.0,
          "transition_duration": 1.0,
          "easing": "ease_out"
        }
      ]
    }
  ]
}
```

## Timeline Example

For the configuration above:

```
Time:  0s    2s    3s    5s
       │     │     │     │
       ▼     ▼     ▼     ▼
       ┌─────┬─────┬─────┐
       │Cam 1│Trans│Cam 2│
       │Hold │ i-  │Hold │
       │2.0s │tion │2.0s │
       │     │1.0s │     │
       └─────┴─────┴─────┘

Camera 1: Overview at zoom 1.0 for 2 seconds
Transition: Smooth zoom from 1.0 to 2.0 over 1 second
Camera 2: Detail at zoom 2.0 for 2 seconds
```

## Key Parameters Explained

### zoom
- `1.0` = Normal view (no zoom)
- `2.0` = 2x zoom (shows half the image)
- Higher = closer/more zoomed

### position
- `{"x": 0.5, "y": 0.5}` = Center of image
- `{"x": 0.0, "y": 0.0}` = Top-left corner
- `{"x": 1.0, "y": 1.0}` = Bottom-right corner
- Values between 0.0 and 1.0

### duration
- Time in seconds to hold this camera view
- Does NOT include transition time

### transition_duration
- Time in seconds to transition FROM previous camera
- Set to 0 for instant cut

### easing
- `"ease_out"` = Smooth deceleration (recommended)
- `"linear"` = Constant speed
- `"ease_in"` = Smooth acceleration
- See ADVANCED_CAMERA_GUIDE.md for all options

## Common Use Cases

### 1. Overview → Detail → Overview
```json
"cameras": [
  {
    "zoom": 1.0,
    "position": {"x": 0.5, "y": 0.5},
    "duration": 2.0
  },
  {
    "zoom": 2.0,
    "position": {"x": 0.6, "y": 0.4},
    "duration": 3.0,
    "transition_duration": 1.0,
    "easing": "ease_out"
  },
  {
    "zoom": 1.0,
    "position": {"x": 0.5, "y": 0.5},
    "duration": 1.5,
    "transition_duration": 1.0,
    "easing": "ease_out"
  }
]
```

### 2. Pan Across Image
```json
"cameras": [
  {
    "zoom": 1.5,
    "position": {"x": 0.2, "y": 0.5},
    "duration": 2.0
  },
  {
    "zoom": 1.5,
    "position": {"x": 0.8, "y": 0.5},
    "duration": 2.0,
    "transition_duration": 2.0,
    "easing": "linear"
  }
]
```

### 3. Multiple Detail Views
```json
"cameras": [
  {
    "zoom": 1.0,
    "position": {"x": 0.5, "y": 0.5},
    "duration": 1.5
  },
  {
    "zoom": 1.8,
    "position": {"x": 0.3, "y": 0.3},
    "duration": 2.0,
    "transition_duration": 0.8,
    "easing": "ease_out"
  },
  {
    "zoom": 1.8,
    "position": {"x": 0.7, "y": 0.3},
    "duration": 2.0,
    "transition_duration": 1.0,
    "easing": "ease_out"
  },
  {
    "zoom": 1.8,
    "position": {"x": 0.5, "y": 0.7},
    "duration": 2.0,
    "transition_duration": 1.0,
    "easing": "ease_out"
  }
]
```

## Running Your First Example

1. Create a configuration file (e.g., `my_cameras.json`)
2. Add your image and camera definitions
3. Run:
   ```bash
   python whiteboard_animator.py --config my_cameras.json --frame-rate 30
   ```

## Tips for Success

✅ **Start simple**: Use 2-3 cameras first
✅ **Test positions**: Use zoom 1.0 first to see what areas are interesting
✅ **Smooth transitions**: `ease_out` works best for most cases
✅ **Timing**: Give viewers 2-3 seconds to absorb each view
✅ **Return to overview**: Help viewers maintain context

## Troubleshooting

**Camera shows wrong area?**
- Check position values (0.5, 0.5 is center, not 0, 0)
- Test with zoom 1.0 first

**Transition too fast/slow?**
- Adjust `transition_duration`
- Try different easing functions

**Video too long/short?**
- Sum all durations + transition_durations
- Adjust individual camera durations

## Next Steps

- Read [ADVANCED_CAMERA_GUIDE.md](ADVANCED_CAMERA_GUIDE.md) for complete documentation
- See [example_advanced_cameras.json](example_advanced_cameras.json) for more examples
- Check [CONFIG_FORMAT.md](CONFIG_FORMAT.md) for all configuration options
