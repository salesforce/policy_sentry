"""
Validation for the Policy Sentry YML Templates.
"""
from schema import Optional, Schema, And, Use, SchemaError


def check(conf_schema, conf):
    """
    Validates a user-supplied JSON vs a defined schema.
    :param conf_schema: The Schema object that defines the required structure.
    :param conf: The user-supplied schema to validate against the required structure.
    """
    try:
        conf_schema.validate(conf)
        return True
    except SchemaError as s_e:
        print(f"{s_e.autos[0]}:\n{s_e.autos[2]}")
        return False


crud_schema = Schema({
    'policy_with_crud_levels': [
        {
            'name': And(Use(str)),
            'description': And(Use(str)),
            'arn': And(Use(str)),
            Optional('read'): [str],
            Optional('write'): [str],
            Optional('list'): [str],
            Optional('permissions-management'): [str],
            Optional('tag'): [str],
            Optional('wildcard'): [str],

        }
    ]
})

actions_schema = Schema({
    'policy_with_actions': [
        {
            'name': And(Use(str)),
            'description': And(Use(str)),
            'arn': And(Use(str)),
            'actions': And([str]),
        }
    ]
})


def check_actions_schema(cfg):
    """
    Determines whether the user-provided config matches the required schema for Actions mode
    """
    result = check(actions_schema, cfg)
    if result is True:
        return result
    else:
        raise Exception(f"The provided template does not match the required schema for ACTIONS mode. "
                        f"Please use the create-template command to generate a valid YML template that "
                        f"Policy Sentry will accept.")


def check_crud_schema(cfg):
    """
    Determines whether the user-provided config matches the required schema for CRUD mode
    """
    result = check(crud_schema, cfg)
    if result is True:
        return result
    else:
        raise Exception(f"The provided template does not match the required schema for CRUD mode. "
                        f"Please use the create-template command to generate a valid YML template that "
                        f"Policy Sentry will accept.")
