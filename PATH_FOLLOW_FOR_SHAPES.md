# Path Follow Animation for Shapes

## Overview

Shapes extracted from SVG files now automatically use **path_follow animation** when using `mode: "draw"`. This creates a smooth, natural animation that follows the outline of your shape instead of drawing it tile-by-tile.

## What Changed

### Before
When using `type: "shape"` with `mode: "draw"`:
- ❌ Shapes were rendered as a complete image
- ❌ Animation was tile-by-tile (grid-based)
- ❌ Didn't follow the natural contour of the shape
- ❌ Less realistic for complex shapes

### After (NEW! ✨)
When using `type: "shape"` with polygon and `mode: "draw"`:
- ✅ **Automatically switches to path_follow animation**
- ✅ Follows the natural outline/contour of the shape
- ✅ Smooth, hand-drawn effect
- ✅ More realistic and visually appealing
- ✅ No extra configuration needed

## How It Works

1. **Automatic Detection**: When you specify a shape layer with:
   - `type: "shape"`
   - `shape_config.shape: "polygon"`
   - `shape_config.points: [...]`
   - `mode: "draw"`

2. **Automatic Conversion**: The system automatically:
   - Converts polygon points to path_config format
   - Switches from tile-based to path_follow animation
   - Follows the outline smoothly with the hand cursor

3. **Result**: Beautiful outline-following animation!

## Examples

### Example 1: SVG Auto-Extraction (Easiest)

```json
{
  "type": "shape",
  "svg_path": "logo.svg",
  "mode": "draw",
  "skip_rate": 5
}
```

**What happens:**
1. SVG is auto-extracted to polygon with points
2. System detects polygon with draw mode
3. Automatically uses path_follow animation
4. ✨ Smooth outline animation!

### Example 2: Manual Polygon

```json
{
  "type": "shape",
  "shape_config": {
    "shape": "polygon",
    "points": [
      [100, 100], [200, 150], [150, 200], [50, 150]
    ],
    "color": "#E74C3C",
    "fill_color": "#FADBD8",
    "stroke_width": 3
  },
  "mode": "draw",
  "skip_rate": 5
}
```

**Result:** Path follows: (100,100) → (200,150) → (150,200) → (50,150) → back to (100,100)

### Example 3: Multiple Shapes

```json
{
  "layers": [
    {
      "_comment": "Polygon - uses path_follow automatically",
      "type": "shape",
      "svg_path": "arrow.svg",
      "mode": "draw",
      "skip_rate": 5
    },
    {
      "_comment": "Circle - uses tile-by-tile (standard)",
      "type": "shape",
      "shape_config": {
        "shape": "circle",
        "color": "#3498DB",
        "fill_color": "#AED6F1",
        "stroke_width": 3,
        "position": {"x": 640, "y": 360},
        "size": 100
      },
      "mode": "draw",
      "skip_rate": 8
    }
  ]
}
```

## Which Shapes Use Path Follow?

| Shape Type | Path Follow? | Animation Style |
|------------|--------------|-----------------|
| **Polygon** (from SVG) | ✅ Yes (automatic) | Smooth outline following |
| **Polygon** (manual) | ✅ Yes (automatic) | Smooth outline following |
| Circle | ❌ No | Tile-by-tile |
| Rectangle | ❌ No | Tile-by-tile |
| Triangle | ❌ No | Tile-by-tile |
| Line | ❌ No | Tile-by-tile |
| Arrow | ❌ No | Custom progressive |

**Why only polygons?**
- Polygons have explicit point sequences (path)
- Other shapes (circle, rectangle) are defined by center/size, not paths
- Path follow needs a sequence of points to follow

## Animation Speed Control

The `skip_rate` parameter controls animation speed:

```json
{
  "svg_path": "shape.svg",
  "mode": "draw",
  "skip_rate": 2   // Slower, more detailed (2 pixels between frames)
}

{
  "svg_path": "shape.svg",
  "mode": "draw",
  "skip_rate": 10  // Faster (10 pixels between frames)
}
```

**Recommended values:**
- **2-3**: Very slow, detailed animation (signatures, calligraphy)
- **5**: Standard speed (good default)
- **8-10**: Faster animation (simple shapes, logos)

## Technical Details

### Point Format Conversion

**Polygon format (input):**
```json
{
  "points": [[100, 100], [200, 150], [150, 200]]
}
```

**Path config format (internal):**
```json
[
  {"x": 100, "y": 100},
  {"x": 200, "y": 150},
  {"x": 150, "y": 200}
]
```

This conversion happens automatically when the system detects a polygon with draw mode.

### Mode Detection Logic

```python
if layer_type == 'shape' and layer_mode == 'draw':
    shape_config = layer.get('shape_config', {})
    if shape_config.get('shape') == 'polygon' and 'points' in shape_config:
        # Convert polygon points to path_config
        path_config = [{'x': int(p[0]), 'y': int(p[1])} for p in polygon_points]
        layer_mode = 'path_follow'  # Auto-switch
```

## Troubleshooting

### Q: My polygon is animating tile-by-tile, not following the path
**A:** Check that:
1. `shape_config.shape` is exactly `"polygon"`
2. `points` array exists in `shape_config`
3. `mode` is set to `"draw"`

### Q: Can I force tile-by-tile animation for a polygon?
**A:** Currently not directly supported. Workarounds:
1. Use a different shape type
2. Render the polygon as an image first
3. Use `mode: "static"` then manually animate

### Q: The animation is too fast/slow
**A:** Adjust `skip_rate`:
- Lower value (2-3) = slower, more frames
- Higher value (10+) = faster, fewer frames

### Q: Can I use path_follow with other shape types?
**A:** Not automatically. Only polygons auto-switch because they have an explicit point sequence. For other shapes, you'd need to manually extract points and use path_config.

## Performance Considerations

**Path Follow vs Tile-by-Tile:**
- Path follow: Draws along the outline only
- Tile-by-tile: Processes the entire canvas grid

**Performance impact:**
- Path follow is generally **faster** for shapes with simple outlines
- Path follow uses **less memory** (only outline pixels)
- Path follow creates **smoother animations** with fewer frames

## See Also

- [SHAPE_FROM_SVG_GUIDE.md](SHAPE_FROM_SVG_GUIDE.md) - Complete SVG shapes guide
- [PATH_FOLLOW_GUIDE.md](PATH_FOLLOW_GUIDE.md) - Path follow animation details
- [examples/shape_auto_extract_svg.json](examples/shape_auto_extract_svg.json) - Working examples

## Summary

🎉 **The new automatic path_follow for polygons makes SVG shape animations look amazing with minimal configuration!**

Just use:
```json
{
  "type": "shape",
  "svg_path": "your_shape.svg",
  "mode": "draw"
}
```

And enjoy smooth, professional outline-following animations! ✨
