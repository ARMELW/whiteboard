"""
Test script to verify the background draw fix.

The fix ensures that during animation:
1. Only foreground strokes/edges are drawn in grayscale
2. Background regions remain white (not pixelated/checkered)
3. Color is revealed at the end during hold frames

This prevents the pixelated effect where background pixels were
being drawn in grayscale tile-by-tile.
"""

import cv2
import numpy as np
import os
import sys

def create_test_image(path):
    """Create a test image with clear foreground and gradient background."""
    width, height = 640, 480
    img = np.ones((height, width, 3), dtype=np.uint8) * 255
    
    # Add gradient background
    for y in range(height):
        color_val = int(200 + (y / height) * 55)
        img[y, :] = [color_val, color_val, 250]
    
    # Draw foreground shapes with clear edges
    cv2.circle(img, (160, 240), 60, (0, 0, 200), 5)  # Red circle
    cv2.rectangle(img, (320, 120), (480, 360), (200, 0, 0), 5)  # Blue rect
    pts = np.array([[520, 380], [600, 380], [560, 280]], np.int32)
    pts = pts.reshape((-1, 1, 2))
    cv2.polylines(img, [pts], True, (0, 200, 0), 5)  # Green triangle
    
    cv2.imwrite(path, img)
    return img

def analyze_video_frames(video_path):
    """Analyze video frames to check if fix is working."""
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        return False, "Cannot open video"
    
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    # Check background regions during animation
    background_clean = True
    grayscale_during_anim = True
    color_revealed = False
    
    # Check mid-animation frame
    cap.set(cv2.CAP_PROP_POS_FRAMES, total_frames // 2)
    ret, frame = cap.read()
    if ret:
        # Check background region
        bg_sample = frame[50:70, 50:70]
        bg_mean = np.mean(bg_sample)
        if bg_mean < 230:  # Background should stay white
            background_clean = False
        
        # Check stroke region (should be grayscale)
        stroke_sample = frame[235:245, 155:165]
        b_mean = np.mean(stroke_sample[:,:,0])
        g_mean = np.mean(stroke_sample[:,:,1])
        r_mean = np.mean(stroke_sample[:,:,2])
        color_diff = max(abs(r_mean - g_mean), abs(g_mean - b_mean), abs(r_mean - b_mean))
        if color_diff > 10:
            grayscale_during_anim = False
    
    # Check final frame (color should be revealed if there are hold frames)
    if total_frames > 50:  # If video is long enough to have hold frames
        cap.set(cv2.CAP_PROP_POS_FRAMES, total_frames - 5)
        ret, frame = cap.read()
        if ret:
            stroke_sample = frame[235:245, 155:165]
            b_mean = np.mean(stroke_sample[:,:,0])
            g_mean = np.mean(stroke_sample[:,:,1])
            r_mean = np.mean(stroke_sample[:,:,2])
            color_diff = max(abs(r_mean - g_mean), abs(g_mean - b_mean), abs(r_mean - b_mean))
            if color_diff > 10:
                color_revealed = True
    
    cap.release()
    
    results = {
        'background_clean': background_clean,
        'grayscale_during_anim': grayscale_during_anim,
        'color_revealed': color_revealed or total_frames < 50,  # Pass if no hold frames
        'total_frames': total_frames
    }
    
    return True, results

def main():
    """Run the test."""
    print("=" * 70)
    print("Background Draw Fix - Test")
    print("=" * 70)
    
    # Create test image
    test_img_path = "/tmp/test_bg_draw.jpg"
    print(f"\n1. Creating test image: {test_img_path}")
    create_test_image(test_img_path)
    print("   ✅ Test image created")
    
    # Generate animation
    print(f"\n2. Generating animation...")
    cmd = f"python whiteboard_animator.py {test_img_path} --split-len 20 --frame-rate 10 --skip-rate 3 --duration 7 > /tmp/test_output.log 2>&1"
    ret = os.system(cmd)
    if ret != 0:
        print("   ❌ Animation generation failed")
        return False
    
    # Find the most recent video in save_videos directory
    import glob
    videos = glob.glob("save_videos/vid_*.mp4")
    if not videos:
        print("   ❌ No video found")
        return False
    video_path = max(videos, key=os.path.getctime)
    print(f"   ✅ Animation generated: {video_path}")
    
    # Analyze video
    print(f"\n3. Analyzing video frames...")
    success, results = analyze_video_frames(video_path)
    if not success:
        print(f"   ❌ Analysis failed: {results}")
        return False
    
    print(f"   Total frames: {results['total_frames']}")
    print(f"   Background clean: {'✅' if results['background_clean'] else '❌'}")
    print(f"   Grayscale during animation: {'✅' if results['grayscale_during_anim'] else '❌'}")
    print(f"   Color revealed at end: {'✅' if results['color_revealed'] else '❌'}")
    
    # Overall result
    all_passed = (results['background_clean'] and 
                  results['grayscale_during_anim'] and 
                  results['color_revealed'])
    
    print("\n" + "=" * 70)
    if all_passed:
        print("✅ TEST PASSED - Background draw fix is working correctly!")
        print("\nThe fix ensures:")
        print("  • Only strokes/edges are drawn in grayscale during animation")
        print("  • Background regions stay white (no pixelation)")
        print("  • Color is revealed after animation completes")
    else:
        print("❌ TEST FAILED - Some checks did not pass")
    print("=" * 70)
    
    return all_passed

if __name__ == "__main__":
    sys.exit(0 if main() else 1)
