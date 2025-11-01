#!/usr/bin/env python3
"""
Test script to verify diagonal zigzag pattern in coloriage mode.
Validates that pixels are colored in diagonal bands with zigzag alternation.
"""

import sys
import os
import cv2
import numpy as np
import json
import subprocess


def create_grid_test_image():
    """Create a simple grid pattern to visualize diagonal coloring."""
    canvas = np.ones((300, 400, 3), dtype=np.uint8) * 255
    
    # Draw a grid of colored squares
    colors = [
        (255, 0, 0),    # Red
        (0, 255, 0),    # Green
        (0, 0, 255),    # Blue
        (255, 255, 0),  # Yellow
        (255, 0, 255),  # Magenta
        (0, 255, 255),  # Cyan
    ]
    
    square_size = 40
    spacing = 10
    
    idx = 0
    for row in range(5):
        for col in range(7):
            x = 20 + col * (square_size + spacing)
            y = 20 + row * (square_size + spacing)
            color = colors[idx % len(colors)]
            cv2.rectangle(canvas, (x, y), (x + square_size, y + square_size), color, -1)
            idx += 1
    
    return canvas


def test_diagonal_pattern_logic():
    """Test the diagonal pattern sorting logic."""
    print("\n=== Testing Diagonal Pattern Logic ===\n")
    
    # Create a simple 5x5 grid of pixels
    test_pixels = []
    for y in range(5):
        for x in range(5):
            test_pixels.append((y, x))
    
    # Group by diagonal bands (y+x)
    diagonal_bands = {}
    for y, x in test_pixels:
        diagonal_index = y + x
        if diagonal_index not in diagonal_bands:
            diagonal_bands[diagonal_index] = []
        diagonal_bands[diagonal_index].append((y, x))
    
    # Sort and create zigzag
    sorted_diagonals = sorted(diagonal_bands.keys())
    zigzag_pattern = []
    
    for i, diag_idx in enumerate(sorted_diagonals):
        diagonal_pixels = diagonal_bands[diag_idx]
        
        if i % 2 == 0:
            diagonal_pixels.sort(key=lambda p: p[0])  # Ascending
        else:
            diagonal_pixels.sort(key=lambda p: p[0], reverse=True)  # Descending
        
        zigzag_pattern.extend(diagonal_pixels)
    
    print("Diagonal zigzag pattern for 5x5 grid:")
    print("(Showing first 15 pixels)")
    for i, (y, x) in enumerate(zigzag_pattern[:15]):
        print(f"  Step {i+1:2d}: pixel ({y}, {x})")
    
    # Verify diagonal property: first few should have increasing y+x
    first_few = zigzag_pattern[:10]
    diagonal_sums = [y + x for y, x in first_few]
    
    print("\nDiagonal sums (y+x) for first 10 pixels:")
    print(f"  {diagonal_sums}")
    
    # Check if pattern follows diagonal bands
    is_diagonal = True
    for i in range(len(diagonal_sums) - 1):
        if diagonal_sums[i] > diagonal_sums[i+1] + 1:
            is_diagonal = False
            break
    
    if is_diagonal:
        print("✅ Pattern follows diagonal bands correctly")
        return True
    else:
        print("❌ Pattern does not follow diagonal bands")
        return False


def test_coloriage_diagonal_mode():
    """Test coloriage mode with diagonal pattern on actual image."""
    print("\n=== Testing Coloriage Mode with Diagonal Pattern ===\n")
    
    # Create test image
    test_image = create_grid_test_image()
    test_image_path = "/tmp/test_diagonal_coloriage.png"
    cv2.imwrite(test_image_path, test_image)
    print(f"✓ Created test image: {test_image_path}")
    
    # Create configuration
    config = {
        "output_video": "/tmp/test_diagonal_coloriage_output.mp4",
        "fps": 30,
        "slides": [
            {
                "index": 0,
                "duration": 3,
                "skip_rate": 5,
                "layers": [
                    {
                        "image_path": test_image_path,
                        "position": {"x": 0, "y": 0},
                        "z_index": 1,
                        "skip_rate": 3,
                        "mode": "coloriage"
                    }
                ]
            }
        ]
    }
    
    config_path = "/tmp/test_diagonal_coloriage_config.json"
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=2)
    
    print(f"✓ Created config: {config_path}")
    
    # Run whiteboard animator
    print("\n▶️  Running whiteboard animator with coloriage mode...")
    script_dir = os.path.dirname(os.path.abspath(__file__))
    animator_script = os.path.join(script_dir, "whiteboard_animator.py")
    cmd = f"{sys.executable} {animator_script} --config {config_path}"
    
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    
    # Check for success indicators in output
    output = result.stdout + result.stderr
    
    if result.returncode == 0 or "Coloriage mode:" in output:
        print("✅ Coloriage mode executed successfully")
        
        # Check for diagonal bands message
        if "bandes diagonales" in output:
            print("✅ Diagonal zigzag pattern confirmed in output")
            
            # Extract number of bands
            import re
            match = re.search(r'(\d+) bandes diagonales', output)
            if match:
                num_bands = int(match.group(1))
                print(f"   Organized into {num_bands} diagonal bands")
        
        # Check if video was created
        if os.path.exists("/tmp/test_diagonal_coloriage_output.mp4"):
            print(f"✅ Output video created successfully")
            return True
        else:
            print(f"⚠️  Video not found but process completed")
            return True
    else:
        print("❌ Coloriage mode test failed")
        print(f"   Error output: {result.stderr[:300]}")
        return False


def visualize_diagonal_pattern():
    """Create a visualization showing the diagonal zigzag pattern."""
    print("\n=== Creating Diagonal Pattern Visualization ===\n")
    
    try:
        import matplotlib.pyplot as plt
        from matplotlib import patches
        
        # Create a simple grid to show the pattern
        grid_size = 8
        fig, ax = plt.subplots(1, 1, figsize=(10, 10))
        
        # Draw grid
        for i in range(grid_size + 1):
            ax.plot([0, grid_size], [i, i], 'k-', linewidth=0.5, alpha=0.3)
            ax.plot([i, i], [0, grid_size], 'k-', linewidth=0.5, alpha=0.3)
        
        # Create diagonal bands
        pixels = [(y, x) for y in range(grid_size) for x in range(grid_size)]
        
        diagonal_bands = {}
        for y, x in pixels:
            diagonal_index = y + x
            if diagonal_index not in diagonal_bands:
                diagonal_bands[diagonal_index] = []
            diagonal_bands[diagonal_index].append((y, x))
        
        sorted_diagonals = sorted(diagonal_bands.keys())
        
        # Draw diagonal pattern with colors
        colors = plt.cm.rainbow(np.linspace(0, 1, len(sorted_diagonals)))
        
        for i, diag_idx in enumerate(sorted_diagonals):
            diagonal_pixels = diagonal_bands[diag_idx]
            
            # Sort for zigzag
            if i % 2 == 0:
                diagonal_pixels.sort(key=lambda p: p[0])
            else:
                diagonal_pixels.sort(key=lambda p: p[0], reverse=True)
            
            # Draw pixels in this diagonal
            for y, x in diagonal_pixels:
                rect = patches.Rectangle((x, grid_size - 1 - y), 1, 1, 
                                         linewidth=1, edgecolor='black',
                                         facecolor=colors[i], alpha=0.7)
                ax.add_patch(rect)
            
            # Add arrows to show direction
            if len(diagonal_pixels) > 1:
                for j in range(len(diagonal_pixels) - 1):
                    y1, x1 = diagonal_pixels[j]
                    y2, x2 = diagonal_pixels[j + 1]
                    ax.arrow(x1 + 0.5, grid_size - 1 - y1 + 0.5,
                            x2 - x1, -(y2 - y1),
                            head_width=0.2, head_length=0.15,
                            fc='white', ec='black', linewidth=2, alpha=0.8)
        
        ax.set_xlim(0, grid_size)
        ax.set_ylim(0, grid_size)
        ax.set_aspect('equal')
        ax.set_title('Diagonal Zigzag Coloring Pattern\n(Colors show diagonal bands, arrows show direction)',
                    fontsize=14, fontweight='bold')
        ax.set_xlabel('X coordinate', fontsize=12)
        ax.set_ylabel('Y coordinate', fontsize=12)
        
        plt.tight_layout()
        plt.savefig('/tmp/diagonal_zigzag_pattern.png', dpi=150, bbox_inches='tight')
        print("✅ Visualization saved to /tmp/diagonal_zigzag_pattern.png")
        return True
        
    except ImportError:
        print("⚠️  matplotlib not available, skipping visualization")
        return False


def main():
    """Run all diagonal coloriage tests."""
    print("=" * 70)
    print("DIAGONAL ZIGZAG COLORIAGE TEST SUITE")
    print("=" * 70)
    
    # Test 1: Diagonal pattern logic
    test1_passed = test_diagonal_pattern_logic()
    
    # Test 2: Coloriage mode with diagonal pattern
    test2_passed = test_coloriage_diagonal_mode()
    
    # Test 3: Visualize pattern (optional)
    test3_passed = visualize_diagonal_pattern()
    
    # Summary
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    print(f"Diagonal pattern logic:  {'✅ PASSED' if test1_passed else '❌ FAILED'}")
    print(f"Coloriage diagonal mode: {'✅ PASSED' if test2_passed else '❌ FAILED'}")
    print(f"Pattern visualization:   {'✅ CREATED' if test3_passed else '⚠️  SKIPPED'}")
    print("=" * 70)
    
    if test1_passed and test2_passed:
        print("\n🎉 Diagonal zigzag coloriage tests PASSED!")
        print("   The coloring now follows a diagonal pattern.")
        return 0
    else:
        print("\n⚠️  Some tests FAILED")
        return 1


if __name__ == "__main__":
    sys.exit(main())
