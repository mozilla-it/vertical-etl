#!/bin/bash -l

/usr/local/bin/vertica-csv-loader /opt/etl/salesforce_sfmc/load.yml
/usr/local/bin/vertica-csv-loader /opt/etl/salesforce_sfmc/load_DESS.yml
