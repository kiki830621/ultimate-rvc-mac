"""
Common definitions for modules in the Ultimate RVC project that
facilitate training voice models.
"""

from __future__ import annotations

from typing import Literal

from ultimate_rvc.core.exceptions import (
    Entity,
    GPUNotFoundError,
    NotProvidedError,
    UIMessage,
)
from ultimate_rvc.typing_extra import DeviceType


def get_gpu_info() -> list[tuple[str, int]]:
    """
    Retrieve information on locally available GPUs.

    Returns
    -------
    list[tuple[str, int]]
        A list of tuples containing the name and index of each locally
        available GPU.

    """
    # NOTE lazy importing does not work with torch so we import it here
    #  manually
    import torch  # noqa: PLC0415

    ngpu = torch.cuda.device_count()
    gpu_infos: list[tuple[str, int]] = []
    if torch.cuda.is_available() or ngpu != 0:
        for i in range(ngpu):
            gpu_name = torch.cuda.get_device_name(i)
            mem = int(
                torch.cuda.get_device_properties(i).total_memory / 1024 / 1024 / 1024  # type: ignore[ReportUnknownMembershipType]
                + 0.4,
            )
            gpu_infos.append((f"{gpu_name} ({mem} GB)", i))
    return gpu_infos


def validate_devices(
    device_type: DeviceType,
    device_ids: set[int] | None = None,
) -> tuple[Literal["cuda", "cpu"], set[int] | None]:
    """
    Validate the devices identified by the provided device type and
    device IDs.

    If the provided device type is AUTOMATIC, the first available GPU
    will be selected if available. Otherwise CPU will be selected.
    If the device type is GPU, then validation will be performed to
    ensure that at least one device ID is provided and that all device
    IDs point to available GPUs. If the device type is CPU, then no
    validation is performed.

    Parameters
    ----------
    device_type : DeviceType
        The type of devices to validate.
    device_ids : set[int], optional
        The IDs of the devices to validate when device type is GPU.

    Returns
    -------
        device_type : str
            The type of the selected devices.
        device_ids : set[int], optional
            The ids of the selected devices. Only returned when the
            device type is GPU or AUTOMATIC.

    Raises
    ------
    NotProvidedError
        If device type is GPU and no device IDs are provided.
    GPUNotFoundError
        If device type is GPU and a provided device ID does not point
        to an available GPU.


    """
    match device_type:
        case DeviceType.AUTOMATIC:
            gpu_info = get_gpu_info()
            if gpu_info:
                return "cuda", {gpu_info[0][1]}
            return "cpu", None
        case DeviceType.GPU:
            if not device_ids:
                raise NotProvidedError(Entity.GPU_IDS, UIMessage.NO_GPUS)
            validated_devices: list[int] = []
            available_ids = {i for _, i in get_gpu_info()}
            for device_id in device_ids:
                if device_id not in available_ids:
                    raise GPUNotFoundError(device_id)
                validated_devices.append(device_id)
            return "cuda", set(validated_devices)
        case DeviceType.CPU:
            return "cpu", None
