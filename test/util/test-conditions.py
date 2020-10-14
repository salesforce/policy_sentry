import unittest
from policy_sentry.util.conditions import is_condition_key_match

class ConditionsTestCase(unittest.TestCase):
    def test_is_condition_key_match_case_1(self):
        """exact match. return True"""
        document_key = "s3:prefix"
        str_to_match = "s3:prefix"
        self.assertTrue(is_condition_key_match(document_key, str_to_match))

    def test_is_condition_key_match_case_2(self):
        """no match. return False"""
        document_key = "s3:prefix"
        str_to_match = "secretsmanager:SecretId"
        self.assertFalse(is_condition_key_match(document_key, str_to_match))

    def test_is_condition_key_match_case_3(self):
        """match with string before $"""
        document_key = "aws:ResourceTag/${TagKey}"
        str_to_match = "aws:Resourcetag/${TagKey1}"
        self.assertTrue(is_condition_key_match(document_key, str_to_match))

    def test_is_condition_key_match_case_4(self):
        """match with string before <"""
        document_key = "s3:ExistingObjectTag/<key>"
        str_to_match = "s3:ExistingObjectTag/<sample-key>"
        self.assertTrue(is_condition_key_match(document_key, str_to_match))
