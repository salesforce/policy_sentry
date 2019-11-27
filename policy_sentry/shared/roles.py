import sys


class Roles:
    """
    This is just a data holder for list of lists - used for running the YAML option.
    The sublists should all contain these:
    Indexes:
    0 - Name
    1 - Description
    2 - ARN (string ARN of the role)
    3 - Actions (list of AWS API Actions)
    """
    roles = None

    def __init__(self):
        self.roles = []

    def add_role(self, role):
        self.roles.append(role)

    def get_roles(self):
        return self.roles

    def process_actions_config(self, cfg):

        try:
            for category in cfg:
                if category == 'roles_with_actions':
                    for principal in cfg[category]:
                        self.add_role([
                            principal['name'],
                            principal['description'],
                            principal['arn'],
                            principal['actions'],
                        ]
                        )
        except KeyError as ke:
            print("Yaml file is missing this block: " + ke.args[0])
            sys.exit()
        # except TypeError:
        #     print("Yaml file is not formatted properly. Please see the documentation for the proper format.")
        #     # print("Error: " + te.args[0])
        #     sys.exit()
