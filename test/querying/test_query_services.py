import unittest

from policy_sentry.querying.services import get_services_data


class QueryServicesTestCase(unittest.TestCase):
    def test_get_services_data(self):
        # when
        results = get_services_data()

        # then
        self.assertGreater(len(results), 400)  # in 07/24 it was 405

        # both should be a non-empty string
        self.assertTrue(results[0]["prefix"])
        self.assertTrue(results[0]["service_name"])
