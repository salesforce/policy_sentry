"""IAM Database queries that are not specific to either the Actions, ARNs, or Condition Keys tables."""
from sqlalchemy import and_
from policy_sentry.shared.database import ActionTable


def get_all_actions(db_session, lowercase=False):
    """
    Gets a huge list of all IAM actions. This is used as part of the policyuniverse approach to minimizing
    IAM Policies to meet AWS-mandated character limits on policies.

    :param db_session: SQLAlchemy database session object
    :param lowercase: Set to true to have the list of actions be in all lowercase strings.
    :return: A list of all actions present in the database.
    """
    all_actions = set()
    rows = db_session.query(ActionTable.service, ActionTable.name).distinct(
        and_(ActionTable.service, ActionTable.name)
    )
    for row in rows:
        if lowercase:
            all_actions.add(str(row.service.lower() + ":" + row.name.lower()))
        else:
            all_actions.add(str(row.service + ":" + row.name))
    # Remove duplicates
    # all_actions = set(dict.fromkeys(all_actions))
    return all_actions


def get_all_service_prefixes(db_session):
    """
    Gets all the AWS service prefixes from the actions table.

    If the action table does NOT have specific IAM actions (and therefore only supports * actions),
    then it will not be included in the response.

    :param db_session: The SQLAlchemy database session
    :return: A list of all AWS service prefixes present in the table.
    """
    service_prefixes = []
    rows = db_session.query(ActionTable.service).distinct(ActionTable.service)
    for row in rows:
        if row.service not in service_prefixes:
            service_prefixes.append(row.service)
    # Remove duplicates
    service_prefixes = list(dict.fromkeys(service_prefixes))  # remove duplicates
    service_prefixes.sort()
    return service_prefixes
