# Font Configuration System

## Overview

The font configuration system allows you to map font names to `.ttf` font files without having to specify `font_path` in every configuration. This makes it much easier to use custom fonts across multiple slides and projects.

## Problem Solved

**Before**: You had to manually specify the font path in every text configuration:

```json
{
  "text_config": {
    "text": "Your text here",
    "font": "Pacifico",
    "font_path": "../fonts/Pacifico/Pacifico-Regular.ttf",
    "size": 55
  }
}
```

**After**: Just specify the font name - the path is resolved automatically:

```json
{
  "text_config": {
    "text": "Your text here",
    "font": "Pacifico",
    "size": 55
  }
}
```

## How It Works

1. **Font Configuration File**: Create or edit `fonts.json` in the root directory
2. **Font Mapping**: Map font names to `.ttf` file paths
3. **Automatic Resolution**: The system automatically finds and uses the correct font file
4. **Fallback Support**: If a font is not in the config, the system falls back to system fonts via fontconfig

## Font Configuration File Format

Create a `fonts.json` file in the repository root:

```json
{
  "fonts": {
    "Pacifico": {
      "normal": "fonts/Pacifico/Pacifico-Regular.ttf"
    },
    "Roboto": {
      "normal": "fonts/Roboto/Roboto-Regular.ttf",
      "bold": "fonts/Roboto/Roboto-Bold.ttf",
      "italic": "fonts/Roboto/Roboto-Italic.ttf",
      "bold italic": "fonts/Roboto/Roboto-BoldItalic.ttf"
    },
    "CustomFont": {
      "normal": "fonts/CustomFont/CustomFont.ttf"
    }
  }
}
```

### Configuration Structure

- **fonts**: Root object containing all font definitions
- **Font Name**: The name you'll use in your configurations (e.g., "Pacifico")
- **Styles**: Object mapping style names to font file paths
  - `"normal"`: Regular font style
  - `"bold"`: Bold font style
  - `"italic"`: Italic font style
  - `"bold italic"`: Bold and italic combined

### Path Resolution

Font paths can be:
- **Relative**: Relative to the repository root (e.g., `"fonts/MyFont/MyFont.ttf"`)
- **Absolute**: Full system path (e.g., `"/usr/share/fonts/truetype/MyFont.ttf"`)

## Adding New Fonts

To add a new font:

1. **Place the font file** in the `fonts` directory:
   ```
   fonts/
   ├── Pacifico/
   │   └── Pacifico-Regular.ttf
   └── MyNewFont/
       ├── MyNewFont-Regular.ttf
       ├── MyNewFont-Bold.ttf
       └── MyNewFont-Italic.ttf
   ```

2. **Add the mapping** to `fonts.json`:
   ```json
   {
     "fonts": {
       "Pacifico": {
         "normal": "fonts/Pacifico/Pacifico-Regular.ttf"
       },
       "MyNewFont": {
         "normal": "fonts/MyNewFont/MyNewFont-Regular.ttf",
         "bold": "fonts/MyNewFont/MyNewFont-Bold.ttf",
         "italic": "fonts/MyNewFont/MyNewFont-Italic.ttf"
       }
     }
   }
   ```

3. **Use the font** in your configurations:
   ```json
   {
     "text_config": {
       "text": "Text with my new font!",
       "font": "MyNewFont",
       "style": "bold",
       "size": 48
     }
   }
   ```

## Example Usage

### Basic Example

```json
{
  "slides": [
    {
      "index": 0,
      "duration": 2,
      "layers": [
        {
          "type": "text",
          "text_config": {
            "text": "Hello World!",
            "font": "Pacifico",
            "size": 72,
            "color": [0, 0, 0]
          }
        }
      ]
    }
  ]
}
```

### Multiple Fonts and Styles

```json
{
  "slides": [
    {
      "index": 0,
      "duration": 3,
      "layers": [
        {
          "type": "text",
          "text_config": {
            "text": "Title",
            "font": "Pacifico",
            "size": 80
          }
        },
        {
          "type": "text",
          "text_config": {
            "text": "Body text",
            "font": "Roboto",
            "style": "normal",
            "size": 40
          }
        },
        {
          "type": "text",
          "text_config": {
            "text": "Bold text",
            "font": "Roboto",
            "style": "bold",
            "size": 40
          }
        }
      ]
    }
  ]
}
```

## Font Resolution Order

The system resolves fonts in the following order:

1. **fonts.json configuration**: Checks if the font is defined in `fonts.json`
2. **Fontconfig (fc-match)**: Falls back to system fontconfig if available
3. **System font paths**: Tries common system font locations
4. **PIL default font**: Uses PIL's default font as last resort

This ensures maximum compatibility and graceful fallback behavior.

## Testing

Run the font configuration test to verify your setup:

```bash
python3 test_font_config.py
```

This will:
- ✅ Load and validate `fonts.json`
- ✅ Test font resolution for configured fonts
- ✅ Test font resolution for system fonts (fallback)
- ✅ Render sample text images
- ✅ Verify the complete configuration works

## Benefits

1. **🎯 Centralized Configuration**: All font mappings in one place
2. **📝 Cleaner Configs**: No need to repeat font paths in every configuration
3. **🔄 Easy Updates**: Change font files without updating all configs
4. **➕ Simple Addition**: Add new fonts by editing one file
5. **🔙 Backward Compatible**: System fonts still work via fontconfig fallback
6. **🌐 Cross-platform**: Works on Linux, macOS, and Windows

## Troubleshooting

### Font not found

If a font cannot be resolved:
1. Check that the font file exists at the specified path
2. Verify the path is correct in `fonts.json`
3. Ensure the file has read permissions
4. Check the console output for warning messages

### Font renders with fallback

If your configured font is not being used:
1. Verify the font name matches exactly (case-sensitive)
2. Check that the `.ttf` file is valid
3. Run `test_font_config.py` to diagnose the issue
4. Check console output for font resolution details

### Multiple font styles

If you need multiple styles (bold, italic):
1. Obtain all style variants of the font
2. Add each style to the font's configuration
3. Specify the `"style"` parameter in your text config

## Example: Complete Setup

1. **Directory structure**:
   ```
   whiteboard/
   ├── fonts.json
   ├── fonts/
   │   ├── Pacifico/
   │   │   └── Pacifico-Regular.ttf
   │   └── Roboto/
   │       ├── Roboto-Regular.ttf
   │       ├── Roboto-Bold.ttf
   │       └── Roboto-Italic.ttf
   └── examples/
       └── my_config.json
   ```

2. **fonts.json**:
   ```json
   {
     "fonts": {
       "Pacifico": {
         "normal": "fonts/Pacifico/Pacifico-Regular.ttf"
       },
       "Roboto": {
         "normal": "fonts/Roboto/Roboto-Regular.ttf",
         "bold": "fonts/Roboto/Roboto-Bold.ttf",
         "italic": "fonts/Roboto/Roboto-Italic.ttf"
       }
     }
   }
   ```

3. **my_config.json**:
   ```json
   {
     "slides": [
       {
         "index": 0,
         "duration": 2,
         "layers": [
           {
             "type": "text",
             "text_config": {
               "text": "Beautiful Title",
               "font": "Pacifico",
               "size": 72
             }
           },
           {
             "type": "text",
             "text_config": {
               "text": "Regular body text",
               "font": "Roboto",
               "style": "normal",
               "size": 40
             }
           }
         ]
       }
     ]
   }
   ```

4. **Generate video**:
   ```bash
   python3 whiteboard_animator.py --config examples/my_config.json
   ```

That's it! No need to specify `font_path` anywhere in your configuration.

## Migration Guide

### Existing Configurations

Existing configurations with `font_path` will continue to work. The `font_path` parameter is still supported for backward compatibility and special cases.

### Migrating to Font Config

To migrate existing configurations:

1. **Extract font paths** from your configurations
2. **Add them to fonts.json** with appropriate font names
3. **Remove font_path** from your configurations
4. **Keep only font name** in your configs

Example migration:

**Before**:
```json
{
  "text_config": {
    "text": "Hello",
    "font": "Pacifico",
    "font_path": "../fonts/Pacifico/Pacifico-Regular.ttf"
  }
}
```

**After** (add to fonts.json):
```json
{
  "fonts": {
    "Pacifico": {
      "normal": "fonts/Pacifico/Pacifico-Regular.ttf"
    }
  }
}
```

**After** (update your config):
```json
{
  "text_config": {
    "text": "Hello",
    "font": "Pacifico"
  }
}
```

## See Also

- [test_font_config.py](test_font_config.py) - Font configuration system tests
- [examples/font_config_demo.json](examples/font_config_demo.json) - Example configuration
- [fonts.json](fonts.json) - Font configuration file
