#!/usr/bin/env python3
"""ppm2png.py a.ppm [b.ppm ...] - the renderer's P3 frames as PNG (no dependencies)."""
import struct, sys, zlib

def chunk(tag, data):
    return struct.pack(">I", len(data)) + tag + data + struct.pack(">I", zlib.crc32(tag + data))

for path in sys.argv[1:]:
    tok = open(path).read().split()
    w, h, mx = int(tok[1]), int(tok[2]), int(tok[3])
    px = bytes(int(v) * 255 // mx for v in tok[4:4 + 3 * w * h])
    raw = b"".join(b"\0" + px[y * 3 * w:(y + 1) * 3 * w] for y in range(h))
    out = path.rsplit(".", 1)[0] + ".png"
    open(out, "wb").write(b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0))
                          + chunk(b"IDAT", zlib.compress(raw, 6)) + chunk(b"IEND", b""))
    print(out)
