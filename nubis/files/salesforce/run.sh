#!/bin/bash -l

export PATH=/usr/local/bin:$PATH

# Import from salesforce
/opt/etl/salesforce/fetch

# Load into Vertica
/opt/etl/salesforce/load

# Populate the summary table
/opt/etl/salesforce/sfdc_populate_sf_summary_table.py
