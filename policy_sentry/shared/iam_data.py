"""Used for loading the IAM data"""
from __future__ import annotations

import json
import logging
import functools
from pathlib import Path
from typing import Any

from policy_sentry.shared.constants import (
    DATASTORE_FILE_PATH,
    POLICY_SENTRY_SCHEMA_VERSION_NAME,
    POLICY_SENTRY_SCHEMA_VERSION_V1,
)

logger = logging.getLogger()
# On initialization, load the IAM data
iam_definition_path = DATASTORE_FILE_PATH
logger.debug(f"Leveraging the IAM definition at {iam_definition_path}")
iam_definition = json.loads(Path(iam_definition_path).read_bytes())


@functools.lru_cache(maxsize=1)
def get_iam_definition_schema_version() -> str:
    return iam_definition.get(POLICY_SENTRY_SCHEMA_VERSION_NAME, POLICY_SENTRY_SCHEMA_VERSION_V1)


@functools.lru_cache(maxsize=1024)
def get_service_prefix_data(service_prefix: str) -> dict[str, Any] | None:
    """
    Given an AWS service prefix, return a large dictionary of IAM privilege data for processing and analysis.

    Arguments:
        service_prefix: An AWS service prefix, like s3 or ssm
    Returns:
        List: A list of metadata about that service
    """
    # result = list(filter(lambda item: item["prefix"] == service_prefix, iam_definition))
    result = iam_definition.get(service_prefix, None)
    try:
        return result
    # pylint: disable=bare-except, inconsistent-return-statements
    except:
        logger.debug("Service prefix not %s found.", service_prefix)
        return None
