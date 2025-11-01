"""
Particle System Module for Whiteboard Animator

This module provides comprehensive particle effects for whiteboard animations:
- Confetti effect for celebrations
- Sparkle effect for twinkling stars
- Smoke/dust trails for motion
- Explosion effects
- Magic sparkles attached to objects/text
- Custom configurable particle systems

Dependencies:
- numpy: For numerical operations
- cv2 (OpenCV): For rendering
"""

import numpy as np
import cv2
import math
from typing import List, Tuple, Dict, Optional, Any
import random


class Particle:
    """Base class for a single particle."""
    
    def __init__(
        self,
        position: Tuple[float, float],
        velocity: Tuple[float, float],
        color: Tuple[int, int, int],
        size: float,
        lifetime: float,
        shape: str = 'circle'
    ):
        """
        Initialize a particle.
        
        Args:
            position: (x, y) starting position
            velocity: (vx, vy) velocity vector
            color: (B, G, R) color in BGR format
            size: Particle size in pixels
            lifetime: Lifetime in seconds
            shape: 'circle', 'square', 'star', 'triangle'
        """
        self.x, self.y = position
        self.vx, self.vy = velocity
        self.color = color
        self.size = size
        self.lifetime = lifetime
        self.age = 0.0
        self.shape = shape
        self.rotation = 0.0
        self.angular_velocity = random.uniform(-10, 10)  # degrees per frame
        self.gravity = 0.0
        self.fade = True
        
    def update(self, dt: float):
        """
        Update particle state.
        
        Args:
            dt: Time delta in seconds
        """
        self.age += dt
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.vy += self.gravity * dt
        self.rotation += self.angular_velocity * dt
        
    def is_alive(self) -> bool:
        """Check if particle is still alive."""
        return self.age < self.lifetime
    
    def get_alpha(self) -> float:
        """Get particle alpha based on age and lifetime."""
        if not self.fade:
            return 1.0
        # Fade out in the last 30% of lifetime
        fade_start = self.lifetime * 0.7
        if self.age < fade_start:
            return 1.0
        else:
            fade_progress = (self.age - fade_start) / (self.lifetime - fade_start)
            return max(0.0, 1.0 - fade_progress)


class ParticleEmitter:
    """Emitter that creates and manages particles."""
    
    def __init__(
        self,
        position: Tuple[float, float],
        emission_rate: float = 10.0,
        particle_lifetime: float = 2.0,
        direction: float = 90.0,
        spread: float = 45.0,
        speed: Tuple[float, float] = (50.0, 100.0),
        colors: List[Tuple[int, int, int]] = None,
        sizes: Tuple[float, float] = (3.0, 8.0),
        shapes: List[str] = None,
        gravity: float = 0.0
    ):
        """
        Initialize particle emitter.
        
        Args:
            position: (x, y) emitter position
            emission_rate: Particles per second
            particle_lifetime: How long each particle lives (seconds)
            direction: Main emission direction in degrees (0=right, 90=up)
            spread: Spread angle in degrees
            speed: (min_speed, max_speed) range in pixels per second
            colors: List of possible particle colors (BGR)
            sizes: (min_size, max_size) range
            shapes: List of particle shapes
            gravity: Gravity force (pixels per second squared)
        """
        self.x, self.y = position
        self.emission_rate = emission_rate
        self.particle_lifetime = particle_lifetime
        self.direction = math.radians(direction)
        self.spread = math.radians(spread)
        self.speed_min, self.speed_max = speed
        self.colors = colors or [(255, 255, 255)]
        self.size_min, self.size_max = sizes
        self.shapes = shapes or ['circle']
        self.gravity = gravity
        self.particles: List[Particle] = []
        self.time_since_emission = 0.0
        self.enabled = True
        self.burst_mode = False
        
    def set_position(self, position: Tuple[float, float]):
        """Update emitter position."""
        self.x, self.y = position
        
    def emit_burst(self, count: int):
        """Emit a burst of particles instantly."""
        for _ in range(count):
            self._create_particle()
    
    def _create_particle(self):
        """Create a single particle."""
        # Random angle within spread
        angle = self.direction + random.uniform(-self.spread / 2, self.spread / 2)
        
        # Random speed
        speed = random.uniform(self.speed_min, self.speed_max)
        
        # Calculate velocity
        vx = math.cos(angle) * speed
        vy = -math.sin(angle) * speed  # Negative because y increases downward
        
        # Random color from palette
        color = random.choice(self.colors)
        
        # Random size
        size = random.uniform(self.size_min, self.size_max)
        
        # Random shape
        shape = random.choice(self.shapes)
        
        # Create particle
        particle = Particle(
            position=(self.x, self.y),
            velocity=(vx, vy),
            color=color,
            size=size,
            lifetime=self.particle_lifetime,
            shape=shape
        )
        particle.gravity = self.gravity
        
        self.particles.append(particle)
    
    def update(self, dt: float):
        """
        Update all particles and emit new ones.
        
        Args:
            dt: Time delta in seconds
        """
        # Update existing particles
        for particle in self.particles:
            particle.update(dt)
        
        # Remove dead particles
        self.particles = [p for p in self.particles if p.is_alive()]
        
        # Emit new particles if enabled and not in burst mode
        if self.enabled and not self.burst_mode:
            self.time_since_emission += dt
            particles_to_emit = int(self.time_since_emission * self.emission_rate)
            
            for _ in range(particles_to_emit):
                self._create_particle()
            
            self.time_since_emission -= particles_to_emit / self.emission_rate
    
    def render(self, frame: np.ndarray):
        """
        Render all particles onto a frame.
        
        Args:
            frame: OpenCV image (numpy array)
        """
        for particle in self.particles:
            self._render_particle(frame, particle)
    
    def _render_particle(self, frame: np.ndarray, particle: Particle):
        """Render a single particle."""
        # Get alpha for fading
        alpha = particle.get_alpha()
        if alpha <= 0:
            return
        
        # Get integer position
        x = int(particle.x)
        y = int(particle.y)
        
        # Check if particle is within frame bounds
        h, w = frame.shape[:2]
        if x < 0 or x >= w or y < 0 or y >= h:
            return
        
        # Render based on shape
        if particle.shape == 'circle':
            self._render_circle(frame, x, y, particle, alpha)
        elif particle.shape == 'square':
            self._render_square(frame, x, y, particle, alpha)
        elif particle.shape == 'star':
            self._render_star(frame, x, y, particle, alpha)
        elif particle.shape == 'triangle':
            self._render_triangle(frame, x, y, particle, alpha)
    
    def _render_circle(self, frame, x, y, particle, alpha):
        """Render a circular particle in doodle style (outline only)."""
        radius = int(particle.size)
        if radius < 1:
            radius = 1
        
        # Doodle style: black outline only, no fill
        thickness = max(1, int(particle.size / 4))
        
        # Create overlay for alpha blending
        overlay = frame.copy()
        cv2.circle(overlay, (x, y), radius, (0, 0, 0), thickness)
        
        # Blend with alpha
        cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0, frame)
    
    def _render_square(self, frame, x, y, particle, alpha):
        """Render a square particle in doodle style (outline only)."""
        half_size = int(particle.size)
        
        # Calculate rotated corners
        corners = self._get_rotated_square(x, y, half_size, particle.rotation)
        
        # Doodle style: black outline only, no fill
        thickness = max(1, int(particle.size / 4))
        
        # Create overlay
        overlay = frame.copy()
        cv2.polylines(overlay, [corners], True, (0, 0, 0), thickness)
        
        # Blend with alpha
        cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0, frame)
    
    def _render_star(self, frame, x, y, particle, alpha):
        """Render a star particle in doodle style (outline only)."""
        outer_radius = int(particle.size)
        inner_radius = int(particle.size * 0.4)
        
        # Calculate star points
        points = self._get_star_points(x, y, outer_radius, inner_radius, particle.rotation)
        
        # Doodle style: black outline only, no fill
        thickness = max(1, int(particle.size / 4))
        
        # Create overlay
        overlay = frame.copy()
        cv2.polylines(overlay, [points], True, (0, 0, 0), thickness)
        
        # Blend with alpha
        cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0, frame)
    
    def _render_triangle(self, frame, x, y, particle, alpha):
        """Render a triangle particle in doodle style (outline only)."""
        size = int(particle.size)
        
        # Calculate rotated triangle points
        points = self._get_rotated_triangle(x, y, size, particle.rotation)
        
        # Doodle style: black outline only, no fill
        thickness = max(1, int(particle.size / 4))
        
        # Create overlay
        overlay = frame.copy()
        cv2.polylines(overlay, [points], True, (0, 0, 0), thickness)
        
        # Blend with alpha
        cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0, frame)
    
    def _get_rotated_square(self, cx, cy, half_size, rotation):
        """Get rotated square corners."""
        angle = math.radians(rotation)
        cos_a = math.cos(angle)
        sin_a = math.sin(angle)
        
        corners = []
        for dx, dy in [(-1, -1), (1, -1), (1, 1), (-1, 1)]:
            px = dx * half_size
            py = dy * half_size
            rx = px * cos_a - py * sin_a
            ry = px * sin_a + py * cos_a
            corners.append([int(cx + rx), int(cy + ry)])
        
        return np.array(corners, dtype=np.int32)
    
    def _get_star_points(self, cx, cy, outer_radius, inner_radius, rotation):
        """Get star points."""
        angle = math.radians(rotation)
        points = []
        
        for i in range(10):
            r = outer_radius if i % 2 == 0 else inner_radius
            theta = angle + (i * math.pi / 5)
            x = int(cx + r * math.cos(theta))
            y = int(cy + r * math.sin(theta))
            points.append([x, y])
        
        return np.array(points, dtype=np.int32)
    
    def _get_rotated_triangle(self, cx, cy, size, rotation):
        """Get rotated triangle points."""
        angle = math.radians(rotation)
        cos_a = math.cos(angle)
        sin_a = math.sin(angle)
        
        # Triangle points (pointing up)
        local_points = [
            (0, -size),
            (-size * 0.866, size * 0.5),
            (size * 0.866, size * 0.5)
        ]
        
        points = []
        for px, py in local_points:
            rx = px * cos_a - py * sin_a
            ry = px * sin_a + py * cos_a
            points.append([int(cx + rx), int(cy + ry)])
        
        return np.array(points, dtype=np.int32)


class ParticleSystem:
    """Main particle system that manages multiple emitters and effects."""
    
    def __init__(self, frame_rate: int = 30):
        """
        Initialize the particle system.
        
        Args:
            frame_rate: Video frame rate (FPS)
        """
        self.frame_rate = frame_rate
        self.dt = 1.0 / frame_rate
        self.emitters: List[ParticleEmitter] = []
        
    def add_emitter(self, emitter: ParticleEmitter):
        """Add an emitter to the system."""
        self.emitters.append(emitter)
        
    def update(self):
        """Update all emitters."""
        for emitter in self.emitters:
            emitter.update(self.dt)
    
    def render(self, frame: np.ndarray):
        """Render all particles onto a frame."""
        for emitter in self.emitters:
            emitter.render(frame)
    
    def clear(self):
        """Remove all emitters."""
        self.emitters = []
    
    @staticmethod
    def create_confetti_effect(
        position: Tuple[float, float],
        duration: float = 3.0,
        burst_count: int = 100
    ) -> 'ParticleSystem':
        """
        Create a confetti celebration effect.
        
        Args:
            position: (x, y) position to emit from
            duration: How long the effect lasts
            burst_count: Number of confetti pieces
            
        Returns:
            ParticleSystem configured for confetti
        """
        system = ParticleSystem()
        
        # Doodle style: black and white only
        colors = [
            (0, 0, 0),      # Black
            (50, 50, 50),   # Dark gray
            (100, 100, 100) # Gray
        ]
        
        emitter = ParticleEmitter(
            position=position,
            emission_rate=0,  # Burst mode
            particle_lifetime=duration,
            direction=90,  # Up
            spread=180,  # Wide spread
            speed=(100, 300),
            colors=colors,
            sizes=(4, 10),
            shapes=['square', 'circle', 'triangle'],
            gravity=200  # Fall down
        )
        emitter.burst_mode = True
        emitter.emit_burst(burst_count)
        
        system.add_emitter(emitter)
        return system
    
    @staticmethod
    def create_sparkle_effect(
        position: Tuple[float, float],
        duration: float = 2.0,
        emission_rate: float = 30.0
    ) -> 'ParticleSystem':
        """
        Create a twinkling sparkle effect.
        
        Args:
            position: (x, y) position to emit from
            duration: How long the effect lasts
            emission_rate: Sparkles per second
            
        Returns:
            ParticleSystem configured for sparkles
        """
        system = ParticleSystem()
        
        # Doodle style: black and white only
        colors = [
            (0, 0, 0),      # Black
            (50, 50, 50),   # Dark gray
        ]
        
        emitter = ParticleEmitter(
            position=position,
            emission_rate=emission_rate,
            particle_lifetime=1.0,
            direction=0,
            spread=360,  # All directions
            speed=(20, 60),
            colors=colors,
            sizes=(2, 5),
            shapes=['star', 'circle'],
            gravity=0  # No gravity for sparkles
        )
        
        system.add_emitter(emitter)
        return system
    
    @staticmethod
    def create_smoke_trail(
        start_position: Tuple[float, float],
        duration: float = 2.0,
        emission_rate: float = 20.0
    ) -> 'ParticleSystem':
        """
        Create a smoke/dust trail effect.
        
        Args:
            start_position: (x, y) starting position
            duration: How long the effect lasts
            emission_rate: Smoke particles per second
            
        Returns:
            ParticleSystem configured for smoke
        """
        system = ParticleSystem()
        
        # Doodle style: black and white only
        colors = [
            (100, 100, 100),  # Gray
            (80, 80, 80),     # Dark gray
            (60, 60, 60),     # Darker gray
        ]
        
        emitter = ParticleEmitter(
            position=start_position,
            emission_rate=emission_rate,
            particle_lifetime=1.5,
            direction=90,
            spread=60,
            speed=(10, 40),
            colors=colors,
            sizes=(8, 16),
            shapes=['circle'],
            gravity=-20  # Slight upward drift
        )
        
        system.add_emitter(emitter)
        return system
    
    @staticmethod
    def create_explosion_effect(
        position: Tuple[float, float],
        particle_count: int = 50
    ) -> 'ParticleSystem':
        """
        Create an explosion effect.
        
        Args:
            position: (x, y) explosion center
            particle_count: Number of explosion particles
            
        Returns:
            ParticleSystem configured for explosion
        """
        system = ParticleSystem()
        
        # Doodle style: black and white only
        colors = [
            (0, 0, 0),      # Black
            (30, 30, 30),   # Very dark gray
            (60, 60, 60),   # Dark gray
        ]
        
        emitter = ParticleEmitter(
            position=position,
            emission_rate=0,  # Burst mode
            particle_lifetime=1.5,
            direction=0,
            spread=360,  # Radial explosion
            speed=(150, 400),
            colors=colors,
            sizes=(3, 12),
            shapes=['circle', 'star'],
            gravity=100  # Particles fall
        )
        emitter.burst_mode = True
        emitter.emit_burst(particle_count)
        
        system.add_emitter(emitter)
        return system
    
    @staticmethod
    def create_magic_sparkles(
        position: Tuple[float, float],
        duration: float = 3.0,
        emission_rate: float = 15.0
    ) -> 'ParticleSystem':
        """
        Create magic sparkles effect (for text/objects).
        
        Args:
            position: (x, y) position to emit from
            duration: How long the effect lasts
            emission_rate: Magic sparkles per second
            
        Returns:
            ParticleSystem configured for magic sparkles
        """
        system = ParticleSystem()
        
        # Doodle style: black and white only
        colors = [
            (0, 0, 0),      # Black
            (50, 50, 50),   # Dark gray
        ]
        
        emitter = ParticleEmitter(
            position=position,
            emission_rate=emission_rate,
            particle_lifetime=2.0,
            direction=90,
            spread=180,
            speed=(30, 80),
            colors=colors,
            sizes=(3, 8),
            shapes=['star'],
            gravity=-30  # Float upward
        )
        
        system.add_emitter(emitter)
        return system
    
    @staticmethod
    def create_custom_particle_system(config: Dict[str, Any]) -> 'ParticleSystem':
        """
        Create a custom particle system from configuration.
        
        Args:
            config: Dictionary with particle system configuration
            
        Returns:
            ParticleSystem configured from config
        """
        system = ParticleSystem(
            frame_rate=config.get('frame_rate', 30)
        )
        
        emitters_config = config.get('emitters', [])
        for emitter_config in emitters_config:
            position = tuple(emitter_config.get('position', [0, 0]))
            
            # Parse colors from various formats
            colors = []
            for color in emitter_config.get('colors', [[255, 255, 255]]):
                if isinstance(color, list):
                    colors.append(tuple(color))
                else:
                    colors.append(color)
            
            emitter = ParticleEmitter(
                position=position,
                emission_rate=emitter_config.get('emission_rate', 10.0),
                particle_lifetime=emitter_config.get('particle_lifetime', 2.0),
                direction=emitter_config.get('direction', 90.0),
                spread=emitter_config.get('spread', 45.0),
                speed=tuple(emitter_config.get('speed', [50, 100])),
                colors=colors,
                sizes=tuple(emitter_config.get('sizes', [3, 8])),
                shapes=emitter_config.get('shapes', ['circle']),
                gravity=emitter_config.get('gravity', 0.0)
            )
            
            # Handle burst mode
            if emitter_config.get('burst_mode', False):
                emitter.burst_mode = True
                emitter.emit_burst(emitter_config.get('burst_count', 50))
            
            system.add_emitter(emitter)
        
        return system


def apply_particle_effect(
    frame: np.ndarray,
    particle_config: Dict[str, Any],
    frame_index: int,
    total_frames: int,
    frame_rate: int = 30
) -> np.ndarray:
    """
    Apply particle effects to a frame based on configuration.
    
    Args:
        frame: Input frame (numpy array)
        particle_config: Particle effect configuration
        frame_index: Current frame index
        total_frames: Total number of frames for this effect
        frame_rate: Video frame rate
        
    Returns:
        Frame with particle effects applied
    """
    effect_type = particle_config.get('type', 'confetti')
    position = particle_config.get('position', [frame.shape[1] // 2, frame.shape[0] // 2])
    position = tuple(position)
    
    # Create particle system based on effect type
    if effect_type == 'confetti':
        duration = particle_config.get('duration', 3.0)
        burst_count = particle_config.get('burst_count', 100)
        system = ParticleSystem.create_confetti_effect(position, duration, burst_count)
    elif effect_type == 'sparkle':
        duration = particle_config.get('duration', 2.0)
        emission_rate = particle_config.get('emission_rate', 30.0)
        system = ParticleSystem.create_sparkle_effect(position, duration, emission_rate)
    elif effect_type == 'smoke':
        duration = particle_config.get('duration', 2.0)
        emission_rate = particle_config.get('emission_rate', 20.0)
        system = ParticleSystem.create_smoke_trail(position, duration, emission_rate)
    elif effect_type == 'explosion':
        particle_count = particle_config.get('particle_count', 50)
        system = ParticleSystem.create_explosion_effect(position, particle_count)
    elif effect_type == 'magic':
        duration = particle_config.get('duration', 3.0)
        emission_rate = particle_config.get('emission_rate', 15.0)
        system = ParticleSystem.create_magic_sparkles(position, duration, emission_rate)
    elif effect_type == 'custom':
        system = ParticleSystem.create_custom_particle_system(particle_config)
    else:
        # Unknown effect type, return frame unchanged
        return frame
    
    # Simulate up to current frame
    system.frame_rate = frame_rate
    for _ in range(frame_index + 1):
        system.update()
    
    # Render particles on frame copy
    result = frame.copy()
    system.render(result)
    
    return result
