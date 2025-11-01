# Whiteboard Video Export Guide

## Overview

This guide explains how to export scenes as **whiteboard-style videos** with progressive drawing animation and an animated drawing hand. The system provides two export modes:

1. **Static Video Export** (`export_scene_to_video`) - Composed scene with optional camera movement
2. **Whiteboard Animation Export** (`export_scene_to_whiteboard_video`) - Progressive drawing with animated hand

## Whiteboard Animation Export

### Function: `export_scene_to_whiteboard_video`

Creates videos where layers are drawn progressively with an animated hand, simulating a whiteboard/doodly-style presentation.

```python
from whiteboard_animator import export_scene_to_whiteboard_video

result = export_scene_to_whiteboard_video(
    scene_config,
    output_path='output.mp4',
    fps=30,
    camera_config=None,
    scene_width=1920,
    scene_height=1080,
    background='#FFFFFF',
    base_path=".",
    crf=18,
    draw_speed=8,
    show_hand=True,
    hand_path=None,
    final_hold_duration=2.0
)
```

### Parameters

- **scene_config** (dict): Scene configuration with layers
- **output_path** (str): Output video file path (.mp4 or .avi)
- **fps** (int): Frames per second (default: 30)
- **camera_config** (dict, optional): Camera viewport configuration
- **scene_width** (int): Scene width in pixels (default: 1920)
- **scene_height** (int): Scene height in pixels (default: 1080)
- **background** (str): Background color (default: '#FFFFFF')
- **base_path** (str): Base path for resolving file paths
- **crf** (int): Video quality, 0-51, lower = better (default: 18)
- **draw_speed** (int): Drawing speed factor (default: 8, lower = slower)
- **show_hand** (bool): Show animated drawing hand (default: True)
- **hand_path** (str, optional): Path to custom hand image
- **final_hold_duration** (float): Duration to hold final frame in seconds (default: 2.0)

### Returns

Dictionary with:
- `success` (bool): Whether export succeeded
- `output_path` (str): Path to created video
- `duration` (float): Total video duration in seconds
- `fps` (int): Frames per second
- `frames` (int): Total number of frames
- `resolution` (str): Video resolution (e.g., "1920x1080")

## Layer Configuration

### Drawing Duration

Each layer can specify how long it takes to draw using the `draw_duration` parameter:

```python
{
    'id': 'my_text',
    'type': 'text',
    'text_config': {...},
    'position': {'x': 500, 'y': 300},
    'z_index': 1,
    'draw_duration': 2.5  # Takes 2.5 seconds to draw this layer
}
```

### Z-Index Order

Layers are drawn in **z-index order** (lowest to highest). This determines the animation sequence:

```python
{
    'layers': [
        {'id': 'background', 'z_index': 0, 'draw_duration': 1.0},  # Drawn first
        {'id': 'title', 'z_index': 1, 'draw_duration': 2.0},       # Drawn second
        {'id': 'subtitle', 'z_index': 2, 'draw_duration': 1.5}     # Drawn third
    ]
}
```

## Complete Examples

### Example 1: Simple Text Animation

```python
from whiteboard_animator import export_scene_to_whiteboard_video

scene = {
    'layers': [
        {
            'id': 'title',
            'type': 'text',
            'text_config': {
                'text': 'Welcome!',
                'font': 'Arial',
                'size': 100,
                'color': (50, 100, 200),
                'style': 'bold',
                'align': 'center'
            },
            'position': {'x': 960, 'y': 540},
            'z_index': 1,
            'draw_duration': 2.0
        }
    ]
}

result = export_scene_to_whiteboard_video(
    scene,
    'welcome.mp4',
    fps=30,
    show_hand=True
)

print(f"Video created: {result['output_path']}")
print(f"Duration: {result['duration']:.1f}s")
```

### Example 2: Multi-Layer Presentation

```python
scene = {
    'layers': [
        # Background box
        {
            'id': 'bg',
            'type': 'shape',
            'shape_config': {
                'shape': 'rectangle',
                'color': (200, 200, 200),
                'fill_color': (245, 245, 250),
                'stroke_width': 3,
                'position': {'x': 960, 'y': 600},
                'width': 1700,
                'height': 600
            },
            'position': {'x': 960, 'y': 600},
            'z_index': 0,
            'draw_duration': 1.0
        },
        # Title
        {
            'id': 'title',
            'type': 'text',
            'text_config': {
                'text': 'My Presentation',
                'font': 'Arial',
                'size': 80,
                'color': (30, 50, 120),
                'style': 'bold'
            },
            'position': {'x': 960, 'y': 200},
            'z_index': 1,
            'draw_duration': 2.0
        },
        # Bullet points drawn one by one
        {
            'id': 'point1',
            'type': 'text',
            'text_config': {
                'text': '• First point',
                'font': 'Arial',
                'size': 50,
                'color': (0, 0, 0)
            },
            'position': {'x': 400, 'y': 450},
            'z_index': 2,
            'draw_duration': 1.5
        },
        {
            'id': 'point2',
            'type': 'text',
            'text_config': {
                'text': '• Second point',
                'font': 'Arial',
                'size': 50,
                'color': (0, 0, 0)
            },
            'position': {'x': 400, 'y': 600},
            'z_index': 3,
            'draw_duration': 1.5
        },
        {
            'id': 'point3',
            'type': 'text',
            'text_config': {
                'text': '• Third point',
                'font': 'Arial',
                'size': 50,
                'color': (0, 0, 0)
            },
            'position': {'x': 400, 'y': 750},
            'z_index': 4,
            'draw_duration': 1.5
        }
    ]
}

result = export_scene_to_whiteboard_video(
    scene,
    'presentation.mp4',
    fps=30,
    show_hand=True,
    final_hold_duration=3.0  # Hold final frame for 3 seconds
)
```

### Example 3: Diagram with Shapes

```python
scene = {
    'layers': [
        # Central box
        {
            'id': 'center',
            'type': 'shape',
            'shape_config': {
                'shape': 'rectangle',
                'color': (50, 100, 200),
                'fill_color': (150, 200, 255),
                'stroke_width': 4,
                'position': {'x': 960, 'y': 540},
                'width': 200,
                'height': 120
            },
            'position': {'x': 960, 'y': 540},
            'z_index': 1,
            'draw_duration': 2.0
        },
        # Top box
        {
            'id': 'top',
            'type': 'shape',
            'shape_config': {
                'shape': 'circle',
                'color': (200, 100, 50),
                'fill_color': (255, 200, 150),
                'stroke_width': 4,
                'position': {'x': 960, 'y': 200},
                'size': 80
            },
            'position': {'x': 960, 'y': 200},
            'z_index': 2,
            'draw_duration': 1.5
        },
        # Arrow connecting them
        {
            'id': 'arrow',
            'type': 'arrow',
            'arrow_config': {
                'start': [960, 280],
                'end': [960, 470],
                'color': (0, 0, 0),
                'stroke_width': 3
            },
            'position': {'x': 0, 'y': 0},
            'z_index': 3,
            'draw_duration': 1.0
        }
    ]
}

result = export_scene_to_whiteboard_video(
    scene,
    'diagram.mp4',
    fps=30
)
```

### Example 4: Using Scene Cameras

```python
scene = {
    'sceneCameras': [
        {
            'id': 'main',
            'width': 1920,
            'height': 1080,
            'position': {'x': 0.5, 'y': 0.5},
            'isDefault': True
        }
    ],
    'layers': [
        # Your layers here
    ]
}

# Camera will be automatically detected from sceneCameras
result = export_scene_to_whiteboard_video(
    scene,
    'output.mp4'
)
```

## Drawing Hand

### Using Default Hand

The system includes a default drawing hand image. Simply set `show_hand=True`:

```python
result = export_scene_to_whiteboard_video(
    scene,
    'output.mp4',
    show_hand=True  # Uses default hand image
)
```

### Using Custom Hand

Provide your own hand image with transparency (PNG with alpha channel):

```python
result = export_scene_to_whiteboard_video(
    scene,
    'output.mp4',
    show_hand=True,
    hand_path='/path/to/custom_hand.png'
)
```

### Hand Requirements

- PNG format with alpha channel (transparency)
- Recommended size: 300-500 pixels wide
- Hand should be positioned as if drawing/writing
- Transparent background

### Disabling Hand

```python
result = export_scene_to_whiteboard_video(
    scene,
    'output.mp4',
    show_hand=False  # No hand animation
)
```

## Animation Timing

### Total Duration Calculation

```
Total Duration = Sum of all layer draw_durations + final_hold_duration
```

Example:
```python
layers = [
    {'draw_duration': 2.0},  # 2 seconds
    {'draw_duration': 1.5},  # 1.5 seconds
    {'draw_duration': 2.0}   # 2 seconds
]
final_hold_duration = 2.0    # 2 seconds

# Total: 2.0 + 1.5 + 2.0 + 2.0 = 7.5 seconds
```

### Controlling Speed

**Draw Duration per Layer**:
```python
{
    'draw_duration': 3.0  # Slower drawing (3 seconds)
}
```

**Final Hold**:
```python
export_scene_to_whiteboard_video(
    scene,
    'output.mp4',
    final_hold_duration=5.0  # Hold final frame for 5 seconds
)
```

## Camera Positioning

All layers are positioned relative to the camera viewport, just like in static export:

```python
camera_config = {
    'width': 1920,
    'height': 1080,
    'position': {'x': 0.5, 'y': 0.5}  # Center of scene
}

result = export_scene_to_whiteboard_video(
    scene,
    'output.mp4',
    camera_config=camera_config
)
```

Camera position determines what part of the scene is visible:
- `{'x': 0.0, 'y': 0.0}`: Top-left corner
- `{'x': 0.5, 'y': 0.5}`: Center (default)
- `{'x': 1.0, 'y': 1.0}`: Bottom-right corner

## Video Quality

Control output quality with the `crf` parameter (Constant Rate Factor):

```python
result = export_scene_to_whiteboard_video(
    scene,
    'output.mp4',
    crf=18  # 0-51, lower = better quality, 18 is visually lossless
)
```

Quality guidelines:
- **0**: Lossless (largest file)
- **18**: Visually lossless (recommended, default)
- **23**: High quality
- **28**: Medium quality
- **35+**: Low quality
- **51**: Worst quality (smallest file)

## Supported Layer Types

### Text Layers
- Progressive text writing animation
- Support for fonts, sizes, colors, styles
- Multi-line text support

### Shape Layers
- Progressive drawing of shapes
- Circles, rectangles, triangles, polygons
- Fill and stroke colors

### Arrow Layers
- Progressive arrow drawing
- Customizable start/end points
- Arrow head styling

### Image Layers
- Progressive reveal of images
- Support for scale, rotation, opacity

### Whiteboard/Strokes Layers
- Progressive drawing of freehand strokes
- Support for stroke width and color

## Best Practices

1. **Z-Index Planning**: Plan your layer order carefully
   ```python
   # Draw background first, details last
   background: z_index=0
   main_content: z_index=1
   highlights: z_index=2
   ```

2. **Timing**: Balance drawing speed with readability
   ```python
   # Title: longer duration for emphasis
   {'draw_duration': 2.5}
   
   # Supporting text: shorter duration
   {'draw_duration': 1.5}
   ```

3. **Final Hold**: Give viewers time to absorb content
   ```python
   final_hold_duration=3.0  # 3 seconds minimum
   ```

4. **Hand Visibility**: Ensure hand doesn't obstruct important content
   - Hand is positioned near layer position
   - Moves progressively during drawing

5. **Resolution**: Use appropriate resolution for output
   ```python
   # HD
   camera_config={'width': 1920, 'height': 1080}
   
   # 4K
   camera_config={'width': 3840, 'height': 2160}
   ```

## Performance Tips

1. **Shorter Durations**: Faster rendering
   ```python
   draw_duration=1.0  # Faster than 3.0
   ```

2. **Lower FPS**: Reduces file size and rendering time
   ```python
   fps=24  # Cinematic, faster than fps=60
   ```

3. **Smaller Resolution**: Faster rendering
   ```python
   camera_config={'width': 1280, 'height': 720}  # HD 720p
   ```

4. **Fewer Layers**: Simpler scenes render faster

## Troubleshooting

### Hand Image Not Found

**Problem**: "Hand image not found" warning

**Solution**: 
- Ensure hand image exists at default path: `data/images/drawing-hand.png`
- Or provide custom path: `hand_path='/path/to/hand.png'`
- Or disable hand: `show_hand=False`

### Video Too Long

**Problem**: Animation takes too long

**Solution**:
- Reduce `draw_duration` for each layer
- Reduce number of layers
- Reduce `final_hold_duration`

### Video Too Short

**Problem**: Animation too fast

**Solution**:
- Increase `draw_duration` for each layer
- Increase `final_hold_duration`

### Poor Quality

**Problem**: Video looks pixelated

**Solution**:
- Lower `crf` value (e.g., `crf=15`)
- Increase resolution
- Use higher quality source images

### Large File Size

**Problem**: Video file too large

**Solution**:
- Increase `crf` value (e.g., `crf=23`)
- Reduce resolution
- Reduce `fps`
- Shorten duration

## Comparison: Static vs Whiteboard Export

### Static Export (`export_scene_to_video`)
- All layers visible from start
- Optional camera animations (pan, zoom)
- Faster rendering
- Smaller file sizes
- Good for: camera movements, completed scenes

### Whiteboard Export (`export_scene_to_whiteboard_video`)
- Progressive layer-by-layer drawing
- Animated drawing hand
- Longer rendering time
- Larger file sizes
- Good for: presentations, tutorials, explanations

## Example Workflow

```python
from whiteboard_animator import export_scene_to_whiteboard_video

# 1. Define your scene
scene = {
    'layers': [
        # Define all your layers with z_index and draw_duration
    ]
}

# 2. Configure camera (optional)
camera = {
    'width': 1920,
    'height': 1080,
    'position': {'x': 0.5, 'y': 0.5}
}

# 3. Export whiteboard video
result = export_scene_to_whiteboard_video(
    scene,
    'my_video.mp4',
    fps=30,
    camera_config=camera,
    show_hand=True,
    final_hold_duration=3.0
)

# 4. Check result
if result['success']:
    print(f"✅ Video created: {result['output_path']}")
    print(f"   Duration: {result['duration']:.1f}s")
    print(f"   Resolution: {result['resolution']}")
else:
    print(f"❌ Export failed: {result['error']}")
```

## Related Documentation

- **SCENE_COMPOSITION_GUIDE.md**: Complete guide for scene composition with camera
- **demo_whiteboard_video.py**: Working examples of whiteboard video export
- **demo_scene_composition.py**: Examples of static scene composition

## Support

For issues or questions:
1. Check this documentation
2. Review demo files: `demo_whiteboard_video.py`
3. Check function docstrings in `whiteboard_animator.py`
4. Review test files for additional examples

---

**Version**: 1.0.0  
**Last Updated**: 2024  
**License**: Same as whiteboard animator project
