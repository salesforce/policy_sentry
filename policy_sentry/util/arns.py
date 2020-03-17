"""
Functions to use for parsing ARNs, matching ARN types, and getting the right fragment/component from an ARN string,
"""
import logging
import re

logger = logging.getLogger(__name__)


def parse_arn(arn):
    """
    Given an ARN, split up the ARN into the ARN namespacing schema dictated by the AWS docs.
    """
    elements = arn.split(":", 5)
    result = {
        "arn": elements[0],
        "partition": elements[1],
        "service": elements[2],
        "region": elements[3],
        "account": elements[4],
        "resource": elements[5],
        "resource_path": None,
    }
    if "/" in result["resource"]:
        result["resource"], result["resource_path"] = result["resource"].split("/", 1)
    elif ":" in result["resource"]:
        result["resource"], result["resource_path"] = result["resource"].split(":", 1)
    return result


# def get_string_arn(arn):
#     result = "{0}".format(str(arn))
#     after = result.strip('((,\'')
#     return after


def get_partition_from_arn(arn):
    """Given an ARN string, return the partition string. This is usually `aws` unless you are in C2S or
    AWS GovCloud."""
    result = parse_arn(arn)
    return result["partition"]


def get_service_from_arn(arn):
    """Given an ARN string, return the service """
    result = parse_arn(arn)
    return result["service"]


def get_region_from_arn(arn):
    """Given an ARN, return the region in the ARN, if it is available. In certain cases like S3 it is not"""
    result = parse_arn(arn)
    # Support S3 buckets with no values under region
    if result["region"] is None:
        result = ""
    else:
        result = result["region"]
    return result


def get_account_from_arn(arn):
    """Given an ARN, return the account ID in the ARN, if it is available. In certain cases like S3 it is not"""
    result = parse_arn(arn)
    # Support S3 buckets with no values under account
    if result["account"] is None:
        result = ""
    else:
        result = result["account"]
    return result


def get_resource_from_arn(arn):
    """Given an ARN, parse it according to ARN namespacing and return the resource. See
    http://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html for more details on ARN namespacing."""
    result = parse_arn(arn)
    return result["resource"]


def get_resource_path_from_arn(arn):
    """Given an ARN, parse it according to ARN namespacing and return the resource path. See
    http://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html for more details on ARN namespacing."""
    result = parse_arn(arn)
    return result["resource_path"]


# pylint: disable=simplifiable-if-statement
def arn_has_slash(arn):
    """Given an ARN, determine if the ARN has a stash in it. Just useful for the hacky methods for
    parsing ARN namespaces. See
    http://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html for more details on ARN namespacing."""
    if arn.count("/") > 0:
        return True
    else:
        return False


# pylint: disable=simplifiable-if-statement
def arn_has_colons(arn):
    """Given an ARN, determine if the ARN has colons in it. Just useful for the hacky methods for
    parsing ARN namespaces. See
    http://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html for more details on ARN namespacing."""
    if arn.count(":") > 0:
        return True
    else:
        return False


def get_resource_string(arn):
    """
    Given an ARN, return the string after the account ID, no matter the ARN format.

    :param arn: arn:partition:service:region:account-id:resourcetype/resource
    :return: resourcetype/resource
    """
    split_arn = arn.split(":")
    resource_string = ":".join(split_arn[5:])
    return resource_string


# TODO: query all arns in the service then find the ARN that matches the pattern here. This will match for buckets, for example.
# In the meantime, we have to skip this pylint check (consider this as tech debt)
# pylint: disable=inconsistent-return-statements
def parse_arn_for_resource_type(arn):
    """
    Parses the resource string (resourcetype/resource and other variants) and grab the resource type.

    :param arn:
    :return:
    """
    split_arn = arn.split(":")
    # Resource string will equal:
    #     Case 1: resource
    #     Case 2: resourcetype/resource
    #     Case 3: resourcetype/resource/qualifier
    #     Case 4: resourcetype/resource:qualifier
    #     Case 5: resourcetype:resource
    #     Case 6: resourcetype:resource:qualifier
    resource_string = ":".join(split_arn[5:])
    split_resource = re.split("/|:", resource_string)
    if len(split_resource) == 1:
        # logger.debug(f"split_resource length is 1: {str(split_resource)}")
        pass
    elif len(split_resource) > 1:
        return split_resource[0]


#     Case 1: arn:partition:service:region:account-id:resource
#     Case 2: arn:partition:service:region:account-id:resourcetype/resource
#     Case 3: arn:partition:service:region:account-id:resourcetype/resource/qualifier
#     Case 4: arn:partition:service:region:account-id:resourcetype/resource:qualifier
#     Case 5: arn:partition:service:region:account-id:resourcetype:resource
#     Case 6: arn:partition:service:region:account-id:resourcetype:resource:qualifier
#     Source: https://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html#genref-arns
def does_arn_match(arn_to_test, arn_in_database):
    """
    Given two ARNs, determine if they have the same resource type.
    :param arn_to_test: ARN provided by user
    :param arn_in_database: Raw ARN that exists in the policy sentry database
    :return: result of whether or not the ARNs match
    """
    score = 0
    # arn_in_database = 'arn:aws:ssm:${Region}:${Account}:parameter/${FullyQualifiedParameterName}'
    # arn_to_test = 'arn:aws:ssm:us-east-1:123456789012:parameter/test'
    exclusion_list = ["${ObjectName}"]
    if arn_in_database == "*":
        return False
    else:
        resource_string_arn_in_database = get_resource_string(arn_in_database)
        resource_string_arn_to_test = get_resource_string(arn_to_test)
        resource_type_arn_in_database = parse_arn_for_resource_type(arn_in_database)
        resource_type_arn_to_test = parse_arn_for_resource_type(arn_to_test)
        if get_service_from_arn(arn_in_database) != get_service_from_arn(arn_to_test):
            score += 10
            return False
        if resource_type_arn_in_database == resource_type_arn_to_test:
            return True
        else:
            score += 1
        if (
            resource_string_arn_in_database.count("/") > 0
            and resource_string_arn_to_test.count("/") > 0
        ):
            # Example: SSM `parameter/`
            if get_resource_from_arn(arn_in_database) != get_resource_from_arn(
                arn_to_test
            ):
                # Some exclusions, like ObjectId for S3 buckets
                if get_resource_path_from_arn(arn_in_database) in exclusion_list:
                    return True
                else:
                    return False
    return score < 1
