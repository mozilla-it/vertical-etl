#!/bin/bash -l

set -e

export PATH=/usr/local/bin:$PATH

NUBIS_PROJECT=$(nubis-metadata NUBIS_PROJECT)

declare ADI_Bucket ADI_AccessKey ADI_SecretKey

# shellcheck disable=SC1090
. "/etc/nubis-config/${NUBIS_PROJECT}.sh"

# default is to process for the previous month of data
PROCESS_YEAR=$(date --date="7 day ago" +%Y)
PROCESS_MONTH=$(date --date="7 day ago" +%m)

FOLDER="adi_by_region/year=$PROCESS_YEAR/month=$PROCESS_MONTH/"

APP_DIR=/var/lib/etl/$FOLDER # log directory to put files

export AWS_ACCESS_KEY_ID=${ADI_AccessKey:?}
export AWS_SECRET_ACCESS_KEY=${ADI_SecretKey:?}

# download the objects from $BUCKET/$PROCESS_DATE into $APP_DIR/$PROCESS_DATE
#aws s3 ls "s3://$ADI_Bucket/$FOLDER"
aws s3 cp --recursive "s3://$ADI_Bucket/$FOLDER" "$APP_DIR"

# delete output file if exists
[ -e "$APP_DIR"/output ] && rm "$APP_DIR"/output

# remove header from file(s) and concatenate to output
for file in "$APP_DIR"/*.csv
do
        sed -e'1d' "$file" >> "$APP_DIR"/output 
done
