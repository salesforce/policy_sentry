"""
ArnActionGroup
"""
import copy
import sys
import re
from sqlalchemy import and_
from policy_sentry.shared.database import ActionTable, ArnTable
from policy_sentry.util.arns import get_service_from_arn, does_arn_match
from policy_sentry.util.actions import get_action_name_from_action, get_service_from_action, get_full_action_name
from policy_sentry.util.text import capitalize_first_character


class ArnActionGroup:
    """
    This class is critical to the creation of least privilege policies.
    It uses the SIDs as namespaces. The namespaces follow this format:
        {Servicename}{Accesslevel}{Resourcetypename}
    So, a resulting statement's SID might look like 'S3ListBucket'
    """

    def __init__(self):
        self.arns = []

    def add(self, db_session, arn_list_from_user, access_level):
        """
        This just adds the ARN, Service, and Access Level. ARN Format and Actions are not filled out.
        Example data can be found in the class ArnActionGroupTestCase in the testing folder.

        :param db_session: SQLAlchemy database session
        :param arn_list_from_user: Just a list of resource ARNs.
        :param access_level: "Read", "List", "Tagging", "Write", or "Permissions management"
        """
        for arn_from_user in arn_list_from_user:
            service = get_service_from_arn(arn_from_user)
            for row in db_session.query(ActionTable).filter(
                    ActionTable.service.like(service)):
                if does_arn_match(arn_from_user, row.resource_arn_format):
                    if row.access_level == access_level:
                        # If it's not a key in the dictionary, add it as a key
                        # and then add the item in the list
                        raw_arn_format = row.resource_arn_format
                        temp_arn_dict = {
                            'arn': arn_from_user,
                            'service': service,
                            'access_level': access_level,
                            'arn_format': raw_arn_format,
                            'actions': []
                        }

                        # If there is already an entry, skip it to avoid duplicates
                        # Otherwise, add it
                        if temp_arn_dict in self.arns:
                            continue
                        self.arns.append(copy.deepcopy(temp_arn_dict))

    # pylint: disable=too-many-arguments
    def add_complete_entry(
            self,
            arn_from_user,
            service,
            access_level,
            raw_arn_format,
            actions_list):
        """
        Add a single entry with all the necessary fields filled out.

        :param arn_from_user: The literal ARN that the user wants to put in the policy
        :param service: A service prefix, like s3
        :param access_level: Access level for the IAM action
        :param raw_arn_format: The raw arn that matches format of the arn_from_user
        :param actions_list: A list of actions
        """
        temp_arn_dict = {
            'arn': arn_from_user,
            'service': service,
            'access_level': access_level,
            'arn_format': raw_arn_format,
            'actions': actions_list
        }
        # If there is already an entry, skip it to avoid duplicates
        # Otherwise, add it
        # if temp_arn_dict in self.arns:
        #     pass
        # else:
        self.arns.append(copy.deepcopy(temp_arn_dict))

    # pylint: disable=too-many-nested-blocks, too-many-branches
    def process_resource_specific_acls(self, cfg, db_session):
        """
        Processes the YAML file for the resources per access level, and adds it to the object.

        :param cfg: A dictionary loaded from the YAML file
        :param db_session: Database session
        :return: the fully formed dict containing the ARNs and actions
        :rtype: dict
        """
        try:
            for category in cfg:
                if category == 'policy_with_crud_levels':
                    for principal in cfg[category]:
                        if 'wildcard' in principal.keys():
                            if principal['wildcard'] is not None:
                                provided_wildcard_actions = principal['wildcard']
                                if isinstance(provided_wildcard_actions, list):
                                    verified_wildcard_actions = remove_actions_that_are_not_wildcard_arn_only(
                                        db_session, provided_wildcard_actions)
                                    if len(verified_wildcard_actions) > 0:
                                        self.process_list_of_actions(
                                            verified_wildcard_actions, db_session)
                        if 'read' in principal.keys():
                            if principal['read'] is not None:
                                self.add(
                                    db_session, principal['read'], "Read")
                        if 'write' in principal.keys():
                            if principal['write'] is not None:
                                self.add(
                                    db_session, principal['write'], "Write")
                        if 'list' in principal.keys():
                            if principal['list'] is not None:
                                self.add(
                                    db_session, principal['list'], "List")
                        if 'permissions-management' in principal.keys():
                            if principal['permissions-management'] is not None:
                                self.add(
                                    db_session,
                                    principal['permissions-management'],
                                    "Permissions management")
                        if 'tag' in principal.keys():
                            if principal['tag'] is not None:
                                self.add(
                                    db_session, principal['tag'], "Tagging")

        # except KeyError as e:
        #     print("Yaml file is missing this block: " + e.args[0])
        #     sys.exit()
        except IndexError:
            print("IndexError: list index out of range. This is likely due to an ARN in your list equaling ''. "
                  "Please evaluate your YML file and try again.")
            sys.exit()

        self.update_actions_for_raw_arn_format(db_session)
        arn_dict = self.get_policy_elements(db_session)
        return arn_dict

    def process_list_of_actions(self, supplied_actions, db_session):
        """
        Takes a list of actions, queries the database for corresponding arns, adds them to the object.

        :param supplied_actions: A list of supplied actions
        :param db_session: SQLAlchemy database session object
        :return: arn_dict: This is the compiled and updated dictionary after all necessary processing.
            This plugs into create_policy
        :rtype: dict
        """
        arns_matching_supplied_actions = []
        # query the database for corresponding ARNs and add them to arns_matching_supplied_actions
        for action in supplied_actions:
            action_name = get_action_name_from_action(action)
            service_name = get_service_from_action(action)
            for row in db_session.query(ActionTable).filter(and_(ActionTable.service.like(service_name),
                                                                 ActionTable.name.like(action_name))):
                if row.resource_arn_format not in arns_matching_supplied_actions:
                    arns_matching_supplied_actions.append(
                        [row.resource_arn_format, row.access_level, str(row.service + ':' + row.name)])
        # Identify the actions that require wildcard ONLY - i.e., they do not permit use of resource ARNs
        # If that's the case, add it to the wildcard namespace. Otherwise, don't add it.
        actions_with_wildcard = []
        for i in range(len(arns_matching_supplied_actions)):
            if '*' not in arns_matching_supplied_actions[i][0]:
                self.add(db_session, [arns_matching_supplied_actions[i][0]],
                         arns_matching_supplied_actions[i][1])
            else:
                actions_with_wildcard.append(
                    arns_matching_supplied_actions[i][2])

        self.update_actions_for_raw_arn_format(db_session)
        # Remove actions from the collection that have the same CRUD level but
        # were not requested by the user
        self.remove_actions_not_matching_list(supplied_actions)
        # If the action exists in the wildcard list,
        # let's remove it from the collection so we don't have actions across
        # both
        actions_with_wildcard_placeholder = []
        for action in range(len(actions_with_wildcard)):
            if self.does_action_exist(actions_with_wildcard[action]):
                pass
            else:
                actions_with_wildcard_placeholder.append(
                    actions_with_wildcard[action])

        actions_with_wildcard.clear()
        actions_with_wildcard.extend(actions_with_wildcard_placeholder)
        self.combine_policy_elements()
        self.remove_actions_duplicated_in_wildcard_resources()

        # If the wildcard list is not empty
        if len(actions_with_wildcard) > 0:
            self.add_complete_entry(
                '*', 'Mult', 'Mult', '*', actions_with_wildcard)
        # NOTE avoid final and other qualifiers IMHO
        arn_dict = self.get_policy_elements(db_session)
        return arn_dict

    def get_arns(self):
        """
        Getter function for the ARNs object

        :return: ARNs object
        :rtype: dict
        """
        return self.arns

    def does_action_exist(self, action):
        """
        Get boolean response for whether or not an action exists under any of the ARNs.

        :param action: full action name, like s3:GetObject
        :return: True or False
        :rtype: bool
        """
        exists = 0
        for i in range(len(self.arns)):
            if action in self.arns[i]['actions']:
                exists = exists + 1
            else:
                continue
        return exists > 0

    def remove_actions_duplicated_in_wildcard_resources(self):
        """
        Removes actions from the object that are in a resource-specific ARN, as well as the `*` resource.
        For example, if ssm:GetParameter is restricted to a specific parameter path, as well as `*`, then we want to
        remove the `*` option to force least privilege.
        """
        actions_under_wildcard_resources = []
        actions_under_wildcard_resources_to_nuke = []
        for i in range(len(self.arns)):
            if self.arns[i]['arn_format'] == '*':
                actions_under_wildcard_resources.extend(
                    self.arns[i]['actions'])
        # Now that we have the list of actions that are under the * ARN,
        # let's see if that action exists under other SIDs
        if len(actions_under_wildcard_resources) > 0:
            for i in range(len(self.arns)):
                if '*' not in self.arns[i]['arn_format']:
                    for j in actions_under_wildcard_resources:
                        if actions_under_wildcard_resources[j] in self.arns[i]['actions']:
                            actions_under_wildcard_resources_to_nuke.append(
                                actions_under_wildcard_resources[j])
        if len(actions_under_wildcard_resources_to_nuke) > 0:
            for i in range(len(self.arns)):
                if '*' in self.arns[i]['arn_format']:
                    for j in actions_under_wildcard_resources_to_nuke:
                        try:
                            self.arns[i]['actions'].remove(
                                str(actions_under_wildcard_resources_to_nuke[j]))
                        except BaseException:  # pylint: disable=broad-except
                            print("Removal not successful")

    def update_actions_for_raw_arn_format(self, db_session):
        """
        Considers the attribute values under each value in self.arns, and fills in the actions lists accordingly.

        :param db_session: SQLAlchemy database session
        """
        for i in range(len(self.arns)):
            for row in db_session.query(ActionTable).filter(and_(  # pylint: disable=bad-continuation
                    ActionTable.access_level.like(
                        self.arns[i]['access_level']),
                    ActionTable.resource_arn_format.like(self.arns[i]['arn_format']))):
                if self.arns[i]['access_level'] == row.access_level and self.arns[i][
                        'arn_format'] == row.resource_arn_format:
                    self.arns[i]['actions'].append(
                        row.service + ':' + row.name)

    def remove_actions_not_matching_list(self, actions_list):
        """
        :param actions_list: List of actions to leave. All actions not in this list are removed
        """
        for i in range(len(self.arns)):
            placeholder_actions_list = []
            for action in range(len(self.arns[i]['actions'])):
                # If the action in self.arns is not in the list of selected actions,
                # don't copy it to the placeholder
                if self.arns[i]['actions'][action] not in actions_list:
                    pass
                # If it is in the list of selected actions, append it to the
                # placeholder
                else:
                    placeholder_actions_list.append(
                        self.arns[i]['actions'][action])
            # Clear the list and then extend it to include the updated actions
            # only
            self.arns[i]['actions'].clear()
            self.arns[i]['actions'].extend(placeholder_actions_list.copy())

        self.remove_sids_with_empty_action_lists()

    def remove_sids_with_empty_action_lists(self):
        """
        Now that we've removed a bunch of actions, if there are SID groups without any actions,
            remove them so we don't get SIDs with empty action lists
        """
        indexes_to_delete = []
        for i in range(len(self.arns)):
            if len(self.arns[i]['actions']) > 0:
                pass
            # If the size is zero, add it to the indexes_to_delete list.
            else:
                indexes_to_delete.append(i)
        # Loop through indexes_to_delete in reverse order (so we delete index
        # 10 before index 8, for example)
        if len(indexes_to_delete) > 0:
            for i in reversed(range(len(indexes_to_delete))):
                del self.arns[indexes_to_delete[i]]
                # except ValueError as e:
                #     if 'list.remove(x)' in str(e):
                #         print("Action is " + self.arns[i]['actions'][action])
                #         print("actions_list is" + str(actions_list))

    def combine_policy_elements(self):
        """
        Consolidate the policy elements by looking at where ARNs are used
        """
        # Using numbers in the 'altered' list to identify indexes that have
        # been altered
        altered = []
        for i in range(len(self.arns)):
            for j in range(len(self.arns)):
                if i == j:
                    continue
                # If the ARN also has other occurrences, get the value of those
                # occurrences and copy it over
                if self.arns[i]['arn_format'] == self.arns[j]['arn_format'] and len(
                        self.arns[i]['actions']) > 0 and i not in altered:
                    self.arns[i]['actions'].extend(self.arns[j]['actions'])
                    self.arns[j]['actions'].clear()
                    altered.append(i)

        self.remove_sids_with_empty_action_lists()
        self.remove_actions_duplicated_in_wildcard_resources()

    def get_policy_elements(self, db_session):
        """
        Return the policy elements to the user.

        :param db_session: database session.
        :return: A dictionary that contains the SID namespace, a list of actions, and a list of resource ARNs that fall under this namespace
        :rtype: dict
        """
        arn_dict = {}
        for i in range(len(self.arns)):
            # Create SID Namespace
            query_resource_arn_format = db_session.query(
                ArnTable.resource_type_name).filter(ArnTable.raw_arn.like(self.arns[i]['arn_format']))
            resource_arn_format = query_resource_arn_format.first()
            temp_name = create_policy_sid_namespace(
                self.arns[i]['service'],
                self.arns[i]['access_level'],
                str(resource_arn_format)
            )
            temp_actions_list = []
            temp_actions_list.extend(self.arns[i]['actions'])
            temp_arns_list = []
            temp_arns_list.append(self.arns[i]['arn'])

            thing = {
                'name': temp_name,
                'actions': copy.deepcopy(temp_actions_list),
                'arns': copy.deepcopy(temp_arns_list)
            }
            # thing = {'name':'namespace', 'actions':'actions_list', 'arns':'arns_list'} for self.arns[i]['arn_format']
            # If raw_arn is also in the list
            # If access_level is also in the list
            if temp_name in arn_dict:
                arn_dict[temp_name]['arns'].extend(temp_arns_list)
            else:
                arn_dict[temp_name] = copy.deepcopy(thing)

        return arn_dict


def remove_actions_that_are_not_wildcard_arn_only(db_session, actions_list):
    """
    Given a list of actions, remove the ones that CAN be restricted to ARNs, leaving only the ones that cannot.

    :param db_session: SQL Alchemy database session object
    :param actions_list: A list of actions
    :return: An updated list of actions
    :rtype: list
    """
    # remove duplicates, if there are any
    actions_list_unique = list(dict.fromkeys(actions_list))
    actions_list_placeholder = []
    for action in actions_list_unique:
        service = get_service_from_action(action)
        action_name = get_action_name_from_action(action)

        rows = db_session.query(ActionTable.service, ActionTable.name).filter(and_(
            ActionTable.service.ilike(service),
            ActionTable.name.ilike(action_name),
            ActionTable.resource_arn_format.like("*"),
            ActionTable.name.notin_(
                db_session.query(ActionTable.name).filter(ActionTable.resource_arn_format.notlike('*')))
        ))
        for row in rows:
            if row.service == service and row.name == action_name:
                actions_list_placeholder.append(
                    get_full_action_name(service, action_name))
    return actions_list_placeholder


def create_policy_sid_namespace(service, access_level, resource_type_name):
    """
    Simply generates the SID name. The SID groups ARN types that share an access level.

    For example, S3 objects vs. SSM Parameter have different ARN types - as do S3 objects vs S3 buckets. That's how we choose to group them.

    :param service: "ssm"
    :param access_level: "Read"
    :param resource_type_name: "parameter"
    :return: SsmReadParameter
    :rtype: str
    """
    # Sanitize the resource_type_name; otherwise we hit some list conversion
    # errors
    resource_type_name = re.sub('[^A-Za-z0-9]+', '', resource_type_name)
    # Also remove the space from the Access level, if applicable. This only
    # applies for "Permissions management"
    access_level = re.sub('[^A-Za-z0-9]+', '', access_level)
    sid_namespace = capitalize_first_character(service) + capitalize_first_character(
        access_level) + capitalize_first_character(resource_type_name)
    return sid_namespace
