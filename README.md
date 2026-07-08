# Pixel Flow — Claude Code plugin marketplace

The **`/pixel-flow-vibe`** skill: describe a look and get a ready‑to‑open Pixel Flow config as a shareable `#cfg=` link — for both apps:

- **Pixel Flow Nodes** — a node/dataflow video synth
- **Pixel Flow Studio** — a zone/sequencer effect studio

Live apps → **https://pixel-flow.atomic47.co**

## Install (Claude Code)

```
/plugin marketplace add Atomic-47-Labs/pixel-flow
/plugin install pixel-flow-vibe@pixel-flow
```

Then, in chat:

```
/pixel-flow-vibe  dreamy kaleidoscope that morphs on the downbeat --nodes --live
```

`--nodes` targets the node app · `--live` returns a link on the deployed site · `--kiosk` opens it as a fullscreen viewer experience.

## What's inside

```
.claude-plugin/marketplace.json      # marketplace manifest
pixel-flow-vibe/
  .claude-plugin/plugin.json         # plugin manifest
  skills/pixel-flow-vibe/            # the skill
    SKILL.md
    reference/schema.md              # Studio config catalog
    reference/schema-nodes.md        # Nodes operator catalog
    scripts/encode.py                # config <-> #cfg= URL codec
```

MIT-style: use it, remix it, share the links.
