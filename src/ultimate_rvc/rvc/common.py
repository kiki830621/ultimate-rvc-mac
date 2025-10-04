"""Common constants and functions for the RVC package."""

from __future__ import annotations

from pathlib import Path

RVC_DIR = Path(__file__).resolve().parent
RVC_CONFIGS_DIR = RVC_DIR / "configs"
RVC_TRAINING_MODELS_DIR = RVC_DIR / "train" / "models"
