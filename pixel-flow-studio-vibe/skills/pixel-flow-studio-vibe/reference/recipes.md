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


## Presets added in Studio 3 (`zone.preset`)

From Pixel Flow Nodes v1/v2: generators, the three missing filters, and the Nodes preset looks.

| id | group | effectors | LFO |
|---|---|---|---|
| `conway` | Cellular | life bloom feedback | genHue sine |
| `spark` | Cellular | brain rgb echo | — |
| `spirals` | Cellular | cyclic twist | twist sine |
| `coral` | Cellular | rd hsv bloom | — |
| `mandelzoom` | Fractal | mandel bloom | — |
| `juliatunnel` | Fractal | julia feedback tunnel | juliaR sine |
| `neural` | Fractal | cppn hsv | cppnScale sine |
| `smoke` | Fractal | dejong bloom | — |
| `plant` | Growth | lsys bloom | — |
| `shell` | Growth | shellca posterize | — |
| `spirograph` | Growth | spiro feedback hue | — |
| `goldenspiral` | Growth | golden bloom echo | — |
| `glass` | Geometry | voronoi | — |
| `cells` | Geometry | voronoi bloom | — |
| `truchet` | Geometry | truchet hue | — |
| `swarmfield` | Geometry | particles bloom | — |
| `motionmap` | Camera | optic bloom echo | — |
| `asciicam` | Camera | hsv ascii | — |
| `camkaleido` | Camera | feedback kaleido | kaleido sine |
| `blurglow` | Camera | blur edges bloom | — |
| `kaleidotrails` | Nodes | kaleido rgb feedback | kaleido sine |
| `liquidmandala` | Nodes | field wallpaper bloom feedback | fieldAmt sine |
| `datamosh` | Nodes | glitch sort rgb | glitchAmt noise |
| `infinitetunnel` | Nodes | twist czoom feedback xform | twist sine |

## Recipes added in Studio 3 (`encode.py --recipe <id>`)

Theme recipes pair a style with a pattern; see `reference/themes.md` for the theme groups.

| id | name | group | layout | what you see |
|---|---|---|---|---|
| `lifegrid` | Life Grid | Generative | grid3 | 3×3 automata (Life, Brain, Cyclic) seeded from the picture, sparked by the kick |
| `fractalwindow` | Fractal Window | Generative | pip | A Mandelbrot zoom journey with a drifting Julia picture-in-picture |
| `coralreef` | Coral Reef | Generative | full | Reaction–diffusion coral growing over a liquid field |
| `garden` | Garden | Generative | bands | Three bands: an L-system plant, a shell pattern and a spirograph |
| `particlesea` | Particle Sea | Generative | ringCenter | A particle swirl with attractor smoke in a ring at the centre |
| `neuralquilt` | Neural Quilt | Generative | grid2 | 2×2 of a CPPN net, Voronoi cells, Truchet tiles and a golden spiral |
| `mirrorhall` | Mirror Hall | Camera | full | Your movement glows and trails, kaleidoscoped. Press K for the camera |
| `stainedglass` | Stained Glass | Camera | splitV | The picture as drifting stained glass beside an ASCII copy. Press K for the camera |
| `lifemirror` | Life Mirror | Camera | full | Conway's Life seeded from the picture and re-sparked on every kick. Press K for the camera |
| `noirburn` | Noir Slow Burn | Movie | full | Black-and-white push-in with smoke and dust. Best on a movie clip or the camera |
| `noirtrailer` | Noir Trailer | Movie | full | Hard cuts every bar, flashes on the beat, in black and white |
| `technicolortitles` | Technicolor Titles | Movie | full | Saturated Academy-frame opening with fading title cards |
| `super8montage` | Super 8 Montage | Movie | grid3 | Home-movie grid of time-delayed copies, light leaks and 18 fps |
| `silentreel` | Silent Reel | Movie | full | Sepia, iris and scratches with intertitles |
| `neontrailer` | Neon Noir Trailer | Movie | full | Teal-and-orange scope frame, halation, cuts on the kick |
| `neonsplit` | Neon Split Reel | Movie | bands | Three neon bands, each a moment behind |
| `coderain` | Code Rain | Movie | bands | Green code bands sliding through time |
| `foundtape` | Found Tape | Movie | full | A washed-out tape that cuts and flashes |
| `pastelsymmetry` | Pastel Symmetry | Movie | full | Centred, mirrored and pastel, with a slow push-in |
| `technogrid` | Techno Grid | Music | grid3 | Cold 3×3 wall strobing at 128 |
| `ambientdrift` | Ambient Drift | Music | scatter | Soft shapes wandering over a calm grade |
| `synthwavewheel` | Synthwave Wheel | Music | wedges | Scope-framed neon wedges with scanlines |
| `hiphopsplit` | Gold Split | Music | bands | Warm printed bands with crate dust |
| `dnbmontage` | Jungle Montage | Music | grid3 | Hot, fast grid of delayed glitch cells |
| `oceanslow` | Deep Water | Nature | full | A slow push into liquid blue |
| `forestdrift` | Forest Floor | Nature | scatter | Plants growing between drifting light |
| `firewheel` | Fire Wheel | Nature | wedges | Embers spinning in eight wedges |
| `auroradrift` | Northern Lights | Nature | scatter | Aurora colours drifting with particles |
| `stormtrailer` | Storm | Nature | full | Lightning cuts in black and white |
| `hazeveils` | Haze Veils | Ambient | stack | Three lavender layers drifting through each other, fading in one by one |
| `tidepool` | Tidepool | Ambient | stack | Water light in slow layers, rippling over each other |
| `moonblooms` | Moon Blooms | Ambient | scatter | Silver orbs of light swelling slowly, with long trails |
| `lanterns` | Lanterns | Ambient | scatter | Warm paper-lantern glows floating and fading |
| `duskundertow` | Dusk Undertow | Ambient | stack | A rose-violet push-in with a ghosted layer a moment behind |
| `pearldream` | Pearl Dream | Ambient | stack | Pastel shimmer pulled slowly forward under its own echo |
| `halloweentape` | Halloween Tape | Occasions | full | Pumpkin and violet tape that jumps on the beat |
| `wintersnow` | Snowfall | Occasions | scatter | Frosted shapes and falling specks |
| `pridewheel` | Pride Wheel | Occasions | wedges | Every colour turning together |
| `newyearmontage` | Midnight | Occasions | grid3 | Gold sparks and a countdown grid |
| `stagecalm` | Quiet Stage | Stage | full | A low, slow field behind a speaker |
| `stagebrand` | Brand Stage | Stage | full | Atomic 47 lime and blue, barely moving |
| `keynote` | Keynote | Stage | full | Dimmed monochrome that keeps slides readable |

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
