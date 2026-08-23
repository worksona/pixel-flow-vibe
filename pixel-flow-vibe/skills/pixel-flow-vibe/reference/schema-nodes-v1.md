# Pixel Flow NODES v1 config schema (LEGACY)

> **This is the legacy single-file Nodes app.** For anything new, author against
> `schema-nodes-v2.md` — v2 is the deployed app and a strict superset of this catalog.
> Use this file only when the target is explicitly `v1/pixel-flow-nodes.html`.

Target app: `/Users/davidolsson/WORKSONA/pixel-flow/v1/pixel-flow-nodes.html` — a TouchDesigner-style dataflow editor in one HTML file, no build step.

Target app: `/Users/davidolsson/WORKSONA/pixel-flow/v1/pixel-flow-nodes.html` — a TouchDesigner-style dataflow
editor. A config is the **graph itself**:

```json
{
  "v": 2, "type": "pixel-flow-nodes-config",
  "viewId": "out1",                       // which node feeds the Output preview (usually the output node)
  "src": { "mic": true },                 // OPTIONAL — request the mic on open (gesture-gated)
  "nodes": [ ...node objects... ]
}
```

Encode with `encode.py config.json --nodes` (targets the nodes app; `--kiosk` appends `&ui=off` for an
output-only fullscreen open with a "◱ Show UI" chip). The app auto-loads `#cfg=` on open, replacing the demo
graph. The Share ▾ menu in-app does the same round-trip.

## Node object

```json
{ "id":"kal1", "type":"kaleido", "name":"Kaleido", "x":240, "y":50,
  "params": { "seg": 8, "spin": 0.5 },
  "imgInputs": ["noise1"],           // length = imgIns; entries are source node ids or null (scene: length = its `slots` param)
  "chopInputs": [],                  // signal inputs (CHOPs like filter/adsr/tstep, and hud/scope); id or "id#outKey"
  "mods": [ { "src":"lfo1", "param":"spin", "depth":3 } ],   // TOP params driven by CHOP signals (src may be "id#outKey")
  "img": "data:image/jpeg;base64,..."   // ONLY for type:"image" — embedded picture
}
```

- **ids**: any unique strings. `imgInputs`/`chopInputs`/`mods.src` reference them. Dangling refs are pruned on load. A signal ref may be `"id#outKey"` to tap a multi-output node's named output (e.g. `"tp1#step"`); see round 6.
- **Wiring is by array position**: `imgInputs[0]` is the first image input; `composite` has two (`A`,`B`).
- **mods**: effective param = base + chopValue × depth (chop values are roughly −1..1; audio bands 0..1). Only numeric params can be modulated.
- **Layout**: nodes are ~200px wide; space them ~220px apart horizontally, rows ~280px apart. The app auto-fits the view.
- Params you omit take defaults. Unknown node types are dropped.

## Operator catalog

### TOP — image operators (blue). Output: image.

**Sources** (no inputs):
- `noise` — scale[1,12]=4, speed[0,4]=1, hue[0,360]=12 · animated blob field (default living source)
- `gradient` — angle[0,360]=30, h1[0,360]=200, h2[0,360]=330
- `bars` — count[2,16]=7, scroll[0,6]=0 · colour test bars
- `camera` — no params · live webcam (re-requests permission on open — this is how "share with cam" works)
- `image` — no params · embed the picture via the node's `img` data-URL field

All filters below take **1 image input** unless noted. Palette categories in parentheses.

**Tile**:
- `mosaic` — cols[1,32]=8, rows[1,32]=6, offset[0,120]=16, jitter[0,120]=0
- `kaleido` — seg[2,16]=6, spin[-4,4]=0.3
- `mirror` — shift[-120,120]=0, axis: `x y`
- `weave` — size[2,40]=10, amount[0,40]=12, speed[0,4]=1 · basket-weave interlace
- `wallpaper` — cols[1,8]=3, rows[1,8]=3, mode: `pmm p4 pg`, drift[0,1]=0.4 · symmetry-group tiling
- `affine` — iter[1,12]=6, scale[0.5,0.99]=0.85, rot[-1.2,1.2]=0.4, dx[-60,60]=10 · Droste/IFS recursion
- `clone` — count[1,16]=6, spread[0,150]=40, spin[0,4]=0.5 · screened rotated copies
- `slice` — count[2,40]=12, shift[0,120]=30

**Warp**:
- `transform` — tx[-200,200]=0, ty[-200,200]=0, scale[0.2,3]=1, rot[-180,180]=0
- `wave` — amp[0,80]=16, freq[0.005,0.3]=0.05, speed[0,6]=1.5
- `twist` — amount[-4,4]=1.4, rings[6,40]=22 · swirl
- `ripple` — amount[0,40]=14, freq[0.01,0.2]=0.05, speed[0,6]=2 · radial rings
- `melt` — amount[0,80]=30, speed[0,4]=1 · brightness-driven column drip
- `smear` — amount[0,60]=22, angle[0,360]=35 · directional streaks
- `czoom` — amount[0,40]=12 · chromatic zoom ghosts
- `field` — amount[0,50]=18, scale[8,64]=24, speed[0,4]=1 · noise vector-field liquify
- `displace` — amount[0,60]=20, cell[4,24]=8 · self-displace by luminance

**Glitch**:
- `rgbshift` — amount[0,40]=6, angle[0,360]=0
- `pixelate` — size[2,64]=12
- `glitch` — amount[0,80]=26, blocks[2,24]=8 · torn blocks that hold briefly
- `vhs` — amount[0,40]=12 · row jitter + tears + fringing + specks
- `sort` — th[0,1]=0.45 · pixel sort (bright runs per row)
- `dither` — levels[2,8]=3 · Bayer ordered dithering

**Color**:
- `posterize` — levels[2,16]=5 · `threshold` — th[0,1]=0.5 · `invert` — mix[0,1]=1
- `hsv` — hue[0,360]=0, sat[0,3]=1, bri[0,3]=1
- `solarize` — th[0,1]=0.5 · invert only above threshold
- `colormtx` — matrix: `swap rswap sepia cool acid`, mix[0,1]=0.8 · RGB channel matrix

**Stylize**:
- `blur` — r[0,24]=3
- `dot` — size[3,28]=8 · colour halftone on black
- `ascii` — size[6,24]=10 · coloured character render
- `edges` — strength[1,6]=3 · edge extraction
- `bloom` — amount[0,1]=0.45 · bright-pass glow
- `convolve` — kernel: `sharpen emboss edge ridge blur`, mix[0,1]=0.8 · 3×3 kernel
- `scan` — spacing[3,40]=8, amount[0,30]=12 · wobbling scanlines

**Time**:
- `feedback` — decay[0,0.98]=0.85, zoom[0.9,1.1]=1.01, rot[-6,6]=0.4 · trails/tunnels; feedback cycles allowed
- `timeslice` — slices[2,40]=12, depth[1,23]=12, dir: `h v` · slit-scan from a 24-frame history

**Combine** (2 image inputs A,B):
- `composite` — mode: `source-over lighter screen multiply overlay difference exclusion hard-light` (default lighter), mix[0,1]=1

**Out** (1 image input):
- `output` — the final image; set `viewId` to its id.

### CHOP — signal operators (green). Output: a number per frame.

- `lfo` — shape: `sine tri square saw`, rate[0.02,6]=0.5, amp[0,1]=1, bias[-1,1]=0
- `audio` — source: `mic file`, band: `low mid high level`, gain[0,4]=1 · loudness from the mic OR a user-loaded audio file (per-node analyser; the file is chosen in-app via the Inspector and is NOT serialized — author configs with source:"mic" unless the user will load a track themselves)
- `constant` — value[-1,1]=0.5
- `noisec` — rate[0.1,8]=1, amp[0,1]=1 · smooth wandering random
- `mathc` — 1 signal input · op: `add mul abs sin clamp01`, k[-2,2]=1

## Mic / camera on open

- Graphs containing an `audio` CHOP (or configs with `src.mic:true`) show a "Tap / click anywhere to enable the mic"
  toast on open and start the mic on the first gesture.
- `camera` nodes request the webcam automatically when the graph loads (browser permission prompt).
- Both need a secure context when hosted (https); `file://` works in Chrome.

## A minimal recipe (audio-reactive kaleidoscope with trails)

```json
{ "viewId":"out1", "nodes":[
  {"id":"src1","type":"noise","x":20,"y":60,"params":{"hue":200}},
  {"id":"kal1","type":"kaleido","x":240,"y":50,"params":{"seg":8},"imgInputs":["src1"],
    "mods":[{"src":"lfo1","param":"spin","depth":2.5}]},
  {"id":"fb1","type":"feedback","x":460,"y":50,"params":{"decay":0.9,"zoom":1.02},"imgInputs":["kal1"]},
  {"id":"out1","type":"output","x":680,"y":60,"imgInputs":["fb1"]},
  {"id":"lfo1","type":"lfo","x":240,"y":330,"params":{"rate":0.3}},
  {"id":"aud1","type":"audio","x":460,"y":330,"params":{"band":"low","gain":2}}
]}
```
(Add a `mods` entry with `"src":"aud1"` on any filter to make it beat-reactive; include `src:{mic:true}`.)

