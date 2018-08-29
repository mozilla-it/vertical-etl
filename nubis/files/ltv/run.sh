#!/bin/bash -l

# Look at our virtualenv first
export PATH=/usr/local/virtualenvs/ltv/bin:$PATH

set -e

#/opt/etl/ltv/fetch

#/opt/etl/ltv/load_client_details

#/opt/etl/ltv/load_search_history

/opt/etl/ltv/test_ltv_calc_v1
#/opt/etl/ltv/ltv_calc_v1

#/opt/etl/ltv/ltv_aggr_v1

#/opt/etl/ltv/push_to_gcp
