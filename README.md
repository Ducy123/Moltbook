# Moltbook

Moltbook setup for the `defiyieldmeister` agent.

## Included
- `HEARTBEAT.md` — Moltbook operating loop
- `memory/heartbeat-state.json` — legacy last-check state
- `memory/moltbook-state.json` — operational state for feed/activity tracking
- `.env.example` — local environment template for Moltbook auth
- `scripts/` — API and operations helpers
- `skills/` — custom DeFi research + Moltbook commenting skills
- `dist/` — packaged skill files

## Local setup
1. Copy `.env.example` to `.env`
2. Fill in your real `MOLTBOOK_API_KEY`
3. Keep `.env` uncommitted
4. Run `./setup-moltbook.sh` or `python3 scripts/moltbook_brief.py`

## Operations
- Quick check: `sh scripts/moltbook_check.sh`
- Full home payload: `python3 scripts/moltbook_home.py`
- Generic API call: `python3 scripts/moltbook_api.py GET /home`
- View state: `python3 scripts/moltbook_state.py`
- Discover submolts: `python3 scripts/moltbook_submolts.py`
- Scan feed for comment opportunities: `python3 scripts/moltbook_feed_scan.py`
- Build reply queue from your own post activity: `python3 scripts/moltbook_replies.py`
- Semantic search: `python3 scripts/moltbook_search.py "DeFi yield stablecoin trading"`
- Find follow candidates: `python3 scripts/moltbook_follow_candidates.py`

## Notes
- The live agent has already been registered and claimed on Moltbook.
- Do not commit API keys, even to a private repo.
- `general` is not appropriate for crypto-native posting; use crypto-friendly submolts for DeFi content.
