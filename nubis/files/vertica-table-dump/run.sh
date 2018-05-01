#!/bin/bash -l

export PATH=/usr/local/bin:/opt/vertica/bin:$PATH

TMPDIR=/tmp/s3_dumps/

NUBIS_ENVIRONMENT=$(nubis-metadata NUBIS_ENVIRONMENT)
NUBIS_PROJECT=$(nubis-metadata NUBIS_PROJECT)

KV_PREFIX="$NUBIS_PROJECT-$NUBIS_ENVIRONMENT/$NUBIS_ENVIRONMENT/config"

BACKUP_BUCKET_NAME=$(consul kv get "$KV_PREFIX/S3/Bucket/Backups")
DBADMIN_PASSWORD=$(consul kv get "vertical-stage/stage/config/AdminPassword")

if [ "$BACKUP_BUCKET_NAME" == "" ]; then
  echo "Need to set Backup Bucket name key in consul://$KV_PREFIX/S3/Bucket/Backups"
  exit 1
fi

mkdir -p $TMPDIR

for table in `vsql -U dbadmin -w $DBADMIN_PASSWORD -h stage.vertical.service.consul -c "select table_name from all_tables where schema_name='public';" -t`;
do
  TIMESTAMP=`date +%Y%m%d%H%M`;
  OUTFILE=${table}_dump_${TIMESTAMP}.sql.gz
  vsql -U dbadmin -w $DBADMIN_PASSWORD -h stage.vertical.service.consul -At -c "select * from $table" | gzip > ${TMPDIR}${OUTFILE}
  aws s3 cp ${TMPDIR}${OUTFILE} s3://${BACKUP_BUCKET_NAME}/${OUTFILE} --quiet
  rm ${TMPDIR}${OUTFILE}
done

