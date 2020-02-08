"""Just a standard place to stash the logging config"""
import logging


def set_log_level(logger, log_level):
    """Set the logging level according to the user-supplied Click.choice() values"""
    if log_level == "CRITICAL":
        logger.setLevel(logging.CRITICAL)
    if log_level == "ERROR":
        logger.setLevel(logging.ERROR)
    if log_level == "WARNING":
        logger.setLevel(logging.WARNING)
    if log_level == "INFO":
        logger.setLevel(logging.INFO)
    if log_level == "DEBUG":
        logger.setLevel(logging.DEBUG)
