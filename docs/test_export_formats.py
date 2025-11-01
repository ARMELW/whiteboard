#!/usr/bin/env python3
"""
Test script for export formats functionality.
Tests GIF, WebM, PNG sequence, and social media presets.
"""

import sys
import os
import cv2
import numpy as np

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from export_formats import (
    export_gif, export_webm, export_png_sequence,
    export_with_transparency, export_lossless,
    get_social_media_preset, list_social_media_presets,
    print_social_media_presets
)

def create_test_frames(num_frames=30, width=640, height=480):
    """Create test frames with a moving circle."""
    frames = []
    
    for i in range(num_frames):
        # Create white background
        frame = np.ones((height, width, 3), dtype=np.uint8) * 255
        
        # Draw a moving circle
        center_x = int((i / num_frames) * width)
        center_y = height // 2
        radius = 30
        color = (255, 0, 0)  # Blue in BGR
        
        cv2.circle(frame, (center_x, center_y), radius, color, -1)
        
        # Add text
        text = f"Frame {i+1}/{num_frames}"
        cv2.putText(frame, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 
                   1, (0, 0, 0), 2, cv2.LINE_AA)
        
        frames.append(frame)
    
    return frames

def test_gif_export():
    """Test GIF export functionality."""
    print("\n" + "="*60)
    print("TEST 1: GIF Export")
    print("="*60)
    
    frames = create_test_frames(30)
    output_path = "/tmp/test_export.gif"
    
    result = export_gif(frames, output_path, fps=10)
    
    if result and os.path.exists(output_path):
        size_mb = os.path.getsize(output_path) / (1024 * 1024)
        print(f"✅ GIF export successful")
        print(f"   File: {output_path}")
        print(f"   Size: {size_mb:.2f} MB")
        return True
    else:
        print(f"❌ GIF export failed")
        return False

def test_webm_export():
    """Test WebM export functionality."""
    print("\n" + "="*60)
    print("TEST 2: WebM Export")
    print("="*60)
    
    frames = create_test_frames(30)
    output_path = "/tmp/test_export.webm"
    
    result = export_webm(frames, output_path, fps=30, quality=10)
    
    if result and os.path.exists(output_path):
        size_mb = os.path.getsize(output_path) / (1024 * 1024)
        print(f"✅ WebM export successful")
        print(f"   File: {output_path}")
        print(f"   Size: {size_mb:.2f} MB")
        return True
    else:
        print(f"❌ WebM export failed")
        return False

def test_png_sequence_export():
    """Test PNG sequence export functionality."""
    print("\n" + "="*60)
    print("TEST 3: PNG Sequence Export")
    print("="*60)
    
    frames = create_test_frames(10)  # Fewer frames for PNG
    output_dir = "/tmp/test_export_frames"
    
    result = export_png_sequence(frames, output_dir)
    
    if result and os.path.exists(output_dir):
        num_files = len([f for f in os.listdir(output_dir) if f.endswith('.png')])
        print(f"✅ PNG sequence export successful")
        print(f"   Directory: {output_dir}")
        print(f"   Files: {num_files} PNG images")
        return True
    else:
        print(f"❌ PNG sequence export failed")
        return False

def test_transparency_export():
    """Test transparency export functionality."""
    print("\n" + "="*60)
    print("TEST 4: WebM with Transparency Export")
    print("="*60)
    
    frames = create_test_frames(30)
    output_path = "/tmp/test_export_alpha.webm"
    
    result = export_with_transparency(frames, output_path, fps=30)
    
    if result and os.path.exists(output_path):
        size_mb = os.path.getsize(output_path) / (1024 * 1024)
        print(f"✅ Transparency export successful")
        print(f"   File: {output_path}")
        print(f"   Size: {size_mb:.2f} MB")
        return True
    else:
        print(f"❌ Transparency export failed")
        return False

def test_lossless_export():
    """Test lossless export functionality."""
    print("\n" + "="*60)
    print("TEST 5: Lossless Export")
    print("="*60)
    
    frames = create_test_frames(30)
    output_path = "/tmp/test_export_lossless.mkv"
    
    result = export_lossless(frames, output_path, fps=30)
    
    if result and os.path.exists(output_path):
        size_mb = os.path.getsize(output_path) / (1024 * 1024)
        print(f"✅ Lossless export successful")
        print(f"   File: {output_path}")
        print(f"   Size: {size_mb:.2f} MB")
        return True
    else:
        print(f"❌ Lossless export failed")
        return False

def test_social_presets():
    """Test social media presets."""
    print("\n" + "="*60)
    print("TEST 6: Social Media Presets")
    print("="*60)
    
    presets = list_social_media_presets()
    print(f"✅ Found {len(presets)} social media presets")
    
    # Test getting a specific preset
    youtube_preset = get_social_media_preset('youtube')
    if youtube_preset:
        print(f"✅ YouTube preset loaded successfully")
        print(f"   Resolution: {youtube_preset['resolution']}")
        print(f"   FPS: {youtube_preset['fps']}")
        print(f"   Format: {youtube_preset['format']}")
        
        # Test TikTok preset
        tiktok_preset = get_social_media_preset('tiktok')
        if tiktok_preset:
            print(f"✅ TikTok preset loaded successfully")
            print(f"   Resolution: {tiktok_preset['resolution']}")
            print(f"   Aspect ratio: {tiktok_preset['aspect_ratio']}")
            return True
        else:
            print(f"❌ TikTok preset not found")
            return False
    else:
        print(f"❌ YouTube preset not found")
        return False

def main():
    """Run all tests."""
    print("\n" + "="*60)
    print("EXPORT FORMATS TEST SUITE")
    print("="*60)
    
    results = []
    
    # Run tests
    results.append(("GIF Export", test_gif_export()))
    results.append(("WebM Export", test_webm_export()))
    results.append(("PNG Sequence", test_png_sequence_export()))
    results.append(("Transparency", test_transparency_export()))
    results.append(("Lossless", test_lossless_export()))
    results.append(("Social Presets", test_social_presets()))
    
    # Print summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{test_name:20s} {status}")
    
    print("="*60)
    print(f"Total: {passed}/{total} tests passed")
    print("="*60 + "\n")
    
    # Print presets list
    print("\n📱 Social Media Presets Available:")
    print_social_media_presets()
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
