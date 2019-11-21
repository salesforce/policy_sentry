#!/usr/bin/env python
"""
Parses the AWS HTML docs to create a YML file that understands the mapping between services and HTML files.
We store the HTML files in this manner so that the user can be more confident in the integrity of the data -
that it has not been altered in any way. The user can reproduce our steps with the original content at any time,
or update the HTML files on their own.

Before running this script, please execute utils/download-docs.sh from the main directory.
"""
from os import listdir
from os.path import isfile, join
import re
from bs4 import BeautifulSoup
import yaml


# Borrowed from Parliament:
# https://github.com/duo-labs/parliament/commit/2979e131ff3af9c79137817eaa57a05ae5007706#diff-1669fdcc34b13c17017fb2aae433801d
def chomp(string):
    """This chomp cleans up all white-space, not just at the ends"""
    string = str(string)
    response = string.replace("\n", " ")  # Convert line ends to spaces
    response = re.sub(
        " [ ]*", " ", response
    )  # Truncate multiple spaces to single space
    response = re.sub("^[ ]*", "", response)  # Clean start
    return re.sub("[ ]*$", "", response)  # Clean end


mypath = "./policy_sentry/shared/data/docs/"


# Borrowed and altered from Parliament:
# https://github.com/duo-labs/parliament/commit/2979e131ff3af9c79137817eaa57a05ae5007706#diff-1669fdcc34b13c17017fb2aae433801d
def create_service_links_mapping_file():
    prefix_list = []
    links_shortened = {}
    for filename in [f for f in listdir(mypath) if isfile(join(mypath, f))]:
        if not filename.startswith("list_"):
            continue

        with open(mypath + filename, "r") as f:
            soup = BeautifulSoup(f.read(), "html.parser")
            main_content = soup.find(id="main-content")
            if main_content is None:
                continue

            # Get service name
            # title = main_content.find("h1", class_="topictitle")
            # title = re.sub(".*Actions, Resources, and Condition Keys for *", "", str(title))
            # title = title.replace("</h1>", "")
            # service_name = chomp(title)

            # prefix = ""
            for c in main_content.find("h1", class_="topictitle").parent.children:
                if "prefix" in str(c):
                    prefix = str(c)
                    prefix = prefix.split('<code class="code">')[1]
                    prefix = prefix.split("</code>")[0]
                    prefix_list.append(prefix)
                    if prefix not in links_shortened:
                        links_shortened[prefix] = [filename]
                    else:
                        links_shortened[prefix].append(filename)
                    break

    links_dict = {}
    for key, value in sorted(links_shortened.items()):
        links_dict[key] = value

    with open('./policy_sentry/shared/links.yml', 'w+') as outfile:
        yaml.dump(links_dict, outfile, default_flow_style=False)
    outfile.close()


if __name__ == '__main__':
    create_service_links_mapping_file()
