default:
    @just --list

[group('docs')]
build-docs:
    mkdocs build

[group('package')]
build-package: clean
    uv build

[group('package')]
clean:
    rm -rf dist/
    rm -rf *.egg-info

[group('docker')]
docker-build:
    docker build -t policy_sentry .

[group('docs')]
download-latest-aws-docs:
    uv run ./utils/download_docs.py

[group('test')]
_int-clean:
    rm -rf "$HOME/.policy_sentry/"

[group('test')]
_int-init:
    uv run ./utils/copy_docs.py
    uv run ./policy_sentry/bin/cli.py initialize

[group('test')]
_int-query-action:
    uv run ./policy_sentry/bin/cli.py query action-table --service ram
    uv run ./policy_sentry/bin/cli.py query action-table --service ram --name tagresource
    uv run ./policy_sentry/bin/cli.py query action-table --service ram --access-level permissions-management
    uv run ./policy_sentry/bin/cli.py query action-table --service ssm --resource-type parameter
    uv run ./policy_sentry/bin/cli.py query action-table --service ssm --access-level write --resource-type parameter
    uv run ./policy_sentry/bin/cli.py query action-table --service ses --condition ses:FeedbackAddress

[group('test')]
_int-query-arn:
    uv run ./policy_sentry/bin/cli.py query arn-table --service ssm
    uv run ./policy_sentry/bin/cli.py query arn-table --service cloud9 --name environment
    uv run ./policy_sentry/bin/cli.py query arn-table --service cloud9 --list-arn-types

[group('test')]
_int-query-condition:
    uv run ./policy_sentry/bin/cli.py query condition-table --service cloud9
    uv run ./policy_sentry/bin/cli.py query condition-table --service cloud9 --name cloud9:Permissions

[group('test')]
_int-write-policy:
    uv run ./policy_sentry/bin/cli.py write-policy --input-file examples/yml/crud.yml
    uv run ./policy_sentry/bin/cli.py write-policy --input-file examples/yml/crud.yml
    uv run ./policy_sentry/bin/cli.py write-policy --input-file examples/yml/actions.yml

[group('test')]
_int-version:
    uv run ./policy_sentry/bin/cli.py --version

[group('test')]
integration-tests: _int-clean _int-version _int-init _int-query-action _int-query-arn _int-query-condition _int-write-policy

[group('docs')]
serve-docs:
    mkdocs serve --dev-addr "127.0.0.1:8001"

[group('test')]
type-check:
    ty check

[group('package')]
uninstall-package:
    uv pip uninstall policy_sentry

[group('test')]
unit-tests:
    coverage run -m pytest -v
    coverage report -m

[group('package')]
validate-sdist: && uninstall-package
    uv pip install dist/policy_sentry-*.tar.gz
    policy_sentry query service-table --fmt csv

[group('package')]
validate-wheel: && uninstall-package
    uv pip install dist/policy_sentry-*.whl
    policy_sentry query service-table --fmt csv
