# Path Animation Guide

## Overview

Path animation allows objects to move along custom trajectories with precise control over speed, orientation, and path visualization. This feature enables creating dynamic and engaging animations where objects follow curves, lines, or complex splines.

## Features Implemented

✅ **Bezier Curve Paths** - Smooth curved trajectories using cubic and quadratic Bezier curves
✅ **Object Following Path** - Objects move along defined paths
✅ **Path Drawing** - Progressive visualization of the path as the object moves
✅ **Motion Along Spline** - Smooth interpolation using Catmull-Rom splines
✅ **Speed Control** - Control animation speed with easing curves
✅ **Orient to Path** - Automatic rotation to face the direction of movement

## Path Types

### 1. Linear Path

Simple straight-line movement between points.

```json
{
  "path_animation": {
    "enabled": true,
    "type": "linear",
    "duration": 2.0,
    "points": [[100, 100], [700, 400]]
  }
}
```

- **Points**: Array of 2+ points `[x, y]`
- **Behavior**: Straight lines connecting each pair of consecutive points

### 2. Bezier Cubic

Smooth curves using cubic Bezier interpolation (4 control points).

```json
{
  "path_animation": {
    "enabled": true,
    "type": "bezier_cubic",
    "duration": 3.0,
    "points": [[100, 300], [300, 100], [500, 100], [700, 300]],
    "speed_profile": "ease_in_out"
  }
}
```

- **Points**: Requires exactly 4 points `[x, y]`
  - p0: Start point
  - p1: First control point
  - p2: Second control point
  - p3: End point
- **Use case**: Smooth S-curves, natural motion paths

### 3. Bezier Quadratic

Simpler curves using quadratic Bezier interpolation (3 control points).

```json
{
  "path_animation": {
    "enabled": true,
    "type": "bezier_quadratic",
    "duration": 2.5,
    "points": [[100, 400], [400, 100], [700, 400]]
  }
}
```

- **Points**: Requires exactly 3 points `[x, y]`
  - p0: Start point
  - p1: Control point
  - p2: End point
- **Use case**: Simple arcs and parabolic paths

### 4. Spline (Catmull-Rom)

Smooth interpolating spline passing through all control points.

```json
{
  "path_animation": {
    "enabled": true,
    "type": "spline",
    "duration": 4.0,
    "points": [
      [100, 300],
      [200, 150],
      [400, 200],
      [600, 100],
      [700, 350]
    ]
  }
}
```

- **Points**: Requires 4+ points `[x, y]`
- **Behavior**: Smooth curve passing through all points
- **Use case**: Complex paths with multiple waypoints

## Configuration Parameters

### Required Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `enabled` | boolean | Must be `true` to activate path animation |
| `type` | string | Path type: "linear", "bezier_cubic", "bezier_quadratic", or "spline" |
| `duration` | number | Animation duration in seconds |
| `points` | array | Array of [x, y] coordinate pairs |

### Optional Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `speed_profile` | string | "linear" | Speed curve: "linear", "ease_in", "ease_out", "ease_in_out" |
| `orient_to_path` | boolean | false | Rotate object to face direction of movement |
| `draw_path` | boolean | false | Draw the path progressively as animation proceeds |
| `path_color` | array | [0, 0, 0] | Path line color in BGR format [B, G, R] |
| `path_thickness` | number | 2 | Path line thickness in pixels |

## Speed Profiles

Control how the object accelerates/decelerates along the path:

- **linear**: Constant speed throughout
- **ease_in**: Slow start, accelerates to normal speed
- **ease_out**: Normal speed, slows down at end
- **ease_in_out**: Slow start and end, normal speed in middle

## Complete Examples

### Example 1: Basic Linear Movement

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
          "scale": 0.3,
          "mode": "static",
          "path_animation": {
            "enabled": true,
            "type": "linear",
            "duration": 3.0,
            "points": [[100, 100], [700, 400]],
            "speed_profile": "ease_in_out"
          }
        }
      ]
    }
  ]
}
```

### Example 2: Curved Path with Orientation

```json
{
  "slides": [
    {
      "index": 0,
      "duration": 8,
      "layers": [
        {
          "image_path": "background.png",
          "z_index": 1,
          "mode": "draw"
        },
        {
          "image_path": "arrow.png",
          "z_index": 2,
          "scale": 0.2,
          "mode": "static",
          "path_animation": {
            "enabled": true,
            "type": "bezier_cubic",
            "duration": 4.0,
            "points": [[100, 300], [300, 100], [500, 100], [700, 300]],
            "speed_profile": "ease_in_out",
            "orient_to_path": true,
            "draw_path": true,
            "path_color": [255, 0, 0],
            "path_thickness": 3
          }
        }
      ]
    }
  ]
}
```

### Example 3: Multiple Objects on Different Paths

```json
{
  "slides": [
    {
      "index": 0,
      "duration": 10,
      "layers": [
        {
          "image_path": "background.png",
          "z_index": 1,
          "mode": "draw"
        },
        {
          "image_path": "object1.png",
          "z_index": 2,
          "scale": 0.2,
          "mode": "static",
          "path_animation": {
            "enabled": true,
            "type": "bezier_cubic",
            "duration": 3.0,
            "points": [[100, 400], [300, 200], [500, 300], [700, 100]],
            "speed_profile": "ease_in",
            "orient_to_path": true
          }
        },
        {
          "image_path": "object2.png",
          "z_index": 3,
          "scale": 0.15,
          "mode": "static",
          "path_animation": {
            "enabled": true,
            "type": "spline",
            "duration": 4.0,
            "points": [[700, 400], [500, 200], [300, 300], [100, 100]],
            "speed_profile": "ease_out"
          }
        }
      ]
    }
  ]
}
```

### Example 4: Spline with Multiple Waypoints

```json
{
  "slides": [
    {
      "index": 0,
      "duration": 12,
      "layers": [
        {
          "image_path": "map.png",
          "z_index": 1,
          "mode": "draw"
        },
        {
          "image_path": "marker.png",
          "z_index": 2,
          "scale": 0.15,
          "mode": "static",
          "path_animation": {
            "enabled": true,
            "type": "spline",
            "duration": 5.0,
            "points": [
              [100, 300],
              [200, 150],
              [400, 200],
              [600, 100],
              [700, 350]
            ],
            "speed_profile": "linear",
            "orient_to_path": true,
            "draw_path": true,
            "path_color": [0, 255, 0],
            "path_thickness": 2
          }
        }
      ]
    }
  ]
}
```

## Tips and Best Practices

### 1. Choosing the Right Path Type

- **Linear**: Use for direct movement, technical diagrams, or when showing straightforward connections
- **Bezier Cubic**: Best for smooth, natural curves like flight paths or flowing animations
- **Bezier Quadratic**: Good for simple arcs, parabolic trajectories
- **Spline**: Ideal for complex paths with multiple waypoints that need smooth transitions

### 2. Speed Profiles

- Use **ease_in_out** for most natural-looking motion
- Use **ease_in** when starting from rest
- Use **ease_out** when coming to a stop
- Use **linear** for mechanical or constant-speed animations

### 3. Orient to Path

Enable `orient_to_path` when:
- Animating vehicles, arrows, or directional objects
- The object has a clear "front" that should face the direction of travel
- You want to emphasize the direction of movement

Disable when:
- The object is symmetrical or has no clear orientation
- You want the object to maintain a fixed rotation

### 4. Path Visualization

Enable `draw_path` to:
- Show the trajectory before or during object movement
- Create trail effects
- Emphasize the path itself in educational content

Customize with:
- `path_color`: Match your design theme
- `path_thickness`: Adjust based on resolution and visibility needs

### 5. Coordinate System

- Origin (0, 0) is at the top-left corner
- X increases to the right
- Y increases downward
- Ensure points are within your canvas dimensions

### 6. Performance Considerations

- Keep duration reasonable (2-5 seconds is typical)
- For very long or complex paths, consider breaking into multiple segments
- Test different speed profiles to find the most appealing motion

## Combining with Other Features

Path animation works seamlessly with:

- **Entrance animations**: Apply entrance animation before path animation starts
- **Exit animations**: Apply after path completes
- **Opacity**: Fade objects in/out while moving
- **Scale**: Resize objects as they move
- **Multiple layers**: Animate multiple objects on different paths simultaneously

## Troubleshooting

### Object not appearing
- Check that points are within canvas bounds
- Verify `mode` is set to "static" or compatible mode
- Ensure `enabled: true` in path_animation config

### Path looks wrong
- Verify point coordinates are correct
- Check path type matches your point count
- For Bezier curves, adjust control points to achieve desired curve

### Motion too fast/slow
- Adjust `duration` parameter
- Try different `speed_profile` settings
- Check your frame rate settings

### Object rotation incorrect
- Verify `orient_to_path: true` is set
- Check if your object image has the correct default orientation
- Path tangent angle is calculated automatically from curve geometry

## Quick Start

1. Add a layer with `mode: "static"` to your configuration
2. Add a `path_animation` object with required parameters
3. Define your path with control points
4. Test with a simple linear path first
5. Experiment with different path types and speed profiles

```bash
# Test with example configs
python whiteboard_animator.py --config examples/path_animation_basic.json --output test_path.mp4
```

## Technical Details

### Bezier Curve Mathematics

**Cubic Bezier** (4 points: p0, p1, p2, p3):
```
B(t) = (1-t)³p0 + 3(1-t)²tp1 + 3(1-t)t²p2 + t³p3
```

**Quadratic Bezier** (3 points: p0, p1, p2):
```
B(t) = (1-t)²p0 + 2(1-t)tp1 + t²p2
```

### Catmull-Rom Spline

Interpolates smoothly through all control points with automatic tangent calculation. Each segment uses 4 points (p0, p1, p2, p3) where the curve goes through p1 and p2.

### Angle Calculation

The orientation angle is calculated from the path tangent (derivative) at each point, ensuring smooth rotation that follows the curve's direction.
