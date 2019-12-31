"""
Just a common storage space for storing some constants.
"""
from pathlib import Path
from os.path import abspath, dirname
# General Folders
HOME = str(Path.home())
CONFIG_DIRECTORY = '/.policy_sentry/'
ANALYSIS_DIRECTORY_NAME = 'analysis'
ANALYSIS_DIRECTORY_PATH = HOME + CONFIG_DIRECTORY + ANALYSIS_DIRECTORY_NAME

# HTML Docs
HTML_DATA_DIRECTORY_SUBFOLDER = '/data/docs/'
HTML_DIRECTORY_PATH = HOME + CONFIG_DIRECTORY + HTML_DATA_DIRECTORY_SUBFOLDER
BASE_DOCUMENTATION_URL = \
    "https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_actions-resources-contextkeys.partial.html"

# The path for the service prefixes <=> links YML file
LINKS_YML_FILE_LOCAL = HOME + CONFIG_DIRECTORY + 'links.yml'
# The one in this directory - i.e., in the code repository
LINKS_YML_FILE_IN_PACKAGE = abspath(dirname(__file__)) + '/data/links.yml'

# Database
DATABASE_FILE_NAME = 'aws.sqlite3'
DATABASE_FILE_PATH = HOME + CONFIG_DIRECTORY + DATABASE_FILE_NAME

# Boto3
DEFAULT_CREDENTIALS_FILE = HOME + '/.aws/credentials'

# Policy constants
# https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_elements_version.html
POLICY_LANGUAGE_VERSION = "2012-10-17"

# Audit functionality constants
AUDIT_DIRECTORY_FOLDER = 'audit/'
AUDIT_DIRECTORY_PATH = HOME + CONFIG_DIRECTORY + AUDIT_DIRECTORY_FOLDER
DEFAULT_AUDIT_FILE_NAME = '/privilege-escalation.txt'
DEFAULT_AUDIT_FILE_PATH = AUDIT_DIRECTORY_PATH + DEFAULT_AUDIT_FILE_NAME
