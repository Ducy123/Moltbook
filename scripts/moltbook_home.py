#!/usr/bin/env python3
import json
from moltbook_api import load_env_file, request

load_env_file()
result = request('GET', '/home')
print(json.dumps(result, indent=2, ensure_ascii=False))
