"""
Functions that relate to manipulating files, loading files, and managing filepaths.
"""
import json
import os.path
from os import listdir
from os.path import isfile, join

import yaml


def read_this_file(filename):
    """Read a file at a path and return the lines from each file"""
    lines = []

    with open(filename, 'r') as fileobj:
        for row in fileobj:
            # FIXME check for bad or unknown characters, we know this should be
            # in a standard format,
            lines.append(row.rstrip('\n'))
            # we should enforce it
    return lines


# FIXME as with the json files we should have a generic validation function, maybe it can read the file extension
# and then figure out what to do with it. I like what is going on here but where do you check to see if the file
# exists or validate the path?
def read_yaml_file(filename):
    """
    Description: Reads a YAML file, safe loads, and returns the dictionary
    :param filename: name of the yaml file
    :return: dictionary of YAML file contents
    """
    with open(filename, 'r') as yaml_file:
        try:
            cfg = yaml.safe_load(yaml_file)
        except yaml.YAMLError as exc:
            print(exc)
    return cfg


def check_valid_file_path(file):
    """
    Checks if the file path is valid.
    :param file: The file to check.
    :return: True if it exists, False if it does not
    """

    if os.path.exists(file):
        # print("Evaluating: " + file)
        return True
    else:
        print("File does not exist or is formatted incorrectly: " +
              file + "\nPlease provide a valid path.")
        return False


def write_json_file(filename, json_contents):
    """
    Description: Writes a YAML file
    :param json_contents: a dictionary used to build the JSON. This is the IAM Policy built by write_policy functions.
    :param filename: name of the yaml file, which should include the path
    """
    with open(filename, 'w') as file:
        # try:
        json.dump(json_contents, file, indent=4)
        # except yaml.YAMLError as exc:
        #     print(exc)
    # return filename


def list_files_in_directory(directory):
    """Equivalent of ls command, and return the list of files"""
    only_files = [f for f in listdir(directory) if isfile(join(directory, f))]
    return only_files


def create_directory_if_it_doesnt_exist(directory):
    """Equivalent of mkdir -p"""
    if os.path.exists(directory):
        pass
    else:
        os.mkdir(directory)


def get_list_of_service_prefixes_from_links_file():
    """
    Gets a list of service prefixes from the links file. Used for unit tests.
    :return:
    """
    links_yml_file = os.path.abspath(os.path.dirname(__file__)) + '/links.yml'
    service_prefixes = []
    with open(links_yml_file, 'r') as yaml_file:
        try:
            cfg = yaml.safe_load(yaml_file)
        except yaml.YAMLError as exc:
            print(exc)
    for service_name in cfg:
        service_prefixes.append(service_name)
    return service_prefixes
