from pathlib import Path
import sys
from glob import glob
import json
import click
import os
from policy_sentry.shared.download import download_remote_policies, download_policies_recursively
import markdown
from policy_sentry.shared.login import get_list_of_aws_profiles
from policy_sentry.shared.analyze import analyze_policy_directory
from policy_sentry.shared.database import connect_db
from policy_sentry.shared.report import create_markdown_report_template, load_report_config_file, create_csv_report, \
    create_json_report, create_markdown_report
from policy_sentry.shared.finding import Findings
from policy_sentry.shared.constants import HOME, CONFIG_DIRECTORY, DEFAULT_CREDENTIALS_FILE, DATABASE_FILE_PATH, \
    AUDIT_DIRECTORY_PATH, ANALYSIS_DIRECTORY_PATH

# Audit filenames
credentials_exposure_filename = AUDIT_DIRECTORY_PATH + '/credentials-exposure.txt'
data_access_filename = AUDIT_DIRECTORY_PATH + '/data-access-arn-list.txt'
privilege_escalation_filename = AUDIT_DIRECTORY_PATH + '/privilege-escalation.txt'
network_exposure_filename = AUDIT_DIRECTORY_PATH + '/network-exposure.txt'
resource_exposure_filename = AUDIT_DIRECTORY_PATH + '/resource-exposure.txt'
# data_access_arn_list_filename = AUDIT_DIRECTORY_PATH + '/data-access-arn-list.txt'

@click.command(
    short_help='Download customer-managed policies from all accounts in credentials file and generate a report.'
)
@click.option(
    '--credentials-file',
    default=DEFAULT_CREDENTIALS_FILE,
    help='Path to the AWS Credentials file. Defaults to ~/.aws/credentials.'
)
@click.option(
    '--download',
    is_flag=True,
    default=False,
    help='Path to the AWS Credentials file. Defaults to ~/.aws/credentials.'
)
@click.option(
    '--include-unattached',
    is_flag=True,
    default=False,
    help='Download both attached and unattached policies.'
)
@click.option(
    '--report-config',
    default=False,
    help='Custom report configuration file. Contains policy name exclusions and custom risk score weighting.'
)
@click.option(
    '--output',
    default='report',
    help='Report file location. Defaults to ./report/'
)
def generate_report(credentials_file, download, output, report_config, include_unattached):
    """Download remote IAM policies to a directory for use in the analyze-iam-policies command."""
    # Consolidated these because we want the default to be attached policies only, with a boolean flag.
    # Only use the --include-unattached flag if you want to download those too.
    # Otherwise they would have to use a really long command every time.
    if include_unattached:
        attached_only = False
    else:
        attached_only = True
    # Only evaluate customer managed policies
    customer_managed = True
    profiles = get_list_of_aws_profiles(credentials_file)
    # if download:
    # download_directories = download_policies_recursively(credentials_file, profiles)

    base_account_directories = glob(HOME + CONFIG_DIRECTORY + 'policy-analysis/' + '*/')
    account_policy_directories = []

    for i in range(len(base_account_directories)):
        account_policy_directories.append(base_account_directories[i] + 'customer-managed/')
    db_session = connect_db(DATABASE_FILE_PATH)

    # Get report config
    report_config = load_report_config_file(HOME + CONFIG_DIRECTORY + 'report-config.yml')
    excluded_role_patterns = report_config['report-config']['excluded-role-patterns']

    findings = Findings()

    for directory in base_account_directories:
        account_id = os.path.split(os.path.dirname(directory))[-1]
        # Resource Exposure
        resource_exposure_findings = analyze_policy_directory(directory + 'customer-managed/', account_id,
                                                              db_session, resource_exposure_filename,
                                                              'resource_exposure', excluded_role_patterns)
        resource_exposure_occurrences = findings.add('resource_exposure', resource_exposure_findings)

        # Privilege Escalation
        privilege_escalation_findings = analyze_policy_directory(directory + 'customer-managed/', account_id,
                                                                 db_session, privilege_escalation_filename,
                                                                 'privilege_escalation', excluded_role_patterns)
        privilege_escalation_occurrences = findings.add('privilege_escalation', privilege_escalation_findings)

        # Network Exposure
        network_exposure_findings = analyze_policy_directory(directory + 'customer-managed/', account_id,
                                                             db_session, network_exposure_filename,
                                                             'network_exposure', excluded_role_patterns)
        network_exposure_occurrences = findings.add('network_exposure', network_exposure_findings)

        # Credentials exposure
        credentials_exposure_findings = analyze_policy_directory(directory + 'customer-managed/', account_id,
                                                                 db_session, credentials_exposure_filename,
                                                                 'credentials_exposure', excluded_role_patterns)
        credentials_exposure_occurrences = findings.add('credentials_exposure', credentials_exposure_findings)

    occurrences = findings.get_findings()
    # Write JSON report
    create_json_report(occurrences, 'overall')

    # Write Markdown formatted report, which can also be used for exporting to HTML with pandoc
    report_contents = create_markdown_report_template(occurrences)
    create_markdown_report(report_contents, 'overall')  # saved to `/.policy_sentry/policy-analysis/overall.md

    # Write CSV report for overall results
    create_csv_report(occurrences, 'overall')  # saved to `/.policy_sentry/policy-analysis/overall.csv
