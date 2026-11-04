#!/usr/bin/env python3
"""Write a small, smooth night-sea gradient PNG (stdlib only) to use as a clean Studio source."""
import sys, zlib, struct, math

W, H = 160, 150

def lerp(a, b, t): return a + (b - a) * t
def mix(c1, c2, t): return tuple(lerp(a, b, max(0.0, min(1.0, t))) for a, b in zip(c1, c2))
def smooth(t): t = max(0.0, min(1.0, t)); return t * t * (3 - 2 * t)

SKY_TOP = (7, 9, 30); SKY_LOW = (30, 34, 82); GLOW = (232, 140, 96); SEA_TOP = (18, 46, 64); SEA_LOW = (4, 10, 18)
HORIZON = 0.56

def pixel(x, y):
    u, v = x / (W - 1), y / (H - 1)
    if v < HORIZON:
        c = mix(SKY_TOP, SKY_LOW, smooth(v / HORIZON))
        # warm glow just above the horizon, widest at the centre
        d = (HORIZON - v) / 0.10
        g = math.exp(-d * d) * (0.55 + 0.45 * math.exp(-((u - 0.5) / 0.35) ** 2))
        c = mix(c, GLOW, g * 0.85)
    else:
        t = (v - HORIZON) / (1 - HORIZON)
        c = mix(SEA_TOP, SEA_LOW, smooth(t))
        # reflection column under the glow, fading with depth
        r = math.exp(-((u - 0.5) / (0.10 + 0.12 * t)) ** 2) * math.exp(-t * 3.2)
        c = mix(c, GLOW, r * 0.45)
        # thin bright line at the horizon itself
        c = mix(c, GLOW, math.exp(-((v - HORIZON) / 0.012) ** 2) * 0.6)
    return tuple(int(round(max(0, min(255, k)))) for k in c)

def png(path):
    raw = bytearray()
    prev = bytes(W * 3)
    for y in range(H):
        row = bytes(v for x in range(W) for v in pixel(x, y))
        raw.append(2)  # 'Up' filter: vertical gradients compress well
        raw += bytes((row[i] - prev[i]) & 255 for i in range(len(row)))
        prev = row
    def chunk(tag, data): return struct.pack('>I', len(data)) + tag + data + struct.pack('>I', zlib.crc32(tag + data) & 0xffffffff)
    out = b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', struct.pack('>IIBBBBB', W, H, 8, 2, 0, 0, 0)) + chunk(b'IDAT', zlib.compress(bytes(raw), 9)) + chunk(b'IEND', b'')
    open(path, 'wb').write(out)
    return len(out)

if __name__ == '__main__':
    print(png(sys.argv[1]), 'bytes')
