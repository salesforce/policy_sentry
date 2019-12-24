#!/usr/bin/env python
import sys
import os
from invoke import task, Collection
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir + '/policy_sentry/')))
from policy_sentry.command import initialize

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


# BUILD
@task
def build_package(c):
    """Build the policy_sentry package from the current directory contents for use with PyPi"""
    c.run('python -m pip install --upgrade setuptools wheel')
    c.run('python setup.py -q sdist bdist_wheel')


@task(pre=[build_package])
def install_package(c):
    """Install the policy_sentry package built from the current directory contents (not PyPi)"""
    c.run('pip3 install -q dist/policy_sentry-*.tar.gz')


@task
def uninstall_package(c):
    """Uninstall the policy_sentry package"""
    c.run('echo "y" | pip3 uninstall policy_sentry', pty=True)


@task
def upload_to_pypi_test_server(c):
    """Upload the package to the TestPyPi server (requires credentials)"""
    c.run('python -m pip install --upgrade twine')
    c.run('python -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*')
    c.run('python -m pip install --index-url https://test.pypi.org/simple/ --no-deps policy_sentry')


@task
def upload_to_pypi_prod_server(c):
    """Upload the package to the PyPi production server (requires credentials)"""
    c.run('python -m pip install --upgrade twine')
    c.run('python -m twine upload dist/*')
    c.run('python -m pip install policy_sentry')


# INTEGRATION TESTS
@task
def clean_config_directory(c):
    """Runs `rm -rf $HOME/.policy_sentry`"""
    c.run('rm -rf $HOME/.policy_sentry/')


@task
def create_db(c):
    """Integration testing: Initialize the policy_sentry database"""
    initialize.initialize('')


@task
def version_check(c):
    """Print the version"""
    c.run('./policy_sentry/bin/policy_sentry --version', pty=True)


@task(pre=[install_package])
def write_policy(c):
    """
    Integration testing: Tests the `write-policy` function.
    """
    c.run('./policy_sentry/bin/policy_sentry write-policy --crud --input-file examples/yml/crud.yml --quiet', pty=True)
    c.run('./policy_sentry/bin/policy_sentry write-policy --crud --input-file examples/yml/crud.yml', pty=True)
    c.run('./policy_sentry/bin/policy_sentry write-policy --crud --input-file examples/yml/crud.yml --minimize=0', pty=True)
    c.run('./policy_sentry/bin/policy_sentry write-policy --input-file examples/yml/actions.yml', pty=True)


@task(pre=[install_package])
def analyze_policy(c):
    """Integration testing: Tests the `analyze` functionality"""
    c.run('./policy_sentry/bin/policy_sentry analyze policy-file --policy examples/analyze/explicit-actions.json', pty=True)


@task(pre=[install_package])
def query(c):
    """Integration testing: Tests the `query` functionality (querying the IAM database)"""
    c.run('echo "Querying the action table"', pty=True)
    c.run('./policy_sentry/bin/policy_sentry query action-table --service ram', pty=True)
    c.run('./policy_sentry/bin/policy_sentry query action-table --service ram --name tagresource', pty=True)
    c.run('./policy_sentry/bin/policy_sentry query action-table '
          '--service ram --access-level permissions-management', pty=True)
    c.run('./policy_sentry/bin/policy_sentry query action-table --service ses --condition ses:FeedbackAddress', pty=True)
    c.run('echo "Querying the ARN table"', pty=True)
    c.run('./policy_sentry/bin/policy_sentry query arn-table --service ssm', pty=True)
    c.run('./policy_sentry/bin/policy_sentry query arn-table --service cloud9 --name environment', pty=True)
    c.run('./policy_sentry/bin/policy_sentry query arn-table --service cloud9 --list-arn-types', pty=True)
    c.run('echo "Querying the condition keys table"', pty=True)
    c.run('./policy_sentry/bin/policy_sentry query condition-table --service cloud9', pty=True)
    c.run('./policy_sentry/bin/policy_sentry query condition-table --service cloud9 --name cloud9:Permissions', pty=True)


# TEST - SECURITY
@task
def security_scan(c):
    """Runs `bandit` and `safety check`"""
    c.run('bandit -r policy_sentry/')
    c.run('safety check', warn=True)


# TEST - LINT
@task
def run_linter(c):
    """Linting with `pylint` and `autopep8`"""
    c.run('pylint policy_sentry/', warn=True)
    c.run('autopep8 -r --in-place policy_sentry/', warn=True)


# UNIT TESTING
@task
def run_unit_tests(c):
    """Unit testing: Runs unit tests using `nosetests`"""
    # TODO If the database is not found we should build it, otherwise just run the tests.
    c.run('echo "Running Unit tests"')
    c.run('nosetests -v --logging-level=INFO', warn=True)


# Add all testing tasks to the test collection
integration.add_task(clean_config_directory, 'clean')
integration.add_task(version_check, 'version')
integration.add_task(create_db, 'initialize')
integration.add_task(analyze_policy, 'analyze-policy')
integration.add_task(write_policy, 'write-policy')
integration.add_task(query, 'query')

unit.add_task(run_unit_tests, 'nose')

# test.add_task(run_full_test_suite, 'all')
test.add_task(run_linter, 'lint')
test.add_task(security_scan, 'security')

build.add_task(build_package, 'build-package')
build.add_task(install_package, 'install-package')
build.add_task(uninstall_package, 'uninstall-package')
build.add_task(upload_to_pypi_test_server, 'upload-test')
build.add_task(upload_to_pypi_prod_server, 'upload-prod')
