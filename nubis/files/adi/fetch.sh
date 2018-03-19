#!/bin/bash -l

set -e

export PATH=/usr/local/bin:$PATH

NUBIS_PROJECT=$(nubis-metadata NUBIS_PROJECT)

declare ADI_Folder ADI_Bucket ADI_AccessKey ADI_SecretKey

# shellcheck disable=SC1090
. "/etc/nubis-config/${NUBIS_PROJECT}.sh"

# default is to process for the previous days data
PROCESS_DATE=$(date --date="1 day ago" +%Y-%m-%d) # YYYY-MM-DD

APP_DIR=/var/lib/etl/adi # log directory to put files
FOLDER=${ADI_Folder:blpadi}

export AWS_ACCESS_KEY_ID=${ADI_AccessKey:?}
export AWS_SECRET_ACCESS_KEY=${ADI_SecretKey:?}

# Allow option to process for previous date.
# No error checking or validation here, the assumption is the argument is a single date in the YYY-MM-DD format
[ $# -ge 1 ] && PROCESS_DATE="$1"

# download the objects from $BUCKET/$PROCESS_DATE into $APP_DIR/$PROCESS_DATE
aws s3 cp --recursive "s3://$ADI_Bucket/$FOLDER/$PROCESS_DATE/" "$APP_DIR/$PROCESS_DATE/"

# concatenate files into one to match with current blp_adi script
# for file in /data/logs/adi_s3/2018-01-01/*; do cat $file >> /data/logs/adi_s3/2018-01-01/output && rm $file; done
cat "$APP_DIR/$PROCESS_DATE/"* > "$APP_DIR/$PROCESS_DATE/.output"
rm "$APP_DIR/$PROCESS_DATE/"*
mv "$APP_DIR/$PROCESS_DATE/.output" "$APP_DIR/$PROCESS_DATE/output"
