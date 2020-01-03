#!/bin/bash
# Usage within the container:
# args="query action-table --service all --access-level permissions-management"
# /usr/bin/entrypoint.sh "$args"

die() {
    echo "$@"
    exit
}

arguments=$1

[ -z "$arguments" ] && die "Missing arguments for policy_sentry.  Usage: $0 <arguments>";

/usr/local/bin/policy_sentry $1
