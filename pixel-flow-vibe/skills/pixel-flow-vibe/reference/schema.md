# Pixel Flow config schema (authoritative)

A config is JSON. Top level:

```json
{
  "v": 1,
  "type": "pixel-flow-config",
  "ui":    { "bpm": 128, "swing": 0.08, "morphCurve": "smooth",
             "mod": { "Kick":140,"Snare":40,"Hat":18,"Bass":30,"Low":160,"Mid":55,"High":32,"Amp":0 } },
  "state": { "bpm":128, "seed":17, "zones":[ ... ], "seq":{ ... }, "global":{ ... }, "scenes":{ ... } },
  "src": { "cam": true, "mic": true, "image": "data:image/jpeg;base64,..." }  // OPTIONAL source, see below
}
```

## `src` — what feeds the engine (optional)

`src` controls the texture/audio source the shared link opens with:
- `"cam": true` — the app requests the **webcam** on open (used as the source texture).
- `"mic": true` — the app requests the **mic** on open (FFT drives the Mod Matrix / LFOs).
- `"image": "data:image/...;base64,..."` — embeds a still image as the source. Bloats the URL; use only when the picture matters.

Camera/mic can't auto-start without a user gesture, so on open the app shows a "Tap / click to enable camera + mic" hint and starts them on the first interaction. `cam` and `image` are mutually exclusive (camera wins). `mic` is independent and combines with either. (Legacy configs may use a top-level `"source": "data:..."` string — still honored as `src.image`.)

Encode these with `encode.py --cam`, `--mic`, `--image path/to.jpg` (or author `src` directly in the JSON).

`state` is merged over the running app state (`Object.assign`), so **partial is fine** — you usually only send `zones`, and optionally `seq`, `global`, `bpm`. Every zone is passed through `ensureZoneShape`, which fills all `fx`/`enabled`/`lfos` defaults, so a zone only needs geometry + the handful of `enabled` flags + `fx` overrides you care about.

## Zone

```json
{ "id":"z1", "name":"Zone 1",
  "shape":"rect",              // rect | ellipse | ring | lasso
  "x":0, "y":0, "w":814, "h":768,   // canvas is 814 x 768
  "points":[[0,0],[1,0],[0.5,1]],   // ONLY for shape:"lasso" — normalized 0..1 polygon
  "enabled": { "mosaic":true, "rgb":true },     // which effectors are ON (all others default false)
  "fx": { "cols":8, "rows":8, "tileFlow":"swirl", "offset":120 },  // param overrides (see below)
  "lfos": [ {"on":true,"target":"offset","wave":"sine","rate":0.4,"depth":0.4}, ... ]  // optional, up to 3
}
```

- Give each zone a unique `id`. Canvas is **814 wide, 768 tall**.
- `ring` uses `fx.innerR` (0.05..0.9) for the hole; `lasso` uses `points`.

## Effectors (`enabled` keys) — 39 total, grouped

- **Tiling**: `mosaic` `wallpaper` `affine` `kaleido` `mirror` `weave`
- **Slicing**: `slice` `timeslice` `scan`
- **Displace**: `flow` `wave` `ripple` `field` `displace` `smear` `melt`
- **Warp**: `twist` `tunnel` `czoom`
- **Glitch**: `glitch` `vhs` `rgb` `sort` `pixel`
- **Color**: `hue` `invert` `posterize` `threshold` `solar` `colormtx` `dither`
- **Stylize**: `dot` `ascii` `edges` `bloom` `convolve`
- **Feedback**: `feedback` `echo` `clone`

## fx params + ranges `[min, max]`

Structure: `cols`[1,32] `rows`[1,32] `slices`[2,80]
Displace: `offset`[0,360] `random`[0,320] `shuffle`[0,1]
Warp: `waveAmp`[0,80] `waveFreq`[0.01,0.3] `twist`[-4,4] `rippleAmt`[0,40] `rippleFreq`[0.01,0.2] `melt`[0,60] `fieldAmt`[0,50] `fieldScale`[8,64]
Break: `glitchAmt`[0,80] `vhsAmt`[0,40] `smear`[0,60] `smearAng`[0,6.3] `pix`[2,64]
Matrix: `convAmt`[0,1] `cmix`[0,1] `iter`[1,12] `mtxScale`[0.5,0.99] `mtxRot`[-1.2,1.2] `mtxDx`[-60,60]
Texture: `weave`[2,40] `weaveAmt`[0,40] `ascii`[6,24] `czoom`[0,40] `timeDepth`[1,23]
Color: `rgb`[0,90] `posterize`[2,16] `thresh`[0,1] `hue`[0,360] `hueSpeed`[0,10]
Layers: `cloneCount`[1,24] `cloneSpread`[0,180] `mirrorShift`[-120,120] `kaleido`[2,16] `echoCount`[1,8] `echoDecay`[0.2,0.95] `feedback`[0,0.55]
Surface: `flow`[0,140] `scan`[3,80] `dotSize`[3,28]
Zone: `opacity`[0,1] `scale`[0.2,2] `feather`[0,40] `rotation`[-3.2,3.2] `innerR`[0.05,0.9] `bloomAmt`[0,1] `dispAmt`[0,60] `shapeMorph`[0,1] `motionSpeed`[0,4] `motionAmt`[0,120] `seed`[0,999]

### enum params (strings)
- `blend`: `source-over` `lighter` `screen` `multiply` `overlay` `difference` `hard-light` `exclusion`
- `tileMode`: `normal` `brick` `brickV` `diamond` `mirror` `rot4`   (mosaic layout)
- `tileFlow`: `both` `lr` `rl` `ud` `du` `diag` `scroll` `radial` `swirl`   (mosaic drift direction)
- `sliceDir`: `h` `v` `radial`   ·   `sliceMode`: `shift` `wave` `shuffle` `flip`
- `wallMode` (wallpaper symmetry): `pmm` `p4` `pg`
- `convKernel`: `sharpen` `emboss` `edge` `ridge` `blur` `custom`  (with `custom`, set `kernel`: 9-number array)
- `cmat` (colormtx): `swap` `rswap` `sepia` `cool` `acid`
- `motion` (per-zone movement): `none` `drift` `orbit` `bounce` `spiral` `shake` `dvd`

## LFOs (`lfos`, up to 3 per zone)

`{ "on":true, "target":"<param>", "wave":"sine|tri|square|saw|noise", "rate":0.4, "depth":0.4 }`
`target` is any fx param name above, or `x`/`y` (moves the zone). `rate` 0.02..8, `depth` 0..1.

## Sequencer (`state.seq`) — 64-step lanes (0/1)

Lanes: `Kick` `Snare` `Hat` `Bass` `Glitch` `Morph` `Visual`. **Each is a length-64 array of 0/1** (4 bars of 16 sixteenth-notes). Shorter arrays are **tiled (repeated) to fill 64** on load, so a 16-length groove plays 4× across the loop. Step 0 is a `1`, etc. Autopilot/scene-cycle fire every 16 steps (once per bar); a bar marker shows every 16 steps in the UI.
`Kick/Snare/Hat/Bass` play the synth + drive envelopes; `Glitch` fires glitch bursts; `Morph` flips scene A/B; `Visual` re-rolls the selected zone.
`ui.bpm` sets tempo; `ui.swing` 0..0.45.

## Songs (`state.songs`, `state.songIdx`) — 5-slot library

`state.songs` is an array of **exactly 5** song objects; `state.songIdx` (0–4) is the active one. Each song:
```json
{ "bpm":128, "swing":0.08, "seq": { "Kick":[…64…], "Hat":[…64…], … } }
```
The active song's `seq/bpm/swing` should match the top-level `state.seq/bpm/ui.swing`. Author distinct patterns per slot to ship a full set (e.g. intro / main / breakdown / drop / outro). Omit `state.songs` entirely and the app fills 5 copies of the current pattern. Slot 1 (index 0) is treated as the default.

## Mod matrix (`ui.mod`) — audio → visual routing amounts

`Kick`→offset · `Snare`→glitch · `Hat`→rgb · `Bass`→flow · `Low/Mid/High`→offset/flow/rgb (FFT) · `Amp`→zoom.

## Global post FX (`state.global`)

`grain`[0,0.5] `vignette`[0,1] `strobe`[0,1] `feedback`[0,0.6] `dim`[0,1].

## Scenes / morph (optional)

`state.scenes = { "A": <snapshot|null>, "B":..., "C":..., "D":... }` where a snapshot is an array of
`{id,x,y,w,h,fx,enabled}` per zone. Morphing/cycling blends A↔B; usually leave `scenes` out and let the
user capture them live.

## Named presets (for reference / inspiration)

These are per-zone effector recipes the app ships; mirror their spirit when authoring zones:
`glitch pulse tiles dream vhs sortstorm vortex neon melt timewarp fabric prism kernel matrixtv escher liquid`.

## Defaults (every unspecified fx value falls back to these)

cols 4, rows 8, offset 80, random 40, opacity 1, flow 16, rgb 8, scale 1, slices 18, sliceDir h, sliceMode shift,
cloneCount 6, cloneSpread 28, kaleido 6, scan 22, dotSize 8, posterize 5, feedback 0.18, waveAmp 16, waveFreq 0.05,
twist 1.4, glitchAmt 26, vhsAmt 12, thresh 0.5, hue 0, hueSpeed 0, echoCount 4, echoDecay 0.6, tileMode normal,
tileFlow both, motion none, motionSpeed 1, motionAmt 30, seed 17.
