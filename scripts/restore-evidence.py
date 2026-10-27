"""Restore supplied screenshots; verify names and hashes."""
from pathlib import Path
import json,base64,lzma,hashlib
root=Path(__file__).resolve().parents[1]
packed=''.join(p.read_text().strip() for p in sorted((root/'evidence-source').glob('part-*.txt')))
items=json.loads(lzma.decompress(base64.b85decode(packed.encode('ascii'))))
expected={f'evidence/{name}.webp' for name in ['braille','braille-detail','environment','player-audio','player-search','web-search','transfers']}
assert {i['path'] for i in items}==expected
for item in items:
    data=base64.b64decode(item['base64'],validate=True)
    assert hashlib.sha256(data).hexdigest()==item['sha256'],item['path']
    target=root/item['path'];target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(data)
    print('Restored',item['path'])
