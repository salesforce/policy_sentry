Testing
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


Local Unit Testing and Integration Testing: Quick and Easy
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

We highly suggest that you run all the tests before pushing a significant commit. It would be painful to copy/paste all of those lines above - so we've compiled a test script in the `utils` folder.

Just run this from the root of the repository:

.. code-block:: bash

    ./utils/run_tests.sh

It will execute all of the tests that would normally be run during the TravisCI build. If you want to see if it will pass TravisCI, you can just run that quick command on your machine.


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
    test_get_dependent_actions_double (test_actions.ActionsTestCase) ... ok
    test_get_dependent_actions_several (test_actions.ActionsTestCase) ... ok
    test_get_dependent_actions_single (test_actions.ActionsTestCase) ... ok
    test_analyze_by_access_level: Test out calling this as a library ... ok
    test_get_actions_from_policy: Verify that the get_actions_from_policy function is grabbing the actions ... ok
    test_get_actions_from_policy_file_with_explicit_actions: Verify that we can get a list of actions from a ... ok
    test_get_actions_from_policy_file_with_wildcards: Verify that we can read the actions from a file, ... ok
    test_remove_actions_not_matching_access_level: Verify remove_actions_not_matching_access_level is working as expected ... ok
    test_get_findings: Ensure that finding.get_findings() combines two risk findings for one policy properly. ... ok
    test_get_findings_by_policy_name: Testing out the 'Findings' object ... ok
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
    test_get_action_data: Tests function that gets details on a specific IAM Action. ... ok
    test_get_actions_for_service: Tests function that gets a list of actions per AWS service. ... ok
    test_get_actions_matching_condition_key: Tests a function that gathers all instances in ... ok
    test_get_actions_that_support_wildcard_arns_only: Tests function that shows all ... ok
    test_get_actions_with_access_level: Tests function that gets a list of actions in a ... ok
    test_get_actions_with_arn_type_and_access_level: Tests a function that gets a list of ... ok
    test_get_arn_type_details: Tests function that grabs details about a specific ARN name ... ok
    test_get_arn_types_for_service: Tests function that grabs arn_type and raw_arn pairs ... ok
    test_get_condition_key_details: Tests function that grabs details about a specific condition key ... ok
    test_get_condition_keys_for_service: Tests function that grabs a list of condition keys per service. ... ok
    test_get_raw_arns_for_service: Tests function that grabs a list of raw ARNs per service ... ok
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
