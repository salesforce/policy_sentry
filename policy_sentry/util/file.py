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
    """
    with open(filename) as yaml_file:
        try:
            cfg = cast("dict[str, Any]", yaml.safe_load(yaml_file))
        except yaml.YAMLError as exc:
            logger.critical(exc)
    return cfg
