#!/bin/bash -l

export PATH=/usr/local/bin:$PATH

# Import from salesforce
/opt/etl/salesforce_sfmc/fetch

# Load into Vertica
/opt/etl/salesforce_sfmc/load

# Populate the unique jobs table
/opt/etl/salesforce_sfmc/populate_sfmc_send_jobs_unique_table.py
