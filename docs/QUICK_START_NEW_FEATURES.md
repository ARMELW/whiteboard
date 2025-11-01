# Quick Start: New Animation Features

## TL;DR

Three new layer modes and advanced animations are now available:

```json
{
  "mode": "draw",      // Normal hand animation (default)
  "mode": "eraser",    // Eraser animation
  "mode": "static",    // No drawing animation
  
  "entrance_animation": {"type": "fade_in", "duration": 1.0},
  "exit_animation": {"type": "fade_out", "duration": 0.8},
  "morph": {"enabled": true, "duration": 0.5}
}
```

## Minimal Example

```json
{
  "slides": [
    {
      "index": 0,
      "duration": 8,
      "layers": [
        {
          "image_path": "background.jpg",
          "z_index": 1,
          "mode": "draw"
        },
        {
          "image_path": "element.jpg",
          "position": {"x": 200, "y": 200},
          "z_index": 2,
          "scale": 0.3,
          "mode": "eraser",
          "entrance_animation": {
            "type": "fade_in",
            "duration": 1.0
          }
        },
        {
          "image_path": "logo.jpg",
          "position": {"x": 50, "y": 50},
          "z_index": 3,
          "scale": 0.2,
          "mode": "static",
          "entrance_animation": {
            "type": "zoom_in",
            "duration": 1.5
          }
        }
      ]
    }
  ]
}
```

## Run It

```bash
python whiteboard_animator.py image.jpg --config config.json
```

## Animation Types

**Entrance:** fade_in, slide_in_left, slide_in_right, slide_in_top, slide_in_bottom, zoom_in

**Exit:** fade_out, slide_out_left, slide_out_right, slide_out_top, slide_out_bottom, zoom_out

## Full Documentation

- **NEW_FEATURES.md** - Complete feature guide
- **IMPLEMENTATION_ANIMATIONS.md** - Technical details
- **CONFIG_FORMAT.md** - Configuration reference
- **LAYERS_GUIDE.md** - Usage examples
