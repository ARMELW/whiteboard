# Camera Controls and Advanced Animations Guide

This guide explains how to use camera controls and advanced animations in Whiteboard-It.

## Table of Contents
- [Camera Concept](#camera-concept)
- [Post-Animation Effects](#post-animation-effects)
- [Layer Types](#layer-types)
- [Configuration Examples](#configuration-examples)

## Camera Concept

The camera system allows you to zoom and focus on specific areas of your layers, creating cinematic effects.

### Camera Properties

| Property | Type | Description | Default |
|----------|------|-------------|---------|
| `zoom` | float | Zoom level (1.0 = no zoom, 2.0 = 2x zoom) | 1.0 |
| `position` | object | Focus position with `x` and `y` (0.0 to 1.0, where 0.5 is center) | `{"x": 0.5, "y": 0.5}` |

### Position System

The position system uses normalized coordinates (0.0 to 1.0):
- `x: 0.0, y: 0.0` = Top-left corner
- `x: 0.5, y: 0.5` = Center (default)
- `x: 1.0, y: 1.0` = Bottom-right corner

### Camera Configuration Example

```json
{
  "camera": {
    "zoom": 1.5,
    "position": {
      "x": 0.5,
      "y": 0.3
    }
  }
}
```

This configuration zooms 1.5x and focuses on the upper-center portion of the layer.

## Post-Animation Effects

Post-animation effects are applied **after** the layer has been fully drawn. These create dynamic transitions and emphasis.

### Available Effects

#### Zoom In
Creates a gradual zoom-in effect after drawing completes.

```json
{
  "animation": {
    "type": "zoom_in",
    "duration": 1.5,
    "start_zoom": 1.0,
    "end_zoom": 2.0,
    "focus_position": {
      "x": 0.5,
      "y": 0.5
    }
  }
}
```

#### Zoom Out
Creates a gradual zoom-out effect after drawing completes.

```json
{
  "animation": {
    "type": "zoom_out",
    "duration": 1.5,
    "start_zoom": 2.0,
    "end_zoom": 1.0,
    "focus_position": {
      "x": 0.5,
      "y": 0.5
    }
  }
}
```

### Animation Properties

| Property | Type | Description | Default |
|----------|------|-------------|---------|
| `type` | string | Animation type: `none`, `zoom_in`, `zoom_out` | `none` |
| `duration` | float | Animation duration in seconds | 1.0 |
| `start_zoom` | float | Starting zoom level | 1.0 |
| `end_zoom` | float | Ending zoom level | 1.5 |
| `focus_position` | object | Focus point during zoom with `x` and `y` | `{"x": 0.5, "y": 0.5}` |

## Layer Types

Whiteboard-It supports different layer types for various content.

### Image Layers
Standard image layers (default type).

```json
{
  "type": "image",
  "image_path": "path/to/image.png",
  "position": {"x": 0, "y": 0},
  "z_index": 1
}
```

### Text Layers
Text layers with handwriting animation support - renders real text dynamically!

```json
{
  "type": "text",
  "z_index": 2,
  "skip_rate": 10,
  "text_config": {
    "text": "Hello World!\nMultiple lines supported.",
    "font": "Arial",
    "size": 48,
    "color": [0, 0, 255],
    "style": "bold",
    "line_height": 1.5,
    "align": "center"
  }
}
```

**Text Configuration Options:**
- `text`: The text content (use `\n` for line breaks)
- `font`: Font family name (default: "Arial")
- `size`: Font size in pixels (default: 32)
- `color`: RGB tuple like `[255, 0, 0]` or hex like `"#FF0000"` (default: black)
- `style`: "normal", "bold", "italic", or "bold_italic" (default: "normal")
- `line_height`: Line spacing multiplier (default: 1.2)
- `align`: "left", "center", or "right" (default: "left")
- `position`: Optional dict with `x`, `y` for absolute positioning (default: centered)

**Note:** Text layers are rendered to images dynamically and can be animated with handwriting effect using the standard layer animation system.

## Configuration Examples

### Example 1: Simple Camera Zoom

Focus on the center with 1.5x zoom:

```json
{
  "slides": [
    {
      "index": 0,
      "duration": 5,
      "layers": [
        {
          "image_path": "diagram.png",
          "position": {"x": 0, "y": 0},
          "z_index": 1,
          "skip_rate": 10,
          "camera": {
            "zoom": 1.5,
            "position": {"x": 0.5, "y": 0.5}
          }
        }
      ]
    }
  ]
}
```

### Example 2: Zoom-In After Animation

Draw the layer, then zoom in on a specific area:

```json
{
  "slides": [
    {
      "index": 0,
      "duration": 8,
      "layers": [
        {
          "image_path": "product.png",
          "position": {"x": 0, "y": 0},
          "z_index": 1,
          "skip_rate": 10,
          "animation": {
            "type": "zoom_in",
            "duration": 2.0,
            "start_zoom": 1.0,
            "end_zoom": 2.5,
            "focus_position": {
              "x": 0.7,
              "y": 0.4
            }
          }
        }
      ]
    }
  ]
}
```

### Example 3: Multiple Layers with Camera Focus

Create a sequence where each layer has different camera focus:

```json
{
  "slides": [
    {
      "index": 0,
      "duration": 12,
      "layers": [
        {
          "image_path": "background.png",
          "position": {"x": 0, "y": 0},
          "z_index": 1,
          "skip_rate": 8,
          "camera": {
            "zoom": 1.0,
            "position": {"x": 0.5, "y": 0.5}
          }
        },
        {
          "image_path": "detail1.png",
          "position": {"x": 100, "y": 100},
          "z_index": 2,
          "skip_rate": 15,
          "scale": 0.5,
          "camera": {
            "zoom": 1.3,
            "position": {"x": 0.3, "y": 0.3}
          }
        },
        {
          "image_path": "detail2.png",
          "position": {"x": 400, "y": 300},
          "z_index": 3,
          "skip_rate": 15,
          "scale": 0.5,
          "camera": {
            "zoom": 1.3,
            "position": {"x": 0.7, "y": 0.6}
          },
          "animation": {
            "type": "zoom_in",
            "duration": 1.5,
            "start_zoom": 1.3,
            "end_zoom": 2.0,
            "focus_position": {"x": 0.7, "y": 0.6}
          }
        }
      ]
    }
  ]
}
```

### Example 4: Cinematic Reveal with Zoom Out

Start zoomed in and zoom out to reveal the full scene:

```json
{
  "slides": [
    {
      "index": 0,
      "duration": 10,
      "layers": [
        {
          "image_path": "scene.png",
          "position": {"x": 0, "y": 0},
          "z_index": 1,
          "skip_rate": 10,
          "camera": {
            "zoom": 2.0,
            "position": {"x": 0.5, "y": 0.5}
          },
          "animation": {
            "type": "zoom_out",
            "duration": 2.5,
            "start_zoom": 2.0,
            "end_zoom": 1.0,
            "focus_position": {"x": 0.5, "y": 0.5}
          }
        }
      ]
    }
  ]
}
```

### Example 5: Combined with Transitions

Use camera controls with slide transitions:

```json
{
  "slides": [
    {
      "index": 0,
      "duration": 6,
      "layers": [
        {
          "image_path": "intro.png",
          "z_index": 1,
          "skip_rate": 10,
          "animation": {
            "type": "zoom_in",
            "duration": 1.5,
            "end_zoom": 1.5
          }
        }
      ]
    },
    {
      "index": 1,
      "duration": 6,
      "layers": [
        {
          "image_path": "details.png",
          "z_index": 1,
          "skip_rate": 10,
          "camera": {
            "zoom": 1.5,
            "position": {"x": 0.5, "y": 0.5}
          }
        }
      ]
    }
  ],
  "transitions": [
    {
      "after_slide": 0,
      "type": "fade",
      "duration": 1.0
    }
  ]
}
```

## Best Practices

### Camera Zoom
1. **Keep zoom levels reasonable**: Values between 1.0 and 3.0 work best
2. **Match zoom with content**: Higher zoom for detailed areas, lower for overview
3. **Consider resolution**: Heavy zoom on low-res images may look pixelated

### Post-Animation Effects
1. **Use sparingly**: Too many zoom effects can be distracting
2. **Match duration to content**: 1-2 seconds usually works well
3. **Plan focus points**: Choose focus positions that highlight important content

### Combining Features
1. **Camera + Animation**: Apply static camera zoom first, then add post-animation zoom for dramatic effect
2. **Multiple layers**: Use different camera settings for each layer to create depth
3. **With transitions**: Coordinate zoom effects with slide transitions for smooth flow

## Limitations

1. **Performance**: Heavy zoom may increase rendering time
2. **Quality**: Zoom can't add detail beyond the original image resolution
3. **Text layers**: Full typewriting animation not yet implemented (use text images)

## Troubleshooting

### Camera zoom looks pixelated
- Use higher resolution source images
- Reduce zoom level
- Consider using vector-based images converted to high-res PNG

### Animation effect too fast/slow
- Adjust the `duration` parameter
- Consider your target frame rate (higher FPS = smoother)

### Focus position not centered correctly
- Remember: 0.5, 0.5 is center
- Adjust x and y incrementally to find the right spot
- Use 0.0-1.0 range (not pixel coordinates)

## Future Enhancements

Planned features for future releases:
- Native text rendering with typewriting animation
- Rotation and tilt camera controls
- Ease-in/ease-out animation curves
- Path-based camera movements
- Layer-specific animation timing
