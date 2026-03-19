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


state = load_state()
state.setdefault('postIdeas', [])
cmd = sys.argv[1] if len(sys.argv) > 1 else 'list'

if cmd == 'list':
    print(json.dumps({'postIdeas': state['postIdeas']}, indent=2, ensure_ascii=False))
elif cmd == 'add':
    if len(sys.argv) < 5:
        raise SystemExit('Usage: add <submolt> <title> <thesis>')
    submolt, title, thesis = sys.argv[2], sys.argv[3], sys.argv[4]
    idea = {
        'submolt': submolt,
        'title': title,
        'thesis': thesis,
        'status': 'new',
        'createdAt': datetime.datetime.utcnow().replace(microsecond=0).isoformat() + 'Z'
    }
    state['postIdeas'].append(idea)
    save_state(state)
    print(json.dumps(idea, indent=2, ensure_ascii=False))
elif cmd == 'mark':
    if len(sys.argv) < 4:
        raise SystemExit('Usage: mark <title> <status>')
    title, status = sys.argv[2], sys.argv[3]
    for idea in state['postIdeas']:
        if idea.get('title') == title:
            idea['status'] = status
    save_state(state)
    print(json.dumps({'postIdeas': state['postIdeas']}, indent=2, ensure_ascii=False))
else:
    raise SystemExit('Commands: list | add <submolt> <title> <thesis> | mark <title> <status>')
