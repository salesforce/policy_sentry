import unittest
from pathlib import Path
from policy_sentry.shared.arns import does_arn_match
from policy_sentry.shared.database import connect_db

home = str(Path.home())
config_directory = '/.policy_sentry/'
database_file_name = 'aws.sqlite3'
database_path = home + config_directory + database_file_name
db_session = connect_db(database_path)

# "Does Arn Match" tests
# See docs for this list: # https://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html#genref-arns
# Case 1: arn:partition:service:region:account-id:resource
# Case 2: arn:partition:service:region:account-id:resourcetype/resource
# Case 3: arn:partition:service:region:account-id:resourcetype/resource/qualifier
# Case 4: arn:partition:service:region:account-id:resourcetype/resource:qualifier
# Case 5: arn:partition:service:region:account-id:resourcetype:resource
# Case 6: arn:partition:service:region:account-id:resourcetype:resource:qualifier


class ArnsTestCase(unittest.TestCase):

    def test_does_arn_match_case_bucket(self):
        # Case 1: arn:partition:service:region:account-id:resource
        arn_to_test = "arn:aws:s3:::bucket_name"
        arn_in_database = "arn:aws:s3:::${BucketName}"
        self.assertTrue(does_arn_match(arn_to_test, arn_in_database))

    def test_does_arn_match_case_1(self):
        # Case 1: arn:partition:service:region:account-id:resource
        arn_to_test = "arn:aws:codecommit:us-east-1:123456789012:MyDemoRepo"
        arn_in_database = "arn:aws:codecommit:${Region}:${Account}:${RepositoryName}"
        self.assertTrue(does_arn_match(arn_to_test, arn_in_database))

    def test_does_arn_match_case_2(self):
        # Case 2: arn:partition:service:region:account-id:resourcetype/resource
        arn_to_test = "arn:aws:ssm:us-east-1:123456789012:parameter/test"
        arn_in_database = "arn:aws:ssm:${Region}:${Account}:parameter/${FullyQualifiedParameterName}"
        self.assertTrue(does_arn_match(arn_to_test, arn_in_database))

    # This one is failing
    # def test_does_arn_match_case_3(self):
    #     # Case 3: arn:partition:service:region:account-id:resourcetype/resource/qualifier
    #     arn_to_test = "arn:aws:kinesis:us-east-1:account-id:firehose/myfirehose/consumer/someconsumer:${ConsumerCreationTimpstamp}"
    #     arn_in_database = "arn:aws:kinesis:${Region}:${Account}:${StreamType}/${StreamName}/consumer/${ConsumerName}:${ConsumerCreationTimpstamp}"
    #     # https://docs.aws.amazon.com/kinesis/latest/APIReference/API_ConsumerDescription.html
    #     self.assertTrue(does_arn_match(arn_to_test, arn_in_database))

    def test_does_arn_match_case_4(self):
        # Case 4: arn:partition:service:region:account-id:resourcetype/resource:qualifier
        arn_to_test = "arn:aws:batch:region:account-id:job-definition/job-name:revision"
        arn_in_database = "arn:aws:batch:${Region}:${Account}:job-definition/${JobDefinitionName}:${Revision}"
        self.assertTrue(does_arn_match(arn_to_test, arn_in_database))

    def test_does_arn_match_case_5(self):
        # Case 5: arn:partition:service:region:account-id:resourcetype:resource
        arn_to_test = "arn:aws:states:region:account-id:stateMachine:stateMachineName"
        arn_in_database = "arn:aws:states:${Region}:${Account}:stateMachine:${StateMachineName}"
        self.assertTrue(does_arn_match(arn_to_test, arn_in_database))

    def test_does_arn_match_case_6(self):
        # Case 6: arn:partition:service:region:account-id:resourcetype:resource:qualifier
        arn_to_test = "arn:aws:states:region:account-id:execution:stateMachineName:executionName"
        arn_in_database = "arn:aws:states:${Region}:${Account}:execution:${StateMachineName}:${ExecutionId}"
        self.assertTrue(does_arn_match(arn_to_test, arn_in_database))

    # def test_does_arn_match_case_greengrass(self):
    #     # Undocumented case: AWS Greengrass: arn:aws:greengrass:${Region}:${Account}:/greengrass/definition/devices/${DeviceDefinitionId}/versions/${VersionId}
    #     arn_to_test = "arn:aws:greengrass:${Region}:${Account}:/greengrass/definition/devices/1234567}/versions/1"
    #     arn_in_database = "arn:aws:greengrass:${Region}:${Account}:/greengrass/definition/devices/${DeviceDefinitionId}/versions/${VersionId}"
    #     self.assertTrue(does_arn_match(arn_to_test, arn_in_database))
