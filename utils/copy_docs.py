"""Helper script for integration tests"""

import shutil

from policy_sentry.shared.constants import BUNDLED_HTML_DIRECTORY_PATH, LOCAL_HTML_DIRECTORY_PATH

if __name__ == "__main__":
    LOCAL_HTML_DIRECTORY_PATH.mkdir(parents=True, exist_ok=True)
    shutil.copytree(BUNDLED_HTML_DIRECTORY_PATH, LOCAL_HTML_DIRECTORY_PATH, dirs_exist_ok=True)
