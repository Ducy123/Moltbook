#!/usr/bin/env sh
set -eu

if [ -f .env ]; then
  export $(grep -v '^#' .env | xargs)
fi

if [ -z "${MOLTBOOK_API_KEY:-}" ]; then
  echo "Missing MOLTBOOK_API_KEY"
  exit 1
fi

curl -s https://www.moltbook.com/api/v1/agents/status \
  -H "Authorization: Bearer $MOLTBOOK_API_KEY"

echo
