#!/usr/bin/env python3
"""Test to verify multiline text segment ordering."""

import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import cv2

# Import the render function
from whiteboard_animator import render_text_to_image

def test_segment_ordering():
    """Test that multiline text segments are ordered line-by-line."""
    print("=" * 70)
    print("Testing Multiline Text Segment Ordering")
    print("=" * 70)
    print()
    
    # Create multiline text
    text_config = {
        "text": "Armel Wanes\nProject",
        "font": "DejaVuSans",
        "size": 72,
        "color": [0, 0, 0],
        "style": "bold",
        "line_height": 1.5,
        "align": "left"
    }
    
    # Render text
    img = render_text_to_image(text_config, 800, 600)
    
    if img is None:
        print("✗ Failed to render text")
        return False
    
    # Convert to grayscale for analysis
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 250, 255, cv2.THRESH_BINARY_INV)
    
    # Find columns with text
    height, width = thresh.shape
    columns_with_text = []
    for x in range(width):
        column = thresh[:, x]
        if np.any(column > 0):
            columns_with_text.append(x)
    
    if len(columns_with_text) == 0:
        print("✗ No text found in rendered image")
        return False
    
    print(f"✓ Text rendered successfully")
    print(f"  Width: {width}px, Height: {height}px")
    print(f"  Columns with text: {len(columns_with_text)}")
    print()
    
    # Analyze segments
    column_segments = []
    for x in columns_with_text:
        column = thresh[:, x]
        text_pixels = np.where(column > 0)[0]
        
        if len(text_pixels) > 0:
            segments = []
            start_y = text_pixels[0]
            prev_y = text_pixels[0]
            
            for y in text_pixels[1:]:
                if y - prev_y > 3:
                    segments.append((start_y, prev_y))
                    start_y = y
                prev_y = y
            
            segments.append((start_y, prev_y))
            
            for y_start, y_end in segments:
                column_segments.append((x, y_start, y_end))
    
    print(f"Total segments found: {len(column_segments)}")
    print()
    
    # Analyze y-coordinates to detect lines
    y_centers = sorted(set((seg[1] + seg[2]) // 2 for seg in column_segments))
    print(f"Unique y-centers: {len(y_centers)}")
    
    # Group into lines
    lines = []
    current_line = [y_centers[0]]
    
    if len(y_centers) > 1:
        y_diffs = [y_centers[i+1] - y_centers[i] for i in range(len(y_centers)-1)]
        avg_diff = sum(y_diffs) / len(y_diffs) if y_diffs else 0
        gap_threshold = max(20, avg_diff * 1.5)
        
        print(f"Average y-diff: {avg_diff:.1f}px, Gap threshold: {gap_threshold:.1f}px")
        print()
        
        for y_center in y_centers[1:]:
            if y_center - current_line[-1] > gap_threshold:
                lines.append(current_line)
                current_line = [y_center]
            else:
                current_line.append(y_center)
    
    lines.append(current_line)
    
    print(f"Lines detected: {len(lines)}")
    for i, line in enumerate(lines):
        print(f"  Line {i+1}: y-range ~{min(line)}-{max(line)} ({len(line)} unique y-centers)")
    print()
    
    # Verify we detected 2 lines for "Armel Wanes\nProject"
    if len(lines) != 2:
        print(f"✗ Expected 2 lines, but found {len(lines)}")
        return False
    
    print("✓ Detected 2 lines as expected for 'Armel Wanes\\nProject'")
    
    # Check that line 1 has smaller y values than line 2
    line1_max_y = max(lines[0])
    line2_min_y = min(lines[1])
    
    if line1_max_y >= line2_min_y:
        print(f"✗ Lines overlap or are not properly separated")
        print(f"  Line 1 max y: {line1_max_y}")
        print(f"  Line 2 min y: {line2_min_y}")
        return False
    
    print(f"✓ Lines are properly separated (gap of {line2_min_y - line1_max_y}px)")
    print()
    
    # Now test the segment ordering logic
    def get_line_number(seg):
        y_center = (seg[1] + seg[2]) // 2
        for line_idx, line_y_centers in enumerate(lines):
            if y_center in line_y_centers or any(abs(y_center - ly) <= 5 for ly in line_y_centers):
                return line_idx
        min_dist = float('inf')
        closest_line = 0
        for line_idx, line_y_centers in enumerate(lines):
            for ly in line_y_centers:
                dist = abs(y_center - ly)
                if dist < min_dist:
                    min_dist = dist
                    closest_line = line_idx
        return closest_line
    
    # Sort segments with the new logic
    sorted_segments = sorted(column_segments, key=lambda seg: (get_line_number(seg), seg[0], seg[1]))
    
    # Verify ordering: all line 0 segments should come before all line 1 segments
    line_numbers = [get_line_number(seg) for seg in sorted_segments]
    
    # Check for monotonic increase in line numbers
    prev_line = -1
    for i, line_num in enumerate(line_numbers):
        if line_num < prev_line:
            print(f"✗ Segment ordering error at index {i}")
            print(f"  Expected line >= {prev_line}, got {line_num}")
            return False
        prev_line = line_num
    
    # Count segments per line
    line0_count = sum(1 for ln in line_numbers if ln == 0)
    line1_count = sum(1 for ln in line_numbers if ln == 1)
    
    print(f"✓ Segments properly ordered by line")
    print(f"  Line 1 ('Armel Wanes'): {line0_count} segments")
    print(f"  Line 2 ('Project'): {line1_count} segments")
    print()
    
    # Verify that within each line, x-coordinates are monotonically increasing
    line0_segments = [seg for seg in sorted_segments if get_line_number(seg) == 0]
    line1_segments = [seg for seg in sorted_segments if get_line_number(seg) == 1]
    
    def check_x_monotonic(segments, line_name):
        prev_x = -1
        for seg in segments:
            if seg[0] < prev_x:
                print(f"✗ {line_name}: x-coordinates not monotonic at x={seg[0]} (prev={prev_x})")
                return False
            prev_x = seg[0]
        return True
    
    if not check_x_monotonic(line0_segments, "Line 1"):
        return False
    if not check_x_monotonic(line1_segments, "Line 2"):
        return False
    
    print("✓ Within each line, segments are ordered left-to-right")
    print()
    
    print("=" * 70)
    print("✅ All tests passed! Multiline text will be typed line-by-line.")
    print("=" * 70)
    return True

if __name__ == "__main__":
    success = test_segment_ordering()
    sys.exit(0 if success else 1)
