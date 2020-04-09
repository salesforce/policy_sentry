Project Structure
=================

We'll focus mostly on the intent and approach of the major files (and subfolders) within the ``policy_sentry/shared`` directory:

Subfolders
~~~~~~~~~~

**Folders per command**:

* The folders are mostly specific to their commands. For example, consider the files in the `policy_sentry/analysis` folder.
* The files in this folder are specific to the `analyze` command
   - They all can import from the `util` folder and the `shared` folder.
   - The files in this folder **don't import from other subfolders specific to other commands**, like `writing` or `downloading`. (*Note: There is an occasional exception here of re-using functions from the `querying` folder*)
   - Files in the `analysis` folder,  to the `analyze` command. They don't import from each other, with the occasional exception of re-using functions from the `querying` folder. They all import common methods from the `util` folder and the `shared` folder as well.


**Files**:

* ``shared/data/aws.sqlite3``\ : This is the pre-bundled IAM database. Third party packages can easily query the pre-bundled IAM database by connecting to the database like this: ``
* ``shared/data/audit/*.txt``\ : These text files are the pre-bundled audit files that you can use with the ``analyze-iam-policy`` command. Currently they are limited to privilege escalation and resource exposure. For more information, see the page on `Analyzing IAM Policies <Analyzing-IAM-Policies>`_.
* ``shared/data/docs/*.html``\ : These are HTML files wget'd from the `Actions, Resources, and Condition Keys <2>`_ AWS documentation. This is used to build our database.
* `shared/data/access-level-overrides.yml`: This is created to override the access levels that AWS incorrectly states in their documentation. For instance, quite often, their service teams will say that an IAM action is "Tagging" when it really should be "Write" - for example, `secretsmanager:CreateSecret`.

Files and functions
~~~~~~~~~~~~~~~~~~~~

**TODO: Generate documentation automagically based on docstrings**
