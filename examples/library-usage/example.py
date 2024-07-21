#! /usr/bin/env python

from policy_sentry.querying.actions import (
    get_actions_for_service,
    get_actions_with_access_level,
)


def example() -> None:
    actions = get_actions_for_service("cloud9")
    print(actions)
    actions = get_actions_with_access_level("s3", "Permissions management")
    print(actions)


if __name__ == "__main__":
    print("Executing example")
    example()
    print("Done with example")
