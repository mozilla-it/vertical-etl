#!/bin/bash -l

export PATH=/usr/local/bin:$PATH

# Cleanup
find /var/salesforce-fetcher/ -name output.csv -mtime +1 -exec rm {} \;

# Import from salesforce
/opt/etl/salesforce/fetch

# Load into Vertica
/opt/etl/salesforce/load
