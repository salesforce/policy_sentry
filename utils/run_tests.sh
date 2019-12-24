#!/usr/bin/env bash
set -ex
# Suppress annoying warnings
export PIPENV_VERBOSITY=-1

pip3 install pipenv
pipenv install --dev

pipenv run invoke build.uninstall-package
pipenv run invoke build.install-package
pipenv run invoke test.lint
pipenv run invoke integration.clean
pipenv run invoke integration.version
pipenv run invoke integration.initialize
pipenv run invoke unit.nose
pipenv run invoke integration.analyze-policy
pipenv run invoke integration.query
pipenv run invoke integration.write-policy
pipenv run invoke test.security
