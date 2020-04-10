#!/usr/bin/env bash
set -ex
# Suppress annoying warnings
export PIPENV_VERBOSITY=-1

pip3 install pipenv
pipenv install --dev

pipenv run invoke test.lint
pipenv run invoke build.uninstall-package
pipenv run invoke build.install-package
pipenv run invoke integration.clean
pipenv run invoke integration.version
#pipenv run invoke unit.nose
pipenv run invoke unit.pytest
pipenv run invoke integration.query
pipenv run invoke integration.query-yaml
pipenv run invoke integration.write-policy
pipenv run invoke test.security
pipenv run invoke docs.clean-html
pipenv run invoke docs.make-html
