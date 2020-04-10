"""Used for loading the IAM data"""
import os
import json

# On initialization, load the IAM data
iam_definition_path = os.path.join(
    os.path.abspath(os.path.dirname(__file__)), "data", "iam-definition.json"
)
iam_definition = json.load(open(iam_definition_path, "r"))


def get_service_prefix_data(service_prefix):
    """
    Given an AWS service prefix, return a large dictionary of IAM privilege data for processing and analysis.

    :param service_prefix: An AWS service prefix, like s3 or ssm
    :return:
    """
    result = list(filter(lambda item: item["prefix"] == service_prefix, iam_definition))
    return result[0]
