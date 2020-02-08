"""
Given a directory of Policy Sentry YML template files, write least-privilege IAM Policies in CRUD mode or Actions mode.
"""
import sys
import os.path
import logging
import glob
import click
from policy_sentry.shared.database import connect_db
from policy_sentry.command.write_policy import write_policy_with_template
from policy_sentry.util.file import (
    read_yaml_file,
    write_json_file,
    check_valid_file_path,
)
from policy_sentry.util.logging import set_log_level
from policy_sentry.shared.constants import DATABASE_FILE_PATH

logger = logging.getLogger()


@click.command(
    short_help="Same as write-policy, but with an input directory of YML files, "
    "and an output directory for the JSON files."
)
@click.option(
    "--input-dir",
    type=str,
    required=True,
    help="Relative path to Input directory that contains policy_sentry .yaml files (CRUD mode only)",
)
@click.option(
    "--output-dir",
    type=str,
    required=True,
    help="Relative path to directory to store AWS JSON policies",
)
@click.option(
    "--minimize",
    required=False,
    type=int,
    help="Minimize the resulting statement with *safe* usage of wildcards to reduce policy length. Set this to the character length you want - for example, 4",
)
@click.option(
    "--log-level",
    help="Set the logging level. Choices are CRITICAL, ERROR, WARNING, INFO, or DEBUG. Defaults to INFO.",
    type=click.Choice(["CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG"]),
    default="INFO",
)
def write_policy_dir(input_dir, output_dir, minimize, log_level):
    """
    write_policy, but this time with an input directory of YML/YAML files, and an output directory for all the JSON files
    """
    set_log_level(logger, log_level)

    db_session = connect_db(DATABASE_FILE_PATH)
    input_dir = os.path.abspath(input_dir)
    output_dir = os.path.abspath(output_dir)

    if not minimize:
        logger.warning(
            "Note: --minimize option is not set. If the policy is too large, "
            "it can hit the AWS IAM Policy character limit. "
            "We'll execute as-is, but try using `--minimize 0` functionality "
            "for production to optimize policy size.\n"
        )
    # Construct the path
    # Get the list of files
    # Write a list of the names
    if not check_valid_file_path(input_dir):
        logger.critical("Input directory is invalid")
        sys.exit()
    if not check_valid_file_path(output_dir):
        logger.critical("Output directory is invalid")
        sys.exit()

    input_files = glob.glob(str(input_dir + "/*.yml"), recursive=False)
    if not input_files:
        logger.critical(
            "Directory is empty or does not have files with *.yml extension. "
            "Please check the folder contents and/or extension spelling."
        )

    logger.info(
        "Writing the policy JSON files from %s to %s...\n", input_dir, output_dir
    )
    for yaml_file in input_files:
        # Get the name of the file, and strip the extension. This is what the
        # policy name will be
        base_name = os.path.basename(yaml_file)
        base_name_no_extension = os.path.splitext(os.path.basename(yaml_file))[0]
        cfg = read_yaml_file(yaml_file)
        policy = write_policy_with_template(db_session, cfg, minimize)
        logger.info("Writing policy for %s\n", base_name)

        target_file = str(output_dir + "/" + base_name_no_extension + ".json")
        if os.path.exists(target_file):
            logger.info(
                "Target file for %s.json exists in the target directory. "
                "Removing it and writing a new file.\n",
                target_file,
            )
            os.remove(target_file)
        write_json_file(target_file, policy)

    logger.info("Finished")
