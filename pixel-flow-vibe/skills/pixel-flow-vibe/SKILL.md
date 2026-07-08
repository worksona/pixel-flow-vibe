---
name: pixel-flow-vibe
description: Vibe-code the Pixel Flow Studio visual/audio-reactive app from natural language. Given a described look ("glitchy VHS grid pulsing to a kick", "dreamy kaleidoscope morphing slowly"), author a Pixel Flow config JSON, encode it into a shareable #cfg= URL that the app auto-applies on load, and hand back a clickable link. Trigger on /pixel-flow-vibe, or when the user asks to generate / share / remix a Pixel Flow look, scene, or preset, or to turn a mood/song/image into a Pixel Flow config.
---

# Pixel Flow Vibe

Turn a natural-language description of a visual into a **Pixel Flow config**, encode it into a
**share URL**, and give the user a clickable link that opens the app with the look already loaded.

## Two target apps — pick one per request

1. **Studio** (`/Users/davidolsson/Desktop/pixel-flow/pixel-flow-studio-pro.html`) — zone-based: marquee
   regions with stacked effectors, LFOs, a 64-step sequencer + synth, songs, scenes. Schema:
   `reference/schema.md`. Default choice for "a look / a song / beat-reactive scene".
2. **Nodes** (`/Users/davidolsson/Desktop/pixel-flow/pixel-flow-nodes.html`) — TouchDesigner-style dataflow
   graph: TOP image operators wired output→input, CHOP signals modulating parameters. Schema:
   `reference/schema-nodes.md`. Choose when the user says nodes/graph/patch/dataflow, wants explicit
   signal-flow chains (source → filter → feedback → output), or asks to vibe the node app. Encode with
   `--nodes`.

Read the matching schema file FIRST, every run.
Codec (both apps): `scripts/encode.py` — JSON config → `#cfg=` URL (and `--decode` back).

## Workflow

1. **Read `reference/schema.md`** to ground yourself in the current vocabulary (39 effectors, param ranges, enums). Never invent effector/param names — only use ones listed there.
2. **Interpret the vibe.** Map the user's words to: a zone layout, a set of enabled effectors per zone, a few param overrides, LFO motion, a **64-step sequencer** pattern (optionally a 5-song set), tempo, and global post FX. Lean on the translation guide below. A "song" vibe = author `state.seq` (64-step lanes) + `bpm` + `swing`, and optionally a `state.songs` library of 5 distinct patterns (intro/main/breakdown/drop/outro).
3. **Author the config JSON.** Keep it minimal — only set what matters; defaults fill the rest. Give zones unique ids. Canvas is 814×768.
4. **Encode.** Write the JSON to a temp file and run:
   ```
   python3 ~/.claude/skills/pixel-flow-vibe/scripts/encode.py /tmp/pf-vibe.json
   ```
   It prints a `file://…#cfg=<base64>` URL. Flags: `--nodes` targets the node-graph app; **`--live`** points at the **deployed site `https://pixel-flow.atomic47.co`** (default when you want a link someone else can open); `--base https://host/app.html` for any other host; `--code` emits just the paste-able code; `--kiosk` appends `&view=viewer` so it opens as a fullscreen output-only **experience** (a tiny ✎ chip returns to the editor). Prefer `--live --kiosk` for a "send someone the finished piece" link.
5. **Deliver.** Give the user:
   - the clickable share URL (opens the app with the look live), and
   - a one-line description of what you built, plus 2–3 knobs they can ask you to tweak.
   Mention they can also open the app's **Share ▾ → Load Config** and paste the raw JSON or the code.
6. **Iterate.** On follow-ups, patch the previous config (keep it in the conversation) and re-encode. Small deltas — change a tileFlow, add an LFO, swap a color matrix — not a rewrite.

Optionally open it: only if the user asks, open the URL in their browser.

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

- Only use effector keys, param names, and enum values from `reference/schema.md`. Respect the `[min,max]` ranges.
- Keep configs partial and minimal; don't emit every default.
- Set `src` when the look needs a live/embedded source: `src.cam` (webcam texture), `src.mic` (FFT-reactive), `src.image` (embedded still, bloats the URL — only when the picture matters). `cam` and `image` are mutually exclusive; `mic` combines with either. On open the app requests cam/mic on the user's first tap. Use `encode.py --cam/--mic/--image` or author `src` directly. Default: no `src` (uses the app's demo texture).
- Prefer `file://` links to the local app unless the user says it's hosted.
- If the user pastes an existing `#cfg=` URL or code, decode it first (`encode.py --decode`) to remix from their current look.

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
