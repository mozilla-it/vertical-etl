#!/bin/bash

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

XFER_FILE_DIR=/var/lib/etl/search/$SCOPE/processed-$FETCH_DATE.csv.gz

set -e

"/opt/etl/search/load-$SCOPE" -f "$XFER_FILE_DIR"
