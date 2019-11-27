
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

    def get_findings_by_policy_name(self, policy_name):
        return self.occurrences[policy_name]

    def get_findings(self):
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
    #         return self.occurrences[account_id][policy_name]['credentials_exposure']

