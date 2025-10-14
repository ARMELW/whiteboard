# Progressive Layer Drawing

## Overview

The whiteboard animation system now correctly supports progressive layer drawing, where multiple layers are drawn sequentially while preserving previously drawn layers. This creates a natural, additive animation effect similar to tools like VideoScribe and Doodly.

## How It Works

When you configure multiple layers in a slide, the animation system:

1. **Draws Layer 1**: The first layer is drawn progressively with the hand animation
2. **Preserves Layer 1**: Once complete, Layer 1 remains visible in full color
3. **Draws Layer 2**: The second layer is drawn on top, preserving Layer 1 underneath
4. **Continues**: This pattern continues for all subsequent layers

### Technical Implementation

The fix ensures that when each layer's drawing animation completes and the final colorization step occurs, only the pixels belonging to that layer are updated. This is accomplished by:

- Creating a content mask that identifies non-white pixels (actual content)
- Applying the colored image only where the mask indicates content
- Preserving all previously drawn pixels in other areas

## Configuration Example

### Basic Multi-Layer Setup

```json
{
  "slides": [
    {
      "index": 0,
      "duration": 10,
      "layers": [
        {
          "image_path": "layer1.png",
          "position": {"x": 0, "y": 0},
          "z_index": 1,
          "skip_rate": 8,
          "mode": "draw"
        },
        {
          "image_path": "layer2.png",
          "position": {"x": 100, "y": 100},
          "z_index": 2,
          "skip_rate": 10,
          "mode": "draw"
        },
        {
          "image_path": "layer3.png",
          "position": {"x": 200, "y": 200},
          "z_index": 3,
          "skip_rate": 12,
          "mode": "draw"
        }
      ]
    }
  ]
}
```

### Mixed Image and Text Layers

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
          "skip_rate": 10,
          "mode": "draw"
        },
        {
          "type": "text",
          "text_config": {
            "text": "Title Text",
            "size": 60,
            "color": "#FF0000",
            "position": {"x": 100, "y": 100}
          },
          "z_index": 2,
          "skip_rate": 5,
          "mode": "draw"
        },
        {
          "image_path": "icon.png",
          "position": {"x": 400, "y": 400},
          "z_index": 3,
          "skip_rate": 8,
          "scale": 0.5,
          "mode": "draw"
        }
      ]
    }
  ]
}
```

## Supported Layer Types

Progressive layer drawing works with all layer types:

- **Image layers**: Regular image files (PNG, JPG, etc.)
- **Text layers**: Dynamically generated text with custom fonts and colors
- **Shape layers**: Geometric shapes (circles, rectangles, arrows, etc.)
- **Mixed layers**: Any combination of the above

## Layer Modes

All layer modes are supported:

- **`draw` mode**: Progressive drawing with hand animation (default)
- **`eraser` mode**: Progressive erasing with eraser animation
- **`static` mode**: Instant appearance without drawing animation

## Animation Features

Progressive layer drawing is compatible with all animation features:

### Entrance Animations

```json
{
  "image_path": "layer2.png",
  "z_index": 2,
  "entrance_animation": {
    "type": "fade_in",
    "duration": 1.0
  }
}
```

### Exit Animations

```json
{
  "image_path": "layer3.png",
  "z_index": 3,
  "exit_animation": {
    "type": "slide_out_right",
    "duration": 0.8
  }
}
```

### Morphing Between Layers

```json
{
  "image_path": "layer2.png",
  "z_index": 2,
  "morph": {
    "enabled": true,
    "duration": 0.5
  }
}
```

## Best Practices

### 1. Layer Ordering

Use `z_index` to control the stacking order:
- Lower values are drawn first (bottom layers)
- Higher values are drawn later (top layers)

```json
{
  "layers": [
    {"z_index": 1, "image_path": "background.png"},
    {"z_index": 2, "image_path": "foreground.png"},
    {"z_index": 3, "image_path": "overlay.png"}
  ]
}
```

### 2. Drawing Speed

Adjust `skip_rate` for each layer to control drawing speed:
- Lower values = slower, more detailed animation
- Higher values = faster animation

```json
{
  "layers": [
    {"skip_rate": 5, "image_path": "detailed_layer.png"},
    {"skip_rate": 15, "image_path": "simple_layer.png"}
  ]
}
```

### 3. Image Preparation

For best results:
- Use transparent PNGs for layers that should overlay cleanly
- Use white backgrounds for layers that should be drawn progressively
- Ensure non-overlapping content when possible for clearer animations

### 4. Duration Planning

Consider the total drawing time when setting slide duration:
- Each layer needs time to be drawn
- Add extra time for viewing the complete result
- Use entrance/exit animations to smooth transitions

## Example: Educational Diagram

```json
{
  "slides": [
    {
      "index": 0,
      "duration": 15,
      "layers": [
        {
          "type": "shape",
          "shape_config": {
            "shape": "circle",
            "color": "#0066CC",
            "position": {"x": 400, "y": 300},
            "size": 150
          },
          "z_index": 1,
          "skip_rate": 8
        },
        {
          "type": "text",
          "text_config": {
            "text": "Step 1",
            "size": 40,
            "color": "#000000",
            "position": {"x": 350, "y": 290}
          },
          "z_index": 2,
          "skip_rate": 5
        },
        {
          "type": "shape",
          "shape_config": {
            "shape": "arrow",
            "color": "#FF0000",
            "start": [500, 300],
            "end": [700, 300]
          },
          "z_index": 3,
          "skip_rate": 6
        },
        {
          "type": "shape",
          "shape_config": {
            "shape": "rectangle",
            "color": "#00CC66",
            "position": {"x": 800, "y": 200},
            "width": 200,
            "height": 150
          },
          "z_index": 4,
          "skip_rate": 8
        },
        {
          "type": "text",
          "text_config": {
            "text": "Step 2",
            "size": 40,
            "color": "#000000",
            "position": {"x": 850, "y": 265}
          },
          "z_index": 5,
          "skip_rate": 5
        }
      ]
    }
  ]
}
```

## Troubleshooting

### Layers Not Appearing

**Problem**: Some layers are missing from the final animation.

**Solutions**:
- Check that all image paths are correct and files exist
- Verify that `z_index` values are properly ordered
- Ensure layer positions are within the video frame bounds

### Layers Overlapping Unexpectedly

**Problem**: Layers are not stacking as expected.

**Solutions**:
- Double-check `z_index` values (lower = drawn first)
- Verify `position` coordinates for each layer
- Consider using `opacity` for semi-transparent overlays

### Performance Issues

**Problem**: Animation takes too long or video is too large.

**Solutions**:
- Reduce image resolution before importing
- Increase `skip_rate` for faster drawing
- Use compressed image formats (JPEG for photos, PNG for graphics)
- Consider using `static` mode for some layers

## Related Features

- [Layer Modes Guide](LAYERS_GUIDE.md)
- [Entrance and Exit Animations](IMPLEMENTATION_ANIMATIONS.md)
- [Text Layer Features](TEXT_LAYERS_GUIDE.md)
- [Shape Layer Features](SHAPES_GUIDE.md)

## Technical Notes

The progressive layer drawing fix was implemented by modifying three key drawing functions:

1. `draw_masked_object()` - Tile-based drawing for images
2. `draw_text_handwriting()` - Column-based drawing for text
3. `draw_svg_path_handwriting()` - Path-based drawing for SVG text

Each function now preserves previously drawn content by only updating pixels where the current layer has non-white content, ensuring that the additive layer effect works correctly.
