#!/bin/bash -l

export PATH=/usr/local/bin:$PATH

# Import from salesforce
/opt/etl/snippets-stats/fetch

# Load into Vertica
/opt/etl/snippets-stats/load
