"""Methods related to overriding the AWS-provided Access Levels for the database."""
import os
import shutil
import logging
from policy_sentry.shared.constants import (
    CONFIG_DIRECTORY,
    BUNDLED_DATA_FILES,
    BUNDLED_ACCESS_OVERRIDES_FILE,
)
from policy_sentry.util.file import read_yaml_file, list_files_in_directory

logger = logging.getLogger(__name__)


def create_default_overrides_file():
    """
    Copies over the overrides file in the config directory

    Essentially:
    cp $MODULE_DIR/policy_sentry/shared/data/access-level-overrides.yml ~/policy_sentry/access-level-overrides.yml
    """
    file_list = list_files_in_directory(BUNDLED_DATA_FILES)

    for file in file_list:
        if file.endswith(".yml"):
            shutil.copy(os.path.join(BUNDLED_DATA_FILES, file), CONFIG_DIRECTORY)
            logger.debug("copying overrides file %s to %s", file, CONFIG_DIRECTORY)


def get_action_access_level_overrides_from_yml(
    service, access_level_overrides_file_path=None
):
    """
    Read the YML overrides file, which is formatted like:
    ['ec2']['permissions-management'][action_name].
    Since the AWS Documentation is sometimes outdated, we can use this YML file to
    override whatever they provide in their documentation.
    """
    if not access_level_overrides_file_path:
        access_level_overrides_file_path = BUNDLED_ACCESS_OVERRIDES_FILE
    cfg = read_yaml_file(access_level_overrides_file_path)
    if service in cfg:
        return cfg[service]
    else:
        return False
