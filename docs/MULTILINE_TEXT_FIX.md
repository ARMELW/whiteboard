# Multiline Text Typing Fix

## Issue
When writing multiline text (e.g., "Armel Wanes\nProject"), the text handwriting animation was not distinguishing between lines. It would write all text column-by-column from left to right across ALL lines simultaneously, rather than finishing one line before moving to the next.

### Example Problem
Text: "Armel Wanes\nProject"

**Before fix:** Would draw like this:
1. Column 0: "A" from "Armel" + "P" from "Project" (both lines at once)
2. Column 1: "r" from "Armel" + "r" from "Project" (both lines at once)
...and so on

**After fix:** Draws line-by-line:
1. Write "Armel Wanes" completely from left to right
2. Then write "Project" from left to right

## Solution

Modified the `draw_text_handwriting()` function in `whiteboard_animator.py` to:

1. **Detect line breaks** by analyzing y-coordinate gaps in the rendered text
2. **Group segments by line** using a gap threshold (1.5x average y-spacing, minimum 20px)
3. **Sort segments** by (line_number, x_coordinate, y_coordinate) instead of just (x, y)

### Technical Details

The fix adds line detection logic after segment collection:

```python
# Find line breaks by detecting significant y-coordinate gaps
y_centers = sorted(set((seg[1] + seg[2]) // 2 for seg in column_segments))

# Group y_centers into lines
lines = []
current_line = [y_centers[0]]

if len(y_centers) > 1:
    y_diffs = [y_centers[i+1] - y_centers[i] for i in range(len(y_centers)-1)]
    avg_diff = sum(y_diffs) / len(y_diffs) if y_diffs else 0
    gap_threshold = max(20, avg_diff * 1.5)
    
    for y_center in y_centers[1:]:
        if y_center - current_line[-1] > gap_threshold:
            lines.append(current_line)
            current_line = [y_center]
        else:
            current_line.append(y_center)
```

Then segments are sorted with line number as the primary key:

```python
column_segments.sort(key=lambda seg: (get_line_number(seg), seg[0], seg[1]))
```

## Usage

Simply use newline characters (`\n`) in your text configuration:

```json
{
  "type": "text",
  "text_config": {
    "text": "First Line\nSecond Line\nThird Line",
    "font": "DejaVuSans",
    "size": 60,
    "line_height": 1.5
  }
}
```

The handwriting animation will now write each line completely before moving to the next line.

## Testing

Run the included tests to verify the fix:

```bash
# Test segment ordering for multiline text
python3 test_segment_ordering.py

# Comprehensive test with 1, 2, 3, and 4-line texts
python3 test_comprehensive_text_ordering.py

# Existing text rendering tests (should all still pass)
python3 test_text_rendering.py
```

## Example

Try the example configuration:

```bash
python3 whiteboard_animator.py --config examples/multiline_text_example.json
```

This demonstrates the fixed behavior with "Armel Wanes\nProject" text.

## Compatibility

- ✅ **Single-line text**: Works as before
- ✅ **Multiline text**: Now writes line-by-line
- ✅ **SVG path-based text**: Already handled correctly, no changes needed
- ✅ **All text alignments**: left, center, right
- ✅ **All text styles**: normal, bold, italic, bold_italic
- ✅ **Backward compatible**: No configuration changes required

## Notes

- The SVG path-based handwriting (`draw_svg_path_handwriting`) already handled multiline text correctly
- This fix only affects the column-based fallback method (`draw_text_handwriting`)
- Line detection is automatic based on y-coordinate gaps
- Works with any number of lines (tested with 1-4 lines)
- Minimum gap threshold of 20px prevents false line breaks within single lines
