# Fix: Background Draw Pixelation Issue

## Problem Description

**Original Issue (French):**
> le probleme precedent, celui du coloration encore du bug, j'ai cette code celui d'avant, mais quand j'ai ajouté quelque chose ca a cassé et en plus il l'a fait pixel par pixel mais pas du drawing stroke

**Translation:**
The previous coloration problem still has a bug. After adding something, it broke and it's drawing pixel by pixel but not following the drawing strokes.

**Visual Symptom:**
During animation, the background appeared pixelated/checkered with grayscale blocks instead of staying clean and white. The entire tile rectangles were being drawn in grayscale, not just the actual strokes/edges.

## Root Cause

In the `draw_masked_object()` function (lines 2604-2616), the grayscale animation fix was drawing entire rectangular tiles in grayscale without considering the threshold mask. This meant:

1. **Foreground pixels** (actual strokes/edges where `threshold < black_pixel_threshold`) were correctly drawn in grayscale
2. **Background pixels** within the tile rectangle were ALSO drawn in grayscale
3. This created a checkered/pixelated effect as tiles were drawn one by one

**Previous code (caused pixelation):**
```python
# Obtenir la tuile correspondante de l'image en niveaux de gris pour l'animation
gray_tile = variables.img_gray[range_v_start:range_v_end, range_h_start:range_h_end]

# Appliquer la tuile au cadre de dessin
if mode == 'eraser':
    variables.drawn_frame[range_v_start:range_v_end, range_h_start:range_h_end] = 255
else:
    # Drawing the ENTIRE tile in grayscale (including background)
    gray_tile_bgr = cv2.cvtColor(gray_tile, cv2.COLOR_GRAY2BGR)
    variables.drawn_frame[range_v_start:range_v_end, range_h_start:range_h_end] = gray_tile_bgr
```

## Solution

Modified the drawing logic to apply the threshold mask when drawing tiles. Now:

1. **Create a content mask** from the threshold (`tile_to_draw < black_pixel_threshold`)
2. **Only draw pixels where the mask is True** (actual content/strokes)
3. **Leave background pixels untouched** (they remain white from initialization)

**Fixed code:**
```python
# Obtenir la tuile correspondante de l'image en niveaux de gris pour l'animation
gray_tile = variables.img_gray[range_v_start:range_v_end, range_h_start:range_h_end]

# Appliquer la tuile au cadre de dessin
if mode == 'eraser':
    variables.drawn_frame[range_v_start:range_v_end, range_h_start:range_h_end] = 255
else:
    # En mode normal, dessiner en niveaux de gris pendant l'animation
    # Mais seulement où le threshold indique du contenu (pixels noirs < threshold)
    # Créer un masque basé sur le threshold (tile_to_draw)
    content_mask = tile_to_draw < black_pixel_threshold
    
    # Convertir la tuile en niveaux de gris en BGR (3 canaux)
    gray_tile_bgr = cv2.cvtColor(gray_tile, cv2.COLOR_GRAY2BGR)
    
    # Appliquer seulement les pixels de contenu (où le masque est True)
    # Cela permet de dessiner uniquement les traits/bords, pas le fond
    frame_region = variables.drawn_frame[range_v_start:range_v_end, range_h_start:range_h_end]
    frame_region[content_mask] = gray_tile_bgr[content_mask]
    variables.drawn_frame[range_v_start:range_v_end, range_h_start:range_h_end] = frame_region
```

## Testing

### Test Script
A comprehensive test script was created: `test_background_draw_fix.py`

The test:
1. Creates a test image with clear foreground shapes and gradient background
2. Generates an animation
3. Analyzes frames to verify:
   - Background regions stay white/clean (no pixelation)
   - Foreground strokes are drawn in grayscale during animation
   - Color is revealed at the end

### Test Results
```
======================================================================
Background Draw Fix - Test
======================================================================

1. Creating test image: /tmp/test_bg_draw.jpg
   ✅ Test image created

2. Generating animation...
   ✅ Animation generated

3. Analyzing video frames...
   Total frames: 70
   Background clean: ✅
   Grayscale during animation: ✅
   Color revealed at end: ✅

======================================================================
✅ TEST PASSED - Background draw fix is working correctly!
======================================================================
```

### Manual Verification
Tested with both synthetic test images and real repository images:

**Frame analysis during animation:**
- Background regions: mean ~251 (white), channel variance ~1.6 (very consistent)
- Stroke regions: mean ~50-120 (grayscale), color diff < 10 (R≈G≈B)

**Frame analysis after animation:**
- Color revealed: color diff > 20 (distinct R, G, B values)
- Background stays clean throughout

## Impact

✅ **Fixed:**
- Eliminates pixelated/checkered background effect during animation
- Only strokes/edges are drawn, following the threshold mask
- Creates clean, professional whiteboard animation effect
- Background remains pristine white during drawing

✅ **Preserved:**
- Grayscale animation behavior (strokes in grayscale → color reveal)
- All animation modes (draw, eraser, static)
- Layer support and opacity blending
- Performance characteristics

## Minimal Change

- **Files modified:** 1 (`whiteboard_animator.py`)
- **Lines changed:** 9 (added content mask logic)
- **Functions affected:** 1 (`draw_masked_object`)
- **Test coverage:** Comprehensive test added

## Usage

No changes to command-line usage. The fix is automatic:

```bash
# Single image
python whiteboard_animator.py image.jpg --split-len 20 --frame-rate 30

# With layers
python whiteboard_animator.py placeholder.png --config layers.json

# All options work unchanged
python whiteboard_animator.py image.jpg --split-len 20 --duration 5 --frame-rate 30
```

## Technical Details

**Key insight:** The `tile_to_draw` variable contains the threshold mask showing where actual content (edges/strokes) exists. By using this as a content mask:
```python
content_mask = tile_to_draw < black_pixel_threshold
```

We ensure that only pixels with actual drawn content are copied from the grayscale tile, while background pixels (where threshold ≥ black_pixel_threshold) remain untouched.

This is the correct behavior because:
1. The threshold identifies edges/strokes (dark pixels in grayscale)
2. Background areas have high threshold values (white/light in grayscale)
3. We want to draw the edges but not the background

## Notes

- The fix applies to all drawing modes except 'eraser' mode
- Works correctly with both single-layer and multi-layer animations
- Compatible with all existing features (transitions, watermarks, audio, etc.)
- The small color differences in compressed video (2-3 units) are expected due to H.264 compression
