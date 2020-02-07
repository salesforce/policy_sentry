# pylint: disable=missing-module-docstring
import logging

# Set default logging handler to avoid "No handler found" warnings.
from logging import NullHandler

logging.getLogger(__name__).addHandler(NullHandler())
name = "policy_sentry"  # pylint: disable=invalid-name
