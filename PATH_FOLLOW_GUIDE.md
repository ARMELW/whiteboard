# Path Follow Animation Guide

## Overview

The `path_follow` animation mode provides a **point-by-point path following** animation where the hand/object moves sequentially through actual drawing path points, simulating realistic hand drawing movement.

## Key Features

✅ **Point-by-Point Animation** - Hand follows actual contour points extracted from the drawing  
✅ **Natural Hand Jitter** - Random offset applied to hand position for realistic movement  
✅ **Variable Speed** - Speed varies naturally to simulate human drawing  
✅ **Automatic Path Extraction** - Contours are automatically detected from the image  
✅ **Configurable Sampling** - Control smoothness by sampling every Nth point  

## How It Works

### 1. Path Extraction

The system uses OpenCV's contour detection to extract path points from your drawing:

```python
# Internally, the system:
# 1. Converts image to binary (black/white)
# 2. Finds all contours using cv2.findContours()
# 3. Extracts individual points from each contour
# 4. Sorts points for natural drawing order
```

### 2. Point-by-Point Animation

The hand moves through each path point sequentially:

```
Point 1 → Point 2 → Point 3 → ... → Point N
   ✋        ✋        ✋              ✋
```

### 3. Natural Movement

- **Jitter**: Small random offset (±2 pixels by default) on each frame
- **Speed Variation**: Drawing speed varies ±20% to simulate human variation

## Configuration

### Basic Usage

```json
{
  "layers": [
    {
      "image_path": "signature.png",
      "mode": "path_follow",
      "skip_rate": 2
    }
  ]
}
```

### Advanced Configuration

The `path_follow` mode supports the following internal parameters (modifiable in code):

| Parameter | Default | Description |
|-----------|---------|-------------|
| `jitter_amount` | 2.0 | Random hand offset in pixels (higher = more jitter) |
| `speed_variation` | 0.2 | Speed variation factor (0-1, where 0.2 = 20%) |
| `point_sampling` | 2 | Sample every Nth point (higher = faster, less smooth) |

### Adjusting Parameters

To customize the behavior, modify the function call in `whiteboard_animator.py`:

```python
# In draw_masked_object function, find:
if mode == 'path_follow':
    draw_path_follow(
        variables, object_mask, skip_rate, black_pixel_threshold,
        eraser, eraser_mask_inv, eraser_ht, eraser_wd,
        jitter_amount=2.0,      # Increase for more jitter
        speed_variation=0.2,    # Increase for more speed variation
        point_sampling=2        # Increase to skip more points
    )
```

## Use Cases

### ✍️ Signatures

Perfect for animating signature drawings:

```json
{
  "layers": [
    {
      "image_path": "john_doe_signature.png",
      "mode": "path_follow",
      "skip_rate": 1,
      "duration": 3
    }
  ]
}
```

### 🖋️ Calligraphy

Ideal for elegant calligraphic text:

```json
{
  "layers": [
    {
      "image_path": "calligraphy_word.png",
      "mode": "path_follow",
      "skip_rate": 2,
      "duration": 5
    }
  ]
}
```

### 🎨 Realistic Drawing

Great for simulating hand-drawn artwork:

```json
{
  "layers": [
    {
      "image_path": "sketch.png",
      "mode": "path_follow",
      "skip_rate": 3,
      "duration": 10
    }
  ]
}
```

## Comparison with Other Modes

| Aspect | `path_follow` | `draw` (tile-based) | `flood_fill` |
|--------|---------------|---------------------|--------------|
| Movement | Follows actual paths | Grid-based | Region-based |
| Realism | High (natural jitter) | Medium | Low |
| Speed | Variable | Consistent | Fast |
| Best For | Signatures, handwriting | General drawings | Logos, icons |

## Performance Considerations

### Frame Count

The number of frames depends on:
- Number of points in the drawing
- `skip_rate` value (lower = more frames)
- `point_sampling` value (higher = fewer frames)

**Example**: A signature with 1000 contour points:
- With `point_sampling=2` and `skip_rate=2`: ~250 frames
- With `point_sampling=5` and `skip_rate=3`: ~67 frames

### Optimization Tips

1. **Increase `point_sampling`** to reduce frame count
2. **Increase `skip_rate`** for faster animation
3. **Use simple, clean drawings** for best results
4. **Pre-process images** to remove noise/artifacts

## Examples

### Example 1: Signature Animation

```json
{
  "output": {
    "path": "signature_animation.mp4",
    "fps": 30,
    "format": "16:9"
  },
  "slides": [
    {
      "duration": 4,
      "layers": [
        {
          "image_path": "signature.png",
          "mode": "path_follow",
          "skip_rate": 2,
          "position": "center"
        }
      ]
    }
  ]
}
```

### Example 2: Handwriting with Background

```json
{
  "slides": [
    {
      "duration": 8,
      "layers": [
        {
          "image_path": "paper_bg.png",
          "mode": "static",
          "z_index": 0
        },
        {
          "image_path": "handwritten_text.png",
          "mode": "path_follow",
          "skip_rate": 3,
          "z_index": 1
        }
      ]
    }
  ]
}
```

### Example 3: Multi-Step Drawing

```json
{
  "slides": [
    {
      "duration": 12,
      "layers": [
        {
          "image_path": "outline.png",
          "mode": "path_follow",
          "skip_rate": 2,
          "z_index": 1
        },
        {
          "image_path": "details.png",
          "mode": "path_follow",
          "skip_rate": 3,
          "z_index": 2
        },
        {
          "image_path": "shading.png",
          "mode": "coloriage",
          "skip_rate": 5,
          "z_index": 3
        }
      ]
    }
  ]
}
```

## Technical Details

### Algorithm

1. **Contour Detection**: Uses `cv2.findContours()` with `CHAIN_APPROX_NONE`
2. **Point Extraction**: All contour points are extracted
3. **Sorting**: Points sorted by vertical bands then horizontal position
4. **Animation Loop**: 
   - For each point in sequence:
     - Draw small radius around point
     - Add jitter to hand position
     - Vary animation speed
     - Render frame

### Path Point Structure

Extracted points are stored as:
```python
path_points = [(x1, y1), (x2, y2), ..., (xN, yN)]
```

### Natural Movement Implementation

```python
# Jitter calculation
jitter_x = (random() - 0.5) * 2 * jitter_amount
jitter_y = (random() - 0.5) * 2 * jitter_amount

# Speed variation
speed_factor = 1.0 + (random() - 0.5) * 2 * speed_variation
adjusted_skip_rate = max(1, int(skip_rate * speed_factor))
```

## Troubleshooting

### Issue: Animation is too fast

**Solution**: Decrease `skip_rate` or decrease `point_sampling`

```json
{
  "mode": "path_follow",
  "skip_rate": 1  // Lower value = slower animation
}
```

### Issue: Hand movement is too jittery

**Solution**: Reduce `jitter_amount` in the code

```python
draw_path_follow(..., jitter_amount=1.0)  # Reduce from default 2.0
```

### Issue: Not enough points extracted

**Solution**: 
1. Check image has clear contours
2. Ensure image is not too noisy
3. Reduce `point_sampling` to capture more points

### Issue: Animation looks choppy

**Solution**: Decrease `point_sampling` to include more intermediate points

```python
draw_path_follow(..., point_sampling=1)  # Use all points
```

## Best Practices

1. **Clean Images**: Use images with clear, well-defined paths
2. **Black on White**: Best results with dark drawings on light background
3. **Simple Paths**: Complex, intricate drawings may take longer to animate
4. **Test Parameters**: Try different combinations of `skip_rate` and `point_sampling`
5. **Preview First**: Use lower quality settings for quick preview before final render

## Integration with Other Features

### With Layers

```json
{
  "layers": [
    {"mode": "static", "z_index": 0},
    {"mode": "path_follow", "z_index": 1},
    {"mode": "flood_fill", "z_index": 2}
  ]
}
```

### With Camera Zoom

```json
{
  "layers": [
    {
      "mode": "path_follow",
      "camera_zoom": {"enabled": true, "factor": 1.5}
    }
  ]
}
```

### With Transitions

```json
{
  "slides": [
    {
      "layers": [{"mode": "path_follow"}],
      "transition": {"type": "fade", "duration": 0.5}
    }
  ]
}
```

## Future Enhancements

Potential future improvements:
- [ ] Pressure-sensitive stroke width variation
- [ ] Customizable path ordering strategies
- [ ] Path smoothing/interpolation options
- [ ] Multi-stroke optimization
- [ ] Brush style variations

## References

- See `whiteboard_animator.py` - Functions: `extract_path_points()`, `draw_path_follow()`
- See `test_path_follow.py` - Unit tests for path extraction
- See `demo_path_follow.py` - Demo configuration generator
- See `ANIMATION_MODES_SUMMARY.md` - Comparison of all animation modes
