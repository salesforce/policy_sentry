#! /bin/env python3

from invoke import task
from policy_sentry.command import initialize as matty

@task
def prep(c):
    # c.run("echo test initialize")
    matty.initialize('')




# ns = Collection()
# test = Collection('test')

# ns.add_collection(test)
# test.add_task(prep, 'initialize')

# from invoke import task

# @task
# def build(c):
#     print("Building!")
