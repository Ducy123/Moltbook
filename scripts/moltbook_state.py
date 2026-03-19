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


def main(argv):
    state = load_state()
    if not argv:
        print(json.dumps(state, indent=2, ensure_ascii=False))
        return
    cmd = argv[0]
    if cmd == 'touch':
        key = argv[1]
        state[key] = datetime.datetime.utcnow().replace(microsecond=0).isoformat() + 'Z'
    elif cmd == 'set-json':
        key = argv[1]
        state[key] = json.loads(argv[2])
    elif cmd == 'append-unique':
        key = argv[1]
        value = argv[2]
        state.setdefault(key, [])
        if value not in state[key]:
            state[key].append(value)
    else:
        raise SystemExit('Commands: touch <key> | set-json <key> <json> | append-unique <key> <value>')
    save_state(state)
    print(json.dumps(state, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main(sys.argv[1:])
