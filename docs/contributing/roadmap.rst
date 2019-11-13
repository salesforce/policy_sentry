Roadmap
===========

* Condition Keys

Currently, Condition Keys are not supported by this script. For an example, see the KMS key Condition Key Table `here <https://docs.aws.amazon.com/IAM/latest/UserGuide/list_awskeymanagementservice.html#awskeymanagementservice-policy-keys>`__. Note: The database does create a table of condition keys in case we develop future support for it, but it isn't used yet.


Log-based policy generation
----------------------------

We are considering building functionality to:

* Use Amazon Athena to query CloudTrail logs from an S3 bucket for AWS IAM API calls, similar to `CloudTracker <https://github.com/duo-labs/cloudtracker>`__.
* Instead of identifying the exact AWS IAM actions that were used, as CloudTracker currently does, we identify:
    - Resource ARNs
    - Actions that indicate a CRUD level corresponding to that resource ARN. For example, if read access is granted to an S3 bucket folder path, assume all Read actions are needed for that folder path. Otherwise, we run into issues where CloudTrail actions and IAM actions don't match, which is a well documented issue by CloudTracker.
* Query the logs to determine which principals touch which ARNs.
    - For each IAM principal, create a list of ARNs.
    - For each ARN, plug that ARN into a policy_sentry yml file, and determine the CRUD level based on a lazy comparison of the action listed in the cloudtrail log vs the resource ARN.
    - And then run the policy_sentry yml file to generate an IAM policy that would have worked.


This was discussed in `the original Hacker News post. <https://news.ycombinator.com/item?id=21262954>`__.