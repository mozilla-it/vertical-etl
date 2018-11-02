#!/bin/bash -l

export PATH=/usr/local/bin:$PATH

# Import from Workday
/opt/etl/peopleteam_dashboard_monthly/fetch

# Load into Vertica
/opt/etl/peopleteam_dashboard_monthly/load
