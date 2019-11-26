"""
Generate markdown-formatted reports
"""
from cvss import CVSS3
from policy_sentry.shared.file import read_yaml_file
from jinja2 import Template
import copy
import json
import csv
from policy_sentry.shared.constants import ANALYSIS_DIRECTORY_PATH

# CVSS VECTORS
CUSTOM_VECTORS = {
    "network-exposure": "CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:L/A:H",
    "privilege-escalation": "CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:L/A:H",
    "resource-exposure": "CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:L/A:H",
    "data-access": "CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:L/A:L",
    "credentials-exposure": "CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:L/I:L/A:L",
}

REPORT_TEMPLATE = '''# Policy Sentry Audit report

# Summary

Here's what we did

# Approach

Here's how it works

## Risk Categories

* Privilege Escalation: Definition
* Resource Exposure: Definition
* Network Exposure: Definition
* Data access: Definition
* Credentials Exposure: Definition

## Risk Scoring Approach

[CVSS 3.1](https://www.first.org/cvss/calculator/3.1)

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


def get_risk_category_score(risk_category):
    c = CVSS3(CUSTOM_VECTORS[risk_category])
    return c.scores()


def get_risk_category_severity(risk_category):
    c = CVSS3(CUSTOM_VECTORS[risk_category])
    return c.severities()


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


def create_csv_report(occurrences, filename, subdirectory="/"):
    report_path = ANALYSIS_DIRECTORY_PATH + subdirectory + filename + '.csv'
    with open(report_path, 'w') as csvfile:
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


def create_json_report(occurrences, filename, subdirectory="/"):
    report_path = ANALYSIS_DIRECTORY_PATH + subdirectory + filename + '.json'
    with open(report_path, 'w') as json_file:
        json_file.write(json.dumps(occurrences, indent=4))
    json_file.close()


def create_markdown_report(report_contents, filename, subdirectory="/"):
    report_path = ANALYSIS_DIRECTORY_PATH + subdirectory + filename + '.md'
    with open(report_path, 'w') as file:
        file.write(report_contents)
    file.close()
    print("If you wish to convert this to html, use Pandoc like this:\n\npandoc -f markdown report.md -t html > report.html")
