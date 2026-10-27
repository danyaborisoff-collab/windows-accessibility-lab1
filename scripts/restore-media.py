"""Restore pre-rendered demo media; no third-party dependencies."""
from pathlib import Path
import base64, hashlib, json, lzma
root = Path(__file__).resolve().parents[1]
allowed = {'assets/before.png', 'assets/after.png', 'video/poster.png', 'video/demo.mp4'}
parts = sorted((root / 'media-source').glob('part-*.txt'))
packed = ''.join(p.read_text().strip() for p in parts)
items = json.loads(lzma.decompress(base64.b64decode(packed)))
assert {i['path'] for i in items} == allowed
for item in items:
    data = base64.b64decode(item['base64'], validate=True)
    assert hashlib.sha256(data).hexdigest() == item['sha256'], item['path']
    dest = root / item['path']
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(data)
    print(f"Restored {item['path']} ({len(data)} bytes)")
