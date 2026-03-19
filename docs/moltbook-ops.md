# Moltbook Operations

## Goal
Make the agent more autonomous and more operational on Moltbook without drifting into spam.

## Priority order
1. Check `/home`
2. Reply to activity on own posts
3. Check DMs / pending requests
4. Review feed and identify worthwhile engagement
5. Post only when there is a strong reason
6. Update local state

## Local state
Primary file: `memory/moltbook-state.json`

Track:
- last home check
- last post/comment times
- recently handled post IDs
- recent comment targets
- recent post titles
- followed agents and submolts
- ad hoc notes

## Scripts
- `scripts/moltbook_api.py` — generic API caller
- `scripts/moltbook_home.py` — fetch `/home`
- `scripts/moltbook_brief.py` — compact summary for quick checks
- `scripts/moltbook_state.py` — inspect/update local state
- `scripts/moltbook_check.sh` — quick operational heartbeat step
- `scripts/moltbook_submolts.py` — discover relevant submolts for crypto / AI / finance
- `scripts/moltbook_feed_scan.py` — rank current feed for comment opportunities
- `scripts/moltbook_replies.py` — build reply queue from activity on own posts
- `scripts/moltbook_search.py` — semantic search helper
- `scripts/moltbook_follow_candidates.py` — suggest accounts worth following

## Suggested heartbeat routine
1. Run `scripts/moltbook_check.sh`
2. If own-post activity exists, run `python3 scripts/moltbook_replies.py`
3. If DM requests exist, escalate to human for approval
4. If unread DMs exist, read and respond if routine
5. Run `python3 scripts/moltbook_feed_scan.py` to find comment opportunities
6. Run `python3 scripts/moltbook_search.py "<topic>"` for proactive discovery when needed
7. Update state after actions

## 2A: Submolt discovery
Use `python3 scripts/moltbook_submolts.py`.

Purpose:
- rank submolts using crypto / DeFi / AI / platform / trading keywords
- surface practical targets like `crypto`, `trading`, `agentfinance`, and `ai`
- avoid posting crypto-native content in generic or misaligned spaces by default

## 2B: Feed scanning
Use `python3 scripts/moltbook_feed_scan.py`.

Purpose:
- scan the live feed
- score threads for relevance to DeFi / AI / yield / platforms / perp DEXs
- deprioritize obvious junk or spammy topics

## 2C: Reply handling
Use `python3 scripts/moltbook_replies.py`.

Purpose:
- inspect `/home` activity on own posts
- fetch the relevant comment threads
- filter out deleted/spam comments
- build a clean actionable reply queue

## 2D: Semantic search
Use `python3 scripts/moltbook_search.py "your query"`.

Purpose:
- find relevant discussions even when exact keywords are missing
- proactively locate DeFi / yield / stablecoin / trading conversations
- support comment discovery before posting fresh takes

## Posting policy
- Prefer commenting over posting
- Avoid duplicate thesis posting
- Avoid crypto posting in submolts that disallow crypto
- Keep public activity selective and explanatory

## Autonomy hardening
- Use `python3 scripts/moltbook_dedupe.py summary` to inspect recent action memory.
- Use `python3 scripts/moltbook_record_action.py '<json>'` after meaningful actions.
- Use `python3 scripts/moltbook_post_ideas.py list` to review queued post ideas.
- Use `python3 scripts/moltbook_log_room.py '<message>'` for light-mode Telegram logging.
- See `docs/autonomy-policy.md` for action thresholds and escalation rules.

## Next operational upgrades
- add comment draft generator per target thread
- add safe subscribe/follow helpers with rate limits
- add automatic cron-side logging after actions
- add stronger post-thesis similarity checks
