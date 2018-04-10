#!/bin/bash

# get most recent file from s3 bucket
set -e
export PATH=/usr/local/bin:$PATH

NUBIS_PROJECT=$(nubis-metadata NUBIS_PROJECT)

declare Pocket_AWSFolder Pocket_Bucket Pocket_AccessKey Pocket_SecretKey

# shellcheck disable=SC1090
. "/etc/nubis-config/${NUBIS_PROJECT}.sh"

export AWS_ACCESS_KEY_ID=${Pocket_AccessKey:?}
export AWS_SECRET_ACCESS_KEY=${Pocket_SecretKey:?}

BUCKET=${Pocket_Bucket:pocket-mozilla-shared-analytics}
FOLDER=${Pocket_AWSFolder:pocket-mobile-active-counts}

OBJECT="$(aws s3 ls s3://$BUCKET/$FOLDER/ | grep mobile_active_counts_* | sort | tail -n 1 | awk '{print $4}')"

echo $OBJECT

APP_DIR=/var/lib/etl/pocket

rm -f $APP_DIR/mobile_active_counts_*

aws s3 cp "s3://$BUCKET/$FOLDER/$OBJECT" "$APP_DIR/"

# change permissions so metrics-etl can read over NFS
chmod -R 0777 $APP_DIR/$OBJECT
gunzip $APP_DIR/$OBJECT
