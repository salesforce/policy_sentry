Testing
=======

Pipenv
------

```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

Invoke
------

To run and develop Policy Sentry without having to install from PyPi,
you can use Invoke.

```bash
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
  docs.make-html               Make the HTML docs locally
  docs.open-html-docs          Open HTML docs in Google Chrome locally on your
                               computer
  docs.remove-html-files       Remove the html files
  integration.analyze-policy   Integration testing: Tests the `analyze`
                               functionality
  integration.clean            Runs `rm -rf $HOME/.policy_sentry`
  integration.initialize       Integration testing: Initialize the
                               policy_sentry database
  integration.query            Integration testing: Tests the `query`
                               functionality (querying the IAM database)
  integration.query-yaml       Integration testing: Tests the `query`
                               functionality (querying the IAM database) - but
                               with yaml
  integration.version          Print the version
  integration.write-policy     Integration testing: Tests the `write-policy`
                               function.
  test.lint                    Linting with `pylint` and `autopep8`
  test.security                Runs `bandit` and `safety check`
  unit.pytest                  Unit testing: Runs unit tests using `pytest`


# To run them, specify `invoke` plus the options:
invoke build.build-package

invoke integration.clean
invoke integration.initialize
invoke integration.analyze-policy
invoke integration.query
invoke integration.write-policy

invoke test.security
```

Local Unit Testing and Integration Testing:
------------------------------------------

### Strategy to write new unit tests

See the writeup here: [https://github.com/salesforce/policy_sentry/pull/254#issuecomment-710098269](https://github.com/salesforce/policy_sentry/pull/254#issuecomment-710098269)


### Quick and Easy way to run tests

Just run this from the root of the repository:

We highly suggest that you run all the tests before pushing a
significant commit. It would be painful to copy/paste all of those lines
above - so we've compiled a test script in the `utils`
folder.

```bash
./utils/run_tests.sh
```

It will execute all of the tests that would normally be run during the  build. If you want to see if it will pass GitHub actions, you can
just run that quick command on your machine.

Running the Test Suite
----------------------

We use [pytest](https://docs.pytest.org/en//) for unit testing.
All tests are placed in the `test` folder.

-   Just run the following:

```bash
pytest -v

# This will output the print() statements in your test code
pytest -v --show-capture=no

# This will include the debug logging statements in the test output
pytest -v --log-level=DEBUG
```

-   Alternatively, you can use `invoke`, as mentioned above:

```bash
invoke unit.pytest
```

Output:

```text
test/analysis/test_analyze.py::AnalysisExpandWildcardActionsTestCase::test_a_determine_actions_to_expand_not_upper_camelcase PASSED  [  0%]
test/analysis/test_analyze.py::AnalysisExpandWildcardActionsTestCase::test_analyze_by_access_level PASSED                            [  1%]
test/analysis/test_analyze.py::AnalysisExpandWildcardActionsTestCase::test_analyze_statement_by_access_level PASSED                  [  2%]
test/analysis/test_analyze.py::AnalysisExpandWildcardActionsTestCase::test_determine_actions_to_expand PASSED                        [  2%]
test/analysis/test_analyze.py::AnalysisExpandWildcardActionsTestCase::test_gh_162 PASSED                                             [  3%]
test/analysis/test_expand.py::PolicyExpansionTestCase::test_policy_expansion PASSED                                                  [  4%]
...

========================================================= 134 passed in 51.04s ============================================================
```
