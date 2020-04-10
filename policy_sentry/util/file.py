"""
Functions that relate to manipulating files, loading files, and managing filepaths.
"""
import logging
import yaml

logger = logging.getLogger(__name__)


def read_yaml_file(filename):
    """
    Reads a YAML file, safe loads, and returns the dictionary

    :param filename: name of the yaml file
    :return: dictionary of YAML file contents
    """
    with open(filename, "r") as yaml_file:
        try:
            cfg = yaml.safe_load(yaml_file)
        except yaml.YAMLError as exc:
            logger.critical(exc)
    return cfg
