#!/bin/bash -l

export PATH=/usr/local/bin:$PATH

NUBIS_PROJECT=$(nubis-metadata NUBIS_PROJECT)

declare Churn_Bucket Churn_BucketPath Churn_AccessKey Churn_SecretKey

# shellcheck disable=SC1090
. "/etc/nubis-config/${NUBIS_PROJECT}.sh"

set -e

export AWS_SECRET_ACCESS_KEY=$Churn_SecretKey
export AWS_ACCESS_KEY_ID=$Churn_AccessKey

CURRENT_DATE=$(date +%Y-%m-%d)
BUCKET="s3://$Churn_Bucket/$Churn_BucketPath"

BASE_DIR=/var/lib/etl/churn

LOCAL_FILES_DIR=$BASE_DIR/work

XFER_FILE_DIR=$BASE_DIR/$CURRENT_DATE

#
# Create $LOCAL_FILES_DIR
if [ ! -d $LOCAL_FILES_DIR ]; then
        mkdir -p $LOCAL_FILES_DIR
fi

# Begin
echo "[${CURRENT_DATE}]"

# We need to get the last update date which should be one day prior to the retrieve date
MODIFIED_DATE=$(date --date="${CURRENT_DATE} 1 days ago" +%Y-%m-%d)

# Using the MODIFIED_DATE we need to get the object name to retrieve
OBJECT=$(aws s3 ls "$BUCKET/" | grep "^$MODIFIED_DATE" | awk '{print $4}')

echo $BUCKET/$OBJECT

# Create XFER_FILE_DIR
if [ ! -d "$XFER_FILE_DIR" ]; then
        mkdir -p "$XFER_FILE_DIR"
fi

# Pull down latest file
aws s3 sync "$BUCKET" "$LOCAL_FILES_DIR"

mv "$LOCAL_FILES_DIR/$OBJECT" "$XFER_FILE_DIR/"

ln -sfn "$CURRENT_DATE" "$BASE_DIR/latest"