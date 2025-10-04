"""
Module which defines extra types for the web application of the Ultimate
RVC project.
"""

from __future__ import annotations

from typing import Any, TypedDict

from collections.abc import Callable, Sequence
from enum import StrEnum, auto

type AnyCallable = Callable[..., Any]

type BaseDropdownChoices = Sequence[str | int | float | tuple[str, str | int | float]]
type DropdownChoices = BaseDropdownChoices | None
type BaseDropdownValue = str | int | float | Sequence[str | int | float] | None
type DropdownValue = BaseDropdownValue | AnyCallable

type RadioChoices = DropdownChoices
type BaseRadioValue = str | int | float | None
type RadioValue = BaseRadioValue | AnyCallable


class ConcurrencyId(StrEnum):
    """Enumeration of possible concurrency identifiers."""

    GPU = auto()


class SongSourceType(StrEnum):
    """The type of source providing the song to generate a cover of."""

    PATH = "YouTube link/local path"
    LOCAL_FILE = "Local file"
    CACHED_SONG = "Cached song"


class SpeechSourceType(StrEnum):
    """The type of source providing the text to generate speech from."""

    TEXT = "Text"
    LOCAL_FILE = "Local file"


class SongTransferOption(StrEnum):
    """Enumeration of possible song transfer options."""

    STEP_1_AUDIO = "Step 1: audio"
    STEP_2_VOCALS = "Step 2: vocals"
    STEP_3_VOCALS = "Step 3: vocals"
    STEP_4_INSTRUMENTALS = "Step 4: instrumentals"
    STEP_4_BACKUP_VOCALS = "Step 4: backup vocals"
    STEP_5_MAIN_VOCALS = "Step 5: main vocals"
    STEP_5_INSTRUMENTALS = "Step 5: instrumentals"
    STEP_5_BACKUP_VOCALS = "Step 5: backup vocals"


class SpeechTransferOption(StrEnum):
    """Enumeration of possible speech transfer options."""

    STEP_2_SPEECH = "Step 2: speech"
    STEP_3_SPEECH = "Step 3: speech"


class ComponentVisibilityKwArgs(TypedDict, total=False):
    """
    Keyword arguments for setting component visibility.

    Attributes
    ----------
    visible : bool
        Whether the component should be visible.
    value : Any
        The value of the component.

    """

    visible: bool
    value: Any


class UpdateDropdownKwArgs(TypedDict, total=False):
    """
    Keyword arguments for updating a dropdown component.

    Attributes
    ----------
    choices : DropdownChoices
        The updated choices for the dropdown component.
    value : DropdownValue
        The updated value for the dropdown component.

    """

    choices: DropdownChoices
    value: DropdownValue


class TextBoxKwArgs(TypedDict, total=False):
    """
    Keyword arguments for updating a textbox component.

    Attributes
    ----------
    value : str | None
        The updated value for the textbox component.
    placeholder : str | None
        The updated placeholder for the textbox component.

    """

    value: str | None
    placeholder: str | None


class UpdateAudioKwArgs(TypedDict, total=False):
    """
    Keyword arguments for updating an audio component.

    Attributes
    ----------
    value : str | None
        The updated value for the audio component.

    """

    value: str | None


class DatasetType(StrEnum):
    """The type of dataset to train a voice model."""

    NEW_DATASET = "New dataset"
    EXISTING_DATASET = "Existing dataset"
