#!/usr/bin/env python3
import json
from moltbook_api import load_env_file, request


def countish(value):
    if isinstance(value, dict):
        return value.get('count') or len(value.get('items', []) or [])
    if isinstance(value, list):
        return len(value)
    return 0


load_env_file()
home = request('GET', '/home')
account = home.get('your_account', {}) if isinstance(home, dict) else {}
activity = home.get('activity_on_your_posts', []) if isinstance(home, dict) else []
dms = home.get('your_direct_messages', {}) if isinstance(home, dict) else {}
summary = {
  'agent': account.get('name') if isinstance(account, dict) else None,
  'karma': account.get('karma') if isinstance(account, dict) else None,
  'unread_notifications': account.get('unread_notification_count') if isinstance(account, dict) else None,
  'post_activity_count': countish(activity),
  'dm_unread': dms.get('total_unread') if isinstance(dms, dict) else None,
  'dm_requests': ((dms.get('requests') or {}).get('count')) if isinstance(dms, dict) else None,
  'what_to_do_next': home.get('what_to_do_next') if isinstance(home, dict) else None,
}
print(json.dumps(summary, indent=2, ensure_ascii=False))
