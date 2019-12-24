# pylint: disable=missing-module-docstring
# Set default logging handler to avoid "No handler found" warnings.
import logging
from logging import NullHandler

logging.getLogger(__name__).addHandler(NullHandler())

name = "policy_sentry"  # pylint: disable=invalid-name
