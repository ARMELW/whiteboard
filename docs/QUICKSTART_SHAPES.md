# Quick Start: Geometric Shapes

## TL;DR

Add geometric shapes to your whiteboard animations with this simple configuration:

```json
{
  "type": "shape",
  "shape_config": {
    "shape": "circle",           // circle, rectangle, triangle, polygon, line, arrow
    "color": "#0066CC",          // Stroke color
    "fill_color": "#99CCFF",     // Fill color (optional)
    "stroke_width": 3,           // Line thickness
    "position": {"x": 400, "y": 300},
    "size": 100
  },
  "z_index": 1,
  "skip_rate": 8,
  "mode": "draw"
}
```

## Minimal Example

Save this as `my_shapes.json`:

```json
{
  "slides": [
    {
      "index": 0,
      "duration": 8,
      "layers": [
        {
          "type": "shape",
          "shape_config": {
            "shape": "circle",
            "color": "#0066CC",
            "fill_color": "#CCDDFF",
            "stroke_width": 3,
            "position": {"x": 400, "y": 400},
            "size": 120
          },
          "z_index": 1,
          "skip_rate": 10,
          "mode": "draw"
        },
        {
          "type": "shape",
          "shape_config": {
            "shape": "arrow",
            "color": "#FF6600",
            "stroke_width": 4,
            "start": [200, 400],
            "end": [600, 400],
            "arrow_size": 30
          },
          "z_index": 2,
          "skip_rate": 8,
          "mode": "draw"
        }
      ]
    }
  ]
}
```

## Run It

```bash
python whiteboard_animator.py --config my_shapes.json
```

Output video will be in `save_videos/` directory.

## All Shape Types

### Circle
```json
{
  "shape": "circle",
  "position": {"x": 400, "y": 300},
  "size": 100
}
```

### Rectangle
```json
{
  "shape": "rectangle",
  "position": {"x": 400, "y": 300},
  "width": 200,
  "height": 150
}
```

### Triangle
```json
{
  "shape": "triangle",
  "position": {"x": 400, "y": 300},
  "size": 150
}
```

### Polygon
```json
{
  "shape": "polygon",
  "points": [
    [400, 200],
    [500, 300],
    [400, 400],
    [300, 300]
  ]
}
```

### Line
```json
{
  "shape": "line",
  "start": [100, 200],
  "end": [700, 400]
}
```

### Arrow
```json
{
  "shape": "arrow",
  "start": [100, 300],
  "end": [700, 300],
  "arrow_size": 30
}
```

## Animation Options

Add entrance animations:

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

**Types**: `fade_in`, `zoom_in`, `slide_in_left`, `slide_in_right`, `slide_in_top`, `slide_in_bottom`

## Full Documentation

- **SHAPES_GUIDE.md** - Complete feature guide with examples
- **example_shapes_config.json** - Working example with multiple shapes
- **test_shapes.py** - Test all shape types
- **CONFIG_FORMAT.md** - Configuration reference

## Test Your Setup

Run the test script to verify shapes work:

```bash
python test_shapes.py
```

This will generate sample images in `/tmp/` directory for all shape types.
