#! /bin/env python3

from invoke import task, Collection
from policy_sentry.command import initialize as sentry

# Create the necessary collections (namespaces)
ns = Collection()
test = Collection('test')
ns.add_collection(test)

# FIXME Add an option so we don't trample the users db that they may have installed for prod usage.
# FIXME Document this in the wiki
# TODO Document this in a contributing.md doc
@task
def create_db(c):
    sentry.initialize('')

# TODO Some kind of non-zero check to make sure that this passes.
@task
def security_scan(c):
    c.run('bandit -r policy_sentry/')
    c.run('safety check')

# TODO Implement this effectively
@task
def run_linter(c):
    print('run linter')
    print('run formatter')

# TODO If the database is not found we should build it, otherwise just run the tests.
# TODO Some kind of non-zero check to make sure that this passes.
@task
def run_tests(c):
    c.run('nosetests -v')

# TODO Implement this effectively
@task
def run_full_test_suite(c):
    print('run all tests in collection')

# Add all testing tasks to the test collection
test.add_task(create_db, 'initialize')
test.add_task(security_scan, 'security')
test.add_task(run_linter, 'lint')
test.add_task(run_tests, 'unit')
test.add_task(run_full_test_suite, 'all')
