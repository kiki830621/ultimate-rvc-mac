"""Extra type definitions for the `ultimate_rvc.rvc.infer` package."""

from typing import TypedDict


class ConvertAudioKwArgs(TypedDict, total=False):
    """Keyword arguments for the `convert_audio` function."""

    # pre-processing arguments
    formant_shifting: bool
    formant_qfrency: float
    formant_timbre: float
    # reverb post-processing arguments
    reverb: bool
    reverb_room_size: float
    reverb_damping: float
    reverb_wet_level: float
    reverb_dry_level: float
    reverb_width: float
    reverb_freeze_mode: int
    # pitch shift post-processing arguments
    pitch_shift: bool
    pitch_shift_semitones: int
    # limiter post-processing arguments
    limiter: bool
    limiter_threshold: float
    limiter_release: float
    # gain post-processing arguments
    gain: bool
    gain_db: int
    # distortion post-processing arguments
    distortion: bool
    distortion_gain: int
    # chorus post-processing arguments
    chorus: bool
    chorus_rate: float
    chorus_depth: float
    chorus_delay: int
    chorus_feedback: float
    chorus_mix: float
    # bitcrush post-processing arguments
    bitcrush: bool
    bitcrush_bit_depth: int
    # clipping post-processing arguments
    clipping: bool
    clipping_threshold: int
    # compressor post-processing arguments
    compressor: bool
    compressor_threshold: int
    compressor_ratio: int
    compressor_attack: float
    compressor_release: int
    # delay post-processing arguments
    delay: bool
    delay_seconds: float
    delay_feedback: float
    delay_mix: float
