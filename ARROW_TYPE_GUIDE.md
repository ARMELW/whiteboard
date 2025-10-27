# Arrow Type Layer Feature

## Overview

The arrow type layer feature allows you to draw arrows with progressive animation, as if drawing them by hand. This is different from the `shape` type with `arrow` shape, which draws arrows using the standard masked drawing method.

## Usage

### Basic Configuration

To use an arrow type layer, set `type: "arrow"` in your layer configuration and provide an `arrow_config` object:

```json
{
  "type": "arrow",
  "arrow_config": {
    "start": [x1, y1],
    "end": [x2, y2],
    "color": "#FF0000",
    "fill_color": "#FFAAAA",
    "stroke_width": 5,
    "arrow_size": 40,
    "duration": 2.0
  },
  "z_index": 1,
  "mode": "draw"
}
```

### Configuration Options

#### Required Parameters

- **start**: `[x, y]` - Starting point of the arrow
- **end**: `[x, y]` - Ending point of the arrow

#### Optional Parameters

- **color**: Arrow line color
  - Hex string: `"#FF0000"`
  - RGB list: `[255, 0, 0]`
  - RGB tuple: `(255, 0, 0)`
  - Default: `(0, 0, 0)` (black)

- **fill_color**: Arrow head fill color (same formats as color)
  - Default: `None` (no fill)

- **stroke_width**: Line thickness in pixels
  - Default: `2`

- **arrow_size**: Arrow head size in pixels
  - Default: `20`

- **duration**: Animation duration in seconds
  - Default: `2.0`

### Animation Behavior

The arrow is drawn progressively:
1. **0% - 80%**: Draws the arrow shaft from start to end
2. **80% - 90%**: Draws the first line of the arrow head
3. **90% - 100%**: Draws the second line of the arrow head
4. **100%**: Fills the arrow head (if fill_color is specified)

This creates a natural, hand-drawn appearance.

## Examples

### Simple Horizontal Arrow

```json
{
  "type": "arrow",
  "arrow_config": {
    "start": [200, 400],
    "end": [800, 400],
    "color": "#E74C3C",
    "fill_color": "#F1948A",
    "stroke_width": 5,
    "arrow_size": 40,
    "duration": 2.0
  },
  "z_index": 1,
  "mode": "draw"
}
```

### Diagonal Arrow

```json
{
  "type": "arrow",
  "arrow_config": {
    "start": [300, 500],
    "end": [900, 200],
    "color": "#3498DB",
    "fill_color": "#85C1E9",
    "stroke_width": 4,
    "arrow_size": 35,
    "duration": 1.5
  },
  "z_index": 2,
  "mode": "draw"
}
```

### Arrow Without Fill

```json
{
  "type": "arrow",
  "arrow_config": {
    "start": [600, 250],
    "end": [600, 550],
    "color": "#F39C12",
    "stroke_width": 4,
    "arrow_size": 35,
    "duration": 1.5
  },
  "z_index": 3,
  "mode": "draw"
}
```

## Complete Example

See `examples/arrow_type_demo.json` for a complete working example with:
- Multiple arrows with different styles
- Integration with text and shape layers
- Process flow diagram

## Differences from Shape Type Arrow

### Arrow Type (`type: "arrow"`)
- Progressive drawing animation
- Draws as a path from start to end
- Natural hand-drawn appearance
- Controlled by `duration` parameter
- Automatically animated

### Shape Type (`type: "shape"` with `shape: "arrow"`)
- Standard masked tile-based drawing
- Draws using the hand/eraser tool
- Uses `skip_rate` for speed control
- Requires separate path_animation for movement

## Tips

1. **Duration**: Adjust `duration` to control how fast the arrow is drawn (2.0 seconds is a good default)

2. **Arrow Size**: Larger `arrow_size` values create more prominent arrow heads (30-40 works well)

3. **Colors**: Use fill_color to make the arrow head more visible and professional

4. **Z-Index**: Place arrows on appropriate layers to ensure they appear above or below other elements

5. **Combining Arrows**: Create process flows by combining multiple arrows with shapes and text

## Testing

Run the test suite to verify arrow type functionality:

```bash
python test_arrow_type.py
```

This tests:
- Progressive drawing at different progress levels
- Hex color support
- Diagonal arrows
- Arrows without fill colors

## Technical Details

The arrow type layer is implemented in `whiteboard_animator.py`:

- `draw_arrow_progressive()`: Draws the arrow progressively based on progress (0-1)
- Layer processing handles `type: "arrow"` in both:
  - `draw_slide_layers()`: For animated drawing
  - `compose_layers()`: For static composition

The progressive drawing ensures a smooth, natural animation that looks like someone drawing an arrow by hand.
