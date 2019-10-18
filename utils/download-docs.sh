#!/usr/bin/env bash
PWD=$(pwd)
FILE="$PWD/utils/links.txt"

# wget's '-N' flag is helping us here.
# According to the description: don't re-retrieve files unless newer than local.

while read LINE; do
    wget ${LINE} --convert-file-only -P policy_sentry/shared/data/docs -S  -nv --timestamping
done < $FILE

#wget https://docs.aws.amazon.com/IAM/latest/UserGuide/list_awsmarketplacemeteringservice.html --convert-file-only
