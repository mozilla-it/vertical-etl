#!/bin/bash -l

set -e

export PATH=/usr/local/bin:$PATH

NUBIS_PROJECT=$(nubis-metadata NUBIS_PROJECT)

declare LTV_GOOGLE_APPLICATION_CREDENTIALS LTV_SampleId

# shellcheck disable=SC1090
. "/etc/nubis-config/${NUBIS_PROJECT}.sh"

# process current dates in file (data in file should be up to previous date)
PROCESS_DATE=$(date +%Y%m%d) #YYYYMMDD

export CLOUDSDK_PYTHON=/bin/python2
export GOOGLE_APPLICATION_CREDENTIALS=${LTV_GOOGLE_APPLICATION_CREDENTIALS:?}

# push ltv and aggr file to GCP                    

echo $LTV_GOOGLE_APPLICATION_CREDENTIALS > tmp.txt
base64 -d tmp.txt > tmp2.txt

# activate service account credentials
gcloud auth activate-service-account --key-file tmp2.txt

# add sample id to filename
mv ltv_output_v1_$PROCESS_DATE.txt ltv_output_v1_sampleid${LTV_SampleId:?}_$PROCESS_DATE.txt
mv ltv_aggr_v1_$PROCESS_DATE.txt ltv_aggr_v1_sampleid${LTV_SampleId:?}_$PROCESS_DATE.txt

gsutil -o GSUtil::parallel_composite_upload_threshold=150M cp ltv_output_v1_sampleid${LTV_SampleId:?}_$PROCESS_DATE.txt gs://ga-mozilla-org-prod-001/ltv_v1
gsutil -o GSUtil::parallel_composite_upload_threshold=150M cp ltv_aggr_v1_sampleid${LTV_SampleId:?}_$PROCESS_DATE.txt gs://ga-mozilla-org-prod-001/ltv_v1
