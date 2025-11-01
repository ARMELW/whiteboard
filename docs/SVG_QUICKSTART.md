# SVG Text Handwriting Feature - Quick Start

## Overview

The SVG text handwriting feature brings VideoScribe-style text animation to Whiteboard-It. Text is drawn following natural character stroke order using font glyph paths.

## Quick Usage

### 1. Basic SVG Text

```json
{
  "slides": [{
    "index": 0,
    "duration": 5,
    "layers": [{
      "type": "text",
      "skip_rate": 3,
      "text_config": {
        "text": "Hello World!",
        "font": "DejaVuSans",
        "size": 72,
        "color": "#0066CC",
        "align": "center"
      }
    }]
  }]
}
```

```bash
python whiteboard_animator.py --config my_text.json
```

### 2. With Natural Rhythm (Pauses)

```json
{
  "text_config": {
    "text": "Natural Writing",
    "size": 64,
    "pause_after_char": 2,
    "align": "center"
  }
}
```

### 3. Multi-line Text

```json
{
  "text_config": {
    "text": "Line 1\nLine 2\nLine 3",
    "size": 48,
    "line_height": 1.5,
    "align": "left"
  }
}
```

## Key Configuration Options

| Option | Description | Example |
|--------|-------------|---------|
| `text` | Text content | `"Hello\nWorld"` |
| `font` | Font name | `"DejaVuSans"` |
| `size` | Font size | `72` |
| `color` | Text color | `"#FF0000"` or `[255,0,0]` |
| `align` | Alignment | `"left"`, `"center"`, `"right"` |
| `pause_after_char` | Pause frames | `2` (0.067s at 30fps) |
| `use_svg_paths` | Enable SVG | `true` (default) |

## Animation Speed

Control with `skip_rate`:
- **Fast**: `skip_rate: 8-12`
- **Medium**: `skip_rate: 4-7`
- **Slow/Smooth**: `skip_rate: 2-3`

## Examples

### Simple Example
```bash
python whiteboard_animator.py --config test_svg_text.json
```

### Full Showcase
```bash
python whiteboard_animator.py --config examples/svg_text_showcase.json
```

### With Images
```bash
# Combine text with images
python whiteboard_animator.py --config examples/text_layer_example.json
```

## What Makes It Special

✅ **Natural Stroke Order** - Follows font-designed character paths  
✅ **Precise Rendering** - Uses exact font geometry  
✅ **Timing Controls** - Add pauses for natural rhythm  
✅ **Auto Fallback** - Works even if SVG extraction fails  
✅ **Full Compatibility** - Works with all existing features  

## Requirements

```bash
pip install fonttools opencv-python pillow numpy
```

## Troubleshooting

**"Using column-based drawing" message:**
- Font doesn't support path extraction
- Install fonttools: `pip install fonttools`
- Try a different font (DejaVuSans works well)

**Text position wrong:**
- Check `align` setting (left/center/right)
- Use `position: {x: 100, y: 200}` for absolute placement

**Animation too fast/slow:**
- Adjust `skip_rate` (lower = slower)
- Add `pause_after_char` for pauses

## Learn More

- **Full Documentation**: [SVG_TEXT_HANDWRITING.md](SVG_TEXT_HANDWRITING.md)
- **Technical Details**: [SVG_IMPLEMENTATION_SUMMARY.md](SVG_IMPLEMENTATION_SUMMARY.md)
- **All Examples**: [examples/README.md](examples/README.md)

## Need Help?

Check the comprehensive documentation files for:
- Detailed configuration options
- Advanced examples
- Performance tips
- Comparison with other methods
- Future enhancement ideas
