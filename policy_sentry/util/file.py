"""
Functions that relate to manipulating files, loading files, and managing filepaths.
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any, cast

import yaml

logger = logging.getLogger(__name__)


def read_yaml_file(filename: str | Path) -> dict[str, Any]:
    """
    Reads a YAML file, safe loads, and returns the dictionary

    :param filename: name of the yaml file
    :return: dictionary of YAML file contents
    :raises yaml.YAMLError: when the file contains invalid YAML
    :raises ValueError: when the document root is not a mapping
    """
    with Path(filename).open(encoding="utf-8") as yaml_file:
        try:
            cfg = yaml.safe_load(yaml_file)
        except yaml.YAMLError as exc:
            logger.critical(exc)
            raise

    if not isinstance(cfg, dict):
        raise ValueError(
            f"YAML file {filename} must contain a mapping at the root, "
            f"got {type(cfg).__name__}"
        )
    return cast("dict[str, Any]", cfg)
