Internals
---------------

Before reading this, make sure you have read all the other documentation - especially the `IAM Policies document <https://policy-sentry.readthedocs.io/en/latest/iam-knowledge/iam-policies.html>`_\ , which covers the Action Tables, ARN tables, and Condition Keys Tables.

Other assumptions:

* You are familiar with these Python things:

  * `click <https://click.palletsprojects.com/en/7.x/>`_
  * package imports, multi folder management
  * PyPi
  * Unit testing

Overall: How policy_sentry uses these tables
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

policy_sentry follows this process for generating policies.


#. If **User-supplied actions** is chosen:

   * Look up the actions in our master Actions Table in the database, which contains the Action Tables for all AWS services
   * If the action in the database matches the actions requested by the user, determine the ARN Format required.
   * Proceed to step 3

#. If **User-supplied ARNs with Access levels** (i.e., the ``--crud`` flag) is chosen:

   * Match the user-supplied ARNs with ARN formats in our ARN Table database, which contains the ARN tables for all AWS Services
   * If it matches, get the access level requested by the user
   * Proceed to step 3

#. Compile those into groups, sorted by an SID namespace. The SID namespace follows the format of **Service**\ , **Access Level**\ , and **Resource ARN Type**\ , with no character delimiter (to meet AWS IAM Policy formatting expectations). For example, the namespace could be ``SsmReadParameter``\ , ``KmsReadKey``\ , or ``Ec2TagInstance``.
#. Then, we associate the user-supplied ARNs matching that namespace with the SID.
#. If **User-supplied actions** is chosen:

   * Associate the IAM actions requested by the user to the service, access level, and ARN type matching the aforementioned SID namespace

#. If **User-supplied ARNs with Access levels** (i.e., the ``--crud`` flag) is chosen:

   * Associate all the IAM actions that correspond to the service, access level, and ARN type matching that SID namespace.

#. Print the policy

Project Structure
^^^^^^^^^^^^^^^^^

We'll focus mostly on the intent and approach of the major files (and subfolders) within the ``policy_sentry/shared`` directory:

Subfolders
~~~~~~~~~~

**Folders per command**:
* The folders are mostly specific to their commands. For example, consider the files in the `policy_sentry/analysis` folder.
    - The files in this folder are specific to the `analyze` command
    - They all can import from the `util` folder and the `shared` folder.
    - The files in this folder **don't import from other subfolders specific to other commands**, like `writing` or `downloading`. (*Note: There is an occasional exception here of re-using functions from the `querying` folder*)
    - Files in the `analysis` folder,  to the `analyze` command. They don't import from each other, with the occasional exception of re-using functions from the `querying` folder. They all import common methods from the `util` folder and the `shared` folder as well.

**Files**:

* ``shared/data/aws.sqlite3``\ : This is the pre-bundled IAM database. Third party packages can easily query the pre-bundled IAM database by connecting to the database like this: `db_session = connect_db('bundled')`
* ``shared/data/audit/*.txt``\ : These text files are the pre-bundled audit files that you can use with the ``analyze-iam-policy`` command. Currently they are limited to privilege escalation and resource exposure. For more information, see the page on `Analyzing IAM Policies <Analyzing-IAM-Policies>`_.
* ``shared/data/docs/*.html``\ : These are HTML files wget'd from the `Actions, Resources, and Condition Keys <2>`_ AWS documentation. This is used to build our database.
* `shared/data/access-level-overrides.yml`: This is created to override the access levels that AWS incorrectly states in their documentation. For instance, quite often, their service teams will say that an IAM action is "Tagging" when it really should be "Write" - for example, `secretsmanager:CreateSecret`.

Files and functions
~~~~~~~~~~~~~~~~~~~~

**TODO: Generate documentation automagically based on docstrings**
