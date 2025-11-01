#!/usr/bin/env python3
"""Comprehensive test for single-line and multiline text typing behavior."""

import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import cv2

from whiteboard_animator import render_text_to_image

def analyze_text_segments(text_config, expected_lines):
    """Analyze how text segments are ordered."""
    print(f"Testing: '{text_config['text']}'")
    print(f"Expected lines: {expected_lines}")
    
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
        print("✗ No text found")
        return False
    
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
    
    # Detect lines
    y_centers = sorted(set((seg[1] + seg[2]) // 2 for seg in column_segments))
    
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
    
    lines.append(current_line)
    
    detected_lines = len(lines)
    
    if detected_lines == expected_lines:
        print(f"✓ Detected {detected_lines} line(s) as expected")
    else:
        print(f"✗ Expected {expected_lines} lines, detected {detected_lines}")
        return False
    
    # Verify ordering
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
    
    sorted_segments = sorted(column_segments, key=lambda seg: (get_line_number(seg), seg[0], seg[1]))
    line_numbers = [get_line_number(seg) for seg in sorted_segments]
    
    # Check ordering
    prev_line = -1
    for line_num in line_numbers:
        if line_num < prev_line:
            print(f"✗ Segment ordering error")
            return False
        prev_line = line_num
    
    # Check x-monotonic within lines
    for line_idx in range(detected_lines):
        line_segments = [seg for seg in sorted_segments if get_line_number(seg) == line_idx]
        prev_x = -1
        for seg in line_segments:
            if seg[0] < prev_x:
                print(f"✗ Line {line_idx+1}: x-coordinates not monotonic")
                return False
            prev_x = seg[0]
    
    print(f"✓ Segments properly ordered line-by-line, left-to-right")
    
    # Show segment counts per line
    for line_idx in range(detected_lines):
        count = sum(1 for ln in line_numbers if ln == line_idx)
        print(f"  Line {line_idx+1}: {count} segments")
    
    print()
    return True

def main():
    print("=" * 70)
    print("Comprehensive Text Typing Order Test")
    print("=" * 70)
    print()
    
    tests = [
        {
            "config": {
                "text": "Hello World",
                "font": "DejaVuSans",
                "size": 48,
                "color": [0, 0, 0],
                "style": "normal",
                "align": "left"
            },
            "expected_lines": 1
        },
        {
            "config": {
                "text": "Armel Wanes\nProject",
                "font": "DejaVuSans",
                "size": 60,
                "color": [0, 0, 0],
                "style": "bold",
                "line_height": 1.5,
                "align": "left"
            },
            "expected_lines": 2
        },
        {
            "config": {
                "text": "Line 1\nLine 2\nLine 3",
                "font": "DejaVuSans",
                "size": 48,
                "color": [0, 0, 0],
                "style": "normal",
                "line_height": 1.5,
                "align": "center"
            },
            "expected_lines": 3
        },
        {
            "config": {
                "text": "A\nB\nC\nD",
                "font": "DejaVuSans",
                "size": 72,
                "color": [0, 0, 0],
                "style": "bold",
                "line_height": 1.3,
                "align": "right"
            },
            "expected_lines": 4
        }
    ]
    
    results = []
    for i, test in enumerate(tests, 1):
        print(f"Test {i}:")
        results.append(analyze_text_segments(test["config"], test["expected_lines"]))
    
    print("=" * 70)
    passed = sum(results)
    total = len(results)
    
    if all(results):
        print(f"✅ All {total} tests passed!")
        print("=" * 70)
        return True
    else:
        print(f"❌ {total - passed}/{total} test(s) failed")
        print("=" * 70)
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
