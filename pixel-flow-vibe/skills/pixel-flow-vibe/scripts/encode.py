#!/usr/bin/env python3
"""Pixel Flow Vibe — config <-> share-URL codec.

Encodes a Pixel Flow config JSON into a `#cfg=<base64>` share URL that the app
auto-applies on load, and decodes such a URL/code back to JSON.

The base64 alphabet + UTF-8 handling here match the app's b64enc/b64dec
(btoa/atob over UTF-8 bytes), so URLs produced here load in the browser and
vice-versa.

Usage
  # config.json -> file:// share URL
  encode.py config.json
  cat config.json | encode.py

  # override the app location / use a hosted URL
  encode.py config.json --app /path/to/pixel-flow-studio-pro.html
  encode.py config.json --base https://example.com/pixel-flow.html

  # Nodes v2 (the current graph app) — deployed, or the local vite dev server
  encode.py graph.json --nodes --live
  encode.py graph.json --nodes --dev

  # Nodes v1 (legacy single-file) — bare --nodes resolves to the local v1 HTML
  encode.py graph.json --nodes

  # emit just the base64 code (for the app's Share -> Load Config box)
  encode.py config.json --code

  # decode a share URL or raw code back to pretty JSON
  encode.py --decode 'file://.../app.html#cfg=eyJ...'
  echo 'eyJ...' | encode.py --decode
"""
import sys, json, base64, argparse, os, re

REPO = "/Users/davidolsson/WORKSONA/pixel-flow"   # worksona/pixel-flow
DEFAULT_APP = REPO + "/v1/pixel-flow-studio-pro.html"
DEFAULT_APP_NODES = REPO + "/v1/pixel-flow-nodes.html"  # legacy single-file Nodes
LIVE_HOST = "https://pixel-flow.atomic47.co"      # deployed site — Nodes here is v2
DEV_HOST = "http://localhost:5173"                # nodes-v2 vite dev server

def read_input(arg):
    if not arg or arg == "-":
        return sys.stdin.read()
    if os.path.exists(arg):
        return open(arg, encoding="utf-8").read()
    return arg  # treat the argument itself as the payload (inline JSON / code / url)

def main():
    p = argparse.ArgumentParser(description="Pixel Flow config <-> share URL codec")
    p.add_argument("config", nargs="?", help="config JSON file, '-' for stdin, or inline payload")
    p.add_argument("--app", default=DEFAULT_APP, help="path to pixel-flow-studio-pro.html")
    p.add_argument("--base", help="override base URL (hosted deploy); replaces the file:// app path")
    p.add_argument("--code", action="store_true", help="print only the base64 code, not a URL")
    p.add_argument("--nodes", action="store_true", help="target the node-graph app (pixel-flow-nodes.html); config is a graph {nodes:[...]}")
    p.add_argument("--live", action="store_true", help="produce a link to the deployed site (%s) instead of a local file://; Nodes there is v2" % LIVE_HOST)
    p.add_argument("--dev", action="store_true", help="target the local nodes-v2 vite dev server (%s) — v2 operators, no deploy needed" % DEV_HOST)
    p.add_argument("--kiosk", action="store_true", help="append &view=viewer so the app opens as a fullscreen output-only experience (a tiny ✎ chip returns to the editor)")
    p.add_argument("--cam", action="store_true", help="set src.cam so the app requests the webcam on open")
    p.add_argument("--mic", action="store_true", help="set src.mic so the app requests the mic (FFT) on open")
    p.add_argument("--image", help="embed an image file as the source (src.image data URL)")
    p.add_argument("--decode", action="store_true", help="decode a share URL / base64 code to JSON")
    a = p.parse_args()

    raw = read_input(a.config)

    if a.decode:
        m = re.search(r"cfg=([^&\s]+)", raw)
        code = m.group(1) if m else raw.strip()
        # tolerate url-encoding and url-safe base64
        code = code.replace("%2B", "+").replace("%2F", "/").replace("%3D", "=")
        code = code.replace("-", "+").replace("_", "/")
        pad = (-len(code)) % 4
        code += "=" * pad
        print(json.dumps(json.loads(base64.b64decode(code).decode("utf-8")), indent=2))
        return

    cfg = json.loads(raw)  # validate
    is_graph = isinstance(cfg.get("nodes"), list)
    cfg.setdefault("v", 2 if is_graph else 1)
    cfg.setdefault("type", "pixel-flow-nodes-config" if is_graph else "pixel-flow-config")
    if a.nodes and a.app == DEFAULT_APP:
        a.app = DEFAULT_APP_NODES
    if a.dev and not a.base:
        # nodes-v2 dev server serves the graph app at the root
        a.base = DEV_HOST + "/"
    if a.live and not a.base:
        # nodes → the deployed v2 app at /pixel-flow-nodes/ . Link it directly: the old
        # /pixel-flow-nodes.html now 302s there, and a redirect can drop the #cfg= fragment.
        a.base = LIVE_HOST + "/" + ("pixel-flow-nodes/" if (a.nodes or is_graph) else "pixel-flow-studio-pro.html")

    if a.cam or a.mic or a.image:
        src = cfg.setdefault("src", {})
        if a.cam:
            src["cam"] = True
        if a.mic:
            src["mic"] = True
        if a.image:
            mime = {"jpg": "jpeg", "jpeg": "jpeg", "png": "png", "webp": "webp",
                    "gif": "gif"}.get(a.image.rsplit(".", 1)[-1].lower(), "jpeg")
            with open(a.image, "rb") as f:
                src["image"] = "data:image/%s;base64,%s" % (
                    mime, base64.b64encode(f.read()).decode("ascii"))
    b64 = base64.b64encode(
        json.dumps(cfg, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    ).decode("ascii")

    if a.code:
        print(b64)
        return

    base = a.base or ("file://" + os.path.abspath(a.app))
    url = base + "#cfg=" + b64 + ("&view=viewer" if a.kiosk else "")
    print(url)
    sys.stderr.write("cfg %d bytes -> url %d chars\n" % (len(raw), len(url)))

if __name__ == "__main__":
    main()
