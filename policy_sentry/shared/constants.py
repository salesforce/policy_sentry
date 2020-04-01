"""
Just a common storage space for storing some constants.
"""
from pathlib import Path
import os

# General Folders
HOME = str(Path.home())
# CONFIG_DIRECTORY = "/.policy_sentry/"
CONFIG_DIRECTORY = os.path.join(HOME, ".policy_sentry")

# HTML Docs
BUNDLED_HTML_DIRECTORY_PATH = os.path.join(
    str(Path(os.path.dirname(__file__))), "data", "docs"
)
# LOCAL_HTML_DIRECTORY_PATH = HOME + CONFIG_DIRECTORY + HTML_DATA_DIRECTORY_SUBFOLDER
LOCAL_HTML_DIRECTORY_PATH = os.path.join(CONFIG_DIRECTORY, "data", "docs")

BASE_DOCUMENTATION_URL = "https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_actions-resources-contextkeys.partial.html"

# The path for the service prefixes <=> links YML file
LOCAL_LINKS_YML_FILE = os.path.join(CONFIG_DIRECTORY, "links.yml")

# The one in this directory - i.e., in the code repository
BUNDLED_LINKS_YML_FILE = os.path.join(
    os.path.abspath(os.path.dirname(__file__)), "data", "links.yml"
)

# Database
BUNDLED_DATABASE_FILE_PATH = os.path.join(
    str(Path(os.path.dirname(__file__))), "data", "aws.sqlite3"
)

LOCAL_DATABASE_FILE_PATH = os.path.join(CONFIG_DIRECTORY, "aws.sqlite3")

# If the local directory exists, use that one. Otherwise, use the bundled database so the user doesn't
# have to run the initialize command, unless they want to.
if os.path.exists(LOCAL_DATABASE_FILE_PATH):
    DATABASE_FILE_PATH = LOCAL_DATABASE_FILE_PATH
else:
    DATABASE_FILE_PATH = BUNDLED_DATABASE_FILE_PATH

BUNDLED_ACCESS_OVERRIDES_FILE = os.path.join(
    os.path.abspath(os.path.dirname(__file__)), "data", "access-level-overrides.yml"
)

LOCAL_ACCESS_OVERRIDES_FILE = os.path.join(
    CONFIG_DIRECTORY, "access-level-overrides.yml"
)

BUNDLED_DATA_FILES = os.path.join(os.path.abspath(os.path.dirname(__file__)), "data")

# Policy constants
# https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_elements_version.html
POLICY_LANGUAGE_VERSION = "2012-10-17"
