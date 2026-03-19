#!/usr/bin/env python3
import json, re
from moltbook_api import load_env_file, request

KEYWORDS = {
    'defi': ['defi', 'lending', 'borrow', 'yield', 'stablecoin', 'credit', 'tokenized'],
    'ai': ['ai', 'agent', 'model', 'automation'],
    'perp': ['perp', 'perpetual', 'dex', 'liquidation', 'funding'],
    'platform': ['platform', 'ecosystem', 'infrastructure', 'integration'],
}

BAD_PATTERNS = ['tiktok', 'aged accounts', 'seo', 'casino', 'betting', 'nsfw']


def text_score(text):
    text = (text or '').lower()
    score = 0
    reasons = []
    for bucket, words in KEYWORDS.items():
        hits = [w for w in words if w in text]
        if hits:
            score += len(hits) * 2
            reasons.append(f"{bucket}:{','.join(hits[:3])}")
    for bad in BAD_PATTERNS:
        if bad in text:
            score -= 5
            reasons.append(f"avoid:{bad}")
    return score, reasons


load_env_file()
feed = request('GET', '/feed', query={'sort': 'new', 'limit': 25})
posts = feed.get('posts', [])
ranked = []
for p in posts:
    merged = ' '.join([p.get('title', ''), p.get('content', ''), p.get('submolt_name', '')])
    score, reasons = text_score(merged)
    if p.get('comment_count', 0) > 0:
        score += 1
        reasons.append('active-thread')
    if p.get('upvotes', 0) > 2:
        score += 1
        reasons.append('some-traction')
    if score > 0:
        ranked.append({
            'id': p.get('id'),
            'title': p.get('title'),
            'author': (p.get('author') or {}).get('name'),
            'submolt_name': p.get('submolt_name'),
            'comment_count': p.get('comment_count'),
            'upvotes': p.get('upvotes'),
            'score': score,
            'reasons': reasons,
        })
ranked.sort(key=lambda x: (-x['score'], -(x.get('comment_count') or 0), -(x.get('upvotes') or 0)))
print(json.dumps({'comment_opportunities': ranked[:15]}, indent=2, ensure_ascii=False))
