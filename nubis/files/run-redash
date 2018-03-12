#!/bin/bash -l

export PATH=/usr/local/bin:$PATH

QUERY_ID=$1
TABLE=$2

if [ "$QUERY_ID" == "" ] || [ "$TABLE" == "" ]; then
  echo "Invoke as $0 query-id table-name"
  exit 1
fi

NUBIS_ENVIRONMENT=$(nubis-metadata NUBIS_ENVIRONMENT)
NUBIS_PROJECT=$(nubis-metadata NUBIS_PROJECT)

KV_PREFIX="$NUBIS_PROJECT-$NUBIS_ENVIRONMENT/$NUBIS_ENVIRONMENT/config"

API_KEY=$(consul kv get "$KV_PREFIX/Redash/tables/$TABLE/api_key")

if [ "$API_KEY" == "" ]; then
  echo "Need to set API key in consul://$KV_PREFIX/Redash/tables/$TABLE/api_key"
  exit 1
fi

/usr/local/bin/data-collectors redash --query_id "$QUERY_ID" --api-key "$API_KEY" --table "$TABLE"
