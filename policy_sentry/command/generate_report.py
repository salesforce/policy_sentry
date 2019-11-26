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
from policy_sentry.shared.report import Findings, create_report_template, load_report_config_file, create_csv_report

HOME = str(Path.home())
DEFAULT_CREDENTIALS_FILE = HOME + '/.aws/credentials'
AUDIT_DIRECTORY_FOLDER = 'audit'
CONFIG_DIRECTORY = '/.policy_sentry/'
audit_directory_path = HOME + CONFIG_DIRECTORY + AUDIT_DIRECTORY_FOLDER
DATABASE_FILE_NAME = 'aws.sqlite3'
database_file_path = HOME + CONFIG_DIRECTORY + DATABASE_FILE_NAME
# Audit filenames
credentials_exposure_filename = audit_directory_path + '/credentials-exposure.txt'
data_access_filename = audit_directory_path + '/data-access-arn-list.txt'
privilege_escalation_filename = audit_directory_path + '/privilege-escalation.txt'
# Permissions management is already in there.
network_exposure_filename = audit_directory_path + '/network-exposure.txt'
data_access_arn_list_filename = audit_directory_path + '/data-access-arn-list.txt'
resource_exposure_filename = audit_directory_path + '/resource-exposure.txt'

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
    # print(account_directories)
    db_session = connect_db(database_file_path)


    # Get report config
    report_config = load_report_config_file(HOME + CONFIG_DIRECTORY + 'report-config.yml')
    excluded_role_patterns = report_config['report-config']['excluded-role-patterns']

    findings = Findings()

    # print("Auditing for Privilege Escalation")
    # TODO: Get the account ID from the download directory
    # for directory in account_policy_directories:
    for directory in base_account_directories:

        # print("Auditing for data access by ARNs")
        # # TODO: The data access by ARNs
        account_id = os.path.split(os.path.dirname(directory))[-1]
        resource_exposure_findings = analyze_policy_directory(directory + 'customer-managed/', account_id, db_session, resource_exposure_filename, 'resource_exposure', excluded_role_patterns)
        resource_exposure_occurrences = findings.add('resource_exposure', resource_exposure_findings)
        # print("Resource Exposure::::")
        # print(json.dumps(resource_exposure_findings, indent=4))
        # print(json.dumps(resource_exposure_occurrences, indent=4))

        # Privilege Escalation
        privilege_escalation_findings = analyze_policy_directory(directory + 'customer-managed/', account_id, db_session, privilege_escalation_filename, 'privilege_escalation', excluded_role_patterns)
        privilege_escalation_occurrences = findings.add('privilege_escalation', privilege_escalation_findings)
        # print("Privilege Escalation::::")
        # print(json.dumps(privilege_escalation_findings, indent=4))
        # print(json.dumps(privilege_escalation_occurrences, indent=4))

        # Network Exposure
        network_exposure_findings = analyze_policy_directory(directory + 'customer-managed/', account_id, db_session, network_exposure_filename, 'network_exposure', excluded_role_patterns)
        network_exposure_occurrences = findings.add('network_exposure', network_exposure_findings)
        # print("Network Exposure::::")
        # print(json.dumps(network_exposure_findings, indent=4))
        # print(json.dumps(network_exposure_occurrences, indent=4))

        # Credentials exposure
        credentials_exposure_findings = analyze_policy_directory(directory + 'customer-managed/', account_id, db_session, credentials_exposure_filename, 'credentials_exposure', excluded_role_patterns)
        credentials_exposure_occurrences = findings.add('credentials_exposure', credentials_exposure_findings)
        # print("Credentials Exposure::::")
        # print(json.dumps(credentials_exposure_findings, indent=4))
        # print(json.dumps(credentials_exposure_occurrences, indent=4))

    occurrences = findings.get_findings()
    # print(json.dumps(occurrences, indent=4))
    with open ('report.json', 'w') as json_file:
        json_file.write(json.dumps(occurrences, indent=4))
    json_file.close()

    report = create_report_template(occurrences)
    # print(report)
    markdown_report_file = "report.md"
    # html_report_file = markdown.markdown(report)

    with open(markdown_report_file, 'w') as file:
        # try:
        # file.write(html_report_file)
        file.write(report)
    file.close()

    create_csv_report(occurrences, 'report.csv')

    print("Now run this command:\n\npandoc -f markdown report.md -t html > tmp/report.html")
