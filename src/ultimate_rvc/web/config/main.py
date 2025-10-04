"""
Module defining models for representing configuration settings for
UI tabs.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from functools import cached_property

from pydantic import BaseModel

from ultimate_rvc.typing_extra import SegmentSize, SeparationModel
from ultimate_rvc.web.config.component import (
    AnyComponentConfig,
    AudioConfig,
    CheckboxConfig,
    ComponentConfig,
    DropdownConfig,
    RadioConfig,
    SliderConfig,
)
from ultimate_rvc.web.config.tab import (
    SongGenerationConfig,
    SpeechGenerationConfig,
    TrainingConfig,
)

if TYPE_CHECKING:
    import gradio as gr


class SongIntermediateAudioConfig(BaseModel):
    """
    Configuration settings for intermediate audio components in the
    one-click song generation tab.

    Attributes
    ----------
    song : AudioConfig
        Configuration settings for the input song audio component.
    vocals : AudioConfig
        Configuration settings for the vocals audio component.
    instrumentals : AudioConfig
        Configuration settings for the instrumentals audio component.
    main_vocals : AudioConfig
        Configuration settings for the main vocals audio component.
    backup_vocals : AudioConfig
        Configuration settings for the backup vocals audio component.
    main_vocals_dereverbed : AudioConfig
        Configuration settings for the main vocals de-reverbed audio
        component.
    main_vocals_reverb : AudioConfig
        Configuration settings for the main vocals reverb audio
        component.
    converted_vocals : AudioConfig
        Configuration settings for the converted vocals audio
        component.
    postprocessed_vocals : AudioConfig
        Configuration settings for the postprocessed vocals audio
        component.
    instrumentals_shifted : AudioConfig
        Configuration settings for the shifted instrumentals audio
        component.
    backup_vocals_shifted : AudioConfig
        Configuration settings for the shifted backup vocals audio
        component.
    all : list[gr.Audio]
        List of instances of all intermediate audio components.

    """

    song: AudioConfig = AudioConfig.intermediate(label="Song")
    vocals: AudioConfig = AudioConfig.intermediate(label="Vocals")
    instrumentals: AudioConfig = AudioConfig.intermediate(
        label="Instrumentals",
    )
    main_vocals: AudioConfig = AudioConfig.intermediate(
        label="Main vocals",
    )
    backup_vocals: AudioConfig = AudioConfig.intermediate(
        label="Backup vocals",
    )
    main_vocals_dereverbed: AudioConfig = AudioConfig.intermediate(
        label="De-reverbed main vocals",
    )
    main_vocals_reverb: AudioConfig = AudioConfig.intermediate(
        label="Main vocals with reverb",
    )
    converted_vocals: AudioConfig = AudioConfig.intermediate(
        label="Converted vocals",
    )
    postprocessed_vocals: AudioConfig = AudioConfig.intermediate(
        label="Postprocessed vocals",
    )
    instrumentals_shifted: AudioConfig = AudioConfig.intermediate(
        label="Pitch-shifted instrumentals",
    )
    backup_vocals_shifted: AudioConfig = AudioConfig.intermediate(
        label="Pitch-shifted backup vocals",
    )

    @property
    def all(self) -> list[gr.Audio]:
        """
        Retrieve instances of all intermediate audio components
        in the one-click song generation tab.

        Returns
        -------
        list[gr.Audio]
            List of instances of all intermediate audio components in
            the one-click song generation tab.

        """
        # NOTE we are using self.__annotations__ to get the fields in
        # the order they are defined in the class
        return [getattr(self, field).instance for field in self.__annotations__]


class OneClickSongGenerationConfig(SongGenerationConfig):
    """
    Configuration settings for the one-click song generation tab.

    Attributes
    ----------
    n_octaves : SliderConfig
        Configuration settings for an octave pitch shift slider
        component.
    n_semitones : SliderConfig
        Configuration settings for a semitone pitch shift slider
        component.
    show_intermediate_audio : CheckboxConfig
        Configuration settings for a show intermediate audio checkbox
        component.
    intermediate_audio : SongIntermediateAudioConfig
        Configuration settings for intermediate audio components.

    See Also
    --------
    SongGenerationConfig
        Parent model defining common component configuration settings
        for song generation tabs.

    """

    n_octaves: SliderConfig = SliderConfig.octave_shift(
        label="Vocal pitch shift",
        info=(
            "The number of octaves to shift the pitch of the converted vocals by. Use 1"
            " for male-to-female and -1 for vice-versa."
        ),
    )

    n_semitones: SliderConfig = SliderConfig.semitone_shift(
        label="Overall pitch shift",
        info=(
            "The number of semi-tones to shift the pitch of the converted vocals,"
            " instrumentals and backup vocals by."
        ),
    )
    show_intermediate_audio: CheckboxConfig = CheckboxConfig(
        label="Show intermediate audio",
        info="Show intermediate audio tracks produced during song cover generation.",
        value=False,
        exclude_value=True,
    )
    intermediate_audio: SongIntermediateAudioConfig = SongIntermediateAudioConfig()


class SongInputAudioConfig(BaseModel):
    """
    Configuration settings for input audio components in the multi-step
    song generation tab.

    Attributes
    ----------
    audio : AudioConfig
        Configuration settings for the input audio component.
    vocals : AudioConfig
        Configuration settings for the vocals audio component.
    converted_vocals : AudioConfig
        Configuration settings for the converted vocals audio
        component.
    instrumentals : AudioConfig
        Configuration settings for the instrumentals audio
        component.
    backup_vocals : AudioConfig
        Configuration settings for the backup vocals audio
        component.
    main_vocals : AudioConfig
        Configuration settings for the main vocals audio
        component.
    shifted_instrumentals : AudioConfig
        Configuration settings for the shifted instrumentals audio
        component.
    shifted_backup_vocals : AudioConfig
        Configuration settings for the shifted backup vocals audio
        component.
    all : list[AudioConfig]
        List of configuration settings for all input audio
        components in the multi-step song generation tab.

    """

    audio: AudioConfig = AudioConfig.input(label="Audio")
    vocals: AudioConfig = AudioConfig.input(label="Vocals")
    converted_vocals: AudioConfig = AudioConfig.input(label="Vocals")
    instrumentals: AudioConfig = AudioConfig.input(label="Instrumentals")
    backup_vocals: AudioConfig = AudioConfig.input(label="Backup vocals")
    main_vocals: AudioConfig = AudioConfig.input(label="Main vocals")
    shifted_instrumentals: AudioConfig = AudioConfig.input(label="Instrumentals")
    shifted_backup_vocals: AudioConfig = AudioConfig.input(label="Backup vocals")

    @property
    def all(self) -> list[AudioConfig]:
        """
        Retrieve configuration settings for all input audio components
        in the multi-step song generation tab.

        Returns
        -------
        list[AudioConfig]
            List of configuration settings for all input audio
            components in the multi-step song generation tab.

        """
        return [getattr(self, field) for field in self.__annotations__]


class SongDirsConfig(BaseModel):
    """
    Configuration settings for song directory components in the
    multi-step song generation tab.

    Attributes
    ----------
    separate_audio : DropdownConfig
        Configuration settings for the song directory component
        for separating audio.
    convert_vocals : DropdownConfig
        Configuration settings for the song directory component
        for converting vocals.
    postprocess_vocals : DropdownConfig
        Configuration settings for the song directory component
        for postprocessing vocals.
    pitch_shift_background : DropdownConfig
        Configuration settings for the song directory component
        for pitch-shifting background audio.
    mix : DropdownConfig
        Configuration settings for the song directory component
        for mixing audio.
    all : list[gr.Dropdown]
        List of instances of all song directory components in the
        multi-step song generation tab.

    """

    separate_audio: DropdownConfig = DropdownConfig.song_dir()
    convert_vocals: DropdownConfig = DropdownConfig.song_dir()
    postprocess_vocals: DropdownConfig = DropdownConfig.song_dir()
    pitch_shift_background: DropdownConfig = DropdownConfig.song_dir()
    mix: DropdownConfig = DropdownConfig.song_dir()

    @property
    def all(self) -> list[gr.Dropdown]:
        """
        Retrieve instances of all song directory components in the
        multi-step song generation tab.

        Returns
        -------
        list[gr.Dropdown]
            List of instances of all song directory components in
            the multi-step song generation tab.

        """
        return [getattr(self, field).instance for field in self.__annotations__]


class MultiStepSongGenerationConfig(SongGenerationConfig):
    """
    Configuration settings for multi-step song generation tab.

    Attributes
    ----------
    separation_model : DropdownConfig
        Configuration settings for a separation model dropdown
        component.
    segment_size : RadioConfig
        Configuration settings for a segment size radio component.
    n_octaves : SliderConfig
        Configuration settings for an octave pitch shift slider
        component.
    n_semitones : SliderConfig
        Configuration settings for a semitone pitch shift slider
        component.
    n_semitones_instrumentals : SliderConfig
        Configuration settings for an instrumentals pitch shift slider
        component.
    n_semitones_backup_vocals : SliderConfig
        Configuration settings for a backup vocals pitch shift slider
        component.
    input_audio : SongInputAudioConfig
        Configuration settings for input audio components.
    song_dirs : SongDirsConfig
        Configuration settings for song directory components.

    See Also
    --------
    SongGenerationConfig
        Parent model defining common component configuration settings
        for song generation tabs.

    """

    separation_model: DropdownConfig = DropdownConfig(
        label="Separation model",
        info="The model to use for audio separation.",
        value=SeparationModel.UVR_MDX_NET_VOC_FT,
        choices=list(SeparationModel),
    )
    segment_size: RadioConfig = RadioConfig(
        label="Segment size",
        info=(
            "The size of the segments into which the audio is split. Using a larger"
            " size consumes more resources, but may give better results."
        ),
        value=SegmentSize.SEG_512,
        choices=list(SegmentSize),
    )
    n_octaves: SliderConfig = SliderConfig.octave_shift(
        label="Pitch shift (octaves)",
        info=(
            "The number of octaves to pitch-shift the converted voice by. Use 1 for"
            " male-to-female and -1 for vice-versa."
        ),
    )
    n_semitones: SliderConfig = SliderConfig.semitone_shift(
        label="Pitch shift (semi-tones)",
        info=(
            "The number of semi-tones to pitch-shift the converted vocals by. Altering"
            " this slightly reduces sound quality."
        ),
    )
    n_semitones_instrumentals: SliderConfig = SliderConfig.semitone_shift(
        label="Instrumental pitch shift",
        info="The number of semi-tones to pitch-shift the instrumentals by.",
    )
    n_semitones_backup_vocals: SliderConfig = SliderConfig.semitone_shift(
        label="Backup vocal pitch shift",
        info="The number of semi-tones to pitch-shift the backup vocals by.",
    )
    input_audio: SongInputAudioConfig = SongInputAudioConfig()
    song_dirs: SongDirsConfig = SongDirsConfig()


class SpeechIntermediateAudioConfig(BaseModel):
    """
    Configuration settings for intermediate audio components in the
    one-click speech generation tab.

    Attributes
    ----------
    speech : AudioConfig
        Configuration settings for the input speech audio component.
    converted_speech : AudioConfig
        Configuration settings for the converted speech audio component.
    all : list[gr.Audio]
        List of instances of all intermediate audio components in the
        speech generation tab.

    """

    speech: AudioConfig = AudioConfig.intermediate(label="Speech")
    converted_speech: AudioConfig = AudioConfig.intermediate(label="Converted speech")

    @property
    def all(self) -> list[gr.Audio]:
        """
        Retrieve instances of all intermediate audio components in the
        speech generation tab.

        Returns
        -------
        list[gr.Audio]
            List of instances of all intermediate audio components in
            the speech generation tab.

        """
        return [getattr(self, field).instance for field in self.__annotations__]


class OneClickSpeechGenerationConfig(SpeechGenerationConfig):
    """
    Configuration settings for one-click speech generation tab.

    Attributes
    ----------
    intermediate_audio : SpeechIntermediateAudioConfig
        Configuration settings for intermediate audio components.
    show_intermediate_audio : CheckboxConfig
        Configuration settings for a show intermediate audio checkbox
        component.

    See Also
    --------
    SpeechGenerationConfig
        Parent model defining common component configuration settings
        for speech generation tabs.

    """

    intermediate_audio: SpeechIntermediateAudioConfig = SpeechIntermediateAudioConfig()

    show_intermediate_audio: CheckboxConfig = CheckboxConfig(
        label="Show intermediate audio",
        info="Show intermediate audio tracks produced during speech generation.",
        value=False,
        exclude_value=True,
    )


class SpeechInputAudioConfig(BaseModel):
    """
    Configuration settings for input audio components in the multi-step
    speech generation tab.

    Attributes
    ----------
    speech : AudioConfig
        Configuration settings for the input speech audio component.
    converted_speech : AudioConfig
        Configuration settings for the converted speech audio component.

    all : list[AudioConfig]
        List of configuration settings for all input audio components in
        the multi-step speech generation tab.

    """

    speech: AudioConfig = AudioConfig.input("Speech")
    converted_speech: AudioConfig = AudioConfig.input("Converted speech")

    @property
    def all(self) -> list[AudioConfig]:
        """
        Retrieve configuration settings for all input audio components
        in the multi-step speech generation tab.

        Returns
        -------
        list[AudioConfig]
            List of configuration settings for all input audio
            components in the multi-step speech generation tab.

        """
        return [getattr(self, field) for field in self.__annotations__]


class MultiStepSpeechGenerationConfig(SpeechGenerationConfig):
    """
    Configuration settings for the multi-step speech generation tab.

    Attributes
    ----------
    input_audio : SpeechInputAudioConfig
        Configuration settings for input audio components.

    See Also
    --------
    SpeechGenerationConfig
        Parent model defining common component configuration settings
        for speech generation tabs.

    """

    input_audio: SpeechInputAudioConfig = SpeechInputAudioConfig()


class MultiStepTrainingConfig(TrainingConfig):
    """Configuration settings for multi-step training tab."""


class ModelManagementConfig(BaseModel):
    """

    Configuration settings for model management tab.

    Attributes
    ----------
    voices : DropdownConfig
        Configuration settings for delete voice models dropdown
        component.
    embedders : DropdownConfig
        Configuration settings for delete embedder models dropdown
        component.
    pretraineds : DropdownConfig
        Configuration settings for delete pretrained models dropdown
        component.
    traineds : DropdownConfig
        Configuration settings for delete training models dropdown
        component.
    dummy_checkbox : CheckboxConfig
        Configuration settings for a dummy checkbox component.

    """

    voices: DropdownConfig = DropdownConfig.multi_delete(
        label="Voice models",
        info="Select one or more voice models to delete.",
    )
    embedders: DropdownConfig = DropdownConfig.multi_delete(
        label="Custom embedder models",
        info="Select one or more embedder models to delete.",
    )
    pretraineds: DropdownConfig = DropdownConfig.multi_delete(
        label="Custom pretrained models",
        info="Select one or more pretrained models to delete.",
    )
    traineds: DropdownConfig = DropdownConfig.multi_delete(
        label="Training models",
        info="Select one or more training models to delete.",
    )

    dummy_checkbox: CheckboxConfig = CheckboxConfig(
        value=False,
        visible=False,
        exclude_value=True,
    )


class AudioManagementConfig(BaseModel):
    """
    Configuration settings for audio management tab.

    Attributes
    ----------
    intermediate : DropdownConfig
        Configuration settings for delete intermediate audio files
        dropdown component
    speech : DropdownConfig
        Configuration settings for delete speech audio files dropdown
        component.
    output : DropdownConfig
        Configuration settings for delete output audio files dropdown
        component.
    dataset : DropdownConfig
        Configuration settings for delete dataset audio files dropdown
        component.
    dummy_checkbox : CheckboxConfig
        Configuration settings for a dummy checkbox component.

    """

    intermediate: DropdownConfig = DropdownConfig.multi_delete(
        label="Song directories",
        info=(
            "Select one or more song directories containing intermediate audio files to"
            " delete."
        ),
    )
    speech: DropdownConfig = DropdownConfig.multi_delete(
        label="Speech audio files",
        info="Select one or more speech audio files to delete.",
    )
    output: DropdownConfig = DropdownConfig.multi_delete(
        label="Output audio files",
        info="Select one or more output audio files to delete.",
    )
    dataset: DropdownConfig = DropdownConfig.multi_delete(
        label="Dataset audio files",
        info="Select one or more datasets containing audio files to delete.",
    )

    dummy_checkbox: CheckboxConfig = CheckboxConfig(
        value=False,
        visible=False,
        exclude_value=True,
    )


class SettingsManagementConfig(BaseModel):
    """
    Configuration settings for settings management tab.

    Attributes
    ----------
    dummy_checkbox : CheckboxConfig
        Configuration settings for a dummy checkbox component.

    """

    load_config_name: DropdownConfig = DropdownConfig(
        label="Configuration name",
        info="The name of a configuration to load UI settings from",
        value=None,
        render=False,
        exclude_value=True,
    )
    delete_config_names: DropdownConfig = DropdownConfig.multi_delete(
        label="Configuration names",
        info="Select the name of one or more configurations to delete",
    )
    dummy_checkbox: CheckboxConfig = CheckboxConfig(
        value=False,
        visible=False,
        exclude_value=True,
    )


class TotalSongGenerationConfig(BaseModel):
    """
    All configuration settings for song generation tabs.

    Attributes
    ----------
    one_click : OneClickSongGenerationConfig
        Configuration settings for the one-click song generation tab.
    multi_step : MultiStepSongGenerationConfig
        Configuration settings for the multi-step song generation tab.

    """

    one_click: OneClickSongGenerationConfig = OneClickSongGenerationConfig()
    multi_step: MultiStepSongGenerationConfig = MultiStepSongGenerationConfig()


class TotalSpeechGenerationConfig(BaseModel):
    """
    All configuration settings for speech generation tabs.

    Attributes
    ----------
    one_click : OneClickSpeechGenerationConfig
        Configuration settings for the one-click speech generation tab.
    multi_step : MultiStepSpeechGenerationConfig
        Configuration settings for the multi-step speech generation tab.

    """

    one_click: OneClickSpeechGenerationConfig = OneClickSpeechGenerationConfig()
    multi_step: MultiStepSpeechGenerationConfig = MultiStepSpeechGenerationConfig()


class TotalTrainingConfig(BaseModel):
    """
    All configuration settings for training tabs.

    Attributes
    ----------
    training : TrainingConfig
        Configuration settings for the multi-step training tab.

    """

    multi_step: MultiStepTrainingConfig = MultiStepTrainingConfig()


class TotalManagementConfig(BaseModel):
    """
    All configuration settings for management tabs.

    Attributes
    ----------
    model : ModelManagementConfig
        Configuration settings for the model management tab.
    audio : AudioManagementConfig
        Configuration settings for the audio management tab.
    settings : SettingsManagementConfig
        Configuration settings for the settings management tab.

    """

    model: ModelManagementConfig = ModelManagementConfig()
    audio: AudioManagementConfig = AudioManagementConfig()
    settings: SettingsManagementConfig = SettingsManagementConfig()


class TotalConfig(BaseModel):
    """
    All configuration settings for the Ultimate RVC app.

    Attributes
    ----------
    song : TotalSongGenerationConfig
        Configuration settings for song generation tabs.
    speech : TotalSpeechGenerationConfig
        Configuration settings for speech generation tabs.
    training : TotalTrainingConfig
        Configuration settings for training tabs.
    management : TotalManagementConfig
        Configuration settings for management tabs.

    """

    song: TotalSongGenerationConfig = TotalSongGenerationConfig()
    speech: TotalSpeechGenerationConfig = TotalSpeechGenerationConfig()
    training: TotalTrainingConfig = TotalTrainingConfig()
    management: TotalManagementConfig = TotalManagementConfig()

    @cached_property
    def all(self) -> list[AnyComponentConfig]:
        """
        Recursively collect those component configuration models nested
        within the current model instance, which have values that are
        not excluded.

        Returns
        -------
        list[AnyComponentConfig]
            A list of component configuration models found within the
            current model instance, which have values that are not
            excluded.

        """

        def _collect(model: BaseModel) -> list[AnyComponentConfig]:
            component_configs: list[Any] = []
            for _, value in model:
                if isinstance(value, ComponentConfig):
                    if not value.exclude_value:
                        component_configs.append(value)
                elif isinstance(value, BaseModel):
                    component_configs.extend(_collect(value))
            return component_configs

        return _collect(self)
