---
name: pixel-flow-studio-vibe
description: Vibe-code Pixel Flow Studio, the zone-based visual instrument, from natural language. Given a described look ("glitchy VHS grid pulsing to a kick", "slow dreamy orbs drifting over a liquid bed", "a broadcast TV wall for a techno set"), compose a whole screen — a layout of zones, a preset and motion per zone, a groove, mod-matrix amounts and post FX — validate it against the Studio vocabulary, encode it into a share link that opens the look running (optionally fullscreen kiosk), and hand back the link plus the knobs to turn next. Trigger on /pixel-flow-studio-vibe, or when the user asks for a Studio look, scene, screen, recipe, zone layout, VJ visual, beat-reactive visual, or to remix a Studio share link. Also themed looks: a style (film noir, Technicolor, Super 8, neon noir, VHS horror, techno, ocean, Halloween, keynote…) times a pattern (trailer cuts, slow burn, split reel, montage, opening titles…), movie-clip looks, title cards and widescreen. For node-graph patches (3D, particles, tracking, synth rack) use /pixel-flow-vibe instead.
---

# Pixel Flow Studio Vibe

Turn a sentence into a **whole Studio screen** and a link that opens it running.

App: `apps/studio/pixel-flow-studio-pro.html` in **worksona/pixel-flow** · live at
`https://pixel-flow.atomic47.co/pixel-flow-studio-pro.html`.

## How Studio thinks (read once)

- The canvas is **814 × 768**, or **1280 × 720** with `--wide` (`ui.stage: "wide"`). A look is a stack of **zones** (back to front). Each zone is a
  shape (rect · ellipse · ring · lasso) that re-renders the source under it through a stack of
  **effectors** (59 of them, including generators: Life, Reaction Diffusion, Mandelbrot, Voronoi, Particles…), animated by **LFOs** and a **motion** that moves the zone itself.
- A **preset** is one zone's effector stack + LFOs (48 of them, e.g. `glitch`, `dream`, `vhs`, `conway`, `glass`, `motionmap`).
- A **recipe** is a whole screen: a **layout** of zones × a preset and motion per zone × BPM,
  groove, mod-matrix and post FX. 56 stock recipes ship in the app (`reference/recipes.md`).
- A **style** is a whole-screen look (grade, letterbox, film grain, dust, halation, palette); a **pattern** is
  layout + timing (cuts, holds, push-ins). **recipe = pattern × style × source.** Themes group them:
  Movie, Music, Nature, Ambient, Occasions, Stage (`reference/themes.md`, `encode.py --list`).
- A 64-step **sequencer** (Kick Snare Hat Bass Glitch Morph Visual) drives a small synth and,
  through the **mod matrix**, punches visual params on each hit. Mic FFT can do the same.

## Workflow

1. **Read `reference/schema.md`, `reference/recipes.md` and `reference/themes.md` every run.** Never invent an
   effector, preset, param, enum value, layout or recipe id. Respect ranges.
2. **Decide: stock recipe, themed look, or authored look.**
   - The ask matches a stock recipe closely ("dreamy kaleidoscope", "DVD bouncing tiles") →
     link the recipe: `encode.py --recipe mandala --live --kiosk --short`. Shortest link, nothing to get wrong.
   - The ask names a mood, genre, era, film or occasion ("noir", "70s horror trailer", "Super 8 home movie",
     "synthwave", "Halloween", "background for my talk") → a **themed look**: pick a style and a pattern from
     `reference/themes.md` and encode them, no zones needed:
     `encode.py --style noir --pattern slowburn --presets ghost --title "…" --live --kiosk --compress --short`.
     Iterate by swapping one of them ("same, but Technicolor" = change `--style` only).
   - A style also goes on top of an authored look: add `"theme": {"style": "super8"}` to the config.
   - Otherwise author a config (step 3). Start from the nearest recipe's spirit.
3. **Author the smallest config that says it.** Use the shorthands — they keep configs short
   and readable, and the encoder expands them:
   - `state.layout` = `{"name": "<layout>", "args": [...], "slots": [<zone template>, ...]}`.
     Slots repeat round-robin over the layout's cells. Use it for anything grid-, band-,
     wedge- or orbit-shaped.
   - `zone.preset` = start from a preset; the zone's own `enabled` / `fx` / `lfos` override it.
   - `zone.motion` = shorthand for `fx.motion`.
   - Extra zones in `state.zones` stack **in front of** the layout (good for a picture-in-picture,
     a floating ring, a bouncing tile).
4. **Validate, then encode.** Write the JSON to a temp file:
   ```bash
   python3 "$CLAUDE_PLUGIN_ROOT/skills/pixel-flow-studio-vibe/scripts/encode.py" /tmp/look.json --check
   python3 "$CLAUDE_PLUGIN_ROOT/skills/pixel-flow-studio-vibe/scripts/encode.py" /tmp/look.json --live --kiosk --compress --short
   ```
   Fix every `warn:` before handing over a link (an unknown name is silently dropped by the app).
   If `$CLAUDE_PLUGIN_ROOT` is unset, use the path of this skill folder.
5. **Title it.** Every `--kiosk` link opens on a landing page, so give the config a `title` (and
   a one-line `about` saying what to watch or listen for); the encoder warns when it's missing.
6. **Deliver**: the clickable link (the a47l.com short link from `--short`; if it warns that
   shortening was unavailable, hand over the full link it printed instead), one line on what's on screen, and 2–3 knobs to ask for next
   ("faster", "more glitch on the snare", "make the orbs bigger"). Mention **⌘K** and **?** in
   the app, and that **C** copies a share link of whatever they tweak.
7. **Iterate** by patching the previous JSON (keep it in the temp file) and re-encoding. Small
   deltas: retune a param, swap a preset, change a motion, change the layout. If the user pastes
   a Studio link, run `encode.py --decode '<link>'` first and remix from that.

### Encoder flags

| flag | effect |
|---|---|
| `--live` | link to the deployed site (use for anything someone else opens) |
| `--local` | `file://` link to your checkout (`$PIXEL_FLOW_REPO`, default `~/WORKSONA/pixel-flow`) |
| `--base URL` | any other host, e.g. a local server |
| `--kiosk` | open fullscreen, output only — "send someone the finished piece" |
| `--recipe ID` | link a stock recipe instead of a config |
| `--compress` | `#cfgz=` deflate link, ~half the length (Studio 2 only) |
| `--style ID` `--pattern ID` `--presets a,b` | a themed look with no config file; `--list` shows the ids |
| `--title TEXT` | name the look (the kiosk landing card shows it) |
| `--wide` | widescreen 1280×720 stage; geometry is checked against it |
| `--short` | also make an **a47l.com** short link through the site's shortener (needs `--live`; prints the full link and a warning if shortening is unavailable). Use it for every link someone else opens: short links fit any QR code and survive chat apps |
| `--cam` `--mic` `--image f.jpg` | source the link opens with (cam/mic arm on first tap) |
| `--check` / `--expand` / `--code` / `--decode` | validate · print expanded JSON · base64 only · link → JSON (a47l.com links are followed first) |

### Studio 2

The live site runs Studio 2: inspector tabs, recipes, direct manipulation, the `wander` /
`swing` / `fig8` motions, `#recipe=` and `#cfgz=` links, hidden zones, and `perform` (scene
cycling, song chains and autopilot that start when a link opens). Everything in this skill works
with `--live`. A downloaded copy of the older single-file Studio ignores these features.

## Vibe → screen

Pick the **layout** from the shape of the ask, the **presets** from its texture, the **motion**
from its energy, the **groove + BPM** from its tempo.

**Layout** (see `reference/recipes.md` for geometry):
- one unified image, a single statement → `full`
- contrast, a wall of screens, "grid" → `grid2` / `grid3` / `grid4`
- scan, stripes, horizon → `bands` (args `[n]`) · columns, rain, bars → `cols`
- radial, mandala, wheel → `wedges` · broken, shards, glass → `shatter`
- a hero with a background → `ringCenter` · TV with an inset → `pip` · editorial → `thirds`
- things moving around, playful → `scatter` (args `[n, "ellipse"]`) · planets, moons → `orbiters`

**Texture → presets:**
- glitchy, broken, datamosh → `glitch` `sortstorm` `vhs` `matrixtv`
- dreamy, soft, ethereal → `dream` `pulse` `lumen` `ghost` (+ `feather` 15–35, `blend: screen`, `opacity` < 1)
- retro TV, VHS, analog → `vhs` `matrixtv` `riso`; grain up, vignette up
- kaleidoscopic, mandala → `dream` `vortex` `droste` `escher`
- liquid, melting, organic → `liquid` `melt` `prism`
- printed, zine, poster → `halftone` `riso` `emboss` `ascii`
- neon, vector, club → `neon` `lumen` `tunnel`
- woven, textile, pixel → `fabric` `tiles`
- infinite, tunnel, falling → `tunnel` `droste`

**Energy → motion, BPM, groove:**
- still / meditative → motion `none` or `drift` (motionAmt 10–25, motionSpeed 0.2–0.4), BPM 70–92, groove "Slow pulse"
- floating / organic → `wander` (Studio 2) or `drift`, `swing` for pendulums
- circling / hypnotic → `orbit`, `spiral`, `fig8` (Studio 2)
- playful → `dvd`, `bounce`
- aggressive / punchy → `shake` (motionAmt 8–16), BPM 140–170, grooves "Techno" / "Breakbeat",
  `global.strobe` 0.2–0.45, mod `Kick` 180–260, `Snare` 60–110

**Long-form / "an experience" / "a set" / "something that evolves"** — build sections, not a
single frame (`reference/schema.md` → Scenes, Songs, Perform):
1. Author the zones once (scene A), then 2–3 more scenes as overrides: move and resize the hero
   zones, swap presets on groups (`"Glitch*": {"preset": "vhs"}`), shift hues, drop opacity for a
   breakdown, blow a zone up for a peak.
2. Write 3–5 songs (intro, main, breakdown, build, drop) with different BPMs and densities.
3. `perform`: `cycle` with `holdBars` 3–8 and `blendBars` 1–4, a `chain` through the songs with
   `chainLoop`, and a light `autopilot`. Make the scene cycle and the chain different lengths.
4. Hand back the `--kiosk` link as the piece and the plain link as "open in editor".

**Ambient / calm / "show the sequencing"** — readable beats on smooth imagery
(`reference/example-tide-clock.json`):
- Use a **clean source**: the default demo texture is busy (red blocks and scribbles). Embed a soft
  gradient with `--image` — `scripts/nightsea.py out.png` writes a 6 KB night-sea one, or bring any
  calm photo. Grain ≤ 0.05, strobe 0, no autopilot.
- On smooth imagery, **displacement is invisible** (shifting a gradient changes nothing). Lanes read
  only through effects that change *brightness*. Give each lane one home:
  | lane | effect that shows it | where |
  |---|---|---|
  | Kick | `bloom` (bloomAmt 1: glow 0.6→1.0 on each hit) | a small bright zone, e.g. an `invert`ed moon disc |
  | Hat | `scan` (line alpha jumps on each hit) | a feathered band, scan 14–20, opacity 0.7–0.9 |
  | Bass | `flow` at flow 2–4 (24 tiny dashes brighten) | a dark sky band — reads as stars twinkling |
  | Morph | flips scene A↔B with a ~1 s ease | move/resize the hero zone between A and B |
  Avoid `field`, `wave`, `ripple`, `echo` for this job: on gradients they do little, and `field` leaves
  square seams.
- Set `ui.mod` to 0 so nothing else reacts, and introduce one lane per song so the viewer learns the
  mapping: bass alone → + kick → + hats → denser → back to one.

**Movies and video** — "make my clip look like…": build a themed look from the Movie theme and tell the user
to import the clip with **⌘I** once the link opens (a link cannot carry a video). The clip plays with sound and its
soundtrack drives the visuals. Use `--wide` so recordings come out 1280×720. **J** plays / pauses, ⌥[ ⌥] set a loop.

**Title cards** — `theme.titles` (or `state.titles`): `{"lines": ["Main title|subtitle", "…"], "pos": "center"}`; one line
shows per hold, inside the letterbox. The `opening` pattern turns titles on.

**Hard cuts** — `perform.blendBars: 0` cuts between scenes instead of blending (the `trailer` pattern does this).

**Beat-reactive**: set `seq` (or say which groove), raise `ui.mod` amounts, add `global.strobe`.
**Mic-reactive**: add `--mic` and raise `ui.mod.Low` / `Mid` / `High`.
**Camera as the source**: add `--cam`; effectors then remix the live camera.

## Rules

- Names come only from `reference/schema.md` and `reference/themes.md`. Run `--check`; zero warnings before delivering.
- Keep zones to 1–16 (24 at most). Rich looks come from 2–4 effectors per zone, not 10.
- Every zone needs at least one effector, or it just shows the source.
- Hand back links, not JSON, unless asked. Open the link in a browser only if asked.

## Examples

Three full long-form pieces live next to the schema:
`reference/example-cathedral-of-hours.json` (meditative, 4 scenes, 70–88 BPM),
`reference/example-signal-riot.json` (club, 4 scenes, 120–156 BPM) and
`reference/example-tide-clock.json` (ambient, one lane per element, Morph-lane tide; encode it
with `--image reference/nightsea.png`). Start from one when the ask is an
experience rather than a single look.

**"slow dreamy orbs drifting over a liquid bed"**
```json
{"state":{"bpm":84,
  "layout":{"name":"full","slots":[{"preset":"liquid","fx":{"hue":200,"hueSpeed":0.5}}]},
  "zones":[
    {"preset":"dream","shape":"ellipse","x":90,"y":120,"w":260,"h":260,"motion":"drift","fx":{"motionAmt":40,"motionSpeed":0.3,"feather":28,"blend":"screen"}},
    {"preset":"lumen","shape":"ellipse","x":470,"y":380,"w":220,"h":220,"motion":"orbit","fx":{"motionAmt":30,"motionSpeed":0.25,"feather":24,"blend":"screen"}}],
  "global":{"grain":0.08,"vignette":0.5,"feedback":0.15}},
 "ui":{"mod":{"Bass":40,"Low":140}}}
```

**"glitchy 3×3 VHS wall that punches on the kick"**
```json
{"state":{"bpm":140,
  "layout":{"name":"grid3","slots":[{"preset":"glitch","motion":"shake","fx":{"motionAmt":10}},{"preset":"vhs"},{"preset":"matrixtv"}]},
  "seq":{"Kick":[1,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0],"Snare":[0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0],"Glitch":[0,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0]},
  "global":{"strobe":0.25,"grain":0.14,"vignette":0.4}},
 "ui":{"mod":{"Kick":220,"Snare":80}}}
```
