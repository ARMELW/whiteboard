# Audio Support - Quick Start Guide

Get started with audio in your whiteboard animations in 5 minutes!

## Prerequisites

Install pydub (one-time setup):
```bash
pip install pydub
```

Verify installation:
```bash
python test_audio.py
```

## 1. Simple Background Music (30 seconds)

Add background music to any video:

```bash
python whiteboard_animator.py demo/1.jpg \
    --background-music audio/music.mp3 \
    --music-volume 0.5
```

**Parameters:**
- `--background-music`: Path to your music file (MP3, WAV, OGG)
- `--music-volume`: Volume level from 0.0 (silent) to 1.0 (full volume)

**Tips:**
- Use 0.3-0.5 for background music so it doesn't overpower
- Music loops automatically if shorter than video

## 2. Auto-Generated Sounds (1 minute)

Enable typewriter and drawing sounds:

```bash
python whiteboard_animator.py demo/1.jpg \
    --enable-drawing-sound
```

**Available Flags:**
- `--enable-typewriter-sound`: Adds typing sounds for text animations
- `--enable-drawing-sound`: Adds sketching sounds for drawing animations

**When to use:**
- Typewriter: For text-heavy animations or typing effects
- Drawing: For sketch/diagram animations to enhance realism

## 3. Music with Fading (2 minutes)

Professional fade-in and fade-out effects:

```bash
python whiteboard_animator.py demo/1.jpg \
    --background-music audio/music.mp3 \
    --music-volume 0.4 \
    --music-fade-in 2.0 \
    --music-fade-out 3.0
```

**Parameters:**
- `--music-fade-in`: Fade-in duration in seconds
- `--music-fade-out`: Fade-out duration in seconds

**Best Practices:**
- Fade-in: 1-2 seconds for smooth start
- Fade-out: 2-4 seconds for graceful ending

## 4. Full Audio Configuration (5 minutes)

For complete control, use a JSON configuration file.

### Step 1: Create `audio_config.json`

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
        "volume": 0.8
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

### Step 2: Run with Configuration

```bash
python whiteboard_animator.py demo/1.jpg \
    --audio-config audio_config.json
```

## Common Use Cases

### Tutorial Video with Voice-Over

```json
{
  "audio": {
    "background_music": {
      "path": "audio/soft_music.mp3",
      "volume": 0.3
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

### Marketing Video with Sound Effects

```json
{
  "audio": {
    "background_music": {
      "path": "audio/upbeat.mp3",
      "volume": 0.5
    },
    "sound_effects": [
      {
        "path": "audio/pop.wav",
        "start_time": 1.0,
        "volume": 0.7
      },
      {
        "path": "audio/ding.wav",
        "start_time": 3.0,
        "volume": 0.8
      },
      {
        "path": "audio/whoosh.wav",
        "start_time": 5.0,
        "volume": 0.6
      }
    ]
  }
}
```

### Educational Content with Typewriter

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
            "text": "Welcome to our educational animation!",
            "font": "Arial",
            "size": 48
          },
          "mode": "typing",
          "position": {"x": 50, "y": 100}
        }
      ]
    }
  ]
}
```

## Volume Guidelines

| Audio Type | Recommended Volume | Purpose |
|------------|-------------------|---------|
| Background Music | 0.3 - 0.5 | Don't overpower narration |
| Voice-Over | 0.9 - 1.0 | Clear and prominent |
| Sound Effects | 0.5 - 0.8 | Noticeable but not jarring |
| Typewriter | 0.2 - 0.4 | Subtle background effect |
| Drawing | 0.15 - 0.25 | Very subtle |

## Tips for Best Results

### 1. Audio File Preparation
- Use high-quality audio files (192 kbps or higher)
- Normalize audio levels before importing
- Keep music files under 10 MB for faster processing

### 2. Timing
- Start with the video first (no audio) to get timing right
- Note the video duration for accurate audio timing
- Add 0.5-1 second buffer before/after for natural feel

### 3. Testing
- Test with a short video first
- Check audio levels on different devices
- Verify synchronization is accurate

### 4. File Organization
```
project/
├── video/
│   └── slides.json
├── audio/
│   ├── music/
│   │   └── background.mp3
│   ├── effects/
│   │   ├── whoosh.wav
│   │   └── pop.wav
│   └── voice/
│       └── narration.mp3
└── audio_config.json
```

## Troubleshooting

### "pydub not installed" Error
```bash
pip install pydub
```

### "FFmpeg not found" Error
- **Ubuntu/Debian:** `sudo apt-get install ffmpeg`
- **macOS:** `brew install ffmpeg`
- **Windows:** Download from https://ffmpeg.org/

### Audio Not Playing
1. Check file paths are correct
2. Verify audio file format is supported (MP3, WAV, OGG)
3. Test with absolute paths

### Audio Out of Sync
1. Check video duration matches expected timing
2. Verify `start_time` values in configuration
3. Test with shorter videos first

## Next Steps

- **Full Documentation:** [AUDIO_GUIDE.md](AUDIO_GUIDE.md)
- **Example Config:** [example_audio_config.json](example_audio_config.json)
- **Test Script:** `python test_audio.py`
- **Implementation Details:** [AUDIO_IMPLEMENTATION_SUMMARY.md](AUDIO_IMPLEMENTATION_SUMMARY.md)

## Examples to Try

### Example 1: Simple Video
```bash
python whiteboard_animator.py demo/1.jpg \
    --background-music audio/music.mp3 \
    --music-volume 0.5
```

### Example 2: With Auto Sounds
```bash
python whiteboard_animator.py demo/1.jpg \
    --background-music audio/music.mp3 \
    --enable-drawing-sound
```

### Example 3: Full Configuration
```bash
python whiteboard_animator.py \
    --config example_config.json \
    --audio-config example_audio_config.json
```

## Resources

### Free Audio Sources
- **Music:** [YouTube Audio Library](https://studio.youtube.com/channel/UC/music)
- **Sound Effects:** [Freesound.org](https://freesound.org/)
- **Voice:** Record with [Audacity](https://www.audacityteam.org/) (free)

### Audio Editing Tools
- **Audacity** (free) - For editing and mixing
- **GarageBand** (macOS, free) - For music creation
- **Adobe Audition** (paid) - Professional audio editing

---

**You're ready to create professional videos with audio!** 🎵

For more advanced features, see the complete [AUDIO_GUIDE.md](AUDIO_GUIDE.md).
