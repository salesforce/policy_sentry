import os
import json

# On initialization, load the IAM data
iam_definition_path = os.path.join(
    os.path.abspath(os.path.dirname(__file__)), "iam-definition.json"
)
iam_definition = json.load(open(iam_definition_path, "r"))


def get_service_prefix_data(service_prefix):
    result = list(filter(lambda item: item["prefix"] == service_prefix, iam_definition))
    return result[0]
