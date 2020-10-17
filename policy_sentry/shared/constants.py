"""
Just a common storage space for storing some constants.
"""
from pathlib import Path
import os
import logging

logger = logging.getLogger()

# General Folders
HOME = str(Path.home())
CONFIG_DIRECTORY = os.path.join(HOME, ".policy_sentry")

# HTML Docs
BUNDLED_HTML_DIRECTORY_PATH = os.path.join(
    str(Path(os.path.dirname(__file__))), "data", "docs"
)
BUNDLED_DATA_DIRECTORY = os.path.join(str(Path(os.path.dirname(__file__))), "data")

LOCAL_HTML_DIRECTORY_PATH = os.path.join(CONFIG_DIRECTORY, "data", "docs")

BASE_DOCUMENTATION_URL = "https://docs.aws.amazon.com/service-authorization/latest/reference/reference_policies_actions-resources-contextkeys.html"
# BASE_DOCUMENTATION_URL = "https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_actions-resources-contextkeys.html"

# Data json file
# On initialization, load the IAM data
BUNDLED_DATASTORE_FILE_PATH = os.path.join(
    str(Path(os.path.dirname(__file__))), "data", "iam-definition.json"
)
LOCAL_DATASTORE_FILE_PATH = os.path.join(CONFIG_DIRECTORY, "iam-definition.json")
# Check for the existence of the local datastore first.
if os.path.exists(LOCAL_DATASTORE_FILE_PATH):
    # If it exists, leverage that datastore instead of the one bundled with the python package
    logger.info(f"Leveraging the local IAM definition at the path: {LOCAL_DATASTORE_FILE_PATH} "
                f"To leverage the bundled definition instead, remove the folder $HOME/.policy_sentry/")
    DATASTORE_FILE_PATH = LOCAL_DATASTORE_FILE_PATH
else:
    # Otherwise, leverage the datastore inside the python package
    logger.debug("Leveraging the bundled IAM Definition.")
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
