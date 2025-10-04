"""Module defining models for representing UI event configurations."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, PrivateAttr

from gradio.events import Dependency  # noqa: TC002

from ultimate_rvc.core.exceptions import EventNotInstantiatedError


class ClickEvent(BaseModel):
    """
    Model which represents a click event for a button in the UI.

    Attributes
    ----------
    _instance : Dependency | None
        Internal attribute storing the click event instance.
        Will be null until a click event is assigned manually.
    instance : Dependency
        The click event instance. Attempting to access this field
        before manually assigning a click event will raise an
        EventNotInstantiatedError.

    """

    _instance: Dependency | None = PrivateAttr(default=None)
    model_config = ConfigDict(arbitrary_types_allowed=True)

    @property
    def instance(self) -> Dependency:
        """
        Retrieve the click event instance.

        Returns
        -------
        Dependency
            The click event instance.

        Raises
        ------
        EventNotInstantiatedError
            If the click event instance has not been assigned yet.

        """
        if self._instance is None:
            raise EventNotInstantiatedError
        return self._instance

    @instance.setter
    def instance(self, value: Dependency) -> None:
        self._instance = value


class ManageAudioEventState(BaseModel):
    """
    Event state of the audio management tab.

    Attributes
    ----------
    delete_intermediate_click: ClickEvent
        Click event for deleting intermediate audio files.
    delete_all_intermediate_click: ClickEvent
        Click event for deleting all intermediate audio files.
    delete_speech_click: ClickEvent
        Click event for deleting speech audio files.
    delete_all_speech_click: ClickEvent
        Click event for deleting all speech audio files.
    delete_output_click: ClickEvent
        Click event for deleting output audio files.
    delete_all_output_click: ClickEvent
        Click event for deleting all output audio files.
    delete_dataset_click: ClickEvent
        Click event for deleting dataset audio files.
    delete_all_dataset_click: ClickEvent
        Click event for deleting all dataset audio files.
    delete_all_click: ClickEvent
        Click event for deleting all audio files.

    """

    delete_intermediate_click: ClickEvent = ClickEvent()
    delete_all_intermediate_click: ClickEvent = ClickEvent()
    delete_speech_click: ClickEvent = ClickEvent()
    delete_all_speech_click: ClickEvent = ClickEvent()
    delete_output_click: ClickEvent = ClickEvent()
    delete_all_output_click: ClickEvent = ClickEvent()
    delete_dataset_click: ClickEvent = ClickEvent()
    delete_all_dataset_click: ClickEvent = ClickEvent()
    delete_all_click: ClickEvent = ClickEvent()


class ManageModelEventState(BaseModel):
    """
    Event state of the model management tab.

    Attributes
    ----------
    download_voice_click: ClickEvent
        Click event for downloading voice models.
    upload_voice_click: ClickEvent
        Click event for uploading voice models.
    download_pretrained_click: ClickEvent
        Click event for downloading pretrained models.
    upload_embedder_click: ClickEvent
        Click event for uploading embedder models.
    delete_voice_click: ClickEvent
        Click event for deleting voice models.
    delete_all_voices_click: ClickEvent
        Click event for deleting all voice models.
    delete_embedder_click: ClickEvent
        Click event for deleting embedder models.
    delete_all_embedders_click: ClickEvent
        Click event for deleting all embedder models.
    delete_pretrained_click: ClickEvent
        Click event for deleting pretrained models.
    delete_all_pretraineds_click: ClickEvent
        Click event for deleting all pretrained models.
    delete_trained_click: ClickEvent
        Click event for deleting training models.
    delete_all_trained_click: ClickEvent
        Click event for deleting all training models.
    delete_all_click: ClickEvent
        Click event for deleting all models.

    """

    download_voice_click: ClickEvent = ClickEvent()
    upload_voice_click: ClickEvent = ClickEvent()
    download_pretrained_click: ClickEvent = ClickEvent()
    upload_embedder_click: ClickEvent = ClickEvent()

    delete_voice_click: ClickEvent = ClickEvent()
    delete_all_voices_click: ClickEvent = ClickEvent()
    delete_embedder_click: ClickEvent = ClickEvent()
    delete_all_embedders_click: ClickEvent = ClickEvent()
    delete_pretrained_click: ClickEvent = ClickEvent()
    delete_all_pretraineds_click: ClickEvent = ClickEvent()
    delete_trained_click: ClickEvent = ClickEvent()
    delete_all_trained_click: ClickEvent = ClickEvent()
    delete_all_click: ClickEvent = ClickEvent()
