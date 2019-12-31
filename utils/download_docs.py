#!/usr/bin/env python3
"""
Parses the AWS HTML docs to create a YML file that understands the mapping between services and HTML files.
We store the HTML files in this manner so that the user can be more confident in the integrity of the data -
that it has not been altered in any way. The user can reproduce our steps with the original content at any time,
or update the HTML files on their own.
"""
import sys
import os

# sys.path.append(
#     os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir + '/policy_sentry/')))
from policy_sentry.scraping.awsdocs import update_html_docs_directory, create_service_links_mapping_file
# from scraping.awsdocs import update_html_docs_directory, create_service_links_mapping_file

if __name__ == '__main__':
    html_directory_path = 'policy_sentry/shared/data/docs/'
    links_yml_file = './policy_sentry/shared/data/links.yml'
    print("Reminder: Run this from the main directory of the code repository.")
    print(f"Updating the HTML docs directory at {html_directory_path}.")
    update_html_docs_directory(html_directory_path)
    print("Creating the service links mapping file.")
    create_service_links_mapping_file(html_directory_path, links_yml_file)
