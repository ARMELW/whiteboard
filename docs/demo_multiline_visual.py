#!/usr/bin/env python3
"""Visual demonstration of the multiline text typing fix."""

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from whiteboard_animator import render_text_to_image

def create_visual_demo():
    """Create a visual demonstration showing segment order."""
    print("=" * 70)
    print("Visual Demonstration: Multiline Text Typing")
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
    
    # Find segments
    height, width = thresh.shape
    columns_with_text = []
    for x in range(width):
        column = thresh[:, x]
        if np.any(column > 0):
            columns_with_text.append(x)
    
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
    
    # Assign line numbers
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
    
    # Sort segments with new logic
    sorted_segments = sorted(column_segments, key=lambda seg: (get_line_number(seg), seg[0], seg[1]))
    
    # Create visualization
    vis_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    # Draw segment order with colors
    colors = [
        (255, 0, 0),    # Red for line 1
        (0, 0, 255),    # Blue for line 2
    ]
    
    # Draw a few segments to show order
    for i in range(0, len(sorted_segments), max(1, len(sorted_segments) // 50)):
        seg = sorted_segments[i]
        x, y_start, y_end = seg
        line_num = get_line_number(seg)
        color = colors[line_num % len(colors)]
        
        # Draw a small marker
        cv2.circle(vis_img, (x, (y_start + y_end) // 2), 3, color, -1)
    
    # Save the visualization
    output_path = "/tmp/multiline_text_demo.png"
    cv2.imwrite(output_path, cv2.cvtColor(vis_img, cv2.COLOR_RGB2BGR))
    
    print("✅ Visual demonstration created!")
    print(f"   Saved to: {output_path}")
    print()
    print("Visualization shows:")
    print("  🔴 Red dots = Line 1 ('Armel Wanes') segments")
    print("  🔵 Blue dots = Line 2 ('Project') segments")
    print()
    print("The animation will draw:")
    print("  1. All red dots (line 1) from left to right")
    print("  2. Then all blue dots (line 2) from left to right")
    print()
    print("=" * 70)
    
    return True

if __name__ == "__main__":
    create_visual_demo()
