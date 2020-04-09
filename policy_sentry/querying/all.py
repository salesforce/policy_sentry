from policy_sentry.shared.iam_data import iam_definition


def get_all_service_prefixes():
    results = [d["prefix"] for d in iam_definition]
    results = list(set(results))
    results.sort()
    return results


def get_all_actions(lowercase=False):
    results = []
    all_actions = set()

    for service_info in iam_definition:
        for privilege_info in service_info["privileges"]:
            if lowercase:
                all_actions.add(f"{service_info['prefix']}:{privilege_info['privilege'].lower()}")
            else:
                all_actions.add(f"{service_info['prefix']}:{privilege_info['privilege']}")

    # results = list(set(results))
    # results.sort()
    return all_actions
