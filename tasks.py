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

# TODO Implement this effectively
@task
def security_scan(c):
    print('run bandit')
    print('run safety')

# TODO Implement this effectively
@task
def run_linter(c):
    print('run linter')
    print('run formatter')

# TODO Implement this effectively
@task
def run_tests(c):
    print('run unit tests')

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
