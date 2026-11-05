# Themes, styles and patterns

Generated from the running app (Studio 3). `scripts/vocab.json` holds the same data; `encode.py --list` prints it.

A **style** is how a piece looks: colour grade, palette, letterbox frame, film artefacts, grain and vignette, applied over every zone.
A **pattern** is how it moves and changes: layout, zone roles, motion, a timeline of scenes and cuts, tempo and groove.
A **theme** is a named set of styles and patterns, plus recipes that pair them. `recipe = pattern × style × source`.

## The theme block

```json
{"theme": {"style": "noir", "pattern": "trailer", "presets": ["ghost"],
           "titles": {"lines": ["THE LAST TAKE|a pixel flow picture"], "pos": "center"}},
 "state": {}, "title": "Last Take"}
```

- `pattern` builds the zones, scenes and timing **only when `state` has no zones**. Leave zones out to use it.
- `presets` fills the pattern's zones round-robin (any zone preset id). Without it the zones start as `dream`.
- `style` is applied over whatever zones there are, so it also works on an authored screen.
- `titles` turns on the title line; see Titles below.
- CLI: `encode.py --style noir --pattern trailer --presets ghost --title "Last Take" --live --kiosk --short`.

## Movie

Film looks and edits for a movie clip (⌘I imports one) or the camera.

| style | grade | frame | feel |
|---|---|---|---|
| `noir` Film Noir | Hard black & white | 1.85 | hard black and white, smoke and shadow |
| `technicolor` Technicolor | Three-strip | 1.37 | 1950s three-strip colour |
| `super8` Super 8 | Warm fade | 4:3 | home movies, light leaks, 18 fps |
| `silent` Silent Era | Sepia | 4:3 | 1920s reel, iris and scratches |
| `neonnoir` Neon Noir | Teal & orange | 2.39 | rain-soaked sci-fi |
| `matrix` Matrix Code | Green code | 2.39 | green digital rain |
| `vhshorror` VHS Horror | VHS wash | 4:3 | a found tape |
| `pastel` Pastel Symmetry | Pastel | 1.85 | centred storybook framing |

Patterns: `trailer` · `slowburn` · `splitreel` · `montage` · `opening`

| recipe | name | style × pattern | what you see |
|---|---|---|---|
| `noirburn` | Noir Slow Burn | noir × slowburn | Black-and-white push-in with smoke and dust. Best on a movie clip or the camera |
| `noirtrailer` | Noir Trailer | noir × trailer | Hard cuts every bar, flashes on the beat, in black and white |
| `technicolortitles` | Technicolor Titles | technicolor × opening | Saturated Academy-frame opening with fading title cards |
| `super8montage` | Super 8 Montage | super8 × montage | Home-movie grid of time-delayed copies, light leaks and 18 fps |
| `silentreel` | Silent Reel | silent × opening | Sepia, iris and scratches with intertitles |
| `neontrailer` | Neon Noir Trailer | neonnoir × trailer | Teal-and-orange scope frame, halation, cuts on the kick |
| `neonsplit` | Neon Split Reel | neonnoir × splitreel | Three neon bands, each a moment behind |
| `coderain` | Code Rain | matrix × splitreel | Green code bands sliding through time |
| `foundtape` | Found Tape | vhshorror × trailer | A washed-out tape that cuts and flashes |
| `pastelsymmetry` | Pastel Symmetry | pastel × slowburn | Centred, mirrored and pastel, with a slow push-in |

## Music

Genre looks with matching grooves and tempos.

| style | grade | frame | feel |
|---|---|---|---|
| `techno` Techno | Ice | none | cold, hard, strobing |
| `ambient` Ambient | Calm | none | slow, soft, wide |
| `synthwave` Synthwave | Synth | 2.39 | 80s neon grid |
| `hiphop` Hip-hop | Gold | none | warm gold, crate dust |
| `dnb` Drum & Bass | Ember | none | fast, hot, jittery |

Patterns: `pulsegrid` · `splitreel` · `montage` · `slowburn` · `wheel`

| recipe | name | style × pattern | what you see |
|---|---|---|---|
| `technogrid` | Techno Grid | techno × pulsegrid | Cold 3×3 wall strobing at 128 |
| `ambientdrift` | Ambient Drift | ambient × drift | Soft shapes wandering over a calm grade |
| `synthwavewheel` | Synthwave Wheel | synthwave × wheel | Scope-framed neon wedges with scanlines |
| `hiphopsplit` | Gold Split | hiphop × splitreel | Warm printed bands with crate dust |
| `dnbmontage` | Jungle Montage | dnb × montage | Hot, fast grid of delayed glitch cells |

## Nature

Elemental looks for slow, calm or stormy pieces.

| style | grade | frame | feel |
|---|---|---|---|
| `ocean` Ocean | Ocean | none | deep blue water |
| `forest` Forest | Forest | none | green light through leaves |
| `fire` Fire | Ember | none | embers and heat |
| `aurora` Aurora | Aurora | none | northern lights |
| `storm` Storm | Soft black & white | none | lightning in black and white |

Patterns: `slowburn` · `drift` · `wheel` · `trailer`

| recipe | name | style × pattern | what you see |
|---|---|---|---|
| `oceanslow` | Deep Water | ocean × slowburn | A slow push into liquid blue |
| `forestdrift` | Forest Floor | forest × drift | Plants growing between drifting light |
| `firewheel` | Fire Wheel | fire × wheel | Embers spinning in eight wedges |
| `auroradrift` | Northern Lights | aurora × drift | Aurora colours drifting with particles |
| `stormtrailer` | Storm | storm × trailer | Lightning cuts in black and white |

## Ambient

Slow, layered and dreamy: low tempos, 16-bar holds, soft blends, and layers that fade in one at a time. Every Ambient pattern plays the `Slow pulse` groove and silences the Glitch, Morph and Visual trigger lanes.

| style | grade | frame | feel |
|---|---|---|---|
| `haze` Haze | Haze | none | lavender fog, lifted blacks · adds bloom to every zone |
| `moonglow` Moonglow | Moonlight | none | silver-blue night light · adds bloom |
| `dusk` Dusk | Dusk | none | rose and violet after sunset |
| `tidepool` Tidepool | Ocean | none | slow light under water |
| `lantern` Lantern | Warm fade | none | warm paper-lantern glow |
| `pearl` Pearl | Pastel | none | pearl and pastel shimmer · adds bloom |

Patterns: `veils` · `blooms` · `undertow` · `drift` · `calm`

| recipe | name | style × pattern | what you see |
|---|---|---|---|
| `hazeveils` | Haze Veils | haze × veils | Three lavender layers drifting through each other, fading in one by one |
| `tidepool` | Tidepool | tidepool × veils | Water light in slow layers, rippling over each other |
| `moonblooms` | Moon Blooms | moonglow × blooms | Silver orbs of light swelling slowly, with long trails |
| `lanterns` | Lanterns | lantern × blooms | Warm paper-lantern glows floating and fading |
| `duskundertow` | Dusk Undertow | dusk × undertow | A rose-violet push-in with a ghosted layer a moment behind |
| `pearldream` | Pearl Dream | pearl × undertow | Pastel shimmer pulled slowly forward under its own echo |

## Occasions

Parties, seasons and celebrations.

| style | grade | frame | feel |
|---|---|---|---|
| `halloween` Halloween | Halloween | 4:3 | pumpkin orange and violet |
| `winter` Winter | Ice | none | frost and falling specks |
| `pride` Pride | Vivid | none | every colour |
| `newyear` New Year | Gold | none | gold and glitter |

Patterns: `trailer` · `drift` · `wheel` · `montage`

| recipe | name | style × pattern | what you see |
|---|---|---|---|
| `halloweentape` | Halloween Tape | halloween × trailer | Pumpkin and violet tape that jumps on the beat |
| `wintersnow` | Snowfall | winter × drift | Frosted shapes and falling specks |
| `pridewheel` | Pride Wheel | pride × wheel | Every colour turning together |
| `newyearmontage` | Midnight | newyear × montage | Gold sparks and a countdown grid |

## Stage

Readable backgrounds for talks and streams.

| style | grade | frame | feel |
|---|---|---|---|
| `calmstage` Calm | Calm | none | quiet behind speakers |
| `brand` Brand | Brand | none | Atomic 47 lime and blue |
| `keynote` Keynote | Soft black & white | none | low-contrast monochrome |

Patterns: `calm` · `slowburn` · `drift`

| recipe | name | style × pattern | what you see |
|---|---|---|---|
| `stagecalm` | Quiet Stage | calmstage × calm | A low, slow field behind a speaker |
| `stagebrand` | Brand Stage | brand × calm | Atomic 47 lime and blue, barely moving |
| `keynote` | Keynote | keynote × calm | Dimmed monochrome that keeps slides readable |

## Patterns

| id | name | layout | bpm | hold / blend (bars) | what it does |
|---|---|---|---|---|---|
| `trailer` | Trailer | full | 112 | 1 / 0 (cut) | full frame, a cut every bar, white flash on the kick |
| `slowburn` | Slow Burn | full | 72 | 8 / 4 | one hero shot, slow push-in, 8-bar holds |
| `splitreel` | Split Reel | bands(3) | 124 | 4 / 1 | three bands of the same picture, each a moment behind the last |
| `montage` | Montage | grid3 | 100 | 2 / 1 | a grid of time-delayed copies, one cell takes the lead at a time |
| `opening` | Opening Titles | full | 80 | 4 / 4 | letterboxed hero, slow drift, the title fades in and out · titles on |
| `pulsegrid` | Pulse Grid | grid3 | 128 | 2 / 1 | 3×3 wall shaking on the kick |
| `drift` | Drift | scatter(5,ellipse) | 84 | 8 / 4 | five soft shapes wandering slowly |
| `wheel` | Wheel | wedges | 118 | 4 / 2 | eight hue-spun wedges turning together |
| `calm` | Calm | full | 70 | 8 / 8 | one quiet field behind speakers, no strobe |
| `veils` | Veils | stack(3) | 60 | 16 / 8 | three full-frame layers drifting through each other, fading in one at a time · trigger lanes silent |
| `blooms` | Blooms | scatter(6,ellipse) | 56 | 16 / 8 | six soft orbs of light swelling slowly, with long trails · trigger lanes silent |
| `undertow` | Undertow | stack(2) | 64 | 16 / 8 | a slow push-in, with a ghosted copy of the picture drifting a moment behind · trigger lanes silent |

## Vibe → theme

Read a sentence as **style + pattern + source + energy**, then patch one field per follow-up.

| they say | style | pattern | notes |
|---|---|---|---|
| "70s horror trailer" | `vhshorror` | `trailer` | movie clip, strobe on kick |
| "noir slow burn on the camera" | `noir` | `slowburn` | `--cam`, kiosk |
| "home-movie montage, dreamy" | `super8` | `montage` | presets `ghost`,`dream` |
| "Blade Runner rain" | `neonnoir` | `splitreel` | `--wide` |
| "silent film with intertitles" | `silent` | `opening` | `titles.lines` = the cards |
| "same, but Technicolor" | `technicolor` | unchanged | patch `theme.style` only |
| "calm background for my talk" | `calmstage` or `keynote` | `calm` | no strobe, dim |
| "techno wall" | `techno` | `pulsegrid` | presets `glitch`,`tiles`,`pulse` |
| "slow, dreamy, layered" | `haze` or `pearl` | `veils` | presets `dream`,`smoke`,`lumen` |
| "ambient bed for a chill-out room" | `moonglow` or `lantern` | `blooms` | 56 BPM, no strobe |
| "sunset, slowly pulling in" | `dusk` | `undertow` | presets `liquid`,`ghost` |

**Movies**: a link cannot carry a video file. Say so, and tell them to press **⌘I** (or Source ▸ Import image / movie) after the link opens. The clip plays with sound, its soundtrack drives the visuals (⌥D toggles), and **J** plays / pauses. Use `--wide` for film work: recordings then come out 1280×720.

## Film settings (`state.global`)

| key | values | what it does |
|---|---|---|
| `grade` | `none` `mono-hard` `mono-soft` `sepia` `technicolor` `warm-fade` `teal-orange` `green-code` `vhs-wash` `pastel` `synth` `ice` `ember` `ocean` `forest` `aurora` `vivid` `halloween` `gold` `calm` `brand` `haze` `moon` `dusk` | colour grade over the whole stage |
| `frame` | `none` `2.39` `1.85` `16:9` `1.37` `4:3` `1:1` | letterbox shape; bars are black and sit over everything |
| `fit` | `fill` `fit` | a movie or camera fills the frame, or fits whole inside it |
| `weave` | 0–1 | projector gate wobble |
| `dust` | 0–1 | specks and the odd hair |
| `scratch` | 0–1 | vertical scratches that drift |
| `halation` | 0–1 | warm glow around highlights |
| `leaks` | 0–1 | drifting light leaks |
| `flicker` | 0–1 | exposure flicker |
| `iris` | 0–1 | round silent-era vignette |
| `fps` | 0 12 16 18 24 | frame hold for stutter (0 = smooth) |

A style sets all of these at once; set them directly only to tune a look.

## Titles (`state.titles`, or `theme.titles`)

| key | values |
|---|---|
| `on` | true / false |
| `lines` | list of text; `"Main title\|subtitle"` splits into two lines; one line shows per hold |
| `mode` | `fade` (in and out each hold) · `always` |
| `every` | 1 2 4 8 bars per line |
| `pos` | `center` `lower` `top` (inside the letterbox) |
| `font` | `serif` `condensed` `sans` `mono` |
| `size` | 0.4–2.5 |

## Stage (`ui.stage`)

`square` (814×768, default) or `wide` (1280×720). `encode.py --wide` sets it and checks geometry against it. A link with a different stage reloads the Studio once to switch.
