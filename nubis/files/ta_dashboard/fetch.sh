#!/bin/bash -l

/usr/local/bin/peopleteam-dashboard-fetcher --output-dir /var/lib/etl/ta_dashboard/ --ta-dashboard --date `date +%Y-%m-%d`
