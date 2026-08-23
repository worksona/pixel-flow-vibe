# Pixel Flow — Claude Code plugin marketplace

The **`/pixel-flow-vibe`** skill: describe a look and get a ready-to-open Pixel Flow config as a
shareable `#cfg=` link.

Three targets, one codec:

- **Pixel Flow Nodes v2** — the deployed node/dataflow video synth. 3D, particles, algorithmic
  sources, hand/face/body tracking, scene & timeline, and a full modular synth rack. **Default.**
- **Pixel Flow Studio** — the zone/sequencer effect studio: marquee regions, stacked effectors,
  LFOs, a 64-step sequencer + synth. No v2 equivalent, so still current.
- **Pixel Flow Nodes v1** — the legacy single-file graph app.

Live apps → **https://pixel-flow.atomic47.co** · App source → **[worksona/pixel-flow](https://github.com/worksona/pixel-flow)**

## Install (Claude Code)

```
/plugin marketplace add worksona/pixel-flow-vibe
/plugin install pixel-flow-vibe@pixel-flow
```

> Previously published as `Atomic-47-Labs/pixel-flow`. That path still redirects, but update it —
> GitHub redirects are not guaranteed to survive a future rename.

Then, in chat:

```
/pixel-flow-vibe  dreamy kaleidoscope that morphs on the downbeat
/pixel-flow-vibe  a patch where my hand bends a particle field
```

## Flags

| Flag | Effect |
|---|---|
| `--nodes` | target the node-graph app (config is a graph `{nodes:[...]}`) |
| `--live` | link on the deployed site — **Nodes there is v2**, so every operator resolves |
| `--dev` | link at the local `nodes-v2` vite dev server (`localhost:5173`) |
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
    reference/schema-studio.md       # Studio config catalog
    scripts/encode.py                # config <-> #cfg= URL codec
```

MIT-style: use it, remix it, share the links.
