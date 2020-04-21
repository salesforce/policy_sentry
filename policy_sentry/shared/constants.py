"""
Just a common storage space for storing some constants.
"""
from pathlib import Path
import os

# General Folders
HOME = str(Path.home())
CONFIG_DIRECTORY = os.path.join(HOME, ".policy_sentry")

# HTML Docs
BUNDLED_HTML_DIRECTORY_PATH = os.path.join(
    str(Path(os.path.dirname(__file__))), "data", "docs"
)
BUNDLED_DATA_DIRECTORY = os.path.join(str(Path(os.path.dirname(__file__))), "data")

LOCAL_HTML_DIRECTORY_PATH = os.path.join(CONFIG_DIRECTORY, "data", "docs")

BASE_DOCUMENTATION_URL = "https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_actions-resources-contextkeys.html"

# Data json file
BUNDLED_DATASTORE_FILE_PATH = os.path.join(
    str(Path(os.path.dirname(__file__))), "data", "iam-definition.json"
)
LOCAL_DATASTORE_FILE_PATH = os.path.join(CONFIG_DIRECTORY, "iam-definition.json")
if os.path.exists(LOCAL_DATASTORE_FILE_PATH):
    DATASTORE_FILE_PATH = LOCAL_DATASTORE_FILE_PATH
else:
    DATASTORE_FILE_PATH = BUNDLED_DATASTORE_FILE_PATH

# Overrides
BUNDLED_ACCESS_OVERRIDES_FILE = os.path.join(
    os.path.abspath(os.path.dirname(__file__)), "data", "access-level-overrides.yml"
)

LOCAL_ACCESS_OVERRIDES_FILE = os.path.join(
    CONFIG_DIRECTORY, "access-level-overrides.yml"
)

# Policy constants
# https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_elements_version.html
POLICY_LANGUAGE_VERSION = "2012-10-17"
