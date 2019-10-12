import click
from policy_sentry.shared.download import download_remote_policies


@click.command()
@click.option(
    '--profile',
    type=str,
    default='default',
    help='To authenticate to AWS and analyze *all* existing IAM policies.'
)
def download_policies(profile):
    """Download remote IAM policies to a directory for use in the analyze-iam-policies command."""
    download_remote_policies(profile)
