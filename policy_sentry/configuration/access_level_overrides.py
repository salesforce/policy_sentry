"""Methods related to overriding the AWS-provided Access Levels for the database."""
from os.path import dirname, join
import shutil
import logging
from pathlib import Path
from policy_sentry.shared.constants import HOME, CONFIG_DIRECTORY
from policy_sentry.util.file import read_yaml_file, list_files_in_directory

logger = logging.getLogger(__name__)


def create_default_overrides_file():
    """
    Copies over the overrides file in the config directory

    Essentially:
    cp $MODULE_DIR/policy_sentry/shared/data/access-level-overrides.yml ~/policy_sentry/access-level-overrides.yml
    """
    # existing_overrides_file_directory = os.path.abspath(
    #     dirname(__file__)) + '/data/'
    existing_overrides_file_directory = join(
        str(Path(dirname(__file__)).parent) + "/shared/data/"
    )
    file_list = list_files_in_directory(existing_overrides_file_directory)

    source = existing_overrides_file_directory
    destination = HOME + CONFIG_DIRECTORY + "/"
    for file in file_list:
        if file.endswith(".yml"):
            shutil.copy(source + "/" + file, destination)
            logger.debug("copying overrides file %s to %s", file, destination)


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
        access_level_overrides_file_path = (
            join(Path(dirname(__file__)).parent)
            + "/shared/data/access-level-overrides.yml"
        )
    cfg = read_yaml_file(access_level_overrides_file_path)
    if service in cfg:
        return cfg[service]
    else:
        return False
