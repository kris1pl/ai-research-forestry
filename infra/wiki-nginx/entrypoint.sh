#!/bin/bash
set -eu

HTML="/usr/share/nginx/html"
mkdir -p "$HTML"

if [ -n "${GCS_BUCKET:-}" ]; then
  echo "Syncing gs://${GCS_BUCKET} -> ${HTML}"
  gcloud storage rsync -r "gs://${GCS_BUCKET}" "$HTML" || {
    echo "WARN: GCS sync failed — serving empty or stale content"
  }
fi

exec nginx -g 'daemon off;'
