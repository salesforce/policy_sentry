import unittest
import json
from policy_sentry.querying.all import (
    get_all_service_prefixes,
    get_all_actions
)


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
