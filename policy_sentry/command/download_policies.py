"""
Download IAM policies from live IAM accounts.
Specify a profile from the AWS Credentials file for a single download.
Alternatively, do a bulk download for all authenticated profiles within the aws credentials file.
"""
import logging
import click
from policy_sentry.shared.download import download_remote_policies, download_policies_recursively
from policy_sentry.shared.login import get_list_of_aws_profiles
from policy_sentry.shared.constants import DEFAULT_CREDENTIALS_FILE

logger = logging.getLogger()
handler = logging.StreamHandler()
formatter = logging.Formatter(
    '%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


@click.command(
    short_help='Download remote IAM policies to a directory for use in the analyze command.'
)
@click.option(
    '--recursive',
    default=False,
    is_flag=True,
    help='Use this flag to download *all* IAM policies from accounts listed in your AWS credentials file.'
)
@click.option(
    '--profile',
    type=str,
    default='default',
    help='To authenticate to AWS and analyze *all* existing IAM policies.'
)
@click.option(
    '--aws-managed',
    is_flag=True,
    default=False,
    help='Use flag if you want to download AWS Managed policies too.'
)
@click.option(
    '--include-unattached',
    is_flag=True,
    default=False,
    help='Download both attached and unattached policies.'
)
@click.option(
    '--quiet',
    default=False,
    is_flag=True
)
def download_policies(recursive, profile, aws_managed, include_unattached, quiet):
    """Download remote IAM policies to a directory for use in the analyze command."""
    if quiet:
        logger.setLevel(logging.WARNING)
    else:
        logger.setLevel(logging.INFO)
    # Consolidated these because we want the default to be attached policies only, with a boolean flag.
    # Only use the --include-unattached flag if you want to download those too.
    # Otherwise they would have to use a really long command every time.
    if include_unattached:
        attached_only = False
    else:
        attached_only = True
    # Consolidated these because we want the default to be customer managed, with a boolean flag.
    # Only include the --aws-managed flag if you want to do those too.
    if aws_managed:
        customer_managed = False
    else:
        customer_managed = True
    if recursive:
        profiles = get_list_of_aws_profiles(DEFAULT_CREDENTIALS_FILE)
        # if download:
        download_policies_recursively(profiles)
    else:
        download_remote_policies(
            profile, customer_managed, attached_only)
