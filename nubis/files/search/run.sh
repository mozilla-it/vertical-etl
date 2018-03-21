#!/bin/bash -l

set -e

/opt/etl/search/fetch "$@"
/opt/etl/search/load "$@"
