SHELL:=/bin/bash

PROJECT := policy-sentry
PROJECT_UNDERSCORE := policy_sentry

# ---------------------------------------------------------------------------------------------------------------------
# Environment setup and management
# ---------------------------------------------------------------------------------------------------------------------
virtualenv:
	python3 -m venv ./venv && source venv/bin/activate
setup-env: virtualenv
	python3 -m pip install -r requirements.txt
setup-dev: setup-env
	python3 -m pip install -r requirements-dev.txt
# ---------------------------------------------------------------------------------------------------------------------
# Documentation
# ---------------------------------------------------------------------------------------------------------------------
build-docs: clean virtualenv
	python3 -m pip install -r docs/requirements.txt
	mkdocs build --clean --site-dir _build/html --config-file mkdocs.yml
serve-docs: clean virtualenv
	python3 -m pip install -r docs/requirements.txt
	mkdocs serve --dev-addr "127.0.0.1:8001"
# ---------------------------------------------------------------------------------------------------------------------
# Installation etc.
# ---------------------------------------------------------------------------------------------------------------------
build: setup-env clean
	python3 -m pip install --upgrade setuptools wheel
	python3 -m setup -q sdist bdist_wheel
install: build
	python3 -m pip install -q ./dist/${PROJECT}*.tar.gz
	${PROJECT} --help
uninstall:
	python3 -m pip uninstall ${PROJECT} -y
	python3 -m pip uninstall -r requirements.txt -y
	python3 -m pip uninstall -r requirements-dev.txt -y
	python3 -m pip freeze | xargs python3 -m pip uninstall -y
clean:
	rm -rf dist/
	rm -rf build/
	rm -rf _build/
	rm -rf *.egg-info
	find . -name '*.pyc' -delete
	find . -name '*.pyo' -delete
	find . -name '*.egg-link' -delete
	find . -name '*.pyc' -exec rm --force {} +
	find . -name '*.pyo' -exec rm --force {} +
# ---------------------------------------------------------------------------------------------------------------------
# Testing
# ---------------------------------------------------------------------------------------------------------------------
test: setup-dev
	python3 -m coverage run -m pytest -v
# ---------------------------------------------------------------------------------------------------------------------
# Package publishing
# ---------------------------------------------------------------------------------------------------------------------
publish: build
	python3 -m pip install --upgrade twine
	python3 -m twine upload dist/*
	python3 -m pip install ${PROJECT}
# ---------------------------------------------------------------------------------------------------------------------
# Miscellaneous
# ---------------------------------------------------------------------------------------------------------------------
count-loc:
	echo "If you don't have tokei installed, you can install it with 'brew install tokei'"
	echo "Website: https://github.com/XAMPPRocky/tokei#installation'"
	tokei ./* --exclude --exclude '**/*.html' --exclude '**/*.json' --exclude "docs/*" --exclude "examples/*" --exclude "test/*"

# ---------------------------------------------------------------------------------------------------------------------
# Project specific scripts
# ---------------------------------------------------------------------------------------------------------------------
update-iam-data: setup-dev
	python3 ./utils/download_docs.py
