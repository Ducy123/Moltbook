#!/usr/bin/env python3
import json
from moltbook_api import load_env_file, request

load_env_file()
feed = request('GET', '/feed', query={'sort': 'top', 'limit': 25})
seen = {}
for p in feed.get('posts', []):
    author = (p.get('author') or {}).get('name')
    if not author or p.get('you_follow_author'):
        continue
    row = seen.setdefault(author, {
        'author': author,
        'posts_seen': 0,
        'total_upvotes_seen': 0,
        'submolts': set(),
    })
    row['posts_seen'] += 1
    row['total_upvotes_seen'] += p.get('upvotes', 0)
    if p.get('submolt_name'):
        row['submolts'].add(p.get('submolt_name'))
rows = []
for v in seen.values():
    rows.append({
        'author': v['author'],
        'posts_seen': v['posts_seen'],
        'total_upvotes_seen': v['total_upvotes_seen'],
        'submolts': sorted(v['submolts']),
    })
rows.sort(key=lambda x: (-x['posts_seen'], -x['total_upvotes_seen']))
print(json.dumps({'follow_candidates': rows[:15]}, indent=2, ensure_ascii=False))
