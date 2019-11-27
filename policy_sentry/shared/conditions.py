# Just some text transformation functions related to our
# conditions-related workarounds


def get_service_from_condition_key(condition_key):
    elements = condition_key.split(':', 2)
    return elements[0]


def get_comma_separated_condition_keys(condition_keys):
    """
    :param condition_keys: String containing multiple condition keys, separated by double spaces
    :return: result: String containing multiple condition keys, comma-separated
    """

    result = condition_keys.replace(
        '  ', ',')  # replace the double spaces with a comma
    return result
