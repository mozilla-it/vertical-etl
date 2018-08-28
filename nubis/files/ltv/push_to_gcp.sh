#!/bin/bash -l

set -e

export PATH=/usr/local/bin:$PATH

NUBIS_PROJECT=$(nubis-metadata NUBIS_PROJECT)

declare LTV_GCP_Bucket LTV_GCP_Credentials

# shellcheck disable=SC1090
. "/etc/nubis-config/${NUBIS_PROJECT}.sh"

# process current dates in file (data in file should be up to previous date)
PROCESS_DATE=$(date +%Y%m%d) #YYYYMMDD

APP_DIR=/var/lib/etl/ltv # log directory to put files

export GOOGLE_APPLICATION_CREDENTIALS=${LTV_GCP_Credentials:?}

# placeholder for GCP automation
# push ltv and aggr file to GCP
# See Fx Sentiment for GCP example
