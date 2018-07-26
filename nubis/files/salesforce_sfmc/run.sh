#!/bin/bash -l

export PATH=/usr/local/bin:$PATH

# Import from salesforce
/opt/etl/salesforce_sfmc/fetch

# Load into Vertica
/opt/etl/salesforce_sfmc/load
