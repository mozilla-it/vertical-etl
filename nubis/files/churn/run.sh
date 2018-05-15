#!/bin/bash -l

set -e

/opt/etl/churn/fetch "$@"
/opt/etl/churn/call_load "$@"
