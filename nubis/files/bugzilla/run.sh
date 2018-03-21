#!/bin/bash -l

set -e

echo "Fetching snapshot from ElasticSearch"
/opt/etl/bugzilla/fetch "$@"

echo "Updating derived table f_bug_status_resolution"
/opt/etl/bugzilla/f_bug_status_resolution "$@"
