#!/bin/bash -l

/usr/local/bin/peopleteam-dashboard-fetcher --output-dir /var/lib/etl/peopleteam_dashboard_monthly/ --monthly --date `date --date="1 day ago" +%Y-%m-%d` --force
