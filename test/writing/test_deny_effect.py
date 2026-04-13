import unittest
import json
from policy_sentry.writing.sid_group import SidGroup


class DenyEffectCrudTestCase(unittest.TestCase):
    """Test that the Deny effect works in CRUD mode"""

    def test_deny_effect_crud_mode(self):
        """Generate a Deny policy via CRUD mode"""
        cfg = {
            "mode": "crud",
            "name": "DenyS3Read",
            "effect": "Deny",
            "read": [
                "arn:aws:s3:::example-org-s3-access-logs",
            ],
        }
        sid_group = SidGroup()
        output = sid_group.process_template(cfg)
        print(json.dumps(output, indent=4))
        self.assertEqual(output["Version"], "2012-10-17")
        for statement in output["Statement"]:
            self.assertEqual(statement["Effect"], "Deny")

    def test_default_allow_crud_mode(self):
        """Verify default is still Allow when effect is not specified"""
        cfg = {
            "mode": "crud",
            "name": "AllowS3Read",
            "read": [
                "arn:aws:s3:::example-org-s3-access-logs",
            ],
        }
        sid_group = SidGroup()
        output = sid_group.process_template(cfg)
        print(json.dumps(output, indent=4))
        self.assertEqual(output["Version"], "2012-10-17")
        for statement in output["Statement"]:
            self.assertEqual(statement["Effect"], "Allow")


class DenyEffectActionsTestCase(unittest.TestCase):
    """Test that the Deny effect works in Actions mode"""

    def test_deny_effect_actions_mode(self):
        """Generate a Deny policy via Actions mode"""
        cfg = {
            "mode": "actions",
            "name": "DenyEc2Actions",
            "effect": "Deny",
            "actions": [
                "ec2:AuthorizeSecurityGroupEgress",
                "ec2:AuthorizeSecurityGroupIngress",
            ],
        }
        sid_group = SidGroup()
        output = sid_group.process_template(cfg)
        print(json.dumps(output, indent=4))
        self.assertEqual(output["Version"], "2012-10-17")
        for statement in output["Statement"]:
            self.assertEqual(statement["Effect"], "Deny")

    def test_default_allow_actions_mode(self):
        """Verify default is still Allow when effect is not specified in actions mode"""
        cfg = {
            "mode": "actions",
            "name": "AllowEc2Actions",
            "actions": [
                "ec2:AuthorizeSecurityGroupEgress",
                "ec2:AuthorizeSecurityGroupIngress",
            ],
        }
        sid_group = SidGroup()
        output = sid_group.process_template(cfg)
        print(json.dumps(output, indent=4))
        self.assertEqual(output["Version"], "2012-10-17")
        for statement in output["Statement"]:
            self.assertEqual(statement["Effect"], "Allow")


class InvalidEffectTestCase(unittest.TestCase):
    """Test that invalid effect values raise errors"""

    def test_invalid_effect_raises_error(self):
        """Test invalid effect value raises ValueError"""
        cfg = {
            "mode": "crud",
            "name": "InvalidEffect",
            "effect": "Something",
            "read": [
                "arn:aws:s3:::example-org-s3-access-logs",
            ],
        }
        sid_group = SidGroup()
        with self.assertRaises(ValueError) as context:
            sid_group.process_template(cfg)
        self.assertIn("Invalid effect", str(context.exception))


if __name__ == "__main__":
    unittest.main()
