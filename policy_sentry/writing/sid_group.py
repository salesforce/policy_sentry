"""
sid_group indicates that this is a collection of policy-related data organized by their SIDs
"""
import logging
import re
from policy_sentry.querying.all import get_all_actions
from policy_sentry.querying.actions import (
    get_action_data,
    get_actions_with_arn_type_and_access_level,
    get_dependent_actions,
    get_actions_that_support_wildcard_arns_only,
    get_actions_at_access_level_that_support_wildcard_arns_only,
)
from policy_sentry.querying.arns import get_resource_type_name_with_raw_arn
from policy_sentry.util.arns import does_arn_match, get_service_from_arn
from policy_sentry.util.text import capitalize_first_character
from policy_sentry.writing.minimize import minimize_statement_actions
from policy_sentry.writing.validate import check_actions_schema, check_crud_schema
from policy_sentry.shared.constants import POLICY_LANGUAGE_VERSION
from policy_sentry.util.actions import get_lowercase_action_list

logger = logging.getLogger(__name__)


class SidGroup:
    """
    This class is critical to the creation of least privilege policies.
    It uses the SIDs as namespaces. The namespaces follow this format:
        {Servicename}{Accesslevel}{Resourcetypename}

    So, a resulting statement's SID might look like 'S3ListBucket'

    If a condition key is supplied (like s3:RequestJob), the SID string will be significantly longer.
    It will resemble this format:
            {Servicename}{Accesslevel}{Resourcetypename}{Conditionkeystring}{Conditiontypestring}{Conditionkeyvalue}
    For example: EC2 write actions on the security-group resource, using the following condition map:
        "Condition": {
            "StringEquals": {"ec2:ResourceTag/Owner": "${aws:username}"}
        }
    The resulting SID would be:
        Ec2WriteSecuritygroupResourcetagownerStringequalsAwsusername
    Or, for actions that support wildcard ARNs only, an example could be:
        Ec2WriteMultResourcetagownerStringequalsAwsusername
    """

    def __init__(self):
        # Dict instead of list
        # sids instead of ARN
        self.sids = {}
        self.universal_conditions = {}

    def get_sid_group(self):
        """
        Get the whole SID group as JSON
        """
        return self.sids

    def get_sid(self, sid):
        """Get a single group by the SID identifier"""
        if self.sids[sid]:
            return self.sids[sid]
        else:
            raise Exception(f"No SID with the value of {sid}")

    def list_sids(self):
        """
        Get a list of all of them by their identifiers

        :rtype: list
        """
        return self.sids.keys()

    def get_universal_conditions(self):
        """
        Get the universal conditions maps back as a dict

        :rtype: dict
        """
        return self.universal_conditions

    def get_rendered_policy(self, db_session, minimize=None):
        """
        Get the JSON rendered policy

        :param db_session: SQLAlchemy database session
        :param minimize: Reduce the character count of policies without creating overlap with other action names
        :rtype: dict
        """
        statements = []
        # Only set the actions to lowercase if minimize is provided
        all_actions = get_all_actions(db_session, lowercase=True)

        # render the policy
        for sid in self.sids:
            actions = self.sids[sid]["actions"]
            if len(actions) == 0:
                logger.debug(f"No actions for sid {sid}")
                continue
            if minimize is not None and isinstance(minimize, int):
                logger.debug("Minimizing statements...")
                actions = minimize_statement_actions(
                    actions, all_actions, minchars=minimize
                )
            logger.debug(f"Adding statement with SID {sid}")
            logger.debug(f"{sid} SID has the actions: {actions}")
            logger.debug(f"{sid} SID has the resources: {self.sids[sid]['arn']}")

            statements.append(
                {
                    "Sid": sid,
                    "Effect": "Allow",
                    "Action": actions,
                    "Resource": self.sids[sid]["arn"],
                }
            )
        policy = {"Version": POLICY_LANGUAGE_VERSION, "Statement": statements}
        return policy

    # pylint: disable=unused-argument
    def add_by_arn_and_access_level(
        self, db_session, arn_list, access_level, conditions_block=None
    ):
        """
        This adds the user-supplied ARN(s), service prefixes, access levels, and condition keys (if applicable) given by the user.
        It derives the list of IAM actions based on the user's requested ARNs and access levels.

        :param db_session: SQLAlchemy database session
        :param arn_list: Just a list of resource ARNs.
        :param access_level: "Read", "List", "Tagging", "Write", or "Permissions management"
        :param conditions_block: Optionally, a condition block with one or more conditions
        """
        for arn in arn_list:
            service_prefix = get_service_from_arn(arn)
            service_action_data = get_action_data(db_session, service_prefix, "*")
            for service_prefix in service_action_data:
                for row in service_action_data[service_prefix]:
                    if (
                        does_arn_match(arn, row["resource_arn_format"])
                        and row["access_level"] == access_level
                    ):
                        raw_arn_format = row["resource_arn_format"]
                        resource_type_name = get_resource_type_name_with_raw_arn(
                            db_session, raw_arn_format
                        )
                        sid_namespace = create_policy_sid_namespace(
                            service_prefix, access_level, resource_type_name
                        )
                        actions = get_actions_with_arn_type_and_access_level(
                            db_session, service_prefix, resource_type_name, access_level
                        )
                        # Make supplied actions lowercase
                        # supplied_actions = [x.lower() for x in actions]
                        supplied_actions = actions.copy()
                        dependent_actions = get_dependent_actions(
                            db_session, supplied_actions
                        )
                        # List comprehension to get all dependent actions that are not in the supplied actions.
                        dependent_actions = [
                            x for x in dependent_actions if x not in supplied_actions
                        ]
                        if len(dependent_actions) > 0:
                            for dep_action in dependent_actions:
                                self.add_action_without_resource_constraint(dep_action)
                                # self.add_action_without_resource_constraint(
                                #     str.lower(dep_action)
                                # )

                        temp_sid_dict = {
                            "arn": [arn],
                            "service": service_prefix,
                            "access_level": access_level,
                            "arn_format": raw_arn_format,
                            "actions": actions,
                            "conditions": [],  # TODO: Add conditions
                        }
                        if sid_namespace in self.sids.keys():
                            # If the ARN already exists there, skip it.
                            if arn not in self.sids[sid_namespace]["arn"]:
                                self.sids[sid_namespace]["arn"].append(arn)
                        # If it did not exist before at all, create it.
                        else:
                            self.sids[sid_namespace] = temp_sid_dict

    def add_action_without_resource_constraint(self, action):
        """
        This handles the cases where certain actions do not handle resource constraints - either by AWS, or for flexibility when adding dependent actions.

        :param action: The single action to add to the MultMultNone SID namespace. For instance, s3:ListAllMyBuckets
        """
        sid_namespace = "MultMultNone"
        temp_sid_dict = {
            "arn": ["*"],
            "service": "Mult",
            "access_level": "Mult",
            "arn_format": "*",
            "actions": [action],
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
        # supplied_actions = [x.lower() for x in supplied_actions]
        # actions_list = get_dependent_actions(db_session, supplied_actions)
        dependent_actions = get_dependent_actions(db_session, supplied_actions)
        # List comprehension to get all dependent actions that are not in the supplied actions.
        dependent_actions = [x for x in dependent_actions if x not in supplied_actions]
        logger.debug("Adding by list of actions")
        logger.debug(f"Supplied actions: {str(supplied_actions)}")
        logger.debug(f"Dependent actions: {str(dependent_actions)}")
        arns_matching_supplied_actions = []

        # arns_matching_supplied_actions is a list of dicts.
        # It must do this rather than dictionaries because there will be duplicate
        #     values by nature of how the entries in the IAM database are structured.
        # I'll provide the example values here to improve readability.

        for action in supplied_actions:
            service_name, action_name = action.split(":")
            action_data = get_action_data(db_session, service_name, action_name)
            for row in action_data[service_name]:
                if row["resource_arn_format"] not in arns_matching_supplied_actions:
                    arns_matching_supplied_actions.append(
                        {
                            "resource_arn_format": row["resource_arn_format"],
                            "access_level": row["access_level"],
                            "action": row["action"],
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
            if item["resource_arn_format"] != "*":
                self.add_by_arn_and_access_level(
                    db_session, [item["resource_arn_format"]], item["access_level"]
                )
            else:
                actions_without_resource_constraints.append(item["action"])

        # If there are any dependent actions, we need to add them without resource constraints.
        # Otherwise, we get into issues where the amount of extra SIDs will balloon.
        # Also, the user has no way of knowing what those dependent actions are beforehand.
        # TODO: This is, in fact, a great opportunity to introduce conditions. But we aren't there yet.
        if len(dependent_actions) > 0:
            for dep_action in dependent_actions:
                self.add_action_without_resource_constraint(dep_action)
                # self.add_action_without_resource_constraint(str.lower(dep_action))
        # Now, because add_by_arn_and_access_level() adds all actions under an access level, we have to
        # remove all actions that do not match the supplied_actions. This is done in-place.
        logger.debug(
            "Purging actions that do not match the requested actions and dependent actions"
        )
        logger.debug(f"Supplied actions: {str(supplied_actions)}")
        logger.debug(f"Dependent actions: {str(dependent_actions)}")
        self.remove_actions_not_matching_these(supplied_actions + dependent_actions)
        for action in actions_without_resource_constraints:
            logger.debug(
                f"Deliberately adding the action {action} without resource constraints"
            )
            self.add_action_without_resource_constraint(action)
        logger.debug(
            "Removing actions that are in the wildcard arn (Resources = '*') as well as other statements that have resource constraints"
        )
        self.remove_actions_duplicated_in_wildcard_arn()
        logger.debug("Getting the rendered policy")
        rendered_policy = self.get_rendered_policy(db_session)
        return rendered_policy

    def process_template(self, db_session, cfg, minimize=None):
        """
        Process the Policy Sentry template as a dict. This auto-detects whether or not the file is in CRUD mode or Actions mode.

        :param db_session: SQLAlchemy database session object
        :param cfg: The loaded YAML as a dict. Must follow Policy Sentry dictated format.
        :param minimize: Minimize the resulting statement with *safe* usage of wildcards to reduce policy length. Set this to the character length you want - for example, 0, or 4. Defaults to none.
        """
        # try:
        if "mode" in cfg.keys():
            if cfg["mode"] == "crud":
                logger.debug("CRUD mode selected")
                check_crud_schema(cfg)
                if "wildcard-only" in cfg.keys():
                    if "single-actions" in cfg["wildcard-only"]:
                        if cfg["wildcard-only"]["single-actions"]:
                            if cfg["wildcard-only"]["single-actions"][0] != "":
                                provided_wildcard_actions = cfg["wildcard-only"][
                                    "single-actions"
                                ]
                                logger.debug(
                                    f"Requested wildcard-only actions: {str(provided_wildcard_actions)}"
                                )
                                self.add_wildcard_only_actions(
                                    db_session, provided_wildcard_actions
                                )
                    if "service-read" in cfg["wildcard-only"]:
                        if cfg["wildcard-only"]["service-read"]:
                            if cfg["wildcard-only"]["service-read"][0] != "":
                                service_read = cfg["wildcard-only"]["service-read"]
                                logger.debug(
                                    f"Requested wildcard-only actions: {str(service_read)}"
                                )
                                self.add_wildcard_only_actions_matching_services_and_access_level(
                                    db_session, service_read, "Read"
                                )
                    if "service-write" in cfg["wildcard-only"]:
                        if cfg["wildcard-only"]["service-write"]:
                            if cfg["wildcard-only"]["service-write"][0] != "":
                                service_write = cfg["wildcard-only"]["service-write"]
                                logger.debug(
                                    f"Requested wildcard-only actions: {str(service_write)}"
                                )
                                self.add_wildcard_only_actions_matching_services_and_access_level(
                                    db_session, service_write, "Write"
                                )
                    if "service-list" in cfg["wildcard-only"]:
                        if cfg["wildcard-only"]["service-list"]:
                            if cfg["wildcard-only"]["service-list"][0] != "":
                                service_list = cfg["wildcard-only"]["service-list"]
                                logger.debug(
                                    f"Requested wildcard-only actions: {str(service_list)}"
                                )
                                self.add_wildcard_only_actions_matching_services_and_access_level(
                                    db_session, service_list, "List"
                                )
                    if "service-tagging" in cfg["wildcard-only"]:
                        if cfg["wildcard-only"]["service-tagging"]:
                            if cfg["wildcard-only"]["service-tagging"][0] != "":
                                service_tagging = cfg["wildcard-only"][
                                    "service-tagging"
                                ]
                                logger.debug(
                                    f"Requested wildcard-only actions: {str(service_tagging)}"
                                )
                                self.add_wildcard_only_actions_matching_services_and_access_level(
                                    db_session, service_tagging, "Tagging"
                                )
                    if "service-permissions-management" in cfg["wildcard-only"]:
                        if cfg["wildcard-only"]["service-permissions-management"]:
                            if (
                                cfg["wildcard-only"]["service-permissions-management"][
                                    0
                                ]
                                != ""
                            ):

                                service_permissions_management = cfg["wildcard-only"][
                                    "service-permissions-management"
                                ]
                                logger.debug(
                                    f"Requested wildcard-only actions: {str(service_permissions_management)}"
                                )
                                self.add_wildcard_only_actions_matching_services_and_access_level(
                                    db_session,
                                    service_permissions_management,
                                    "Permissions management",
                                )
                if "read" in cfg.keys():
                    if cfg["read"] is not None and cfg["read"][0] != "":
                        logger.debug(f"Requested access to arns: {str(cfg['read'])}")
                        self.add_by_arn_and_access_level(
                            db_session, cfg["read"], "Read"
                        )
                if "write" in cfg.keys():
                    if cfg["write"] is not None and cfg["write"][0] != "":
                        logger.debug(f"Requested access to arns: {str(cfg['write'])}")
                        self.add_by_arn_and_access_level(
                            db_session, cfg["write"], "Write"
                        )
                if "list" in cfg.keys():
                    if cfg["list"] is not None and cfg["list"][0] != "":
                        logger.debug(f"Requested access to arns: {str(cfg['list'])}")
                        self.add_by_arn_and_access_level(
                            db_session, cfg["list"], "List"
                        )
                if "permissions-management" in cfg.keys():
                    if (
                        cfg["permissions-management"] is not None
                        and cfg["permissions-management"][0] != ""
                    ):
                        logger.debug(
                            f"Requested access to arns: {str(cfg['permissions-management'])}"
                        )
                        self.add_by_arn_and_access_level(
                            db_session,
                            cfg["permissions-management"],
                            "Permissions management",
                        )
                if "tagging" in cfg.keys():
                    if cfg["tagging"] is not None and cfg["tagging"][0] != "":
                        logger.debug(f"Requested access to arns: {str(cfg['tagging'])}")
                        self.add_by_arn_and_access_level(
                            db_session, cfg["tagging"], "Tagging"
                        )

            if cfg["mode"] == "actions":
                check_actions_schema(cfg)
                if "actions" in cfg.keys():
                    if cfg["actions"] is not None and cfg["actions"][0] != "":
                        self.add_by_list_of_actions(db_session, cfg["actions"])

        rendered_policy = self.get_rendered_policy(db_session, minimize)
        return rendered_policy

    def add_wildcard_only_actions(self, db_session, provided_wildcard_actions):
        """
        Given a list of IAM actions, add individual IAM Actions that do not support resource constraints to the MultMultNone SID

        :param db_session: SQLAlchemy database session
        :param provided_wildcard_actions: list actions provided by the user.
        """
        if isinstance(provided_wildcard_actions, list):
            verified_wildcard_actions = remove_actions_that_are_not_wildcard_arn_only(
                db_session, provided_wildcard_actions
            )
            if len(verified_wildcard_actions) > 0:
                logger.debug(
                    "Attempting to add the following actions to the policy: %s",
                    verified_wildcard_actions,
                )
                self.add_by_list_of_actions(db_session, verified_wildcard_actions)
                logger.debug(
                    "Added the following wildcard-only actions to the policy: %s",
                    verified_wildcard_actions,
                )

    def add_wildcard_only_actions_matching_services_and_access_level(
        self, db_session, services, access_level
    ):
        """
        :param db_session: SQLAlchemy database session
        :param services: A list of AWS services
    :param access_level: An access level as it is written in the database, such as 'Read', 'Write', 'List', 'Permisssions management', or 'Tagging'
        """
        wildcard_only_actions_to_add = []
        for service in services:
            actions = get_actions_at_access_level_that_support_wildcard_arns_only(
                db_session, service, access_level
            )
            wildcard_only_actions_to_add.extend(actions)
        self.add_wildcard_only_actions(db_session, wildcard_only_actions_to_add)

    def remove_actions_not_matching_these(self, actions_to_keep):
        """
        :param actions_to_keep: A list of actions to leave in the policy. All actions not in this list are removed.
        """
        actions_to_keep = get_lowercase_action_list(actions_to_keep)
        for sid in self.sids:
            placeholder_actions_list = []
            for action in self.sids[sid]["actions"]:
                # if the action is not in the list of selected actions, don't copy it to the placeholder list
                if action.lower() in actions_to_keep:
                    placeholder_actions_list.append(action)
            # Clear the list and then extend it to include the updated actions only
            self.sids[sid]["actions"].clear()
            self.sids[sid]["actions"].extend(placeholder_actions_list.copy())

        # Now that we've removed a bunch of actions, if there are SID groups without any actions,
        # remove them so we don't get SIDs with empty action lists
        self.remove_sids_with_empty_action_lists()

    def remove_sids_with_empty_action_lists(self):
        """
        Now that we've removed a bunch of actions, if there are SID groups without any actions,
            remove them so we don't get SIDs with empty action lists
        """
        sid_namespaces_to_delete = []
        for sid in self.sids:
            if len(self.sids[sid]["actions"]) > 0:
                pass
            # If the size is zero, add it to the indexes_to_delete list.
            else:
                sid_namespaces_to_delete.append(sid)
        # Loop through sid_namespaces_to_delete in reverse order (so we delete index
        # 10 before index 8, for example)
        if len(sid_namespaces_to_delete) > 0:
            for i in reversed(range(len(sid_namespaces_to_delete))):
                del self.sids[sid_namespaces_to_delete[i]]

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
                if "*" not in self.sids[sid]["arn_format"]:
                    for action in actions_under_wildcard_resources:
                        if action in self.sids[sid]["actions"]:
                            # add it to a list of actions to nuke when they are under other SIDs
                            actions_under_wildcard_resources_to_nuke.append(action)

        # If there are actions that we need to remove from SIDs outside of MultMultNone SID
        if len(actions_under_wildcard_resources_to_nuke) > 0:
            for sid in self.sids:
                if "*" in self.sids[sid]["arn_format"]:
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
        try:
            service_name, action_name = action.split(":")
        except ValueError as v_e:
            # We will skip the action because this likely means that the wildcard action provided is not valid.
            logger.debug(v_e)
            logger.debug(
                "The value provided in wildcard-only section is not formatted properly."
            )
            continue
        rows = get_actions_that_support_wildcard_arns_only(db_session, service_name)
        for row in rows:
            if row.lower() == action.lower():
                actions_list_placeholder.append(f"{service_name}:{action_name}")
    return actions_list_placeholder


def create_policy_sid_namespace(
    service, access_level, resource_type_name, condition_block=None
):
    """
    Simply generates the SID name. The SID groups ARN types that share an access level.

    For example, S3 objects vs. SSM Parameter have different ARN types - as do S3 objects vs S3 buckets. That's how we choose to group them.

    :param service: "ssm"
    :param access_level: "Read"
    :param resource_type_name: "parameter"
    :param condition_block: {"condition_key_string": "ec2:ResourceTag/purpose", "condition_type_string": "StringEquals", "condition_value": "test"}
    :return: SsmReadParameter
    :rtype: str
    """
    # Sanitize the resource_type_name; otherwise we hit some list conversion
    # errors
    resource_type_name = re.sub("[^A-Za-z0-9]+", "", resource_type_name)
    # Also remove the space from the Access level, if applicable. This only
    # applies for "Permissions management"
    access_level = re.sub("[^A-Za-z0-9]+", "", access_level)
    sid_namespace_prefix = (
        capitalize_first_character(service)
        + capitalize_first_character(access_level)
        + capitalize_first_character(resource_type_name)
    )

    if condition_block:
        condition_key_namespace = re.sub(
            "[^A-Za-z0-9]+", "", condition_block["condition_key_string"]
        )
        condition_type_namespace = condition_block["condition_type_string"]
        condition_value_namespace = re.sub(
            "[^A-Za-z0-9]+", "", condition_block["condition_value"]
        )
        sid_namespace_condition_suffix = (
            f"{capitalize_first_character(condition_key_namespace)}"
            f"{capitalize_first_character(condition_type_namespace)}"
            f"{capitalize_first_character(condition_value_namespace)}"
        )
        sid_namespace = sid_namespace_prefix + sid_namespace_condition_suffix
    else:
        sid_namespace = sid_namespace_prefix
    return sid_namespace
