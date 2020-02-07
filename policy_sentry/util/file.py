"""
Functions that relate to manipulating files, loading files, and managing filepaths.
"""
import json
import logging
from os import listdir, makedirs
from os.path import isfile, join, exists
import yaml

logger = logging.getLogger(__name__)


def read_this_file(filename):
    """Read a file at a path and return the lines from each file"""
    lines = []

    with open(filename, "r") as fileobj:
        for row in fileobj:
            lines.append(row.rstrip("\n"))
    return lines


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


def check_valid_file_path(file):
    """
    Checks if the file path is valid.

    :param file: The file to check.
    :return: True if it exists, False if it does not
    :rtype: bool
    """

    if exists(file):
        return True
    else:
        logger.critical(
            "File does not exist or is formatted incorrectly: %s \nPlease provide a valid path.",
            file,
        )
        return False


def write_json_file(filename, json_contents):
    """
    Description: Writes a YAML file
    :param json_contents: a dictionary used to build the JSON. This is the IAM Policy built by write_policy functions.
    :param filename: name of the yaml file, which should include the path
    """
    with open(filename, "w") as file:
        # try:
        json.dump(json_contents, file, indent=4)
        # except yaml.YAMLError as exc:
        #     logger.critical(exc)
    # return filename


def list_files_in_directory(directory):
    """Equivalent of ls command, and return the list of files"""
    only_files = [f for f in listdir(directory) if isfile(join(directory, f))]
    return only_files


def create_directory_if_it_doesnt_exist(directory):
    """Equivalent of mkdir -p"""
    if exists(directory):
        pass
    else:
        makedirs(directory)
