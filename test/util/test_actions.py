from policy_sentry.util.actions import (
    get_service_from_action,
    get_action_name_from_action,
    get_full_action_name,
)


def test_get_service_from_action():
    # given
    action = "ec2:DescribeInstance"

    # when
    service = get_service_from_action(action=action)

    # then
    assert service == "ec2"


def test_get_action_name_from_action():
    # given
    action = "ec2:DescribeInstance"

    # when
    service = get_action_name_from_action(action=action)

    # then
    assert service == "describeinstance"


def test_get_full_action_name():
    # given
    service = "ec2"
    action_name = "DescribeInstance"

    # when
    action = get_full_action_name(service=service, action_name=action_name)

    # then
    assert action == "ec2:DescribeInstance"
