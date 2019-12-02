#!/usr/bin/env bash

echo "Please run this from the main file of the directory."

# wget's '-N' flag is helping us here.
# According to the description: don't re-retrieve files unless newer than local.

wget -r --no-parent --convert-links --server-response --accept 'list_*.html' --reject 'feedbackno.html','feedbackyes.html' --no-clobber https://docs.aws.amazon.com/IAM/latest/UserGuide/introduction.html --no-host-directories --cut-dirs=3 --directory-prefix policy_sentry/shared/data/docs

# Remove a random straggler file
rm policy_sentry/shared/data/docs/robots.txt.tmp
#while read LINE; do
#    wget ${LINE} --convert-file-only -P policy_sentry/shared/data/docs -S  -nv --timestamping
#done < $FILE

# Adjusting
# wget -r -np -k --accept 'list_*.html' --reject 'feedbackno.html','feedbackyes.html' -nc https://docs.aws.amazon.com/IAM/latest/UserGuide/introduction.html --no-host-directories --cut-dirs=3 -P policy_sentry/shared/data/docs
