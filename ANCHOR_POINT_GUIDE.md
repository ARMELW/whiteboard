# Anchor Point Guide

## 📍 Overview

The `anchor_point` feature allows you to control how the `position` parameter is interpreted when placing layers (images, text, shapes, arrows) on the canvas. This is particularly useful for compatibility with external editors that use center-based positioning.

## 🎯 Problem Solved

External editors (especially those with camera systems, zoom, or central coordinate systems) often export configurations where the `position` represents the **center** of an object. However, whiteboard-animator previously interpreted `position` as the **top-left corner**. This caused positioning errors when importing from external editors.

The `anchor_point` feature resolves this incompatibility.

## 🔧 Usage

### Basic Syntax

```json
{
  "type": "image",
  "image_path": "path/to/image.png",
  "position": {"x": 960, "y": 540},
  "anchor_point": "center",
  "width": 300,
  "height": 200
}
```

### Supported Values

- **`"top-left"`** (default): Position refers to the top-left corner of the layer
- **`"center"`**: Position refers to the center of the layer

## 📐 How It Works

### Top-Left Anchor (Default Behavior)

```json
{
  "position": {"x": 100, "y": 100},
  "anchor_point": "top-left"
}
```

The layer's **top-left corner** is placed at coordinates (100, 100).

```
Canvas:
    (100,100) ┌─────────┐
              │ Layer   │
              │         │
              └─────────┘
```

### Center Anchor

```json
{
  "position": {"x": 100, "y": 100},
  "anchor_point": "center"
}
```

The layer's **center** is placed at coordinates (100, 100).

```
Canvas:
         ┌─────────┐
         │ Layer   │
         │  (100,  │
         │  100)   │
         └─────────┘
```

## 🖼️ Layer Type Support

### Image Layers

```json
{
  "type": "image",
  "image_path": "logo.png",
  "position": {"x": 960, "y": 540},
  "anchor_point": "center",
  "width": 200,
  "height": 150
}
```

**Features:**
- `anchor_point` applies to the final resized image
- `width` and `height` parameters resize the image before positioning
- `width`/`height` takes priority over `scale`

### Text Layers

```json
{
  "type": "text",
  "text_config": {
    "text": "Hello World",
    "font": "Arial",
    "size": 48,
    "color": [0, 0, 0]
  },
  "position": {"x": 960, "y": 540},
  "anchor_point": "center"
}
```

**Features:**
- `anchor_point` centers the text bounding box
- Works with multi-line text
- Compatible with `align` property (left, center, right)

### Shape Layers

```json
{
  "type": "shape",
  "shape_config": {
    "shape": "circle",
    "color": [255, 0, 0],
    "fill_color": [255, 200, 200],
    "size": 100
  },
  "position": {"x": 960, "y": 540},
  "anchor_point": "center"
}
```

**Features:**
- `anchor_point` applies to the shape's bounding box
- Supported shapes: circle, rectangle, triangle, polygon

### Arrow Layers

```json
{
  "type": "arrow",
  "arrow_config": {
    "start": {"x": 100, "y": 100},
    "end": {"x": 500, "y": 500}
  },
  "anchor_point": "center"
}
```

**Note:** For arrows, `anchor_point` applies to the bounding box of the entire arrow.

## 🔄 Width and Height Parameters

The `width` and `height` parameters are now supported for image layers and take priority over `scale`:

```json
{
  "type": "image",
  "image_path": "photo.jpg",
  "position": {"x": 960, "y": 540},
  "anchor_point": "center",
  "width": 400,
  "height": 300
}
```

**Priority:**
1. If `width` AND `height` are specified → Use explicit dimensions
2. Else if `scale` is specified → Apply scale factor
3. Else → Use original image dimensions

## 📝 Examples

### Example 1: Centered Logo

```json
{
  "layers": [
    {
      "type": "image",
      "image_path": "logo.png",
      "position": {"x": 960, "y": 540},
      "anchor_point": "center",
      "width": 300,
      "height": 200,
      "z_index": 1
    }
  ]
}
```

### Example 2: Centered Title with Background

```json
{
  "layers": [
    {
      "type": "shape",
      "shape_config": {
        "shape": "rectangle",
        "fill_color": [240, 240, 240],
        "width": 800,
        "height": 100
      },
      "position": {"x": 960, "y": 200},
      "anchor_point": "center",
      "z_index": 0
    },
    {
      "type": "text",
      "text_config": {
        "text": "Welcome",
        "font": "Arial",
        "size": 60,
        "color": [0, 0, 0],
        "style": "bold"
      },
      "position": {"x": 960, "y": 200},
      "anchor_point": "center",
      "z_index": 1
    }
  ]
}
```

### Example 3: Mixed Anchoring

```json
{
  "layers": [
    {
      "type": "image",
      "image_path": "watermark.png",
      "position": {"x": 50, "y": 50},
      "anchor_point": "top-left",
      "width": 100,
      "height": 50,
      "z_index": 10
    },
    {
      "type": "shape",
      "shape_config": {
        "shape": "circle",
        "color": [255, 0, 0],
        "size": 150
      },
      "position": {"x": 960, "y": 540},
      "anchor_point": "center",
      "z_index": 1
    }
  ]
}
```

## 🔁 Backward Compatibility

Existing configurations **continue to work** without any changes:

- If `anchor_point` is not specified, it defaults to `"top-left"`
- Text layers with `text_config.position` continue to work as before
- All existing tests pass without modification

## ⚠️ Important Notes

1. **Default Behavior**: Without `anchor_point`, positioning remains unchanged (top-left corner)
2. **Canvas Coordinates**: Position coordinates are always in canvas space (typically 1920x1080)
3. **Text Alignment**: The `align` property in `text_config` controls internal text alignment, NOT the anchor point
4. **Resizing**: For images, apply `width`/`height` or `scale` **before** anchor point calculation

## 🎨 Use Cases

### External Editor Compatibility

When importing from editors that use center-based coordinates:

```json
{
  "type": "image",
  "position": {"x": 960, "y": 540},
  "anchor_point": "center",
  "width": 300,
  "height": 200
}
```

### Precise Positioning

Center multiple elements at the same point:

```json
{
  "layers": [
    {
      "type": "shape",
      "position": {"x": 960, "y": 540},
      "anchor_point": "center"
    },
    {
      "type": "text",
      "position": {"x": 960, "y": 540},
      "anchor_point": "center"
    }
  ]
}
```

### Responsive Layouts

Position elements relative to canvas center:

```json
{
  "type": "image",
  "position": {"x": "{{canvas_width / 2}}", "y": "{{canvas_height / 2}}"},
  "anchor_point": "center"
}
```

## 🧪 Testing

Run the anchor point tests to verify functionality:

```bash
python test_anchor_point.py
```

## 📚 See Also

- [Layers Guide](LAYERS_GUIDE.md)
- [Scene Composition Guide](SCENE_COMPOSITION_GUIDE.md)
- [Configuration Format](CONFIG_FORMAT.md)
- [Example: anchor_point_demo.json](examples/anchor_point_demo.json)
