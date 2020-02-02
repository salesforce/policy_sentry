# pylint: disable=W1202
"""
Functions for logging into AWS and returning Boto3 sessions.
"""
import configparser
import os
import logging
import boto3
from botocore.exceptions import ClientError, NoCredentialsError

logger = logging.getLogger(__name__)


def login_sts_test(sts_session):
    """Test the login procedure with boto3 STS session."""
    # Mute botocore, except when errors occur
    logging.getLogger('botocore').setLevel(logging.WARN)
    try:
        sts_session.get_caller_identity()
    except ClientError as c_e:
        if "InvalidClientTokenId" in str(c_e):
            logger.critical(
                "ERROR: sts.get_caller_identity failed with InvalidClientTokenId. "
                "Likely cause is no AWS credentials are set.",
                flush=True,
            )
            exit(-1)
        else:
            logger.critical(
                "ERROR: Unknown exception when trying to call sts.get_caller_identity: {}".format(
                    c_e
                ),
                flush=True,
            )
            exit(-1)


def login_iam_test(iam_session):
    """Test the login procedure with boto3 IAM session."""
    # Mute botocore, except when errors occur
    logging.getLogger('botocore').setLevel(logging.WARN)
    try:
        iam_session.get_user(UserName="test")
    except ClientError as c_e:
        if "InvalidClientTokenId" in str(c_e):
            logger.critical(
                "ERROR: AWS doesn't allow you to make IAM calls from a session without MFA, and the collect"
                " command gathers IAM data.  Please use MFA or don't use a session. With aws-vault,"
                " specify `--no-session` on your `exec`.",
                flush=True,
            )
            exit(-1)
        if "NoSuchEntity" in str(c_e):
            # Ignore, we're just testing that our creds work
            pass
        else:
            logger.critical("ERROR: Ensure your creds are valid.", flush=True)
            logger.critical(c_e, flush=True)
            exit(-1)
    except NoCredentialsError:
        logger.critical("ERROR: No AWS credentials configured.", flush=True)
        exit(-1)


def login(profile_name, service='iam'):
    """Log in to AWS and return a boto3 session."""
    default_region = os.environ.get("AWS_REGION", "us-east-1")
    session_data = {"region_name": default_region}
    if profile_name:
        session_data["profile_name"] = profile_name

    session = boto3.Session(**session_data)

    sts_session = session.client("sts")
    login_sts_test(sts_session)

    # Ensure we can make iam calls
    iam_session = session.client("iam")
    login_iam_test(iam_session)

    # Return the service requested by the function - either sts or iam
    if service:
        this_session = session.client(service)
    # By default return IAM
    else:
        this_session = session.client("iam")
    return this_session


def get_list_of_aws_profiles(credentials_file):
    """Get a list of profiles from the AWS Credentials file"""
    config = configparser.RawConfigParser()
    config.read(credentials_file)
    sections = config.sections()
    legitimate_sections = []
    for section in sections:
        # https://github.com/broamski/aws-mfa#credentials-file-setup
        broamski_suffix = "-long-term"
        # pylint: disable=no-else-continue
        if section.endswith(broamski_suffix):
            # skip it if it's not a real profile we want to evaluate
            continue
        else:
            legitimate_sections.append(section)
    return legitimate_sections
