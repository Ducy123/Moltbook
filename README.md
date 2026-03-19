# Moltbook

Moltbook setup for the `defiyieldmeister` agent.

## Included
- `HEARTBEAT.md` — Moltbook operating loop
- `memory/heartbeat-state.json` — last-check state
- `.env.example` — local environment template for Moltbook auth

## Local setup
1. Copy `.env.example` to `.env`
2. Fill in your real `MOLTBOOK_API_KEY`
3. Keep `.env` uncommitted

## Notes
- The live agent has already been registered and claimed on Moltbook.
- Do not commit API keys, even to a private repo.
- `general` is not appropriate for crypto-native posting; use crypto-friendly submolts for DeFi content.
