# SVG-Based Text Handwriting Implementation (Opt-In Feature)

## Overview

This implementation adds **VideoScribe-style text handwriting animation** using SVG path extraction from font outlines. This provides a more natural and authentic handwriting effect that follows the actual character strokes defined in the font.

**⚠️ Important:** As of the latest update, this feature is **opt-in**. By default, text layers use the simpler column-based approach. To enable SVG path-based drawing, add `"use_svg_paths": true` to your text configuration.

## Default vs Opt-In Behavior

### Default (Column-Based)
Text layers use a simpler, pixel-based column-by-column approach that works on all systems without additional dependencies.

### Opt-In (SVG Path-Based)
When you explicitly set `"use_svg_paths": true`, the system will attempt to use SVG path extraction for more authentic character stroke order.

**To enable SVG path-based drawing:**
```json
{
  "text_config": {
    "text": "Hello World!",
    "use_svg_paths": true
  }
}
```

## How It Works (VideoScribe Approach)

### 1. Text to SVG Path Conversion
When you add text to a layer:
- The text is converted to vector paths using the font's glyph outlines
- Each letter becomes a series of path commands (moveTo, lineTo, curveTo)
- The paths define the exact contours of each character

### 2. Path-Based Drawing
The system creates a drawing sequence that:
- Follows the actual stroke paths from the font
- Draws in a natural order (left to right, top to bottom)
- Maintains proper character proportions and spacing
- Respects text alignment and positioning

### 3. Progressive Animation
The animation works by:
- Drawing each path segment sequentially
- Positioning the hand at each point along the path
- Creating frames at intervals defined by `skip_rate`
- Revealing the text progressively as paths are drawn

### 4. Timing Control
The speed and flow are controlled by:
- `skip_rate`: Lower values = slower, more detailed animation
- `pause_after_char`: Frames to pause after each character (creates more natural rhythm)
- `pause_after_word`: Frames to pause after each word (future enhancement)
- Character spacing and line height affect drawing duration
- Each path segment is drawn smoothly with hand following

### 5. Natural Writing Flow
The animation creates realistic handwriting by:
- Following font-defined stroke order
- Smooth hand movement along character paths
- Optional pauses between characters for natural rhythm
- Progressive reveal as text is written

## Technical Implementation

### Core Functions

#### 1. `extract_character_paths(text, font_path, font_size)`
Extracts vector paths from TTF/OTF font files using fontTools.

**Features:**
- Uses RecordingPen to capture glyph drawing commands
- Handles moveTo, lineTo, qCurveTo, and closePath commands
- Supports any font that provides glyph outlines
- Handles spaces and line breaks appropriately

**Example:**
```python
char_paths = extract_character_paths("Hello", "/path/to/font.ttf", 48)
# Returns list of character path data
```

#### 2. `convert_glyph_paths_to_points(char_paths, font_size, text_config, target_width, target_height)`
Converts font glyph paths to screen coordinates.

**Features:**
- Respects text alignment (left, center, right)
- Handles multi-line text with proper line height
- Applies absolute positioning if specified
- Scales paths from font units to pixels
- Maintains proper character spacing

**Returns:**
List of drawing segments (sequences of coordinate points)

#### 3. `draw_svg_path_handwriting(variables, skip_rate, mode, text_config=None, ...)`
Main drawing function with SVG path support.

**Features:**
- Automatically detects if font supports path extraction
- Falls back to column-based drawing if extraction fails
- Draws each path segment with hand following
- Supports draw and eraser modes
- Clips coordinates to image bounds

**Fallback Behavior:**
If SVG path extraction fails (font not found, no glyph data), the system automatically falls back to the existing column-based drawing algorithm.

## Usage

### Basic Text with SVG Paths

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
        "style": "bold",
        "align": "center"
      }
    }]
  }]
}
```

### Multi-line Text

```json
{
  "type": "text",
  "skip_rate": 5,
  "text_config": {
    "text": "Line 1\nLine 2\nLine 3",
    "font": "DejaVuSans",
    "size": 48,
    "line_height": 1.5,
    "align": "left"
  }
}
```

### Custom Positioning

```json
{
  "type": "text",
  "skip_rate": 4,
  "text_config": {
    "text": "Fixed Position",
    "size": 56,
    "position": {"x": 100, "y": 200}
  }
}
```

### With Timing Controls (Pauses Between Characters)

```json
{
  "type": "text",
  "skip_rate": 2,
  "text_config": {
    "text": "Hello World!",
    "size": 72,
    "pause_after_char": 3,
    "align": "center"
  }
}
```

### Disable SVG Path-Based (Use Column-Based)

```json
{
  "type": "text",
  "skip_rate": 5,
  "text_config": {
    "text": "Column-based drawing",
    "size": 48,
    "use_svg_paths": false
  }
}
```

## Configuration Options

### Text Configuration

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `text` | string | Required | Text content (use `\n` for line breaks) |
| `font` | string | "Arial" | Font family name |
| `size` | int | 32 | Font size in pixels |
| `color` | RGB/hex | `[0, 0, 0]` | Text color |
| `style` | string | "normal" | "normal", "bold", "italic", "bold_italic" |
| `line_height` | float | 1.2 | Line spacing multiplier |
| `align` | string | "left" | "left", "center", "right" |
| `position` | dict | null | Optional `{x, y}` for absolute positioning |
| `use_svg_paths` | bool | true | Enable/disable SVG path-based drawing |
| `pause_after_char` | int | 0 | Number of frames to pause after each character |
| `pause_after_word` | int | 0 | Number of frames to pause after each word (not yet implemented) |

### Layer Configuration

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `skip_rate` | int | 8 | Animation speed (lower = slower, more frames) |
| `mode` | string | "draw" | "draw", "eraser", or "static" |
| `z_index` | int | 0 | Layer drawing order |

## Advantages of SVG Path-Based Approach

### ✅ Natural Stroke Order
- Follows actual character contours from font design
- Creates authentic handwriting appearance
- Respects font designer's intended stroke order

### ✅ Precise Character Rendering
- Uses exact font outlines
- Maintains proper letter proportions
- No pixel-based approximations

### ✅ Better Quality
- Vector-based drawing is resolution-independent
- Smooth curves from font bezier paths
- Clean, professional results

### ✅ Automatic Fallback
- If path extraction fails, uses column-based method
- No configuration needed
- Works with all fonts

## Comparison: Path-Based vs Column-Based

### Path-Based (New - SVG)
```
Drawing order: Follows font stroke paths
  ████████████████████████
  H → e → l → l → o
(Smooth path following)
Result: ✅ Natural handwriting effect
        ✅ Follows actual character strokes
        ✅ Professional appearance
```

### Column-Based (Previous)
```
Drawing order: Left to right, column by column
  ████████████████████████
  H → → → e → → l → l → o
(Vertical segments per column)
Result: ✅ Natural left-to-right motion
        ✅ Good for simple text
        ⚠️  Less authentic stroke order
```

### Tile-Based (For Images)
```
Drawing order: Nearest tile first
  ████ → ██ → ██ → ████
(Random proximity jumps)
Result: ✅ Efficient for complex drawings
        ❌ Not suitable for text
```

## Performance Considerations

### Animation Speed
- **Path-based:** ~2-8 frames per character (depends on skip_rate)
- **Recommended skip_rate:** 3-5 for smooth writing
- **Faster text:** skip_rate = 6-10
- **Slower detailed:** skip_rate = 2-4

### Font Compatibility
- Works with all TTF and OTF fonts that provide glyph outlines
- Automatically tested: DejaVuSans, Liberation fonts
- Falls back gracefully if font doesn't support path extraction

## Examples

### Simple Handwriting
```bash
python whiteboard_animator.py --config test_svg_text.json
```

### Full Featured Example
```bash
python whiteboard_animator.py --config examples/text_layer_example.json
```

## Dependencies

- **fontTools** - For font glyph path extraction
  ```bash
  pip install fonttools
  ```

- **PIL/Pillow** - For text rendering (already required)
- **OpenCV** - For video generation (already required)

## Backward Compatibility

✅ **100% Backward Compatible**

- Existing text layers work unchanged
- Automatically uses path-based if available
- Falls back to column-based if needed
- No breaking changes to API
- All existing features preserved

## Troubleshooting

### "Using column-based drawing" Message
This means SVG path extraction couldn't be used. Reasons:
- Font file not found in system paths
- Font doesn't provide glyph outline data
- fontTools library not installed

**Solution:** Install fontTools or use a different font:
```bash
pip install fonttools
```

### Text Position Incorrect
- Check `position` parameter in text_config
- Verify `align` setting (left/center/right)
- Adjust `line_height` for multi-line text

### Animation Too Fast/Slow
- Adjust `skip_rate` parameter
- Lower values = slower, more detailed
- Higher values = faster animation

## Future Enhancements

Potential improvements based on VideoScribe features:

1. **Stroke + Fill Animation**
   - Draw outline first
   - Fill interior after slight delay

2. **Pause Between Characters**
   - Add configurable delays between letters/words
   - More natural human-like writing

3. **Custom Stroke Order**
   - Allow manual path order definition
   - Support for specific handwriting styles

4. **Progressive Masking**
   - More sophisticated reveal effects
   - Gradient-based masking

## Testing

### Test File Included
```bash
# Simple test
python whiteboard_animator.py --config test_svg_text.json

# Complex test with multiple layers
python whiteboard_animator.py --config examples/text_layer_example.json
```

### Expected Output
- Console shows "Using SVG path-based drawing" message
- Video shows smooth character-by-character writing
- Hand follows natural stroke paths

## References

This implementation is inspired by how VideoScribe handles text animation:
- Text converted to vector paths
- Path-guided hand animation
- Progressive reveal of characters
- Natural writing order

See issue description for more details on the VideoScribe approach.
