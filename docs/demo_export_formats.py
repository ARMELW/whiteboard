#!/usr/bin/env python3
"""
Demo script for export formats functionality.
Shows examples of using different export formats and social media presets.
"""

import os
import sys

def print_section(title):
    """Print a formatted section header."""
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70 + "\n")

def main():
    print_section("📦 EXPORT FORMATS DEMO")
    
    # Check if image exists
    if not os.path.exists("1.jpg"):
        print("❌ Test image '1.jpg' not found.")
        print("   Please run this script from the whiteboard-it directory.")
        return 1
    
    print("This demo shows various export format options.\n")
    print("Examples use fast settings for demonstration (--split-len 30 --skip-rate 50 --duration 1)")
    print("For production, use higher quality settings.\n")
    
    # Example 1: GIF export
    print_section("Example 1: Animated GIF Export")
    print("Export video as animated GIF for web use:")
    print("\n  python whiteboard_animator.py 1.jpg --export-formats gif \\")
    print("    --split-len 30 --skip-rate 50 --duration 1\n")
    print("Outputs:")
    print("  - vid_YYYYMMDD_HHMMSS_h264.mp4  (main video)")
    print("  - vid_YYYYMMDD_HHMMSS_h264.gif  (animated GIF)\n")
    
    # Example 2: WebM export
    print_section("Example 2: WebM Export for Modern Web")
    print("Export as WebM with VP9 codec:")
    print("\n  python whiteboard_animator.py 1.jpg --export-formats webm \\")
    print("    --split-len 30 --skip-rate 50 --duration 1\n")
    print("Outputs:")
    print("  - vid_YYYYMMDD_HHMMSS_h264.mp4   (main video)")
    print("  - vid_YYYYMMDD_HHMMSS_h264.webm  (WebM version)\n")
    
    # Example 3: Multiple formats
    print_section("Example 3: Multiple Format Export")
    print("Export to multiple formats at once:")
    print("\n  python whiteboard_animator.py 1.jpg --export-formats gif webm png \\")
    print("    --split-len 30 --skip-rate 50 --duration 1\n")
    print("Outputs:")
    print("  - vid_YYYYMMDD_HHMMSS_h264.mp4         (main video)")
    print("  - vid_YYYYMMDD_HHMMSS_h264.gif         (animated GIF)")
    print("  - vid_YYYYMMDD_HHMMSS_h264.webm        (WebM version)")
    print("  - vid_YYYYMMDD_HHMMSS_h264_frames/     (PNG sequence)\n")
    
    # Example 4: Transparency
    print_section("Example 4: Export with Transparency")
    print("Export WebM with alpha channel for overlays:")
    print("\n  python whiteboard_animator.py 1.jpg --export-formats webm-alpha \\")
    print("    --split-len 30 --skip-rate 50 --duration 1\n")
    print("Outputs:")
    print("  - vid_YYYYMMDD_HHMMSS_h264.mp4        (main video)")
    print("  - vid_YYYYMMDD_HHMMSS_h264_alpha.webm (with transparency)\n")
    
    # Example 5: Lossless
    print_section("Example 5: Lossless Export for Archiving")
    print("Export in lossless quality (FFV1 codec):")
    print("\n  python whiteboard_animator.py 1.jpg --export-formats lossless \\")
    print("    --split-len 30 --skip-rate 50 --duration 1\n")
    print("Outputs:")
    print("  - vid_YYYYMMDD_HHMMSS_h264.mp4           (main video)")
    print("  - vid_YYYYMMDD_HHMMSS_h264_lossless.mkv (lossless quality)\n")
    
    # Example 6: Social media presets
    print_section("Example 6: Social Media Presets")
    print("Use optimized presets for social platforms:\n")
    
    print("Instagram Reels (vertical 9:16):")
    print("  python whiteboard_animator.py 1.jpg --social-preset instagram-reel \\")
    print("    --split-len 30 --skip-rate 50 --duration 1\n")
    
    print("YouTube (horizontal 16:9):")
    print("  python whiteboard_animator.py 1.jpg --social-preset youtube \\")
    print("    --split-len 30 --skip-rate 50 --duration 1\n")
    
    print("TikTok (vertical 9:16):")
    print("  python whiteboard_animator.py 1.jpg --social-preset tiktok \\")
    print("    --split-len 30 --skip-rate 50 --duration 1\n")
    
    print("Instagram Feed (square 1:1):")
    print("  python whiteboard_animator.py 1.jpg --social-preset instagram-feed \\")
    print("    --split-len 30 --skip-rate 50 --duration 1\n")
    
    # Example 7: Combined
    print_section("Example 7: Combined - Social Preset + Multiple Exports")
    print("Combine social preset with multiple export formats:")
    print("\n  python whiteboard_animator.py 1.jpg --social-preset tiktok \\")
    print("    --export-formats gif webm --split-len 30 --skip-rate 50 --duration 1\n")
    print("Outputs:")
    print("  - Vertical 9:16 video optimized for TikTok")
    print("  - Plus GIF and WebM versions\n")
    
    # List all presets
    print_section("Available Social Media Presets")
    print("To see all available presets with details:")
    print("\n  python whiteboard_animator.py --list-presets\n")
    print("Available presets:")
    print("  • youtube          - YouTube standard (1080p 16:9)")
    print("  • youtube-shorts   - YouTube Shorts (vertical 9:16)")
    print("  • tiktok           - TikTok (vertical 9:16)")
    print("  • instagram-feed   - Instagram feed (square 1:1)")
    print("  • instagram-story  - Instagram Story (vertical 9:16)")
    print("  • instagram-reel   - Instagram Reels (vertical 9:16)")
    print("  • facebook         - Facebook (720p 16:9)")
    print("  • twitter          - Twitter/X (720p 16:9)")
    print("  • linkedin         - LinkedIn (1080p 16:9)\n")
    
    # Tips
    print_section("💡 Tips and Best Practices")
    print("1. GIF Export:")
    print("   - Best for short animations (< 10 seconds)")
    print("   - Use lower frame rate (10 FPS) to reduce file size")
    print("   - Automatically optimized for web\n")
    
    print("2. WebM Export:")
    print("   - Better compression than MP4 for same quality")
    print("   - Use for modern web browsers")
    print("   - Supports transparency (--export-formats webm-alpha)\n")
    
    print("3. PNG Sequence:")
    print("   - Use for post-production (After Effects, Premiere)")
    print("   - Each frame is a separate PNG file")
    print("   - Highest quality but large file size\n")
    
    print("4. Social Media Presets:")
    print("   - Automatically sets resolution, aspect ratio, and FPS")
    print("   - Optimized for each platform's requirements")
    print("   - Can combine with --export-formats for multiple outputs\n")
    
    print("5. Lossless Export:")
    print("   - Use for archival or as master copy")
    print("   - Large file size but perfect quality")
    print("   - FFV1 codec in MKV container\n")
    
    # Documentation
    print_section("📚 Documentation")
    print("For complete documentation, see:")
    print("  • EXPORT_FORMATS_GUIDE.md - Complete export formats guide")
    print("  • VIDEO_QUALITY.md         - Video quality and CRF settings")
    print("  • README.md                - Main documentation")
    print("  • CONFIG_FORMAT.md         - Configuration file format\n")
    
    print_section("✨ Summary")
    print("Export formats implementation adds:")
    print("  ✅ GIF animated export")
    print("  ✅ WebM export (VP9 codec)")
    print("  ✅ PNG sequence export")
    print("  ✅ Transparency support (WebM + alpha)")
    print("  ✅ Lossless export (FFV1 codec)")
    print("  ✅ 9 social media platform presets")
    print("  ✅ Multiple simultaneous exports\n")
    
    print("All features work with existing functionality:")
    print("  • Layers")
    print("  • Transitions")
    print("  • Camera animations")
    print("  • Text and shapes")
    print("  • Watermarks")
    print("  • Quality settings\n")
    
    print("="*70)
    print("  To run any example, copy and paste the command above")
    print("="*70 + "\n")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
