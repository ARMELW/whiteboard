# Advanced Camera System Guide

This guide explains the advanced camera system in Whiteboard-It, which allows you to define multiple camera views per slide with smooth transitions between them.

## Table of Contents
- [Overview](#overview)
- [Camera Properties](#camera-properties)
- [Camera Sequences](#camera-sequences)
- [Easing Functions](#easing-functions)
- [Configuration Examples](#configuration-examples)
- [Best Practices](#best-practices)

## Overview

The advanced camera system lets you:
- Define multiple cameras per slide
- Automatically transition between camera views
- Control camera size, position, and zoom
- Apply easing functions for smooth transitions
- Create cinematic camera movements

### Key Concepts

- **Camera**: A viewpoint with position, zoom, and optional size
- **Camera Sequence**: Multiple cameras shown in order with transitions
- **Transition**: Smooth movement from one camera to another
- **Easing**: Mathematical function controlling the acceleration/deceleration of transitions

## Camera Properties

Each camera in a sequence can have the following properties:

| Property | Type | Description | Default |
|----------|------|-------------|---------|
| `zoom` | float | Zoom level (1.0 = normal, 2.0 = 2x zoom) | 1.0 |
| `position` | object | Focus position with `x` and `y` (0.0-1.0) | `{"x": 0.5, "y": 0.5}` |
| `size` | object | Camera viewport size with `width` and `height` in pixels | Based on aspect ratio |
| `duration` | float | How long to hold this camera view (seconds) | 2.0 |
| `transition_duration` | float | Time to transition from previous camera (seconds) | 0 |
| `easing` | string | Easing function for transition | `"ease_out"` |

### Position System

Positions use normalized coordinates (0.0 to 1.0):
- `x: 0.0, y: 0.0` = Top-left corner
- `x: 0.5, y: 0.5` = Center
- `x: 1.0, y: 1.0` = Bottom-right corner

### Camera Size

The `size` property defines the camera's viewport dimensions:
- By default, size is calculated from zoom and aspect ratio
- You can specify explicit dimensions: `{"width": 2275, "height": 1280}`
- Dimensions are in pixels and define what the camera "sees"

## Camera Sequences

Camera sequences are defined at the **slide level** (not layer level) using the `cameras` array:

```json
{
  "slides": [
    {
      "index": 0,
      "duration": 10,
      "layers": [...],
      "cameras": [
        {
          "zoom": 1.0,
          "position": {"x": 0.5, "y": 0.5},
          "duration": 2.0
        },
        {
          "zoom": 1.5,
          "position": {"x": 0.3, "y": 0.3},
          "duration": 2.0,
          "transition_duration": 1.0,
          "easing": "ease_out"
        }
      ]
    }
  ]
}
```

## Easing Functions

Easing functions control the acceleration/deceleration of camera transitions:

| Easing Type | Description | Use Case |
|-------------|-------------|----------|
| `linear` | Constant speed | Simple movements |
| `ease_in` | Slow start, fast end | Dramatic reveals |
| `ease_out` | Fast start, slow end | **Recommended for camera movements** |
| `ease_in_out` | Slow start and end | Smooth bidirectional |
| `ease_in_cubic` | Very slow start | Extremely dramatic |
| `ease_out_cubic` | Very slow end | Extremely smooth stops |

**Recommendation**: Use `ease_out` for most camera movements as it feels most natural.

## Configuration Examples

### Example 1: Simple Camera Sequence

Two cameras with a smooth transition:

```json
{
  "slides": [
    {
      "index": 0,
      "duration": 10,
      "layers": [
        {
          "image_path": "diagram.png",
          "position": {"x": 0, "y": 0},
          "z_index": 1,
          "skip_rate": 10
        }
      ],
      "cameras": [
        {
          "zoom": 1.0,
          "position": {"x": 0.5, "y": 0.5},
          "duration": 3.0
        },
        {
          "zoom": 2.0,
          "position": {"x": 0.7, "y": 0.3},
          "duration": 3.0,
          "transition_duration": 1.5,
          "easing": "ease_out"
        }
      ]
    }
  ]
}
```

### Example 2: Multiple Camera Views

Showcase different areas of a complex diagram:

```json
{
  "slides": [
    {
      "index": 0,
      "duration": 15,
      "layers": [
        {
          "image_path": "complex_diagram.png",
          "position": {"x": 0, "y": 0},
          "z_index": 1,
          "skip_rate": 8
        }
      ],
      "cameras": [
        {
          "zoom": 1.0,
          "position": {"x": 0.5, "y": 0.5},
          "duration": 2.0,
          "comment": "Overview"
        },
        {
          "zoom": 1.8,
          "position": {"x": 0.3, "y": 0.25},
          "duration": 2.5,
          "transition_duration": 1.0,
          "easing": "ease_out",
          "comment": "Top-left detail"
        },
        {
          "zoom": 1.8,
          "position": {"x": 0.7, "y": 0.25},
          "duration": 2.5,
          "transition_duration": 1.0,
          "easing": "ease_out",
          "comment": "Top-right detail"
        },
        {
          "zoom": 1.8,
          "position": {"x": 0.5, "y": 0.75},
          "duration": 2.5,
          "transition_duration": 1.0,
          "easing": "ease_out",
          "comment": "Bottom center detail"
        },
        {
          "zoom": 1.0,
          "position": {"x": 0.5, "y": 0.5},
          "duration": 1.5,
          "transition_duration": 1.0,
          "easing": "ease_out",
          "comment": "Return to overview"
        }
      ]
    }
  ]
}
```

### Example 3: Custom Camera Size

Using specific camera dimensions (e.g., 2275.6 x 1280):

```json
{
  "slides": [
    {
      "index": 0,
      "duration": 8,
      "layers": [
        {
          "image_path": "presentation.png",
          "position": {"x": 0, "y": 0},
          "z_index": 1,
          "skip_rate": 10
        }
      ],
      "cameras": [
        {
          "size": {"width": 2275, "height": 1280},
          "position": {"x": 0.5, "y": 0.5},
          "duration": 3.0
        },
        {
          "size": {"width": 1920, "height": 1080},
          "position": {"x": 0.6, "y": 0.4},
          "duration": 3.0,
          "transition_duration": 1.5,
          "easing": "ease_out"
        }
      ]
    }
  ]
}
```

### Example 4: Pan and Zoom

Cinematic pan across an image:

```json
{
  "slides": [
    {
      "index": 0,
      "duration": 12,
      "layers": [
        {
          "image_path": "panorama.png",
          "position": {"x": 0, "y": 0},
          "z_index": 1,
          "skip_rate": 10
        }
      ],
      "cameras": [
        {
          "zoom": 1.5,
          "position": {"x": 0.2, "y": 0.5},
          "duration": 2.0,
          "comment": "Start left"
        },
        {
          "zoom": 1.5,
          "position": {"x": 0.5, "y": 0.5},
          "duration": 2.0,
          "transition_duration": 2.0,
          "easing": "linear",
          "comment": "Pan to center"
        },
        {
          "zoom": 1.5,
          "position": {"x": 0.8, "y": 0.5},
          "duration": 2.0,
          "transition_duration": 2.0,
          "easing": "linear",
          "comment": "Pan to right"
        }
      ]
    }
  ]
}
```

### Example 5: Zoom-In Sequence

Progressive zoom to reveal details:

```json
{
  "slides": [
    {
      "index": 0,
      "duration": 10,
      "layers": [
        {
          "image_path": "detailed_map.png",
          "position": {"x": 0, "y": 0},
          "z_index": 1,
          "skip_rate": 10
        }
      ],
      "cameras": [
        {
          "zoom": 1.0,
          "position": {"x": 0.5, "y": 0.5},
          "duration": 2.0,
          "comment": "Full view"
        },
        {
          "zoom": 1.5,
          "position": {"x": 0.6, "y": 0.4},
          "duration": 2.0,
          "transition_duration": 1.0,
          "easing": "ease_out",
          "comment": "Zoom to area 1"
        },
        {
          "zoom": 2.5,
          "position": {"x": 0.65, "y": 0.35},
          "duration": 2.0,
          "transition_duration": 1.0,
          "easing": "ease_out",
          "comment": "Zoom to specific detail"
        }
      ]
    }
  ]
}
```

## Best Practices

### Camera Design

1. **Start with an overview**: Begin with zoom 1.0 to show the full context
2. **Limit camera count**: 3-5 cameras per slide is usually optimal
3. **Plan your story**: Each camera should reveal or emphasize something specific
4. **End with context**: Consider returning to overview at the end

### Transitions

1. **Use appropriate durations**:
   - Short transitions (0.5-1.0s) for small movements
   - Medium transitions (1.0-2.0s) for moderate zooms/pans
   - Long transitions (2.0-3.0s) for dramatic movements

2. **Choose the right easing**:
   - `ease_out` for most camera movements (feels natural)
   - `linear` for continuous pans
   - `ease_in_out` for back-and-forth movements

3. **Match transition speed to content**:
   - Faster for energetic content
   - Slower for contemplative or detailed content

### Duration

1. **Hold durations**: Give viewers time to absorb information
   - 2-3 seconds minimum per camera
   - 4-5 seconds for complex details
   - 1-2 seconds for quick reveals

2. **Total timing**: 
   - When cameras are defined, they replace the standard final hold
   - Plan total camera sequence duration to match your content needs

### Technical

1. **Resolution awareness**: 
   - Heavy zoom on low-res images will look pixelated
   - Use high-resolution source images for zoomed views

2. **Position accuracy**:
   - Test camera positions to ensure proper framing
   - Remember: 0.5, 0.5 is center, not top-left!

3. **Camera size**:
   - Default size based on zoom works well for most cases
   - Use explicit size for specific aspect ratio needs

## Combining with Other Features

### With Layer Cameras

You can use both:
- **Layer-level camera**: Applied during layer drawing
- **Slide-level cameras**: Applied after all layers are drawn

```json
{
  "slides": [
    {
      "index": 0,
      "duration": 10,
      "layers": [
        {
          "image_path": "diagram.png",
          "z_index": 1,
          "skip_rate": 10,
          "camera": {
            "zoom": 1.2,
            "position": {"x": 0.5, "y": 0.5}
          }
        }
      ],
      "cameras": [
        {
          "zoom": 1.2,
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

### With Animations

Combine camera sequences with layer animations:

```json
{
  "slides": [
    {
      "index": 0,
      "duration": 12,
      "layers": [
        {
          "image_path": "scene.png",
          "z_index": 1,
          "skip_rate": 10,
          "animation": {
            "type": "zoom_in",
            "duration": 1.5,
            "end_zoom": 1.5
          }
        }
      ],
      "cameras": [
        {
          "zoom": 1.5,
          "position": {"x": 0.5, "y": 0.5},
          "duration": 3.0
        },
        {
          "zoom": 2.0,
          "position": {"x": 0.6, "y": 0.4},
          "duration": 3.0,
          "transition_duration": 1.5,
          "easing": "ease_out"
        }
      ]
    }
  ]
}
```

## Troubleshooting

### Camera movement too fast/slow
- Adjust `transition_duration` for smoother or quicker transitions
- Try different easing functions

### Camera not showing expected area
- Verify position values are between 0.0 and 1.0
- Remember: (0.5, 0.5) is center, not (0, 0)
- Test with lower zoom first to see full frame

### Transition looks jerky
- Increase `transition_duration` for smoother movement
- Use `ease_out` or `ease_in_out` instead of `linear`
- Ensure frame rate is adequate (30fps recommended)

### Camera sequence too long/short
- Sum up all durations + transition durations to get total time
- Adjust individual camera durations to match desired total
- Remember: camera sequence replaces standard final hold

## Notes

- **Camera sequences replace final hold**: When cameras are defined, the standard "hold final frame" behavior is replaced by the camera sequence
- **No cameras defined**: Falls back to standard behavior (hold final frame for specified duration)
- **Easing affects smoothness**: Choose easing functions that match your content's mood
- **Performance**: Complex camera sequences with many transitions may increase rendering time

## Future Enhancements

Planned features:
- Path-based camera movements
- Camera rotation
- 3D camera effects
- Keyframe-based camera animation
