#!/bin/bash -l

/usr/local/bin/vertica-csv-loader --start-date `date +%Y-%m-%d` /opt/etl/ta_dashboard/load.yml
