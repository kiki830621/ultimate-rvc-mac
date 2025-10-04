"""Module which defines functions to manage configuration files."""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar

from pathlib import Path

from ultimate_rvc.common import CONFIG_DIR
from ultimate_rvc.core.common import json_dump, json_load
from ultimate_rvc.core.exceptions import (
    ConfigExistsError,
    ConfigNotFoundError,
    Entity,
    NotProvidedError,
    UIMessage,
)
from ultimate_rvc.core.manage.common import delete_directory, get_items

if TYPE_CHECKING:
    from collections.abc import Sequence

from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


def get_config_names() -> list[str]:
    """
    Get the names of all configuration files.

    Returns
    -------
    list[str]
        A list containing the names of all configuration files.


    """
    return get_items(CONFIG_DIR)


def load_config(name: str, config_class: type[T]) -> T:  # noqa: UP047
    """
    Load a configuration from a JSON file into a Pydantic model.

    Parameters
    ----------
    name: str
        The name of the configuration to load.
    config_class: type[T]
        The class of pydantic model to load the configuration into.


    Returns
    -------
    T
        The Pydantic model containing the configuration.

    Raises
    ------
    NotProvidedError
        If no name is provided for the configuration to load.
    ConfigNotFoundError
        If a configuration with the provided name does not exist.

    """
    if not name:
        raise NotProvidedError(entity=Entity.CONFIG_NAME)
    name = name.strip()
    file_path = CONFIG_DIR / f"{name}.json"
    if not file_path.is_file():
        raise ConfigNotFoundError(name=name)
    config_data = json_load(file_path)
    return config_class.model_validate(config_data)


def save_config(name: str, model: BaseModel) -> None:
    """
    Save a configuration to a JSON file.

    Parameters
    ----------
    name : str
        The name of the configuration to save.
    model : Config
        The Pydantic model containing the configuration to save.

    Raises
    ------
    NotProvidedError
        If no name is provided for the configuration to save.
    ConfigExistsError
        If a configuration with the provided name already exists.

    """
    if not name:
        raise NotProvidedError(entity=Entity.CONFIG_NAME)

    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    name = name.strip()
    config_path = CONFIG_DIR / f"{name}.json"
    if config_path.is_file():
        raise ConfigExistsError(name=name)
    json_dump(model.model_dump(), config_path)


def delete_configs(names: Sequence[str]) -> None:
    """
    Delete the configurations with the provided names.

    Parameters
    ----------
    names : Sequence[str]
        Names of the configurations to delete.

    Raises
    ------
    NotProvidedError
        If no names of items are provided.
    ConfigNotFoundError
        If a configuration with a provided name does not exist.

    """
    if not names:
        raise NotProvidedError(entity=Entity.CONFIG_NAMES, ui_msg=UIMessage.NO_CONFIG)
    config_file_paths: list[Path] = []
    for name in names:
        stripped_name = name.strip()
        config_file_path = Path(CONFIG_DIR) / f"{stripped_name}.json"
        if not config_file_path.is_file():
            raise ConfigNotFoundError(name=stripped_name)
        config_file_paths.append(config_file_path)
    for config_file_path in config_file_paths:
        config_file_path.unlink()


def delete_all_configs() -> None:
    """Delete all configuration files."""
    delete_directory(CONFIG_DIR)
