import os

from ultimate_rvc.common import PRETRAINED_MODELS_DIR


def pretrained_selector(vocoder: str, sample_rate: int) -> tuple[str, str]:
    base_path = os.path.join(PRETRAINED_MODELS_DIR, f"{vocoder.lower()}")

    path_g = os.path.join(base_path, f"f0G{str(sample_rate)[:2]}k.pth")
    path_d = os.path.join(base_path, f"f0D{str(sample_rate)[:2]}k.pth")

    if os.path.exists(path_g) and os.path.exists(path_d):
        return path_g, path_d
    return "", ""
