#!/usr/bin/env python
import sys
import os
from invoke import task, Collection, UnexpectedExit, Failure
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir + '/policy_sentry/')))
from policy_sentry.command import initialize

# Create the necessary collections (namespaces)
ns = Collection()

docs = Collection('docs')
ns.add_collection(docs)

test = Collection('test')
ns.add_collection(test)

integration = Collection('integration')
ns.add_collection(integration)

unit = Collection('unit')
ns.add_collection(unit)

build = Collection('build')
ns.add_collection(build)


@task
def make_html(c):
    """Make the HTML docs locally"""
    c.run('make -C ./docs html')


@task
def remove_html_files(c):
    """Remove the html files"""
    c.run('rm -rf ./docs/_build/*')
    c.run('rmdir ./docs/_build/')


@task
def open_html_docs(c):
    """Open HTML docs in Google Chrome locally on your computer"""
    c.run('open -a "Google Chrome" docs/_build/html/index.html')


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
    try:
        c.run('rm -rf $HOME/.policy_sentry/')
    except UnexpectedExit as u_e:
        print(f"FAIL! UnexpectedExit: {u_e}")
        sys.exit(-1)
    except Failure as f_e:
        print(f"FAIL: Failure: {f_e}")
        sys.exit(-1)


@task
def create_db(c):
    """Integration testing: Initialize the policy_sentry database"""
    try:
        initialize.initialize('')
    except UnexpectedExit as u_e:
        print(f"FAIL! UnexpectedExit: {u_e}")
        sys.exit()
    except Failure as f_e:
        print(f"FAIL: Failure: {f_e}")
        sys.exit()


@task
def version_check(c):
    """Print the version"""
    try:
        c.run('./policy_sentry/bin/policy_sentry --version', pty=True)
    except UnexpectedExit as u_e:
        print(f"FAIL! UnexpectedExit: {u_e}")
        sys.exit()
    except Failure as f_e:
        print(f"FAIL: Failure: {f_e}")
        sys.exit()


@task(pre=[install_package])
def write_policy(c):
    """
    Integration testing: Tests the `write-policy` function.
    """
    try:
        c.run('./policy_sentry/bin/policy_sentry write-policy --crud --input-file examples/yml/crud.yml', pty=True)
        c.run('./policy_sentry/bin/policy_sentry write-policy --crud --input-file examples/yml/crud.yml', pty=True)
        c.run('./policy_sentry/bin/policy_sentry write-policy --input-file examples/yml/actions.yml', pty=True)
    except UnexpectedExit as u_e:
        print(f"FAIL! UnexpectedExit: {u_e}")
        sys.exit()
    except Failure as f_e:
        print(f"FAIL: Failure: {f_e}")
        sys.exit()


@task(pre=[install_package])
def analyze_policy(c):
    """Integration testing: Tests the `analyze` functionality"""
    try:
        c.run('./policy_sentry/bin/policy_sentry analyze policy-file --policy examples/analyze/explicit-actions.json', pty=True)
    except UnexpectedExit as u_e:
        print(f"FAIL! UnexpectedExit: {u_e}")
        sys.exit()
    except Failure as f_e:
        print(f"FAIL: Failure: {f_e}")
        sys.exit()


@task(pre=[install_package])
def query(c):
    """Integration testing: Tests the `query` functionality (querying the IAM database)"""
    try:
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
    except UnexpectedExit as u_e:
        print(f"FAIL! UnexpectedExit: {u_e}")
        sys.exit()
    except Failure as f_e:
        print(f"FAIL: Failure: {f_e}")
        sys.exit()


@task(pre=[install_package])
def query_with_yaml(c):
    """Integration testing: Tests the `query` functionality (querying the IAM database) - but with yaml"""
    try:
        c.run('echo "Querying the action table with yaml option"')
        c.run('echo "Querying the action table"', pty=True)
        c.run('./policy_sentry/bin/policy_sentry query action-table --service ram --fmt yaml', pty=True)
        c.run('./policy_sentry/bin/policy_sentry query action-table --service ram --name tagresource --fmt yaml', pty=True)
        c.run('./policy_sentry/bin/policy_sentry query action-table ''--service ram --access-level permissions-management --fmt yaml', pty=True)
        c.run('./policy_sentry/bin/policy_sentry query action-table --service ses --condition ses:FeedbackAddress --fmt yaml', pty=True)
        c.run('echo "Querying the ARN table"', pty=True)
        c.run('./policy_sentry/bin/policy_sentry query arn-table --service ssm --fmt yaml', pty=True)
        c.run('./policy_sentry/bin/policy_sentry query arn-table --service cloud9 --name environment --fmt yaml', pty=True)
        c.run('./policy_sentry/bin/policy_sentry query arn-table --service cloud9 --list-arn-types --fmt yaml', pty=True)
        c.run('echo "Querying the condition keys table"', pty=True)
        c.run('./policy_sentry/bin/policy_sentry query condition-table --service cloud9 --fmt yaml', pty=True)
        c.run('./policy_sentry/bin/policy_sentry query condition-table --service cloud9 --name cloud9:Permissions --fmt yaml', pty=True)
    except UnexpectedExit as u_e:
        print(f"FAIL! UnexpectedExit: {u_e}")
        sys.exit()
    except Failure as f_e:
        print(f"FAIL: Failure: {f_e}")
        sys.exit()


# TEST - SECURITY
@task
def security_scan(c):
    """Runs `bandit` and `safety check`"""
    try:
        c.run('bandit -r policy_sentry/')
        c.run('safety check')
    except UnexpectedExit as u_e:
        print(f"FAIL! UnexpectedExit: {u_e}")
        sys.exit()
    except Failure as f_e:
        print(f"FAIL: Failure: {f_e}")
        sys.exit()


# TEST - LINT
@task
def run_linter(c):
    """Linting with `pylint` and `autopep8`"""
    try:
        c.run('autopep8 -r --in-place policy_sentry/', warn=False)
        c.run('pylint policy_sentry/', warn=False)
    except UnexpectedExit as u_e:
        print(f"FAIL! UnexpectedExit: {u_e}")
        sys.exit()
    except Failure as f_e:
        print(f"FAIL: Failure: {f_e}")
        sys.exit()


# UNIT TESTING
@task
def run_nosetests(c):
    """Unit testing: Runs unit tests using `nosetests`"""
    c.run('echo "Running Unit tests"')
    try:
        c.run('nosetests -v')
    except UnexpectedExit as u_e:
        print(f"FAIL! UnexpectedExit: {u_e}")
        sys.exit()
    except Failure as f_e:
        print(f"FAIL: Failure: {f_e}")
        sys.exit()


@task
def run_pytest(c):
    """Unit testing: Runs unit tests using `pytest`"""
    c.run('echo "Running Unit tests"')
    try:
        c.run('python -m pytest -v')
    except UnexpectedExit as u_e:
        print(f"FAIL! UnexpectedExit: {u_e}")
        sys.exit()
    except Failure as f_e:
        print(f"FAIL: Failure: {f_e}")
        sys.exit()


# Add all testing tasks to the test collection
integration.add_task(clean_config_directory, 'clean')
integration.add_task(version_check, 'version')
integration.add_task(create_db, 'initialize')
integration.add_task(analyze_policy, 'analyze-policy')
integration.add_task(write_policy, 'write-policy')
integration.add_task(query, 'query')
integration.add_task(query_with_yaml, 'query-yaml')

unit.add_task(run_nosetests, 'nose')
unit.add_task(run_pytest, 'pytest')

docs.add_task(remove_html_files, 'remove-html-files')
docs.add_task(make_html, 'make-html')
docs.add_task(open_html_docs, 'open-html-docs')

# test.add_task(run_full_test_suite, 'all')
test.add_task(run_linter, 'lint')
test.add_task(security_scan, 'security')

build.add_task(build_package, 'build-package')
build.add_task(install_package, 'install-package')
build.add_task(uninstall_package, 'uninstall-package')
build.add_task(upload_to_pypi_test_server, 'upload-test')
build.add_task(upload_to_pypi_prod_server, 'upload-prod')
