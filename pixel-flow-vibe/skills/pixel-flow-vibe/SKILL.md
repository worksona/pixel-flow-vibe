---
name: pixel-flow-vibe
description: Vibe-code the Pixel Flow apps from natural language. Given a described look ("glitchy VHS grid pulsing to a kick", "a patch where my hand bends a particle field", "dreamy kaleidoscope morphing slowly"), author a Pixel Flow config — a Nodes v2 graph or a Studio zone/sequencer state — encode it into a shareable #cfg= URL the app auto-applies on load, and hand back a clickable link. Trigger on /pixel-flow-vibe, or when the user asks to generate / share / remix a Pixel Flow look, patch, graph, scene or preset, or to turn a mood/song/image into a Pixel Flow config.
---

# Pixel Flow Vibe

Turn a natural-language description into a **Pixel Flow config**, encode it into a **share URL**, and
give the user a clickable link that opens the app with the look already running.

Repos: app **worksona/pixel-flow** (`/Users/davidolsson/WORKSONA/pixel-flow`) · this skill
**worksona/pixel-flow-vibe**. Live site: **https://pixel-flow.atomic47.co**.

## Pick a target — Nodes v2 is the default

| Target | When | Schema | Encode |
|---|---|---|---|
| **Nodes v2** *(default)* | Anything graph/patch/dataflow shaped, and anything needing 3D, particles, tracking, scenes, or the modular synth rack. This is the **deployed** Nodes app. | `reference/schema-nodes-v2.md` | `--nodes --live` (or `--nodes --dev`) |
| **Studio** | Zone-based looks: marquee regions with stacked effectors, LFOs, a 64-step sequencer + synth, songs, scenes. Reach for it when the ask is "a look / a song / a beat-reactive scene" rather than a signal chain. v2 has **no Studio equivalent**, so Studio is still current. | `reference/schema-studio.md` | *(no flag)* |
| **Nodes v1** *(legacy)* | Only when the user explicitly wants the old single-file `v1/pixel-flow-nodes.html`. | `reference/schema-nodes-v1.md` | `--nodes` (bare) |

**Read the matching schema file FIRST, every run.** Never invent operator, effector, or param names —
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
   ids. Studio canvas is 814×768; Nodes are ~200px wide, ~220px apart horizontally, rows ~280px apart.
4. **Encode.** Write the JSON to a temp file and run:
   ```
   python3 ~/.claude/plugins/marketplaces/pixel-flow/pixel-flow-vibe/skills/pixel-flow-vibe/scripts/encode.py /tmp/pf-vibe.json --nodes --live
   ```
   Flags: `--nodes` targets the graph app · **`--live`** points at the deployed site (**Nodes there is
   v2**) — use this for any link someone else will open · `--dev` targets the local nodes-v2 vite server
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

## Vibe → effector translation

Compose per zone; stacking a few reads better than one.

- **glitchy / broken / datamosh** → `glitch` `vhs` `rgb` `slice`(sliceMode shift/wave) `sort` `pixel`; high `random`, `glitchAmt`; route `Snare→glitch` and put glitch hits on the Glitch lane.
- **dreamy / ethereal / soft** → `kaleido` `bloom` `echo` `feedback` `flow`; low bpm, `hueSpeed` small, opacity <1, slow LFO on `kaleido`/`scale`.
- **retro TV / VHS / analog** → `vhs` `scan` `colormtx`(cmat acid|cool) `dither`; grain up, vignette up.
- **kaleidoscopic / mandala / symmetry** → `kaleido` or `wallpaper`(wallMode p4/pmm) + `affine` (Droste), motion `orbit`.
- **liquid / melting / flowing** → `field` `ripple` `melt` `wave` `flow`; LFO on `fieldAmt`/`melt`.
- **tiled / mosaic / grid** → `mosaic` with `cols`/`rows`, and pick a `tileFlow` (`lr` `rl` `ud` `du` `diag` `scroll` `radial` `swirl`) and `tileMode` (`brick` `diamond` `mirror` `rot4`). This is the headline tiling control — use it.
- **neon / edges / vector** → `edges` `hue`(hueSpeed) `bloom` `echo`.
- **psychedelic / vortex** → `twist` `tunnel` `kaleido` `czoom`, motion `spiral`.
- **matrix / code / kernel** → `convolve`(emboss/edge, or custom kernel) `colormtx` `dither` `posterize`.

Motion/energy:
- Beat-reactive → set a punchy `seq` (Kick on 1/5/9/13), raise the relevant `ui.mod` amounts (Kick→offset, Bass→flow), add `strobe` for kick flashes.
- Continuous motion → LFOs (`rate` 0.1–1, `depth` 0.3–0.6) and per-zone `motion` (`drift` `orbit` `dvd`).
- Slow/meditative → bpm 70–96, gentle LFOs; Fast/aggressive → bpm 140–170, dense seq, `shake`.

Layout:
- One fullscreen zone (0,0,814,768) for a single unified look.
- A 2×2 / 3×3 grid of zones (each ~407×384 / 271×256) with contrasting effectors for variety.
- Horizontal bands (full width, stacked) for scan/slice looks; vertical bands for columns.

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

## Example config (glitchy VHS grid pulsing to a kick)

```json
{
  "ui": { "bpm": 140, "swing": 0.08, "mod": { "Kick":180, "Snare":70, "Bass":50 } },
  "state": {
    "bpm": 140,
    "zones": [
      { "id":"g", "name":"Grid", "shape":"rect", "x":0,"y":0,"w":814,"h":768,
        "enabled": { "mosaic":true, "rgb":true, "vhs":true, "glitch":true, "scan":true },
        "fx": { "cols":6, "rows":6, "tileMode":"brick", "tileFlow":"scroll",
                "offset":90, "glitchAmt":34, "vhsAmt":16, "scan":7, "rgb":18 },
        "lfos": [ { "on":true, "target":"offset", "wave":"noise", "rate":0.6, "depth":0.4 } ] }
    ],
    "seq": {
      "Kick":  [1,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0],
      "Snare": [0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0],
      "Hat":   [0,0,1,0,0,0,1,0,0,0,1,0,0,0,1,0],
      "Glitch":[0,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0]
    },
    "global": { "grain":0.14, "vignette":0.4, "strobe":0.25 }
  }
}
```
