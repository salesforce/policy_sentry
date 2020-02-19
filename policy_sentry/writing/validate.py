"""
Validation for the Policy Sentry YML Templates.
"""
import logging
from schema import Optional, Schema, And, Use, SchemaError

logger = logging.getLogger("__main__." + __name__)


def check(conf_schema, conf):
    """
    Validates a user-supplied JSON vs a defined schema.
    :param conf_schema: The Schema object that defines the required structure.
    :param conf: The user-supplied schema to validate against the required structure.
    """
    try:
        conf_schema.validate(conf)
        return True
    except SchemaError as schema_error:
        try:
            # workarounds for Schema's logging approach
            print(schema_error.autos[0])
            detailed_error_message = schema_error.autos[2]
            print(detailed_error_message.split(" in {'")[0])
            # for error in schema_error.autos:
        except:  # pylint: disable=bare-except
            logger.critical(schema_error)
        return False


CRUD_SCHEMA = Schema(
    {
        "mode": "crud",
        Optional("name"): And(Use(str)),
        Optional("read"): [str],
        Optional("write"): [str],
        Optional("list"): [str],
        Optional("permissions-management"): [str],
        Optional("tagging"): [str],
        Optional("wildcard-only"): {
            Optional("single-actions"): [str],
            Optional("service-read"): [str],
            Optional("service-write"): [str],
            Optional("service-list"): [str],
            Optional("service-tagging"): [str],
            Optional("service-permissions-management"): [str],
        },
    }
)

ACTIONS_SCHEMA = Schema(
    {"mode": "actions", Optional("name"): And(Use(str)), "actions": And([str]),}
)


def check_actions_schema(cfg):
    """
    Determines whether the user-provided config matches the required schema for Actions mode
    """
    result = check(ACTIONS_SCHEMA, cfg)
    if result is True:
        return result
    else:
        raise Exception(
            f"The provided template does not match the required schema for ACTIONS mode. "
            f"Please use the create-template command to generate a valid YML template that "
            f"Policy Sentry will accept."
        )


def check_crud_schema(cfg):
    """
    Determines whether the user-provided config matches the required schema for CRUD mode
    """
    result = check(CRUD_SCHEMA, cfg)
    if result is True:
        return result
    else:
        raise Exception(
            f"The provided template does not match the required schema for CRUD mode. "
            f"Please use the create-template command to generate a valid YML template that "
            f"Policy Sentry will accept."
        )


def validate_condition_block(condition_block):
    """
    :param condition_block: {"condition_key_string": "ec2:ResourceTag/purpose", "condition_type_string": "StringEquals", "condition_value": "test"}
    :return:
    """

    # TODO: Validate that the values are legit somehow
    CONDITION_BLOCK_SCHEMA = Schema(
        {
            "condition_key_string": And(Use(str)),
            "condition_type_string": And(Use(str)),
            "condition_value": And(Use(str)),
        }
    )
    try:
        CONDITION_BLOCK_SCHEMA.validate(condition_block)
        # TODO: Try to validate whether or not the condition keys are legit
        return True
    except SchemaError as s_e:
        logger.warning(s_e)
        return False
