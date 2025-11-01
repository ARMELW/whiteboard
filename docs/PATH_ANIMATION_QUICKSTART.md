# Path Animation - Quick Start

## What is Path Animation?

Path animation allows objects to move along custom trajectories (straight lines, curves, or splines) with control over speed and orientation. Perfect for creating dynamic animations like:
- Flying objects
- Vehicle routes on maps
- Animated arrows showing flow
- Objects following complex paths

## Quick Example

```json
{
  "slides": [
    {
      "index": 0,
      "duration": 6,
      "layers": [
        {
          "image_path": "background.png",
          "z_index": 1,
          "mode": "draw"
        },
        {
          "image_path": "object.png",
          "z_index": 2,
          "scale": 0.2,
          "mode": "static",
          "path_animation": {
            "enabled": true,
            "type": "bezier_cubic",
            "duration": 3.0,
            "points": [[100, 300], [300, 100], [500, 100], [700, 300]],
            "speed_profile": "ease_in_out",
            "orient_to_path": true
          }
        }
      ]
    }
  ]
}
```

## Path Types

### 1. Linear (2+ points)
Straight lines between points
```json
"type": "linear",
"points": [[100, 100], [400, 200], [700, 300]]
```

### 2. Bezier Cubic (4 points)
Smooth S-curves
```json
"type": "bezier_cubic",
"points": [[start_x, start_y], [control1_x, control1_y], [control2_x, control2_y], [end_x, end_y]]
```

### 3. Bezier Quadratic (3 points)
Simple arcs
```json
"type": "bezier_quadratic",
"points": [[start_x, start_y], [control_x, control_y], [end_x, end_y]]
```

### 4. Spline (4+ points)
Smooth curve through all points
```json
"type": "spline",
"points": [[x1, y1], [x2, y2], [x3, y3], [x4, y4], ...]
```

## Key Parameters

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `enabled` | Yes | - | Must be `true` |
| `type` | Yes | - | "linear", "bezier_cubic", "bezier_quadratic", "spline" |
| `duration` | Yes | - | Animation duration in seconds |
| `points` | Yes | - | Array of [x, y] coordinates |
| `speed_profile` | No | "linear" | "linear", "ease_in", "ease_out", "ease_in_out" |
| `orient_to_path` | No | false | Rotate object to face direction |
| `draw_path` | No | false | Draw the path as object moves |
| `path_color` | No | [0,0,0] | Path color in BGR [B, G, R] |
| `path_thickness` | No | 2 | Path line thickness |

## Speed Profiles

- **linear**: Constant speed
- **ease_in**: Slow start, accelerate
- **ease_out**: Fast start, slow down
- **ease_in_out**: Slow start and end

## Common Use Cases

### Arrow Following Route
```json
{
  "image_path": "arrow.png",
  "mode": "static",
  "path_animation": {
    "enabled": true,
    "type": "bezier_cubic",
    "duration": 2.0,
    "points": [[100, 100], [200, 50], [300, 150], [400, 100]],
    "orient_to_path": true,
    "draw_path": true,
    "path_color": [0, 255, 0],
    "path_thickness": 2
  }
}
```

### Marker on Map
```json
{
  "image_path": "marker.png",
  "mode": "static",
  "path_animation": {
    "enabled": true,
    "type": "spline",
    "duration": 4.0,
    "points": [[50, 200], [150, 100], [300, 150], [450, 80], [600, 200]],
    "speed_profile": "ease_in_out"
  }
}
```

### Simple Linear Movement
```json
{
  "image_path": "object.png",
  "mode": "static",
  "path_animation": {
    "enabled": true,
    "type": "linear",
    "duration": 2.0,
    "points": [[100, 100], [700, 400]],
    "speed_profile": "ease_in_out"
  }
}
```

## Testing Your Animation

```bash
# Test with example configs
python whiteboard_animator.py --config examples/path_animation_basic.json --output test.mp4

# Test bezier curves
python whiteboard_animator.py --config examples/path_animation_bezier.json --output bezier.mp4

# Test splines
python whiteboard_animator.py --config examples/path_animation_spline.json --output spline.mp4
```

## Tips

1. **Coordinate System**: Origin (0,0) is top-left, x increases right, y increases down
2. **Path Visibility**: Enable `draw_path: true` to see the trajectory
3. **Orientation**: Use `orient_to_path: true` for directional objects (arrows, vehicles)
4. **Speed**: Try different `speed_profile` settings to find the most natural motion
5. **Multiple Paths**: Add multiple layers with different paths for complex animations

## Troubleshooting

- **Object not visible**: Check coordinates are within canvas bounds
- **Path looks wrong**: Verify control points for Bezier curves
- **Speed issues**: Adjust `duration` or try different `speed_profile`
- **No rotation**: Make sure `orient_to_path: true` is set

For detailed documentation, see [PATH_ANIMATION_GUIDE.md](PATH_ANIMATION_GUIDE.md)
