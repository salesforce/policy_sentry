"""
Given a Policy Sentry YML template, write a least-privilege IAM Policy in CRUD mode or Actions mode.
"""
import sys
import json
import logging
import yaml
import click
from policy_sentry.shared.constants import DATABASE_FILE_PATH
from policy_sentry.shared.database import connect_db
from policy_sentry.util.file import read_yaml_file
from policy_sentry.writing.sid_group import SidGroup

logger = logging.getLogger()
handler = logging.StreamHandler()
formatter = logging.Formatter(
    '%(name)-12s %(levelname)-8s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


@click.command(
    short_help='Write least-privilege IAM policies, restricting all actions to resource ARNs.'
)
# pylint: disable=duplicate-code
@click.option(
    '--input-file',
    type=str,
    # required=True,
    help='Path of the YAML File used for generating policies'
)
@click.option(
    '--minimize',
    required=False,
    type=int,
    help='Minimize the resulting statement with *safe* usage of wildcards to reduce policy length. '
         'Set this to the character length you want - for example, 4'
)
@click.option(
    '--quiet',
    help='Set the logging level to WARNING instead of INFO.',
    default=False,
    is_flag=True
)
def write_policy(input_file, minimize, quiet):
    """
    Write a least-privilege IAM Policy by supplying either a list of actions or
    access levels specific to resource ARNs!
    """
    if quiet:
        logger.setLevel(logging.WARNING)
    else:
        logger.setLevel(logging.INFO)
    db_session = connect_db(DATABASE_FILE_PATH)

    if input_file:
        cfg = read_yaml_file(input_file)
    else:
        try:
            cfg = yaml.safe_load(sys.stdin)
        except yaml.YAMLError as exc:
            logger.critical(exc)
            sys.exit()
    write_policy_with_template(db_session, cfg, minimize)
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
    sid_group = SidGroup()
    policy = sid_group.process_template(db_session, cfg, minimize)
    print(json.dumps(policy, indent=4))
    return policy
