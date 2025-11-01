# Advanced Text Animation and Multilingual Support

## Overview

This document describes the advanced text animation features and multilingual support implemented in the whiteboard animator.

## New Features Implemented

### 1. Text Animation Modes

#### Character-by-Character Animation
Reveals text one character at a time with precise timing control.

**Configuration:**
```json
{
  "type": "text",
  "text_config": {
    "text": "Hello World!",
    "animation_type": "character_by_character",
    "char_duration_frames": 5,
    "pause_after_char": 2,
    "pause_after_word": 10
  }
}
```

**Parameters:**
- `animation_type`: Set to `"character_by_character"`
- `char_duration_frames`: Number of frames to display each character (default: skip_rate)
- `pause_after_char`: Frames to pause after each character (default: 0)
- `pause_after_word`: Frames to pause after each word (default: 0)

#### Word-by-Word Animation
Reveals text one word at a time, ideal for typing effects.

**Configuration:**
```json
{
  "type": "text",
  "text_config": {
    "text": "Word by word animation",
    "animation_type": "word_by_word",
    "word_duration_frames": 8,
    "pause_after_word": 5
  }
}
```

**Parameters:**
- `animation_type`: Set to `"word_by_word"`
- `word_duration_frames`: Number of frames to display each word (default: skip_rate)
- `pause_after_word`: Frames to pause after each word (default: 0)

### 2. Text Effects

#### Shadow Effect
Adds a shadow behind the text for depth and readability.

**Configuration:**
```json
{
  "text_config": {
    "text": "Shadow Text",
    "text_effects": {
      "shadow": {
        "offset": [3, 3],
        "color": "#888888"
      }
    }
  }
}
```

**Parameters:**
- `offset`: [x, y] pixel offset for shadow (default: [2, 2])
- `color`: Shadow color as hex string or RGB tuple

#### Outline Effect
Adds an outline/stroke around text characters.

**Configuration:**
```json
{
  "text_config": {
    "text": "Outlined Text",
    "text_effects": {
      "outline": {
        "width": 2,
        "color": "#000000"
      }
    }
  }
}
```

**Parameters:**
- `width`: Outline width in pixels (default: 1)
- `color`: Outline color as hex string or RGB tuple

#### Combined Effects
You can combine multiple effects:

```json
{
  "text_config": {
    "text": "Amazing Text!",
    "text_effects": {
      "shadow": {
        "offset": [4, 4],
        "color": "#000000"
      },
      "outline": {
        "width": 1,
        "color": "#FFFFFF"
      }
    }
  }
}
```

### 3. Multilingual Support

#### Right-to-Left (RTL) Text
Support for Arabic, Hebrew, and other RTL languages.

**Configuration:**
```json
{
  "text_config": {
    "text": "مرحبا بالعالم",
    "direction": "rtl",
    "align": "right"
  }
}
```

**Parameters:**
- `direction`: `"ltr"`, `"rtl"`, or `"auto"` (default: "auto")
  - `"ltr"`: Left-to-right (English, etc.)
  - `"rtl"`: Right-to-left (Arabic, Hebrew)
  - `"auto"`: Auto-detect based on text content

**Requirements:**
- Requires `arabic-reshaper` and `python-bidi` packages for full RTL support
- Install with: `pip install arabic-reshaper python-bidi`

#### Bidirectional Text
Supports mixed LTR and RTL text in the same line.

**Example:**
```json
{
  "text_config": {
    "text": "Hello مرحبا World",
    "direction": "auto"
  }
}
```

#### Vertical Text
Support for vertical text (Asian languages).

**Configuration:**
```json
{
  "text_config": {
    "text": "縦書き",
    "vertical": true
  }
}
```

**Parameters:**
- `vertical`: Set to `true` for vertical text layout (default: false)

#### Font Fallback Chain
Automatically tries multiple fonts for complex scripts.

**Configuration:**
```json
{
  "text_config": {
    "text": "Hello 你好 مرحبا",
    "font": "DejaVuSans",
    "font_fallbacks": ["NotoSans", "NotoSansArabic", "NotoSansCJK"]
  }
}
```

**Parameters:**
- `font_fallbacks`: List of fallback font names to try if primary font doesn't support all characters

**Default Fallbacks:**
The system automatically tries these fonts if not specified:
- DejaVuSans
- Arial
- NotoSans (general)
- NotoSansArabic (Arabic)
- NotoSansHebrew (Hebrew)
- NotoSansCJK (Chinese/Japanese/Korean)

### 4. Typewriter Sound Sync Points

The animation timing parameters can be used to sync with sound effects:

```json
{
  "text_config": {
    "animation_type": "character_by_character",
    "char_duration_frames": 3,
    "pause_after_char": 1
  }
}
```

Calculate timing for audio sync:
- Frame time = 1 / frame_rate (e.g., 1/30 = 0.033s per frame)
- Time per character = char_duration_frames * frame_time
- Total animation time = number_of_chars * (char_duration_frames + pause_after_char) * frame_time

## Complete Examples

### Example 1: Educational Content with Character-by-Character

```json
{
  "slides": [{
    "index": 0,
    "duration": 10,
    "layers": [{
      "type": "text",
      "skip_rate": 8,
      "text_config": {
        "text": "Learn Something New Today!",
        "font": "DejaVuSans",
        "size": 56,
        "color": "#0066CC",
        "style": "bold",
        "align": "center",
        "animation_type": "character_by_character",
        "char_duration_frames": 4,
        "pause_after_word": 8,
        "text_effects": {
          "shadow": {
            "offset": [3, 3],
            "color": "#888888"
          }
        }
      }
    }]
  }]
}
```

### Example 2: Multilingual Presentation

```json
{
  "slides": [{
    "index": 0,
    "duration": 15,
    "layers": [
      {
        "type": "text",
        "text_config": {
          "text": "Welcome",
          "animation_type": "word_by_word",
          "position": {"x": 100, "y": 100}
        }
      },
      {
        "type": "text",
        "text_config": {
          "text": "مرحبا",
          "direction": "rtl",
          "animation_type": "word_by_word",
          "position": {"x": 100, "y": 200}
        }
      },
      {
        "type": "text",
        "text_config": {
          "text": "欢迎",
          "animation_type": "word_by_word",
          "position": {"x": 100, "y": 300}
        }
      }
    ]
  }]
}
```

### Example 3: Text with All Effects

```json
{
  "slides": [{
    "index": 0,
    "duration": 8,
    "layers": [{
      "type": "text",
      "skip_rate": 10,
      "text_config": {
        "text": "SPECTACULAR!",
        "font": "DejaVuSans",
        "size": 80,
        "color": "#FF0066",
        "style": "bold",
        "align": "center",
        "animation_type": "character_by_character",
        "char_duration_frames": 5,
        "text_effects": {
          "shadow": {
            "offset": [5, 5],
            "color": "#000000"
          },
          "outline": {
            "width": 2,
            "color": "#FFFFFF"
          }
        }
      }
    }]
  }]
}
```

## Performance Considerations

### Animation Speed
- **character_by_character**: Slower, more dramatic
  - Recommended `skip_rate`: 5-8
  - Recommended `char_duration_frames`: 3-5
  
- **word_by_word**: Medium speed
  - Recommended `skip_rate`: 8-12
  - Recommended `word_duration_frames`: 5-10
  
- **handwriting**: Fastest, most natural
  - Recommended `skip_rate`: 8-15

### Text Effects Impact
- Shadow: Minimal performance impact
- Outline: Slight performance impact (draws text multiple times)
- Combined effects: Moderate impact

### RTL Text
- Requires `arabic-reshaper` and `python-bidi` packages
- Slight processing overhead for text reshaping
- Falls back gracefully if packages not installed

## Troubleshooting

### RTL Text Not Displaying Correctly
1. Install required packages:
   ```bash
   pip install arabic-reshaper python-bidi
   ```
2. Ensure `direction` is set to `"rtl"` or `"auto"`
3. Use appropriate fonts that support RTL scripts

### Font Not Found
1. Use `font_fallbacks` to specify alternative fonts
2. Check available system fonts: `/usr/share/fonts/` (Linux) or `C:\Windows\Fonts\` (Windows)
3. Use common fonts like DejaVuSans for better compatibility

### Animation Too Slow/Fast
- Adjust `skip_rate` (higher = faster)
- Adjust `char_duration_frames` or `word_duration_frames`
- Reduce `pause_after_char` or `pause_after_word`

### Effects Not Visible
- Increase effect parameters (shadow offset, outline width)
- Ensure colors contrast with text color
- Check that text size is large enough for effects to be visible

## API Reference

### Text Config Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `text` | string | "" | Text content to display |
| `font` | string | "Arial" | Font family name |
| `size` | int | 32 | Font size in pixels |
| `color` | string/tuple | (0,0,0) | Text color |
| `style` | string | "normal" | Font style: normal, bold, italic, bold_italic |
| `align` | string | "left" | Text alignment: left, center, right |
| `direction` | string | "auto" | Text direction: ltr, rtl, auto |
| `vertical` | boolean | false | Enable vertical text layout |
| `line_height` | float | 1.2 | Line height multiplier |
| `animation_type` | string | "handwriting" | Animation mode |
| `char_duration_frames` | int | skip_rate | Frames per character |
| `word_duration_frames` | int | skip_rate | Frames per word |
| `pause_after_char` | int | 0 | Pause frames after character |
| `pause_after_word` | int | 0 | Pause frames after word |
| `text_effects` | object | {} | Text effects configuration |
| `font_fallbacks` | array | [] | Fallback font list |

### Animation Types

- `"handwriting"` - Default column-based handwriting (fastest)
- `"character_by_character"` - Character-by-character reveal
- `"word_by_word"` - Word-by-word typing
- `"svg_path"` - SVG path-based drawing (opt-in)

## See Also

- [TEXT_LAYERS_GUIDE.md](TEXT_LAYERS_GUIDE.md) - Basic text layers guide
- [IMPLEMENTATION_TEXT_HANDWRITING.md](IMPLEMENTATION_TEXT_HANDWRITING.md) - Technical implementation details
- [examples/advanced_text_animations.json](examples/advanced_text_animations.json) - Example configuration
- [examples/multilingual_text.json](examples/multilingual_text.json) - Multilingual examples
- [examples/text_effects.json](examples/text_effects.json) - Text effects examples
