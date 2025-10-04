"""
Module which defines functions for initializing the core of the Ultimate
RVC project.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import lazy_loader as lazy

from pathlib import Path

from rich import print as rprint

from ultimate_rvc.common import VOICE_MODELS_DIR
from ultimate_rvc.core.common import FLAG_FILE
from ultimate_rvc.core.generate.song_cover import initialize_audio_separator
from ultimate_rvc.core.manage.models import download_voice_model
from ultimate_rvc.rvc.lib.tools.prerequisites_download import (
    prequisites_download_pipeline,
)

if TYPE_CHECKING:
    import static_sox

else:
    static_sox = lazy.load("static_sox")


def download_sample_models() -> None:
    """Download sample RVC models."""
    named_model_links = [
        (
            "https://huggingface.co/damnedraxx/TaylorSwift/resolve/main/TaylorSwift.zip",
            "Taylor Swift",
        ),
        (
            "https://huggingface.co/Vermiculos/balladjames/resolve/main/Ballad%20James.zip?download=true",
            "James Hetfield",
        ),
        ("https://huggingface.co/ryolez/MMLP/resolve/main/MMLP.zip", "Eminem"),
    ]
    for model_url, model_name in named_model_links:
        if not Path(VOICE_MODELS_DIR / model_name).is_dir():
            rprint(f"Downloading {model_name}...")
            try:
                download_voice_model(model_url, model_name)
            except Exception as e:  # noqa: BLE001
                rprint(f"Failed to download {model_name}: {e}")


def initialize() -> None:
    """Initialize the Ultimate RVC project."""
    prequisites_download_pipeline(exe=False)
    if not FLAG_FILE.is_file():
        # NOTE we only add_paths so that sox
        # binaries are downloaded as part of initialization.
        static_sox.add_paths(weak=True)
        download_sample_models()
        initialize_audio_separator()
        FLAG_FILE.touch()


if __name__ == "__main__":
    initialize()
