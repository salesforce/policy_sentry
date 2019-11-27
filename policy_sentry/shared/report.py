"""
Generate markdown-formatted reports
"""
from policy_sentry.shared.file import read_yaml_file
from jinja2 import Template
import json
import csv
from policy_sentry.shared.constants import ANALYSIS_DIRECTORY_PATH


REPORT_TEMPLATE = '''# Policy Sentry Audit report

# Summary

This report contains the details of all IAM policies flagged during the IAM analysis. All of these details can also be viewed in the JSON data file.

## Risk Categories

  - Privilege Escalation: This is based off of [Rhino Security Labs research](https://github.com/RhinoSecurityLabs/AWS-IAM-Privilege-Escalation).

  - Resource Exposure: This contains all IAM Actions at the "Permissions Management" resource level. Essentially - if your policy can (1) write IAM Trust Policies, (2) write to the RAM service, or (3) write Resource-based Policies, then the action has the potential to result in resource exposure if an IAM principal with that policy was compromised.

  - Network Exposure: This highlights IAM actions that indicate an IAM principal possessing these actions could create resources that could be exposed to the public at the network level. For example, public RDS clusters, public EC2 instances. While possession of these privileges does not constitute a security vulnerability, it is important to know exactly who has these permissions.

  - Credentials Exposure: This includes IAM actions that grant some kind of credential, where if exposed, it could grant access to sensitive information. For example, `ecr:GetAuthorizationToken` creates a token that is valid for 12 hours, which you can use to authenticate to Elastic Container Registries and download Docker images that are private to the account.

# Results


| Account ID        | Policy Name       | Resource Exposure                   | Privilege Escalation                   | Network Exposure                   | Credentials Exposure                   |
|-------------------|-------------------|------------------------------------|----------------------------------------|------------------------------------------|----------------------------------------|

{%- for key, value in occurrences.items() %}
    | {{ occurrences[key]['account_id'] }} | {{ key }} | {{ occurrences[key]['resource_exposure']|length }} | {{ occurrences[key]['privilege_escalation']|length }} | {{ occurrences[key]['network_exposure']|length }} | {{ occurrences[key]['credentials_exposure']|length }} |
{%- endfor %}


{%- for key, value in occurrences.items() %}
### Policy: {{ key }}
| Resource Exposure                                                                         | Privilege Escalation                                                                         | Network Exposure                                                                         | Credentials Exposure                                                                         |
|-------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------|
| {%- for action in occurrences[key]['resource_exposure'] %}- {{ action }}<br>{%- endfor %} | {%- for action in occurrences[key]['privilege_escalation'] %}- {{ action }}<br>{%- endfor %} | {%- for action in occurrences[key]['network_exposure'] %}- {{ action }}<br>{%- endfor %} | {%- for action in occurrences[key]['credentials_exposure'] %}- {{ action }}<br>{%- endfor %} |
{%- endfor %}
'''

# Just stashing this old report format, basically a long word document style

"""
{%- for key, value in occurrences.items() %}
### Policy: {{ key }}
{% if 'resource_exposure' in occurrences[key] %}
#### Resource Exposure
{%- for action in occurrences[key]['resource_exposure'] %}
- {{ action }}
{%- endfor %}
{% endif %}
{% if 'privilege_escalation' in occurrences[key] %}
#### Privilege Escalation
{%- for action in occurrences[key]['privilege_escalation'] %}
- {{ action }}
{%- endfor %}
{% endif %}
{% if 'network_exposure' in occurrences[key] %}
#### Network Exposure
{%- for action in occurrences[key]['network_exposure'] %}
- {{ action }}
{%- endfor %}
{% endif %}
{% if 'data_access' in occurrences[key] %}
#### Data Access
{%- for action in occurrences[key]['data_access'] %}
- {{ action }}
{%- endfor %}
{% endif %}
{% if 'credentials_exposure' in occurrences[key] %}
#### Credentials Exposure
{%- for action in occurrences[key]['credentials_exposure'] %}
- {{ action }}
{%- endfor %}
{% endif %}
{%- endfor %}
"""


def load_report_config_file(filename):
    report_config_file = read_yaml_file(filename)
    return report_config_file


def create_markdown_report_template(occurrences):
    tm = Template(REPORT_TEMPLATE)
    # occurrences = {
    #         "policyName1": {
    #             "resource_exposure": [
    #                 "sqs:addpermission",
    #                 "sqs:removepermission"
    #             ],
    #             "credentials_exposure": [
    #                 "rds-db:connect"
    #             ]
    #         },
    #         "policyName2": {
    #             "resource_exposure": [
    #                 "sqs:addpermission",
    #                 "sqs:removepermission"
    #             ]
    #         }
    # }
    msg = tm.render(
        occurrences=occurrences
    )
    return msg


def create_csv_report(occurrences, filename, report_dir=False):
    if report_dir:
        report_filepath = report_dir + '/' + filename + '.csv'
    else:
        report_filepath = ANALYSIS_DIRECTORY_PATH + '/' + filename + '.csv'
    with open(report_filepath, 'w') as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        filewriter.writerow(
            [
                "Account ID",
                "Policy Name",
                "Resource Exposure",
                "Privilege Escalation",
                "Network Exposure",
                "Credentials Exposure",
             ]
        )
        for key, value in occurrences.items():
            if 'resource_exposure' in occurrences[key]:
                resource_exposure_length = len(occurrences[key]['resource_exposure'])
            else:
                resource_exposure_length = 0
            if 'privilege_escalation' in occurrences[key]:
                privilege_escalation_length = len(occurrences[key]['privilege_escalation'])
            else:
                privilege_escalation_length = 0
            if 'network_exposure' in occurrences[key]:
                network_exposure_length = len(occurrences[key]['network_exposure'])
            else:
                network_exposure_length = 0
            if 'credentials_exposure' in occurrences[key]:
                credentials_exposure_length = len(occurrences[key]['credentials_exposure'])
            else:
                credentials_exposure_length = 0
            row = [
                occurrences[key]['account_id'],
                key,
                resource_exposure_length,
                privilege_escalation_length,
                network_exposure_length,
                credentials_exposure_length
            ]

            filewriter.writerow(row)
    return report_filepath


def create_json_report(occurrences, filename, report_dir=False):
    if report_dir:
        report_filepath = report_dir + '/' + filename + '.json'
    else:
        report_filepath = ANALYSIS_DIRECTORY_PATH + '/' + filename + '.json'
    with open(report_filepath, 'w') as json_file:
        json_file.write(json.dumps(occurrences, indent=4))
    json_file.close()
    return report_filepath


def create_markdown_report(report_contents, filename, report_dir=False):
    if report_dir:
        report_filepath = report_dir + '/' + filename + '.md'
    else:
        report_filepath = ANALYSIS_DIRECTORY_PATH + '/' + filename + '.md'
    with open(report_filepath, 'w') as file:
        file.write(report_contents)
    file.close()
    print("If you wish to convert this to html, use Pandoc like this:\n\npandoc -f markdown overall.md -t html > overall.html")
    return report_filepath
