"""
At policy_sentry initialize time, this function is used to scrape the AWS HTML docs to build the sqlite database.
"""
import os
import logging
import yaml
import pandas
from policy_sentry.shared.constants import LOCAL_LINKS_YML_FILE

logger = logging.getLogger(__name__)


def get_html(directory, requested_service):
    """Get the tables from each HTML file from the AWS docs.."""
    links = []
    with open(LOCAL_LINKS_YML_FILE, "r") as yaml_file:
        try:
            cfg = yaml.safe_load(yaml_file)
        except yaml.YAMLError as exc:
            logger.critical(exc)
    # pylint: disable=duplicate-code
    for service_name in cfg:
        if service_name == requested_service:
            links.extend(cfg[service_name])
    html_list = []
    for link in links:
        try:
            parsed_html = pandas.read_html(os.path.join(directory, link))
            html_list.append(parsed_html)
        except ValueError as v_e:
            if "No tables found" in str(v_e):
                logger.debug("No tables found for %s", link)
            else:
                raise v_e

    return html_list
