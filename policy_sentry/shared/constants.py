"""
Just a common storage space for storing some constants.
"""
from pathlib import Path
from os.path import abspath, dirname, exists

# General Folders
HOME = str(Path.home())
CONFIG_DIRECTORY = "/.policy_sentry/"

# HTML Docs
HTML_DATA_DIRECTORY_SUBFOLDER = "/data/docs/"
HTML_DIRECTORY_PATH = HOME + CONFIG_DIRECTORY + HTML_DATA_DIRECTORY_SUBFOLDER
BASE_DOCUMENTATION_URL = "https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_actions-resources-contextkeys.partial.html"

# The path for the service prefixes <=> links YML file
LINKS_YML_FILE_LOCAL = HOME + CONFIG_DIRECTORY + "links.yml"
# The one in this directory - i.e., in the code repository
LINKS_YML_FILE_IN_PACKAGE = abspath(dirname(__file__)) + "/data/links.yml"

# Database
BUNDLED_DATABASE_FILE_PATH = (
    str(Path(dirname(__file__)).parent) + "/shared/data/" + "aws.sqlite3"
)
DATABASE_FILE_NAME = "aws.sqlite3"

# If the local directory exists, use that one. Otherwise, use the bundled database so the user doesn't
# have to run the initialize command, unless they want to.
if exists(HOME + CONFIG_DIRECTORY + DATABASE_FILE_NAME):
    DATABASE_FILE_PATH = HOME + CONFIG_DIRECTORY + DATABASE_FILE_NAME
else:
    DATABASE_FILE_PATH = BUNDLED_DATABASE_FILE_PATH

DEFAULT_ACCESS_OVERRIDES_FILE = (
    abspath(dirname(__file__)) + "/data/access-level-overrides.yml"
)

# Policy constants
# https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_elements_version.html
POLICY_LANGUAGE_VERSION = "2012-10-17"
