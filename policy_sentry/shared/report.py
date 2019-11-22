"""
Generate markdown-formatted reports
"""
from cvss import CVSS3
from policy_sentry.shared.file import read_yaml_file
from jinja2 import Template

# CVSS VECTORS
CUSTOM_VECTORS = {
    "network-exposure": "CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:L/A:H",
    "privilege-escalation": "CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:L/A:H",
    "permissions-management": "CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:L/A:H",
    "data-access": "CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:L/A:L",
    "credentials-exposure": "CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:L/I:L/A:L",
}

REPORT_TEMPLATE='''# Policy Sentry Audit report

## Summary

Here's what we did

## Approach

Here's how it works

### Risk Categories

* Privilege Escalation: Definition
* Resource Exposure: Definition
* Permissions Management: Definition
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

| Account ID       | Policy Name       | Network Exposure                   | Privilege Escalation                   | Permissions Management                   | Data Access                   | Credentials Exposure                   |
|------------------|-------------------|------------------------------------|----------------------------------------|------------------------------------------|-------------------------------|----------------------------------------|

{%- for dict_item in occurrences %}
    | {{ dict_item['account_id'] }} | {{ dict_item['policy_name'] }} | {{ dict_item['network_exposure_occurrences'] }} | {{ dict_item['privilege_escalation_occurrences'] }} | {{ dict_item['permissions_management_occurrences'] }} | {{ dict_item['data_access_occurrences'] }} | {{ dict_item['credentials_exposure_occurrences'] }} |
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
    # occurrences = [
    #     {
    #         "account_id": account_id,
    #         "policy_name": "MyPolicy",
    #         "network_exposure_occurrences": "10",
    #         "privilege_escalation_occurrences": 20,
    #         "permissions_management_occurrences": 3,
    #         "data_access_occurrences": "4",
    #         "credentials_exposure_occurrences": "5",
    #     },
    #     {
    #         "account_id": account_id,
    #         "policy_name": "Policy2",
    #         "network_exposure_occurrences": "10",
    #         "privilege_escalation_occurrences": 20,
    #         "permissions_management_occurrences": 3,
    #         "data_access_occurrences": "4",
    #         "credentials_exposure_occurrences": "5",
    #     },
    #     {
    #         "account_id": account_id,
    #         "policy_name": "Policy3",
    #         "network_exposure_occurrences": "10",
    #         "privilege_escalation_occurrences": 20,
    #         "permissions_management_occurrences": 3,
    #         "data_access_occurrences": "4",
    #         "credentials_exposure_occurrences": "5",
    #     }
    # ]

    msg = tm.render(
        account_id=account_id,
        policy_list=policy_list,
        occurrences=occurrences
    )
    return msg
