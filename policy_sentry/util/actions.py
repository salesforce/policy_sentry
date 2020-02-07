"""
Text operations specific to IAM actions
"""


def get_service_from_action(action):
    """
    Returns the service name from a service:action combination
    :param action: ec2:DescribeInstance
    :return: ec2
    """
    service, action_name = action.split(":")  # pylint: disable=unused-variable
    return str.lower(service)


def get_action_name_from_action(action):
    """
    Returns the lowercase action name from a service:action combination
    :param action: ec2:DescribeInstance
    :return: describeinstance
    """
    service, action_name = action.split(":")  # pylint: disable=unused-variable
    return str.lower(action_name)


def get_lowercase_action_list(action_list):
    """
    Given a list of actions, return the list but in lowercase format
    """
    new_action_list = []
    for action in action_list:
        new_action_list.append(str.lower(action))
    return new_action_list


def get_full_action_name(service, action_name):
    """
    Gets the proper formatting for an action - the service, plus colon, plus action name.
    :param service: service name, like s3
    :param action_name: action name, like createbucket
    :return: the resulting string
    """
    action = service + ":" + action_name
    return action
