"""
Export Formats Module for Whiteboard Animator
Provides advanced export functionality including GIF, WebM, PNG sequences, and more.
"""

import os
import cv2
import numpy as np
from pathlib import Path
from PIL import Image

# Social media platform presets
SOCIAL_MEDIA_PRESETS = {
    'youtube': {
        'resolution': (1920, 1080),
        'fps': 30,
        'format': 'mp4',
        'codec': 'h264',
        'bitrate': '8M',
        'aspect_ratio': '16:9',
        'description': 'YouTube standard (1080p 16:9)'
    },
    'youtube-shorts': {
        'resolution': (1080, 1920),
        'fps': 30,
        'format': 'mp4',
        'codec': 'h264',
        'bitrate': '6M',
        'aspect_ratio': '9:16',
        'description': 'YouTube Shorts (vertical 9:16)'
    },
    'tiktok': {
        'resolution': (1080, 1920),
        'fps': 30,
        'format': 'mp4',
        'codec': 'h264',
        'bitrate': '5M',
        'aspect_ratio': '9:16',
        'description': 'TikTok (vertical 9:16)'
    },
    'instagram-feed': {
        'resolution': (1080, 1080),
        'fps': 30,
        'format': 'mp4',
        'codec': 'h264',
        'bitrate': '5M',
        'aspect_ratio': '1:1',
        'description': 'Instagram feed (square 1:1)'
    },
    'instagram-story': {
        'resolution': (1080, 1920),
        'fps': 30,
        'format': 'mp4',
        'codec': 'h264',
        'bitrate': '5M',
        'aspect_ratio': '9:16',
        'description': 'Instagram Story/Reels (vertical 9:16)'
    },
    'instagram-reel': {
        'resolution': (1080, 1920),
        'fps': 30,
        'format': 'mp4',
        'codec': 'h264',
        'bitrate': '5M',
        'aspect_ratio': '9:16',
        'description': 'Instagram Reels (vertical 9:16)'
    },
    'facebook': {
        'resolution': (1280, 720),
        'fps': 30,
        'format': 'mp4',
        'codec': 'h264',
        'bitrate': '4M',
        'aspect_ratio': '16:9',
        'description': 'Facebook standard (720p 16:9)'
    },
    'twitter': {
        'resolution': (1280, 720),
        'fps': 30,
        'format': 'mp4',
        'codec': 'h264',
        'bitrate': '4M',
        'aspect_ratio': '16:9',
        'description': 'Twitter/X (720p 16:9)'
    },
    'linkedin': {
        'resolution': (1920, 1080),
        'fps': 30,
        'format': 'mp4',
        'codec': 'h264',
        'bitrate': '5M',
        'aspect_ratio': '16:9',
        'description': 'LinkedIn (1080p 16:9)'
    }
}


def export_gif(frames, output_path, fps=10, loop=0, optimize=True, quality=85):
    """
    Export frames as an animated GIF.
    
    Args:
        frames: List of frames (numpy arrays in BGR format)
        output_path: Path to save the GIF
        fps: Frames per second (default: 10)
        loop: Number of loops (0 = infinite)
        optimize: Optimize GIF size
        quality: Quality setting (1-100, higher is better)
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        if not frames:
            print("❌ No frames to export")
            return False
        
        # Convert frames to PIL Images
        pil_images = []
        for frame in frames:
            # Convert BGR to RGB
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            pil_img = Image.fromarray(frame_rgb)
            pil_images.append(pil_img)
        
        # Calculate duration per frame in milliseconds
        duration = int(1000 / fps)
        
        # Save as GIF
        pil_images[0].save(
            output_path,
            save_all=True,
            append_images=pil_images[1:],
            duration=duration,
            loop=loop,
            optimize=optimize
        )
        
        print(f"✅ GIF exported successfully: {output_path}")
        return True
        
    except Exception as e:
        print(f"❌ Error exporting GIF: {e}")
        return False


def export_webm(frames, output_path, fps=30, quality=10, with_alpha=False):
    """
    Export frames as WebM video format.
    
    Args:
        frames: List of frames (numpy arrays in BGR format)
        output_path: Path to save the WebM file
        fps: Frames per second
        quality: Quality (0-63, lower is better)
        with_alpha: Include alpha channel for transparency
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        import av
        
        if not frames:
            print("❌ No frames to export")
            return False
        
        # Get dimensions from first frame
        height, width = frames[0].shape[:2]
        
        # Open output container
        container = av.open(output_path, mode='w')
        
        # Add video stream with VP9 codec (WebM)
        codec = 'vp9'
        pix_fmt = 'yuva420p' if with_alpha else 'yuv420p'
        stream = container.add_stream(codec, rate=fps)
        stream.width = width
        stream.height = height
        stream.pix_fmt = pix_fmt
        stream.options = {'crf': str(quality)}
        
        # Encode frames
        for frame in frames:
            # Convert frame to appropriate format
            if with_alpha and frame.shape[2] == 3:
                # Add alpha channel if not present
                alpha = np.ones((height, width, 1), dtype=np.uint8) * 255
                frame = np.concatenate([frame, alpha], axis=2)
            
            # Create VideoFrame
            if with_alpha:
                av_frame = av.VideoFrame.from_ndarray(frame, format='bgra')
            else:
                av_frame = av.VideoFrame.from_ndarray(frame, format='bgr24')
            
            # Encode
            packets = stream.encode(av_frame)
            for packet in packets:
                container.mux(packet)
        
        # Flush encoder
        packets = stream.encode()
        for packet in packets:
            container.mux(packet)
        
        container.close()
        
        print(f"✅ WebM exported successfully: {output_path}")
        return True
        
    except ImportError:
        print("❌ PyAV library required for WebM export. Install with: pip install av")
        return False
    except Exception as e:
        print(f"❌ Error exporting WebM: {e}")
        return False


def export_png_sequence(frames, output_dir, prefix="frame", start_number=0, padding=6):
    """
    Export frames as a sequence of PNG images.
    
    Args:
        frames: List of frames (numpy arrays in BGR format)
        output_dir: Directory to save PNG files
        prefix: Filename prefix
        start_number: Starting frame number
        padding: Number of digits for frame numbering
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        if not frames:
            print("❌ No frames to export")
            return False
        
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Save each frame
        for i, frame in enumerate(frames):
            frame_num = start_number + i
            filename = f"{prefix}_{frame_num:0{padding}d}.png"
            filepath = os.path.join(output_dir, filename)
            cv2.imwrite(filepath, frame)
        
        print(f"✅ PNG sequence exported successfully: {len(frames)} frames in {output_dir}")
        return True
        
    except Exception as e:
        print(f"❌ Error exporting PNG sequence: {e}")
        return False


def export_with_transparency(frames, output_path, fps=30, codec='vp9', quality=10):
    """
    Export frames with alpha channel (transparency support).
    
    Args:
        frames: List of frames (numpy arrays in BGRA format)
        output_path: Path to save the video
        fps: Frames per second
        codec: Video codec ('vp9' for WebM, 'prores' for ProRes)
        quality: Quality setting
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        import av
        
        if not frames:
            print("❌ No frames to export")
            return False
        
        # Determine output format based on codec
        if codec == 'prores':
            container_format = 'mov'
            pix_fmt = 'yuva444p10le'
        else:  # vp9
            container_format = 'webm'
            pix_fmt = 'yuva420p'
            
        # Ensure output path has correct extension
        output_path = str(output_path)
        if not output_path.endswith(f'.{container_format}'):
            output_path = output_path.rsplit('.', 1)[0] + f'.{container_format}'
        
        # Get dimensions from first frame
        height, width = frames[0].shape[:2]
        
        # Open output container
        container = av.open(output_path, mode='w')
        
        # Add video stream
        stream = container.add_stream(codec, rate=fps)
        stream.width = width
        stream.height = height
        stream.pix_fmt = pix_fmt
        
        if codec != 'prores':
            stream.options = {'crf': str(quality)}
        
        # Encode frames
        for frame in frames:
            # Ensure frame has alpha channel
            if frame.shape[2] == 3:
                alpha = np.ones((height, width, 1), dtype=np.uint8) * 255
                frame = np.concatenate([frame, alpha], axis=2)
            
            # Create VideoFrame
            av_frame = av.VideoFrame.from_ndarray(frame, format='bgra')
            
            # Encode
            packets = stream.encode(av_frame)
            for packet in packets:
                container.mux(packet)
        
        # Flush encoder
        packets = stream.encode()
        for packet in packets:
            container.mux(packet)
        
        container.close()
        
        print(f"✅ Video with transparency exported successfully: {output_path}")
        return True
        
    except ImportError:
        print("❌ PyAV library required for transparency export. Install with: pip install av")
        return False
    except Exception as e:
        print(f"❌ Error exporting with transparency: {e}")
        return False


def export_lossless(frames, output_path, fps=30, codec='ffv1'):
    """
    Export frames in lossless format.
    
    Args:
        frames: List of frames (numpy arrays in BGR format)
        output_path: Path to save the video
        fps: Frames per second
        codec: Lossless codec ('ffv1', 'utvideo', 'huffyuv')
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        import av
        
        if not frames:
            print("❌ No frames to export")
            return False
        
        # Get dimensions from first frame
        height, width = frames[0].shape[:2]
        
        # Determine container format
        container_format = 'avi' if codec in ['utvideo', 'huffyuv'] else 'mkv'
        
        # Ensure output path has correct extension
        output_path = str(output_path)
        if not output_path.endswith(f'.{container_format}'):
            output_path = output_path.rsplit('.', 1)[0] + f'.{container_format}'
        
        # Open output container
        container = av.open(output_path, mode='w')
        
        # Add video stream
        stream = container.add_stream(codec, rate=fps)
        stream.width = width
        stream.height = height
        stream.pix_fmt = 'yuv420p'
        
        # Encode frames
        for frame in frames:
            av_frame = av.VideoFrame.from_ndarray(frame, format='bgr24')
            packets = stream.encode(av_frame)
            for packet in packets:
                container.mux(packet)
        
        # Flush encoder
        packets = stream.encode()
        for packet in packets:
            container.mux(packet)
        
        container.close()
        
        print(f"✅ Lossless video exported successfully: {output_path}")
        return True
        
    except ImportError:
        print("❌ PyAV library required for lossless export. Install with: pip install av")
        return False
    except Exception as e:
        print(f"❌ Error exporting lossless: {e}")
        return False


def get_social_media_preset(platform):
    """
    Get preset configuration for a social media platform.
    
    Args:
        platform: Platform name (e.g., 'youtube', 'tiktok', 'instagram-reel')
    
    Returns:
        dict: Preset configuration or None if not found
    """
    platform_lower = platform.lower()
    return SOCIAL_MEDIA_PRESETS.get(platform_lower)


def list_social_media_presets():
    """
    List all available social media presets.
    
    Returns:
        dict: Dictionary of all presets
    """
    return SOCIAL_MEDIA_PRESETS.copy()


def print_social_media_presets():
    """Print all available social media presets in a formatted way."""
    print("\n📱 Available Social Media Presets:\n")
    print("-" * 80)
    
    for name, preset in SOCIAL_MEDIA_PRESETS.items():
        res = preset['resolution']
        print(f"  {name:20s} - {preset['description']}")
        print(f"  {' '*20}   Resolution: {res[0]}x{res[1]}, FPS: {preset['fps']}, Format: {preset['format'].upper()}")
        print("-" * 80)
