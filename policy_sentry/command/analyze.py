"""
    `analyze` will audit all locally downloaded IAM policy files and generate a report.

    Approach:
    * Policies should be downloaded entirely through the download-policies subcommand.
    * Compile list of actions, from the policy. This includes wildcards in the actions
    * Look them up in the database and expand them to all the explicit actions, to avoid bypass via s3:*
    * Generate a report to illustrate the risk levels of IAM policies across various accounts.
    * The risk levels are Credentials Exposure, Privilege Escalation, Network Exposure, and Resource Exposure.
"""
import os
from glob import glob
import logging
import click
from policy_sentry.shared.analyze import analyze_policy_directory, analyze_policy_file
from policy_sentry.shared.report import load_report_config_file, create_csv_report, create_json_report, \
    create_markdown_report, create_markdown_report_template
from policy_sentry.shared.finding import Findings
from policy_sentry.shared.constants import HOME, CONFIG_DIRECTORY, \
    AUDIT_DIRECTORY_PATH

# Audit filenames
CREDENTIALS_EXPOSURE_FILENAME = AUDIT_DIRECTORY_PATH + '/credentials-exposure.txt'
DATA_ACCESS_FILENAME = AUDIT_DIRECTORY_PATH + '/data-access-arn-list.txt'
PRIVILEGE_ESCALATION_FILENAME = AUDIT_DIRECTORY_PATH + '/privilege-escalation.txt'
NETWORK_EXPOSURE_FILENAME = AUDIT_DIRECTORY_PATH + '/network-exposure.txt'
RESOURCE_EXPOSURE_FILENAME = AUDIT_DIRECTORY_PATH + '/resource-exposure.txt'
# DATA_ACCESS_ARN_LIST_FILENAME = AUDIT_DIRECTORY_PATH + '/data-access-arn-list.txt'

logger = logging.getLogger()
handler = logging.StreamHandler()
formatter = logging.Formatter(
    '%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


@click.group()
def analyze():
    """Analyze IAM policies and generate a report."""


@analyze.command(
    short_help='Analyze *all* locally downloaded IAM policy files and generate a report.'
)
@click.option(
    '--report-config',
    default=AUDIT_DIRECTORY_PATH + 'report-config.yml',
    type=click.Path(exists=True),
    help='Custom report configuration file. Contains policy name exclusions and custom risk score weighting. '
         'Defaults to ~/.policy_sentry/report-config.yml'
)
@click.option(
    '--report-name',
    default='overall',
    type=str,
    help='Name of the report. Defaults to "overall".'
)
@click.option(
    '--include-markdown-report',
    default=False,
    is_flag=True,
    help='Use this flag to enable a Markdown report, which can be used with pandoc to generate an HTML report. '
         'Due to potentially very large report sizes, this is set to False by default.'
)
@click.option(
    '--quiet',
    default=False,
    is_flag=True
)
def downloaded_policies(report_config, report_name, include_markdown_report, quiet):
    """Analyze all locally downloaded IAM policy files and generate a report."""
    if quiet:
        logger.setLevel(logging.WARNING)
    else:
        logger.setLevel(logging.INFO)

    # Get report config
    report_config = load_report_config_file(report_config)
    excluded_role_patterns = report_config['report-config']['excluded-role-patterns']

    findings = Findings()

    base_account_directories = glob(
        HOME + CONFIG_DIRECTORY + 'analysis/' + '*/')
    account_policy_directories = []

    for i in range(len(base_account_directories)):
        account_policy_directories.append(
            base_account_directories[i] + 'customer-managed/')

    print("Analyzing... ")
    for directory in base_account_directories:
        print(f"{directory}")
        account_id = os.path.split(os.path.dirname(directory))[-1]
        # Resource Exposure
        resource_exposure_findings = analyze_policy_directory(directory + 'customer-managed/', account_id,
                                                              RESOURCE_EXPOSURE_FILENAME, 'resource_exposure',
                                                              excluded_role_patterns)
        findings.add(resource_exposure_findings)

        # Privilege Escalation
        privilege_escalation_findings = analyze_policy_directory(directory + 'customer-managed/', account_id,
                                                                 PRIVILEGE_ESCALATION_FILENAME, 'privilege_escalation',
                                                                 excluded_role_patterns)
        findings.add(privilege_escalation_findings)

        # Network Exposure
        network_exposure_findings = analyze_policy_directory(directory + 'customer-managed/', account_id,
                                                             NETWORK_EXPOSURE_FILENAME, 'network_exposure',
                                                             excluded_role_patterns)
        findings.add(network_exposure_findings)

        # Credentials exposure
        credentials_exposure_findings = analyze_policy_directory(directory + 'customer-managed/', account_id,
                                                                 CREDENTIALS_EXPOSURE_FILENAME, 'credentials_exposure',
                                                                 excluded_role_patterns)
        findings.add(credentials_exposure_findings)

    occurrences = findings.get_findings()

    # Write JSON report - save to `~/.policy_sentry/analysis/report_name.json`
    json_report_path = create_json_report(occurrences, report_name)

    # Write Markdown formatted report, which can also be used for exporting to HTML with pandoc
    # Save it to `/.policy_sentry/analysis/report_name.md
    if include_markdown_report:
        report_contents = create_markdown_report_template(occurrences)
        markdown_report_path = create_markdown_report(
            report_contents, report_name)

    # Write CSV report for overall results
    # Save it to `/.policy_sentry/analysis/report_name.csv
    csv_report_path = create_csv_report(occurrences, report_name)

    print(f"\nReports saved to: \n-{json_report_path}\n-{csv_report_path}")
    if include_markdown_report:
        print(f"{markdown_report_path}")
    print("The JSON Report contains the raw data.\nThe CSV report shows a report summary.")
    if include_markdown_report:
        print("The Markdown report shows the same data as the JSON and CSV report, "
              "and can be converted to HTML using pandoc.")


@analyze.command(
    short_help='Analyze a *single* policy file and generate a report'
)
@click.option(
    '--policy',
    type=click.Path(exists=True),
    required=True,
    help='The policy file to analyze.'
)
@click.option(
    '--report-config',
    default=AUDIT_DIRECTORY_PATH + 'report-config.yml',
    type=click.Path(exists=True),
    help='Custom report configuration file. Contains policy name exclusions and custom risk score weighting. '
         'Defaults to ~/.policy_sentry/report-config.yml'
)
@click.option(
    '--report-path',
    default=os.getcwd(),
    type=click.Path(exists=True),
    help='*Path* to the **directory** of the final report. Defaults to current directory.'
)
@click.option(
    '--account-id',
    default="000000000000",
    type=str,
    required=False,
    help='Account ID for the policy. If you want the report to include the account ID, provide it here. '
         'Defaults to a placeholder value.'
)
@click.option(
    '--include-markdown-report',
    default=False,
    is_flag=True,
    help='Use this flag to enable a Markdown report, which can be used with pandoc to generate an HTML report. '
         'Due to potentially very large report sizes, this is set to False by default.'
)
@click.option(
    '--quiet',
    default=False,
    is_flag=True
)
# pylint: disable=too-many-arguments
def policy_file(policy, report_config, report_path, account_id, include_markdown_report, quiet):
    """Analyze a *single* policy file and generate a report"""
    if quiet:
        logger.setLevel(logging.WARNING)
    else:
        logger.setLevel(logging.INFO)
    # Get report config
    report_config = load_report_config_file(report_config)
    excluded_role_patterns = report_config['report-config']['excluded-role-patterns']
    findings = Findings()

    print("Analyzing... ")
    print(f"{policy}")

    # Resource Exposure
    resource_exposure_findings = analyze_policy_file(policy, account_id, RESOURCE_EXPOSURE_FILENAME,
                                                     'resource_exposure', excluded_role_patterns)
    findings.add(resource_exposure_findings)

    # Privilege Escalation
    privilege_escalation_findings = analyze_policy_file(policy, account_id, PRIVILEGE_ESCALATION_FILENAME,
                                                        'privilege_escalation', excluded_role_patterns)
    findings.add(privilege_escalation_findings)

    # Network Exposure
    network_exposure_findings = analyze_policy_file(policy, account_id, NETWORK_EXPOSURE_FILENAME, 'network_exposure',
                                                    excluded_role_patterns)
    findings.add(network_exposure_findings)

    # Credentials exposure
    credentials_exposure_findings = analyze_policy_file(policy, account_id, CREDENTIALS_EXPOSURE_FILENAME,
                                                        'credentials_exposure', excluded_role_patterns)
    findings.add(credentials_exposure_findings)

    occurrences = findings.get_findings()
    report_dir = report_path
    # Write JSON report - save to `~/.policy_sentry/analysis/report_name.json`
    json_report_path = create_json_report(occurrences, 'report', report_dir)

    # Write Markdown formatted report, which can also be used for exporting to HTML with pandoc
    # Save it to `/.policy_sentry/analysis/report_name.md
    if include_markdown_report:
        report_contents = create_markdown_report_template(occurrences)
        markdown_report_path = create_markdown_report(
            report_contents, 'report', report_dir)

    # Write CSV report for overall results
    # Save it to `/.policy_sentry/analysis/report_name.csv
    csv_report_path = create_csv_report(occurrences, 'report', report_dir)

    print(f"\nReports saved to: \n-{json_report_path}\n-{csv_report_path}")
    if include_markdown_report:
        print(f"{markdown_report_path}")
    print("The JSON Report contains the raw data.\nThe CSV report shows a report summary.")
    if include_markdown_report:
        print("The Markdown report shows the same data as the JSON and CSV report, "
              "and can be converted to HTML using pandoc.")
