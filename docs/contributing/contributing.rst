Contributing
============

Want to contribute back to Policy Sentry? This page describes the general development
flow, our philosophy, the test suite, and issue tracking.

Impostor Syndrome Disclaimer
----------------------------

Before we get into the details: **We want your help. No, really.**

There may be a little voice inside your head that is telling you that you're
not ready to be an open source contributor; that your skills aren't nearly good
enough to contribute. What could you possibly offer a project like this one?

We assure you -- the little voice in your head is wrong. If you can write code
at all, you can contribute code to open source. Contributing to open source
projects is a fantastic way to advance one's coding skills. Writing perfect
code isn't the measure of a good developer (that would disqualify all of us!);
it's trying to create something, making mistakes, and learning from those
mistakes. That's how we all improve.

We've provided some clear `Contribution Guidelines`_ that you can read below.
The guidelines outline the process that you'll need to follow to get a patch
merged. By making expectations and process explicit, we hope it will make it
easier for you to contribute.

And you don't just have to write code. You can help out by writing
documentation, tests, or even by giving feedback about this work. (And yes,
that includes giving feedback about the contribution guidelines.)

(`Adrienne Friend`_ came up with this disclaimer language.)

.. _Adrienne Friend: https://github.com/adriennefriend/imposter-syndrome-disclaimer


Documentation
-------------

If you're looking to help document Policy Sentry, your first step is to get set up with Sphinx, our documentation tool. First you will want to make sure you have a few things on your local system:

* python-dev (if you're on OS X, you already have this)
* pip
* pipenv

Once you've got all that, the rest is simple:

::

    # If you have a fork, you'll want to clone it instead
    git clone git@github.com:salesforce/policy_sentry.git

    # Set up the Pipenv
    pipenv install --skip-lock
    pipenv shell

    # Enter the docs directory and compile
    cd docs/
    make html

    # View the file titled docs/_build/html/index.html in your browser



Building Documentation
~~~~~~~~~~~~~~~~~~~~~~

Inside the ``docs`` directory, you can run ``make`` to build the documentation.
See ``make help`` for available options and the `Sphinx Documentation
<http://sphinx-doc.org/contents.html>`_ for more information.


Coding Standards
----------------

* Use `Python Black <https://black.readthedocs.io/en/stable/>`__ to adhere to pep8 automagically.


Developing Against HEAD
-----------------------


Pipenv
~~~~~~

.. code-block:: bash

   pipenv --python 3.7  # create the environment
   pipenv shell         # start the environment
   pipenv install       # install both development and production dependencies


Running the Test Suite
----------------------

I use `Nose <https://nose.readthedocs.io/en/latest/>`_ for unit testing. All tests are placed in the ``tests`` folder.


* Just run the following:

.. code-block:: bash

   nosetests -v

Output:

.. code-block:: text

   Tests the format of the overrides yml file for the RAM service ... ok
   Tests iam:CreateAccessKey (in overrides file as Permissions management, but in the AWS docs as Write) ... ok
   test_get_actions_by_access_level (test_actions.ActionsTestCase) ... ok
   test_get_dependent_actions_double (test_actions.ActionsTestCase) ... ok
   test_get_dependent_actions_several (test_actions.ActionsTestCase) ... ok
   test_get_dependent_actions_single (test_actions.ActionsTestCase) ... ok
   test_add_s3_permissions_management_arn (test_arn_action_group.ArnActionGroupTestCase) ... ok
   test_get_policy_elements (test_arn_action_group.ArnActionGroupTestCase) ... ok
   test_update_actions_for_raw_arn_format (test_arn_action_group.ArnActionGroupTestCase) ... ok
   test_does_arn_match_case_1 (test_arns.ArnsTestCase) ... ok
   test_does_arn_match_case_2 (test_arns.ArnsTestCase) ... ok
   test_does_arn_match_case_4 (test_arns.ArnsTestCase) ... ok
   test_does_arn_match_case_5 (test_arns.ArnsTestCase) ... ok
   test_does_arn_match_case_6 (test_arns.ArnsTestCase) ... ok
   test_does_arn_match_case_bucket (test_arns.ArnsTestCase) ... ok
   test_determine_actions_to_expand: provide expanded list of actions, like ecr:* ... ok
   test_minimize_statement_actions (test_minimize_wildcard_actions.MinimizeWildcardActionsTestCase) ... ok
   test_actions_template (test_template.TemplateTestCase) ... ok
   test_crud_template (test_template.TemplateTestCase) ... ok
   test_print_policy_with_actions_having_dependencies (test_write_policy.WritePolicyActionsTestCase) ... ok
   test_write_policy (test_write_policy.WritePolicyCrudTestCase) ... ok
   test_actions_missing_actions: write-policy actions if the actions block is missing ... ok
   test_allow_missing_access_level_categories_in_cfg: write-policy --crud when the YAML file is missing access level categories ... ok
   test_allow_empty_access_level_categories_in_cfg: If the content of a list is an empty string, it should sysexit ... ok
   test_actions_missing_arn: write-policy actions command when YAML file block is missing an ARN ... ok
   test_actions_missing_description: write-policy when the YAML file is missing a description ... ok
   test_actions_missing_name: write-policy when the YAML file is missing a name? ... ok


Updating the AWS HTML files
----------------------------

Run the following:

.. code-block:: bash

   ./utils/grab-docs.sh
   # Or:
   ./utils/download-docs.sh

Contribution Guidelines
=======================

Fill this in later.
