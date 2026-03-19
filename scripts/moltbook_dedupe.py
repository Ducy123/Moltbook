#!/usr/bin/env python3
import json, os, sys, datetime

STATE_PATH = os.environ.get('MOLTBOOK_STATE_PATH', 'memory/moltbook-state.json')
NOW = datetime.datetime.utcnow()


def load_state():
    if not os.path.exists(STATE_PATH):
        return {}
    with open(STATE_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)


def parse_ts(value):
    if not value:
        return None
    try:
        return datetime.datetime.fromisoformat(value.replace('Z', '+00:00')).replace(tzinfo=None)
    except Exception:
        return None


def recent(items, hours=72):
    cutoff = NOW - datetime.timedelta(hours=hours)
    out = []
    for item in items or []:
        ts = parse_ts(item.get('at'))
        if ts and ts >= cutoff:
            out.append(item)
    return out


state = load_state()
actions = recent(state.get('recentActions', []), hours=168)
mode = sys.argv[1] if len(sys.argv) > 1 else 'summary'
value = sys.argv[2] if len(sys.argv) > 2 else ''

if mode == 'summary':
    print(json.dumps({'recentActions': actions}, indent=2, ensure_ascii=False))
elif mode == 'commented-post':
    print('true' if any(a.get('kind') == 'comment' and a.get('postId') == value for a in actions) else 'false')
elif mode == 'replied-comment':
    print('true' if any(a.get('kind') == 'reply' and a.get('commentId') == value for a in actions) else 'false')
elif mode == 'used-title':
    titles = [a.get('title','').strip().lower() for a in actions if a.get('kind') == 'post']
    print('true' if value.strip().lower() in titles else 'false')
else:
    raise SystemExit('Modes: summary | commented-post <postId> | replied-comment <commentId> | used-title <title>')
