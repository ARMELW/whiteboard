# Push Animation - Quick Reference

## 🚀 Quick Start

Add a push animation to any layer in your configuration:

```json
{
  "entrance_animation": {
    "type": "push_from_left",
    "duration": 1.5
  }
}
```

## 📋 Animation Types

| Type | Description | Hand Position |
|------|-------------|---------------|
| `push_from_left` | Object slides in from left | Left edge of object |
| `push_from_right` | Object slides in from right | Right edge of object |
| `push_from_top` | Object slides in from top | Top edge of object |
| `push_from_bottom` | Object slides in from bottom | Bottom edge of object |

## ⚙️ Parameters

```json
{
  "type": "push_from_left",     // Required: Animation type
  "duration": 1.5                // Required: Duration in seconds (1.0-2.0 recommended)
}
```

## 💡 Usage Example

```json
{
  "slides": [{
    "index": 0,
    "duration": 10,
    "layers": [
      {
        "image_path": "background.jpg",
        "position": {"x": 0, "y": 0},
        "z_index": 1,
        "mode": "draw"
      },
      {
        "image_path": "laptop.png",
        "position": {"x": 200, "y": 150},
        "z_index": 2,
        "scale": 0.5,
        "mode": "static",
        "entrance_animation": {
          "type": "push_from_left",
          "duration": 1.5
        }
      }
    ]
  }]
}
```

## ⚡ Best Practices

1. **Mode**: Use `"mode": "static"` for objects with push animations
2. **Duration**: 1.0-2.0 seconds works best
3. **Z-Index**: Higher z-index = appears on top
4. **Position**: Plan final position before applying animation
5. **Multiple Objects**: Stagger timing by layer order

## 🎯 Common Use Cases

### Product Presentation
```json
{
  "entrance_animation": {
    "type": "push_from_bottom",
    "duration": 1.2
  }
}
```

### Side Panel
```json
{
  "entrance_animation": {
    "type": "push_from_left",
    "duration": 1.0
  }
}
```

### Header/Title
```json
{
  "entrance_animation": {
    "type": "push_from_top",
    "duration": 1.5
  }
}
```

## 🔗 Related

- See `PUSH_ANIMATION_GUIDE.md` for detailed documentation
- See `examples/push_animation_example.json` for complete example
- See `IMPLEMENTATION_ANIMATIONS.md` for other animation types
