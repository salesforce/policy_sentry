import unittest
import json
from policy_sentry.shared.iam_data import iam_definition
from policy_sentry.shared.iam_data import get_service_prefix_data


# class IAMDataChanges(unittest.TestCase):
#     def test_unique_privilege_names_only(self):
#         list_of_actions = []
#         for service_prefix in iam_definition:
#             for privilege in iam_definition[service_prefix].get("privileges"):
#                 list_of_actions.append(f"{service_prefix}:{privilege.get('privilege')}")
#         set_of_actions = set(list_of_actions)
#         print(len(list_of_actions))
#         print(len(set_of_actions))
#         # 7781 and 7781.
#         # We are good to go. I'll convert it to dictionaries
#     def test_unique_resource_names_only(self):
#         list_of_resources = []
#         for service_prefix in iam_definition:
#             for resource in iam_definition[service_prefix].get("resources"):
#                 # Even though the resource doesn't have the service prefix included IRL,
#                 # this ensures all the list items are unique for our test.
#                 list_of_resources.append(f"{service_prefix}:{resource.get('resource')}")
#         set_of_resources = set(list_of_resources)
#         print(len(list_of_resources))
#         print(len(set_of_resources))
#         # 770 and 770. We are good to go
#
#     def test_unique_condition_names_only(self):
#         list_of_conditions = []
#         for service_prefix in iam_definition:
#             for condition in iam_definition[service_prefix].get("conditions"):
#                 # Even though the resource doesn't have the service prefix included IRL,
#                 # this ensures all the list items are unique for our test.
#                 list_of_conditions.append(f"{service_prefix}:{condition.get('condition')}")
#         set_of_conditions = set(list_of_conditions)
#         print(len(list_of_conditions))
#         print(len(set_of_conditions))
#         # 791 and 790. The only non-unique item is swf:workflowType.name, and if you look at the docs, it is pretty much the same so we won't be losing any valuale information by using this as a dictionary key
#         extra_condition = set([x for x in list_of_conditions if list_of_conditions.count(x) > 1])
#         print(extra_condition)

class IAMDataTestCase(unittest.TestCase):

    def test_get_service_prefix_data_raises_exception(self):
        with self.assertRaises(Exception):
            get_service_prefix_data('invalid_aws_service')
