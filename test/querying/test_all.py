import unittest
import json
from policy_sentry.querying.all import (
    get_all_service_prefixes,
    get_all_actions,
    get_service_authorization_url
)
from policy_sentry.command.query import query_action_table


class QueryActionsTestCase(unittest.TestCase):
    def test_get_all_service_prefixes(self):
        result = get_all_service_prefixes()
        self.assertGreater(len(result), 212)
        # print(len(result))
        # print(json.dumps(result, indent=4))
        # performance notes:
        # old: 0.013s
        # new: 0.005s

    def test_get_all_actions(self):
        result = get_all_actions()
        print("Total count of unique IAM actions:", len(result))
        self.assertGreater(len(result), 7000)

        # performance notes:
        # old: 0.112s (without sort)
        # new: 0.106s

    def test_query_actions_with_access_level_and_wildcard_only(self):
        service = "all"
        resource_type = "*"
        result = query_action_table(
            service=service,
            resource_type=resource_type,
            name=None,
            access_level="permissions-management",
            condition=None
        )
        print(len(result))
        self.assertTrue(len(result) > 200)

    def test_GH_296_query_all_actions_with_wildcard_resources(self):
        service = "all"
        resource_type = "*"
        result = query_action_table(
            service=service,
            resource_type=resource_type,
            name=None,
            access_level=None,
            condition=None
        )
        self.assertTrue(len(result) > 3000)

    def test_get_service_authorization_url(self):
        result = get_service_authorization_url("a4b")
        print(result)
        expected_result = "https://docs.aws.amazon.com/service-authorization/latest/reference/list_alexaforbusiness.html"
        self.assertTrue(result == expected_result)

