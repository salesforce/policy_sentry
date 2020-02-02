"""
Functions to use for parsing ARNs, matching ARN types, and getting the right fragment/component from an ARN string,
"""


def parse_arn(arn):
    """
    Given an ARN, split up the ARN into the ARN namespacing schema dictated by the AWS docs.
    """
    elements = arn.split(':', 5)
    result = {
        'arn': elements[0],
        'partition': elements[1],
        'service': elements[2],
        'region': elements[3],
        'account': elements[4],
        'resource': elements[5],
        'resource_path': None,
    }
    if '/' in result['resource']:
        result['resource'], result['resource_path'] = result['resource'].split(
            '/', 1)
    elif ':' in result['resource']:
        result['resource'], result['resource_path'] = result['resource'].split(
            ':', 1)
    return result

# def get_string_arn(arn):
#     result = "{0}".format(str(arn))
#     after = result.strip('((,\'')
#     return after


def get_partition_from_arn(arn):
    """Given an ARN string, return the partition string. This is usually `aws` unless you are in C2S or
    AWS GovCloud."""
    result = parse_arn(arn)
    return result['partition']


def get_service_from_arn(arn):
    """Given an ARN string, return the service """
    result = parse_arn(arn)
    return result['service']


def get_region_from_arn(arn):
    """Given an ARN, return the region in the ARN, if it is available. In certain cases like S3 it is not"""
    result = parse_arn(arn)
    # Support S3 buckets with no values under region
    if result['region'] is None:
        result = ''
    else:
        result = result['region']
    return result


def get_account_from_arn(arn):
    """Given an ARN, return the account ID in the ARN, if it is available. In certain cases like S3 it is not"""
    result = parse_arn(arn)
    # Support S3 buckets with no values under account
    if result['account'] is None:
        result = ''
    else:
        result = result['account']
    return result


def get_resource_from_arn(arn):
    """Given an ARN, parse it according to ARN namespacing and return the resource. See
    http://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html for more details on ARN namespacing."""
    result = parse_arn(arn)
    return result['resource']


def get_resource_path_from_arn(arn):
    """Given an ARN, parse it according to ARN namespacing and return the resource path. See
    http://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html for more details on ARN namespacing."""
    result = parse_arn(arn)
    return result['resource_path']


# pylint: disable=simplifiable-if-statement
def arn_has_slash(arn):
    """Given an ARN, determine if the ARN has a stash in it. Just useful for the hacky methods for
    parsing ARN namespaces. See
    http://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html for more details on ARN namespacing."""
    if arn.count('/') > 0:
        return True
    else:
        return False


# pylint: disable=simplifiable-if-statement
def arn_has_colons(arn):
    """Given an ARN, determine if the ARN has colons in it. Just useful for the hacky methods for
    parsing ARN namespaces. See
    http://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html for more details on ARN namespacing."""
    if arn.count(':') > 0:
        return True
    else:
        return False


def does_arn_match(arn_to_test, arn_in_database):
    """Given two ARNs, determine if they match. The cases supported are outlined below.

    Case 1: arn:partition:service:region:account-id:resource
    Case 2: arn:partition:service:region:account-id:resourcetype/resource
    Case 3: arn:partition:service:region:account-id:resourcetype/resource/qualifier
    Case 4: arn:partition:service:region:account-id:resourcetype/resource:qualifier
    Case 5: arn:partition:service:region:account-id:resourcetype:resource
    Case 6: arn:partition:service:region:account-id:resourcetype:resource:qualifier
    Source: https://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html#genref-arns

    :param arn: ARN to parse
    :return: result of whether or not the ARNs match
    """
    score = 0
    # arn_in_database = 'arn:aws:ssm:${Region}:${Account}:parameter/${FullyQualifiedParameterName}'
    # arn_to_test = 'arn:aws:ssm:us-east-1:123456789012:parameter/test'
    exclusion_list = [
        "${ObjectName}"
    ]
    if arn_in_database == '*':
        score += 10  # Exit in this scenario
    else:
        if get_service_from_arn(arn_in_database) != get_service_from_arn(arn_to_test):
            score += 1
        if arn_has_colons(arn_in_database) != arn_has_colons(arn_to_test):
            score += 1
        if arn_has_slash(arn_in_database) != arn_has_slash(arn_to_test):
            score += 1
        if arn_has_slash(arn_in_database) and arn_has_slash(arn_to_test):
            # Example: SSM `parameter/`
            if get_resource_from_arn(arn_in_database) != get_resource_from_arn(arn_to_test):

                # Some exclusions, like ObjectId for S3 buckets
                if get_resource_path_from_arn(arn_in_database) in exclusion_list:
                    pass
                else:
                    score += 1

    # logger.debug("Score is " + str(score))
    # It passes if the alarm does not ring
    return score < 1
