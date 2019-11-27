from policy_sentry.shared.login import login
from policy_sentry.shared.policy import PolicyGroup
from policy_sentry.shared.file import write_json_file, list_files_in_directory, create_directory_if_it_doesnt_exist
from policy_sentry.shared.constants import HOME, CONFIG_DIRECTORY
import sys


def download_remote_policies(
        profile=None,
        customer_managed=True,
        attached_only=True):
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
    print("If you want to analyze the policies, specify the policy file in the analyze command\n")
    # print("The list of policies downloaded are:")
    # print("")
    only_files = list_files_in_directory(filename_directory)
    # for filename in only_files:
    #     print(filename)
    return filename_directory


def download_policies_recursively(credentials_file, profiles):
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
