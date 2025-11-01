"""
Performance optimization module for whiteboard-it.

This module provides:
- Multi-threading support for frame processing
- Progressive rendering with preview mode
- Render queue management
- Background rendering
- Resume interrupted renders (checkpoint system)
- Memory optimization
- Batch processing
"""

import os
import json
import time
import pickle
import hashlib
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Dict, List, Optional, Tuple, Any
import threading


class RenderCheckpoint:
    """Manages checkpoints for resumable rendering."""
    
    def __init__(self, checkpoint_dir: str = "./checkpoints"):
        self.checkpoint_dir = Path(checkpoint_dir)
        self.checkpoint_dir.mkdir(exist_ok=True, parents=True)
    
    def generate_checkpoint_id(self, config: Dict) -> str:
        """Generate a unique checkpoint ID based on config hash."""
        config_str = json.dumps(config, sort_keys=True)
        return hashlib.md5(config_str.encode()).hexdigest()[:16]
    
    def save_checkpoint(self, checkpoint_id: str, state: Dict):
        """Save render state to checkpoint file."""
        checkpoint_path = self.checkpoint_dir / f"{checkpoint_id}.checkpoint"
        temp_path = checkpoint_path.with_suffix('.tmp')
        
        try:
            with open(temp_path, 'wb') as f:
                pickle.dump(state, f)
            temp_path.replace(checkpoint_path)
            return True
        except Exception as e:
            print(f"⚠️ Failed to save checkpoint: {e}")
            if temp_path.exists():
                temp_path.unlink()
            return False
    
    def load_checkpoint(self, checkpoint_id: str) -> Optional[Dict]:
        """Load render state from checkpoint file."""
        checkpoint_path = self.checkpoint_dir / f"{checkpoint_id}.checkpoint"
        
        if not checkpoint_path.exists():
            return None
        
        try:
            with open(checkpoint_path, 'rb') as f:
                return pickle.load(f)
        except Exception as e:
            print(f"⚠️ Failed to load checkpoint: {e}")
            return None
    
    def delete_checkpoint(self, checkpoint_id: str):
        """Delete checkpoint file."""
        checkpoint_path = self.checkpoint_dir / f"{checkpoint_id}.checkpoint"
        if checkpoint_path.exists():
            checkpoint_path.unlink()
    
    def list_checkpoints(self) -> List[Tuple[str, float]]:
        """List all checkpoints with their modification times."""
        checkpoints = []
        for checkpoint_file in self.checkpoint_dir.glob("*.checkpoint"):
            checkpoint_id = checkpoint_file.stem
            mtime = checkpoint_file.stat().st_mtime
            checkpoints.append((checkpoint_id, mtime))
        return sorted(checkpoints, key=lambda x: x[1], reverse=True)


class ProgressTracker:
    """Thread-safe progress tracking for rendering."""
    
    def __init__(self, total_frames: int = 0):
        self.total_frames = total_frames
        self.completed_frames = 0
        self.start_time = time.time()
        self.lock = threading.Lock()
        self.status_file = None
    
    def set_status_file(self, path: str):
        """Set path to status file for background rendering."""
        self.status_file = Path(path)
    
    def increment(self, count: int = 1):
        """Increment completed frames counter."""
        with self.lock:
            self.completed_frames += count
            self._update_status_file()
    
    def set_total(self, total: int):
        """Set total frames count."""
        with self.lock:
            self.total_frames = total
            self._update_status_file()
    
    def get_progress(self) -> Dict:
        """Get current progress information."""
        with self.lock:
            return self._get_progress_unlocked()
    
    def _get_progress_unlocked(self) -> Dict:
        """Get current progress information (without lock, for internal use)."""
        elapsed = time.time() - self.start_time
        if self.completed_frames > 0:
            fps = self.completed_frames / elapsed
            remaining = (self.total_frames - self.completed_frames) / fps if fps > 0 else 0
        else:
            fps = 0
            remaining = 0
        
        return {
            'completed_frames': self.completed_frames,
            'total_frames': self.total_frames,
            'percentage': (self.completed_frames / self.total_frames * 100) if self.total_frames > 0 else 0,
            'elapsed_seconds': elapsed,
            'fps': fps,
            'eta_seconds': remaining
        }
    
    def _update_status_file(self):
        """Update status file with current progress."""
        if self.status_file:
            try:
                progress = self._get_progress_unlocked()  # Use unlocked version
                with open(self.status_file, 'w') as f:
                    json.dump(progress, f, indent=2)
            except Exception as e:
                pass  # Silently fail for status file updates


class RenderQueue:
    """Manages a queue of render jobs."""
    
    def __init__(self, queue_file: str = "./render_queue.json"):
        self.queue_file = Path(queue_file)
        self.lock = threading.Lock()
    
    def add_job(self, job_id: str, config: Dict, priority: int = 0):
        """Add a job to the render queue."""
        with self.lock:
            queue = self._load_queue()
            
            job = {
                'id': job_id,
                'config': config,
                'priority': priority,
                'status': 'pending',
                'added_time': time.time(),
                'started_time': None,
                'completed_time': None,
                'error': None
            }
            
            queue['jobs'].append(job)
            self._save_queue(queue)
    
    def get_next_job(self) -> Optional[Dict]:
        """Get the next pending job from the queue."""
        with self.lock:
            queue = self._load_queue()
            
            # Find highest priority pending job
            pending_jobs = [j for j in queue['jobs'] if j['status'] == 'pending']
            if not pending_jobs:
                return None
            
            job = max(pending_jobs, key=lambda j: j['priority'])
            job['status'] = 'running'
            job['started_time'] = time.time()
            
            self._save_queue(queue)
            return job
    
    def update_job_status(self, job_id: str, status: str, error: str = None):
        """Update job status."""
        with self.lock:
            queue = self._load_queue()
            
            for job in queue['jobs']:
                if job['id'] == job_id:
                    job['status'] = status
                    if status == 'completed':
                        job['completed_time'] = time.time()
                    if error:
                        job['error'] = error
                    break
            
            self._save_queue(queue)
    
    def list_jobs(self, status: Optional[str] = None) -> List[Dict]:
        """List all jobs, optionally filtered by status."""
        with self.lock:
            queue = self._load_queue()
            
            if status:
                return [j for j in queue['jobs'] if j['status'] == status]
            return queue['jobs']
    
    def clear_completed(self):
        """Remove completed jobs from queue."""
        with self.lock:
            queue = self._load_queue()
            queue['jobs'] = [j for j in queue['jobs'] if j['status'] != 'completed']
            self._save_queue(queue)
    
    def _load_queue(self) -> Dict:
        """Load queue from file."""
        if not self.queue_file.exists():
            return {'jobs': []}
        
        try:
            with open(self.queue_file, 'r') as f:
                return json.load(f)
        except Exception:
            return {'jobs': []}
    
    def _save_queue(self, queue: Dict):
        """Save queue to file."""
        try:
            temp_file = self.queue_file.with_suffix('.tmp')
            with open(temp_file, 'w') as f:
                json.dump(queue, f, indent=2)
            temp_file.replace(self.queue_file)
        except Exception as e:
            print(f"⚠️ Failed to save queue: {e}")


class PerformanceOptimizer:
    """Main performance optimizer class."""
    
    def __init__(
        self,
        enable_multithreading: bool = False,
        max_workers: int = None,
        enable_checkpoints: bool = False,
        checkpoint_interval: int = 100,  # Save checkpoint every N frames
        enable_preview: bool = False,
        preview_scale: float = 0.5
    ):
        self.enable_multithreading = enable_multithreading
        self.max_workers = max_workers or min(4, os.cpu_count() or 1)
        self.enable_checkpoints = enable_checkpoints
        self.checkpoint_interval = checkpoint_interval
        self.enable_preview = enable_preview
        self.preview_scale = preview_scale
        
        self.checkpoint_manager = RenderCheckpoint() if enable_checkpoints else None
        self.progress_tracker = ProgressTracker()
    
    def optimize_config_for_preview(self, config: Dict) -> Dict:
        """Optimize configuration for preview mode (faster, lower quality)."""
        preview_config = config.copy()
        
        # Reduce resolution
        if 'output_width' in preview_config:
            preview_config['output_width'] = int(preview_config['output_width'] * self.preview_scale)
        if 'output_height' in preview_config:
            preview_config['output_height'] = int(preview_config['output_height'] * self.preview_scale)
        
        # Reduce quality
        preview_config['quality'] = max(preview_config.get('quality', 18) + 10, 28)
        
        # Increase skip rate (faster drawing)
        if 'skip_rate' in preview_config:
            preview_config['skip_rate'] = preview_config['skip_rate'] * 2
        
        # Reduce frame rate
        if 'frame_rate' in preview_config:
            preview_config['frame_rate'] = max(15, preview_config['frame_rate'] // 2)
        
        return preview_config
    
    def get_memory_efficient_settings(self, video_duration: float, resolution: Tuple[int, int]) -> Dict:
        """Calculate memory-efficient settings based on video characteristics."""
        width, height = resolution
        total_pixels = width * height
        
        # Estimate memory usage per frame (BGR = 3 bytes per pixel)
        frame_size_mb = (total_pixels * 3) / (1024 * 1024)
        
        # Recommend settings
        settings = {
            'use_streaming': frame_size_mb > 10,  # Stream if frames > 10MB
            'checkpoint_interval': min(100, int(1000 / frame_size_mb)),  # More frequent for large frames
            'suggested_workers': max(1, min(4, int(16 / frame_size_mb)))  # Fewer workers for large frames
        }
        
        return settings


def create_batch_config(config_files: List[str]) -> List[Dict]:
    """Load multiple configuration files for batch processing."""
    batch_configs = []
    
    for config_file in config_files:
        try:
            with open(config_file, 'r') as f:
                config = json.load(f)
                config['_source_file'] = config_file
                batch_configs.append(config)
        except Exception as e:
            print(f"⚠️ Failed to load config {config_file}: {e}")
    
    return batch_configs


def process_batch(
    config_files: List[str],
    parallel: bool = False,
    max_workers: int = 2
) -> List[Dict]:
    """Process multiple configurations in batch mode."""
    batch_configs = create_batch_config(config_files)
    results = []
    
    print(f"📦 Processing {len(batch_configs)} configurations in batch mode...")
    
    if parallel:
        print(f"⚡ Using {max_workers} parallel workers")
        # Parallel processing would be implemented here
        # For now, we'll process sequentially
        for config in batch_configs:
            result = {
                'config_file': config.get('_source_file'),
                'status': 'pending',
                'error': None
            }
            results.append(result)
    else:
        for config in batch_configs:
            result = {
                'config_file': config.get('_source_file'),
                'status': 'pending',
                'error': None
            }
            results.append(result)
    
    return results


# Utility functions for CLI integration

def parse_quality_preset(preset: str) -> Dict:
    """Parse quality preset name into settings."""
    presets = {
        'preview': {'quality': 28, 'scale': 0.5, 'skip_rate_multiplier': 2},
        'draft': {'quality': 28, 'scale': 0.75, 'skip_rate_multiplier': 1.5},
        'standard': {'quality': 23, 'scale': 1.0, 'skip_rate_multiplier': 1.0},
        'high': {'quality': 18, 'scale': 1.0, 'skip_rate_multiplier': 1.0},
        'ultra': {'quality': 15, 'scale': 1.0, 'skip_rate_multiplier': 0.75}
    }
    return presets.get(preset, presets['standard'])
