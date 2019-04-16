#!/bin/bash -l

export PATH=/usr/local/bin:$PATH

# Import from Workday
/opt/etl/ta_dashboard/fetch

# Load into Vertica
/opt/etl/ta_dashboard/load
