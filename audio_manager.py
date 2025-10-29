"""
Audio Manager Module for Whiteboard Animator

This module provides comprehensive audio support for whiteboard animations:
- Background music
- Sound effects synchronized with animations
- Voice-over/narration
- Typewriter sounds for text animations
- Drawing sounds
- Audio/video synchronization
- Multi-track audio mixing
- Volume control per element

Dependencies:
- pydub: For audio manipulation
- FFmpeg: For audio/video encoding (with audio support enabled)
"""

import os
import subprocess
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import json

# Try to import pydub
try:
    from pydub import AudioSegment
    from pydub.generators import WhiteNoise
    PYDUB_AVAILABLE = True
except ImportError:
    PYDUB_AVAILABLE = False
    # Create dummy type for type hints when pydub is not available
    AudioSegment = None
    print("⚠️ Warning: pydub not installed. Audio features will be disabled.")
    print("   Install with: pip install pydub")


class AudioManager:
    """
    Manages all audio aspects of whiteboard animation.
    """
    
    def __init__(self, frame_rate: int = 30, sample_rate: int = 44100):
        """
        Initialize the Audio Manager.
        
        Args:
            frame_rate: Video frame rate (frames per second)
            sample_rate: Audio sample rate (Hz)
        """
        self.frame_rate = frame_rate
        self.sample_rate = sample_rate
        self.audio_tracks: List[AudioSegment] = []
        self.background_music: Optional[AudioSegment] = None
        self.total_duration_ms: int = 0
        
        if not PYDUB_AVAILABLE:
            print("⚠️ AudioManager initialized but pydub is not available")
    
    def set_total_duration(self, duration_seconds: float):
        """
        Set the total duration of the video.
        
        Args:
            duration_seconds: Total video duration in seconds
        """
        self.total_duration_ms = int(duration_seconds * 1000)
    
    def load_background_music(
        self, 
        music_path: str, 
        volume: float = 1.0,
        loop: bool = True,
        fade_in: float = 0,
        fade_out: float = 0
    ) -> bool:
        """
        Load background music for the video.
        
        Args:
            music_path: Path to the music file (mp3, wav, ogg, etc.)
            volume: Volume multiplier (0.0 to 1.0, default 1.0)
            loop: Whether to loop the music if shorter than video
            fade_in: Fade in duration in seconds (default 0)
            fade_out: Fade out duration in seconds (default 0)
            
        Returns:
            True if successful, False otherwise
        """
        if not PYDUB_AVAILABLE:
            print("⚠️ Cannot load background music: pydub not available")
            return False
        
        try:
            if not os.path.exists(music_path):
                print(f"⚠️ Music file not found: {music_path}")
                return False
            
            # Load audio file
            music = AudioSegment.from_file(music_path)
            
            # Apply volume
            if volume != 1.0:
                # Convert to dB change (volume 0.5 = -6dB, volume 2.0 = +6dB)
                db_change = 20 * (volume - 1)
                music = music + db_change
            
            # Loop if necessary
            if loop and self.total_duration_ms > 0:
                if len(music) < self.total_duration_ms:
                    loops_needed = (self.total_duration_ms // len(music)) + 1
                    music = music * loops_needed
                music = music[:self.total_duration_ms]
            
            # Apply fade effects
            if fade_in > 0:
                fade_in_ms = int(fade_in * 1000)
                music = music.fade_in(fade_in_ms)
            
            if fade_out > 0:
                fade_out_ms = int(fade_out * 1000)
                music = music.fade_out(fade_out_ms)
            
            self.background_music = music
            print(f"✅ Background music loaded: {music_path}")
            print(f"   Duration: {len(music)/1000:.2f}s, Channels: {music.channels}, Sample rate: {music.frame_rate}Hz")
            return True
            
        except Exception as e:
            print(f"❌ Error loading background music: {e}")
            return False
    
    def add_sound_effect(
        self,
        sound_path: str,
        start_time: float,
        volume: float = 1.0,
        duration: Optional[float] = None
    ) -> bool:
        """
        Add a sound effect at a specific time.
        
        Args:
            sound_path: Path to the sound file
            start_time: When to play the sound (seconds from video start)
            volume: Volume multiplier (0.0 to 1.0)
            duration: Optional duration to trim/extend the sound
            
        Returns:
            True if successful, False otherwise
        """
        if not PYDUB_AVAILABLE:
            return False
        
        try:
            if not os.path.exists(sound_path):
                print(f"⚠️ Sound effect file not found: {sound_path}")
                return False
            
            # Load sound effect
            sound = AudioSegment.from_file(sound_path)
            
            # Apply volume
            if volume != 1.0:
                db_change = 20 * (volume - 1)
                sound = sound + db_change
            
            # Trim/extend if duration specified
            if duration is not None:
                duration_ms = int(duration * 1000)
                if len(sound) > duration_ms:
                    sound = sound[:duration_ms]
                elif len(sound) < duration_ms:
                    # Extend with silence
                    silence = AudioSegment.silent(duration=duration_ms - len(sound))
                    sound = sound + silence
            
            # Store with timing information
            start_time_ms = int(start_time * 1000)
            self.audio_tracks.append({
                'audio': sound,
                'start': start_time_ms,
                'type': 'effect'
            })
            
            print(f"✅ Sound effect added: {os.path.basename(sound_path)} at {start_time:.2f}s")
            return True
            
        except Exception as e:
            print(f"❌ Error adding sound effect: {e}")
            return False
    
    def add_voice_over(
        self,
        voice_path: str,
        start_time: float,
        volume: float = 1.0
    ) -> bool:
        """
        Add voice-over/narration at a specific time.
        
        Args:
            voice_path: Path to the voice file
            start_time: When to play the voice (seconds from video start)
            volume: Volume multiplier (0.0 to 1.0)
            
        Returns:
            True if successful, False otherwise
        """
        if not PYDUB_AVAILABLE:
            return False
        
        try:
            if not os.path.exists(voice_path):
                print(f"⚠️ Voice-over file not found: {voice_path}")
                return False
            
            # Load voice file
            voice = AudioSegment.from_file(voice_path)
            
            # Apply volume
            if volume != 1.0:
                db_change = 20 * (volume - 1)
                voice = voice + db_change
            
            # Store with timing information
            start_time_ms = int(start_time * 1000)
            self.audio_tracks.append({
                'audio': voice,
                'start': start_time_ms,
                'type': 'voiceover'
            })
            
            print(f"✅ Voice-over added: {os.path.basename(voice_path)} at {start_time:.2f}s")
            return True
            
        except Exception as e:
            print(f"❌ Error adding voice-over: {e}")
            return False
    
    def generate_typewriter_sound(
        self,
        start_time: float,
        num_characters: int,
        char_interval: float = 0.1,
        volume: float = 0.3
    ) -> bool:
        """
        Generate typewriter sound effects for text animations.
        
        Args:
            start_time: When to start the typewriter sound
            num_characters: Number of characters being typed
            char_interval: Time between each keystroke (seconds)
            volume: Volume multiplier (0.0 to 1.0)
            
        Returns:
            True if successful, False otherwise
        """
        if not PYDUB_AVAILABLE:
            return False
        
        try:
            # Generate simple click sound for each character
            # In a real implementation, you could load actual typewriter samples
            click_duration = 50  # ms
            
            typewriter_audio = AudioSegment.silent(duration=0)
            
            for i in range(num_characters):
                # Add silence before click
                silence = AudioSegment.silent(duration=int(char_interval * 1000))
                # Generate a simple click (short white noise burst)
                click = WhiteNoise().to_audio_segment(duration=click_duration)
                # Apply volume and envelope to make it sound like a click
                click = click - 20  # Reduce volume
                click = click.fade_in(5).fade_out(20)
                
                typewriter_audio += silence + click
            
            # Apply overall volume
            if volume != 1.0:
                db_change = 20 * (volume - 1)
                typewriter_audio = typewriter_audio + db_change
            
            # Store with timing information
            start_time_ms = int(start_time * 1000)
            self.audio_tracks.append({
                'audio': typewriter_audio,
                'start': start_time_ms,
                'type': 'typewriter'
            })
            
            print(f"✅ Typewriter sound generated: {num_characters} chars at {start_time:.2f}s")
            return True
            
        except Exception as e:
            print(f"❌ Error generating typewriter sound: {e}")
            return False
    
    def generate_drawing_sound(
        self,
        start_time: float,
        duration: float,
        volume: float = 0.2
    ) -> bool:
        """
        Generate drawing/sketching sound effects for animations.
        
        Args:
            start_time: When to start the drawing sound
            duration: How long the drawing lasts (seconds)
            volume: Volume multiplier (0.0 to 1.0)
            
        Returns:
            True if successful, False otherwise
        """
        if not PYDUB_AVAILABLE:
            return False
        
        try:
            # Generate a subtle scratching/drawing sound
            # In a real implementation, you could load actual drawing samples
            duration_ms = int(duration * 1000)
            
            # Create a continuous low-level noise to simulate drawing
            drawing_audio = WhiteNoise().to_audio_segment(duration=duration_ms)
            # Apply filtering and volume to make it subtle
            drawing_audio = drawing_audio - 25  # Reduce volume significantly
            
            # Apply overall volume
            if volume != 1.0:
                db_change = 20 * (volume - 1)
                drawing_audio = drawing_audio + db_change
            
            # Add fade in and out for smoothness
            drawing_audio = drawing_audio.fade_in(100).fade_out(200)
            
            # Store with timing information
            start_time_ms = int(start_time * 1000)
            self.audio_tracks.append({
                'audio': drawing_audio,
                'start': start_time_ms,
                'type': 'drawing'
            })
            
            print(f"✅ Drawing sound generated: {duration:.2f}s at {start_time:.2f}s")
            return True
            
        except Exception as e:
            print(f"❌ Error generating drawing sound: {e}")
            return False
    
    def mix_audio(self) -> Optional[AudioSegment]:
        """
        Mix all audio tracks together.
        
        Returns:
            Mixed audio as AudioSegment, or None if no audio or pydub unavailable
        """
        if not PYDUB_AVAILABLE:
            return None
        
        if not self.background_music and not self.audio_tracks:
            print("ℹ️ No audio to mix")
            return None
        
        try:
            # Start with silence or background music
            if self.background_music:
                mixed = self.background_music
            elif self.total_duration_ms > 0:
                mixed = AudioSegment.silent(duration=self.total_duration_ms)
            else:
                # Calculate duration from all tracks
                max_end_time = max(
                    track['start'] + len(track['audio']) 
                    for track in self.audio_tracks
                )
                mixed = AudioSegment.silent(duration=max_end_time)
            
            # Overlay all sound effects and voice-overs
            for track in self.audio_tracks:
                mixed = mixed.overlay(track['audio'], position=track['start'])
            
            print(f"✅ Audio mixed: {len(mixed)/1000:.2f}s total")
            return mixed
            
        except Exception as e:
            print(f"❌ Error mixing audio: {e}")
            return None
    
    def export_audio(self, output_path: str, format: str = "wav") -> bool:
        """
        Export the mixed audio to a file.
        
        Args:
            output_path: Where to save the audio file
            format: Audio format (wav, mp3, ogg, etc.)
            
        Returns:
            True if successful, False otherwise
        """
        if not PYDUB_AVAILABLE:
            return False
        
        try:
            mixed_audio = self.mix_audio()
            if mixed_audio is None:
                print("⚠️ No audio to export")
                return False
            
            # Ensure output directory exists
            os.makedirs(os.path.dirname(output_path) or '.', exist_ok=True)
            
            # Export audio
            mixed_audio.export(output_path, format=format)
            
            print(f"✅ Audio exported: {output_path}")
            return True
            
        except Exception as e:
            print(f"❌ Error exporting audio: {e}")
            return False
    
    def get_audio_for_video(self) -> Optional[AudioSegment]:
        """
        Get the final mixed audio ready for video encoding.
        
        Returns:
            Mixed audio as AudioSegment, or None if no audio
        """
        return self.mix_audio()


def add_audio_to_video(
    video_path: str,
    audio_path: str,
    output_path: str,
    audio_codec: str = "aac",
    audio_bitrate: str = "192k"
) -> bool:
    """
    Combine video with audio using FFmpeg.
    
    Args:
        video_path: Path to the video file (without audio)
        audio_path: Path to the audio file
        output_path: Where to save the final video
        audio_codec: Audio codec to use (aac, mp3, etc.)
        audio_bitrate: Audio bitrate (e.g., "192k")
        
    Returns:
        True if successful, False otherwise
    """
    try:
        if not os.path.exists(video_path):
            print(f"⚠️ Video file not found: {video_path}")
            return False
        
        if not os.path.exists(audio_path):
            print(f"⚠️ Audio file not found: {audio_path}")
            return False
        
        # Build FFmpeg command
        cmd = [
            'ffmpeg',
            '-y',  # Overwrite output file
            '-i', video_path,
            '-i', audio_path,
            '-c:v', 'copy',  # Copy video stream
            '-c:a', audio_codec,
            '-b:a', audio_bitrate,
            '-shortest',  # Match shortest stream duration
            output_path
        ]
        
        # Run FFmpeg
        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        if result.returncode == 0:
            print(f"✅ Video with audio created: {output_path}")
            return True
        else:
            print(f"❌ FFmpeg error: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error adding audio to video: {e}")
        return False


def process_audio_config(
    audio_config: Dict,
    audio_manager: AudioManager,
    current_time: float = 0.0
) -> bool:
    """
    Process audio configuration and add to audio manager.
    
    Args:
        audio_config: Audio configuration dictionary
        audio_manager: AudioManager instance to add audio to
        current_time: Current time in video (seconds) for relative timing
        
    Returns:
        True if successful, False otherwise
    """
    if not audio_config:
        return True
    
    success = True
    
    # Process background music
    if 'background_music' in audio_config:
        music_cfg = audio_config['background_music']
        if isinstance(music_cfg, str):
            # Simple string path
            success &= audio_manager.load_background_music(music_cfg)
        elif isinstance(music_cfg, dict):
            # Detailed configuration
            path = music_cfg.get('path', '')
            volume = music_cfg.get('volume', 1.0)
            loop = music_cfg.get('loop', True)
            fade_in = music_cfg.get('fade_in', 0)
            fade_out = music_cfg.get('fade_out', 0)
            success &= audio_manager.load_background_music(
                path, volume, loop, fade_in, fade_out
            )
    
    # Process sound effects
    if 'sound_effects' in audio_config:
        for effect in audio_config['sound_effects']:
            path = effect.get('path', '')
            start = effect.get('start_time', current_time)
            volume = effect.get('volume', 1.0)
            duration = effect.get('duration', None)
            success &= audio_manager.add_sound_effect(path, start, volume, duration)
    
    # Process voice-overs
    if 'voice_overs' in audio_config:
        for voice in audio_config['voice_overs']:
            path = voice.get('path', '')
            start = voice.get('start_time', current_time)
            volume = voice.get('volume', 1.0)
            success &= audio_manager.add_voice_over(path, start, volume)
    
    # Process typewriter sounds
    if 'typewriter' in audio_config:
        tw_cfg = audio_config['typewriter']
        start = tw_cfg.get('start_time', current_time)
        num_chars = tw_cfg.get('num_characters', 10)
        interval = tw_cfg.get('char_interval', 0.1)
        volume = tw_cfg.get('volume', 0.3)
        success &= audio_manager.generate_typewriter_sound(
            start, num_chars, interval, volume
        )
    
    # Process drawing sounds
    if 'drawing_sound' in audio_config:
        draw_cfg = audio_config['drawing_sound']
        start = draw_cfg.get('start_time', current_time)
        duration = draw_cfg.get('duration', 1.0)
        volume = draw_cfg.get('volume', 0.2)
        success &= audio_manager.generate_drawing_sound(start, duration, volume)
    
    return success


# Example configuration format
EXAMPLE_AUDIO_CONFIG = {
    "audio": {
        "background_music": {
            "path": "audio/background.mp3",
            "volume": 0.5,
            "loop": True,
            "fade_in": 1.0,
            "fade_out": 2.0
        },
        "sound_effects": [
            {
                "path": "audio/whoosh.wav",
                "start_time": 2.5,
                "volume": 0.8,
                "duration": 0.5
            }
        ],
        "voice_overs": [
            {
                "path": "audio/narration.mp3",
                "start_time": 0.0,
                "volume": 1.0
            }
        ]
    },
    "slides": [
        {
            "index": 0,
            "audio": {
                "typewriter": {
                    "start_time": 1.0,
                    "num_characters": 20,
                    "char_interval": 0.1,
                    "volume": 0.3
                },
                "drawing_sound": {
                    "start_time": 0.0,
                    "duration": 3.0,
                    "volume": 0.2
                }
            }
        }
    ]
}
