"""
Functions for downloading the AWS docs on Actions, Resources, and Condition Keys.

The initialize command uses this to download the docs to the ~/policy_sentry/data/docs folder.
The utils/get_docs

We store the HTML files in this manner so that the user can be more confident in the integrity of the data -
that it has not been altered in any way. The user can reproduce our steps with the original content at any time,
or update the HTML files on their own.
"""

import os
import logging
import re
import json
from pathlib import Path
import requests
from bs4 import BeautifulSoup
from policy_sentry.shared.constants import (
    BASE_DOCUMENTATION_URL,
    BUNDLED_HTML_DIRECTORY_PATH,
    BUNDLED_ACCESS_OVERRIDES_FILE,
)
from policy_sentry.util.access_levels import determine_access_level_override
from policy_sentry.util.file import read_yaml_file

logger = logging.getLogger(__name__)  # pylint: disable=invalid-name


def header_matches(string, table):
    """checks if the string is found in the table header"""
    headers = [chomp(str(x)).lower() for x in table.find_all("th")]
    match_found = False
    for header in headers:
        if string in header:
            match_found = True
            break
    if not match_found:
        return False
    return True


def get_links_from_base_actions_resources_conditions_page():
    """Gets the links from the actions, resources, and conditions keys page, and returns their filenames."""
    html = requests.get(BASE_DOCUMENTATION_URL)
    soup = BeautifulSoup(html.content, "html.parser")
    html_filenames = []
    for i in soup.find("div", {"class": "highlights"}).findAll("a"):
        html_filenames.append(i["href"])
    return html_filenames


def get_action_access_level_overrides_from_yml(
    service, access_level_overrides_file_path=None
):
    """
    Read the YML overrides file, which is formatted like:
        ['ec2']['permissions-management'][action_name].

    Since the AWS Documentation is sometimes outdated, we can use this YML file to     override whatever they provide in their documentation.
    """
    if not access_level_overrides_file_path:
        access_level_overrides_file_path = BUNDLED_ACCESS_OVERRIDES_FILE
    cfg = read_yaml_file(access_level_overrides_file_path)
    if service in cfg:
        return cfg[service]
    else:
        return False


def update_html_docs_directory(html_docs_destination):
    """
    Updates the HTML docs from remote location to either:
    (1) local directory (i.e., this repository, or
    (2) the config directory
    :return:
    """
    link_url_prefix = "https://docs.aws.amazon.com/service-authorization/latest/reference/"
    initial_html_filenames_list = (
        get_links_from_base_actions_resources_conditions_page()
    )
    # Remove the relative path so we can download it
    html_filenames = [sub.replace("./", "") for sub in initial_html_filenames_list]
    # Replace '.html' with '.partial.html' because that's where the current docs live
    # html_filenames = [sub.replace(".html", ".partial.html") for sub in html_filenames]

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

        for script in soup.find_all("script"):
            try:
                if "src" in script.attrs:
                    if script.get("src").startswith("/"):
                        temp = script.attrs["src"]
                        script.attrs["src"] = script.attrs["src"].replace(
                            temp, f"https://docs.aws.amazon.com{temp}"
                        )
            except TypeError as t_e:
                logger.warning(t_e)
                logger.warning(script)
            except AttributeError as a_e:
                logger.warning(a_e)
                logger.warning(script)

        with open(os.path.join(html_docs_destination, page), "w") as file:
            # file.write(str(soup.html))
            file.write(str(soup.prettify()))
            file.close()
        logger.info("%s downloaded", page)


# Borrowed from Parliament:
# https://github.com/duo-labs/parliament/commit/2979e131ff3af9c79137817eaa57a05ae5007706#diff-1669fdcc34b13c17017fb2aae433801dR22
def chomp(string):
    """This chomp cleans up all white-space, not just at the ends"""
    string = str(string)
    response = string.replace("\n", " ")  # Convert line ends to spaces
    response = re.sub(
        " [ ]*", " ", response
    )  # Truncate multiple spaces to single space
    response = re.sub("^[ ]*", "", response)  # Clean start
    return re.sub("[ ]*$", "", response)  # Clean end


def no_white_space(string):
    """Remove all whitespaces"""
    string = str(string)
    response = string.replace("\n", "")  # Convert line ends to spaces
    response = re.sub("[ ]*", "", response)
    return response


def create_database(destination_directory, access_level_overrides_file):
    """
    Create the JSON Data source that holds the IAM data.

    :param destination_directory:
    :param access_level_overrides_file: The path to the file that we use for overriding access levels that are incorrect in the AWS documentation
    :return:
    """

    # Create the docs directory if it doesn't exist
    Path(os.path.join(destination_directory, "docs")).mkdir(
        parents=True, exist_ok=True
    )

    schema = {}

    # for filename in ['list_amazonathena.partial.html']:
    file_list = []
    for filename in os.listdir(BUNDLED_HTML_DIRECTORY_PATH):
        if os.path.isfile(os.path.join(BUNDLED_HTML_DIRECTORY_PATH, filename)):
            if filename not in file_list:
                file_list.append(filename)

    file_list.sort()
    for filename in file_list:
        if not filename.startswith("list_"):
            continue

        with open(os.path.join(BUNDLED_HTML_DIRECTORY_PATH, filename), "r") as f:
            soup = BeautifulSoup(f.read(), "html.parser")
            main_content = soup.find(id="main-content")
            if main_content is None:
                continue

            # Get service name
            title = main_content.find("h1", class_="topictitle").text
            title = re.sub(
                ".*Actions, resources, and condition Keys for *", "", str(title),
                flags=re.IGNORECASE
            )

            title = title.replace("</h1>", "")
            service_name = chomp(title)

            prefix = ""
            for c in main_content.find("h1", class_="topictitle").parent.children:
                if "prefix" in str(c):
                    prefix = str(c)
                    prefix = prefix.split('<code class="code">')[1]
                    prefix = chomp(prefix.split("</code>")[0])
                    break
            # The URL to that service's Actions, Resources, and Condition Keys page
            service_authorization_url_prefix = "https://docs.aws.amazon.com/service-authorization/latest/reference"
            service_authorization_url = f"{service_authorization_url_prefix}/{filename}"
            service_schema = {
                "service_name": service_name,
                "prefix": prefix,
                "service_authorization_url": service_authorization_url,
                "privileges": {},
                "resources": {},
                "conditions": {},
            }

            access_level_overrides_cfg = get_action_access_level_overrides_from_yml(
                prefix, access_level_overrides_file
            )

            tables = main_content.find_all("div", class_="table-contents")

            for table in tables:
                # There can be 3 tables, the actions table, an ARN table, and a condition key table
                # Example: https://docs.aws.amazon.com/IAM/latest/UserGuide/list_awssecuritytokenservice.html
                if not header_matches("actions", table) or not header_matches("description", table):
                    continue

                rows = table.find_all("tr")
                row_number = 0
                while row_number < len(rows):
                    row = rows[row_number]

                    cells = row.find_all("td")
                    if len(cells) == 0:
                        # Skip the header row, which has th, not td cells
                        row_number += 1
                        continue

                    if len(cells) != 6:
                        # Sometimes the privilege contains Scenarios, and I don't know how to handle this
                        # raise Exception("Unexpected format in {}: {}".format(prefix, row))
                        break

                    # See if this cell spans multiple rows
                    rowspan = 1
                    if "rowspan" in cells[0].attrs:
                        rowspan = int(cells[0].attrs["rowspan"])

                    priv = ""
                    # Get the privilege
                    for link in cells[0].find_all("a"):
                        if "href" not in link.attrs:  # pylint: disable=no-else-continue
                            # Skip the <a id='...'> tags
                            api_documentation_link = None
                            continue
                        else:
                            api_documentation_link = link.attrs.get('href')
                            logger.debug(api_documentation_link)
                        priv = chomp(link.text)
                    if priv == "":
                        priv = chomp(cells[0].text)
                    service_prefix = prefix
                    action_name = priv
                    description = chomp(cells[1].text)
                    access_level = chomp(cells[2].text)
                    # Access Level #####
                    # access_level_overrides_cfg will only be true if the service in question is present
                    # in the overrides YML file
                    if access_level_overrides_cfg:
                        override_result = determine_access_level_override(
                            service_prefix,
                            action_name,
                            access_level,
                            access_level_overrides_cfg,
                        )
                        if override_result:
                            access_level = override_result
                            logger.debug(
                                "Override: Setting access level for %s:%s to %s",
                                service_prefix,
                                action_name,
                                access_level,
                            )
                    #     else:
                    #         access_level = access_level
                    # else:
                    #     access_level = access_level
                    resource_types = {}
                    resource_cell = 3

                    while rowspan > 0:
                        if len(cells) == 3 or len(cells) == 6:
                            # ec2:RunInstances contains a few "scenarios" which start in the
                            # description field, len(cells) is 5.
                            # I'm ignoring these as I don't know how to handle them.
                            # These include things like "EC2-Classic-InstanceStore" and
                            # "EC2-VPC-InstanceStore-Subnet"

                            resource_type = chomp(cells[resource_cell].text)

                            condition_keys_element = cells[resource_cell + 1]
                            condition_keys = []
                            if condition_keys_element.text != "":
                                for key_element in condition_keys_element.find_all("p"):
                                    condition_keys.append(chomp(key_element.text))

                            dependent_actions_element = cells[resource_cell + 2]
                            dependent_actions = []
                            if dependent_actions_element.text != "":
                                for (
                                    action_element
                                ) in dependent_actions_element.find_all("p"):
                                    dependent_actions.append(chomp(action_element.text))
                            if "*" in resource_type:
                                required = True
                                resource_type = resource_type.strip("*")
                            else:
                                required = False

                            resource_types[resource_type] = {
                                "resource_type": resource_type,
                                "required": required,
                                "condition_keys": condition_keys,
                                "dependent_actions": dependent_actions,
                            }
                        rowspan -= 1
                        if rowspan > 0:
                            row_number += 1
                            resource_cell = 0
                            row = rows[row_number]
                            cells = row.find_all("td")

                    if "[permission only]" in priv:
                        priv = priv.split(" ")[0]

                    privilege_schema = {
                        "privilege": priv,
                        "description": description,
                        "access_level": access_level,
                        "resource_types": resource_types,
                        "api_documentation_link": api_documentation_link
                    }

                    service_schema["privileges"][priv] = privilege_schema
                    row_number += 1

            # Get resource table
            for table in tables:
                if not header_matches("resource types", table) or not header_matches("arn", table):
                    continue

                rows = table.find_all("tr")
                for row in rows:
                    cells = row.find_all("td")

                    if len(cells) == 0:
                        # Skip the header row, which has th, not td cells
                        continue

                    if len(cells) != 3:
                        raise Exception(
                            "Unexpected number of resource cells {} in {}".format(
                                len(cells), filename
                            )
                        )

                    resource = chomp(cells[0].text)

                    arn = no_white_space(cells[1].text)
                    conditions = []
                    for condition in cells[2].find_all("p"):
                        conditions.append(chomp(condition.text))

                    service_schema["resources"][resource] = {
                        "resource": resource,
                        "arn": arn,
                        "condition_keys": conditions
                    }

            # Get condition keys table
            for table in tables:
                if not (header_matches("<th> condition keys </th>", table) and header_matches("<th> type </th>", table)):
                    continue

                rows = table.find_all("tr")
                for row in rows:
                    cells = row.find_all("td")

                    if len(cells) == 0:
                        # Skip the header row, which has th, not td cells
                        continue

                    if len(cells) != 3:
                        raise Exception(
                            "Unexpected number of condition cells {} in {}".format(
                                len(cells), filename
                            )
                        )

                    condition = no_white_space(cells[0].text)
                    description = chomp(cells[1].text)
                    value_type = chomp(cells[2].text)

                    service_schema["conditions"][condition] = {
                        "condition": condition,
                        "description": description,
                        "type": value_type,
                    }
            this_service_schema = {
                service_prefix: service_schema
            }
            schema.update(this_service_schema)

    iam_definition_file = os.path.join(destination_directory, "iam-definition.json")
    with open(iam_definition_file, "w") as file:
        json.dump(schema, file, indent=4)
    logger.info("Wrote IAM definition file to path: ", iam_definition_file)
