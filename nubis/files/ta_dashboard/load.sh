#!/bin/bash -l

/usr/local/bin/vertica-csv-loader --start-date `date --date="1 day ago" +%Y-%m-%d` /opt/etl/ta_dashboard/load.yml
