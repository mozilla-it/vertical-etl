#!/bin/bash -l

export PATH=/usr/local/bin:$PATH

NUBIS_PROJECT=$(nubis-metadata NUBIS_PROJECT)

declare FX_Sentiments_GOOGLE_APPLICATION_CREDENTIALS FX_Sentiments_db_host FX_Sentiments_db FX_Sentiments_pwd

# shellcheck disable=SC1090
. "/etc/nubis-config/${NUBIS_PROJECT}.sh"

set -e

echo $FX_Sentiments_GOOGLE_APPLICATION_CREDENTIALS | base64 -d > ~/.google.fx-sentiment.json

export GOOGLE_APPLICATION_CREDENTIALS=~/.google.fx-sentiment.json

echo $GOOGLE_APPLICATION_CREDENTIALS

export TEST_FX_SENTIMENTS_HOST=$FX_Sentiments_db_host

echo $TEST_FX_SENTIMENTS_HOST

BASEDIR=$(dirname $0)

cd $BASEDIR && /usr/local/virtualenvs/fx-sentiment/bin/python data_processing.py --u dbadmin --host $FX_Sentiments_db_host -db $FX_Sentiments_db -p $FX_Sentiments_pwd

