#!/usr/bin/env python3
import json, os, sys, datetime

STATE_PATH = os.environ.get('MOLTBOOK_STATE_PATH', 'memory/moltbook-state.json')


def load_state():
    if not os.path.exists(STATE_PATH):
        return {}
    with open(STATE_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_state(state):
    os.makedirs(os.path.dirname(STATE_PATH), exist_ok=True)
    with open(STATE_PATH, 'w', encoding='utf-8') as f:
        json.dump(state, f, indent=2, ensure_ascii=False)
        f.write('\n')


if len(sys.argv) < 2:
    raise SystemExit('Usage: moltbook_record_action.py <json>')
entry = json.loads(sys.argv[1])
entry.setdefault('at', datetime.datetime.utcnow().replace(microsecond=0).isoformat() + 'Z')
state = load_state()
state.setdefault('recentActions', [])
state['recentActions'] = (state['recentActions'] + [entry])[-200:]
save_state(state)
print(json.dumps(entry, indent=2, ensure_ascii=False))
