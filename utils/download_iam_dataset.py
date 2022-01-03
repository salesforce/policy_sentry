"""
Functions for applying overrides to the iam-definitions.json file we downloaded.
"""

import sys
import os
import logging
from pathlib import Path
sys.path.append(str(Path(os.path.dirname(__file__)).parent))
from policy_sentry.shared.dataset import create_database
from policy_sentry.shared.constants import (
    BUNDLED_ACCESS_OVERRIDES_FILE,
    BUNDLED_DATA_DIRECTORY,
    BUNDLED_DATASTORE_FILE_PATH,
)

logger = logging.getLogger(__name__)  # pylint: disable=invalid-name

if __name__ == '__main__':
    print("Applying override YAML")
    print("Data store file path: " + str(BUNDLED_DATASTORE_FILE_PATH))

    print("Building the IAM database")
    create_database(BUNDLED_DATA_DIRECTORY, BUNDLED_ACCESS_OVERRIDES_FILE)

    print("Checking the size of the IAM database as a sanity check.")
    file_size = os.path.getsize(BUNDLED_DATASTORE_FILE_PATH)
    # 1 Megabyte == 1024*1024 Bytes
    file_size = file_size/(1024*1024)
    print(f"IAM Definition file size in MB: {file_size} MB")
    assert file_size > 5
