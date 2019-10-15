import click
from policy_sentry.shared.download import download_remote_policies


@click.command(
    short_help='Download remote IAM policies to a directory for use in the analyze-iam-policies command.'
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
    help='Download only policies that are attached.'
)
def download_policies(profile, aws_managed, include_unattached):
    """Download remote IAM policies to a directory for use in the analyze-iam-policies command."""
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
    download_remote_policies(profile, customer_managed, attached_only)
