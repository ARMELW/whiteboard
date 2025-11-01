# Geometric Shapes Feature - User Guide

## Overview

The geometric shapes feature allows you to create and animate vector-based shapes in your whiteboard animations. This is perfect for creating diagrams, flowcharts, mathematical visualizations, and educational content.

## Supported Shapes

### Basic Shapes
1. **Circle** - Circular shapes with customizable radius
2. **Rectangle** - Rectangular shapes with customizable width and height
3. **Triangle** - Equilateral triangles
4. **Polygon** - Custom polygons with any number of sides

### Lines and Arrows
5. **Line** - Straight lines between two points
6. **Arrow** - Arrows with customizable arrowhead size

## Shape Configuration

### Basic Structure

Shapes are defined as layers with `type: "shape"` and a `shape_config` object:

```json
{
  "type": "shape",
  "shape_config": {
    "shape": "circle",
    "color": "#0066CC",
    "fill_color": "#99CCFF",
    "stroke_width": 3,
    "position": {"x": 400, "y": 300},
    "size": 100
  },
  "z_index": 1,
  "skip_rate": 8,
  "mode": "draw"
}
```

### Common Properties

All shapes support these properties:

- **shape**: The shape type (required)
  - Options: `"circle"`, `"rectangle"`, `"triangle"`, `"polygon"`, `"line"`, `"arrow"`
  
- **color**: Stroke/outline color (default: black)
  - RGB tuple: `[255, 0, 0]` or `(255, 0, 0)`
  - Hex string: `"#FF0000"`
  
- **fill_color**: Fill color for the shape (optional)
  - RGB tuple: `[255, 200, 200]` or `(255, 200, 200)`
  - Hex string: `"#FFC8C8"`
  - Set to `null` or omit for no fill
  
- **stroke_width**: Thickness of the outline in pixels (default: 2)

### Shape-Specific Properties

#### Circle

```json
{
  "shape": "circle",
  "position": {"x": 400, "y": 300},  // Center position
  "size": 100                         // Radius in pixels
}
```

#### Rectangle

```json
{
  "shape": "rectangle",
  "position": {"x": 400, "y": 300},  // Center position
  "width": 200,                       // Width in pixels
  "height": 150                       // Height in pixels
}
```

If `width` or `height` is not specified, `size` is used for both dimensions.

#### Triangle

```json
{
  "shape": "triangle",
  "position": {"x": 400, "y": 300},  // Center position
  "size": 150                         // Size of the triangle
}
```

Creates an equilateral triangle centered at the position.

#### Polygon

```json
{
  "shape": "polygon",
  "points": [                         // Array of [x, y] points
    [400, 200],
    [600, 300],
    [500, 500],
    [300, 500],
    [200, 300]
  ]
}
```

Creates a custom polygon by connecting the specified points.

#### Line

```json
{
  "shape": "line",
  "start": [100, 200],               // Start point [x, y]
  "end": [700, 400]                  // End point [x, y]
}
```

#### Arrow

```json
{
  "shape": "arrow",
  "start": [100, 300],               // Start point [x, y]
  "end": [700, 300],                 // End point [x, y]
  "arrow_size": 30                   // Arrow head size (default: 20)
}
```

## Animation Support

Shapes support all the same animation features as other layer types:

### Drawing Animation

By default, shapes are drawn progressively (mode: "draw"):

```json
{
  "type": "shape",
  "shape_config": {...},
  "mode": "draw",        // Progressive drawing animation
  "skip_rate": 8         // Animation speed (higher = faster)
}
```

### Entrance Animations

```json
{
  "type": "shape",
  "shape_config": {...},
  "entrance_animation": {
    "type": "zoom_in",
    "duration": 1.0
  }
}
```

Available entrance animations:
- `fade_in` - Fade in from transparent
- `zoom_in` - Zoom in from small
- `slide_in_left` - Slide in from left
- `slide_in_right` - Slide in from right
- `slide_in_top` - Slide in from top
- `slide_in_bottom` - Slide in from bottom

### Exit Animations

```json
{
  "type": "shape",
  "shape_config": {...},
  "exit_animation": {
    "type": "fade_out",
    "duration": 0.8
  }
}
```

Available exit animations:
- `fade_out` - Fade out to transparent
- `zoom_out` - Zoom out to small
- `slide_out_left` - Slide out to left
- `slide_out_right` - Slide out to right
- `slide_out_top` - Slide out to top
- `slide_out_bottom` - Slide out to bottom

### Morphing

Shapes can morph between layers:

```json
{
  "type": "shape",
  "shape_config": {...},
  "morph": {
    "enabled": true,
    "duration": 0.5
  }
}
```

## Complete Examples

### Example 1: Simple Circle

```json
{
  "slides": [
    {
      "index": 0,
      "duration": 5,
      "layers": [
        {
          "type": "shape",
          "shape_config": {
            "shape": "circle",
            "color": "#0066CC",
            "fill_color": "#99CCFF",
            "stroke_width": 3,
            "position": {"x": 800, "y": 450},
            "size": 150
          },
          "z_index": 1,
          "skip_rate": 10,
          "mode": "draw"
        }
      ]
    }
  ]
}
```

### Example 2: Flowchart Diagram

```json
{
  "slides": [
    {
      "index": 0,
      "duration": 12,
      "layers": [
        {
          "type": "shape",
          "shape_config": {
            "shape": "rectangle",
            "color": "#333333",
            "fill_color": "#E6F3FF",
            "stroke_width": 2,
            "position": {"x": 400, "y": 200},
            "width": 200,
            "height": 100
          },
          "z_index": 1,
          "skip_rate": 10,
          "mode": "draw"
        },
        {
          "type": "shape",
          "shape_config": {
            "shape": "arrow",
            "color": "#000000",
            "stroke_width": 3,
            "start": [400, 250],
            "end": [400, 400],
            "arrow_size": 20
          },
          "z_index": 2,
          "skip_rate": 8,
          "mode": "draw"
        },
        {
          "type": "shape",
          "shape_config": {
            "shape": "rectangle",
            "color": "#333333",
            "fill_color": "#FFE6E6",
            "stroke_width": 2,
            "position": {"x": 400, "y": 500},
            "width": 200,
            "height": 100
          },
          "z_index": 3,
          "skip_rate": 10,
          "mode": "draw"
        }
      ]
    }
  ]
}
```

### Example 3: Mathematical Visualization

```json
{
  "slides": [
    {
      "index": 0,
      "duration": 10,
      "layers": [
        {
          "type": "shape",
          "shape_config": {
            "shape": "circle",
            "color": "#FF0000",
            "stroke_width": 2,
            "position": {"x": 400, "y": 400},
            "size": 150
          },
          "z_index": 1,
          "skip_rate": 12,
          "mode": "draw"
        },
        {
          "type": "shape",
          "shape_config": {
            "shape": "line",
            "color": "#0000FF",
            "stroke_width": 2,
            "start": [400, 250],
            "end": [400, 550]
          },
          "z_index": 2,
          "skip_rate": 8,
          "mode": "draw"
        },
        {
          "type": "shape",
          "shape_config": {
            "shape": "line",
            "color": "#0000FF",
            "stroke_width": 2,
            "start": [250, 400],
            "end": [550, 400]
          },
          "z_index": 3,
          "skip_rate": 8,
          "mode": "draw"
        }
      ]
    }
  ]
}
```

## Tips and Best Practices

### 1. Animation Speed

- **Complex shapes**: Use lower `skip_rate` (5-8) for smoother animation
- **Simple shapes**: Use higher `skip_rate` (10-15) for faster animation

### 2. Layering

- Use `z_index` to control drawing order
- Draw background shapes first (lower z_index)
- Draw foreground elements last (higher z_index)

### 3. Colors

- Use hex colors for consistency: `"#0066CC"`
- Use RGB tuples for programmatic generation: `[0, 102, 204]`
- Remember: OpenCV uses BGR format internally, but the config accepts RGB

### 4. Performance

- Filled shapes take longer to draw than outlined shapes
- Use appropriate `skip_rate` to balance animation smoothness and render time
- Complex polygons with many points will take longer to animate

### 5. Combining with Text

Shapes work great with text layers for labels and explanations:

```json
{
  "layers": [
    {
      "type": "shape",
      "shape_config": {
        "shape": "circle",
        "color": "#0066CC",
        "position": {"x": 400, "y": 300},
        "size": 100
      },
      "z_index": 1
    },
    {
      "type": "text",
      "text_config": {
        "text": "Circle",
        "align": "center",
        "size": 32
      },
      "position": {"x": 0, "y": 450},
      "z_index": 2
    }
  ]
}
```

## Command Line Usage

To create a video with geometric shapes:

```bash
python whiteboard_animator.py --config example_shapes_config.json
```

The output video will be saved in the `save_videos` directory.

## See Also

- `example_shapes_config.json` - Complete working example
- `test_shapes.py` - Test script demonstrating all shape types
- `CONFIG_FORMAT.md` - Full configuration reference
- `LAYERS_GUIDE.md` - Layer system documentation
