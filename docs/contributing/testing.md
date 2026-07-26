Testing
=======

Uv
------

```bash
uv sync --frozen
```

Just
----

To run and develop Policy Sentry without having to install from PyPi,
you can use the [just](https://github.com/casey/just) task runner.

```bash
# List available recipes
just --list

# Unit tests: runs pytest with coverage (what CI runs)
just unit-tests

# Integration tests: initializes the database and exercises the CLI
# (query action-table/arn-table/condition-table, write-policy)
just integration-tests

# Build the package
just build-package

# Build and serve the docs locally
just build-docs
just serve-docs
```

Local Unit Testing and Integration Testing:
------------------------------------------

### Strategy to write new unit tests

See the writeup here: [https://github.com/salesforce/policy_sentry/pull/254#issuecomment-710098269](https://github.com/salesforce/policy_sentry/pull/254#issuecomment-710098269)


### Quick and Easy way to run tests

Just run this from the root of the repository:

We highly suggest that you run all the tests before pushing a
significant commit.

```bash
just unit-tests
just integration-tests
```

These are the same recipes that run during the GitHub Actions build, so
if they pass on your machine the CI test jobs should pass too.

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

-   Alternatively, you can use `just`, as mentioned above:

```bash
just unit-tests
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
