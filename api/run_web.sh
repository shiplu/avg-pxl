#!/bin/bash

set -e

PORT=${1:-8000}

set -x
exec gunicorn \
    --workers 4 \
    --bind "0.0.0.0:${PORT}" \
    --limit-request-line 0 \
    --timeout 1000 \
    --keep-alive 75 \
    --worker-class gevent \
    web:app

