"""
Just some text transformation functions related to our
conditions-related workarounds
"""


# Borrowed from parliament. Altered with normalization for lowercase.
def translate_condition_key_data_types(condition_str):
    """
    The docs use different type names, so this standardizes them.
    Example: The condition secretsmanager:RecoveryWindowInDays is listed as using a "Long"
    So return "Number"
    """

    if condition_str.lower() in ["arn", "arn"]:
        return "Arn"
    elif condition_str.lower() in ["bool", "boolean"]:
        return "Bool"
    elif condition_str.lower() in ["date"]:
        return "Date"
    elif condition_str.lower() in ["long", "numeric"]:
        return "Number"
    elif condition_str.lower() in ["string", "string", "arrayofstring"]:
        return "String"
    elif condition_str.lower() in ["ip"]:
        return "Ip"
    else:
        raise Exception("Unknown data format: {}".format(str))


def get_service_from_condition_key(condition_key):
    """Given a condition key, return the service prefix"""
    elements = condition_key.split(":", 2)
    return elements[0]


def get_comma_separated_condition_keys(condition_keys):
    """
    :param condition_keys: String containing multiple condition keys, separated by double spaces
    :return: result: String containing multiple condition keys, comma-separated
    """

    result = condition_keys.replace("  ", ",")  # replace the double spaces with a comma
    return result
