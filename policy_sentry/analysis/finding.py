"""
Findings is a class dedicated to storing the findings for our Analyze report.

There are a few different uses of this:
- credentials exposure,
- resource exposure,
- privilege escalation, and
- credentials exposure
"""


class Findings:
    """
    One finding type per Finding instance. Multiple policies per instances.
    A single finding object looks like this:
    credentials_exposure_findings = [{"PolicyName": ["ecr:GetAuthorizationToken"]}]
    """
    occurrences = {}

    def __init__(self):
        self.occurrences = {}

    def add(self, policy_finding):
        """
        Add a new policy to the Finding object.

        :param policy_finding: An entry to add to the finding object, like {"PolicyName": ["ecr:GetAuthorizationToken"]}
        :return: The findings and finding types for that policy.
        """
        for key, value in policy_finding.items():
            if key in self.occurrences:
                self.occurrences[key].update(value)
            else:
                self.occurrences[key] = value

        return self.occurrences

    def get_findings_by_policy_name(self, policy_name):
        """
        Given the name of a policy, return findings that contain finding types with action lists under them.

        :param policy_name: The name of the policy to look for.
        :return: The findings and finding types for that policy.
        """
        return self.occurrences[policy_name]

    def get_findings(self):
        """
        Get all findings as a dict

        :return: The findings and finding types for that policy.
        """
        return self.occurrences

    # def get_findings_by_account_id(self, account_id):
    #     return self.occurrences[account_id]

    # def get_findings_by_finding_type(self, account_id, policy_name, finding_type):
    #     if finding_type == "network_exposure":
    #         return self.occurrences[account_id][policy_name]['network_exposure']
    #     if finding_type == "privilege_escalation":
    #         return self.occurrences[account_id][policy_name]['privilege_escalation']
    #     if finding_type == "resource_exposure":
    #         return self.occurrences[account_id][policy_name]['resource_exposure']
    #     if finding_type == "data_access":
    #         return self.occurrences[account_id][policy_name]['data_access']
    #     if finding_type == "credentials_exposure":
    # return self.occurrences[account_id][policy_name]['credentials_exposure']
