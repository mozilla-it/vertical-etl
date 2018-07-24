#!/bin/bash -l

export PATH=/usr/local/bin:$PATH

# Import from salesforce
/opt/etl/snippets_stats/fetch

# Load into Vertica
/opt/etl/snippets_stats/load
