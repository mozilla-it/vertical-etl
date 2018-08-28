#!/bin/bash -l

set -e

export PATH=/usr/local/bin:$PATH

NUBIS_PROJECT=$(nubis-metadata NUBIS_PROJECT)

declare LTV_GOOGLE_APPLICATION_CREDENTIALS

# shellcheck disable=SC1090
. "/etc/nubis-config/${NUBIS_PROJECT}.sh"

# process current dates in file (data in file should be up to previous date)
PROCESS_DATE=$(date +%Y%m%d) #YYYYMMDD

APP_DIR=/var/lib/etl/ltv # log directory to put files

export GOOGLE_APPLICATION_CREDENTIALS=${LTV_GCP_Credentials:?}

# placeholder for GCP automation
# push ltv and aggr file to GCP                    

echo $LTV_GOOGLE_APPLICATION_CREDENTIALS > tmp.txt
base64 -d tmp.txt > tmp2.txt
#export GOOGLE_APPLICATION_CREDENTIALS=tmp2.txt

# activate service account credentials
gcloud auth activate-service-account --key-file ga-mozilla-org-prod-001-cfcfa1a3d0ee.json

gsutil -o GSUtil::parallel_composite_upload_threshold=150M cp ltv_output_v1_$PROCESS_DATE gs://ga-mozilla-org-prod-001/ltv_v1
gsutil -o GSUtil::parallel_composite_upload_threshold=150M cp ltv_aggr_v1_$PROCESS_DATE gs://ga-mozilla-org-prod-001/ltv_v1
