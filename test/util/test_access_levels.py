import unittest
from policy_sentry.util.access_levels import determine_access_level_override
from policy_sentry.configuration.access_level_overrides import get_action_access_level_overrides_from_yml


class AccessLevelOverride(unittest.TestCase):
    def test_passing_overall_iam_action_override(self):
        """test_passing_overall_iam_action_override: Tests iam:CreateAccessKey
        (in overrides file as Permissions management, but in the AWS docs as Write)"""
        desired_result = "Permissions management"
        action_overrides = get_action_access_level_overrides_from_yml("iam")
        result = determine_access_level_override("iam", "CreateAccessKey", "Write", action_overrides)
        self.assertEqual(result, desired_result)

    def test_overrides_yml_config(self):
        """test_overrides_yml_config: Tests the format of the overrides yml file for the RAM service"""
        desired_result = {
            'Permissions management': [
                'acceptresourceshareinvitation',
                'associateresourceshare',
                'createresourceshare',
                'deleteresourceshare',
                'disassociateresourceshare',
                'enablesharingwithawsorganization',
                'rejectresourceshareinvitation',
                'updateresourceshare'
            ],
            'Tagging': [
                'tagresource',
                'untagresource'
            ]
        }
        ram_action_overrides = get_action_access_level_overrides_from_yml("ram")
        self.assertDictEqual(ram_action_overrides, desired_result)
