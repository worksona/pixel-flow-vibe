# Studio recipes, presets, layouts, grooves

Generated from the running app (`window.PF`), Studio 2. `scripts/vocab.json` holds the same
data in machine form; the encoder validates against it.

## Stock recipes — whole screen (`encode.py --recipe <id>`, Studio 2)

| id | name | group | layout | bpm | what you see |
|---|---|---|---|---|---|
| `kickgrid` | Kick Grid | Club | grid3 | 140 | 3×3 mosaic / glitch tiles punching on the kick |
| `strobebands` | Strobe Bands | Club | bands | 150 | Six horizontal slice bands with a strobe on the kick |
| `shatterstorm` | Shatter Storm | Club | shatter | 160 | Triangular shards shaking on a breakbeat |
| `wedgewheel` | Wedge Wheel | Club | wedges | 128 | Eight hue-spun wedges, neon and prism alternating |
| `mandala` | Mandala | Dream | full | 76 | One kaleidoscope with bloom, slowly orbiting |
| `deepsea` | Deep Sea | Dream | ringCenter | 88 | Liquid field bed with a prism ring floating in the centre |
| `aurora` | Aurora | Dream | bands(3) | 92 | Three soft bands of flow and hue drifting past each other |
| `softfocus` | Soft Focus | Dream | full | 70 | A single feathered ellipse of echo and clones breathing |
| `broadcast` | Broadcast | Retro | pip | 120 | VHS full frame with a bouncing MatrixTV picture-in-picture |
| `arcade` | Arcade | Retro | grid4 | 132 | 4×4 pixelated dithered tiles in brick scroll |
| `taperot` | Tape Rot | Retro | cols(5) | 100 | Five time-sliced columns smearing the past |
| `crtwall` | CRT Wall | Retro | grid2 | 110 | A 2×2 wall of scanlines, kernels and sort storms |
| `escherwall` | Escher Wall | Structure | full | 96 | Wallpaper symmetry with a slow affine fold |
| `halftonepress` | Halftone Press | Structure | bands(4) | 104 | Four printed bands: halftone, riso, emboss, ASCII |
| `weaveloom` | Weave Loom | Structure | splitV | 98 | Fabric weave beside a droste fold |
| `matrixrain` | Matrix Rain | Structure | cols | 124 | Six columns of MatrixTV melting downward |
| `dvdparty` | DVD Party | Motion | scatter | 124 | Six tiles bouncing off the edges, DVD-logo style |
| `orbiters` | Orbiters | Motion | orbiters | 100 | Four prism moons orbiting a dreaming centre |
| `drifters` | Drifters | Motion | scatter(5,ellipse) | 84 | Five soft ellipses wandering slowly |
| `swarm` | Swarm | Motion | grid4 | 150 | Sixteen small shaking tiles with a storm autopilot |

In the app: **Recipes ▾** in the top bar, **⇧1–0** for the first ten, or ⌘K and type the name.

## Zone presets (`zone.preset`)

| id | group | effectors | LFO |
|---|---|---|---|
| `glitch` | Classic | mosaic rgb slice scan posterize glitch | offset noise |
| `pulse` | Classic | clone flow rgb feedback | cloneSpread sine |
| `tiles` | Classic | mosaic mirror dot | — |
| `dream` | Classic | kaleido clone flow feedback | kaleido sine |
| `vhs` | Retro | vhs scan rgb glitch | vhsAmt noise |
| `sortstorm` | Retro | sort slice rgb | offset sine |
| `vortex` | Retro | twist kaleido echo | twist sine |
| `neon` | Retro | edges hue flow echo | flow tri |
| `melt` | Organic | melt flow hue | melt sine |
| `timewarp` | Organic | timeslice rgb echo | timeDepth tri |
| `fabric` | Organic | weave pixel posterize | weaveAmt tri |
| `prism` | Organic | czoom ripple mirror | czoom sine |
| `kernel` | Matrix | convolve posterize rgb | convAmt sine |
| `matrixtv` | Matrix | colormtx scan glitch dither | cmix square |
| `escher` | Matrix | wallpaper affine | mtxRot sine |
| `liquid` | Matrix | field ripple hue | fieldAmt sine |
| `halftone` | Print | dot posterize hue | dotSize sine |
| `ascii` | Print | ascii posterize | scale sine |
| `riso` | Print | posterize colormtx dither rgb | rgb square |
| `emboss` | Print | convolve posterize scan | convAmt tri |
| `tunnel` | Deep | tunnel hue echo | mtxRot sine |
| `droste` | Deep | affine kaleido | mtxScale sine |
| `ghost` | Deep | echo feedback smear | smearAng tri |
| `lumen` | Deep | bloom edges hue czoom | czoom sine |

Keys **1–0** apply the first ten (glitch … neon) to the selected zone in the app.

## Layouts (`state.layout.name`, encoder-side)

All take the full canvas `[0,0,814,768]` unless `rect: [x,y,w,h]` is given.

| name | args | cells |
|---|---|---|
| `full` | — | 1 rect, the whole rect |
| `splitV` / `splitH` | — | 2 rects side by side / stacked |
| `grid2` `grid3` `grid4` | — | 4 / 9 / 16 rects |
| `bands` | `[n=6]` | n horizontal strips |
| `cols` | `[n=6]` | n vertical strips |
| `thirds` | — | big left 2/3 + two stacked on the right |
| `wedges` | `[n=8]` | n pie slices (lasso) around the centre |
| `shatter` | `[seed=17]` | ~18 jittered triangles (lasso) |
| `ringCenter` | — | full bed + a centred ring (diameter 62% of the short side) |
| `pip` | — | full bed + an inset at bottom-right (34% size) |
| `orbiters` | — | a centre ellipse + 4 ellipses around it |
| `scatter` | `[n=6, shape="rect", seed=17]` | n random tiles 16–34% of the canvas |

Slots repeat round-robin: 9 cells with 3 slots → A B C A B C A B C. A slot may set `shape`
to override the cell's shape (e.g. make grid cells ellipses).

## Grooves (in the app: Sequencer ▸ Groove ▾)

Four on the floor · Breakbeat · Half-time · Techno · Trap hats · Slow pulse · Clear.
When authoring, write the lanes directly into `state.seq` (16 steps tile to 64):

```
four on the floor  Kick 1000100010001000  Snare 0000100000001000  Hat 0010001000100010
breakbeat          Kick 1000001000100000  Snare 0000100000001001  Hat 1010101010101010
half-time          Kick 1000000000100000  Snare 0000000010000000
techno             Kick 1000100010001000  Hat 0010001000100011  Bass 0010001000100010
trap hats          Kick 1000000100100000  Snare 0000000010000000  Hat 1111111111111111
slow pulse         Kick 1000000010000000  Hat 0000100000001000
```
