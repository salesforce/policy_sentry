"""
Allow users to use specific pre-compiled queries against the action, arn, and condition tables from command line.
"""
import os
import json
import logging
import click
import click_log
import yaml
from policy_sentry.util.access_levels import transform_access_level_text
from policy_sentry.querying.all import get_all_service_prefixes
from policy_sentry.querying.arns import (
    get_arn_type_details,
    get_arn_types_for_service,
    get_raw_arns_for_service,
)
from policy_sentry.querying.actions import (
    get_actions_for_service,
    get_actions_with_access_level,
    get_action_data,
    get_actions_that_support_wildcard_arns_only,
    get_actions_matching_condition_key,
    get_actions_at_access_level_that_support_wildcard_arns_only,
)
from policy_sentry.querying.conditions import (
    get_condition_keys_for_service,
    get_condition_key_details,
)
from policy_sentry.shared.constants import DATASTORE_FILE_PATH, LOCAL_DATASTORE_FILE_PATH

logger = logging.getLogger(__name__)
click_log.basic_config(logger)
iam_definition_path = DATASTORE_FILE_PATH


@click.group()
def query():
    """Allow users to query the IAM tables from command line"""


@query.command(
    short_help="Query the action table based on access levels, conditions, or actions that only support wildcard "
    "resources."
)
@click.option(
    "--service", type=str, required=True, help="Filter according to AWS service."
)
@click.option(
    "--name",
    type=str,
    required=False,
    help='The name of IAM Action. For example, if the action is "iam:ListUsers", supply "ListUsers" here.',
)
@click.option(
    "--access-level",
    type=click.Choice(["read", "write", "list", "tagging", "permissions-management"]),
    required=False,
    help="Filter according to CRUD levels. "
    "Acceptable values are read, write, list, tagging, permissions-management",
)
@click.option(
    "--condition",
    type=str,
    required=False,
    help="Supply a condition key to show a list of all IAM actions that support the condition key.",
)
@click.option(
    "--wildcard-only",
    is_flag=True,
    required=False,
    help="Show the IAM actions that only support "
    "wildcard resources - i.e., cannot support ARNs in the resource block.",
)
@click.option(
    "--fmt",
    type=click.Choice(["yaml", "json"]),
    default="json",
    required=False,
    help='Format output as YAML or JSON. Defaults to "yaml"',
)
@click_log.simple_verbosity_option(logger)
def action_table(name, service, access_level, condition, wildcard_only, fmt):
    """Query the Action Table from the Policy Sentry database"""
    query_action_table(name, service, access_level, condition, wildcard_only, fmt)


def query_action_table(
    name, service, access_level, condition, wildcard_only, fmt="json"
):
    """Query the Action Table from the Policy Sentry database.
    Use this one when leveraging Policy Sentry as a library."""
    if os.path.exists(LOCAL_DATASTORE_FILE_PATH):
        logger.info(f"Using the Local IAM definition: {LOCAL_DATASTORE_FILE_PATH}. To leverage the bundled definition instead, remove the folder $HOME/.policy_sentry/")
    else:
        # Otherwise, leverage the datastore inside the python package
        logger.debug("Leveraging the bundled IAM Definition.")
    # Actions on all services
    if service == "all":
        all_services = get_all_service_prefixes()
        if access_level:
            level = transform_access_level_text(access_level)
            print(f"{access_level} actions across ALL services:\n")
            output = []
            for serv in all_services:
                result = get_actions_with_access_level(serv, level)
                output.extend(result)
            print(yaml.dump(output)) if fmt == "yaml" else [
                print(result) for result in output
            ]
        # Get a list of all services in the database
        else:
            print("All services in the database:\n")
            output = all_services
            print(yaml.dump(output)) if fmt == "yaml" else [
                print(item) for item in output
            ]
    elif name is None and access_level and not wildcard_only:
        print(
            f"All IAM actions under the {service} service that have the access level {access_level}:"
        )
        level = transform_access_level_text(access_level)
        output = get_actions_with_access_level(service, level)
        print(yaml.dump(output)) if fmt == "yaml" else [
            print(json.dumps(output, indent=4))
        ]
    elif name is None and access_level and wildcard_only:
        print(
            f"{service} {access_level.upper()} actions that must use wildcards in the resources block:"
        )
        access_level = transform_access_level_text(access_level)
        output = get_actions_at_access_level_that_support_wildcard_arns_only(
            service, access_level
        )
        print(yaml.dump(output)) if fmt == "yaml" else [
            print(json.dumps(output, indent=4))
        ]
    # Get a list of all IAM actions under the service that support the specified condition key.
    elif condition:
        print(
            f"IAM actions under {service} service that support the {condition} condition only:"
        )
        output = get_actions_matching_condition_key(service, condition)
        print(yaml.dump(output)) if fmt == "yaml" else [
            print(json.dumps(output, indent=4))
        ]
    # Get a list of IAM Actions under the service that only support resources = "*"
    # (i.e., you cannot restrict it according to ARN)
    elif wildcard_only:
        print(
            f"IAM actions under {service} service that support wildcard resource values only:"
        )
        output = get_actions_that_support_wildcard_arns_only(service)
        print(yaml.dump(output)) if fmt == "yaml" else [
            print(json.dumps(output, indent=4))
        ]
    elif name and access_level is None:
        output = get_action_data(service, name)
        print(yaml.dump(output)) if fmt == "yaml" else [
            print(json.dumps(output, indent=4))
        ]
    else:
        # Get a list of all IAM Actions available to the service
        output = get_actions_for_service(service)
        print(f"ALL {service} actions:")
        print(yaml.dump(output)) if fmt == "yaml" else [print(item) for item in output]
    return output


@query.command(
    short_help="Query the ARN table to show RAW ARNs, like `aws:s3:::bucket/object`. "
    "Use --list-arn-types ARN types, like `object`."
)
@click.option(
    "--service", type=str, required=True, help="Filter according to AWS service."
)
@click.option(
    "--name",
    type=str,
    required=False,
    help="The short name of the resource ARN type. For example, `bucket` under service `s3`.",
)
@click.option(
    "--list-arn-types",
    is_flag=True,
    required=False,
    help="Show the short names of ARN Types. If empty, this will show RAW ARNs only.",
)
@click.option(
    "--fmt",
    type=click.Choice(["yaml", "json"]),
    default="json",
    required=False,
    help='Format output as YAML or JSON. Defaults to "yaml"',
)
@click_log.simple_verbosity_option(logger)
def arn_table(name, service, list_arn_types, fmt="json"):
    """Query the ARN Table from the Policy Sentry database"""
    query_arn_table(name, service, list_arn_types, fmt)


def query_arn_table(name, service, list_arn_types, fmt):
    """Query the ARN Table from the Policy Sentry database. Use this one when leveraging Policy Sentry as a library."""
    if os.path.exists(LOCAL_DATASTORE_FILE_PATH):
        logger.info(f"Using the Local IAM definition: {LOCAL_DATASTORE_FILE_PATH}. To leverage the bundled definition instead, remove the folder $HOME/.policy_sentry/")
    else:
        # Otherwise, leverage the datastore inside the python package
        logger.debug("Leveraging the bundled IAM Definition.")
    # Get a list of all RAW ARN formats available through the service.
    if name is None and list_arn_types is False:
        output = get_raw_arns_for_service(service)
        print(yaml.dump(output)) if fmt == "yaml" else [print(item) for item in output]
    # Get a list of all the ARN types per service, paired with the RAW ARNs
    elif name is None and list_arn_types:
        output = get_arn_types_for_service(service)
        print(yaml.dump(output)) if fmt == "yaml" else [
            print(json.dumps(output, indent=4))
        ]
    # Get the raw ARN format for the `cloud9` service with the short name
    # `environment`
    else:
        output = get_arn_type_details(service, name)
        print(yaml.dump(output)) if fmt == "yaml" else [
            print(json.dumps(output, indent=4))
        ]
    return output


@query.command(short_help="Query the condition table.")
@click.option(
    "--name",
    type=str,
    required=False,
    help="Get details on a specific condition key. Leave this blank to get a list of all condition keys "
    "available to the service.",
)
@click.option(
    "--service", type=str, required=True, help="Filter according to AWS service."
)
@click.option(
    "--fmt",
    type=click.Choice(["yaml", "json"]),
    default="json",
    required=False,
    help='Format output as YAML or JSON. Defaults to "yaml"',
)
@click_log.simple_verbosity_option(logger)
def condition_table(name, service, fmt):
    """Query the condition table from the Policy Sentry database"""
    query_condition_table(name, service, fmt)


def query_condition_table(name, service, fmt="json"):
    """Query the condition table from the Policy Sentry database.
    Use this one when leveraging Policy Sentry as a library."""
    if os.path.exists(LOCAL_DATASTORE_FILE_PATH):
        logger.info(f"Using the Local IAM definition: {LOCAL_DATASTORE_FILE_PATH}. To leverage the bundled definition instead, remove the folder $HOME/.policy_sentry/")
    else:
        # Otherwise, leverage the datastore inside the python package
        logger.debug("Leveraging the bundled IAM Definition.")
    # Get a list of all condition keys available to the service
    if name is None:
        output = get_condition_keys_for_service(service)
        print(yaml.dump(output)) if fmt == "yaml" else [print(item) for item in output]
    # Get details on the specific condition key
    else:
        output = get_condition_key_details(service, name)
        print(yaml.dump(output)) if fmt == "yaml" else [
            print(json.dumps(output, indent=4))
        ]
    return output
