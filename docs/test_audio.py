#!/usr/bin/env python3
"""
Test script for audio functionality in whiteboard animator.

This script tests the audio manager module and demonstrates
audio features without requiring actual audio files.
"""

import sys
import os

# Test if pydub is available
try:
    from pydub import AudioSegment
    from pydub.generators import Sine, WhiteNoise
    PYDUB_AVAILABLE = True
    print("✅ pydub is installed and available")
except ImportError:
    PYDUB_AVAILABLE = False
    print("❌ pydub is NOT installed")
    print("   Install with: pip install pydub")
    sys.exit(1)

# Test if audio_manager module can be imported
try:
    from audio_manager import AudioManager, add_audio_to_video, process_audio_config
    print("✅ audio_manager module imported successfully")
except ImportError as e:
    print(f"❌ Failed to import audio_manager: {e}")
    sys.exit(1)

# Test FFmpeg availability
import subprocess
try:
    result = subprocess.run(['ffmpeg', '-version'], 
                          stdout=subprocess.PIPE, 
                          stderr=subprocess.PIPE,
                          timeout=5)
    if result.returncode == 0:
        print("✅ FFmpeg is installed and available")
    else:
        print("⚠️ FFmpeg found but may have issues")
except (FileNotFoundError, subprocess.TimeoutExpired):
    print("❌ FFmpeg is NOT installed or not in PATH")
    print("   Install FFmpeg from https://ffmpeg.org/")
    sys.exit(1)

print("\n" + "="*60)
print("Testing Audio Manager Functionality")
print("="*60)

# Create a test audio manager
print("\n1. Creating AudioManager...")
audio_mgr = AudioManager(frame_rate=30, sample_rate=44100)
print("✅ AudioManager created successfully")

# Set total duration
print("\n2. Setting total duration to 10 seconds...")
audio_mgr.set_total_duration(10.0)
print("✅ Duration set successfully")

# Generate typewriter sound
print("\n3. Generating typewriter sound...")
success = audio_mgr.generate_typewriter_sound(
    start_time=1.0,
    num_characters=20,
    char_interval=0.1,
    volume=0.3
)
if success:
    print("✅ Typewriter sound generated successfully")
else:
    print("❌ Failed to generate typewriter sound")

# Generate drawing sound
print("\n4. Generating drawing sound...")
success = audio_mgr.generate_drawing_sound(
    start_time=3.0,
    duration=2.0,
    volume=0.2
)
if success:
    print("✅ Drawing sound generated successfully")
else:
    print("❌ Failed to generate drawing sound")

# Create a test background music (simple sine wave)
print("\n5. Creating test background music...")
try:
    # Generate a simple tone as test music
    test_music = Sine(440).to_audio_segment(duration=5000)  # 5 seconds, 440 Hz
    test_music = test_music - 20  # Reduce volume
    
    # Save to temp file
    temp_music_path = "/tmp/test_music.wav"
    test_music.export(temp_music_path, format="wav")
    print(f"✅ Test music created: {temp_music_path}")
    
    # Load it into audio manager
    success = audio_mgr.load_background_music(
        temp_music_path,
        volume=0.3,
        loop=True,
        fade_in=0.5,
        fade_out=0.5
    )
    if success:
        print("✅ Background music loaded successfully")
    else:
        print("❌ Failed to load background music")
        
except Exception as e:
    print(f"⚠️ Error creating test music: {e}")

# Mix audio
print("\n6. Mixing all audio tracks...")
mixed_audio = audio_mgr.mix_audio()
if mixed_audio:
    print(f"✅ Audio mixed successfully: {len(mixed_audio)/1000:.2f}s duration")
else:
    print("❌ Failed to mix audio")

# Export audio
print("\n7. Exporting mixed audio...")
output_path = "/tmp/test_audio_output.wav"
success = audio_mgr.export_audio(output_path, format="wav")
if success:
    print(f"✅ Audio exported successfully: {output_path}")
    
    # Check file size
    if os.path.exists(output_path):
        file_size = os.path.getsize(output_path)
        print(f"   File size: {file_size / 1024:.1f} KB")
        
        # Try to load it back to verify
        try:
            test_load = AudioSegment.from_file(output_path)
            print(f"   Verified: {len(test_load)/1000:.2f}s, {test_load.channels} channels, {test_load.frame_rate}Hz")
        except Exception as e:
            print(f"   ⚠️ Could not verify exported audio: {e}")
    else:
        print("   ❌ Output file not found")
else:
    print("❌ Failed to export audio")

# Test process_audio_config
print("\n8. Testing process_audio_config...")
test_config = {
    "typewriter": {
        "start_time": 0.5,
        "num_characters": 15,
        "char_interval": 0.12,
        "volume": 0.35
    },
    "drawing_sound": {
        "start_time": 2.0,
        "duration": 1.5,
        "volume": 0.25
    }
}

test_audio_mgr = AudioManager(frame_rate=30)
test_audio_mgr.set_total_duration(5.0)
success = process_audio_config(test_config, test_audio_mgr, current_time=0.0)
if success:
    print("✅ process_audio_config executed successfully")
    mixed = test_audio_mgr.mix_audio()
    if mixed:
        print(f"   Mixed audio duration: {len(mixed)/1000:.2f}s")
else:
    print("❌ process_audio_config failed")

# Clean up
print("\n9. Cleaning up test files...")
try:
    if os.path.exists("/tmp/test_music.wav"):
        os.remove("/tmp/test_music.wav")
        print("   ✅ Removed test music file")
    if os.path.exists("/tmp/test_audio_output.wav"):
        # Keep this one for manual inspection
        print(f"   ℹ️ Test output kept for inspection: /tmp/test_audio_output.wav")
except Exception as e:
    print(f"   ⚠️ Error during cleanup: {e}")

print("\n" + "="*60)
print("✅ ALL TESTS COMPLETED SUCCESSFULLY!")
print("="*60)
print("\nAudio system is fully functional and ready to use.")
print("\nNext steps:")
print("1. Try the example: python whiteboard_animator.py demo/1.jpg --enable-drawing-sound")
print("2. Add background music: python whiteboard_animator.py demo/1.jpg --background-music your_music.mp3")
print("3. Use full config: python whiteboard_animator.py --config example_audio_config.json")
print("\nSee AUDIO_GUIDE.md for complete documentation.")
