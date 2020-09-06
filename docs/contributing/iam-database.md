IAM Database
============

Policy Sentry leverages HTML files from the [Actions, Resources, and
Condition Keys
page](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_actions-resources-contextkeys.html)
AWS documentation to build the IAM database.

-   These HTML files are included as part of the PyPi package
-   The database itself is

This design choice was made for a few reasons:

1.  **Don't break because of AWS**: The automation must **not** break
    if the AWS website is down, or if AWS drastically changes the
    documentation.
2.  **Replicability**: Two `git clones` that build the data source
    should always have the same results
3.  **Easy to review**: The repository itself should contain
    easy-to-understand and easy-to-view documentation, which the user
    can replicate, to verify with the human eye that no malicious
    changes have been made.
    -   This means no JSON files with complicated structures, or Binary
        files (the latter of which does not permit `git diff`) in the
        repository.
    -   This helps to mitigate the concern that open source software
        could be modified to alter IAM permissions at other
        organizations.

How Policy Sentry uses the IAM database
---------------------------------------

policy_sentry follows this process for generating policies.

1.  If the **User-supplied actions** template is provided:
    -   Look up the actions in our master Actions Table in the database,
        which contains the Action Tables for all AWS services
    -   If the action in the database matches the actions requested by
        the user, determine the ARN Format required.
    -   Proceed to step 3
2.  If **User-supplied ARNs with Access levels** template was provided:
    -   Match the user-supplied ARNs with ARN formats in our ARN Table
        database, which contains the ARN tables for all AWS Services
    -   If it matches, get the access level requested by the user
    -   Proceed to step 3
3.  Compile those into groups, sorted by an SID namespace. The SID
    namespace follows the format of **Service**, **Access Level**, and
    **Resource ARN Type**, with no character delimiter (to meet AWS IAM
    Policy formatting expectations). For example, the namespace could be
    `SsmReadParameter`, `KmsReadKey`, or `Ec2TagInstance`.
4.  Then, we associate the user-supplied ARNs matching that namespace
    with the SID.
5.  If **User-supplied actions** template was provided:
    -   Associate the IAM actions requested by the user to the service,
        access level, and ARN type matching the aforementioned SID
        namespace
6.  If the **User-supplied ARNs with Access levels** template was
    provided:
    -   Associate all the IAM actions that correspond to the service,
        access level, and ARN type matching that SID namespace.
7.  Print the policy

### Updating the AWS HTML files

The command shown below downloads the Actions, Resources, and Condition
Keys pages per-service to the `policy_sentry/shared/data/docs` folder.

-   The HTML files will be stored in
    `policy_sentry/shared/data/docs/list_*.html`
-   It also builds a JSON file that serves as the IAM data source to include as part of the PyPi
    package.

This will update the HTML files stored in
`policy_sentry/shared/data/docs/[list]()*.html`:

```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt
python3 ./utils/download_docs.py
```

This downloads the Actions, Resources, and Condition Keys pages
per-service to the `policy_sentry/shared/data/docs` folder.

When a user runs `policy_sentry initialize`, these files are copied over
to the config folder (`~/.policy_sentry/`).

This design choice was made for a few reasons:

1.  **Don't break because of AWS**: The automation must **not** break
    if the AWS website is down, or if AWS drastically changes the
    documentation.

2.  **Replicability**: Two `git clone`s that build the
    local database should always have the same results

3.

    **Easy to review**: The repository itself should contain easy-to-understand and easy-to-view documentation, which the user can replicate, to verify with the human eye that no malicious changes have been made.

    :   -   This means no JSON files with complicated structures, or
            Binary files (the latter of which does not permit
            `git diff`) in the repository.
        -   This helps to mitigate the concern that open source software
            could be modified to alter IAM permissions at other
            organizations.
