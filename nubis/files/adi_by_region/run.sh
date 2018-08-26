#!/bin/bash -l

set -e

/opt/etl/adi_by_region/fetch

/opt/etl/adi_by_region/load
