"""
sid_group indicates that this is a collection of policy-related data organized by their SIDs
"""
import copy
import logging
from policy_sentry.querying.all import get_all_actions
from policy_sentry.querying.actions import get_action_data, get_actions_with_arn_type_and_access_level, \
    get_dependent_actions_only, get_actions_that_support_wildcard_arns_only
from policy_sentry.querying.arns import get_arn_data, get_resource_type_name_with_raw_arn
from policy_sentry.writing.policy import create_policy_sid_namespace
from policy_sentry.util.arns import does_arn_match, get_service_from_arn
from policy_sentry.writing.minimize import minimize_statement_actions
from policy_sentry.shared.constants import POLICY_LANGUAGE_VERSION
from policy_sentry.util.actions import get_lowercase_action_list

logger = logging.getLogger(__name__)


class SidGroup:
    def __init__(self):
        # Dict instead of list
        # sids instead of ARN
        self.sids = {}
        self.universal_conditions = {}

    def get_sid_group(self):
        """
        Get the whole SID group
        """
        return self.sids

    def get_sid(self, sid):
        """Get a single group by the SID identifier"""
        if self.sids[sid]:
            return self.sids[sid]
        else:
            raise Exception("No SID with the value of %s", sid)

    def list_sids(self):
        """Get a list of all of them by their identifiers"""
        return self.sids.keys()

    def get_universal_conditions(self):
        return self.universal_conditions

    def get_rendered_policy(self, db_session, minimize=None):
        """
        Get the JSON rendered policy
        """
        statements = []
        all_actions = get_all_actions(db_session)

        #
        # render the policy
        for sid in self.sids:
            actions = self.sids[sid]["actions"]
            if len(actions) == 0:
                continue
            if minimize is not None and isinstance(minimize, int):
                actions = minimize_statement_actions(actions, all_actions, minchars=minimize)
            statements.append({
                "Sid": sid,
                "Effect": "Allow",
                "Action": actions,
                "Resource": self.sids[sid]["arn"]
            })
        policy = {
            "Version": POLICY_LANGUAGE_VERSION,
            "Statement": statements
        }
        return policy

    def add_by_arn_and_access_level(self, db_session, arn_list, access_level, conditions_block=None):
        """

        """
        for arn in arn_list:
            service_prefix = get_service_from_arn(arn)
            service_action_data = get_action_data(db_session, service_prefix, "*")
            for service_prefix in service_action_data:
                for row in service_action_data[service_prefix]:
                    if does_arn_match(arn, row["resource_arn_format"]) and row["access_level"] == access_level:
                        raw_arn_format = row["resource_arn_format"]
                        resource_type_name = get_resource_type_name_with_raw_arn(db_session, raw_arn_format)
                        sid_namespace = create_policy_sid_namespace(service_prefix, access_level, resource_type_name)
                        actions = get_actions_with_arn_type_and_access_level(db_session, service_prefix,
                                                                             resource_type_name, access_level)
                        # Make supplied actions lowercase
                        supplied_actions = [x.lower() for x in actions]
                        dependent_actions = get_dependent_actions_only(db_session, supplied_actions)
                        # List comprehension to get all dependent actions that are not in the supplied actions.
                        dependent_actions = [x for x in dependent_actions if x not in supplied_actions]
                        if len(dependent_actions) > 0:
                            for dep_action in dependent_actions:
                                self.add_action_without_resource_constraint(str.lower(dep_action))

                        temp_sid_dict = {
                            'arn': [arn],
                            'service': service_prefix,
                            'access_level': access_level,
                            'arn_format': raw_arn_format,
                            'actions': actions,
                            'conditions': []  # TODO: Add conditions
                        }
                        if sid_namespace in self.sids.keys():
                            # If the ARN already exists there, skip it.
                            if arn in self.sids[sid_namespace]["arn"]:
                                continue
                            # Otherwise, just append the ARN
                            else:
                                self.sids[sid_namespace]["arn"].append(arn)
                        # If it did not exist before at all, create it.
                        else:
                            self.sids[sid_namespace] = temp_sid_dict

    def add_action_without_resource_constraint(self, action):
        sid_namespace = "MultMultNone"
        temp_sid_dict = {
            'arn': ["*"],
            'service': "Mult",
            'access_level': "Mult",
            'arn_format': "*",
            'actions': [action]
        }
        if sid_namespace in self.sids.keys():
            if action not in self.sids[sid_namespace]["actions"]:
                self.sids[sid_namespace]["actions"].append(action)
        else:
            self.sids[sid_namespace] = temp_sid_dict
        return self.sids

    def add_by_list_of_actions(self, db_session, supplied_actions):
        """
        Takes a list of actions, queries the database for corresponding arns, adds them to the object.
        :param db_session: SQLAlchemy database session object
        :param supplied_actions: A list of supplied actions
        """
        # Make supplied actions lowercase
        supplied_actions = [x.lower() for x in supplied_actions]
        # actions_list = get_dependent_actions(db_session, supplied_actions)
        dependent_actions = get_dependent_actions_only(db_session, supplied_actions)
        # List comprehension to get all dependent actions that are not in the supplied actions.
        dependent_actions = [x for x in dependent_actions if x not in supplied_actions]

        arns_matching_supplied_actions = []

        # arns_matching_supplied_actions is a list of dicts.
        # It must do this rather than dictionaries because there will be duplicate
        #     values by nature of how the entries in the IAM database are structured.
        # I'll provide the example values here to improve readability.

        for action in supplied_actions:
            service_name, action_name = action.split(':')
            action_data = get_action_data(db_session, service_name, action_name)
            for row in action_data[service_name]:
                if row["resource_arn_format"] not in arns_matching_supplied_actions:
                    arns_matching_supplied_actions.append(
                        {
                            "resource_arn_format": row["resource_arn_format"],
                            "access_level": row["access_level"],
                            "action": row["action"]
                        }
                        # [row["resource_arn_format"], row["access_level"], row["action"]])
                    )

        # arns_matching_supplied_actions = [{
        #         "resource_arn_format": "*",
        #         "access_level": "Write",
        #         "action": "kms:createcustomkeystore"
        #     },{
        #         "resource_arn_format": "arn:${Partition}:kms:${Region}:${Account}:key/${KeyId}",
        #         "access_level": "Permissions management",
        #         "action": "kms:creategrant"
        #     },{
        #         "resource_arn_format": "*",
        #         "access_level": "Permissions management",
        #         "action": "kms:creategrant"
        # }]

        # Identify the actions that do not support resource constraints
        # If that's the case, add it to the wildcard namespace. Otherwise, don't add it.

        actions_without_resource_constraints = []
        for item in arns_matching_supplied_actions:
            if item["resource_arn_format"] is not "*":
                self.add_by_arn_and_access_level(db_session, [item["resource_arn_format"]], item["access_level"])
            else:
                actions_without_resource_constraints.append(item["action"])

        # If there are any dependent actions, we need to add them without resource constraints.
        # Otherwise, we get into issues where the amount of extra SIDs will balloon.
        # Also, the user has no way of knowing what those dependent actions are beforehand.
        # TODO: This is, in fact, a great opportunity to introduce conditions. But we aren't there yet.
        if len(dependent_actions) > 0:
            for dep_action in dependent_actions:
                self.add_action_without_resource_constraint(str.lower(dep_action))
        # Now, because add_by_arn_and_access_level() adds all actions under an access level, we have to
        # remove all actions that do not match the supplied_actions. This is done in-place.
        self.remove_actions_not_matching_these(supplied_actions + dependent_actions)
        for action in actions_without_resource_constraints:
            self.add_action_without_resource_constraint(action)
        self.remove_actions_duplicated_in_wildcard_arn()
        rendered_policy = self.get_rendered_policy(db_session)
        return rendered_policy

    def process_template(self, db_session, cfg):
        try:
            for template in cfg:
                if template == 'policy_with_crud_levels':
                    # for policy in cfg[template]:
                    if 'wildcard' in cfg['policy_with_crud_levels'].keys():
                        provided_wildcard_actions = cfg['policy_with_crud_levels']['wildcard']
                        if isinstance(provided_wildcard_actions, list):
                            verified_wildcard_actions = remove_actions_that_are_not_wildcard_arn_only(
                                db_session, provided_wildcard_actions)
                            if len(verified_wildcard_actions) > 0:
                                self.add_by_list_of_actions(db_session, verified_wildcard_actions)
                    if 'read' in cfg['policy_with_crud_levels'].keys():
                        if cfg['policy_with_crud_levels']['read'] is not None:
                            self.add_by_arn_and_access_level(
                                db_session, cfg['policy_with_crud_levels']['read'], "Read")
                    if 'write' in cfg['policy_with_crud_levels'].keys():
                        if cfg['policy_with_crud_levels']['write'] is not None:
                            self.add_by_arn_and_access_level(
                                db_session, cfg['policy_with_crud_levels']['write'], "Write")
                    if 'list' in cfg['policy_with_crud_levels'].keys():
                        if cfg['policy_with_crud_levels']['list'] is not None:
                            self.add_by_arn_and_access_level(
                                db_session, cfg['policy_with_crud_levels']['list'], "List")
                    if 'permissions-management' in cfg['policy_with_crud_levels'].keys():
                        if cfg['policy_with_crud_levels']['permissions-management'] is not None:
                            self.add_by_arn_and_access_level(
                                db_session,
                                cfg['policy_with_crud_levels']['permissions-management'],
                                "Permissions management")
                    if 'tagging' in cfg['policy_with_crud_levels'].keys():
                        if cfg['policy_with_crud_levels']['tagging'] is not None:
                            self.add_by_arn_and_access_level(
                                db_session, cfg['policy_with_crud_levels']['tagging'], "Tagging")

                if template == 'policy_with_actions':
                    # for policy in cfg[template]:
                    if 'actions' in cfg['policy_with_actions'].keys():
                        if cfg['policy_with_actions']['actions'] is not None:
                            self.add_by_list_of_actions(db_session, cfg['policy_with_actions']['actions'])

        except IndexError:
            raise Exception("IndexError: list index out of range. This is likely due to an ARN in your list "
                            "equaling ''. Please evaluate your YML file and try again.")
        rendered_policy = self.get_rendered_policy(db_session)
        return rendered_policy

    def remove_actions_not_matching_these(self, actions_to_keep):
        """
        :param actions_to_keep: A list of actions to leave in the policy. All actions not in this list are removed.
        """
        actions_to_keep = get_lowercase_action_list(actions_to_keep)
        for sid in self.sids:
            placeholder_actions_list = []
            for action in self.sids[sid]["actions"]:
                # if the action is not in the list of selected actions, don't copy it to the placeholder list
                if action in actions_to_keep:
                    placeholder_actions_list.append(action)
            # Clear the list and then extend it to include the updated actions only
            self.sids[sid]["actions"].clear()
            self.sids[sid]["actions"].extend(placeholder_actions_list.copy())

        # remove_sids_with_empty_action_lists
        # Now that we've removed a bunch of actions, if there are SID groups without any actions,
        # remove them so we don't get SIDs with empty action lists
        for sid in self.sids:
            # If the size is zero, add it to the indexes_to_delete list.
            if len(self.sids[sid]["actions"]) == 0:
                del self.sids[sid]

    def remove_actions_duplicated_in_wildcard_arn(self):
        """
        Removes actions from the object that are in a resource-specific ARN, as well as the `*` resource.
        For example, if ssm:GetParameter is restricted to a specific parameter path, as well as `*`, then we want to
        remove the `*` option to force least privilege.
        """
        actions_under_wildcard_resources = []
        actions_under_wildcard_resources_to_nuke = []

        # Build a temporary list. Contains actions in MultMultNone SID (where resources = "*")
        for sid in self.sids:
            if self.sids[sid]["arn_format"] == "*":
                actions_under_wildcard_resources.extend(self.sids[sid]["actions"])

        # If the actions under the MultMultNone SID exist under other SIDs
        if len(actions_under_wildcard_resources) > 0:
            for sid in self.sids:
                if '*' not in self.sids[sid]["arn_format"]:
                    for action in actions_under_wildcard_resources:
                        if action in self.sids[sid]["actions"]:
                            # add it to a list of actions to nuke when they are under other SIDs
                            actions_under_wildcard_resources_to_nuke.append(action)

        # If there are actions that we need to remove from SIDs outside of MultMultNone SID
        if len(actions_under_wildcard_resources_to_nuke) > 0:
            for sid in self.sids:
                if '*' in self.sids[sid]["arn_format"]:
                    for action in actions_under_wildcard_resources_to_nuke:
                        try:
                            self.sids[sid]["actions"].remove(str(action))
                        except BaseException:  # pylint: disable=broad-except
                            logger.debug("Removal not successful")


def remove_actions_that_are_not_wildcard_arn_only(db_session, actions_list):
    """
    Given a list of actions, remove the ones that CAN be restricted to ARNs, leaving only the ones that cannot.

    :param db_session: SQL Alchemy database session object
    :param actions_list: A list of actions
    :return: An updated list of actions
    :rtype: list
    """
    # remove duplicates, if there are any
    actions_list = list(dict.fromkeys(actions_list))
    actions_list_placeholder = []

    for action in actions_list:
        service_name, action_name = action.split(':')
        rows = get_actions_that_support_wildcard_arns_only(db_session, service_name)
        for row in rows:
            if row == action:
                actions_list_placeholder.append(f"{service_name}:{action_name}")
    return actions_list_placeholder
