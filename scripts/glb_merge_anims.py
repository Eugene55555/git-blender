#!/usr/bin/env python3
"""Merge all glTF animations in a GLB into a single animation named 'Orbit'."""
import json
import struct
import sys

p = sys.argv[1] if len(sys.argv) > 1 else '/home/kat/hermes-workspace/git-repo/git-blender/scene/ai_core.glb'
d = open(p, 'rb').read()
clen, _ = struct.unpack('<II', d[12:20])
js = json.loads(d[20:20 + clen])
bin_start = 20 + clen
blen, _ = struct.unpack('<II', d[bin_start:bin_start + 8])
binchunk = d[bin_start + 8:bin_start + 8 + blen]

anims = js.get('animations', [])
if len(anims) > 1:
    a0 = anims[0]
    samplers = a0['samplers']
    channels = a0['channels']
    for a in anims[1:]:
        base = len(samplers)
        samplers.extend(a['samplers'])
        for ch in a['channels']:
            ch2 = dict(ch)
            ch2['sampler'] = ch['sampler'] + base
            channels.append(ch2)
    a0['name'] = 'Orbit'
    js['animations'] = [a0]

jsb = json.dumps(js, separators=(',', ':')).encode('utf-8')
while len(jsb) % 4:
    jsb += b' '
binb = binchunk
while len(binb) % 4:
    binb += b'\x00'
total = 12 + 8 + len(jsb) + 8 + len(binb)
out = (struct.pack('<III', 0x46546C67, 2, total) + struct.pack('<II', len(jsb), 0x4E4F534A) + jsb
       + struct.pack('<II', len(binb), 0x004E4942) + binb)
open(p, 'wb').write(out)
print("merged animations ->", [(a.get('name'), len(a['channels'])) for a in js['animations']], "| size:", len(out))
