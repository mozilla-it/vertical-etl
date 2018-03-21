#!/bin/bash
export PATH=/usr/local/bin:$PATH

NUBIS_PROJECT=$(nubis-metadata NUBIS_PROJECT)

declare Search_Bucket Search_BucketPath Search_AccessKey Search_SecretKey

# shellcheck disable=SC1090
. "/etc/nubis-config/${NUBIS_PROJECT}.sh"

# Check arguments for daily or monthly run or for a specific date to process for
SCOPE="daily" # daily or monthly
DEFINED_DATE="false"
PRE_DATE=$(date +%Y-%m-%d) # default is to process for current date

while [[ $# -gt 1 ]]
do
    arg="$1"

    case $arg in
    -s|--scope)
    SCOPE="$2"
    shift # past argument
    ;;
    -d|--date)
    PRE_DATE="$2"
    DEFINED_DATE="true"
    shift # past argument
    ;;
    *)

    ;;
esac
shift
done

set -e

export AWS_SECRET_ACCESS_KEY=$Search_SecretKey
export AWS_ACCESS_KEY_ID=$Search_AccessKey

BUCKET="s3://$Search_Bucket/$Search_BucketPath"

LOCAL_FILES_DIR=/var/lib/etl/search/work/$SCOPE

XFER_FILE_DIR=/var/lib/etl/search/$SCOPE

#
# Create $LOCAL_FILES_DIR
if [ ! -d "$LOCAL_FILES_DIR" ]; then
        mkdir -p "$LOCAL_FILES_DIR"
fi

# Begin
echo "[${PRE_DATE}]"

FETCH_DATE=$PRE_DATE

if [ "$SCOPE" == "monthly" ]; then
        FRMT_DATE=$(date --date="${PRE_DATE}" +%Y-%m-01)
        if [ "$DEFINED_DATE" == "true" ]; then
                FETCH_DATE=$FRMT_DATE
        else
                PREV_DATE=$(date --date="${PRE_DATE} 1 month ago" +%Y-%m-01)
                FETCH_DATE=$PREV_DATE
        fi
fi

# Create XFER_FILE_DIR
if [ ! -d "$XFER_FILE_DIR" ]; then
        mkdir -p "$XFER_FILE_DIR"
fi

ROLLUP="$BUCKET/$SCOPE/processed-$FETCH_DATE.csv"

echo "(downloading) $ROLLUP"
# copy objects into $LOCAL_FILES_DIR
echo "(executing) aws s3 cp $ROLLUP $LOCAL_FILES_DIR/"
aws s3 cp "$ROLLUP" "$LOCAL_FILES_DIR/"

for ROLLUP_FILE in $LOCAL_FILES_DIR/*.csv
do
        echo "(scrubbing) $LOCAL_FILES_DIR/$ROLLUP_FILE"
        # replace field ending ',' character with '|' character
        sed -i 's/,/|/g' "$ROLLUP_FILE"
        # remove CTRL-M from end of line
        sed -i 's/\r//g' "$ROLLUP_FILE"
        # gzip file
        gzip "$ROLLUP_FILE"
        # move to XFER_FILE_DIR
        mv "$ROLLUP_FILE.gz" "$XFER_FILE_DIR/"
done
