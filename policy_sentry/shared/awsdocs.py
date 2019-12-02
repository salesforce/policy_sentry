"""
Functions for downloading the AWS docs on Actions, Resources, and Condition Keys.

The initialize command uses this to download the docs to the ~/policy_sentry/data/docs folder.
The utils/get_docs

We store the HTML files in this manner so that the user can be more confident in the integrity of the data -
that it has not been altered in any way. The user can reproduce our steps with the original content at any time,
or update the HTML files on their own.
"""

from os import listdir, remove
from os.path import isfile, join, exists
from subprocess import run, CalledProcessError
import re
from bs4 import BeautifulSoup
import yaml


def update_html_docs_directory(html_docs_destination):
    """
    Updates the HTML docs from remote location to either (1) local directory
    (i.e., this repository, or (2) the config directory
    :return:
    """
    wget_command = "wget -r --no-parent -nv --convert-links --accept 'list_*.html' --reject 'feedbackno.html','feedbackyes.html' --no-clobber https://docs.aws.amazon.com/IAM/latest/UserGuide/introduction.html --no-host-directories --cut-dirs=3 --directory-prefix=" + html_docs_destination
    try:
        run(wget_command, shell=True, check=True)
    except CalledProcessError as cp_e:
        # This really isn't an issue. The subprocess.run function will throw an error whenever there
        # is a non-zero error. In this case, wget will issue exit status #8 - "Server issued an error response."
        # This could be because of HTTP 404 errors on pages linked from that AWS documentation that we don't care about
        # and won't download. In any case, we don't want it to break our whole script.
        print(f"CalledProcessError: Please ignore this error, especially if it says 'exit status 8', which "
              f"is a false positive. {cp_e}")
    print("\nNote: Despite what the wget command output says here, the actual number of files downloaded is only the "
          "number of HTML files matching `list_aws*.html` or `list_amazon*.html`\n")

    # Remove a random straggler file
    if exists(html_docs_destination + '/robots.txt.tmp'):
        remove(html_docs_destination + '/robots.txt.tmp')


# Borrowed and altered from Parliament:
# https://github.com/duo-labs/parliament/commit/2979e131ff3af9c79137817eaa57a05ae5007706#diff-1669fdcc34b13c17017fb2aae433801d
# pylint: disable=invalid-name
def create_service_links_mapping_file(html_docs_destination, links_yml_file):
    """Parses the AWS HTML docs to create a YML file that understands the mapping between services and HTML files."""
    prefix_list = []
    links_shortened = {}
    for filename in [f for f in listdir(html_docs_destination) if isfile(join(html_docs_destination, f))]:
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
                    prefix_list.append(prefix)
                    if prefix not in links_shortened:
                        links_shortened[prefix] = [filename]
                    else:
                        links_shortened[prefix].append(filename)
                    break

    links_dict = {}
    for key, value in sorted(links_shortened.items()):
        links_dict[key] = value
    with open(links_yml_file, 'w+') as outfile:
        yaml.dump(links_dict, outfile, default_flow_style=False)
    outfile.close()
    print(f"Created the service-to-links YML mapping file")


def get_list_of_service_prefixes_from_links_file(links_yml_file):
    """
    Gets a list of service prefixes from the links file. Used for unit tests.
    :return:
    """
    # links_yml_file = os.path.abspath(os.path.dirname(__file__)) + '/links.yml'
    service_prefixes = []
    with open(links_yml_file, 'r') as yaml_file:
        try:
            cfg = yaml.safe_load(yaml_file)
        except yaml.YAMLError as exc:
            print(exc)
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
