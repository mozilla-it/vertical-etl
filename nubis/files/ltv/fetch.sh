#!/bin/bash -l

set -e

export PATH=/usr/local/bin:$PATH

NUBIS_PROJECT=$(nubis-metadata NUBIS_PROJECT)

declare LTV_Bucket LTV_AccessKey LTV_SecretKey LTV_SampleId

# shellcheck disable=SC1090
. "/etc/nubis-config/${NUBIS_PROJECT}.sh"

# process current dates in file (data in file should be up to previous date)
PROCESS_DATE=$(date +%Y%m%d) #YYYYMMDD

APP_DIR=/var/lib/etl/ltv # log directory to put files

export AWS_ACCESS_KEY_ID=${LTV_AccessKey:?}
export AWS_SECRET_ACCESS_KEY=${LTV_SecretKey:?}

echo "s3://${LTV_Bucket:?}/nawong/cdv6s${LTV_SampleId:?}_"$PROCESS_DATE
echo "$APP_DIR/client_details"
echo "s3://${LTV_Bucket:?}/nawong/scdv4s${LTV_SampleId:?}_"$PROCESS_DATE

aws s3 sync "s3://${LTV_Bucket:?}/nawong/cdv6s${LTV_SampleId:?}_"$PROCESS_DATE "$APP_DIR/client_details" --delete
aws s3 sync "s3://${LTV_Bucket:?}/nawong/scdv4s${LTV_SampleId:?}_hist_"$PROCESS_DATE "$APP_DIR/scd" --delete
