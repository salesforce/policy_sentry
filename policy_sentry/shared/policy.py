import copy
import sys
import re
import json
from sqlalchemy import and_
from policy_sentry.shared.database import ActionTable, ArnTable
from policy_sentry.shared.arns import get_service_from_arn, does_arn_match
from policy_sentry.shared.actions import get_action_name_from_action, get_service_from_action


class ArnActionGroup:
    def __init__(self):
        self.arns = []

    def add(self, db_session, arn_list_from_user, access_level):
        """
        This just adds the ARN, Service, and Access Level. ARN Format and Actions are not filled out.
        Example data can be found in the class ArnActionGroupTestCase in the testing folder.

        :param session: SQLAlchemy database session
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

    def add_complete_entry(
            self,
            arn_from_user,
            service,
            access_level,
            raw_arn_format,
            actions_list):
        """
        Add a single entry with all the necessary fields filled out.
        :param arn_from_user:
        :param service:
        :param access_level:
        :param raw_arn_format:
        :param actions_list:
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

    def process_resource_specific_acls(self, cfg, db_session):
        """
        Processes the YAML file for the resources per access level, and adds it to the object.
        :param cfg: A dictionary loaded from the YAML file
        :param db_session: Database session
        :return: the fully formed dict containing the ARNs and actions
        """
        try:
            for category in cfg:
                if category == 'roles_with_crud_levels':
                    for principal in cfg[category]:
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
        Full processing of the list of actions
        :param supplied_actions: A list of supplied actions
        :param db_session: SQLAlchemy database session object
        :return: arn_dict: This is the compiled and updated dictionary after all necessary processing.
            This plugs into create_policy
        """
        arns_matching_supplied_actions = []
        for action in supplied_actions:
            action_name = get_action_name_from_action(action)
            service_name = get_service_from_action(action)
            for row in db_session.query(ActionTable).filter(
                and_(
                    ActionTable.service.like(service_name),
                    ActionTable.name.like(action_name))):
                if row.resource_arn_format not in arns_matching_supplied_actions:
                    arns_matching_supplied_actions.append(
                        [row.resource_arn_format, row.access_level, str(row.service + ':' + row.name)])

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
        return self.arns

    def does_action_exist(self, action):
        exists = 0
        for i in range(len(self.arns)):
            if action in self.arns[i]['actions']:
                exists = exists + 1
            else:
                continue
        return exists > 0

    def remove_actions_duplicated_in_wildcard_resources(self):
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
                        except BaseException:
                            print("Removal not successful")

    def update_actions_for_raw_arn_format(self, db_session):
        """
        Simply fills in the actions list
        :param session: SQLAlchemy database session
        """
        for i in range(len(self.arns)):
            for row in db_session.query(ActionTable).filter(
                and_(
                    ActionTable.access_level.like(
                        self.arns[i]['access_level']), ActionTable.resource_arn_format.like(
                    self.arns[i]['arn_format']))):
                if self.arns[i]['access_level'] == row.access_level and self.arns[i][
                        'arn_format'] == row.resource_arn_format:
                    self.arns[i]['actions'].append(
                        row.service + ':' + row.name)

    def remove_actions_not_matching_list(self, actions_list):
        """
        :param actions_list: List of actions to leave. All actions not in this list are removed
        :return: Nothing
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
        # Now that we've removed a bunch of actions, if there are SID groups
        # without any actions, remove them so we don't get SIDs with empty
        # action lists
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
        # self.remove_sids_with_empty_action_lists()

    def get_policy_elements(self, db_session):
        """

        :param db_session: database session.
        :return: arn_dict. This is a dictionary of dictionaries. Each sub-dictionary has the following elements:
          1. name: The SID namespace. This follows the format of {Servicename} + {Accesslevel} + {Resourcetypename}.
          2. actions: A list of actions
          3. arns: A list of resource ARNs that fall under this namespace.
        """
        arn_dict = {}
        for i in range(len(self.arns)):
            # Create SID Namespace
            query_resource_arn_format = db_session.query(
                ArnTable.resource_type_name).filter(
                ArnTable.raw_arn.like(
                    self.arns[i]['arn_format']))
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


def create_policy_sid_namespace(service, access_level, resource_type_name):
    """
    Description: Simply generates the SID name. The SID groups ARN types that share an access level. For example, S3 objects vs. SSM Parameter have different ARN types - as do S3 objects vs S3 buckets. That's how we choose to group them.
    :param service: "ssm"
    :param access_level: "Read"
    :param resource_type_name: "parameter"
    :return: SsmReadParameter
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


def capitalize_first_character(some_string):
    """
    Description: Capitalizes the first character of a string
    :param some_string:
    :return:
    """
    return ' '.join(''.join([w[0].upper(), w[1:].lower()])
                    for w in some_string.split())


class PolicyGroup:

    def __init__(self):
        self.policies = {}
        # each dict has:
        # policy_name, policy_id, policy_arn, default_version_id, and
        # policy_document

    def add(self, policy_name, policy_id, policy_arn, default_version_id):
        temp_dict = {
            'policy_id': policy_id,
            'policy_arn': policy_arn,
            'default_version_id': default_version_id
        }
        self.policies[policy_name] = temp_dict

    def get_policy_names(self):
        temp_list_of_policy_names = []
        for policy in self.policies:
            temp_list_of_policy_names.append(policy)
        return temp_list_of_policy_names

    def get_policy_document(self, policy_name, formatted_as_string=None):
        if formatted_as_string:
            policy = self.policies[policy_name]['policy_document']
            return json.dumps(policy, indent=4, default=str)
        else:
            return self.policies[policy_name]['policy_document']

    def set_remote_policy_metadata(
            self,
            iam_session,
            customer_managed=True,
            attached_only=True):
        """
        Grabs IAM policies and adds them to the object
        :param iam_session: IAM boto session
        :param customer_managed: True for 'Local' (customer managed policies), False for 'AWS' (managed policies)
        :param only_attached: True/False
        """
        if customer_managed:
            scope = 'Local'
        else:
            scope = 'AWS'
        # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.list_policies
        response = iam_session.list_policies(
            Scope=scope,
            OnlyAttached=attached_only,
            PathPrefix='/',  # slash (/) lists all policies
            # PolicyUsageFilter='PermissionsPolicy',
            MaxItems=123
        )
        for policy in response['Policies']:
            policy_name = policy['PolicyName']
            policy_id = policy['PolicyId']
            policy_arn = policy['Arn']
            default_version_id = policy['DefaultVersionId']
            self.add(policy_name, policy_id, policy_arn, default_version_id)

    def set_policy_document(self, policy_name, document):
        # document is a dict containing version and statement. Statement contains typical IAM policy statements.
        # for policy in self.policies:
        # TODO: Handle an error where the policy name does not exist
        self.policies[policy_name]['policy_document'] = document

    def set_remote_policy_documents(self, iam_session):
        for policy in self.policies:
            response = iam_session.get_policy_version(
                PolicyArn=self.policies[policy]['policy_arn'],
                VersionId=self.policies[policy]['default_version_id']
            )
            self.set_policy_document(
                policy, response['PolicyVersion']['Document'])
