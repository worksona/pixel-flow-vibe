# Pixel Flow Studio config schema (authoritative)

A config is JSON:

```json
{
  "ui":    { "bpm": 128, "swing": 0.08, "morphCurve": "smooth",
             "mod": { "Kick":140, "Snare":40, "Hat":18, "Bass":30, "Low":160, "Mid":55, "High":32, "Amp":0 } },
  "state": { "bpm":128, "seed":17, "zones":[ ... ], "seq":{ ... }, "global":{ ... },
             "layout": { ... }   // encoder-only shorthand, see below
           },
  "src":   { "cam": true, "mic": true, "image": "data:image/jpeg;base64,..." }   // optional
}
```

`state` is merged over the running app state, so **partial is fine**. Every zone is filled out
with defaults on load, so a zone needs only geometry, its effectors and the params you care about.

## Zone

```json
{ "id":"z1", "name":"Zone 1",
  "shape":"rect",                       // rect | ellipse | ring | lasso
  "x":0, "y":0, "w":814, "h":768,       // canvas is 814 wide x 768 tall
  "points":[[0,0],[1,0],[0.5,1]],       // lasso only: polygon normalised 0..1 inside x,y,w,h
  "preset":"glitch",                    // SHORTHAND: start from a preset (expanded by the encoder and the app)
  "motion":"orbit",                     // SHORTHAND: same as fx.motion
  "enabled": { "mosaic":true, "rgb":true },        // effectors ON (all others off)
  "fx": { "cols":8, "rows":8, "tileFlow":"swirl" }, // param overrides
  "lfos": [ {"on":true,"target":"offset","wave":"sine","rate":0.4,"depth":0.4} ],  // up to 3
  "hidden": false                       // Studio 2: zone kept but not drawn
}
```

- Zones draw **back to front** in array order. `ring` uses `fx.innerR` for its hole.
- With `preset`, the zone's own `enabled` / `fx` / `lfos` override the preset's.
- `id` and `name` are optional when authoring; the encoder fills them.

## Layout shorthand (`state.layout`, encoder-side)

```json
"layout": { "name":"grid3", "args":[], "rect":[0,0,814,768],
            "slots":[ {"preset":"glitch","motion":"shake"}, {"preset":"vhs"} ] }
```

Expands to one zone per cell; slots repeat round-robin; a slot may set `shape`. Layout zones
come **first** (behind); anything in `state.zones` stacks in front. Names and args are in
`recipes.md`.

## Effectors (`enabled` keys) — 39, grouped as in the app

- **Tiling**: `mosaic` `wallpaper` `affine` `kaleido` `mirror` `weave`
- **Slicing**: `slice` `timeslice` `scan`
- **Displace**: `flow` `wave` `ripple` `field` `displace` `smear` `melt`
- **Warp**: `twist` `tunnel` `czoom`
- **Glitch**: `glitch` `vhs` `rgb` `sort` `pixel`
- **Color**: `hue` `invert` `posterize` `threshold` `solar` `colormtx` `dither`
- **Stylize**: `dot` `ascii` `edges` `bloom` `convolve`
- **Feedback**: `feedback` `echo` `clone`

### Which params each effector reads

| effector | params |
|---|---|
| mosaic | cols rows offset random shuffle tileMode tileFlow |
| wallpaper | cols rows wallMode |
| affine | iter mtxScale mtxRot mtxDx |
| kaleido | kaleido · mirror: mirrorShift · weave: weave weaveAmt |
| slice | slices sliceDir sliceMode offset random |
| timeslice | slices timeDepth sliceDir · scan: scan |
| flow | flow · wave: waveAmp waveFreq · ripple: rippleAmt rippleFreq · field: fieldAmt fieldScale |
| displace | dispAmt · smear: smear smearAng · melt: melt |
| twist | twist · tunnel: mtxRot · czoom: czoom |
| glitch | glitchAmt · vhs: vhsAmt · rgb: rgb · sort: thresh · pixel: pix |
| hue | hue hueSpeed · posterize / dither: posterize · threshold / solar: thresh · colormtx: cmat cmix |
| dot | dotSize · ascii: ascii · bloom: bloomAmt · convolve: convKernel convAmt (kernel) |
| feedback | feedback · echo: echoCount echoDecay · clone: cloneCount cloneSpread |
| every zone | opacity scale rotation feather blend seed motion motionAmt motionSpeed shapeMorph (rect) innerR (ring) |

## fx params + ranges `[min, max]`

Structure: `cols`[1,32] `rows`[1,32] `slices`[2,80]
Displace: `offset`[0,360] `random`[0,320] `shuffle`[0,1]
Warp: `waveAmp`[0,80] `waveFreq`[0.01,0.3] `twist`[-4,4] `rippleAmt`[0,40] `rippleFreq`[0.01,0.2] `melt`[0,60] `fieldAmt`[0,50] `fieldScale`[8,64]
Break: `glitchAmt`[0,80] `vhsAmt`[0,40] `smear`[0,60] `smearAng`[0,6.3] `pix`[2,64]
Matrix: `convAmt`[0,1] `cmix`[0,1] `iter`[1,12] `mtxScale`[0.5,0.99] `mtxRot`[-1.2,1.2] `mtxDx`[-60,60]
Texture: `weave`[2,40] `weaveAmt`[0,40] `ascii`[6,24] `czoom`[0,40] `timeDepth`[1,23] `bloomAmt`[0,1] `dispAmt`[0,60]
Color: `rgb`[0,90] `posterize`[2,16] `thresh`[0,1] `hue`[0,360] `hueSpeed`[0,10]
Layers: `cloneCount`[1,24] `cloneSpread`[0,180] `mirrorShift`[-120,120] `kaleido`[2,16] `echoCount`[1,8] `echoDecay`[0.2,0.95] `feedback`[0,0.55]
Surface: `flow`[0,140] `scan`[3,80] `dotSize`[3,28]
Zone: `opacity`[0,1] `scale`[0.2,2] `feather`[0,40] `rotation`[-3.2,3.2] `innerR`[0.05,0.9] `shapeMorph`[0,1] `motionSpeed`[0,4] `motionAmt`[0,120] `seed`[0,999]

### Enum params

- `blend`: `source-over` `lighter` `screen` `multiply` `overlay` `difference` `hard-light` `exclusion`
- `tileMode`: `normal` `brick` `brickV` `diamond` `mirror` `rot4`
- `tileFlow`: `both` `lr` `rl` `ud` `du` `diag` `scroll` `radial` `swirl`
- `sliceDir`: `h` `v` `radial` · `sliceMode`: `shift` `wave` `shuffle` `flip`
- `wallMode`: `pmm` `p4` `pg`
- `convKernel`: `sharpen` `emboss` `edge` `ridge` `blur` `custom` (with `custom`, `fx.kernel` = 9 numbers)
- `cmat`: `swap` `rswap` `sepia` `cool` `acid`
- `motion`: `none` `drift` `orbit` `bounce` `spiral` `shake` `dvd` · Studio 2 adds `wander` `swing` `fig8`

### Motion — how zones move

| motion | path | good for |
|---|---|---|
| `drift` | slow elliptical sway | ambient, floating |
| `orbit` | circle of radius motionAmt | hypnotic, planets |
| `bounce` | hops upward | playful, on-beat |
| `spiral` | breathing circle | psychedelic |
| `shake` | jitter, grows on the kick | aggressive, club |
| `dvd` | real velocity, reflects off canvas edges (speed = motionSpeed) | playful, screensaver |
| `wander` | smooth noise path | organic, creatures (Studio 2) |
| `swing` | pendulum arc | lyrical (Studio 2) |
| `fig8` | figure-eight | hypnotic, loops (Studio 2) |

`motionAmt` is the radius in canvas px, `motionSpeed` the rate. LFOs on `x` / `y` / `rotation` /
`scale` stack on top of motion.

## LFOs (`lfos`, up to 3 per zone)

`{ "on":true, "target":"<param>", "wave":"sine|tri|square|saw|noise", "rate":0.4, "depth":0.4 }`
`target`: any of `offset random rgb flow slices cloneSpread mirrorShift kaleido scan dotSize waveAmp
waveFreq twist glitchAmt vhsAmt hue opacity scale rotation feather melt rippleAmt czoom pix smear
smearAng weaveAmt timeDepth innerR convAmt cmix mtxRot mtxScale fieldAmt shapeMorph bloomAmt dispAmt x y`.
`rate` 0.02–8 (Hz-ish), `depth` 0–1.

## Sequencer (`state.seq`) — 64-step lanes of 0/1

Lanes: `Kick` `Snare` `Hat` `Bass` `Glitch` `Morph` `Visual`. Shorter arrays tile to 64 (a
16-step groove plays four times). Kick/Snare/Hat/Bass play the synth and drive envelopes;
`Glitch` fires glitch bursts; `Morph` flips scene A/B; `Visual` re-rolls the selected zone.
`ui.bpm` sets tempo, `ui.swing` 0–0.45.

Authoring conveniences (encoder): a lane may be a string of 0/1 (`"1000100010001000"`,
spaces and `|` ignored, 16/32/64 long), and `state.groove` names a stock groove
(`four` `break` `half` `techno` `trap` `slow` `silence`) that `seq` lanes then override.

## Songs (`state.songs`) — a 5-slot set

```json
"songs": [ { "bpm": 140, "groove": "four", "seq": { "Visual": "1000000000000000" } },
           { "bpm": 148, "seq": { "Kick": "1000100010001000", "Hat": "1111111111111111" } } ]
```

1–5 songs of `{bpm, swing, seq | groove}`; the encoder pads to the 5 slots the app keeps and starts
the live groove and tempo from song 1 (or `state.songIdx`). One song = one 64-step loop (4 bars).
Play them in order with `perform.chain`.

## Mod matrix (`ui.mod`) — audio → visual

`Kick`→offset [0,300] · `Snare`→glitch [0,120] · `Hat`→rgb [0,60] · `Bass`→flow [0,90] ·
`Low`→offset [0,360] · `Mid`→flow [0,140] · `High`→rgb [0,90] (mic FFT) · `Amp`→zoom [0,60].

## Global post FX (`state.global`)

`grain`[0,0.5] `vignette`[0,1] `strobe`[0,1] (flash on kick) `feedback`[0,0.6] `dim`[0,1].

## Scenes (`state.scenes`) — up to four looks of the same zones

Author scenes as **overrides of the zones as written** (scene A); the encoder turns them into full
snapshots:

```json
"scenes": {
  "B": { "Neon*": { "fx": { "hue": 350, "scale": 0.7 }, "enabled": { "kaleido": true } },
         "Rose Window": { "x": 57, "y": 34, "w": 700, "h": 700, "fx": { "innerR": 0.62 } } },
  "C": { "*": { "fx": { "opacity": 0.4 } }, "Glitch*": { "preset": "emboss", "motion": "none" } },
  "D": { ... }
}
```

- Selectors: `"*"` (every zone), an exact zone name or id, or a name prefix ending in `*`.
  Layout zones are named after their preset plus a number (`Neon 1`, `Prism 2`, …), so `"Neon*"`
  addresses all of them. Later selectors win.
- An override may set `x` `y` `w` `h`, `fx {}`, `enabled {}`, `preset` (swaps the whole effector
  stack) and `motion`.
- Between scenes, geometry and every numeric param **blend**; effector stacks, `blend`,
  `sliceDir`, `sliceMode` and `motion` **switch** at the midpoint.
- A zone with `"scenes": false` stays out of every scene and keeps its own motion (use it for a
  `dvd` zone, which scenes would otherwise pin in place).
- `"A": {...}` is optional; give it to make the opening scene differ from the zones as written.
- Raw snapshots (arrays of `{id,x,y,w,h,fx,enabled}`) also work and pass straight through.

## Perform (`perform`) — what runs when the link opens (Studio 2)

```json
"perform": { "cycle": true, "holdBars": 6, "blendBars": 3,
             "chain": [ { "song": 1, "loops": 1 }, { "song": 2, "loops": 2 } ], "chainLoop": true,
             "autopilot": "drift", "autopilotGain": 0.4 }
```

| key | meaning |
|---|---|
| `cycle` | walk the scenes A→B→C→D→A…; needs 2+ scenes |
| `holdBars` | bars each scene holds, 1–32 (the opening scene holds its full length first) |
| `blendBars` | bars each transition takes, 1–8, at most `holdBars` |
| `morph` | `"auto"`: a ~16 s sine sweep A↔B instead of `cycle` |
| `chain` | play songs in order, `song` 1–5, `loops` 1–16 (one loop = 4 bars) |
| `chainLoop` | repeat the chain (default true) |
| `autopilot` | `drift` `storm` `bloom` `matrix`: nudge one zone every bar |
| `autopilotGain` | 0.2–2.5, how hard autopilot pushes (1 = default) |
| `play` | false to open paused |

**Long-form tip**: make the scene cycle and the song chain different lengths so they drift against
each other (e.g. 4 scenes × 6 bars = 24 bars against a 32-bar chain repeats only every 96 bars).
Keep `autopilotGain` low (0.3–0.6) so scenes stay recognisable. Share links made in the app carry
`perform` too, so whatever is running when someone presses Share is what the link replays.

## Links

- `#cfg=<base64 JSON>` — every Studio build.
- `#cfgz=<base64url deflate-raw JSON>` — Studio 2, about half the length.
- `#recipe=<id>` — Studio 2, a stock recipe.
- append `&view=viewer` for kiosk (fullscreen, no UI; a ✎ chip returns to the editor).
