#!/usr/bin/env python3
import json, os, sys, urllib.request

TARGET = os.environ.get('MOLTBOOK_LOG_ROOM_TARGET', 'telegram:-4963416569')
TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN', '')


def load_env(path='.env'):
    if not os.path.exists(path):
        return
    with open(path, 'r', encoding='utf-8') as f:
        for raw in f:
            line = raw.strip()
            if not line or line.startswith('#') or '=' not in line:
                continue
            k, v = line.split('=', 1)
            os.environ.setdefault(k.strip(), v.strip())


load_env()
TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN', TOKEN)
if not TOKEN:
    raise SystemExit('Missing TELEGRAM_BOT_TOKEN')
message = ' '.join(sys.argv[1:]).strip()
if not message:
    raise SystemExit('Usage: moltbook_log_room.py <message>')
chat_id = TARGET.split(':', 1)[1] if TARGET.startswith('telegram:') else TARGET
url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
payload = json.dumps({'chat_id': chat_id, 'text': message}).encode()
req = urllib.request.Request(url, data=payload, headers={'Content-Type': 'application/json'}, method='POST')
with urllib.request.urlopen(req, timeout=30) as r:
    print(r.read().decode())
