"""
Functions for downloading the AWS docs on Actions, Resources, and Condition Keys.

The initialize command uses this to download the docs to the ~/policy_sentry/data/docs folder.
The utils/get_docs

We store the HTML files in this manner so that the user can be more confident in the integrity of the data -
that it has not been altered in any way. The user can reproduce our steps with the original content at any time,
or update the HTML files on their own.
"""

from os import listdir
from os.path import isfile, join
import logging
import re
from bs4 import BeautifulSoup
import yaml
import requests
from policy_sentry.shared.constants import BASE_DOCUMENTATION_URL

logger = logging.getLogger(__name__)  # pylint: disable=invalid-name


def get_links_from_base_actions_resources_conditions_page():
    """Gets the links from the actions, resources, and conditions keys page, and returns their filenames."""
    html = requests.get(BASE_DOCUMENTATION_URL)
    soup = BeautifulSoup(html.content, "html.parser")
    html_filenames = []
    for i in soup.find("div", {"class": "highlights"}).findAll("a"):
        html_filenames.append(i["href"])
    return html_filenames


def update_html_docs_directory(html_docs_destination):
    """
    Updates the HTML docs from remote location to either (1) local directory
    (i.e., this repository, or (2) the config directory
    :return:
    """
    link_url_prefix = "https://docs.aws.amazon.com/IAM/latest/UserGuide/"
    initial_html_filenames_list = (
        get_links_from_base_actions_resources_conditions_page()
    )
    # Remove the relative path so we can download it
    html_filenames = [sub.replace("./", "") for sub in initial_html_filenames_list]
    # Replace '.html' with '.partial.html' because that's where the current docs live
    html_filenames = [sub.replace(".html", ".partial.html") for sub in html_filenames]

    for page in html_filenames:
        response = requests.get(link_url_prefix + page, allow_redirects=False)
        # Replace the CSS stuff. Basically this:
        """
        <link href='href="https://docs.aws.amazon.com/images/favicon.ico"' rel="icon" type="image/ico"/>
        <link href='href="https://docs.aws.amazon.com/images/favicon.ico"' rel="shortcut icon" type="image/ico"/>
        <link href='href="https://docs.aws.amazon.com/font/css/font-awesome.min.css"' rel="stylesheet" type="text/css"/>
        <link href='href="https://docs.aws.amazon.com/css/code/light.css"' id="code-style" rel="stylesheet" type="text/css"/>
        <link href='href="https://docs.aws.amazon.com/css/awsdocs.css?v=20181221"' rel="stylesheet" type="text/css"/>
        <link href='href="https://docs.aws.amazon.com/assets/marketing/css/marketing-target.css"' rel="stylesheet" type="text/css"/>
        list_amazonkendra.html downloaded
        """
        soup = BeautifulSoup(response.content, "html.parser")
        for link in soup.find_all("link"):
            if link.get("href").startswith("/"):
                temp = link.attrs["href"]
                link.attrs["href"] = link.attrs["href"].replace(
                    temp, f"https://docs.aws.amazon.com{temp}"
                )

        with open(html_docs_destination + page, "w") as file:
            # file.write(str(soup.html))
            file.write(str(soup.prettify()))
            file.close()
        logger.info("%s downloaded", page)


# Borrowed and altered from Parliament:
# https://github.com/duo-labs/parliament/commit/2979e131ff3af9c79137817eaa57a05ae5007706#diff-1669fdcc34b13c17017fb2aae433801d
# pylint: disable=invalid-name
def create_service_links_mapping_file(html_docs_destination, links_yml_file):
    """Parses the AWS HTML docs to create a YML file that understands the mapping between services and HTML files."""
    prefix_list = []
    links_shortened = {}
    for filename in [
        f
        for f in listdir(html_docs_destination)
        if isfile(join(html_docs_destination, f))
    ]:
        if not filename.startswith("list_"):
            continue

        with open(html_docs_destination + filename, "r") as f:
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
                    prefix = chomp(prefix)
                    prefix_list.append(prefix)
                    if prefix not in links_shortened:
                        links_shortened[prefix] = [filename]
                    else:
                        links_shortened[prefix].append(filename)
                    break

    links_dict = {}
    for key, value in sorted(links_shortened.items()):
        links_dict[key] = value
    with open(links_yml_file, "w+") as outfile:
        yaml.dump(links_dict, outfile, default_flow_style=False)
    outfile.close()
    prefix_list.sort()
    prefix_list = list(dict.fromkeys(prefix_list))
    logger.info("Created the service-to-links YML mapping file: ", links_yml_file)
    return prefix_list


def get_list_of_service_prefixes_from_links_file(links_yml_file):
    """
    Gets a list of service prefixes from the links file. Used for unit tests.
    :return:
    """
    # links_yml_file = os.path.abspath(os.path.dirname(__file__)) + '/data/links.yml'
    service_prefixes = []
    with open(links_yml_file, "r") as yaml_file:
        try:
            cfg = yaml.safe_load(yaml_file)
        except yaml.YAMLError as exc:
            logger.critical(exc)
    for service_name in cfg:
        service_prefixes.append(service_name)
    return service_prefixes


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
