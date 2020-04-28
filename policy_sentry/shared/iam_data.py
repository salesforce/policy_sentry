"""Used for loading the IAM data"""
import os
import json
import logging
import functools

# On initialization, load the IAM data
iam_definition_path = os.path.join(
    os.path.abspath(os.path.dirname(__file__)), "data", "iam-definition.json"
)
iam_definition = json.load(open(iam_definition_path, "r"))
logger = logging.getLogger(__name__)


@functools.lru_cache(maxsize=1024)
def get_service_prefix_data(service_prefix):
    """
    Given an AWS service prefix, return a large dictionary of IAM privilege data for processing and analysis.

    :param service_prefix: An AWS service prefix, like s3 or ssm
    :return:
    """
    result = list(filter(lambda item: item["prefix"] == service_prefix, iam_definition))
    try:
        return result[0]
    except IndexError as i_e:
        logger.debug("Service prefix not %s found - See error: %s", service_prefix, str(i_e))
