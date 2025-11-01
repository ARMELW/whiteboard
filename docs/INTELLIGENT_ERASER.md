# Intelligent Eraser Feature

## Overview

The intelligent eraser feature provides a natural way to handle overlapping content between layers. When enabled, a layer will automatically "erase" any overlapping content from the canvas before being drawn, creating a smooth and natural appearance where new content replaces old content.

## Use Case

This feature is particularly useful when:
- You want to create animations where new elements appear to replace old ones
- Multiple layers overlap and you want a clean appearance
- You need to simulate a natural erasing effect as new content is drawn

## How It Works

1. **Content Detection**: When a layer with `intelligent_eraser: true` is being applied, the system detects all non-white pixels in the layer image
2. **Overlap Detection**: The system identifies where the new layer will overlap with existing canvas content
3. **Pre-Erasure**: Before drawing the new layer, the overlapping regions on the canvas are erased (set to white)
4. **Drawing**: The new layer is then drawn normally on the erased area

## Configuration

### Basic Example

```json
{
  "slides": [
    {
      "index": 0,
      "duration": 5,
      "layers": [
        {
          "image_path": "demo/1.jpg",
          "position": {"x": 50, "y": 50},
          "z_index": 1,
          "scale": 0.6
        },
        {
          "image_path": "demo/2.jpg",
          "position": {"x": 150, "y": 150},
          "z_index": 2,
          "scale": 0.5,
          "intelligent_eraser": true
        }
      ]
    }
  ]
}
```

### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `intelligent_eraser` | boolean | `false` | Enables intelligent eraser effect for the layer |

## Visual Comparison

### Without Intelligent Eraser (Default)
When `intelligent_eraser: false` or omitted:
- Layer 1 is drawn at position (50, 50)
- Layer 2 is drawn at position (150, 150)
- Overlapping area shows Layer 2 content blended with Layer 1 content (if opacity < 1.0)

### With Intelligent Eraser
When `intelligent_eraser: true`:
- Layer 1 is drawn at position (50, 50)
- Before Layer 2 is drawn, the overlapping area is erased (set to white)
- Layer 2 is drawn at position (150, 150)
- Result: Layer 2 content is blended with white background in overlap area (if opacity < 1.0)

**Key Difference:** The intelligent eraser is most visible when using opacity < 1.0. Without it, the new layer blends with existing content. With it, the new layer blends with a white (erased) background, creating a cleaner, more natural appearance.

## Technical Details

### Content Detection Threshold

The intelligent eraser uses a threshold of 250 (out of 255) to detect content:
- Pixels with any RGB channel value < 250 are considered "content"
- Pixels at or near white (255, 255, 255) are considered "background"

This ensures that nearly-white pixels are preserved as background while actual content is detected and erased appropriately.

### Processing Order

Layers are processed in z-index order (lowest to highest). The intelligent eraser only affects content from layers already drawn on the canvas, not future layers with higher z-index values.

### Performance

The intelligent eraser feature has minimal performance impact:
- Content detection is performed once per layer
- Only operates on the specific overlap region
- Uses efficient NumPy array operations

## Backward Compatibility

The feature is fully backward compatible:
- Default value is `false`, so existing configurations are unaffected
- Only layers explicitly setting `intelligent_eraser: true` will use this feature
- All other layer properties and behaviors remain unchanged

## Examples

### Example 1: Simple Overlap

Two images with partial overlap, second image erases the overlapping area:

```json
{
  "layers": [
    {
      "image_path": "image1.png",
      "position": {"x": 0, "y": 0},
      "z_index": 1
    },
    {
      "image_path": "image2.png",
      "position": {"x": 100, "y": 100},
      "z_index": 2,
      "intelligent_eraser": true
    }
  ]
}
```

### Example 2: Multiple Overlapping Layers

Three layers where each subsequent layer erases previous content:

```json
{
  "layers": [
    {
      "image_path": "base.png",
      "position": {"x": 0, "y": 0},
      "z_index": 1
    },
    {
      "image_path": "middle.png",
      "position": {"x": 50, "y": 50},
      "z_index": 2,
      "intelligent_eraser": true
    },
    {
      "image_path": "top.png",
      "position": {"x": 100, "y": 100},
      "z_index": 3,
      "intelligent_eraser": true
    }
  ]
}
```

### Example 3: Combined with Other Features

Intelligent eraser works seamlessly with other layer features:

```json
{
  "layers": [
    {
      "image_path": "background.png",
      "position": {"x": 0, "y": 0},
      "z_index": 1,
      "skip_rate": 5
    },
    {
      "image_path": "foreground.png",
      "position": {"x": 100, "y": 100},
      "z_index": 2,
      "scale": 0.8,
      "opacity": 0.9,
      "skip_rate": 10,
      "intelligent_eraser": true,
      "entrance_animation": {
        "type": "fade_in",
        "duration": 1.0
      }
    }
  ]
}
```

## Tips and Best Practices

1. **Most effective with opacity < 1.0**: The visual difference is most apparent when the new layer has opacity less than 1.0. This creates a blending effect with the erased (white) background rather than the underlying layer.

2. **Use with overlapping content**: The intelligent eraser is most effective when layers actually overlap. If layers don't overlap, the feature has no visible effect.

3. **Z-index matters**: Ensure your z-index values are correct. The intelligent eraser only affects layers already drawn (lower z-index values).

4. **Content vs Background**: Images with transparent or white backgrounds work best, as the eraser detects actual content based on non-white pixels.

5. **Combine with animations**: Use intelligent eraser with entrance animations for smooth transitions where new content appears to replace old content.

6. **Test threshold sensitivity**: If your images have near-white content that should be preserved, consider adjusting the threshold in the code (currently set to 250).

## Troubleshooting

### Issue: Eraser not working as expected

**Solution**: Check that:
- `intelligent_eraser` is set to `true` (case-sensitive)
- Layers actually overlap in position
- The new layer has actual content (non-white pixels) in the overlap area
- Z-index values are correct (lower layers are drawn first)

### Issue: Too much or too little content is erased

**Solution**: The threshold (250) may need adjustment for your specific images. Images with very light content might not be detected correctly.

## See Also

- [Layers Guide](LAYERS_GUIDE.md) - General information about using layers
- [Configuration Format](CONFIG_FORMAT.md) - Complete configuration reference
- [Examples](example_config.json) - Working configuration examples
