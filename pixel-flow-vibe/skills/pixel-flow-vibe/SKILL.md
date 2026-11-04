---
name: pixel-flow-vibe
description: Vibe-code Pixel Flow Nodes, the node-graph app, from natural language. Given a described look ("a patch where my hand bends a particle field", "dreamy kaleidoscope morphing slowly", "glitchy datamosh pulsing to a kick"), author a Nodes v2 graph, encode it into a shareable #cfg= URL the app auto-applies on load, and hand back a clickable link. Trigger on /pixel-flow-vibe, or when the user asks to generate / share / remix a Pixel Flow Nodes patch, graph, scene or preset, or to turn a mood/song/image into a node graph. For Pixel Flow Studio looks (zones, effectors, sequencer, whole-screen recipes) use /pixel-flow-studio-vibe instead.
---

# Pixel Flow Vibe

Turn a natural-language description into a **Pixel Flow Nodes graph**, encode it into a **share URL**, and
give the user a clickable link that opens the app with the look already running.

Source: `skills/pixel-flow-vibe/` in **worksona/pixel-flow** (the app repo; `$PIXEL_FLOW_REPO`, default
`~/WORKSONA/pixel-flow`), published to the **worksona/pixel-flow-vibe** marketplace. Live site: **https://pixel-flow.atomic47.co**.

## Pick a target — Nodes v2 is the default

| Target | When | Schema | Encode |
|---|---|---|---|
| **Nodes v2** *(default)* | Anything graph/patch/dataflow shaped, and anything needing 3D, particles, tracking, scenes, or the modular synth rack. This is the **deployed** Nodes app. | `reference/schema-nodes-v2.md` | `--nodes --live` (or `--nodes --dev`) |
| **Nodes v1** *(legacy)* | Only when the user explicitly wants the old single-file `legacy/nodes-v1/pixel-flow-nodes.html`. | `reference/schema-nodes-v1.md` | `--nodes` (bare) |

**Studio is not this skill's target.** For zone-based Studio looks (marquee regions, stacked effectors,
the sequencer, whole-screen recipes) use **`/pixel-flow-studio-vibe`**, the other plugin in this marketplace.

**Read the matching schema file FIRST, every run.** Never invent operator or param names —
only use what the schema lists, and respect its `[min,max]` ranges.

### What v2 adds over v1

v2 is a strict superset — same `#cfg=` codec, same node object, plus, across rounds 1–13 of
`reference/schema-nodes-v2.md`: signal ops (Beat Clock, Envelope, Random Walk, Smoother, Remap, Logic,
Step Seq); geometry/particle/3D ops (Grid, Point Cloud, Particle Field, Instancer, Voronoi, Truchet,
Spirograph, **Render 3D**, Points 3D, Terrain 3D); algorithmic sources (CA, fractals, L-system, CPPN,
De Jong); DAT data/text ops; **Scene & Timeline** (scene compositor, transport, media bank, HUD, scope);
**vision→control** (hand/face/body/object tracking, video sensor, onset); **Shell Melody** (shell CA,
reveal, sonify); and a full **modular synth rack** — Oscillator / Wavetable Osc (its wavetable is an
image) / Noise / Filter / ADSR / VCA / Duck / Delay / Reverb / Sample & Hold / Mixer 4ch / Compressor /
Audio Out, driven by Pattern Seq, Chords, Clock Divide, Quantizer, Attenuvert, Quad LFO, CV Mixer, Slew,
Bernoulli and Drum voices, with a lookahead scheduler for sample-accurate timing.

## Workflow

1. **Read the schema** for the chosen target (table above). Ground yourself in the current vocabulary.
2. **Interpret the vibe** using the translation guides below.
3. **Author the config JSON.** Keep it minimal — set only what matters; defaults fill the rest. Unique
   ids. Nodes are ~200px wide, ~220px apart horizontally, rows ~280px apart.
4. **Encode.** Write the JSON to a temp file and run:
   ```
   python3 ~/.claude/plugins/marketplaces/pixel-flow/pixel-flow-vibe/skills/pixel-flow-vibe/scripts/encode.py /tmp/pf-vibe.json --nodes --live
   ```
   Flags: `--nodes` targets the graph app · **`--live`** points at the deployed site (**Nodes there is
   v2**) — use this for any link someone else will open · `--dev` targets the local Nodes v2 vite server (`apps/nodes`)
   at `localhost:5173` · `--base https://host/app.html` for any other host · `--code` emits just the
   paste-able code · `--kiosk` appends `&view=viewer` for a fullscreen output-only **experience** (a tiny
   ✎ chip returns to the editor) · `--cam` / `--mic` / `--image path.jpg` set the source. Prefer
   `--live --kiosk` for "send someone the finished piece".
5. **Deliver.** Give the user the clickable share URL, a one-line description of what you built, and
   2–3 knobs they can ask you to tweak. Mention they can also open **Share ▾ → Load Config** in-app and
   paste the raw JSON or the code.
6. **Iterate.** On follow-ups, patch the previous config and re-encode. Small deltas — retune a param,
   add an LFO, swap one operator — not a rewrite.

Open the URL in their browser only if they ask.

## Vibe → Nodes v2 translation

Build a **chain**, then modulate it. A readable patch is: source → 1–3 filters → feedback → output,
with CHOPs hanging below driving params via `mods`.

- **source** — `noise` / `camera` / `image` for a texture; `cppn` `dejong` `fractal` `lsystem` `ca` for
  something algorithmic and self-generating; `grid` `voronoi` `truchet` for structure.
- **filters** — `kaleido` `twist` `tunnel` `ripple` `melt` `edges` `glitch` `vhs` for the look; stack 2–3,
  not 8.
- **motion** — `feedback` (decay ~0.9, zoom ~1.02) is the single highest-value node for "alive"; add it
  before the output on almost anything ambient.
- **beat** — `audio` CHOP (set `src.mic`) or `bclock`; route through `env`/`smooth` into `mods` so hits
  land as swells rather than jitter.
- **hands / body** — the tracking ops emit CHOP signals; `mods` them onto a field, particle or 3D param.
  This is the strongest "wow" in v2 — reach for it when the user mentions hands, gesture, or presence.
- **3D / depth** → `render3d` with `points3d` or `terrain3d` upstream.
- **sound** → the rack: a voice (`osc`/`wtosc`/`noise`) → `filter` → `vca` (gated by `adsr`) → `mixer` →
  `audioout`, clocked by `patternseq` and pitched by `chords`/`quantizer`.

Only numeric params modulate. `mods` is `base + chopValue × depth` (chop ≈ −1..1; audio bands 0..1).

## Rules

- Only use keys, param names and enum values from the schema you read. Respect `[min,max]`.
- Keep configs partial and minimal; don't emit every default.
- Set `src` when the look needs a live source: `src.cam` (webcam texture), `src.mic` (FFT-reactive),
  `src.image` (embedded still — bloats the URL, only when the picture matters). `cam` and `image` are
  mutually exclusive; `mic` combines with either. The app requests cam/mic on the user's first tap.
- Default to **`--live`** for Nodes: it serves v2, so every operator resolves. A bare `file://` Nodes link
  opens **v1** and will silently drop v2-only node types.
- If the user pastes an existing `#cfg=` URL or code, decode it first (`encode.py --decode`) and remix
  from their current look rather than starting over.

## Example graph (glitchy datamosh)

Noise → glitch → pixel sort → RGB shift → output, with an LFO swelling the glitch amount. Encode with
`--nodes --live`.

```json
{
  "viewId": "out",
  "nodes": [
    { "id":"src", "type":"noise",    "x":20,  "y":60,  "params": { "hue":120, "speed":2 } },
    { "id":"gl",  "type":"glitch",   "x":260, "y":50,  "params": { "amount":40, "blocks":12 }, "imgInputs":["src"],
      "mods": [ { "src":"lfo", "param":"amount", "depth":30 } ] },
    { "id":"so",  "type":"sort",     "x":500, "y":50,  "params": { "th":0.42 }, "imgInputs":["gl"] },
    { "id":"rgb", "type":"rgbshift", "x":740, "y":50,  "params": { "amount":20, "angle":90 }, "imgInputs":["so"] },
    { "id":"out", "type":"output",   "x":980, "y":60,  "imgInputs":["rgb"] },
    { "id":"lfo", "type":"lfo",      "x":260, "y":340, "params": { "shape":"tri", "rate":0.4 } }
  ]
}
```
