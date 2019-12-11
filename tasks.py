#! /bin/env python3

from invoke import task, Collection

# Create the necessary collections (namespaces)
ns = Collection()
test = Collection('test')
ns.add_collection(test)

integration = Collection('integration')
ns.add_collection(integration)

unit = Collection('unit')
ns.add_collection(unit)

build = Collection('build')
ns.add_collection(build)
# FIXME Add an option so we don't trample the users db that they may have installed for prod usage.
# FIXME Document this in the wiki
# TODO Document this in a contributing.md doc
# TODO Some kind of non-zero check to make sure that some of these things pass

# INTEGRATION TESTS
@task
def clean_config_directory(c):
    c.run('rm -rf $HOME/.policy_sentry/')


@task
def create_db(c):
    c.run('python3 policy_sentry/bin/policy_sentry initialize')


@task
def write_policy(c):
    c.run('python3 policy_sentry/bin/policy_sentry write-policy --crud --input-file examples/yml/crud.yml')
    c.run('python3 policy_sentry/bin/policy_sentry write-policy --crud --input-file examples/yml/crud.yml')
    c.run('python3 policy_sentry/bin/policy_sentry write-policy --input-file examples/yml/actions.yml')


@task
def analyze_policy(c):
    c.run('python3 policy_sentry/bin/policy_sentry analyze policy-file --policy examples/analyze/explicit-actions.json')


@task
def query(c):
    c.run('echo "Querying the action table"')
    c.run('python3 policy_sentry/bin/policy_sentry query action-table --service ram')
    c.run('python3 policy_sentry/bin/policy_sentry query action-table --service ram --name tagresource')
    c.run('python3 policy_sentry/bin/policy_sentry query action-table '
          '--service ram --access-level permissions-management')
    c.run('python3 policy_sentry/bin/policy_sentry query action-table --service ses --condition ses:FeedbackAddress')
    c.run('echo "Querying the ARN table"')
    c.run('python3 policy_sentry/bin/policy_sentry query arn-table --service ssm')
    c.run('python3 policy_sentry/bin/policy_sentry query arn-table --service cloud9 --name environment')
    c.run('python3 policy_sentry/bin/policy_sentry query arn-table --service cloud9 --list-arn-types')
    c.run('echo "Querying the condition keys table"')
    c.run('python3 policy_sentry/bin/policy_sentry query condition-table --service cloud9')
    c.run('python3 policy_sentry/bin/policy_sentry query condition-table --service cloud9 --name cloud9:Permissions')

# TEST
@task
def security_scan(c):
    c.run('bandit -r policy_sentry/')
    c.run('safety check', warn=True)


@task
def run_linter(c):
    c.run('pylint policy_sentry/', warn=True)
    c.run('autopep8 -r --in-place policy_sentry/', warn=True)


# UNIT
@task
def run_unit_tests(c):
    # TODO If the database is not found we should build it, otherwise just run the tests.
    c.run('echo "Running Unit tests"')
    c.run('nosetests -v', warn=True)


@task(create_db, analyze_policy, write_policy, query)
def run_integration_tests(c):
    # TODO If the database is not found we should build it, otherwise just run the tests.
    c.run('echo "Running Integration tests"')


# @task(pre=[run_integration_tests, run_unit_tests])
# def run_full_test_suite(c):
#     c.run('echo "run all tests in collection"')
#     run_integration_tests()
#     run_unit_tests()


# BUILD
@task
def build_pypi_package(c):
    c.run('python3 -m pip install --upgrade setuptools wheel')
    c.run('python3 setup.py sdist bdist_wheel')


@task
def upload_to_pypi_test_server(c):
    c.run('python3 -m pip install --upgrade twine')
    # TODO: Figure out how to grab the creds from environment variables in travis and then release
    c.run('python3 -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*')
    c.run('python3 -m pip install --index-url https://test.pypi.org/simple/ --no-deps policy_sentry')


@task
def upload_to_pypi_prod_server(c):
    c.run('python3 -m pip install --upgrade twine')
    # TODO: Figure out how to grab the creds from environment variables in travis and then release
    c.run('python3 -m twine upload dist/*')
    c.run('python3 -m pip install policy_sentry')


# Add all testing tasks to the test collection
integration.add_task(clean_config_directory, 'clean')
integration.add_task(create_db, 'initialize')
integration.add_task(analyze_policy, 'analyze-policy')
integration.add_task(write_policy, 'write-policy')
integration.add_task(query, 'query')
integration.add_task(run_integration_tests, 'all')

unit.add_task(run_unit_tests, 'nose')

# test.add_task(run_full_test_suite, 'all')
test.add_task(run_linter, 'lint')
test.add_task(security_scan, 'security')

build.add_task(build_pypi_package, 'build-package')
build.add_task(upload_to_pypi_test_server, 'upload-test')
build.add_task(upload_to_pypi_prod_server, 'upload-prod')
