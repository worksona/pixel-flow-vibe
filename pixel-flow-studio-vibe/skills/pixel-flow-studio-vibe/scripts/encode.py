#!/usr/bin/env python3
"""Pixel Flow Studio Vibe — author, validate and encode Studio looks into share links.

A Studio config is JSON: {"ui":{...}, "state":{"bpm":..,"zones":[...],"seq":{...},"global":{...}}, "src":{...}}.
This script adds three authoring conveniences on top of the raw app format:

  zone.preset   "glitch" ...   expanded here into enabled/fx/lfos (zone's own keys win)
  zone.motion   "orbit"  ...   shorthand for fx.motion
  state.layout  {"name":"grid3", "slots":[{zone template}, ...]}
                expanded here into geometry; slots repeat round-robin over the cells

Because expansion happens here, the link works on any Studio build that reads #cfg=.

Usage
  encode.py look.json --live --kiosk          # deployed site, opens fullscreen
  encode.py look.json --local                  # file:// link to your checkout
  encode.py look.json --base http://localhost:8799/pixel-flow-studio-pro.html
  encode.py --recipe mandala --live            # a stock whole-screen recipe (Studio 2+)
  encode.py look.json --check                  # validate only, print warnings
  encode.py look.json --expand                 # print the expanded JSON
  encode.py look.json --code                   # base64 code for Share ▸ Load a look
  encode.py --decode '<url or code>'           # #cfg= or #cfgz= back to JSON
Flags: --cam --mic --image f.jpg (source) · --compress (#cfgz=, Studio 2+ only)
"""
import sys, os, json, base64, zlib, argparse, re, random, math

HERE = os.path.dirname(os.path.abspath(__file__))
VOCAB = json.load(open(os.path.join(HERE, "vocab.json"), encoding="utf-8"))
REPO = os.environ.get("PIXEL_FLOW_REPO", os.path.expanduser("~/WORKSONA/pixel-flow"))
LOCAL_APP = os.path.join(REPO, "v1", "pixel-flow-studio-pro.html")
LIVE = "https://pixel-flow.atomic47.co/pixel-flow-studio-pro.html"
W, H = 814, 768

# ---------------------------------------------------------------- layouts
def cells(r, cx, cy):
    return [dict(x=r[0] + gx * r[2] / cx, y=r[1] + gy * r[3] / cy, w=r[2] / cx, h=r[3] / cy, shape="rect")
            for gy in range(cy) for gx in range(cx)]

def lasso(pts):
    xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
    x0, y0 = max(0, min(xs)), max(0, min(ys)); x1, y1 = min(W, max(xs)), min(H, max(ys))
    w, h = x1 - x0, y1 - y0
    if w < 8 or h < 8: return None
    return dict(x=x0, y=y0, w=w, h=h, shape="lasso", points=[[round((p[0]-x0)/w, 3), round((p[1]-y0)/h, 3)] for p in pts])

def wedges(r, n=8):
    cx, cy, R, out = r[0]+r[2]/2, r[1]+r[3]/2, min(r[2], r[3])/2, []
    for i in range(n):
        a0 = i/n*math.pi*2 - math.pi/2; a1 = (i+1)/n*math.pi*2 - math.pi/2
        pts = [[cx, cy]] + [[cx+math.cos(a0+(a1-a0)*s/4)*R, cy+math.sin(a0+(a1-a0)*s/4)*R] for s in range(5)]
        g = lasso(pts)
        if g: out.append(g)
    return out

def shatter(r, seed=17):
    rng = random.Random(seed); gx = gy = 3; P = []
    for iy in range(gy+1):
        row = []
        for ix in range(gx+1):
            jx = 0 if ix in (0, gx) else (rng.random()-.5)*r[2]/gx*.7
            jy = 0 if iy in (0, gy) else (rng.random()-.5)*r[3]/gy*.7
            row.append([r[0]+ix*r[2]/gx+jx, r[1]+iy*r[3]/gy+jy])
        P.append(row)
    out = []
    for iy in range(gy):
        for ix in range(gx):
            A, B, C, D = P[iy][ix], P[iy][ix+1], P[iy+1][ix+1], P[iy+1][ix]
            for tp in ([[A, B, C], [A, C, D]] if rng.random() < .5 else [[A, B, D], [B, C, D]]):
                g = lasso(tp)
                if g: out.append(g)
    return out

def orbiters(r):
    cx, cy = r[0]+r[2]/2, r[1]+r[3]/2; d = min(r[2], r[3])*.3; R = min(r[2], r[3])*.33
    out = [dict(x=cx-d*.7, y=cy-d*.7, w=d*1.4, h=d*1.4, shape="ellipse")]
    for i in range(4):
        a = i/4*math.pi*2
        out.append(dict(x=cx+math.cos(a)*R-d/2, y=cy+math.sin(a)*R-d/2, w=d, h=d, shape="ellipse"))
    return out

def scatter(r, n=6, shape="rect", seed=17):
    rng = random.Random(seed); out = []
    for i in range(n):
        w = r[2]*(.18+rng.random()*.16); h = r[3]*(.16+rng.random()*.16)
        out.append(dict(x=r[0]+rng.random()*(r[2]-w), y=r[1]+rng.random()*(r[3]-h), w=w, h=h, shape=shape))
    return out

LAYOUTS = {
    "full":       lambda r, *a: [dict(x=r[0], y=r[1], w=r[2], h=r[3], shape="rect")],
    "splitV":     lambda r, *a: cells(r, 2, 1),
    "splitH":     lambda r, *a: cells(r, 1, 2),
    "grid2":      lambda r, *a: cells(r, 2, 2),
    "grid3":      lambda r, *a: cells(r, 3, 3),
    "grid4":      lambda r, *a: cells(r, 4, 4),
    "bands":      lambda r, n=6, *a: cells(r, 1, int(n)),
    "cols":       lambda r, n=6, *a: cells(r, int(n), 1),
    "thirds":     lambda r, *a: [dict(x=r[0], y=r[1], w=r[2]*2/3, h=r[3], shape="rect"),
                                 dict(x=r[0]+r[2]*2/3, y=r[1], w=r[2]/3, h=r[3]/2, shape="rect"),
                                 dict(x=r[0]+r[2]*2/3, y=r[1]+r[3]/2, w=r[2]/3, h=r[3]/2, shape="rect")],
    "wedges":     lambda r, n=8, *a: wedges(r, int(n)),
    "shatter":    lambda r, seed=17, *a: shatter(r, int(seed)),
    "ringCenter": lambda r, *a: [dict(x=r[0], y=r[1], w=r[2], h=r[3], shape="rect"),
                                 dict(x=r[0]+r[2]/2-min(r[2], r[3])*.31, y=r[1]+r[3]/2-min(r[2], r[3])*.31,
                                      w=min(r[2], r[3])*.62, h=min(r[2], r[3])*.62, shape="ring")],
    "pip":        lambda r, *a: [dict(x=r[0], y=r[1], w=r[2], h=r[3], shape="rect"),
                                 dict(x=r[0]+r[2]*.62, y=r[1]+r[3]*.62, w=r[2]*.34, h=r[3]*.34, shape="rect")],
    "orbiters":   lambda r, *a: orbiters(r),
    "scatter":    lambda r, n=6, shape="rect", seed=17, *a: scatter(r, int(n), shape, int(seed)),
}

# ---------------------------------------------------------------- expansion + validation
warnings = []
def warn(msg): warnings.append(msg)

def expand_zone(z, i):
    z = json.loads(json.dumps(z))
    z.setdefault("id", "z%d" % (i+1))
    z.setdefault("shape", "rect")
    p = z.pop("preset", None)
    if p:
        P = VOCAB["presets"].get(p)
        if not P:
            warn("zone %s: unknown preset %r (have: %s)" % (z["id"], p, " ".join(VOCAB["presets"])))
        else:
            en = {k: True for k in P["e"]}
            en.update(z.get("enabled") or {})
            fx = dict(P["f"]); fx.update(z.get("fx") or {})
            z["enabled"], z["fx"] = en, fx
            if "lfos" not in z and P.get("l"): z["lfos"] = json.loads(json.dumps(P["l"]))
            z.setdefault("name", "%s %d" % (p.capitalize(), i+1))
    m = z.pop("motion", None)
    if m: z.setdefault("fx", {})["motion"] = m
    z.setdefault("name", "Zone %d" % (i+1))
    for k in ("x", "y", "w", "h"):
        if k in z: z[k] = round(float(z[k]), 1)
    return z

def expand(cfg):
    st = cfg.setdefault("state", {})
    lay = st.pop("layout", None)
    explicit = list(st.get("zones") or [])
    zones = []                      # layout cells go first (back), explicit zones stack in front
    if lay:
        name = lay.get("name", "full"); args = lay.get("args", [])
        if name not in LAYOUTS:
            warn("unknown layout %r (have: %s)" % (name, " ".join(LAYOUTS))); name = "full"
        rect = lay.get("rect", [0, 0, W, H])
        geo = LAYOUTS[name](rect, *args)
        slots = lay.get("slots") or [{}]
        for i, g in enumerate(geo):
            s = json.loads(json.dumps(slots[i % len(slots)]))
            if "shape" in s: g["shape"] = s.pop("shape")
            g.update(s); zones.append(g)
    zones += explicit
    st["zones"] = [expand_zone(z, i) for i, z in enumerate(zones)]
    if "bpm" in st:
        cfg.setdefault("ui", {})["bpm"] = st["bpm"]
    cfg.setdefault("v", 1); cfg.setdefault("type", "pixel-flow-config")
    return cfg

def validate(cfg):
    fxkeys, ranges, enums = set(VOCAB["fx"]), VOCAB["ranges"], VOCAB["enums"]
    known_fx_params = set(ranges) | set(enums) | {"kernel"}
    for z in cfg["state"]["zones"]:
        zid = z.get("id")
        if z.get("shape", "rect") not in ("rect", "ellipse", "ring", "lasso"): warn("zone %s: bad shape %r" % (zid, z.get("shape")))
        if z.get("shape") == "lasso" and not z.get("points"): warn("zone %s: lasso needs points" % zid)
        for k in ("x", "y", "w", "h"):
            if k not in z: warn("zone %s: missing %s" % (zid, k))
        if z.get("x", 0) < 0 or z.get("y", 0) < 0 or z.get("x", 0) + z.get("w", 0) > W + 1 or z.get("y", 0) + z.get("h", 0) > H + 1:
            warn("zone %s: geometry runs off the %dx%d canvas" % (zid, W, H))
        for k in (z.get("enabled") or {}):
            if k not in fxkeys: warn("zone %s: unknown effector %r" % (zid, k))
        if not any((z.get("enabled") or {}).values()): warn("zone %s: no effectors on (it will look like the source)" % zid)
        for k, v in (z.get("fx") or {}).items():
            if k not in known_fx_params: warn("zone %s: unknown fx param %r" % (zid, k)); continue
            if k in enums and v not in enums[k]: warn("zone %s: %s=%r not in %s" % (zid, k, v, enums[k]))
            if k in ranges and isinstance(v, (int, float)) and not (ranges[k][0] <= v <= ranges[k][1]):
                warn("zone %s: %s=%s outside %s" % (zid, k, v, ranges[k]))
        for l in z.get("lfos") or []:
            if l.get("target") not in VOCAB["lfoTargets"]: warn("zone %s: LFO target %r unknown" % (zid, l.get("target")))
            if l.get("wave") not in ("sine", "tri", "square", "saw", "noise"): warn("zone %s: LFO wave %r unknown" % (zid, l.get("wave")))
        if (z.get("fx") or {}).get("motion") in VOCAB["newInStudio2"]["motions"]:
            warn("zone %s: motion %r needs Studio 2 (older builds treat it as none)" % (zid, z["fx"]["motion"]))
    lanes = {"Kick", "Snare", "Hat", "Bass", "Glitch", "Morph", "Visual"}
    for l, a in (cfg["state"].get("seq") or {}).items():
        if l not in lanes: warn("seq: unknown lane %r" % l)
        elif any(v not in (0, 1) for v in a): warn("seq %s: steps must be 0/1" % l)
    if len(cfg["state"]["zones"]) > 24: warn("%d zones — over ~24 the frame rate drops" % len(cfg["state"]["zones"]))

# ---------------------------------------------------------------- codec
def b64(s): return base64.b64encode(s.encode("utf-8")).decode("ascii")
def b64url(b): return base64.urlsafe_b64encode(b).decode("ascii").rstrip("=")
def deflate(s):
    c = zlib.compressobj(9, zlib.DEFLATED, -15); return b64url(c.compress(s.encode("utf-8")) + c.flush())

def decode(text):
    m = re.search(r"cfgz=([^&\s]+)", text)
    if m:
        code = m.group(1); code += "=" * (-len(code) % 4)
        return json.loads(zlib.decompress(base64.urlsafe_b64decode(code), -15).decode("utf-8"))
    m = re.search(r"cfg=([^&\s]+)", text)
    code = (m.group(1) if m else text.strip()).replace("%2B", "+").replace("%2F", "/").replace("%3D", "=").replace("-", "+").replace("_", "/")
    code += "=" * (-len(code) % 4)
    return json.loads(base64.b64decode(code).decode("utf-8"))

def read_input(arg):
    if not arg or arg == "-": return sys.stdin.read()
    if os.path.exists(arg): return open(arg, encoding="utf-8").read()
    return arg

def main():
    ap = argparse.ArgumentParser(description="Pixel Flow Studio look -> share link")
    ap.add_argument("config", nargs="?")
    ap.add_argument("--live", action="store_true", help="link to %s" % LIVE)
    ap.add_argument("--local", action="store_true", help="file:// link to %s" % LOCAL_APP)
    ap.add_argument("--base", help="any other app URL")
    ap.add_argument("--kiosk", action="store_true", help="open fullscreen, output only")
    ap.add_argument("--compress", action="store_true", help="#cfgz= deflate link (Studio 2+ only)")
    ap.add_argument("--recipe", help="link a stock recipe by id (Studio 2+): %s" % " ".join(VOCAB["recipes"]))
    ap.add_argument("--cam", action="store_true"); ap.add_argument("--mic", action="store_true"); ap.add_argument("--image")
    ap.add_argument("--code", action="store_true", help="print only the base64 code")
    ap.add_argument("--check", action="store_true", help="validate only")
    ap.add_argument("--expand", action="store_true", help="print the expanded JSON")
    ap.add_argument("--decode", action="store_true")
    a = ap.parse_args()

    base = a.base or (LIVE if a.live else "file://" + LOCAL_APP)
    if a.decode:
        print(json.dumps(decode(read_input(a.config)), indent=2)); return
    if a.recipe:
        if a.recipe not in VOCAB["recipes"]: sys.exit("unknown recipe %r — have: %s" % (a.recipe, " ".join(VOCAB["recipes"])))
        print(base + "#recipe=" + a.recipe + ("&view=viewer" if a.kiosk else "")); return

    cfg = expand(json.loads(read_input(a.config)))
    if a.cam or a.mic or a.image:
        src = cfg.setdefault("src", {})
        if a.cam: src["cam"] = True
        if a.mic: src["mic"] = True
        if a.image:
            ext = a.image.rsplit(".", 1)[-1].lower(); mime = {"jpg": "jpeg"}.get(ext, ext)
            src["image"] = "data:image/%s;base64,%s" % (mime, base64.b64encode(open(a.image, "rb").read()).decode("ascii"))
    validate(cfg)
    for w in warnings: sys.stderr.write("warn: " + w + "\n")
    if a.check:
        print("ok" if not warnings else "%d warning(s)" % len(warnings)); return
    if a.expand:
        print(json.dumps(cfg, indent=2)); return
    js = json.dumps(cfg, separators=(",", ":"), ensure_ascii=False)
    if a.code: print(b64(js)); return
    frag = ("cfgz=" + deflate(js)) if a.compress else ("cfg=" + b64(js))
    url = base + "#" + frag + ("&view=viewer" if a.kiosk else "")
    print(url)
    sys.stderr.write("%d zones · %d chars%s\n" % (len(cfg["state"]["zones"]), len(url), " · over ~2900 chars a QR code won't fit; try --compress" if len(url) > 2900 else ""))

if __name__ == "__main__":
    main()
