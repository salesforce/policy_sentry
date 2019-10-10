#!/usr/bin/env bash
# Just run this script to check if there are new links that need to be added.
# It will add a file titled scripts/links.txt and scripts/links.yml if necessary
# If there have been updates to the AWS IAM docs, it will make new HTML files in the shared/data/docs directory.
# This way, when we build the SQLite database, we are always using documentation that is owned by this directory
# and our automation won't break if the AWS website is down, or if they drastically change their documentation.
# After running this script, make sure to run ./policy_sentry.py create_all_tables

python3 ./utils/get_links.py
bash ./utils/download-docs.sh
