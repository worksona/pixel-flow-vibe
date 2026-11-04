# Pixel Flow — Claude Code plugin marketplace

Two skills, one per app: describe a look and get a ready-to-open Pixel Flow link.

> **Generated, do not edit here.** This repo is built from `skills/` in the app repo
> [worksona/pixel-flow](https://github.com/worksona/pixel-flow) by `scripts/sync-marketplace.mjs`.
> Make skill changes there, next to the app they describe, then sync.

- **`/pixel-flow-vibe`** — Pixel Flow Nodes: v2 node graphs (and the legacy v1 app).
- **`/pixel-flow-studio-vibe`** — whole Studio screens: a layout of zones, a preset and motion
  per zone, a groove, mod matrix and post FX, validated against the Studio vocabulary. Also links
  any of the 20 stock recipes (`--recipe mandala`).

The two apps share one `#cfg=` link format:

- **Pixel Flow Nodes** (`/pixel-flow-vibe`) — the deployed node/dataflow video synth (v2). 3D,
  particles, algorithmic sources, hand/face/body tracking, scene & timeline, and a full modular
  synth rack. The legacy single-file v1 app is still a target.
- **Pixel Flow Studio** (`/pixel-flow-studio-vibe`) — the zone/sequencer effect studio: marquee
  regions, stacked effectors, LFOs, a 64-step sequencer + synth, themes and recipes.

Live apps → **https://pixel-flow.atomic47.co** · App source → **[worksona/pixel-flow](https://github.com/worksona/pixel-flow)**

## Install (Claude Code)

```
/plugin marketplace add worksona/pixel-flow-vibe
/plugin install pixel-flow-vibe@pixel-flow
/plugin install pixel-flow-studio-vibe@pixel-flow
```

> Previously published as `Atomic-47-Labs/pixel-flow`. That path still redirects, but update it —
> GitHub redirects are not guaranteed to survive a future rename.

Then, in chat:

```
/pixel-flow-vibe  dreamy kaleidoscope that morphs on the downbeat
/pixel-flow-vibe  a patch where my hand bends a particle field
/pixel-flow-studio-vibe  slow dreamy orbs drifting over a liquid bed
/pixel-flow-studio-vibe  a 3x3 VHS wall that punches on the kick, kiosk link
```

## Flags (`/pixel-flow-vibe`)

The Studio encoder has its own flags; see its `SKILL.md`.

| Flag | Effect |
|---|---|
| `--nodes` | accepted for compatibility; every config is a graph `{nodes:[...]}` |
| `--live` | link on the deployed site — **Nodes there is v2**, so every operator resolves |
| `--dev` | link at the local `apps/nodes` vite dev server (`localhost:5173`) |
| `--kiosk` | open fullscreen, output-only; a ✎ chip returns to the editor |
| `--cam` `--mic` `--image f.jpg` | set the source the link opens with |
| `--code` | print just the paste-able code for **Share ▾ → Load Config** |
| `--decode` | turn a share URL or code back into JSON, to remix |

A bare `file://` Nodes link opens **v1** and silently drops v2-only node types — prefer `--live`.

## What's inside

```
.claude-plugin/marketplace.json      # marketplace manifest
pixel-flow-vibe/
  .claude-plugin/plugin.json         # plugin manifest
  skills/pixel-flow-vibe/
    SKILL.md
    reference/schema-nodes-v2.md     # Nodes v2 catalog — rounds 1-13 (default target)
    reference/schema-nodes-v1.md     # Nodes v1 catalog (legacy)
    scripts/encode.py                # Nodes graph <-> #cfg= URL codec
pixel-flow-studio-vibe/
  .claude-plugin/plugin.json
  skills/pixel-flow-studio-vibe/
    SKILL.md
    reference/schema.md              # Studio config: zones, effectors, params, motion, links
    reference/recipes.md             # recipes, presets, layouts, grooves
    reference/themes.md              # themes, styles, patterns, film settings, titles
    scripts/encode.py                # expand layouts/presets, validate, encode (#cfg= / #cfgz= / #recipe=)
    scripts/vocab.json               # machine vocabulary the validator checks against
```

MIT-style: use it, remix it, share the links.
