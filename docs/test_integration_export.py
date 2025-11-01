#!/usr/bin/env python3
"""
Comprehensive integration test for export formats.
Tests the export features with actual whiteboard animation generation.
"""

import os
import sys
import tempfile
import shutil

def run_test(description, command):
    """Run a test command and report results."""
    print(f"\n{'='*70}")
    print(f"TEST: {description}")
    print(f"{'='*70}")
    print(f"Command: {command}\n")
    
    result = os.system(command)
    
    if result == 0:
        print(f"\n✅ {description} - PASSED")
        return True
    else:
        print(f"\n❌ {description} - FAILED")
        return False

def main():
    print("\n" + "="*70)
    print("  COMPREHENSIVE EXPORT FORMATS INTEGRATION TEST")
    print("="*70)
    
    # Check if test image exists
    if not os.path.exists("1.jpg"):
        print("\n❌ Test image '1.jpg' not found.")
        print("   Please run this script from the whiteboard-it directory.")
        return 1
    
    # Create temporary directory for outputs
    temp_dir = tempfile.mkdtemp(prefix="export_test_")
    print(f"\n📁 Test output directory: {temp_dir}")
    
    results = []
    
    # Common parameters for fast testing
    base_cmd = "python3 whiteboard_animator.py 1.jpg --split-len 30 --skip-rate 50 --duration 1 --frame-rate 10"
    
    # Test 1: Basic GIF export
    results.append(run_test(
        "GIF Export",
        f"{base_cmd} --export-formats gif"
    ))
    
    # Test 2: WebM export
    results.append(run_test(
        "WebM Export",
        f"{base_cmd} --export-formats webm"
    ))
    
    # Test 3: Multiple formats
    results.append(run_test(
        "Multiple Formats (GIF + WebM)",
        f"{base_cmd} --export-formats gif webm"
    ))
    
    # Test 4: Social media preset (TikTok)
    results.append(run_test(
        "TikTok Preset",
        f"python3 whiteboard_animator.py 1.jpg --social-preset tiktok --split-len 30 --skip-rate 50 --duration 1"
    ))
    
    # Test 5: Social media preset + export formats
    results.append(run_test(
        "Instagram Preset + GIF Export",
        f"python3 whiteboard_animator.py 1.jpg --social-preset instagram-reel --export-formats gif --split-len 30 --skip-rate 50 --duration 1"
    ))
    
    # Test 6: PNG sequence (fewer frames for speed)
    results.append(run_test(
        "PNG Sequence Export",
        f"{base_cmd} --export-formats png"
    ))
    
    # Test 7: Transparency export
    results.append(run_test(
        "WebM with Transparency",
        f"{base_cmd} --export-formats webm-alpha"
    ))
    
    # Print summary
    print("\n" + "="*70)
    print("  TEST SUMMARY")
    print("="*70)
    
    passed = sum(results)
    total = len(results)
    
    tests = [
        "GIF Export",
        "WebM Export", 
        "Multiple Formats",
        "TikTok Preset",
        "Instagram + GIF",
        "PNG Sequence",
        "Transparency"
    ]
    
    for i, (test_name, result) in enumerate(zip(tests, results)):
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{i+1}. {test_name:25s} {status}")
    
    print("="*70)
    print(f"Total: {passed}/{total} tests passed")
    
    if passed == total:
        print("✅ ALL TESTS PASSED!")
    else:
        print(f"⚠️  {total - passed} test(s) failed")
    
    print("="*70)
    
    # Check generated files
    print("\n📁 Checking generated files in save_videos/...")
    if os.path.exists("save_videos"):
        files = os.listdir("save_videos")
        
        mp4_files = [f for f in files if f.endswith('.mp4')]
        gif_files = [f for f in files if f.endswith('.gif')]
        webm_files = [f for f in files if f.endswith('.webm')]
        frame_dirs = [f for f in files if f.endswith('_frames')]
        
        print(f"\n✅ Generated files:")
        print(f"   • MP4 videos: {len(mp4_files)}")
        print(f"   • GIF files: {len(gif_files)}")
        print(f"   • WebM files: {len(webm_files)}")
        print(f"   • Frame directories: {len(frame_dirs)}")
        
        if gif_files:
            print(f"\n   Example GIF files:")
            for gif in gif_files[:3]:
                size = os.path.getsize(os.path.join("save_videos", gif)) / (1024 * 1024)
                print(f"   • {gif} ({size:.2f} MB)")
        
        if webm_files:
            print(f"\n   Example WebM files:")
            for webm in webm_files[:3]:
                size = os.path.getsize(os.path.join("save_videos", webm)) / (1024 * 1024)
                print(f"   • {webm} ({size:.2f} MB)")
    
    print("\n" + "="*70)
    print("  INTEGRATION TEST COMPLETE")
    print("="*70 + "\n")
    
    # Cleanup
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
    
    return 0 if passed == total else 1

if __name__ == "__main__":
    sys.exit(main())
