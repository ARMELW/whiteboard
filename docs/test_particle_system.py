#!/usr/bin/env python
"""
Test script for particle animations.
Tests particle effects with a simple animation.
"""

import os
import sys
import cv2
import numpy as np
from particle_system import ParticleSystem, apply_particle_effect

def test_particle_rendering():
    """Test particle rendering to images."""
    print("=" * 60)
    print("PARTICLE SYSTEM TEST")
    print("=" * 60)
    
    # Create output directory
    output_dir = "test_output"
    os.makedirs(output_dir, exist_ok=True)
    
    # Test 1: Confetti effect
    print("\n1. Testing Confetti Effect...")
    frame = np.ones((640, 720, 3), dtype=np.uint8) * 255
    system = ParticleSystem.create_confetti_effect((360, 100), duration=2.0, burst_count=80)
    
    for i in range(60):  # 2 seconds at 30fps
        system.update()
        if i in [0, 15, 30, 45, 59]:  # Save key frames
            test_frame = frame.copy()
            system.render(test_frame)
            cv2.imwrite(f"{output_dir}/confetti_frame_{i:03d}.png", test_frame)
            print(f"   Frame {i}: {len(system.emitters[0].particles)} particles alive")
    
    print(f"   ✅ Confetti frames saved to {output_dir}/")
    
    # Test 2: Sparkle effect
    print("\n2. Testing Sparkle Effect...")
    frame = np.ones((640, 720, 3), dtype=np.uint8) * 255
    system = ParticleSystem.create_sparkle_effect((360, 320), duration=1.5, emission_rate=40.0)
    
    for i in range(45):  # 1.5 seconds at 30fps
        system.update()
        if i in [0, 15, 30, 44]:
            test_frame = frame.copy()
            system.render(test_frame)
            cv2.imwrite(f"{output_dir}/sparkle_frame_{i:03d}.png", test_frame)
            print(f"   Frame {i}: {len(system.emitters[0].particles)} particles alive")
    
    print(f"   ✅ Sparkle frames saved to {output_dir}/")
    
    # Test 3: Explosion effect
    print("\n3. Testing Explosion Effect...")
    frame = np.ones((640, 720, 3), dtype=np.uint8) * 255
    system = ParticleSystem.create_explosion_effect((360, 320), particle_count=60)
    
    for i in range(45):  # 1.5 seconds at 30fps
        system.update()
        if i in [0, 10, 20, 30, 44]:
            test_frame = frame.copy()
            system.render(test_frame)
            cv2.imwrite(f"{output_dir}/explosion_frame_{i:03d}.png", test_frame)
            print(f"   Frame {i}: {len(system.emitters[0].particles)} particles alive")
    
    print(f"   ✅ Explosion frames saved to {output_dir}/")
    
    # Test 4: apply_particle_effect function
    print("\n4. Testing apply_particle_effect function...")
    frame = np.ones((640, 720, 3), dtype=np.uint8) * 255
    
    particle_config = {
        "type": "magic",
        "position": [360, 320],
        "duration": 2.0,
        "emission_rate": 25.0
    }
    
    for i in range(60):  # 2 seconds at 30fps
        if i % 15 == 0:
            result = apply_particle_effect(frame.copy(), particle_config, i, 60, 30)
            cv2.imwrite(f"{output_dir}/magic_frame_{i:03d}.png", result)
            print(f"   Frame {i}: applied particle effect")
    
    print(f"   ✅ Magic sparkle frames saved to {output_dir}/")
    
    # Test 5: Custom particle system
    print("\n5. Testing Custom Particle System...")
    frame = np.ones((640, 720, 3), dtype=np.uint8) * 255
    
    custom_config = {
        "frame_rate": 30,
        "emitters": [
            {
                "position": [200, 320],
                "emission_rate": 15.0,
                "particle_lifetime": 2.0,
                "direction": 45,
                "spread": 30,
                "speed": [80, 150],
                "colors": [[255, 0, 0], [0, 255, 0], [0, 0, 255]],
                "sizes": [5, 10],
                "shapes": ["star", "circle"],
                "gravity": 50,
                "burst_mode": False
            },
            {
                "position": [520, 320],
                "emission_rate": 0,
                "particle_lifetime": 1.5,
                "direction": 90,
                "spread": 360,
                "speed": [100, 200],
                "colors": [[255, 255, 0], [255, 0, 255]],
                "sizes": [4, 8],
                "shapes": ["square"],
                "gravity": 100,
                "burst_mode": True,
                "burst_count": 40
            }
        ]
    }
    
    system = ParticleSystem.create_custom_particle_system(custom_config)
    
    for i in range(60):  # 2 seconds at 30fps
        system.update()
        if i % 15 == 0:
            test_frame = frame.copy()
            system.render(test_frame)
            cv2.imwrite(f"{output_dir}/custom_frame_{i:03d}.png", test_frame)
            total_particles = sum(len(e.particles) for e in system.emitters)
            print(f"   Frame {i}: {total_particles} particles alive")
    
    print(f"   ✅ Custom particle frames saved to {output_dir}/")
    
    print("\n" + "=" * 60)
    print("✅ ALL TESTS PASSED!")
    print(f"Output saved to: {os.path.abspath(output_dir)}/")
    print("=" * 60)
    
    return True

if __name__ == "__main__":
    try:
        success = test_particle_rendering()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
