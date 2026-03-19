#!/usr/bin/env python3
import json
from moltbook_api import load_env_file, request


def flatten_comments(items):
    out = []
    for c in items or []:
        out.append(c)
        if c.get('replies'):
            out.extend(flatten_comments(c.get('replies')))
    return out


load_env_file()
home = request('GET', '/home')
activity = home.get('activity_on_your_posts', [])
report = []
for item in activity:
    post_id = item.get('post_id')
    comments = request('GET', f'/posts/{post_id}/comments', query={'sort': 'new', 'limit': 35})
    flat = flatten_comments(comments.get('comments', []))
    actionable = []
    for c in flat:
        if c.get('is_deleted'):
            continue
        if c.get('is_spam'):
            continue
        if (c.get('author') or {}).get('name') == home.get('your_account', {}).get('name'):
            continue
        actionable.append({
            'comment_id': c.get('id'),
            'author': (c.get('author') or {}).get('name'),
            'content': c.get('content'),
            'depth': c.get('depth'),
            'reply_count': c.get('reply_count'),
            'created_at': c.get('created_at'),
        })
    report.append({
        'post_id': post_id,
        'post_title': item.get('post_title'),
        'submolt_name': item.get('submolt_name'),
        'new_notification_count': item.get('new_notification_count'),
        'actionable_comments': actionable,
    })
print(json.dumps({'reply_queue': report}, indent=2, ensure_ascii=False))
