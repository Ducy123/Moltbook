#!/usr/bin/env python3
import json, os, sys, urllib.request, urllib.parse

BASE = os.environ.get('MOLTBOOK_API_BASE', 'https://www.moltbook.com/api/v1').rstrip('/')
API_KEY = os.environ.get('MOLTBOOK_API_KEY', '')


def load_env_file(path='.env'):
    if not os.path.exists(path):
        return
    with open(path, 'r', encoding='utf-8') as f:
        for raw in f:
            line = raw.strip()
            if not line or line.startswith('#') or '=' not in line:
                continue
            k, v = line.split('=', 1)
            os.environ.setdefault(k.strip(), v.strip())


def request(method, path, data=None, query=None):
    api_key = os.environ.get('MOLTBOOK_API_KEY', API_KEY)
    if not api_key:
        raise SystemExit('Missing MOLTBOOK_API_KEY')
    url = BASE + path
    if query:
        url += '?' + urllib.parse.urlencode(query)
    body = None
    headers = {'Authorization': f'Bearer {api_key}'}
    if data is not None:
        body = json.dumps(data).encode()
        headers['Content-Type'] = 'application/json'
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    with urllib.request.urlopen(req, timeout=30) as resp:
        text = resp.read().decode()
    try:
        return json.loads(text)
    except Exception:
        return {'raw': text}


def main(argv):
    load_env_file()
    if len(argv) < 2:
        raise SystemExit('Usage: moltbook_api.py METHOD PATH [JSON_BODY] [QUERY_JSON]')
    method = argv[0].upper()
    path = argv[1]
    data = json.loads(argv[2]) if len(argv) > 2 and argv[2] else None
    query = json.loads(argv[3]) if len(argv) > 3 and argv[3] else None
    result = request(method, path, data=data, query=query)
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main(sys.argv[1:])
