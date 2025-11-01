# Quick Fix Guide - Element Position Correction

## Your Issue
Elements in the exported video don't match their positions in the editor.

## Solution
Add canvas dimensions to your JSON configuration.

## Step-by-Step Fix

### 1. Update Your JSON Config

**Before:**
```json
{
  "slides": [
    {
      "index": 0,
      "duration": 2,
      "layers": [ ... ]
    }
  ]
}
```

**After:**
```json
{
  "canvas_width": 1920,
  "canvas_height": 1080,
  "slides": [
    {
      "index": 0,
      "duration": 2,
      "layers": [ ... ]
    }
  ]
}
```

### 2. Verify Canvas Dimensions

The canvas dimensions should match what your editor uses:
- Default editor canvas: **1920x1080**
- Check `SceneCanvas.tsx` in whiteboard-frontend if unsure

### 3. Regenerate Video

```bash
python whiteboard_animator.py --config examples/test-layer.json --preview --aspect-ratio 16:9
```

### 4. Check Console Output

You should see:
```
📏 Canvas original: 1920x1080
📏 Scaling positions: x=1.000, y=1.000
```

If scaling shows 1.000, positions won't change (dimensions match).
If scaling shows different values, positions will be adjusted.

## For Your Specific Case (test-layer.json)

Your current JSON positions:
- Image 1: (583, 336)
- Text 1: (1049, 518)  
- Text 2: (1027, 671)
- Image 2: (1146, 333)
- Text 3: (1151, 396)

These positions are already for a 1920x1080 canvas. Adding explicit canvas dimensions ensures they're interpreted correctly:

```json
{
  "canvas_width": 1920,
  "canvas_height": 1080,
  "slides": [ your existing slides ]
}
```

## If Positions Are Still Wrong

### Check 1: Image URLs
Your JSON uses localhost URLs:
```json
"image_path": "http://localhost:9000/assets/..."
```

These need to be accessible. Either:
- Run the MinIO server on localhost:9000
- Replace with direct file paths
- Use publicly accessible URLs

### Check 2: Compare Coordinates

Take a screenshot of your editor at the exact position you want.
Note the X, Y coordinates from the editor's position panel.
Compare with the JSON positions.

If they don't match, update the JSON positions to match the editor.

### Check 3: Aspect Ratio

Ensure you're using the same aspect ratio:
```bash
# Your command uses 16:9
python whiteboard_animator.py --config examples/test-layer.json --preview --aspect-ratio 16:9

# Make sure the editor is also showing 16:9 aspect ratio
```

## Testing Without Images

If you can't access the images, test with text-only layers:

```json
{
  "canvas_width": 1920,
  "canvas_height": 1080,
  "slides": [
    {
      "index": 0,
      "duration": 2,
      "layers": [
        {
          "type": "text",
          "mode": "draw",
          "text_config": {
            "text": "Test Position",
            "font": "Arial",
            "size": 48,
            "color": [255, 0, 0],
            "position": {
              "x": 960,
              "y": 540
            }
          }
        }
      ]
    }
  ]
}
```

This should appear centered in the video (960, 540 is center of 1920x1080).

## Frontend Update Required

For a permanent fix, update whiteboard-frontend to export canvas dimensions automatically:

**File:** `src/utils/sceneExporter.ts` (or similar export utility)

**Add this to the export function:**
```typescript
const exportedConfig = {
  canvas_width: 1920,   // From SceneCanvas.tsx
  canvas_height: 1080,  // From SceneCanvas.tsx
  slides: exportedSlides
};
```

## Need More Help?

1. Check `POSITION_FIX_SUMMARY.md` for complete documentation
2. Run `python3 test_position_scaling.py` to verify the fix works
3. Check `CONFIG_FORMAT.md` for all configuration options

## Quick Validation

To verify positions are correct after regenerating:

1. **In Editor**: Note the X,Y position of an element (e.g., "583, 336")
2. **In JSON**: Check the same element's position matches
3. **In Video**: Element should appear at the same relative position

If element appears more left/right or up/down than expected:
- Canvas dimensions might be wrong
- Positions in JSON might be incorrect
- Aspect ratio might differ between editor and video

## Expected Result

After applying this fix with correct canvas dimensions:
- ✅ Elements in video match editor positions exactly
- ✅ Text appears at the same location
- ✅ Images are positioned correctly
- ✅ No unexpected scaling or shifting
