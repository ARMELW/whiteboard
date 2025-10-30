# Before/After Comparison: Positioning Fix

## Issue Description

Elements (text and images) in video generation were not positioned correctly according to the JSON configuration. The coordinates specified in `test-layer.json` did not match the actual positions in the generated video.

## Visual Comparison

### Example Configuration

```json
{
  "type": "text",
  "text_config": {
    "text": "Votre texte ici",
    "align": "center",
    "size": 48
  },
  "position": {"x": 800, "y": 450}
}
```

### Before the Fix ❌

**Problem:**
- Text with `align="center"` was centered in the **entire canvas**
- The `position` then offset this already-centered text
- Result: Text appeared at wrong coordinates

**Behavior:**
1. Canvas is 1920x1080
2. Text "Votre texte ici" is centered → appears at x≈960 (canvas center)
3. Layer position adds offset: 960 + 800 = 1760
4. **Final position: x=1760** (wrong!)

```
Before Fix - Center Alignment:
┌─────────────────────────────────────┐
│                                     │
│                                     │
│                                     │
│                          Text       │  ← Wrong position (x≈1760)
│                                     │  Expected at x=800
│                                     │
└─────────────────────────────────────┘
  x=0                              x=1920
       x=800 (expected)
```

**Other Issues:**
- Changing position coordinates in JSON had unexpected or no effect
- Images were auto-centered instead of using exact coordinates
- Editor preview didn't match generated video
- Alignment affected position anchor point (incorrect behavior)

### After the Fix ✅

**Solution:**
- Text is rendered at position (0, 0) within the canvas
- Layer system positions the entire text at `layer.position`
- `align="center"` only affects multi-line text alignment within the bounding box

**Behavior:**
1. Text rendered at x=0 with centered lines (for multi-line)
2. Layer system positions text block at x=800
3. **Final position: x=800** (correct!)

```
After Fix - Center Alignment:
┌─────────────────────────────────────┐
│                                     │
│                                     │
│                                     │
│          Text                       │  ← Correct position (x=800)
│                                     │
│                                     │
└─────────────────────────────────────┘
  x=0                              x=1920
       x=800 ✓
```

## Multi-line Text Alignment

### Before Fix ❌

Each line was positioned independently based on alignment:

```json
{
  "text": "Line One\nLonger Line Two\nShort",
  "align": "center",
  "position": {"x": 100, "y": 100}
}
```

**Problem:** Lines appeared centered in canvas, position had unpredictable effect.

### After Fix ✅

Lines are aligned **relative to each other**, bounding box starts at position:

```
align="left":               align="center":           align="right":
x=100                      x=100                     x=100
↓                          ↓                         ↓
┌─────────────────┐        ┌─────────────────┐       ┌─────────────────┐
│Line One         │        │    Line One     │       │         Line One│
│Longer Line Two  │        │ Longer Line Two │       │  Longer Line Two│
│Short            │        │      Short      │       │            Short│
└─────────────────┘        └─────────────────┘       └─────────────────┘
^ All start at x=100       ^ Centered within box     ^ Right-aligned in box
                           Box starts at x=100       Box starts at x=100
```

## Real World Example from Issue

### Scenario
Editor layout with:
- Person image on the left (x=100, y=300)
- Speech bubble on the right (x=1500, y=300)
- Text "Votre texte ici" centered between them (x=800, y=450)

### Before Fix ❌

```
Generated Video (Incorrect):
┌────────────────────────────────────────┐
│                                        │
│       [Person]                         │  ← Too centered
│            "Votre texte ici"           │  ← Wrong position
│                    [Bubble]            │  ← Too centered
│                                        │
└────────────────────────────────────────┘
```

**Problems:**
- Person image not at left edge (x=100)
- Bubble not at right position (x=1500)
- Text displaced from center position (x=800)
- Layout completely different from editor

### After Fix ✅

```
Generated Video (Correct):
┌────────────────────────────────────────┐
│                                        │
│ [Person]          "Votre texte ici"    │  [Bubble]
│  x=100                  x=800           x=1500
│                                        │
└────────────────────────────────────────┘
```

**Results:**
- ✅ Person image exactly at x=100 (left edge)
- ✅ Text exactly at x=800 (center position)
- ✅ Bubble exactly at x=1500 (right position)
- ✅ Layout matches editor preview perfectly

## Test Results

### Verification Test

```python
# All three texts with different alignments
# All should start at the same x position (100)

layers = [
    {"text": "LEFT aligned at (100, 100)", "align": "left", "position": {"x": 100, "y": 100}},
    {"text": "CENTER aligned at (100, 200)", "align": "center", "position": {"x": 100, "y": 200}},
    {"text": "RIGHT aligned at (100, 300)", "align": "right", "position": {"x": 100, "y": 300}}
]
```

**Before Fix:** ❌
- LEFT text at x=100 ✓
- CENTER text at x≈960 (canvas center) ❌
- RIGHT text at x≈1800 (canvas right) ❌

**After Fix:** ✅
- LEFT text at x=100 ✓
- CENTER text at x=100 ✓
- RIGHT text at x=100 ✓

All three texts now start at x=100 as expected! The alignment only affects the internal text layout for multi-line text.

## Code Comparison

### Before Fix

```python
# render_text_to_image()
if position and 'x' in position:
    x = position['x']  # Use position directly
    # Problem: This positions text at absolute canvas coordinate
```

Then in layer system:
```python
# compose_layers()
position = layer.get('position', {'x': 0, 'y': 0})
# Copy layer image to canvas at position
# Problem: Image already positioned, so double positioning!
```

### After Fix

```python
# In compose_layers() / draw_layered_whiteboard_animations()
# Force text to render at (0,0)
text_config_for_render = text_config.copy()
text_config_for_render['position'] = {'x': 0, 'y': 0}
layer_img = render_text_to_image(text_config_for_render, width, height)
# Now layer system can position it correctly using layer.position
```

```python
# render_text_to_image() - improved alignment
if position and 'x' in position:
    base_x = position['x']  # Start at position
    if align == 'center':
        # Center line relative to widest line
        x = base_x + (max_line_width - line_width) // 2
    elif align == 'right':
        # Right-align relative to widest line
        x = base_x + (max_line_width - line_width)
    else:  # left
        x = base_x  # All lines start at base_x
```

## Key Takeaways

### Position Semantics

**Before:** Position meaning was inconsistent
- Sometimes it was center
- Sometimes it was offset from center
- Depended on alignment setting

**After:** Position is always top-left corner
- Consistent across all elements
- Predictable behavior
- Matches standard UI/graphics conventions

### Alignment Semantics

**Before:** Alignment affected position anchor
- `center` → element centered in canvas
- `right` → element right-aligned in canvas
- Unpredictable interaction with position

**After:** Alignment only affects internal layout
- For multi-line text: how lines align relative to each other
- For single-line text: no effect (as expected)
- Position anchor always at top-left

### Impact

✅ **Fixed:** Elements respect JSON coordinates
✅ **Fixed:** Generated video matches editor preview
✅ **Fixed:** Changing coordinates immediately reflects in output
✅ **Improved:** Multi-line text alignment works correctly
✅ **Maintained:** Backward compatibility with old JSON files

## Migration

### Old JSON Files (Still Work)

```json
{
  "type": "text",
  "text_config": {
    "text": "Hello",
    "position": {"x": 100, "y": 200}
  }
}
```

Automatically converted to:
```json
{
  "type": "text",
  "text_config": {
    "text": "Hello"
  },
  "position": {"x": 100, "y": 200}
}
```

### Recommended Structure

```json
{
  "type": "text",
  "text_config": {
    "text": "Hello",
    "align": "center"
  },
  "position": {"x": 100, "y": 200},
  "z_index": 1
}
```

Position at layer level is now the authoritative source.
