from policy_sentry.shared.login import login
from policy_sentry.shared.policy import PolicyGroup
from policy_sentry.shared.file import write_json_file, list_files_in_directory
from pathlib import Path
from os import listdir
from os.path import isfile, join
import os
from pprint import pprint

home = str(Path.home())
config_directory = '/.policy_sentry/'
# database_file_name = 'aws.sqlite3'
# database_path = home + config_directory + database_file_name


def download_remote_policies(profile=None):
    if profile:
        profile = profile
    else:
        profile = "default"
    iam_session = login(profile, "iam")
    sts_session = login(profile, "sts")
    account_id = sts_session.get_caller_identity()["Account"]
    policy_file_directory = home + config_directory + 'policy-analysis' + '/' + account_id
    if os.path.exists(policy_file_directory):
        pass
    else:
        os.mkdir(policy_file_directory)
    # Create the PolicyGroup Object
    policy_group = PolicyGroup()

    # Grab the list of policies and the associated metadata via boto3 list_policies
    policy_group.set_remote_policy_metadata(iam_session)
    # Get the list of policy names and put it in a list
    policy_names = policy_group.get_policy_names()

    # Grab all the custom policy documents and set it
    policy_group.set_remote_policy_documents(iam_session)

    print("Writing the policy files to " + policy_file_directory)
    print("")
    for policy_name in policy_names:
        # get the default policy version for that specific policy
        document = policy_group.get_policy_document(policy_name)
        filename = policy_file_directory + '/' + policy_name + '.json'
        print("Writing policy for " + policy_name)
        # Write it to $HOME/.policy_sentry
        write_json_file(filename, document)
    print("")
    print("Downloaded policies to " + policy_file_directory + "/")
    print("")
    print("If you want to analyze the policies, specify the policy file in the analyze-iam-policy command\n")
    print("The list of policies downloaded are:")
    print("")
    # https://stackoverflow.com/questions/3207219/how-do-i-list-all-files-of-a-directory#answer-3207973
    only_files = list_files_in_directory(policy_file_directory)
    for filename in only_files:
        print(filename)

