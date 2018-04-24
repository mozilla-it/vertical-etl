#!/bin/bash

FETCH_DATE=$(date +%Y-%m-%d) # default is to process for current date

APP_DIR=search-cohort-churn/

XFER_FILE_DIR=/var/lib/etl/chur/latest/work
set -e

for file in $XFER_FILE_DIR/*.csv.gz
do
	echo $file
	# pass file to python script to load
	python ~/load -f $file -d $FETCH_DATE
done
