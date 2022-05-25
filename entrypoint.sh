#! /usr/bin/env bash

# Required environment variables
# API_KEY
# API_URL

if [[ -z "${API_KEY}" ]]; then
  echo "Environment variable API_KEY not exists!"
  exit 1
fi

if [[ -z "${API_URL}" ]]; then
  echo "Environment variable API_URL not exists!"
  exit 1
fi

python3 /app/src/main.py