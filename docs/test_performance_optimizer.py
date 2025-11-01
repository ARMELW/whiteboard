#!/usr/bin/env python3
"""
Test script for performance optimizer module.
Tests all major features without requiring video rendering.
"""

import sys
import json
import time
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from performance_optimizer import (
    PerformanceOptimizer,
    RenderCheckpoint,
    ProgressTracker,
    RenderQueue,
    parse_quality_preset,
    create_batch_config
)


def test_checkpoint_manager():
    """Test checkpoint save/load functionality."""
    print("Testing Checkpoint Manager...")
    
    checkpoint_mgr = RenderCheckpoint(checkpoint_dir="./test_checkpoints")
    
    # Test checkpoint ID generation
    config = {"slides": [{"index": 0, "duration": 5}]}
    checkpoint_id = checkpoint_mgr.generate_checkpoint_id(config)
    print(f"  ✓ Generated checkpoint ID: {checkpoint_id}")
    
    # Test save/load
    state = {
        "frame_index": 100,
        "total_frames": 500,
        "config": config
    }
    
    success = checkpoint_mgr.save_checkpoint(checkpoint_id, state)
    assert success, "Failed to save checkpoint"
    print(f"  ✓ Saved checkpoint")
    
    loaded_state = checkpoint_mgr.load_checkpoint(checkpoint_id)
    assert loaded_state is not None, "Failed to load checkpoint"
    assert loaded_state["frame_index"] == 100, "Checkpoint data mismatch"
    print(f"  ✓ Loaded checkpoint successfully")
    
    # Test list checkpoints
    checkpoints = checkpoint_mgr.list_checkpoints()
    assert len(checkpoints) > 0, "No checkpoints found"
    print(f"  ✓ Listed {len(checkpoints)} checkpoint(s)")
    
    # Cleanup
    checkpoint_mgr.delete_checkpoint(checkpoint_id)
    print(f"  ✓ Deleted checkpoint")
    
    print("✅ Checkpoint Manager tests passed!\n")


def test_progress_tracker():
    """Test progress tracking functionality."""
    print("Testing Progress Tracker...")
    
    tracker = ProgressTracker(total_frames=1000)
    tracker.set_status_file("./test_progress.json")
    
    # Simulate progress
    for i in range(5):
        tracker.increment(100)
    
    progress = tracker.get_progress()
    assert progress["completed_frames"] == 500, "Progress tracking incorrect"
    assert progress["percentage"] == 50.0, "Percentage calculation incorrect"
    print(f"  ✓ Progress: {progress['percentage']:.1f}%")
    print(f"  ✓ FPS: {progress['fps']:.2f}")
    print(f"  ✓ ETA: {progress['eta_seconds']:.1f}s")
    
    # Check status file exists
    status_file = Path("./test_progress.json")
    assert status_file.exists(), "Status file not created"
    
    with open(status_file) as f:
        status = json.load(f)
        assert status["completed_frames"] == 500, "Status file data incorrect"
    
    print(f"  ✓ Status file created and updated")
    
    # Cleanup
    status_file.unlink()
    
    print("✅ Progress Tracker tests passed!\n")


def test_render_queue():
    """Test render queue functionality."""
    print("Testing Render Queue...")
    
    queue = RenderQueue(queue_file="./test_queue.json")
    
    # Add jobs
    job1_config = {"video": "video1.json"}
    job2_config = {"video": "video2.json"}
    
    queue.add_job("job1", job1_config, priority=1)
    queue.add_job("job2", job2_config, priority=2)
    print(f"  ✓ Added 2 jobs to queue")
    
    # List jobs
    jobs = queue.list_jobs()
    assert len(jobs) == 2, "Wrong number of jobs"
    print(f"  ✓ Listed {len(jobs)} job(s)")
    
    # Get next job (should be job2 due to higher priority)
    next_job = queue.get_next_job()
    assert next_job is not None, "No job returned"
    assert next_job["id"] == "job2", "Wrong job priority"
    print(f"  ✓ Got next job: {next_job['id']}")
    
    # Update job status
    queue.update_job_status("job2", "completed")
    jobs = queue.list_jobs(status="completed")
    assert len(jobs) == 1, "Job status not updated"
    print(f"  ✓ Updated job status")
    
    # Clear completed
    queue.clear_completed()
    jobs = queue.list_jobs()
    assert len(jobs) == 1, "Completed jobs not cleared"
    print(f"  ✓ Cleared completed jobs")
    
    # Cleanup
    Path("./test_queue.json").unlink()
    
    print("✅ Render Queue tests passed!\n")


def test_performance_optimizer():
    """Test performance optimizer functionality."""
    print("Testing Performance Optimizer...")
    
    optimizer = PerformanceOptimizer(
        enable_multithreading=True,
        max_workers=4,
        enable_checkpoints=True,
        enable_preview=True,
        preview_scale=0.5
    )
    
    # Test preview config optimization
    config = {
        "output_width": 1920,
        "output_height": 1080,
        "quality": 18,
        "skip_rate": 8,
        "frame_rate": 30
    }
    
    preview_config = optimizer.optimize_config_for_preview(config)
    assert preview_config["output_width"] == 960, "Preview width incorrect"
    assert preview_config["output_height"] == 540, "Preview height incorrect"
    assert preview_config["quality"] >= 28, "Preview quality not reduced"
    print(f"  ✓ Optimized config for preview mode")
    print(f"    Resolution: {config['output_width']}x{config['output_height']} → {preview_config['output_width']}x{preview_config['output_height']}")
    print(f"    Quality: {config['quality']} → {preview_config['quality']}")
    
    # Test memory-efficient settings
    settings = optimizer.get_memory_efficient_settings(
        video_duration=60.0,
        resolution=(1920, 1080)
    )
    assert "use_streaming" in settings, "Memory settings missing"
    print(f"  ✓ Calculated memory-efficient settings")
    print(f"    Use streaming: {settings['use_streaming']}")
    print(f"    Suggested workers: {settings['suggested_workers']}")
    
    print("✅ Performance Optimizer tests passed!\n")


def test_quality_presets():
    """Test quality preset parsing."""
    print("Testing Quality Presets...")
    
    presets = ["preview", "draft", "standard", "high", "ultra"]
    
    for preset in presets:
        settings = parse_quality_preset(preset)
        assert "quality" in settings, f"Missing quality in {preset}"
        assert "scale" in settings, f"Missing scale in {preset}"
        print(f"  ✓ {preset:8s}: quality={settings['quality']}, scale={settings['scale']}, skip_rate={settings['skip_rate_multiplier']}x")
    
    print("✅ Quality Preset tests passed!\n")


def test_batch_config():
    """Test batch configuration loading."""
    print("Testing Batch Config...")
    
    # Create test config files
    test_configs = []
    for i in range(3):
        config_file = f"./test_config_{i}.json"
        config = {"video": f"video{i}.mp4", "duration": i + 1}
        
        with open(config_file, 'w') as f:
            json.dump(config, f)
        
        test_configs.append(config_file)
    
    # Load batch configs
    batch_configs = create_batch_config(test_configs)
    assert len(batch_configs) == 3, "Wrong number of configs loaded"
    print(f"  ✓ Loaded {len(batch_configs)} configurations")
    
    # Verify each config has source file
    for config in batch_configs:
        assert "_source_file" in config, "Source file not tracked"
    print(f"  ✓ Source files tracked")
    
    # Cleanup
    for config_file in test_configs:
        Path(config_file).unlink()
    
    print("✅ Batch Config tests passed!\n")


def main():
    """Run all tests."""
    print("="*60)
    print("Performance Optimizer Module Test Suite")
    print("="*60)
    print()
    
    try:
        test_checkpoint_manager()
        test_progress_tracker()
        test_render_queue()
        test_performance_optimizer()
        test_quality_presets()
        test_batch_config()
        
        print("="*60)
        print("✅ All tests passed successfully!")
        print("="*60)
        
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    finally:
        # Cleanup test directories
        import shutil
        for test_dir in ["./test_checkpoints"]:
            if Path(test_dir).exists():
                shutil.rmtree(test_dir)


if __name__ == "__main__":
    main()
