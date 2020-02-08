"""
Given a Policy Sentry YML template, write a least-privilege IAM Policy in CRUD mode or Actions mode.
"""
import sys
import json
import logging
import yaml
import click
from policy_sentry.util.logging import set_log_level
from policy_sentry.shared.constants import DATABASE_FILE_PATH
from policy_sentry.shared.database import connect_db
from policy_sentry.util.file import read_yaml_file
from policy_sentry.writing.sid_group import SidGroup

logger = logging.getLogger()


@click.command(
    short_help="Write least-privilege IAM policies, restricting all actions to resource ARNs."
)
# pylint: disable=duplicate-code
@click.option(
    "--input-file",
    type=str,
    # required=True,
    help="Path of the YAML File used for generating policies",
)
@click.option(
    "--minimize",
    required=False,
    type=int,
    help="Minimize the resulting statement with *safe* usage of wildcards to reduce policy length. "
    "Set this to the character length you want - for example, 4",
)
@click.option(
    "--log-level",
    help="Set the logging level. Choices are CRITICAL, ERROR, WARNING, INFO, or DEBUG. Defaults to INFO.",
    type=click.Choice(["CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG"]),
    default="INFO",
)
def write_policy(input_file, minimize, log_level):
    """
    Write a least-privilege IAM Policy by supplying either a list of actions or
    access levels specific to resource ARNs!
    """
    set_log_level(logger, log_level)

    db_session = connect_db(DATABASE_FILE_PATH)

    if input_file:
        cfg = read_yaml_file(input_file)
    else:
        try:
            cfg = yaml.safe_load(sys.stdin)
        except yaml.YAMLError as exc:
            logger.critical(exc)
            sys.exit()
    policy = write_policy_with_template(db_session, cfg, minimize)
    print(json.dumps(policy, indent=4))
    #
    # if input_file:
    #     cfg = read_yaml_file(input_file)
    # else:
    #     try:
    #         cfg = yaml.safe_load(sys.stdin)
    #     except yaml.YAMLError as exc:
    #         logger.critical(exc)
    #         sys.exit()
    #
    # # User supplies file containing resource-specific access levels
    # sid_group = SidGroup()
    # policy = sid_group.process_template(db_session, cfg, minimize)
    # print(json.dumps(policy, indent=4))


def write_policy_with_template(db_session, cfg, minimize=None):
    """
    This function is called by write-policy so the config can be passed in as a dict without running into a Click-related error. Use this function, rather than the write-policy function, if you are using Policy Sentry as a python library.

    :param db_session: SQL Alchemy database session object
    :param cfg: The loaded YAML as a dict. Must follow Policy Sentry dictated format.
    :param minimize: Minimize the resulting statement with *safe* usage of wildcards to reduce policy length. Set this to the character length you want - for example, 0, or 4. Defaults to none.
    """
    sid_group = SidGroup()
    policy = sid_group.process_template(db_session, cfg, minimize)
    return policy
