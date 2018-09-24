#!/bin/bash -l

export PATH=/usr/local/bin:/opt/vertica/bin:$PATH

TMPDIR=/var/lib/etl/vertica-table-dump

NUBIS_ENVIRONMENT=$(nubis-metadata NUBIS_ENVIRONMENT)
NUBIS_PROJECT=$(nubis-metadata NUBIS_PROJECT)

KV_PREFIX="$NUBIS_PROJECT-$NUBIS_ENVIRONMENT/$NUBIS_ENVIRONMENT/config"

BACKUP_BUCKET_NAME=$(consul kv get "$KV_PREFIX/S3/Bucket/Backups")
DBADMIN_PASSWORD=$(consul kv get "vertical-${NUBIS_ENVIRONMENT}/${NUBIS_ENVIRONMENT}/config/AdminPassword")
VERTICA_HOST="${NUBIS_ENVIRONMENT}.vertical.service.consul"

if [ -z "$BACKUP_BUCKET_NAME" ]; then
  echo "Need to set Backup Bucket name key in consul://$KV_PREFIX/S3/Bucket/Backups"
  exit 1
fi

TIMESTAMP=$(date +%Y%m%d)
DUMP_DIR="$TMPDIR/$TIMESTAMP"

cleanup () {
 rm -rfv "$DUMP_DIR" 2>/dev/null
}
trap cleanup EXIT

mkdir -p "$DUMP_DIR"

# Dump tables
for table in $(vsql -U dbadmin -w "$DBADMIN_PASSWORD" -h "$VERTICA_HOST" -c "select table_name from all_tables where schema_name='public';" -t | sort);
do
  OUTFILE="${table}.sql.gz"
  vsql -U dbadmin -w "$DBADMIN_PASSWORD" -h "$VERTICA_HOST" -At -c "select * from $table" | gzip > "${DUMP_DIR}/${OUTFILE}"
  # Sync to S3
  aws s3 sync --quiet "$DUMP_DIR/${OUTFILE}" "s3://${BACKUP_BUCKET_NAME}/$TIMESTAMP/${OUTFILE}"
  # Cleanup
  rm "$OUTFILE"
done
