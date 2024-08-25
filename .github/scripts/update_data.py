from pathlib import Path

from policy_sentry.shared import constants

CONFIG_DIRECTORY = Path("/tmp/.policy_sentry")

constants.CONFIG_DIRECTORY = CONFIG_DIRECTORY
constants.LOCAL_DATASTORE_FILE_PATH = CONFIG_DIRECTORY / "iam-definition.json"
constants.LOCAL_ACCESS_OVERRIDES_FILE = CONFIG_DIRECTORY / "access-level-overrides.yml"
constants.LOCAL_HTML_DIRECTORY_PATH = CONFIG_DIRECTORY / "data/docs"

from policy_sentry.command.initialize import initialize

if __name__ == "__main__":
    initialize(None, True, True)
