# Push Animation Feature - README

## 🎯 What is Push Animation?

Push animation is a new entrance animation type that shows a visible hand pushing elements onto the scene. This creates an interactive, engaging effect perfect for:

- Product demonstrations
- Tutorial videos
- Presentation slides
- Interactive content

## 🚀 Quick Start (30 seconds)

### 1. Basic Usage

Create a JSON configuration file:

```json
{
  "slides": [{
    "index": 0,
    "duration": 10,
    "layers": [
      {
        "image_path": "demo/1.jpg",
        "position": {"x": 0, "y": 0},
        "z_index": 1,
        "mode": "draw"
      },
      {
        "image_path": "demo/2.png",
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

### 2. Generate Video

```bash
python whiteboard_animator.py --config your_config.json
```

### 3. Done! 🎉

Your video will be in the `save_videos/` directory with the hand push animation.

## 📋 Available Animation Types

| Type | Direction | Use Case |
|------|-----------|----------|
| `push_from_left` | ← Left | Side panels, menus |
| `push_from_right` | Right → | Contextual info |
| `push_from_top` | ↑ Top | Headers, titles |
| `push_from_bottom` | Bottom ↓ | Footers, CTAs |

## 💡 Examples

### Example 1: Simple Push

```json
{
  "entrance_animation": {
    "type": "push_from_left",
    "duration": 1.5
  }
}
```

### Example 2: Multiple Directions

See `examples/push_all_directions.json` for a complete example showing all 4 directions.

### Example 3: Product Demo

See `examples/push_product_demo.json` for a realistic product presentation setup.

## 📖 Documentation

| Document | Description |
|----------|-------------|
| `PUSH_ANIMATION_QUICKSTART.md` | Quick reference guide |
| `PUSH_ANIMATION_GUIDE.md` | Comprehensive documentation |
| `PUSH_ANIMATION_VISUAL_GUIDE.md` | Visual examples and comparisons |
| `PUSH_ANIMATION_IMPLEMENTATION.md` | Technical implementation details |

## 🧪 Testing

Run the test suite:

```bash
python test_push_animation.py
```

Expected output: `6/6 tests passed` ✅

## ⚙️ Configuration Options

### Required Parameters

```json
{
  "type": "push_from_left",    // Animation type
  "duration": 1.5               // Duration in seconds
}
```

### Recommended Settings

- **Duration**: 1.0-2.0 seconds (1.5 is ideal)
- **Mode**: Use `"mode": "static"` for elements with push animations
- **Scale**: 0.3-0.5 for small objects, 1.0 for full-size
- **Z-Index**: Higher numbers appear on top

## 🎨 Tips for Best Results

1. **Start Simple**: Begin with one push animation
2. **Test Durations**: Try 1.0s, 1.5s, and 2.0s to find what feels right
3. **Position Carefully**: Ensure element position makes sense for push direction
4. **Scale Appropriately**: Smaller scales (0.3-0.5) often look better
5. **Stagger Timing**: For multiple elements, vary the layer order

## 🔧 Troubleshooting

### Hand Not Visible?
- Check layer `mode` is set to `"static"`
- Verify hand image exists: `data/images/drawing-hand.png`

### Animation Too Fast?
- Increase `duration` value (try 2.0)

### Animation Too Slow?
- Decrease `duration` value (try 1.0)

### Element Position Wrong?
- Verify `position` coordinates
- Check `scale` value

## 🎬 Demo Videos

Generate demo videos with provided examples:

```bash
# Basic example
python whiteboard_animator.py --config examples/push_animation_example.json

# All directions
python whiteboard_animator.py --config examples/push_all_directions.json

# Product demo
python whiteboard_animator.py --config examples/push_product_demo.json
```

## 📞 Support

- **Questions?** Check `PUSH_ANIMATION_GUIDE.md`
- **Issues?** Run `test_push_animation.py` to verify setup
- **Examples?** See the `examples/` directory

## 🎯 Next Steps

1. ✅ Try the basic example
2. ✅ Experiment with different durations
3. ✅ Test all four directions
4. ✅ Create your own animations
5. ✅ Share your results!

## 🌟 Features

- ✅ 4 push directions supported
- ✅ Smooth hand overlay animation
- ✅ Works with all layer types
- ✅ Backward compatible
- ✅ Zero breaking changes
- ✅ Production ready

## 📝 License

Same as the main whiteboard-it project.

---

**Ready to create engaging hand-pushed animations!** 🚀✋

For detailed information, see the comprehensive guides in the documentation files.
