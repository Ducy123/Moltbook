#!/usr/bin/env sh
set -eu
cd "$(dirname "$0")/.."
python3 scripts/moltbook_brief.py
python3 scripts/moltbook_state.py touch lastHomeCheck >/dev/null
python3 scripts/moltbook_state.py touch lastMoltbookCheck >/dev/null || true
