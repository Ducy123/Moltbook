#!/usr/bin/env python3
import json, sys
from moltbook_api import load_env_file, request

load_env_file()
query = ' '.join(sys.argv[1:]).strip() or 'DeFi yield stablecoin platform perp DEX AI'
res = request('GET', '/search', query={'q': query, 'type': 'all', 'limit': 20})
results = []
for r in res.get('results', []):
    results.append({
        'id': r.get('id'),
        'type': r.get('type'),
        'title': r.get('title'),
        'author': (r.get('author') or {}).get('name'),
        'submolt': (r.get('submolt') or {}).get('name') if isinstance(r.get('submolt'), dict) else None,
        'similarity': r.get('similarity', r.get('relevance')),
        'post_id': r.get('post_id'),
        'url': r.get('url'),
    })
print(json.dumps({'query': query, 'results': results}, indent=2, ensure_ascii=False))
