import yaml
import os
from policy_sentry.shared.file import get_list_of_service_prefixes_from_links_file
import pandas

all_aws_services = get_list_of_service_prefixes_from_links_file()


def get_html(directory, requested_service):
    links = []
    links_yml_file = os.path.abspath(os.path.dirname(__file__)) + '/links.yml'
    with open(links_yml_file, 'r') as yaml_file:
        try:
            cfg = yaml.safe_load(yaml_file)
        except yaml.YAMLError as exc:
            print(exc)
    for service_name in cfg:
        if service_name == requested_service:
            links.extend(cfg[service_name])
    html_list = []
    for link in links:
        try:
            parsed_html = pandas.read_html(directory + '/' + link)
            html_list.append(parsed_html)
        except ValueError as e:
            if 'No tables found' in str(e):
                pass
            else:
                raise e

    return html_list
