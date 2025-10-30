# Scene Composition with Camera Viewport Guide

## Overview

The `compose_scene_with_camera` function provides camera-based scene composition, allowing you to render scenes with precise viewport positioning. This function is similar to the TypeScript `exportSceneImage` function used in web-based canvas applications.

## Key Features

- **Camera Viewport Positioning**: Elements are positioned relative to the camera's viewport in the scene
- **Multi-Layer Support**: Supports image, text, shape, arrow, and whiteboard/strokes layers
- **Z-Index Ordering**: Layers are rendered in correct stacking order
- **Transformations**: Supports scale, rotation, flip, and opacity
- **Background Images**: Camera-aware cropping of background images
- **Scene Cameras**: Automatic camera detection from scene configuration

## Function Signature

```python
def compose_scene_with_camera(
    scene_config,
    camera_config=None,
    scene_width=1920,
    scene_height=1080,
    background='#FFFFFF',
    base_path="."
)
```

### Parameters

- **scene_config** (dict): Scene configuration containing:
  - `layers`: List of layer configurations
  - `backgroundImage`: Optional background image path
  - `sceneCameras`: Optional list of camera configurations
  
- **camera_config** (dict, optional): Camera configuration with:
  - `width`: Camera viewport width (default: 800)
  - `height`: Camera viewport height (default: 450)
  - `position`: Dict with `x`, `y` (0.0-1.0, default 0.5, 0.5 for center)
  - `isDefault`: Boolean indicating default camera
  
- **scene_width** (int): Scene width in pixels (default: 1920)

- **scene_height** (int): Scene height in pixels (default: 1080)

- **background** (str or tuple): Background color as hex string or RGB tuple (default: '#FFFFFF')

- **base_path** (str): Base path for resolving relative file paths (default: ".")

### Returns

- **numpy.ndarray**: Composed image in BGR format

## Layer Types

### 1. Image Layer

```python
{
    'id': 'image1',
    'type': 'image',
    'image_path': 'path/to/image.jpg',
    'position': {'x': 100, 'y': 200},
    'z_index': 1,
    'scale': 1.0,
    'opacity': 1.0,
    'rotation': 0,      # degrees
    'flipX': False,     # horizontal flip
    'flipY': False,     # vertical flip
    'visible': True
}
```

### 2. Text Layer

```python
{
    'id': 'text1',
    'type': 'text',
    'text_config': {
        'text': 'Hello World',
        'font': 'Arial',
        'size': 48,
        'color': (255, 0, 0),  # RGB or hex '#FF0000'
        'style': 'bold',       # 'normal', 'bold', 'italic', 'bold_italic'
        'align': 'center',     # 'left', 'center', 'right'
        'line_height': 1.2
    },
    'position': {'x': 500, 'y': 300},
    'z_index': 2,
    'scale': 1.0,
    'opacity': 1.0
}
```

### 3. Shape Layer

```python
{
    'id': 'shape1',
    'type': 'shape',
    'shape_config': {
        'shape': 'circle',           # 'circle', 'rectangle', 'triangle', etc.
        'color': (0, 0, 255),        # Border color
        'fill_color': (200, 200, 255), # Fill color
        'stroke_width': 5,
        'position': {'x': 400, 'y': 400},
        'size': 100,                 # For circle
        'width': 200,                # For rectangle
        'height': 150                # For rectangle
    },
    'position': {'x': 400, 'y': 400},
    'z_index': 0,
    'scale': 1.0,
    'opacity': 0.8
}
```

### 4. Arrow Layer

```python
{
    'id': 'arrow1',
    'type': 'arrow',
    'arrow_config': {
        'start': [100, 100],
        'end': [700, 400],
        'color': (0, 0, 0),
        'fill_color': (0, 0, 0),
        'stroke_width': 3,
        'arrow_size': 20
    },
    'position': {'x': 0, 'y': 0},
    'z_index': 1
}
```

### 5. Whiteboard/Strokes Layer

```python
{
    'id': 'whiteboard1',
    'type': 'whiteboard',
    'strokes': [
        {
            'points': [
                {'x': 100, 'y': 100},
                {'x': 150, 'y': 120},
                {'x': 200, 'y': 140}
            ],
            'strokeWidth': 2,
            'strokeColor': '#000000'
        }
    ],
    'position': {'x': 0, 'y': 0},
    'z_index': 1
}
```

## Camera Positioning

The camera position is specified as normalized coordinates (0.0 to 1.0):
- `{'x': 0.0, 'y': 0.0}`: Top-left corner
- `{'x': 0.5, 'y': 0.5}`: Center (default)
- `{'x': 1.0, 'y': 1.0}`: Bottom-right corner

The camera viewport is calculated as:
```
camera_x = (position.x * scene_width) - (camera_width / 2)
camera_y = (position.y * scene_height) - (camera_height / 2)
```

## Usage Examples

### Example 1: Basic Scene with Manual Camera

```python
import cv2
from whiteboard_animator import compose_scene_with_camera

# Define scene
scene_config = {
    'layers': [
        {
            'id': 'bg_shape',
            'type': 'shape',
            'shape_config': {
                'shape': 'rectangle',
                'color': (100, 100, 255),
                'fill_color': (200, 200, 255),
                'stroke_width': 3,
                'position': {'x': 960, 'y': 540},
                'width': 400,
                'height': 300
            },
            'position': {'x': 960, 'y': 540},
            'z_index': 0
        },
        {
            'id': 'title',
            'type': 'text',
            'text_config': {
                'text': 'My Scene',
                'font': 'Arial',
                'size': 72,
                'color': (0, 0, 0),
                'style': 'bold'
            },
            'position': {'x': 960, 'y': 200},
            'z_index': 1
        }
    ]
}

# Define camera centered on scene
camera_config = {
    'width': 1920,
    'height': 1080,
    'position': {'x': 0.5, 'y': 0.5}
}

# Compose scene
result = compose_scene_with_camera(
    scene_config,
    camera_config,
    scene_width=1920,
    scene_height=1080
)

# Save result
cv2.imwrite('output.png', result)
```

### Example 2: Using Scene Cameras

```python
scene_config = {
    'sceneCameras': [
        {
            'id': 'camera1',
            'width': 800,
            'height': 450,
            'position': {'x': 0.3, 'y': 0.3},
            'isDefault': True
        }
    ],
    'layers': [
        # ... your layers
    ]
}

# Camera will be automatically detected from sceneCameras
result = compose_scene_with_camera(
    scene_config,
    camera_config=None,  # Will use default from sceneCameras
    scene_width=1920,
    scene_height=1080
)
```

### Example 3: Focus on Different Scene Areas

```python
# Create a large scene
scene_config = {
    'layers': [
        {'id': 'tl', 'type': 'text', 'text_config': {'text': 'TOP LEFT'}, 
         'position': {'x': 200, 'y': 200}, 'z_index': 1},
        {'id': 'tr', 'type': 'text', 'text_config': {'text': 'TOP RIGHT'}, 
         'position': {'x': 1720, 'y': 200}, 'z_index': 1},
        {'id': 'bl', 'type': 'text', 'text_config': {'text': 'BOTTOM LEFT'}, 
         'position': {'x': 200, 'y': 880}, 'z_index': 1},
        {'id': 'br', 'type': 'text', 'text_config': {'text': 'BOTTOM RIGHT'}, 
         'position': {'x': 1720, 'y': 880}, 'z_index': 1},
    ]
}

# Focus on top-left
camera_tl = {'width': 800, 'height': 450, 'position': {'x': 0.25, 'y': 0.25}}
result_tl = compose_scene_with_camera(scene_config, camera_tl, 1920, 1080)
cv2.imwrite('focus_top_left.png', result_tl)

# Focus on bottom-right
camera_br = {'width': 800, 'height': 450, 'position': {'x': 0.75, 'y': 0.75}}
result_br = compose_scene_with_camera(scene_config, camera_br, 1920, 1080)
cv2.imwrite('focus_bottom_right.png', result_br)
```

### Example 4: With Background Image

```python
scene_config = {
    'backgroundImage': 'background.jpg',
    'layers': [
        {
            'id': 'overlay',
            'type': 'shape',
            'shape_config': {
                'shape': 'circle',
                'color': (255, 0, 0),
                'fill_color': (255, 200, 200),
                'stroke_width': 5,
                'position': {'x': 960, 'y': 540},
                'size': 150
            },
            'position': {'x': 960, 'y': 540},
            'z_index': 1,
            'opacity': 0.7
        }
    ]
}

camera_config = {
    'width': 1920,
    'height': 1080,
    'position': {'x': 0.5, 'y': 0.5}
}

result = compose_scene_with_camera(
    scene_config,
    camera_config,
    scene_width=1920,
    scene_height=1080,
    background='#F0F0F0'  # Fallback if background image fails
)
```

## Coordinate System

### Scene Coordinates
- Origin (0, 0) is at the top-left of the scene
- Scene dimensions: typically 1920x1080 (configurable)
- All layer positions are specified in scene coordinates

### Camera Viewport
- Camera position is normalized (0.0 to 1.0)
- Camera has its own width and height (e.g., 800x450)
- Camera viewport is calculated in scene coordinates
- Layers are positioned relative to the camera viewport

### Example Calculation
```
Scene: 1920x1080
Camera: 800x450, position (0.5, 0.5)

Camera viewport in scene coordinates:
camera_x = (0.5 * 1920) - (800 / 2) = 960 - 400 = 560
camera_y = (0.5 * 1080) - (450 / 2) = 540 - 225 = 315

Layer at scene position (960, 540) appears at:
viewport_x = 960 - 560 = 400 (center of camera width)
viewport_y = 540 - 315 = 225 (center of camera height)
```

## Best Practices

1. **Use Appropriate Camera Size**: Match your target output resolution
2. **Z-Index Management**: Use clear z-index values (0, 1, 2, ...) to control layer order
3. **Opacity for Overlays**: Use opacity < 1.0 for transparent overlays
4. **Scene Dimensions**: Use larger scene dimensions for detailed compositions
5. **Background Color**: Provide a fallback background color even with background images
6. **File Paths**: Use absolute paths or ensure base_path is set correctly

## Performance Considerations

- Large scenes (> 4K) may require more memory
- Many layers with transformations (rotation, flip) increase processing time
- Background images are cropped to camera viewport for efficiency
- Consider using lower resolution for previews and higher for final output

## Testing

Run the test suite to verify functionality:

```bash
python test_scene_composition.py
```

This will generate test images showing:
- Basic composition
- Camera positioning at different locations
- Layer transformations
- Z-index ordering
- Scene cameras usage

## Troubleshooting

### Layer Not Visible
- Check if layer position is within camera viewport
- Verify z_index ordering
- Check `visible` property (default: true)
- Ensure opacity > 0

### Incorrect Positioning
- Verify scene coordinates vs. camera viewport
- Check camera position calculation
- Ensure scale is applied correctly

### Image Quality Issues
- Use higher resolution camera viewport
- Check image file quality
- Verify scale factors

### Background Not Showing
- Check background image path
- Verify file permissions
- Check if camera viewport includes background area

## Related Functions

- `compose_layers()`: Original layer composition without camera support
- `apply_camera_transform()`: Apply camera transformations to frames
- `render_text_to_image()`: Render text layers
- `render_shape_to_image()`: Render shape layers
- `draw_arrow_progressive()`: Render arrow layers

## Migration from compose_layers

If you're using `compose_layers()`, migration is straightforward:

```python
# Old code
result = compose_layers(layers_config, target_width, target_height)

# New code with camera
scene_config = {'layers': layers_config}
camera_config = {
    'width': target_width,
    'height': target_height,
    'position': {'x': 0.5, 'y': 0.5}
}
result = compose_scene_with_camera(
    scene_config,
    camera_config,
    scene_width=target_width,
    scene_height=target_height
)
```

## Future Enhancements

Potential future additions:
- Camera zoom support
- Multiple camera rendering in one call
- Animation frame generation with camera movement
- Camera transition effects
- Advanced blend modes
- Layer masking
- Effects and filters per layer

## License

This function is part of the whiteboard animator project and follows the same license.
