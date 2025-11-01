# Geometric Shapes Visual Guide

This document provides visual examples of all the geometric shapes supported by Whiteboard-It.

## Shape Gallery

### Circle
![Circle Example](/tmp/test_circle.png)

A circle with:
- Color: Red (RGB: 0, 0, 255)
- Fill Color: Light red
- Stroke Width: 3
- Position: (400, 300)
- Size (radius): 100

### Rectangle
![Rectangle Example](/tmp/test_rectangle.png)

A rectangle with:
- Color: Blue (RGB: 255, 0, 0)
- Fill Color: Light blue
- Stroke Width: 3
- Position: (400, 300)
- Width: 200, Height: 150

### Triangle
![Triangle Example](/tmp/test_triangle.png)

An equilateral triangle with:
- Color: Green (RGB: 0, 255, 0)
- Fill Color: Light green
- Stroke Width: 3
- Position: (400, 300)
- Size: 150

### Arrow
![Arrow Example](/tmp/test_arrow.png)

An arrow with:
- Color: Black (RGB: 0, 0, 0)
- Fill Color: Gray (for arrowhead)
- Stroke Width: 3
- Start: [100, 300]
- End: [700, 300]
- Arrow Size: 30

### Polygon
![Polygon Example](/tmp/test_polygon.png)

A custom pentagon with:
- Color: Purple (RGB: 128, 0, 128)
- Fill Color: Light purple
- Stroke Width: 3
- Points: 5 custom points forming a pentagon

### Line
![Line Example](/tmp/test_line.png)

A straight line with:
- Color: Orange (RGB: 255, 128, 0)
- Stroke Width: 4
- Start: [100, 100]
- End: [700, 500]

### Hex Colors
![Hex Colors Example](/tmp/test_hex_colors.png)

A circle using hex color codes:
- Color: #FF0000 (Red)
- Fill Color: #FFCCCC (Light red)
- Stroke Width: 3

## Configuration Examples

All these shapes can be configured using JSON like this:

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
  "skip_rate": 10,
  "mode": "draw"
}
```

## Color Formats Supported

1. **RGB Tuples**: `(255, 0, 0)` or `[255, 0, 0]`
2. **Hex Strings**: `"#FF0000"`
3. **Named Colors**: `"red"`, `"blue"`, `"green"`, etc. (basic support)

Note: OpenCV uses BGR format internally, but the configuration accepts RGB for convenience.

## Animation Support

All shapes support:
- **Drawing animation**: Progressive reveal using tile-based rendering
- **Entrance animations**: fade_in, zoom_in, slide_in_left/right/top/bottom
- **Exit animations**: fade_out, zoom_out, slide_out_left/right/top/bottom
- **Morphing**: Smooth transitions between shapes
- **Skip rate**: Control animation speed (lower = slower, higher = faster)

## Practical Applications

### Flowcharts
Combine rectangles, diamonds (polygons), and arrows to create flowcharts.

### Diagrams
Use circles and lines to create network diagrams, organizational charts, etc.

### Educational Content
Create geometry lessons, math visualizations, and technical illustrations.

### Technical Documentation
Build system architecture diagrams, API flows, and component relationships.

## Testing

Run the test suite to generate all example images:

```bash
python test_shapes.py
```

This will create test images in `/tmp/` for visual verification.

## See Also

- [SHAPES_GUIDE.md](SHAPES_GUIDE.md) - Complete documentation
- [QUICKSTART_SHAPES.md](QUICKSTART_SHAPES.md) - Quick start guide
- [example_shapes_config.json](example_shapes_config.json) - Working examples
- [example_flowchart.json](example_flowchart.json) - Complex flowchart example
