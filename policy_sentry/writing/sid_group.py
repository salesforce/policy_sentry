"""
sid_group indicates that this is a collection of policy-related data organized by their SIDs
"""
import copy
import logging
from policy_sentry.querying.all import get_all_actions
from policy_sentry.querying.actions import get_action_data, get_actions_with_arn_type_and_access_level
from policy_sentry.querying.arns import get_arn_data, get_resource_type_name_with_raw_arn
from policy_sentry.writing.policy import create_policy_sid_namespace
from policy_sentry.util.arns import does_arn_match
from policy_sentry.writing.minimize import minimize_statement_actions
from policy_sentry.shared.constants import POLICY_LANGUAGE_VERSION

logger = logging.getLogger(__name__)

sid_group = {
    "sid_namespace": {
        "arns": [],
        "service": "",
        "access_level": "",
        "arn_format": "",
        "actions": "",
        "conditions": ""
    }
}


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

        for sid in self.sids:
            actions = self.sids[sid]["actions"]
            if minimize is not None and isinstance(minimize, int):
                actions = minimize_statement_actions(self.sids[sid]["actions"], all_actions, minchars=minimize)
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

    # TODO: Add conditions as an optional thing here.
    def add_by_arn_and_access_level(self, db_session, arn_list, access_level):
        for arn in arn_list:
            # service_prefix = arn.split(':', 5)[2]
            service_action_data = get_action_data(db_session, arn.split(':', 5)[2], "*")
            for service_prefix in service_action_data:
                for row in service_action_data[service_prefix]:
                    if does_arn_match(arn, row["resource_arn_format"]) and row["access_level"] == access_level:
                        raw_arn_format = row["resource_arn_format"]
                        # service_arn_data = get_arn_data(db_session, serv, "*")
                        resource_type_name = get_resource_type_name_with_raw_arn(db_session, raw_arn_format)
                        sid_namespace = create_policy_sid_namespace(service_prefix, access_level, resource_type_name)
                        actions = get_actions_with_arn_type_and_access_level(db_session, service_prefix,
                                                                             resource_type_name, access_level)
                        temp_sid_dict = {
                            'arn': [arn],
                            'service': service_prefix,
                            'access_level': access_level,
                            'arn_format': raw_arn_format,
                            'actions': actions
                        }
                        if sid_namespace in self.sids.keys():
                            # if the exact value already exists, skip it.
                            # if self.sids[sid_namespace] == temp_sid_dict:
                            #     continue
                            # # Or, if the ARN already exists there, skip it.
                            if arn in self.sids[sid_namespace]["arn"]:
                                continue
                            # Otherwise, just append the ARN
                            else:
                                self.sids[sid_namespace]["arn"].append(arn)
                        # If it did not exist before at all, create it.
                        else:
                            self.sids[sid_namespace] = temp_sid_dict

    def process_template(self, db_session, cfg):
        try:
            for template in cfg:
                if template == 'policy_with_crud_levels':
                    for policy in cfg[template]:
                        if 'read' in policy.keys():
                            if policy['read'] is not None:
                                self.add_by_arn_and_access_level(
                                    db_session, policy['read'], "Read")
                        if 'write' in policy.keys():
                            if policy['write'] is not None:
                                self.add_by_arn_and_access_level(
                                    db_session, policy['write'], "Write")
                        if 'list' in policy.keys():
                            if policy['list'] is not None:
                                self.add_by_arn_and_access_level(
                                    db_session, policy['list'], "List")
                        if 'permissions-management' in policy.keys():
                            if policy['permissions-management'] is not None:
                                self.add_by_arn_and_access_level(
                                    db_session,
                                    policy['permissions-management'],
                                    "Permissions management")
                        if 'tagging' in policy.keys():
                            if policy['tagging'] is not None:
                                self.add_by_arn_and_access_level(
                                    db_session, policy['tagging'], "Tagging")
        except IndexError:
            raise Exception("IndexError: list index out of range. This is likely due to an ARN in your list "
                            "equaling ''. Please evaluate your YML file and try again.")
        rendered_policy = self.get_rendered_policy(db_session)
        return rendered_policy


