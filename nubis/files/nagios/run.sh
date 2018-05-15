#!/bin/bash -l

set -e

/opt/etl/nagios/fetch

/opt/etl/nagios/load
