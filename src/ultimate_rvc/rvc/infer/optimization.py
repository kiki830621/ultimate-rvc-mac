"""
Optimization utilities for RVC inference on Apple Silicon and other platforms.

This module provides optimization flags and utilities for:
- GPU tensor persistence (avoiding CPU-GPU transfers)
- Mixed precision inference (float16)
- Batch processing
- Performance profiling
"""

import os
from dataclasses import dataclass
from typing import Literal


@dataclass
class OptimizationConfig:
    """Configuration for RVC inference optimizations."""

    # GPU Optimization
    use_gpu_retrieval: bool = True  # Use GPU-based feature retrieval (15-25% speedup)
    use_fp16: bool = False  # Mixed precision inference (5-15% speedup, may affect quality)

    # Audio Processing
    use_gpu_filter: bool = False  # GPU-based filtering (currently experimental)

    # Batch Processing
    batch_size: int = 1  # Batch multiple audio segments (1 = no batching)

    # Device Selection
    device: Literal['auto', 'mps', 'cuda', 'cpu'] = 'auto'

    # Performance Profiling
    enable_profiling: bool = False  # Log detailed performance metrics

    @classmethod
    def from_env(cls) -> 'OptimizationConfig':
        """Create configuration from environment variables."""
        return cls(
            use_gpu_retrieval=os.getenv('RVC_GPU_RETRIEVAL', 'true').lower() == 'true',
            use_fp16=os.getenv('RVC_USE_FP16', 'false').lower() == 'true',
            use_gpu_filter=os.getenv('RVC_GPU_FILTER', 'false').lower() == 'true',
            batch_size=int(os.getenv('RVC_BATCH_SIZE', '1')),
            device=os.getenv('RVC_DEVICE', 'auto'),
            enable_profiling=os.getenv('RVC_PROFILING', 'false').lower() == 'true',
        )

    @classmethod
    def for_apple_silicon(cls) -> 'OptimizationConfig':
        """Optimized configuration for Apple Silicon (M1/M2/M3/M4)."""
        return cls(
            use_gpu_retrieval=True,
            use_fp16=False,  # Limited benefit on MPS
            use_gpu_filter=False,  # Experimental
            batch_size=1,
            device='mps',
            enable_profiling=False,
        )

    @classmethod
    def for_nvidia_gpu(cls) -> 'OptimizationConfig':
        """Optimized configuration for NVIDIA GPU (CUDA)."""
        return cls(
            use_gpu_retrieval=True,
            use_fp16=True,  # Good speedup on CUDA
            use_gpu_filter=True,
            batch_size=4,  # Higher batch size for CUDA
            device='cuda',
            enable_profiling=False,
        )

    @classmethod
    def for_cpu(cls) -> 'OptimizationConfig':
        """Configuration for CPU-only inference."""
        return cls(
            use_gpu_retrieval=False,
            use_fp16=False,
            use_gpu_filter=False,
            batch_size=1,
            device='cpu',
            enable_profiling=False,
        )


def get_default_config() -> OptimizationConfig:
    """
    Get the default optimization configuration based on available hardware.

    Returns:
        OptimizationConfig: Optimized configuration for current hardware
    """
    import torch

    if torch.backends.mps.is_available():
        return OptimizationConfig.for_apple_silicon()
    elif torch.cuda.is_available():
        return OptimizationConfig.for_nvidia_gpu()
    else:
        return OptimizationConfig.for_cpu()


# Performance profiling utilities
class PerformanceProfiler:
    """Simple performance profiler for RVC inference."""

    def __init__(self, enabled: bool = False):
        self.enabled = enabled
        self.metrics = {}

    def start(self, name: str):
        """Start timing a operation."""
        if self.enabled:
            import time
            if name not in self.metrics:
                self.metrics[name] = {'times': [], 'start': None}
            self.metrics[name]['start'] = time.perf_counter()

    def end(self, name: str):
        """End timing a operation."""
        if self.enabled and name in self.metrics:
            import time
            elapsed = time.perf_counter() - self.metrics[name]['start']
            self.metrics[name]['times'].append(elapsed)

    def report(self) -> str:
        """Generate performance report."""
        if not self.enabled or not self.metrics:
            return "Profiling not enabled or no metrics collected."

        lines = ["=== Performance Report ==="]
        for name, data in self.metrics.items():
            times = data['times']
            if times:
                avg_time = sum(times) / len(times)
                min_time = min(times)
                max_time = max(times)
                lines.append(
                    f"{name}: avg={avg_time*1000:.2f}ms, "
                    f"min={min_time*1000:.2f}ms, "
                    f"max={max_time*1000:.2f}ms, "
                    f"count={len(times)}"
                )

        return "\n".join(lines)
