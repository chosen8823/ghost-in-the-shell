"""
import_chatgpt_export.py

Simple script to import a ChatGPT export JSON (from ChatGPT "Export data") and store
conversations into a local SQLite database `data/chatgpt_export.db` so Sophia can use
these memories.

Usage:
  python import_chatgpt_export.py path/to/chatgpt_export.json

The script is deliberately conservative: it extracts conversation timestamps, participants,
and messages and creates basic tables for lookup. You can extend it later for richer
indexing and embedding.
"""
import sys
import os
import json
import sqlite3
from datetime import datetime

if len(sys.argv) < 2:
    print("Usage: python import_chatgpt_export.py path/to/chatgpt_export.json")
    sys.exit(1)

src = sys.argv[1]
if not os.path.exists(src):
    print("File not found:", src)
    sys.exit(1)

with open(src, 'r', encoding='utf-8') as f:
    data = json.load(f)

# naive detection of conversation records
convos = []
if isinstance(data, dict) and 'conversations' in data:
    convos = data['conversations']
elif isinstance(data, list):
    convos = data
else:
    # try to find objects shaped like conversations
    for v in data.values():
        if isinstance(v, list):
            convos = v
            break

if not convos:
    print('No conversations found in the export file (expected "conversations" array).')
    sys.exit(1)

os.makedirs('data', exist_ok=True)
conn = sqlite3.connect('data/chatgpt_export.db')
cur = conn.cursor()

cur.execute('''
CREATE TABLE IF NOT EXISTS conversations (
    id TEXT PRIMARY KEY,
    title TEXT,
    created_at TEXT
)
''')
cur.execute('''
CREATE TABLE IF NOT EXISTS messages (
    id TEXT PRIMARY KEY,
    conversation_id TEXT,
    role TEXT,
    content TEXT,
    created_at TEXT,
    FOREIGN KEY(conversation_id) REFERENCES conversations(id)
)
''')

inserted = 0
for c in convos:
    conv_id = c.get('id') or c.get('conversation_id') or str(hash(str(c.get('title', ''))))
    title = c.get('title') or c.get('name') or ''
    created = c.get('created_at') or c.get('created') or datetime.utcnow().isoformat()
    try:
        cur.execute('INSERT OR IGNORE INTO conversations (id, title, created_at) VALUES (?,?,?)', (conv_id, title, created))
    except Exception as e:
        print('skip conversation insert', e)
    msgs = c.get('messages') or c.get('content') or []
    for m in msgs:
        mid = m.get('id') or str(hash(json.dumps(m)))
        role = m.get('role') or m.get('author', {}).get('role') or 'user'
        content = m.get('content') or m.get('text') or ''
        created_m = m.get('created_at') or m.get('timestamp') or created
        try:
            cur.execute('INSERT OR IGNORE INTO messages (id, conversation_id, role, content, created_at) VALUES (?,?,?,?,?)', (mid, conv_id, role, content, created_m))
            inserted += 1
        except Exception as e:
            print('skip message', e)

conn.commit()
conn.close()
print(f'Imported {inserted} messages into data/chatgpt_export.db')
