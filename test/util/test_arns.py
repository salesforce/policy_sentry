import unittest
from policy_sentry.util.arns import does_arn_match, ARN
import os
import yaml

# "Does Arn Match" tests
# See docs for this list: # https://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html#genref-arns
# They removed some of the cases. The old version that gave this comprehensive list of resource ARN formats is here:
# https://web.archive.org/web/20190903192015/https://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html
# Case 1: arn:partition:service:region:account-id:resource
# Case 2: arn:partition:service:region:account-id:resourcetype/resource
# Case 3: arn:partition:service:region:account-id:resourcetype/resource/qualifier
# Case 4: arn:partition:service:region:account-id:resourcetype/resource:qualifier
# Case 5: arn:partition:service:region:account-id:resourcetype:resource
# Case 6: arn:partition:service:region:account-id:resourcetype:resource:qualifier
# Case 7: arn:partition:service:region:account-id:/greengrass/definition/devices/${DeviceDefinitionId}/versions/${VersionId}

class ArnsTestCase(unittest.TestCase):
    def test_does_arn_match_case_bucket(self):
        # Case 1: arn:partition:service:region:account-id:resource
        arn_to_test = "arn:aws:s3:::bucket_name"
        arn_in_database = "arn:${Partition}:s3:::${BucketName}"
        this_arn = ARN(arn_to_test)
        self.assertTrue(this_arn.same_resource_type(arn_in_database))

    def test_does_arn_match_case_1(self):
        # Case 1: arn:partition:service:region:account-id:resource
        arn_to_test = "arn:aws:codecommit:us-east-1:123456789012:MyDemoRepo"
        arn_in_database = (
            "arn:${Partition}:codecommit:${Region}:${Account}:${RepositoryName}"
        )
        this_arn = ARN(arn_to_test)
        self.assertTrue(this_arn.same_resource_type(arn_in_database))

    def test_does_arn_match_case_2(self):
        # Case 2: arn:partition:service:region:account-id:resourcetype/resource
        arn_to_test = "arn:aws:ssm:us-east-1:123456789012:parameter/test"
        arn_in_database = "arn:${Partition}:ssm:${Region}:${Account}:parameter/${FullyQualifiedParameterName}"
        this_arn = ARN(arn_to_test)
        self.assertTrue(this_arn.same_resource_type(arn_in_database))

    def test_does_arn_match_case_3(self):
        # Case 3: arn:partition:service:region:account-id:resourcetype/resource/qualifier
        arn_to_test = "arn:aws:kinesis:us-east-1:account-id:firehose/myfirehose/consumer/someconsumer:${ConsumerCreationTimpstamp}"
        arn_in_database = "arn:aws:kinesis:${Region}:${Account}:${StreamType}/${StreamName}/consumer/${ConsumerName}:${ConsumerCreationTimpstamp}"
        # https://docs.aws.amazon.com/kinesis/latest/APIReference/API_ConsumerDescription.html
        this_arn = ARN(arn_to_test)
        self.assertTrue(this_arn.same_resource_type(arn_in_database))

    def test_does_arn_match_case_4(self):
        # Case 4: arn:partition:service:region:account-id:resourcetype/resource:qualifier
        arn_to_test = "arn:aws:batch:region:account-id:job-definition/job-name:revision"
        arn_in_database = "arn:${Partition}:batch:${Region}:${Account}:job-definition/${JobDefinitionName}:${Revision}"
        this_arn = ARN(arn_to_test)
        self.assertTrue(this_arn.same_resource_type(arn_in_database))

    def test_does_arn_match_case_5(self):
        # Case 5: arn:partition:service:region:account-id:resourcetype:resource
        arn_to_test = "arn:aws:states:region:account-id:stateMachine:stateMachineName"
        arn_in_database = "arn:${Partition}:states:${Region}:${Account}:stateMachine:${StateMachineName}"
        this_arn = ARN(arn_to_test)
        self.assertTrue(this_arn.same_resource_type(arn_in_database))

    def test_does_arn_match_case_6(self):
        # Case 6: arn:partition:service:region:account-id:resourcetype:resource:qualifier
        arn_to_test = (
            "arn:aws:states:region:account-id:execution:stateMachineName:executionName"
        )
        arn_in_database = "arn:${Partition}:states:${Region}:${Account}:execution:${StateMachineName}:${ExecutionId}"
        this_arn = ARN(arn_to_test)
        self.assertTrue(this_arn.same_resource_type(arn_in_database))

    def test_does_arn_match_case_greengrass(self):
        # Undocumented case: AWS Greengrass: arn:aws:greengrass:${Region}:${Account}:/greengrass/definition/devices/${DeviceDefinitionId}/versions/${VersionId}
        arn_to_test = "arn:aws:greengrass:${Region}:${Account}:/greengrass/definition/devices/1234567/versions/1"
        arn_in_database = "arn:aws:greengrass:${Region}:${Account}:/greengrass/definition/devices/${DeviceDefinitionId}/versions/${VersionId}"
        this_arn = ARN(arn_to_test)
        self.assertTrue(this_arn.same_resource_type(arn_in_database))

    def test_does_arn_match_rds(self):
        arns_to_test = [
            "arn:${Partition}:rds:${Region}:${Account}:cluster:${DbClusterInstanceName}",
            "arn:${Partition}:rds:${Region}:${Account}:cluster-endpoint:${DbClusterEndpoint}",
            "arn:${Partition}:rds:${Region}:${Account}:cluster-pg:${ClusterParameterGroupName}",
            "arn:${Partition}:rds:${Region}:${Account}:cluster-snapshot:${ClusterSnapshotName}",
            "arn:${Partition}:rds:${Region}:${Account}:es:${SubscriptionName}",
            "arn:${Partition}:rds:${Account}:global-cluster:${GlobalCluster}",
            "arn:${Partition}:rds:${Region}:${Account}:og:${OptionGroupName}",
            "arn:${Partition}:rds:${Region}:${Account}:pg:${ParameterGroupName}",
            "arn:${Partition}:rds:${Region}:${Account}:db-proxy:${DbProxyId}",
            "arn:${Partition}:rds:${Region}:${Account}:ri:${ReservedDbInstanceName}",
            "arn:${Partition}:rds:${Region}:${Account}:secgrp:${SecurityGroupName}",
            "arn:${Partition}:rds:${Region}:${Account}:snapshot:${SnapshotName}",
            "arn:${Partition}:rds:${Region}:${Account}:subgrp:${SubnetGroupName}",
            "arn:${Partition}:rds:${Region}:${Account}:target:${TargetId}",
            "arn:${Partition}:rds:${Region}:${Account}:target-group:${TargetGroupId}"
        ]
        arn_in_database = "arn:${Partition}:rds:${Region}:${Account}:db:${DbInstanceName}"
        for arn in arns_to_test:
            this_arn = ARN(arn)
            self.assertFalse(this_arn.same_resource_type(arn_in_database))

        arn_to_test = "arn:${Partition}:rds:${Region}:${Account}:cluster:${DbClusterInstanceName}"
        this_arn = ARN(arn_to_test)
        self.assertFalse(this_arn.same_resource_type(arn_in_database))

        arn_to_test = "arn:${Partition}:rds:${Region}:${Account}:db:${DbInstanceName}"
        arn_in_database = "arn:${Partition}:rds:${Region}:${Account}:db:${DbInstanceName}"
        this_arn = ARN(arn_to_test)
        self.assertTrue(this_arn.same_resource_type(arn_in_database))

    def test_does_arn_match_resource_wildcard(self):
        arn_to_test = "arn:${Partition}:rds:${Region}:${Account}:*:*"
        arn_in_database = "arn:${Partition}:rds:${Region}:${Account}:db:${DbInstanceName}"
        this_arn = ARN(arn_to_test)
        self.assertTrue(this_arn.same_resource_type(arn_in_database))

        # Make sure wrong service yields False
        arn_to_test = "arn:${Partition}:s3:${Region}:${Account}:*:*"
        arn_in_database = "arn:${Partition}:rds:${Region}:${Account}:db:${DbInstanceName}"
        this_arn = ARN(arn_to_test)
        self.assertFalse(this_arn.same_resource_type(arn_in_database))

    def test_dynamodb_arn_matching_gh_215(self):
        """test_dynamodb_arn_matching_gh_215: Validate fix for DynamoDB arn mismatch in GitHub issue #215"""
        index = "arn:${Partition}:dynamodb:${Region}:${Account}:table/${TableName}/index/${IndexName}"
        stream = "arn:${Partition}:dynamodb:${Region}:${Account}:table/${TableName}/stream/${StreamLabel}"
        table = "arn:${Partition}:dynamodb:${Region}:${Account}:table/${TableName}"
        backup = "arn:${Partition}:dynamodb:${Region}:${Account}:table/${TableName}/backup/${BackupName}"
        global_table = "arn:${Partition}:dynamodb::${Account}:global-table/${GlobalTableName}"

        this_arn = ARN("arn:aws:dynamodb:us-east-1:123456789123:table/mytable")
        self.assertTrue(this_arn.same_resource_type(table))
        result = this_arn.same_resource_type(index)
        self.assertFalse(result)
        result = this_arn.same_resource_type(stream)
        self.assertFalse(result)
        result = this_arn.same_resource_type(backup)
        self.assertFalse(result)
        result = this_arn.same_resource_type(global_table)
        self.assertFalse(result)

        this_arn = "arn:aws:dynamodb:us-east-1:123456789123:table/mytable"
        self.assertTrue(does_arn_match(this_arn, table))
        self.assertFalse(does_arn_match(this_arn, index))
        self.assertFalse(does_arn_match(this_arn, stream))
        self.assertFalse(does_arn_match(this_arn, backup))
        self.assertFalse(does_arn_match(this_arn, global_table))
