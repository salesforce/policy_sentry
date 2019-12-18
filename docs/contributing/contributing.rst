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



Developing Locally
-----------------------


Pipenv
~~~~~~

.. code-block:: bash

   pipenv --python 3.7  # create the environment
   pipenv shell         # start the environment
   pipenv install       # install both development and production dependencies

Invoke
~~~~~~

To run and develop Policy Sentry without having to install from PyPi, you can use Invoke.

.. code-block:: bash

    # List available tasks
    invoke -l

    # that will show the following options:
    Available tasks:

      build.build-package          Build the policy_sentry package from the current
                                   directory contents for use with PyPi
      build.install-package        Install the policy_sentry package built from the
                                   current directory contents (not PyPi)
      build.uninstall-package      Uninstall the policy_sentry package
      build.upload-prod            Upload the package to the PyPi production server
                                   (requires credentials)
      build.upload-test            Upload the package to the TestPyPi server
                                   (requires credentials)
      integration.analyze-policy   Integration testing: Tests the `analyze`
                                   functionality
      integration.clean            Runs `rm -rf $HOME/.policy_sentry`
      integration.initialize       Integration testing: Initialize the
                                   policy_sentry database
      integration.query            Integration testing: Tests the `query`
                                   functionality (querying the IAM database)
      integration.write-policy     Integration testing: Tests the `write-policy`
                                   function
      test.lint                    Linting with `pylint` and `autopep8`
      test.security                Runs `bandit` and `safety check`
      unit.nose                    Unit testing: Runs unit tests using `nosetests`


    # To run them, specify `invoke` plus the options:
    invoke build.build-package

    invoke integration.clean
    invoke integration.initialize
    invoke integration.analyze-policy
    invoke integration.query
    invoke integration.write-policy

    invoke test.lint
    invoke test.security

    invoke unit.nose



Running the Test Suite
~~~~~~~~~~~~~~~~~~~~~~~~

We use `Nose <https://nose.readthedocs.io/en/latest/>`_ for unit testing. All tests are placed in the ``tests`` folder.


* Just run the following:

.. code-block:: bash

    nosetests -v


* Alternatively, you can use `invoke`, as mentioned above:

.. code-block:: bash

    invoke test.unit

Output:

.. code-block:: text

    test_overrides_yml_config: Tests the format of the overrides yml file for the RAM service ... ok
    test_passing_overall_iam_action_override: Tests iam:CreateAccessKey ... ok
    test_get_actions_by_access_level (test_actions.ActionsTestCase) ... ok
    test_get_dependent_actions_double (test_actions.ActionsTestCase) ... ok
    test_get_dependent_actions_several (test_actions.ActionsTestCase) ... ok
    test_get_dependent_actions_single (test_actions.ActionsTestCase) ... ok
    test_get_findings: Ensure that finding.get_findings() combines two risk findings for one policy properly. ... ok
    test_get_findings_by_policy_name (test_analyze.FindingsTestCase) ... ok
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
    test_query_action_table: Tests function that gets a list of actions per AWS service. ... ok
    test_query_action_table_by_access_level: Tests function that gets a list of actions in a ... ok
    test_query_action_table_by_arn_type_and_access_level: Tests a function that gets a list of ... ok
    test_query_action_table_by_name: Tests function that gets details on a specific IAM Action. ... ok
    test_query_action_table_for_actions_supporting_wildcards_only: Tests function that shows all ... ok
    test_query_action_table_for_service_specific_condition_key_matches: Tests a function that gathers all instances in ... ok
    test_query_arn_table_by_name: Tests function that grabs details about a specific ARN name ... ok
    test_query_arn_table_for_arn_types: Tests function that grabs arn_type and raw_arn pairs ... ok
    test_query_arn_table_for_raw_arns: Tests function that grabs a list of raw ARNs per service ... ok
    test_query_condition_table: Tests function that grabs a list of condition keys per service. ... ok
    test_query_condition_table_by_name: Tests function that grabs details about a specific condition key ... ok
    test_remove_actions_that_are_not_wildcard_arn_only: Tests function that removes actions from a list that ... ok
    test_actions_template (test_template.TemplateTestCase) ... ok
    test_crud_template (test_template.TemplateTestCase) ... ok
    test_print_policy_with_actions_having_dependencies (test_write_policy.WritePolicyActionsTestCase) ... ok
    test_write_policy (test_write_policy.WritePolicyCrudTestCase) ... ok
    Tests ARNs with the partiion `aws-cn` instead of just `aws` ... ok
    Tests ARNs with the partition `aws-us-gov` instead of `aws` ... ok
    test_wildcard_when_not_necessary: Attempts bypass of CRUD mode wildcard-only ... ok
    test_actions_missing_actions: write-policy actions if the actions block is missing ... ok
    test_allow_missing_access_level_categories_in_cfg: write-policy --crud when the YAML file ... ok
    test_allow_empty_access_level_categories_in_cfg: If the content of a list is an empty string, it should sysexit ... ok
    test_actions_missing_arn: write-policy actions command when YAML file block is missing an ARN ... ok
    test_actions_missing_description: write-policy when the YAML file is missing a description ... ok
    test_actions_missing_name: write-policy when the YAML file is missing a name ... ok

    ----------------------------------------------------------------------
    Ran 44 tests in 1.762s

    OK

Updating the AWS HTML files
----------------------------

This will update the HTML files stored in `policy_sentry/shared/data/docs/list_*.partial.html`

.. code-block:: bash

   ./utils/download_docs.py


