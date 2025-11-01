"""
Timeline and Synchronization System for Whiteboard Animator

This module provides advanced timeline features including:
- Global timeline across all slides
- Keyframe system for property animations
- Time markers for timeline navigation
- Sync points for multi-element synchronization
- Animation curves (easing functions)
- Time remapping capabilities
- Loop segments functionality
"""

import math
from typing import Dict, List, Any, Optional, Tuple, Callable
from dataclasses import dataclass, field
from enum import Enum


class KeyframeInterpolation(Enum):
    """Types of interpolation between keyframes."""
    LINEAR = "linear"
    EASE_IN = "ease_in"
    EASE_OUT = "ease_out"
    EASE_IN_OUT = "ease_in_out"
    EASE_IN_CUBIC = "ease_in_cubic"
    EASE_OUT_CUBIC = "ease_out_cubic"
    STEP = "step"  # No interpolation, jump to value
    BEZIER = "bezier"  # Custom bezier curve


@dataclass
class Keyframe:
    """Represents a keyframe at a specific time with a value."""
    time: float  # Time in seconds
    value: Any  # Can be number, tuple, dict, etc.
    interpolation: KeyframeInterpolation = KeyframeInterpolation.LINEAR
    bezier_handles: Optional[Tuple[float, float, float, float]] = None  # For bezier curves: (cp1x, cp1y, cp2x, cp2y)
    
    def __post_init__(self):
        if isinstance(self.interpolation, str):
            self.interpolation = KeyframeInterpolation(self.interpolation)


@dataclass
class TimeMarker:
    """A marker at a specific time on the timeline."""
    time: float  # Time in seconds
    label: str
    color: Optional[str] = None  # Hex color for UI representation
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SyncPoint:
    """A synchronization point where multiple elements should align."""
    time: float  # Time in seconds
    elements: List[str]  # IDs of elements to sync
    label: str
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class LoopSegment:
    """A segment of the timeline that loops."""
    start_time: float  # Start time in seconds
    end_time: float  # End time in seconds
    loop_count: int  # Number of times to loop (-1 for infinite in preview)
    label: Optional[str] = None


@dataclass
class TimeRemapping:
    """Time remapping configuration for speed changes."""
    original_start: float
    original_end: float
    remapped_start: float
    remapped_end: float
    curve: KeyframeInterpolation = KeyframeInterpolation.LINEAR
    
    def get_remapped_time(self, time: float) -> float:
        """Get the remapped time for a given input time."""
        if time < self.original_start:
            return self.remapped_start
        if time > self.original_end:
            return self.remapped_end
        
        # Calculate progress through original range
        progress = (time - self.original_start) / (self.original_end - self.original_start)
        
        # Apply curve
        eased_progress = apply_easing(progress, self.curve)
        
        # Map to remapped range
        return self.remapped_start + eased_progress * (self.remapped_end - self.remapped_start)


@dataclass
class PropertyTrack:
    """A track of keyframes for a specific property."""
    property_path: str  # e.g., "layers.0.opacity", "camera.zoom"
    keyframes: List[Keyframe] = field(default_factory=list)
    
    def add_keyframe(self, time: float, value: Any, 
                     interpolation: KeyframeInterpolation = KeyframeInterpolation.LINEAR,
                     bezier_handles: Optional[Tuple[float, float, float, float]] = None):
        """Add a keyframe to this track."""
        kf = Keyframe(time, value, interpolation, bezier_handles)
        self.keyframes.append(kf)
        # Keep keyframes sorted by time
        self.keyframes.sort(key=lambda k: k.time)
    
    def get_value_at_time(self, time: float) -> Any:
        """Get the interpolated value at a specific time."""
        if not self.keyframes:
            return None
        
        # If before first keyframe, return first value
        if time < self.keyframes[0].time:
            return self.keyframes[0].value
        
        # Check for exact keyframe match first
        for kf in self.keyframes:
            if abs(time - kf.time) < 0.0001:  # Close enough to be considered exact
                return kf.value
        
        # If after last keyframe, return last value
        if time > self.keyframes[-1].time:
            return self.keyframes[-1].value
        
        # Find surrounding keyframes
        for i in range(len(self.keyframes) - 1):
            kf1 = self.keyframes[i]
            kf2 = self.keyframes[i + 1]
            
            if kf1.time < time < kf2.time:
                # Calculate progress between keyframes
                progress = (time - kf1.time) / (kf2.time - kf1.time)
                
                # Apply interpolation
                if kf1.interpolation == KeyframeInterpolation.STEP:
                    return kf1.value
                
                # Apply easing
                eased_progress = apply_easing(progress, kf1.interpolation, kf1.bezier_handles)
                
                # Interpolate value
                return interpolate_values(kf1.value, kf2.value, eased_progress)
        
        return self.keyframes[-1].value


class GlobalTimeline:
    """Global timeline managing all animations across slides."""
    
    def __init__(self, duration: float = 0.0, frame_rate: int = 30):
        self.duration = duration  # Total duration in seconds
        self.frame_rate = frame_rate
        self.property_tracks: Dict[str, PropertyTrack] = {}
        self.markers: List[TimeMarker] = []
        self.sync_points: List[SyncPoint] = []
        self.loop_segments: List[LoopSegment] = []
        self.time_remappings: List[TimeRemapping] = []
    
    def add_property_track(self, property_path: str) -> PropertyTrack:
        """Add a new property track or return existing one."""
        if property_path not in self.property_tracks:
            self.property_tracks[property_path] = PropertyTrack(property_path)
        return self.property_tracks[property_path]
    
    def add_keyframe(self, property_path: str, time: float, value: Any,
                     interpolation: KeyframeInterpolation = KeyframeInterpolation.LINEAR,
                     bezier_handles: Optional[Tuple[float, float, float, float]] = None):
        """Add a keyframe to a property track."""
        track = self.add_property_track(property_path)
        track.add_keyframe(time, value, interpolation, bezier_handles)
    
    def add_marker(self, time: float, label: str, color: Optional[str] = None, 
                   metadata: Optional[Dict[str, Any]] = None):
        """Add a time marker."""
        marker = TimeMarker(time, label, color, metadata or {})
        self.markers.append(marker)
        self.markers.sort(key=lambda m: m.time)
    
    def add_sync_point(self, time: float, elements: List[str], label: str,
                       metadata: Optional[Dict[str, Any]] = None):
        """Add a synchronization point."""
        sync = SyncPoint(time, elements, label, metadata or {})
        self.sync_points.append(sync)
        self.sync_points.sort(key=lambda s: s.time)
    
    def add_loop_segment(self, start_time: float, end_time: float, 
                         loop_count: int, label: Optional[str] = None):
        """Add a loop segment."""
        loop = LoopSegment(start_time, end_time, loop_count, label)
        self.loop_segments.append(loop)
        self.loop_segments.sort(key=lambda l: l.start_time)
    
    def add_time_remapping(self, original_start: float, original_end: float,
                          remapped_start: float, remapped_end: float,
                          curve: KeyframeInterpolation = KeyframeInterpolation.LINEAR):
        """Add a time remapping."""
        remap = TimeRemapping(original_start, original_end, remapped_start, remapped_end, curve)
        self.time_remappings.append(remap)
    
    def get_property_value(self, property_path: str, time: float) -> Any:
        """Get the value of a property at a specific time."""
        if property_path in self.property_tracks:
            return self.property_tracks[property_path].get_value_at_time(time)
        return None
    
    def get_remapped_time(self, time: float) -> float:
        """Get remapped time if time remapping is active."""
        for remap in self.time_remappings:
            if remap.original_start <= time <= remap.original_end:
                return remap.get_remapped_time(time)
        return time
    
    def get_effective_time(self, time: float) -> float:
        """Get effective time accounting for loops and remapping."""
        # First apply loop segments
        effective_time = self._apply_loops(time)
        # Then apply time remapping
        effective_time = self.get_remapped_time(effective_time)
        return effective_time
    
    def _apply_loops(self, time: float) -> float:
        """Apply loop segments to calculate effective time."""
        for loop in self.loop_segments:
            if loop.start_time <= time <= loop.end_time:
                # This time is within a loop segment
                loop_duration = loop.end_time - loop.start_time
                time_in_loop = time - loop.start_time
                
                # For rendering, we don't actually loop infinitely
                # We just return the position within the loop
                return loop.start_time + (time_in_loop % loop_duration)
        return time
    
    def get_total_duration_with_loops(self) -> float:
        """Calculate total duration including loop expansions."""
        total = self.duration
        
        for loop in self.loop_segments:
            if loop.loop_count > 1:
                loop_duration = loop.end_time - loop.start_time
                # Add extra duration for additional loops
                total += loop_duration * (loop.loop_count - 1)
        
        return total
    
    def to_dict(self) -> Dict[str, Any]:
        """Export timeline to dictionary format."""
        return {
            'duration': self.duration,
            'frame_rate': self.frame_rate,
            'property_tracks': {
                path: {
                    'keyframes': [
                        {
                            'time': kf.time,
                            'value': kf.value,
                            'interpolation': kf.interpolation.value,
                            'bezier_handles': kf.bezier_handles
                        }
                        for kf in track.keyframes
                    ]
                }
                for path, track in self.property_tracks.items()
            },
            'markers': [
                {
                    'time': m.time,
                    'label': m.label,
                    'color': m.color,
                    'metadata': m.metadata
                }
                for m in self.markers
            ],
            'sync_points': [
                {
                    'time': s.time,
                    'elements': s.elements,
                    'label': s.label,
                    'metadata': s.metadata
                }
                for s in self.sync_points
            ],
            'loop_segments': [
                {
                    'start_time': l.start_time,
                    'end_time': l.end_time,
                    'loop_count': l.loop_count,
                    'label': l.label
                }
                for l in self.loop_segments
            ],
            'time_remappings': [
                {
                    'original_start': r.original_start,
                    'original_end': r.original_end,
                    'remapped_start': r.remapped_start,
                    'remapped_end': r.remapped_end,
                    'curve': r.curve.value
                }
                for r in self.time_remappings
            ]
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'GlobalTimeline':
        """Create timeline from dictionary format."""
        timeline = cls(
            duration=data.get('duration', 0.0),
            frame_rate=data.get('frame_rate', 30)
        )
        
        # Load property tracks
        for path, track_data in data.get('property_tracks', {}).items():
            track = timeline.add_property_track(path)
            for kf_data in track_data.get('keyframes', []):
                track.add_keyframe(
                    time=kf_data['time'],
                    value=kf_data['value'],
                    interpolation=KeyframeInterpolation(kf_data.get('interpolation', 'linear')),
                    bezier_handles=kf_data.get('bezier_handles')
                )
        
        # Load markers
        for m_data in data.get('markers', []):
            timeline.add_marker(
                time=m_data['time'],
                label=m_data['label'],
                color=m_data.get('color'),
                metadata=m_data.get('metadata', {})
            )
        
        # Load sync points
        for s_data in data.get('sync_points', []):
            timeline.add_sync_point(
                time=s_data['time'],
                elements=s_data['elements'],
                label=s_data['label'],
                metadata=s_data.get('metadata', {})
            )
        
        # Load loop segments
        for l_data in data.get('loop_segments', []):
            timeline.add_loop_segment(
                start_time=l_data['start_time'],
                end_time=l_data['end_time'],
                loop_count=l_data['loop_count'],
                label=l_data.get('label')
            )
        
        # Load time remappings
        for r_data in data.get('time_remappings', []):
            timeline.add_time_remapping(
                original_start=r_data['original_start'],
                original_end=r_data['original_end'],
                remapped_start=r_data['remapped_start'],
                remapped_end=r_data['remapped_end'],
                curve=KeyframeInterpolation(r_data.get('curve', 'linear'))
            )
        
        return timeline


def apply_easing(progress: float, easing: KeyframeInterpolation,
                 bezier_handles: Optional[Tuple[float, float, float, float]] = None) -> float:
    """Apply easing function to progress value."""
    if easing == KeyframeInterpolation.LINEAR:
        return progress
    elif easing == KeyframeInterpolation.EASE_IN:
        return progress * progress
    elif easing == KeyframeInterpolation.EASE_OUT:
        return progress * (2 - progress)
    elif easing == KeyframeInterpolation.EASE_IN_OUT:
        if progress < 0.5:
            return 2 * progress * progress
        else:
            return -1 + (4 - 2 * progress) * progress
    elif easing == KeyframeInterpolation.EASE_IN_CUBIC:
        return progress * progress * progress
    elif easing == KeyframeInterpolation.EASE_OUT_CUBIC:
        p = progress - 1
        return p * p * p + 1
    elif easing == KeyframeInterpolation.STEP:
        return 0.0
    elif easing == KeyframeInterpolation.BEZIER and bezier_handles:
        return cubic_bezier(progress, *bezier_handles)
    return progress


def cubic_bezier(t: float, cp1x: float, cp1y: float, cp2x: float, cp2y: float) -> float:
    """Calculate cubic bezier curve value.
    
    Args:
        t: Progress (0-1)
        cp1x, cp1y: First control point (x, y in 0-1 range)
        cp2x, cp2y: Second control point (x, y in 0-1 range)
    
    Returns:
        Y value at time t
    """
    # Simplified cubic bezier for timing functions
    # P0 = (0, 0), P3 = (1, 1), P1 = (cp1x, cp1y), P2 = (cp2x, cp2y)
    
    # Use Newton-Raphson method to solve for x
    # This is a simplified version - in production, you'd want more iterations
    
    def bezier_x(t):
        return 3 * (1 - t) ** 2 * t * cp1x + 3 * (1 - t) * t ** 2 * cp2x + t ** 3
    
    def bezier_y(t):
        return 3 * (1 - t) ** 2 * t * cp1y + 3 * (1 - t) * t ** 2 * cp2y + t ** 3
    
    # Binary search to find t for given x value (progress)
    t_guess = t
    for _ in range(8):  # 8 iterations should be enough
        x = bezier_x(t_guess)
        if abs(x - t) < 0.001:
            break
        # Derivative
        dx = 3 * (1 - t_guess) ** 2 * cp1x + 6 * (1 - t_guess) * t_guess * (cp2x - cp1x) + 3 * t_guess ** 2 * (1 - cp2x)
        if abs(dx) < 0.000001:
            break
        t_guess -= (x - t) / dx
    
    return bezier_y(t_guess)


def interpolate_values(value1: Any, value2: Any, progress: float) -> Any:
    """Interpolate between two values based on progress."""
    # Handle numeric values
    if isinstance(value1, (int, float)) and isinstance(value2, (int, float)):
        return value1 + (value2 - value1) * progress
    
    # Handle tuples/lists (e.g., RGB colors, positions)
    if isinstance(value1, (tuple, list)) and isinstance(value2, (tuple, list)):
        if len(value1) == len(value2):
            result = []
            for v1, v2 in zip(value1, value2):
                if isinstance(v1, (int, float)) and isinstance(v2, (int, float)):
                    result.append(v1 + (v2 - v1) * progress)
                else:
                    result.append(v1 if progress < 0.5 else v2)
            return tuple(result) if isinstance(value1, tuple) else result
    
    # Handle dictionaries (e.g., position {x, y})
    if isinstance(value1, dict) and isinstance(value2, dict):
        result = {}
        keys = set(value1.keys()) | set(value2.keys())
        for key in keys:
            v1 = value1.get(key, 0)
            v2 = value2.get(key, 0)
            if isinstance(v1, (int, float)) and isinstance(v2, (int, float)):
                result[key] = v1 + (v2 - v1) * progress
            else:
                result[key] = v1 if progress < 0.5 else v2
        return result
    
    # For non-numeric values, switch at 50% progress
    return value1 if progress < 0.5 else value2
