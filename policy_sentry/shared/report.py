"""
Generate markdown-formatted reports
"""
from cvss import CVSS3
from policy_sentry.shared.file import read_yaml_file
from jinja2 import Template
import copy

# CVSS VECTORS
CUSTOM_VECTORS = {
    "network-exposure": "CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:L/A:H",
    "privilege-escalation": "CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:L/A:H",
    "resource-exposure": "CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:L/A:H",
    "data-access": "CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:L/A:L",
    "credentials-exposure": "CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:L/I:L/A:L",
}

REPORT_TEMPLATE = '''# Policy Sentry Audit report

## Summary

Here's what we did

## Approach

Here's how it works

### Risk Categories

* Privilege Escalation: Definition
* Resource Exposure: Definition
* Network Exposure: Definition
* Data access: Definition
* Credentials Exposure: Definition

### Risk Scoring Approach

[CVSS 3.1](https://www.first.org/cvss/calculator/3.1)

## Results

### Account ID: {{ account_id }}

#### Policies

{% for item in policy_list %}
* [{{ item }}](./{{ item }}.json)
{%- endfor %}

| Policy Name       | Resource Exposure                   | Privilege Escalation                   | Network Exposure                   | Data Access                   | Credentials Exposure                   |
|-------------------|------------------------------------|----------------------------------------|------------------------------------------|-------------------------------|----------------------------------------|

{%- for key, value in occurrences.items() %}
    | {{ key }} | {{ occurrences[key]['resource_exposure'] }} | {{ occurrences[key]['privilege_escalation'] }} | {{ occurrences[key]['network_exposure'] }} | {{ occurrences[key]['data_access'] }} | {{ occurrences[key]['credentials_exposure'] }} |
{%- endfor %}
'''


def get_risk_category_score(risk_category):
    c = CVSS3(CUSTOM_VECTORS[risk_category])
    return c.scores()


def get_risk_category_severity(risk_category):
    c = CVSS3(CUSTOM_VECTORS[risk_category])
    return c.severities()


def load_report_config_file(filename):
    report_config_file = read_yaml_file(filename)
    return report_config_file


def create_report_template(account_id, occurrences):
    tm = Template(REPORT_TEMPLATE)
    policy_list = []
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
        account_id=account_id,
        policy_list=policy_list,
        occurrences=occurrences
    )
    return msg


class Findings:
    occurrences = {}

    def __init__(self):
        self.occurrences = {}

    def add(self, finding_type, policy_finding):
        for key, value in policy_finding.items():
            if key in self.occurrences:
                self.occurrences[key].update(value)
            else:
                self.occurrences[key] = value

        return self.occurrences

    def get_findings_by_account(self, account_id):
        return self.occurrences[account_id]

    def get_findings_by_policy_name(self, account_id, policy_name):
        return self.occurrences[account_id][policy_name]

    def get_findings_by_finding_type(self, account_id, policy_name, finding_type):
        if finding_type == "network_exposure":
            return self.occurrences[account_id][policy_name]['network_exposure']
        if finding_type == "privilege_escalation":
            return self.occurrences[account_id][policy_name]['privilege_escalation']
        if finding_type == "resource_exposure":
            return self.occurrences[account_id][policy_name]['resource_exposure']
        if finding_type == "data_access":
            return self.occurrences[account_id][policy_name]['data_access']
        if finding_type == "credentials_exposure":
            return self.occurrences[account_id][policy_name]['credentials_exposure']

    def get_findings(self):
        return self.occurrences
