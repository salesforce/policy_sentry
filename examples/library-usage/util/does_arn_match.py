#!/usr/bin/env python
from policy_sentry.util.arns import does_arn_match

if __name__ == '__main__':
    print(does_arn_match("arn:aws:s3:::bucket_name", "arn:${Partition}:s3:::${BucketName}"))
    print(does_arn_match("arn:aws:codecommit:us-east-1:123456789012:MyDemoRepo", "arn:${Partition}:codecommit:${Region}:${Account}:${RepositoryName}"))
    print(does_arn_match("arn:aws:ssm:us-east-1:123456789012:parameter/test", "arn:${Partition}:ssm:${Region}:${Account}:parameter/${FullyQualifiedParameterName}"))
    print(does_arn_match("arn:aws:batch:region:account-id:job-definition/job-name:revision", "arn:${Partition}:batch:${Region}:${Account}:job-definition/${JobDefinitionName}:${Revision}"))
    print(does_arn_match("arn:aws:states:region:account-id:stateMachine:stateMachineName", "arn:${Partition}:states:${Region}:${Account}:stateMachine:${StateMachineName}"))
    print(does_arn_match("arn:aws:states:region:account-id:execution:stateMachineName:executionName", "arn:${Partition}:states:${Region}:${Account}:execution:${StateMachineName}:${ExecutionId}"))


"""
Output:

True
True
True
True
True
True
"""
