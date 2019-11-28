import unittest
from policy_sentry.shared.analyze import determine_risky_actions
from policy_sentry.shared.finding import Findings

resource_exposure_finding = {
    "some-risky-policy": {
        "account_id": "0123456789012",
        "resource_exposure": [
            "iam:createaccesskey",
            "iam:deleteaccesskey"
        ]
    }
}
privilege_escalation_finding = {
    "some-risky-policy": {
        "account_id": "0123456789012",
        "privilege_escalation": [
            "iam:createaccesskey"
        ]
    }
}
privilege_escalation_finding_account_2 = {
    "some-risky-policy": {
        "account_id": "9876543210123",
        "privilege_escalation": [
            "iam:createaccesskey"
        ]
    }
}
privilege_escalation_yolo_policy = {
    "yolo-policy": {
        "account_id": "9876543210123",
        "privilege_escalation": [
            "iam:createaccesskey"
        ]
    }
}


class FindingsTestCase(unittest.TestCase):
    def test_get_findings(self):
        """test_get_findings: Ensure that finding.get_findings() combines two risk findings for one policy properly."""
        findings = Findings()
        desired_result = {
            "some-risky-policy": {
                "account_id": "0123456789012",
                "resource_exposure": [
                    "iam:createaccesskey",
                    "iam:deleteaccesskey"
                ],
                "privilege_escalation": [
                    "iam:createaccesskey"
                ]
            }
        }
        findings.add(resource_exposure_finding)
        findings.add(privilege_escalation_finding)
        occurrences = findings.get_findings()
        self.assertDictEqual(occurrences, desired_result)

    def test_get_findings_by_policy_name(self):
        findings = Findings()
        # Policy name: some-risky-policy
        findings.add(privilege_escalation_finding)
        print(privilege_escalation_finding)
        # Policy name: yolo-policy
        findings.add(privilege_escalation_yolo_policy)
        print(privilege_escalation_yolo_policy)
        findings_for_second_policy_name = findings.get_findings_by_policy_name('yolo-policy')
        print(findings_for_second_policy_name)
        self.assertDictEqual(findings_for_second_policy_name, privilege_escalation_yolo_policy['yolo-policy'])

    # def test_get_findings_by_account_id(self):
    #     findings = Findings()
    #     # account ID = 0123456789012
    #     findings.add('privilege_escalation', privilege_escalation_finding)
    #     # account ID = 9876543210123
    #     findings.add('privilege_escalation', privilege_escalation_finding_account_2)
    #     findings_for_second_account = findings.get_findings_by_account_id('9876543210123')
    #     self.assertDictEqual(findings_for_second_account, privilege_escalation_finding_account_2)
