#!/bin/bash -l

set -e

export PATH=/usr/local/bin:$PATH

NUBIS_PROJECT=$(nubis-metadata NUBIS_PROJECT)

declare Nagios_Bucket Nagios_AccessKey Nagios_SecretKey

# shellcheck disable=SC1090
. "/etc/nubis-config/${NUBIS_PROJECT}.sh"

# default is to process for the previous days data
PROCESS_DATE=$(date --date="1 day ago" +%Y-%m-%d) # YYYY-MM-DD

APP_DIR=/var/lib/etl/nagios # log directory to put files

export AWS_ACCESS_KEY_ID=${Nagios_AccessKey:?}
export AWS_SECRET_ACCESS_KEY=${Nagios_SecretKey:?}

# Allow option to process for previous date.
# No error checking or validation here, the assumption is the argument is a single date in the YYY-MM-DD format
[ $# -ge 1 ] && PROCESS_DATE="$1"

# download the objects from $BUCKET/*$PROCESS_DATE.gz into $APP_DIR/
aws s3 cp --recursive "s3://$Nagios_Bucket/" "$APP_DIR/" --recursive --exclude "*" --include "*$PROCESS_DATE.gz"
