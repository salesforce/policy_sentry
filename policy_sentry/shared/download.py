"""
Functions to support downloading policies from live AWS accounts in bulk for analysis
"""
import sys
import json
from policy_sentry.shared.login import login
from policy_sentry.shared.file import write_json_file, create_directory_if_it_doesnt_exist
from policy_sentry.shared.constants import HOME, CONFIG_DIRECTORY


def download_remote_policies(profile=None, customer_managed=True, attached_only=True):
    """Download IAM Policies from live accounts to ~/policy_sentry/analysis/account_id/"""
    # Credentials profile selection
    if profile:
        profile = profile
    else:
        profile = "default"
    iam_session = login(profile, "iam")
    sts_session = login(profile, "sts")
    # Get the account ID for use in folder directory naming
    account_id = sts_session.get_caller_identity()["Account"]

    # Directory names
    policy_file_directory = HOME + CONFIG_DIRECTORY + \
        'analysis' + '/' + account_id
    customer_managed_policy_file_directory = policy_file_directory + '/' + 'customer-managed'
    aws_managed_policy_file_directory = policy_file_directory + '/' + 'aws-managed'

    create_directory_if_it_doesnt_exist(policy_file_directory)
    create_directory_if_it_doesnt_exist(customer_managed_policy_file_directory)
    create_directory_if_it_doesnt_exist(aws_managed_policy_file_directory)

    policy_group = PolicyGroup()
    policy_group.set_remote_policy_metadata(
        iam_session, customer_managed, attached_only)
    policy_names = policy_group.get_policy_names()
    policy_group.set_remote_policy_documents(iam_session)

    # Determine whether we should store it in the customer-managed or
    # aws-managed directory
    if customer_managed:
        filename_directory = customer_managed_policy_file_directory
    else:
        filename_directory = aws_managed_policy_file_directory

    print("Writing the policy files to " + filename_directory)
    print("")
    for policy_name in policy_names:
        # get the default policy version for that specific policy
        document = policy_group.get_policy_document(policy_name)
        filename = filename_directory + '/' + policy_name + '.json'
        write_json_file(filename, document)
    print("If you want to analyze the policies, just run:\n\npolicy_sentry analyze downloaded-policies")
    return filename_directory


def download_policies_recursively(profiles):
    """Given a list of profiles from the AWS Credentials file, download policies from all of those accounts."""
    download_directories = []

    for profile in profiles:
        try:
            print(f"Downloading policies under profile {profile}")
            download_dir = download_remote_policies(profile, True, True)
            download_directories.append(download_dir)
        except TypeError as t_e:
            print(t_e)
            sys.exit()
    return download_directories


class PolicyGroup:
    """
    This is used for downloading IAM policies remotely. It requires chaining two boto3 calls back to back.
    """

    def __init__(self):
        self.policies = {}
        # each dict has:
        # policy_name, policy_id, policy_arn, default_version_id, and
        # policy_document

    def add(self, policy_name, policy_id, policy_arn, default_version_id):
        """Add a new policy, along with policy metadata"""
        temp_dict = {
            'policy_id': policy_id,
            'policy_arn': policy_arn,
            'default_version_id': default_version_id
        }
        self.policies[policy_name] = temp_dict

    def get_policy_names(self):
        """Get a list of the policy names currently stored."""
        temp_list_of_policy_names = []
        for policy in self.policies:
            temp_list_of_policy_names.append(policy)
        return temp_list_of_policy_names

    def get_policy_document(self, policy_name, formatted_as_string=None):
        """Given a policy name, return the policy's document, either as a string or a dict"""
        if formatted_as_string:
            policy = self.policies[policy_name]['policy_document']
            return json.dumps(policy, indent=4, default=str)
        else:
            return self.policies[policy_name]['policy_document']

    def set_remote_policy_metadata(
            self,
            iam_session,
            customer_managed=True,
            attached_only=True):
        """
        Downloads IAM policies and adds them to the object
        :param attached_only: Attached policies only
        :param iam_session: IAM boto session
        :param customer_managed: True for 'Local' (customer managed policies), False for 'AWS' (managed policies)
        :param only_attached: True/False
        """
        if customer_managed:
            scope = 'Local'
        else:
            scope = 'AWS'
        # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.list_policies
        response = iam_session.list_policies(
            Scope=scope,
            OnlyAttached=attached_only,
            PathPrefix='/',  # slash (/) lists all policies
            # PolicyUsageFilter='PermissionsPolicy',
            MaxItems=123
        )
        for policy in response['Policies']:
            policy_name = policy['PolicyName']
            policy_id = policy['PolicyId']
            policy_arn = policy['Arn']
            default_version_id = policy['DefaultVersionId']
            self.add(policy_name, policy_id, policy_arn, default_version_id)

    def set_policy_document(self, policy_name, document):
        """Store a single policy document"""
        # document is a dict containing version and statement. Statement contains typical IAM policy statements.
        # TODO: Handle an error where the policy name does not exist
        self.policies[policy_name]['policy_document'] = document

    def set_remote_policy_documents(self, iam_session):
        """
        Given a boto3 session, look at the list of policies stored in this object and query AWS
        for the policy documents associated with each policy name
        """
        for policy in self.policies:
            response = iam_session.get_policy_version(
                PolicyArn=self.policies[policy]['policy_arn'],
                VersionId=self.policies[policy]['default_version_id']
            )
            self.set_policy_document(
                policy, response['PolicyVersion']['Document'])
