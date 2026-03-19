#!/usr/bin/env python3
import json
from moltbook_api import load_env_file, request

PRIORITY_KEYWORDS = {
    'crypto': ['crypto', 'defi', 'yield', 'stablecoin', 'perp', 'trading', 'finance', 'market', 'alpha'],
    'ai': ['ai', 'agent', 'automation', 'model', 'tooling'],
}


def score_submolt(submolt):
    text = ' '.join([
        submolt.get('name', ''),
        submolt.get('display_name', ''),
        submolt.get('description', ''),
    ]).lower()
    score = 0
    reasons = []
    for bucket, words in PRIORITY_KEYWORDS.items():
        hits = [w for w in words if w in text]
        if hits:
            score += len(hits)
            reasons.append(f"{bucket}:{','.join(hits[:3])}")
    if submolt.get('subscriber_count', 0) > 500:
        score += 1
        reasons.append('active')
    if submolt.get('name') in {'crypto', 'trading', 'agentfinance', 'ai'}:
        score += 3
        reasons.append('priority-name')
    return score, reasons


load_env_file()
res = request('GET', '/submolts')
submolts = res.get('submolts', [])
ranked = []
for s in submolts:
    score, reasons = score_submolt(s)
    if score > 0:
        ranked.append({
            'name': s.get('name'),
            'display_name': s.get('display_name'),
            'description': s.get('description'),
            'subscriber_count': s.get('subscriber_count'),
            'post_count': s.get('post_count'),
            'score': score,
            'reasons': reasons,
        })
ranked.sort(key=lambda x: (-x['score'], -(x.get('subscriber_count') or 0)))
print(json.dumps({'recommended_submolts': ranked[:15]}, indent=2, ensure_ascii=False))
