"""
At policy_sentry initialize time, this function is used to scrape the AWS HTML docs to build the sqlite database.
"""
import os
import yaml
import pandas
from policy_sentry.shared.constants import LINKS_YML_FILE_LOCAL
# from policy_sentry.shared.awsdocs import get_list_of_service_prefixes_from_links_file
# ALL_AWS_SERVICES = get_list_of_service_prefixes_from_links_file()


def get_html(directory, requested_service):
    """Get the tables from each HTML file from the AWS docs.."""
    links = []
    # links_yml_file = os.path.abspath(os.path.dirname(__file__)) + '/links.yml'
    # with open(links_yml_file, 'r') as yaml_file:
    with open(LINKS_YML_FILE_LOCAL, 'r') as yaml_file:
        try:
            cfg = yaml.safe_load(yaml_file)
        except yaml.YAMLError as exc:
            print(exc)
    # pylint: disable=duplicate-code
    for service_name in cfg:
        if service_name == requested_service:
            links.extend(cfg[service_name])
    html_list = []
    for link in links:
        try:
            parsed_html = pandas.read_html(directory + '/' + link)
            html_list.append(parsed_html)
        except ValueError as v_e:
            if 'No tables found' in str(v_e):
                print(f"No tables found for {link}")
                pass
            else:
                raise v_e

    return html_list
