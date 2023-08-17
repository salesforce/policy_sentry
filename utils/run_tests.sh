#!/usr/bin/env bash
set -ex
# Suppress annoying warnings
#export PIPENV_VERBOSITY=-1
pip install -r requirements.txt
pip install -r requirements-dev.txt

invoke build.uninstall-package
invoke build.install-package
invoke integration.clean
invoke integration.version
invoke unit.pytest
invoke integration.query
invoke integration.query-yaml
invoke integration.write-policy
invoke test.security
invoke docs.clean-html
invoke docs.make-html
