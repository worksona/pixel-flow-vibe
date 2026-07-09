# Pixel Flow NODES config schema (authoritative)

Target app: `/Users/davidolsson/Desktop/pixel-flow/pixel-flow-nodes.html` — a TouchDesigner-style dataflow
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

---

## v2 nodes (Pixel Flow Nodes v2)

**Availability:** these operators exist in **Pixel Flow Nodes v2** (the multi-file project at
`/Users/davidolsson/Desktop/pixel-flow/pixel-flow-nodes-v2/`, run via `npm run dev`), not in the
legacy single-file `pixel-flow-nodes.html`. The `#cfg=` codec is unchanged, so the SAME
`encode.py … --nodes` round-trip works — just target a host serving v2. A node declares
`family` (`TOP`=image / `CHOP`=signal — how it cooks) and optional `group` (`SOP`=geometry/3D —
how it is coloured/catalogued). Author these exactly like any other node; only numeric params modulate.

### New CHOP signal operators (green). Output: a number per frame.

- `clock` — bpm[20,300]=120, div: `4 2 1 1/2 1/4 1/8` =1, shape: `pulse ramp tri square` =pulse · BPM-locked clock (0..1)
- `envelope` — 1 signal input (`trig`) · attack[0,2]=.05, release[0,4]=.5, thresh[0,1]=.5 · AR envelope, rises while trig>thresh
- `randwalk` — speed[0,4]=1, step[0,1]=.3 · gently-centred Brownian drift (−1..1)
- `smooth` — 1 signal input (`sig`) · lag[0,1]=.5 · one-pole low-pass / dampener
- `remap` — 1 signal input (`sig`) · inLo[-2,2]=-1, inHi[-2,2]=1, outLo[-2,2]=0, outHi[-2,2]=1, clamp: `on off` =on · linear range remap
- `logic` — 1 signal input (`sig`) · op: `gt lt pulse` =gt, thresh[-1,1]=.5 · threshold → 0/1, `pulse`=rising edge
- `seq` — bpm[20,300]=120, steps[2,16]=8, gate: `hold pulse` =hold · step sequencer; per-step values live in `params.pattern` (array of 0..1, length=steps; default `[1,0,0,0,1,0,0,0]`)

### New SOP geometry / particle operators (pink). family:`TOP`, group:`SOP`. Output: image.

- `grid` — cols[2,64]=16, rows[2,48]=12, dot[1,20]=3, hue[0,360]=190, style: `dots cross lines` · procedural lattice (source, no input)
- `pointcloud` — 1 image input · step[2,24]=6, size[1,16]=3, jitter[0,20]=0, mode: `dot square` · samples the input image into coloured points (image→points)
- `particles` — 1 image input (`spawn`, optional) · count[20,1500]=400, speed[0,4]=1, size[1,10]=2, spread[0,1]=.4, gravity[-2,2]=0, swirl[-3,3]=0, trail[0,.98]=.85, hue[0,360]=35 · particle field; with an image input, particles spawn from and take the colour of bright areas. Modulate count/speed/swirl for audio-reactive motion.
- `instancer` — 1 image input · cols[1,20]=6, rows[1,20]=6, scale[.05,1]=.32, spin[-3,3]=0, jitter[0,60]=0 · stamps the input image across a jittered grid

### 3D operator (Three.js). family:`TOP`, group:`SOP`, cat:`Render 3D`. Output: image.

- `render3d` — 1 image input (`tex`, optional) · shape: `torusKnot ico box sphere` =torusKnot, rotX[-2,2]=.15, rotY[-2,2]=.35, dist[1.5,8]=3.6, metal[0,1]=.6, rough[0,1]=.3, hue[0,360]=215 · renders a lit 3D mesh to a texture. An image input wraps onto the mesh (TOP→material map); rotX/rotY are modulatable (audio-reactive 3D). Output flows into any downstream TOP.

### v2 recipes

Audio-reactive 3D (camera texture on a spinning icosahedron, feedback trails):
```json
{ "viewId":"out1","src":{"mic":true},"nodes":[
  {"id":"cam1","type":"camera","x":20,"y":60},
  {"id":"r3","type":"render3d","x":260,"y":50,"params":{"shape":"ico","metal":0.7},"imgInputs":["cam1"],
    "mods":[{"src":"aud1","param":"rotY","depth":3}]},
  {"id":"fb1","type":"feedback","x":500,"y":50,"params":{"decay":0.8,"zoom":1.02},"imgInputs":["r3"]},
  {"id":"out1","type":"output","x":740,"y":60,"imgInputs":["fb1"]},
  {"id":"aud1","type":"audio","x":260,"y":340,"params":{"band":"low","gain":3}}
]}
```

Rhythmic glitch driven by a step sequencer (no mic needed):
```json
{ "viewId":"out1","nodes":[
  {"id":"n1","type":"noise","x":20,"y":60,"params":{"hue":150}},
  {"id":"g1","type":"glitch","x":260,"y":50,"imgInputs":["n1"],"mods":[{"src":"q1","param":"amount","depth":40}]},
  {"id":"out1","type":"output","x":500,"y":60,"imgInputs":["g1"]},
  {"id":"q1","type":"seq","x":260,"y":340,"params":{"bpm":120,"steps":8,"pattern":[1,0,0.5,0,1,0,0.5,0]}}
]}
```

Particle field from a noise source, swirl modulated by an LFO:
```json
{ "viewId":"out1","nodes":[
  {"id":"n1","type":"noise","x":20,"y":60,"params":{"hue":35}},
  {"id":"p1","type":"particles","x":260,"y":50,"params":{"count":600,"trail":0.9},"imgInputs":["n1"],
    "mods":[{"src":"l1","param":"swirl","depth":2}]},
  {"id":"b1","type":"bloom","x":500,"y":50,"imgInputs":["p1"]},
  {"id":"out1","type":"output","x":740,"y":60,"imgInputs":["b1"]},
  {"id":"l1","type":"lfo","x":260,"y":340,"params":{"rate":0.2}}
]}
```

---

## v2 nodes — round 2 (sequencer/synth · more geometry & 3D · algorithmic)

Same availability note as above (Pixel Flow Nodes **v2**). All are authored like any node.

### Synth / sequencer (CHOP, green)
- `synth` — bpm[40,240]=110, steps[2,16]=8, wave: `sine triangle square sawtooth`, scale: `penta major minor dorian chrom`, root: `C..B`, octave[0,4]=2, attack[0,.5]=.01, release[.05,1.5]=.4, gain[0,1]=.5 · a step-sequenced Web-Audio synth; internal pattern in `params.on` (0/1 per step) + `params.pitch` (scale-degree per step). Its output signal is the live note **amplitude** (0..1) — modulate visuals to what it plays. Audio starts on a user gesture.
- `arp` — bpm[40,240]=120, steps[2,12]=5, mode: `up down updown random` · arpeggiator signal (0..1), no sound.

### More geometry (SOP, pink). family:`TOP`. Output: image.
- `voronoi` — cells[4,80]=26, drift[0,1]=.35, mode: `flat edges dots`, hue[0,360]=210 · drifting Voronoi diagram (source)
- `truchet` — cols[4,40]=12, weight[1,10]=3, style: `arcs diagonals`, hue[0,360]=160 · Truchet-tile curve field (source)
- `spiro` — R[20,140]=96, r[5,90]=36, d[5,120]=64, speed[0,3]=.6, hue[0,360]=280 · animated spirograph (source)

### More 3D (SOP, Three.js lazy). family:`TOP`, 1 image input. Output: image.
- `points3d` — density[3,16]=6, depth[0,3]=1, size[.5,6]=2, rotY[-2,2]=.3, dist[1.5,6]=2.6 · input image → rotating 3D point cloud (Z = brightness)
- `terrain3d` — height[0,3]=1, rotY[-2,2]=.25, wire: `solid wire`, dist[1.5,6]=3, hue[0,360]=150 · input image → lit 3D heightfield
- `render3d` now also offers shapes: `torusKnot torus ico dodeca box sphere cone cylinder`

### Algorithmic / generative (ALGO, gold). family:`TOP`, group:`ALGO`. Output: image.
- `life` — cell[2,20]=5, speed[0,30]=12, density[.05,.8]=.32, hue, wrap: `on off` · Conway's Game of Life (source; reseed in-app)
- `brain` — cell, speed, density, hue · Brian's Brain 3-state automaton (source)
- `cyclic` — cell, speed, states[3,16]=10, thresh[1,3]=1, hue · cyclic CA spirals (source)
- `rd` — feed[.01,.09]=.037, kill[.03,.07]=.06, iter[1,14]=8, hue · Gray-Scott reaction-diffusion (source)
- `mandelbrot` — cx, cy, zoom[.4,400]=1, iter[24,220]=90, hue · Mandelbrot set (source)
- `julia` — radius[.1,.9]=.7, speed[0,2]=.15, iter, zoom, hue · animated Julia set (source)
- `lsystem` — preset: `plant tree koch dragon sierpinski`, iter[1,7]=5, angle[5,90]=25, sway[0,1]=.15, hue · turtle-drawn L-system (source)
- `cppn` — seed[1,9999]=42, layers[1,5]=3, scale[.5,6]=2.4, speed[0,2]=.25, hue · a random-weight neural net (CPPN) → image (source)
- `kernel` — 1 image input · div[.1,9]=1, bias[-1,1]=0, mix[0,1]=1, plus `params.k` (9-number 3×3 matrix) · editable convolution matrix (filter)
- `dejong` — a,b,c,d[-3,3], drift[0,1]=.12, fade[.5,.99]=.9, hue · De Jong strange attractor (source)

### Components
Reusable grouped patches are authored in-app (shift-select → Components ▾ → Save), stored in
localStorage and exported as `*.pfcomp.json`. They are not part of the `#cfg=` graph payload — a
shared link already contains all the materialised nodes.

---

## v2 nodes — round 3 (data/text · MIDI/touch/gyro · force field/optical flow · exposed components)

Same v2-only availability note as above.

### DAT — data / text (CHOP, group DAT, cat Data)
- `expr` — 1 signal input (`x`) · k[-4,4]=1, plus `params.expr` (freeform JS string, vars `x,t,k,TAU,clamp`) · expression node
- `table` — rows[1,8]=3, cols[1,8]=3, row[0,7]=0 (moddable), col[0,7]=0 (moddable), plus `params.data` (2D array) · editable numeric grid, cell selected by row/col
- `jsonin` — index[0,63]=0 (moddable), auto: `off on`, bpm[20,300]=120, plus `params.json` (string, JSON array of numbers) · steps through the array
- `datamap` — 1 signal input (`sig`) · inLo/inHi[-2,2]=-1/1, plus `params.points` (array of [x,y] pairs, x in 0..1) · piecewise-linear curve remap
- `text` / `prompt` / `annotation` — no params; `params.text` (string) · inert documentation nodes (short label / AI-prompt metadata / bigger note)
- `exportdata` — 1 signal input (`sig`) · maxlen[16,2000]=256 · records + passes through the signal; Inspector has a Download JSON button

### More Signal (CHOP)
- `midi` — mode: `note cc` · Web MIDI note-on velocity or latest CC (0..1); needs `enableMIDI` gesture in-app
- `touch` — axis: `x y pressure`, area: `window output` · pointer/touch position + pressure
- `gyro` — axis: `beta gamma alpha` · phone tilt via Device Orientation (mobile only; 0 on desktop)

### More Geometry/3D (TOP, group SOP, cat Particles)
- `forcefield` — mode: `attract repel turbulence`, strength[0,2]=1, scale[8,64]=24 (cell size), speed[0,3]=.5 · a vector field visualised as a displacement map (source) — feed into `displace`/`field` as the driving image
- `opticalflow` — 1 image input · thresh[0,1]=.08, gain[.5,6]=2, hue[0,360]=120 · frame-difference motion map (lite optical flow)

### Components (editor-only, not part of `#cfg=`)
Saving a component (shift-select → Components ▾ → Save) now opens a picker to check off numeric
params to **expose**. Placed instances tag their nodes with a shared instance id; selecting ANY node
in that instance shows a "⧉ exposed controls" panel in the Inspector with live sliders across the
whole instance. This is editor-session state only — not serialized into shared `#cfg=` links (those
already contain every materialised node in full).

---

## v2 nodes — round 4 (Video source)

- `video` — no params · a **video FILE** played as a texture (`camera` is the webcam; this is the
  file-based counterpart). The file is chosen in-app (Browse / drag-drop onto the canvas) and is NOT
  serialized, so author graphs with `video` only when the user will load a clip themselves. v2-only.

---

## v2 nodes — round 5 (modular analog synth · audio-rate CHOP nodes)

A light, TouchDesigner-style modular synth you patch on the canvas (distinct from the monolithic
`synth`). These are `family:'CHOP'`, `cat:'Synth'`, flagged `audio:true` — their green wires carry
Web Audio **audio-rate** streams. Each declares `audioIns` (input indices that are audio); the other
inputs are control (per-frame numbers). Sound is only audible via an `audioout` node (click its Enable
button — gesture-gated). Audio is NOT part of the `#cfg=` visual payload, but these nodes DO serialize
(params + wiring), so a shared graph re-creates the patch; each audio node also outputs its live
amplitude as a signal, so you can `mods` a visual from it.

- `osc` — 1 input `pitch` (control, 0..1 → scale degree) · wave: `saw square tri sine`, root: `C..B`,
  octave[0,6], range[1,4] (octaves the pitch input spans), scale: `penta major minor dorian chrom`,
  detune[-50,50] cents, glide[0,.3], level[0,1] · audio oscillator (no pitch input = held drone)
- `filter` — inputs `in` (audio), `cutoff` (control CV, ±1 ≈ ±3.5 oct) · type: `lowpass highpass
  bandpass`, cutoff[50,9000], reso[0,24] · resonant biquad filter
- `adsr` — inputs `in` (audio), `gate` (control, >0.5 = note on) · attack[0,2], decay[0,2],
  sustain[0,1], release[.02,3], level[0,1] · ADSR envelope / VCA (no gate wired = holds open)
- `mixer` — inputs `a`,`b`,`c` (all audio) · level[0,1] · sums audio inputs
- `audioout` — input `in` (audio) · level[0,1] · the speaker sink

Typical patch: `Step Seq → osc.pitch`, `Beat Clock (pulse) → adsr.gate`, `LFO → filter.cutoff`,
`osc → filter → adsr → audioout`; then `mods` a visual param from the `adsr` amplitude.

## v2 nodes — round 6 (Scene & Timeline · compose a framed scene from one clock)

Build a **framed, clock-driven scene**: many chains composited into one frame, driven by a shared
playhead. A Scene is an ordinary TOP — view it (or feed an `output`) and it *is* your output.

Two schema capabilities were added here (both serialize in `#cfg=`):

- **Multi-output signals.** A `chopInputs`/`mods.src` ref may address a specific output of a
  multi-output node as `"nodeId#outKey"` (plain `"nodeId"` = that node's primary output). The
  `transport` node exposes `phase` (primary), `step`, and `gate` — so `"tp1#step"` taps its step index.
- **Dynamic Scene inputs.** The `scene` node's `slots` param (1–12) sets how many image inputs it has;
  `imgInputs` length follows it. Wire chains into `imgInputs[0..slots-1]`.

### Scene compositor (COMP, purple). family:`TOP`, group:`COMP`, cat:`Scene`. Output: image.
- `scene` — `slots` image inputs (1–12, default 6) · layout: `single pip grid2 grid3 golden free`,
  slots[1,12]=6, gap[0,24]=4, border[0,5]=1, bg: `ink black white none`, render: `full half quarter`
  (per-node cook resolution — cheaper for big scenes), aspect: `app 16:9 9:16 1:1 4:3 21:9` (own frame
  ratio, letterboxed) · **`golden`** = Fibonacci subdivision, adapts cell count to how many inputs are
  wired; grids/pip map by input number; `free` reads `params.rects` = `[{x,y,w,h}]` normalized 0–1.

### Timeline (CHOP, green). cat:`Timeline`. Output: a number per frame.
- `transport` — **multi-output** `#phase` (0→1, primary), `#step` (integer 0..steps-1), `#gate` (1/0 per
  step) · source: `local global` (global = follow the app-wide timeline scrubber in the toolbar),
  bpm[30,240]=120, steps[1,32]=8, bars[1,8]=1, run: `play hold`, swing[0,.5]=0 · shared playhead
  (dt-accumulated, so the global Speed knob + pause apply)
- `tstep` — 1 input `phase` · steps[1,32]=8 · phase → step index (inherits steps from a wired transport)
- `tgate` — 1 input `phase` · width[.05,.95]=.5, steps[1,32]=8 · phase → 1/0 gate, one pulse per step

> The global toolbar timeline (⏱) is app state, not graph state — it isn't in `#cfg=`. A `transport`
> with `source:"global"` taps it and auto-enables it. For a self-contained shareable graph, use
> `source:"local"` (the default) so the clock lives in the node.

### Scene sources / overlays. family:`TOP`. Output: image.
- `mediabank` (cat:`Source`, blue) — no image inputs · index[0,64]=0 (mod it from a `transport#step`),
  fit: `cover contain` · an ordered image set, outputs the one at Index. **Images are in-memory only**
  (like `image`): `#cfg=` can't embed them — the count/order isn't saved, the user re-adds files.
- `hud` (group:`DAT`, amber; cat:`Scene`) — 1 image input `bg` + 4 signal inputs `a b c d` · template
  (string; tokens `{a} {b} {c} {d}` print the inputs live, `{a:2}` sets decimals), size[10,80]=22,
  hue[0,360]=78, align: `left center right`, x[0,1]=.05, y[0,1]=.08, plate: `on off` · text/value overlay
- `scope` (cat:`Scene`, blue) — 1 signal input · mode: `line fill bars`, hue[0,360]=90, thick[1,6]=2,
  grid: `on off` · full-frame oscilloscope of the wired signal
- `spiral` (group:`SOP`, pink; cat:`Geometry`) — no inputs · turns[3,10]=6, phase[0,1]=0 (mod from a
  transport for a travelling dot), stroke[1,6]=2, hue[0,360]=48, squares: `on off` · golden/Fibonacci
  overlay (transparent bg — composite over a Scene)

### Fibonacci-Fruits recipe (one clock → images + params + readout + overlay, in one golden frame)
1. `transport` `tp` (steps 7). 
2. `mediabank` `bank` — `mods:[{src:"tp#step", param:"index", depth:1}]` so it flips a fruit per step.
   (User adds 7 images in-app; the graph still runs empty, showing the framework.)
3. Main chain: `bank → twist → feedback` (`mods` twist.amount from `tp#phase`) → `hud` (bg input) with
   `template:"Fn = Fn-1 + Fn-2\nphase {a:2}  step {b}"`, `chopInputs:["tp","tp#step"]` (a=phase, b=step).
4. `spiral` `sp` — `mods:[{src:"tp", param:"phase", depth:1}]` (Fibonacci overlay tracks the clock).
5. `scope` `sc` — `chopInputs:["tp"]` (plots the phase).
6. `scene` (layout `golden`, slots 5): `imgInputs:["hud","bank","<kaleido of bank>","sp","sc"]` — big
   cell = the HUD'd main chain, then the raw fruit, a filtered variant, the spiral, the scope.
7. `output` ← `scene` (or just view the scene). One `transport` drives image, params, readout and overlay
   in sync inside one framed composite.

Generic scene starters: **dashboard** (`grid3`, 6 chains incl. a `scope` + `spiral` on a `transport`),
**picture-in-picture** (`pip`, a big chain + an inset `camera`). Bump `slots` for more `golden`/`free` cells.

## v2 nodes — round 7 (vision → sound & control · motion, tracking, waveforms, webs)

Turn a camera into a controller: motion / hand / face / body / object → **signals** (drive any node)
**and** an annotated video **output**. Two schema things recur here:

- **CHOPs can read an image.** Some CHOPs declare `imgIns:1` — image-wire a video/tracker into them and
  they read its pixels/landmarks (they still output a signal). `chopInputs` is unused; use `imgInputs`.
- **Runtime, not `#cfg=`.** Camera frames, MediaPipe models (hand/face/pose) and colour blobs are live —
  none are embedded in a share link. A shared graph re-creates the *wiring*; detection happens on open.

### Motion → sound (the "METALPECKER" trio)
- `vsensor` (Video Sensor, CHOP · **imgIns:1**) — mode: `motion bright`, box `x/y/w/h` (0–1), gain[.5,30],
  smooth[0,.95] · reduces a box region of a wired video to a 0..1 signal (frame-difference motion or
  brightness). The first image-reading CHOP; turns any camera into a controller.
- `onset` (CHOP, **multi-output** `#gate`/`#env`) — 1 signal input · thresh[0,1]=.2, hyst[0,.9]=.4,
  len[10,500]ms, hold[0,1000]ms lockout, decay[50,2000]ms · Schmitt trigger: a rising input → a gate
  (`#gate`, → an ADSR) + a decaying pluck (`#env`, → visuals). One strike = one hit.
- `wave3d` (3D Waveform, TOP · SOP) — 2 signal inputs `level`,`strike` · hue, density[12,160] columns,
  burst[2,80], spread[10,220], scroll[.05,2], depth[0,1] · a scrolling 3D score: the spine follows
  `level`; each rising edge on `strike` sprays a vertical point-burst that recedes — hits accumulate
  into a plant-shaped graphic score.

Recipe (one lane, replicate ×3): `camera → vsensor(box on the subject) → onset`; `onset#gate → adsr`
of a voice (metal = `noiseosc→filter(bandpass)→adsr`); `vsensor → wave3d.level`, `onset → wave3d.strike`;
`scene` composites the feed + the score.

### Landmark tracking (Track, cat `Track`)
Each modality is a **Tracker TOP** (video in → video out with the overlay drawn on it; landmarks stashed)
+ a **Values reader CHOP** (multi-output). **Image-wire the tracker into the reader** (the reader has
`imgIns:1`). Hand/face/pose load a MediaPipe model on first cook (a few MB, once); object tracking is
colour-blob (no model). Every tracker has a `bg: video black` param — set `black` to draw the overlay on
black so you can `composite` it (screen/lighter) **over another node** (e.g. the hand skeleton over a `web`).

- `handtrack` (TOP · imgIns:1) — 2 hands × 21 pts, skeleton overlay · `handval` (CHOP, **imgIns:1**,
  outs `x y pinch spread fist dist touch`), param `hand`(1/2) · `#fist` = 1 when the fingertips curl to
  the palm (closed fist), 0 when open — a clean gesture trigger, distinct from `#pinch` (thumb–index)
- `facetrack` (TOP · imgIns:1) — 468-pt mesh + expressions · `faceval` (CHOP, imgIns:1, outs
  `x y mouth smile brow tilt`)
- `posetrack` (TOP · imgIns:1) — 33-pt body skeleton · `poseval` (CHOP, imgIns:1, outs `x y handsUp lean`),
  param `joint`(`rWrist lWrist rAnkle lAnkle nose`)
- `objtrack` (TOP · imgIns:1) — colour-blob, no model · hue[0,360], tol[5,90], sat[0,1], min px · draws a
  box round the blob · `objval` (CHOP, imgIns:1, outs `x y size present`)
- `web` (String Spiders, TOP · SOP) — 4 signal inputs `x1 y1 x2 y2` (two spiders) · legs[2,10],
  beads[4,22], reach[.1,.6], twist[0,8], walk[0,2], link[.02,.2] (Web dist), flow[0,2], depth[0,1], glow ·
  two spiders each spin spiral arms of beads (flowing outward via Walk) strung into a 3D mesh with radial
  legs from each core; Flow sends bright pulses walking along the strings; spider 1 is blue, spider 2
  pink — they warm to orange as they approach and fuse into a gold burst on contact (Touch = anchor dist).

Recipe (Hand Spiders): `camera → handtrack`; image-wire `handtrack →` two `handval`s (`hand:1`, `hand:2`);
`web.x1/y1/x2/y2 ← handval1#x/#y, handval2#x/#y`; `mod web.link by handval1#pinch`; `scene` = the hand-cam
overlay + the web. All the tracker signals mod any parameter — pinch a filter cutoff, lean a warp, etc.

## v2 nodes — round 8 (Shell Melody · grow an algo onto an item, in sync, and sonify it)

Draw an algorithmically-growing texture across an object over a timeline, and turn its evolving pattern
into a melody — one `transport` drives the growth **and** the sound.

- `shellca` (Shell CA, TOP · ALGO, cat `Cellular`) — no inputs · rule[0,255]=30 (Wolfram rule: 30=chaotic,
  90=Sierpinski, 110/…), cell[2,10], speed[0,60] (grow rate), hue, seed: `single random`, wrap: `on off` ·
  a **1D elementary cellular automaton** — the classic seashell "hieroglyphic" pattern, new rows added
  over time (the shell growing). Cream bands + a hue-tinted pattern.
- `reveal` (TOP, cat `Combine`) — 2 image inputs `item`, `pattern` · progress[0,1] (mod from a Transport
  phase → time-lapse growth), dir: `up down left right radial`, blend: `multiply overlay screen lighter
  source-over`, amount[0,1], soft[0,.5] · draws the pattern onto the item, unmasked progressively — the
  algo grows across the object. `multiply`/`overlay` sit it into a photo's surface; `source-over` overlays.
- `sonify` (CHOP · **imgIns:1**, multi-output `#pitch`/`#gate`/`#level`) — pos[0,1] (mod from a Transport
  to sweep the scanline), steps[2,32], read: `dark bright` · scans a vertical column of the wired image at
  Pos and reads its bands into a melody: `pitch` = where the pattern sits, `gate` = a note per Step,
  `level` = density. Wire `#pitch → osc.pitch`, `#gate → adsr.gate`, `#level → filter.cutoff`.

Recipe (Shell Melody): `transport` `tp`; an `image` (your shell photo) as the item + a `shellca` `ca`;
`reveal(item, ca)` with `progress ← tp` (blend `multiply` on a photo); `sonify(ca)` with `pos ← tp` →
`osc.pitch ← son#pitch`, `filter.cutoff ← son#level`, `adsr.gate ← son#gate` → reverb → audioout; a `scope`
on `son#pitch` for the time-graph; `scene` = waveform strip + the drawn-on shell. One clock, growth + melody.

## v2 nodes — round 9 (Magnetic Mastery · move a field with your hand)

A hand-driven magnetic / iron-filings flow field: the hand is a magnetic pole, fingertip distance sets the
pull, a closed fist fires a ripple. Uses the `#fist` output added to `handval` this round.

- `magfield` (Magnetic Field, TOP · SOP, cat `Particles`) — **4 signal inputs** `x y strength fist` · a
  field of iron-filings streaks flowing along a curl-noise field, with a **pole** at (x, y) that
  swirls / attracts / repels the filings around it. `strength` scales the pull; a rising `fist` (>0.6)
  fires a **ripple** outward from the pole. Feedback buffer for silky trails + a glow at the pole. Params:
  filings[1000,12000], flow[0,5], pull[0,3], field: `swirl attract repel`, trail[.7,.99], hue, tint[0,1].
  Wire a hand: `x/y ← handval#x/#y`, `strength ← handval#spread` (fingertip distance), `fist ← handval#fist`.

Recipe (Magnetic Mastery): `camera → handtrack → handval`(`hand:1`); `magfield` with `x/y ← h#x/#y`,
`strength ← h#spread`, `fist ← h#fist` — move your hand to steer the whorl, spread your fingers to pull
harder, close a fist to send a ripple. Audio: a `noiseosc`(pink) → `filter`(bandpass) → `reverb` →
`audioout` particle drone, `mod noiseosc.level` **and** `filter.cutoff` by `h#spread` (fingertip distance →
volume + brightness), `mod reverb.mix` by `h#fist` (a fist swells the ripple's reverb). `scene` = the field
big with a live-cam inset. One hand drives the field **and** its voice.
