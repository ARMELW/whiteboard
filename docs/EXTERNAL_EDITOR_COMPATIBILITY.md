# External Editor Compatibility Guide

## 🎯 Problem Overview

This guide addresses the positioning incompatibility issue when importing JSON configurations from external editors (especially those using camera systems, zoom, or central coordinate systems).

### The Issue

**External Editors** typically export `position` as the **center** of objects:
```json
{
  "position": {"x": 960, "y": 540}  // Center of the object
}
```

**whiteboard-animator** (previously) interpreted `position` as the **top-left corner**:
```
Result: Object appears shifted down and right by (width/2, height/2)
```

## ✅ Solution: anchor_point Feature

The new `anchor_point` parameter lets you specify how `position` should be interpreted.

### Quick Fix for External Editor Configs

Add `"anchor_point": "center"` to all layers imported from external editors:

```json
{
  "type": "image",
  "image_path": "logo.png",
  "position": {"x": 960, "y": 540},
  "anchor_point": "center",     // ← Add this line
  "width": 300,
  "height": 200
}
```

## 🔧 Complete Migration Example

### Before (External Editor Export)

```json
{
  "layers": [
    {
      "type": "image",
      "image_path": "logo.png",
      "position": {"x": 960, "y": 540},
      "originalWidth": 600,
      "originalHeight": 400,
      "scale": 0.5
    },
    {
      "type": "text",
      "text": "Hello World",
      "position": {"x": 960, "y": 300}
    }
  ]
}
```

### After (whiteboard-animator Compatible)

```json
{
  "layers": [
    {
      "type": "image",
      "image_path": "logo.png",
      "position": {"x": 960, "y": 540},
      "anchor_point": "center",
      "width": 300,
      "height": 200
    },
    {
      "type": "text",
      "text_config": {
        "text": "Hello World",
        "font": "Arial",
        "size": 48,
        "color": [0, 0, 0]
      },
      "position": {"x": 960, "y": 300},
      "anchor_point": "center"
    }
  ]
}
```

## 📐 Understanding the Transformation

### Center Position Calculation

If your external editor gives you:
- Position: (960, 540) as center
- Size: 300×200

Without `anchor_point`, whiteboard-animator would place the top-left corner at (960, 540), causing the object to appear at an offset.

With `anchor_point: center`:
- The center is placed at (960, 540)
- Top-left corner is automatically calculated as (960 - 150, 540 - 100) = (810, 440)
- ✅ Object appears exactly where expected

### Visual Comparison

```
WITHOUT anchor_point (incorrect):
    (960,540) ┌─────────┐
              │         │
              │ Object  │
              │         │
              └─────────┘
              
WITH anchor_point: center (correct):
         ┌─────────┐
         │         │
         │ Object  │
         │ (960,   │
         │  540)   │
         └─────────┘
```

## 🔄 Width and Height Parameters

External editors often provide final dimensions after scaling/zooming. Use `width` and `height` parameters:

```json
{
  "type": "image",
  "image_path": "photo.jpg",
  "position": {"x": 960, "y": 540},
  "anchor_point": "center",
  "width": 400,     // Final width after zoom/scale
  "height": 300     // Final height after zoom/scale
}
```

**Important**: `width` and `height` take **priority** over `scale`.

## 🎨 All Layer Types

### Image Layers

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

### Text Layers

```json
{
  "type": "text",
  "text_config": {
    "text": "Centered Text",
    "font": "Arial",
    "size": 48,
    "color": [0, 0, 0]
  },
  "position": {"x": 960, "y": 540},
  "anchor_point": "center"
}
```

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

## 🤖 Automated Conversion Script

If you have many configurations to convert, here's a Python script:

```python
import json

def add_anchor_point(config_file):
    """Add anchor_point: center to all layers in a config file."""
    with open(config_file, 'r') as f:
        data = json.load(f)
    
    # Add anchor_point to all layers
    for layer in data.get('layers', []):
        layer['anchor_point'] = 'center'
        
        # If scale and original dimensions exist, convert to width/height
        if 'scale' in layer and 'originalWidth' in layer:
            layer['width'] = int(layer['originalWidth'] * layer['scale'])
            layer['height'] = int(layer['originalHeight'] * layer['scale'])
            del layer['scale']
            del layer['originalWidth']
            del layer['originalHeight']
    
    # Save updated config
    output_file = config_file.replace('.json', '_converted.json')
    with open(output_file, 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"✓ Converted: {config_file} → {output_file}")

# Usage
add_anchor_point('external_config.json')
```

## 📊 Conversion Checklist

When importing from external editors:

- [ ] Add `"anchor_point": "center"` to all layers
- [ ] Convert scale + original dimensions to explicit `width` and `height`
- [ ] Verify position coordinates are in 1920×1080 canvas space
- [ ] Test with a single layer first before batch conversion
- [ ] Check that text layers have proper `text_config` structure

## ⚠️ Common Pitfalls

### 1. Missing Width/Height

**Problem**: Image appears at wrong size
```json
{
  "position": {"x": 960, "y": 540},
  "anchor_point": "center"
  // Missing width/height!
}
```

**Solution**: Add explicit dimensions
```json
{
  "position": {"x": 960, "y": 540},
  "anchor_point": "center",
  "width": 300,
  "height": 200
}
```

### 2. Wrong Coordinate System

**Problem**: Position is in camera space, not canvas space

**Solution**: Transform coordinates to 1920×1080 canvas:
```python
canvas_x = (camera_x / camera_width) * 1920
canvas_y = (camera_y / camera_height) * 1080
```

### 3. Text Config Structure

**Problem**: Text parameters at wrong level
```json
{
  "type": "text",
  "text": "Hello",  // ❌ Wrong
  "position": {"x": 960, "y": 540}
}
```

**Solution**: Use text_config
```json
{
  "type": "text",
  "text_config": {  // ✅ Correct
    "text": "Hello",
    "font": "Arial",
    "size": 48,
    "color": [0, 0, 0]
  },
  "position": {"x": 960, "y": 540},
  "anchor_point": "center"
}
```

## 🧪 Testing Your Conversion

1. **Convert a single layer first**:
   ```json
   {
     "layers": [
       {
         "type": "image",
         "image_path": "test.png",
         "position": {"x": 960, "y": 540},
         "anchor_point": "center",
         "width": 100,
         "height": 100
       }
     ]
   }
   ```

2. **Verify positioning**:
   - Object should appear centered on the canvas
   - Object should be at exact coordinates you specified

3. **Scale up** to all layers once confirmed

## 📚 Additional Resources

- [Anchor Point Guide](ANCHOR_POINT_GUIDE.md) - Complete feature documentation
- [Layers Guide](LAYERS_GUIDE.md) - Layer system overview
- [Example: anchor_point_demo.json](examples/anchor_point_demo.json) - Working example

## 💡 Need Help?

If you're still experiencing positioning issues:

1. Verify `anchor_point` is set to `"center"` for all layers
2. Check that `width` and `height` are set correctly
3. Ensure positions are in canvas space (1920×1080)
4. Run test: `python test_anchor_point.py`
5. Open an issue with your configuration file

## ✅ Summary

**Two simple changes** fix external editor compatibility:

1. Add `"anchor_point": "center"` to each layer
2. Add explicit `"width"` and `"height"` for images

```json
{
  "type": "image",
  "position": {"x": 960, "y": 540},
  "anchor_point": "center",      // ← Add this
  "width": 300,                   // ← Add this
  "height": 200                   // ← Add this
}
```

That's it! Your external editor configurations will now work perfectly with whiteboard-animator. 🎉
