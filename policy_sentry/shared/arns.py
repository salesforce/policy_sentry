def parse_arn(arn):
    # http://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html
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


def get_string_arn(arn):
    result = "{0}".format(str(arn))
    after = result.strip('((,\'')
    return after


def get_partition_from_arn(arn):
    result = parse_arn(arn)
    return result['partition']


def get_service_from_arn(arn):
    result = parse_arn(arn)
    return result['service']


def get_region_from_arn(arn):
    result = parse_arn(arn)
    # Support S3 buckets with no values under region
    if result['region'] is None:
        result = ''
    else:
        result = result['region']
    return result


def get_account_from_arn(arn):
    result = parse_arn(arn)
    # Support S3 buckets with no values under account
    if result['account'] is None:
        result = ''
    else:
        result = result['account']
    return result


def get_resource_from_arn(arn):
    result = parse_arn(arn)
    return result['resource']


def get_resource_path_from_arn(arn):
    result = parse_arn(arn)
    return result['resource_path']


def arn_has_slash(arn):
    if arn.count('/') > 0:
        return True
    else:
        return False


def arn_has_colons(arn):
    if arn.count(':') > 0:
        return True
    else:
        return False


def does_arn_match(arn_to_test, arn_in_database):
    score = 0
    # arn_in_database = 'arn:aws:ssm:${Region}:${Account}:parameter/${FullyQualifiedParameterName}'
    # arn_to_test = 'arn:aws:ssm:us-east-1:123456789012:parameter/test'
    exclusion_list = [
        "${ObjectName}"
    ]
    if arn_in_database == '*':
        score += 10  # Exit in this scenario
    else:
        if get_service_from_arn(
                arn_in_database) != get_service_from_arn(arn_to_test):
            score += 1
        if arn_has_colons(arn_in_database) != arn_has_colons(arn_to_test):
            score += 1
        if arn_has_slash(arn_in_database) != arn_has_slash(arn_to_test):
            score += 1
        if arn_has_slash(arn_in_database) and arn_has_slash(arn_to_test):
            # Example: SSM `parameter/`
            arn_in_db_resource = get_resource_from_arn(
                arn_in_database)  # robot
            arn_to_test_resource = get_resource_from_arn(
                arn_to_test)  # robot-application
            if get_resource_from_arn(
                    arn_in_database) != get_resource_from_arn(arn_to_test):

                # Some exclusions, like ObjectId for S3 buckets
                if get_resource_path_from_arn(
                        arn_in_database) in exclusion_list:
                    pass
                else:
                    score += 1

    # print("Score is " + str(score))
    # It passes if the alarm does not ring
    return score < 1
