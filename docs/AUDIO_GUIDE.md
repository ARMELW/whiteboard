# Audio Support Guide

## Overview

The whiteboard animator now supports comprehensive audio features including:
- Background music with looping and fading
- Sound effects synchronized with animations
- Voice-over/narration
- Typewriter sounds for text animations
- Drawing sounds for sketch animations
- Multi-track audio mixing
- Volume control for each audio element

## Installation

To use audio features, you need to install the `pydub` library:

```bash
pip install pydub
```

**Note:** FFmpeg must be installed on your system with audio codec support. Most systems have this by default.

## Quick Start

### Simple Background Music

Add background music to your video with a single command:

```bash
python whiteboard_animator.py image.jpg \
    --background-music audio/music.mp3 \
    --music-volume 0.5
```

### Enable Auto-Generated Sounds

Enable typewriter and drawing sounds:

```bash
python whiteboard_animator.py image.jpg \
    --enable-typewriter-sound \
    --enable-drawing-sound
```

### Using Audio Configuration File

For more advanced audio control, use a JSON configuration file:

```bash
python whiteboard_animator.py --config config.json --audio-config audio_config.json
```

## Command Line Options

### Audio CLI Arguments

| Argument | Type | Default | Description |
|----------|------|---------|-------------|
| `--audio-config` | string | None | Path to JSON audio configuration file |
| `--background-music` | string | None | Path to background music file (mp3, wav, ogg, etc.) |
| `--music-volume` | float | 0.5 | Background music volume (0.0 to 1.0) |
| `--music-fade-in` | float | 0.0 | Music fade-in duration in seconds |
| `--music-fade-out` | float | 0.0 | Music fade-out duration in seconds |
| `--enable-typewriter-sound` | flag | False | Enable typewriter sounds for text animations |
| `--enable-drawing-sound` | flag | False | Enable drawing sounds for sketch animations |
| `--audio-output` | string | None | Export mixed audio separately (wav, mp3, etc.) |

## Audio Configuration Format

### Global Audio Configuration

Add an `"audio"` section to your configuration JSON:

```json
{
  "audio": {
    "background_music": {
      "path": "audio/background.mp3",
      "volume": 0.5,
      "loop": true,
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
  }
}
```

### Per-Slide Audio Configuration

Add audio specific to each slide:

```json
{
  "slides": [
    {
      "index": 0,
      "duration": 5,
      "audio": {
        "drawing_sound": {
          "start_time": 0.0,
          "duration": 3.0,
          "volume": 0.2
        },
        "sound_effects": [
          {
            "path": "audio/pop.wav",
            "start_time": 4.0,
            "volume": 0.7
          }
        ]
      }
    }
  ]
}
```

## Audio Configuration Parameters

### Background Music

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `path` | string | Yes | - | Path to music file |
| `volume` | float | No | 1.0 | Volume multiplier (0.0 to 1.0) |
| `loop` | boolean | No | true | Loop if shorter than video |
| `fade_in` | float | No | 0 | Fade-in duration in seconds |
| `fade_out` | float | No | 0 | Fade-out duration in seconds |

### Sound Effects

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `path` | string | Yes | - | Path to sound file |
| `start_time` | float | Yes | - | When to play (seconds from video start) |
| `volume` | float | No | 1.0 | Volume multiplier (0.0 to 1.0) |
| `duration` | float | No | Auto | Duration to play (trim/extend) |

### Voice-Overs

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `path` | string | Yes | - | Path to voice file |
| `start_time` | float | Yes | - | When to play (seconds from video start) |
| `volume` | float | No | 1.0 | Volume multiplier (0.0 to 1.0) |

### Typewriter Sounds

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `start_time` | float | Yes | - | When to start typing sound |
| `num_characters` | int | Yes | - | Number of characters being typed |
| `char_interval` | float | No | 0.1 | Time between keystrokes (seconds) |
| `volume` | float | No | 0.3 | Volume multiplier (0.0 to 1.0) |

### Drawing Sounds

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `start_time` | float | Yes | - | When to start drawing sound |
| `duration` | float | Yes | - | How long the drawing lasts |
| `volume` | float | No | 0.2 | Volume multiplier (0.0 to 1.0) |

## Complete Examples

### Example 1: Simple Video with Background Music

```bash
python whiteboard_animator.py demo/1.jpg \
    --background-music audio/upbeat.mp3 \
    --music-volume 0.4 \
    --music-fade-in 2.0 \
    --music-fade-out 3.0
```

### Example 2: Tutorial Video with Voice-Over

Create `audio_config.json`:
```json
{
  "audio": {
    "background_music": {
      "path": "audio/soft_background.mp3",
      "volume": 0.3,
      "loop": true
    },
    "voice_overs": [
      {
        "path": "audio/intro.mp3",
        "start_time": 0.0,
        "volume": 1.0
      },
      {
        "path": "audio/step1.mp3",
        "start_time": 5.0,
        "volume": 1.0
      },
      {
        "path": "audio/conclusion.mp3",
        "start_time": 15.0,
        "volume": 1.0
      }
    ]
  }
}
```

Run:
```bash
python whiteboard_animator.py --config slides.json --audio-config audio_config.json
```

### Example 3: Animated Text with Typewriter Sound

Create `config.json`:
```json
{
  "slides": [
    {
      "index": 0,
      "duration": 8,
      "audio": {
        "typewriter": {
          "start_time": 0.5,
          "num_characters": 45,
          "char_interval": 0.08,
          "volume": 0.35
        }
      },
      "layers": [
        {
          "text": {
            "text": "Welcome to our animated whiteboard tutorial!",
            "font": "Arial",
            "size": 48,
            "color": [0, 0, 0]
          },
          "position": {"x": 50, "y": 100},
          "z_index": 1,
          "mode": "typing"
        }
      ]
    }
  ]
}
```

Run:
```bash
python whiteboard_animator.py --config config.json
```

### Example 4: Drawing Animation with Sound Effects

Create `config.json`:
```json
{
  "audio": {
    "background_music": {
      "path": "audio/ambient.mp3",
      "volume": 0.4
    },
    "sound_effects": [
      {
        "path": "audio/pencil_start.wav",
        "start_time": 0.0,
        "volume": 0.6
      },
      {
        "path": "audio/done.wav",
        "start_time": 8.0,
        "volume": 0.8
      }
    ]
  },
  "slides": [
    {
      "index": 0,
      "duration": 10,
      "audio": {
        "drawing_sound": {
          "start_time": 0.5,
          "duration": 7.5,
          "volume": 0.25
        }
      },
      "layers": [
        {
          "image_path": "demo/diagram.jpg",
          "position": {"x": 0, "y": 0},
          "z_index": 1,
          "skip_rate": 8,
          "mode": "draw"
        }
      ]
    }
  ]
}
```

Run:
```bash
python whiteboard_animator.py --config config.json
```

### Example 5: Complex Multi-Slide with All Audio Features

See `example_audio_config.json` for a complete example with:
- Background music with fading
- Multiple sound effects
- Voice-over narration
- Per-slide typewriter sounds
- Per-slide drawing sounds

## Audio File Formats

Supported audio formats (via pydub and FFmpeg):
- **MP3** - Compressed, good for music
- **WAV** - Uncompressed, best quality
- **OGG** - Compressed, good quality
- **M4A/AAC** - Compressed, good for voice
- **FLAC** - Lossless compression

## Tips and Best Practices

### Volume Levels

- **Background Music**: 0.3 - 0.5 (so it doesn't overpower voice/effects)
- **Voice-Over**: 0.9 - 1.0 (clear and prominent)
- **Sound Effects**: 0.5 - 0.8 (noticeable but not jarring)
- **Typewriter Sounds**: 0.2 - 0.4 (subtle background effect)
- **Drawing Sounds**: 0.15 - 0.25 (very subtle)

### Timing

1. **Start with the video first**: Generate without audio to get timing right
2. **Use video duration**: Check the final video duration to sync audio
3. **Add buffer time**: Give 0.5-1 second before/after for natural feel
4. **Test increments**: Start with clear timing, adjust as needed

### Audio Quality

1. **Use high-quality source files**: 192 kbps or higher for music
2. **Match sample rates**: 44100 Hz is standard for video
3. **Normalize audio levels**: Pre-process audio files for consistent volume
4. **Avoid clipping**: Keep combined audio under 0 dB to prevent distortion

### Performance

1. **Audio processing is fast**: Typically adds only 1-3 seconds to render
2. **Large files**: Keep music files under 10 MB for faster processing
3. **Multiple effects**: You can add dozens of sound effects without issues

## Troubleshooting

### "pydub not installed" Warning

Install pydub:
```bash
pip install pydub
```

### "FFmpeg error" Messages

Ensure FFmpeg is installed with audio support:
```bash
# Ubuntu/Debian
sudo apt-get install ffmpeg

# macOS
brew install ffmpeg

# Windows
# Download from https://ffmpeg.org/download.html
```

### Audio Not Playing in Video

1. Check that audio files exist at specified paths
2. Verify audio file formats are supported
3. Check FFmpeg installation: `ffmpeg -version`
4. Try with absolute paths for audio files

### Audio Out of Sync

1. Verify video duration matches expected timing
2. Check `start_time` values in configuration
3. Use exported animation JSON to see exact frame timings
4. Test with shorter videos first

### Volume Too Low/High

1. Adjust `volume` parameters (0.0 to 1.0)
2. Pre-process audio files with audio editing software
3. Use fade-in/fade-out for smoother transitions
4. Check combined audio doesn't clip (distort)

## Advanced Usage

### Export Audio Separately

Export just the mixed audio without video:

```bash
python whiteboard_animator.py --config config.json \
    --audio-config audio.json \
    --audio-output final_audio.wav
```

### Using with Timeline System

Combine with advanced timeline features:

```json
{
  "timeline": {
    "enabled": true,
    "slides": [
      {
        "start": 0,
        "duration": 5,
        "audio": {
          "typewriter": {
            "start_time": 0.5,
            "num_characters": 30,
            "char_interval": 0.1
          }
        }
      }
    ]
  }
}
```

### Custom Audio Effects

For custom audio processing, you can:
1. Pre-process audio files with tools like Audacity
2. Create custom sound effects with synthesis tools
3. Use audio editing software for advanced mixing
4. Export mixed audio and re-process with video

## API Usage

For programmatic usage, see the `audio_manager.py` module:

```python
from audio_manager import AudioManager

# Create audio manager
audio_mgr = AudioManager(frame_rate=30)

# Add background music
audio_mgr.load_background_music("music.mp3", volume=0.5)

# Add sound effect
audio_mgr.add_sound_effect("whoosh.wav", start_time=2.5, volume=0.8)

# Generate typewriter sound
audio_mgr.generate_typewriter_sound(
    start_time=5.0, 
    num_characters=50, 
    char_interval=0.1
)

# Mix and export
audio_mgr.set_total_duration(10.0)
audio_mgr.export_audio("output.wav")
```

## See Also

- [Configuration Format Guide](CONFIG_FORMAT.md)
- [Timeline Guide](TIMELINE_GUIDE.md)
- [Text Animation Guide](QUICKSTART_TEXT_ANIMATIONS.md)
- [Example Configurations](examples/)

## Support

For issues or questions about audio features:
1. Check this documentation
2. Review example configurations
3. Test with simple audio files first
4. Check FFmpeg and pydub installation
