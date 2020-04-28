#!/usr/bin/env bash
set -x
pipenv install --dev
pipenv run invoke build.build-package
pipenv uninstall --all
pipenv run pip install homebrew-pypi-poet
pipenv run pip install policy_sentry -U
pipenv run poet -f policy_sentry > HomebrewFormula/policy_sentry.rb
