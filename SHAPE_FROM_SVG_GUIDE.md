# Shape from SVG Guide

This guide explains how to convert SVG files to shape animations with proper fill colors.

## Problem Solved

Previously, when using `path_follow` mode with SVG files, the animation would only draw the outline/stroke of the shape, not the filled content. This has been fixed by:

1. **Fixed `render_shape_to_image` function** - Now properly renders shapes with both stroke AND fill colors
2. **Enhanced `path_extractor.py`** - Extracts color information from SVG files and generates shape configurations
3. **Added shape type support** - Use `type: "shape"` with polygon points extracted from SVG paths

## Quick Start

### Method 1: Automatic Extraction (NEW! ✨)

**No manual steps required!** Just specify the SVG file path in your configuration:

```json
{
  "slides": [{
    "layers": [{
      "type": "shape",
      "svg_path": "path/to/your_file.svg",
      "z_index": 1,
      "skip_rate": 5,
      "mode": "draw"
    }]
  }]
}
```

The system will automatically:
- ✅ Extract path points from the SVG
- ✅ Detect and apply fill/stroke colors
- ✅ Generate the shape configuration

**With custom parameters:**

```json
{
  "type": "shape",
  "svg_path": "your_file.svg",
  "svg_sampling_rate": 10,
  "svg_num_points": 100,
  "svg_reverse": false,
  "shape_config": {
    "color": "#E74C3C",
    "fill_color": "#FADBD8",
    "stroke_width": 4
  },
  "skip_rate": 5,
  "mode": "draw"
}
```

**Parameters:**
- `svg_path`: Path to your SVG file (required)
- `svg_sampling_rate`: Density of points (default: 10)
- `svg_num_points`: Maximum number of points (optional)
- `svg_reverse`: Reverse the path direction (default: false)
- `shape_config`: Override colors and stroke width (optional)

### Method 2: Manual Extraction (Advanced)

If you need more control or want to inspect the extracted data first:

#### Step 1: Extract Path and Colors from SVG

```bash
# Basic extraction
python path_extractor.py your_file.svg

# With custom sampling rate (controls number of points)
python path_extractor.py your_file.svg 10

# Limit to specific number of points
python path_extractor.py your_file.svg 10 --num-points 100

# Reverse the path direction
python path_extractor.py your_file.svg 10 --reverse

# Combine options
python path_extractor.py your_file.svg 5 --num-points 50 --reverse
```

This will create a `<filename>_path_config.json` file with:
- Extracted path points
- Suggested shape configuration
- Color information (if available in SVG)
- Metadata (number of points, reversed status)

#### Step 2: Use the Generated Configuration

The generated file includes a `suggested_shape_config` that you can copy directly into your animation configuration:

```json
{
  "type": "shape",
  "shape_config": {
    "shape": "polygon",
    "points": [[x1, y1], [x2, y2], ...],
    "color": "#000000",
    "fill_color": "#CCCCCC",
    "stroke_width": 2
  },
  "mode": "draw",
  "skip_rate": 5
}
```

### Step 3: Customize Colors and Animation

You can customize the configuration:

```json
{
  "type": "shape",
  "shape_config": {
    "shape": "polygon",
    "points": [[x1, y1], [x2, y2], ...],
    "color": "#2C3E50",        // Outline color
    "fill_color": "#3498DB",    // Fill color (NEW!)
    "stroke_width": 3           // Outline thickness
  },
  "mode": "draw",               // Animation mode
  "skip_rate": 5,               // Animation speed
  "z_index": 1                  // Layer order
}
```

## Example Configuration

See `examples/shape_from_svg_example.json` for a complete example showing:
- Shape extracted from SVG with fill colors
- Multiple shapes with different fill colors
- Proper layering and animation

## Supported Shape Types

The `render_shape_to_image` function now properly supports all shape types with fill colors:

### 1. Circle
```json
{
  "shape": "circle",
  "color": "#FF0000",
  "fill_color": "#FFCCCC",
  "stroke_width": 3,
  "position": {"x": 320, "y": 240},
  "size": 100
}
```

### 2. Rectangle
```json
{
  "shape": "rectangle",
  "color": "#0000FF",
  "fill_color": "#CCCCFF",
  "stroke_width": 2,
  "position": {"x": 320, "y": 240},
  "width": 200,
  "height": 150
}
```

### 3. Triangle
```json
{
  "shape": "triangle",
  "color": "#00FF00",
  "fill_color": "#CCFFCC",
  "stroke_width": 2,
  "position": {"x": 320, "y": 240},
  "size": 120
}
```

### 4. Polygon (from SVG)
```json
{
  "shape": "polygon",
  "color": "#2C3E50",
  "fill_color": "#3498DB",
  "stroke_width": 3,
  "points": [[x1, y1], [x2, y2], ...]
}
```

### 5. Line
```json
{
  "shape": "line",
  "color": "#FF6600",
  "stroke_width": 4,
  "start": [100, 240],
  "end": [540, 240]
}
```

### 6. Arrow
```json
{
  "shape": "arrow",
  "color": "#FF6600",
  "fill_color": "#FFAA66",
  "stroke_width": 4,
  "start": [100, 240],
  "end": [540, 240],
  "arrow_size": 30
}
```

## Color Formats

All color parameters support multiple formats:

- **Hex string**: `"#FF5733"`
- **RGB tuple**: `[255, 87, 51]`
- **RGB list**: `(255, 87, 51)`

Colors are automatically converted to OpenCV's BGR format internally.

## Path Extractor Options

### Sampling Rate
Controls the density of extracted points. Lower values = more points = smoother path but larger file.

```bash
python path_extractor.py file.svg 5   # Dense (every 5 pixels)
python path_extractor.py file.svg 10  # Medium (every 10 pixels)
python path_extractor.py file.svg 20  # Sparse (every 20 pixels)
```

### Number of Points
Limit the total number of points for simpler animations:

```bash
python path_extractor.py file.svg 5 --num-points 50   # Max 50 points
python path_extractor.py file.svg 5 --num-points 100  # Max 100 points
```

### Reverse Path
Change the drawing direction:

```bash
python path_extractor.py file.svg 10 --reverse
```

## Workflow Examples

### Easy Way (Automatic Extraction) ⚡

Create an animation from an SVG logo in 2 steps:

```bash
# 1. Create your animation config (animation.json):
{
  "slides": [{
    "duration": 6,
    "layers": [{
      "type": "shape",
      "svg_path": "logo.svg",
      "svg_num_points": 80,
      "shape_config": {
        "color": "#2C3E50",
        "fill_color": "#3498DB",
        "stroke_width": 3
      },
      "mode": "draw",
      "skip_rate": 5
    }]
  }]
}

# 2. Generate the video
python whiteboard_animator.py --config animation.json
```

That's it! The SVG extraction happens automatically.

### Advanced Way (Manual Extraction) 🔧

If you want to inspect or reuse the extracted data:

```bash
# 1. Extract path with colors
python path_extractor.py logo.svg 10 --num-points 80

# 2. This creates logo_path_config.json - inspect it if needed

# 3. Create your animation config (animation.json):
{
  "slides": [{
    "duration": 6,
    "layers": [{
      "type": "shape",
      "shape_config": {
        "shape": "polygon",
        "points": [...],  // Copy from logo_path_config.json
        "color": "#2C3E50",
        "fill_color": "#3498DB",
        "stroke_width": 3
      },
      "mode": "draw",
      "skip_rate": 5
    }]
  }]
}

# 4. Generate the video
python whiteboard_animator.py --config animation.json
```

## Comparison: path_follow vs shape

### Before (path_follow mode)
- ❌ Only draws outline/stroke
- ❌ No fill colors
- ❌ Limited customization

### After (shape type with polygon)
- ✅ Draws both outline AND fill
- ✅ Full color control
- ✅ Better integration with other shapes
- ✅ Consistent animation behavior

## Tips

1. **For complex SVG paths**: Use higher sampling rates (3-5) for smoother curves
2. **For simple shapes**: Use lower sampling rates (10-20) for faster processing
3. **Large files**: Use `--num-points` to limit the number of points
4. **Colors**: If your SVG doesn't have embedded colors, the extractor will use black (#000000) by default. You can manually set colors in the configuration.
5. **Multiple paths in SVG**: The extractor combines all paths into one. If you need separate paths, extract them individually.

## Troubleshooting

### No colors extracted from SVG
- **Issue**: SVG colors are not detected
- **Solution**: Colors might be in CSS styles or external. Manually specify `fill_color` and `color` in the configuration

### Too many/few points
- **Solution**: Adjust sampling rate or use `--num-points` option

### Shape appears inverted
- **Solution**: Use the `--reverse` flag when extracting

### Animation too fast/slow
- **Solution**: Adjust `skip_rate` in the layer configuration (lower = slower, higher = faster)

## See Also

- `examples/shape_from_svg_example.json` - Complete example
- `examples/example_shapes_config.json` - More shape examples
- `README.md` - General documentation
- `SHAPES_GUIDE.md` - Comprehensive shapes guide
