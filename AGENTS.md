# The Chase — branding

Brand source of truth for **The Chase — Unlock the City**. Read by every coding agent
(Claude Code, Codex, Cursor, Gemini CLI, Copilot, …).

| What | Where |
|---|---|
| Brand book (colours, logo, type, icons, voice) | `BRAND_BOOK.md` |
| Colour tokens (source of truth) | `tokens/colors.json`, mirrored in `tokens/colors.css` |
| Original key art (read-only reference) | `base-images/` |
| Logo, app icon, favicon | `assets/logo/`, `assets/app/` |
| UI icons (24 px, stroke, currentColor) | `assets/icons/ui/` |
| Game icons (64 px, full colour) | `assets/icons/game/` |
| Asset preview page (generated) | `assets/gallery.html` |

## Creating or editing any asset

Follow the skill at **`.agents/skills/chase-brand-assets/SKILL.md`** — read it before
drawing anything. (Claude Code also finds it via the `.claude/skills/` link.)

Short version:
1. Colours only from `tokens/colors.json`.
2. Start from `.agents/skills/chase-brand-assets/templates/`.
3. Finish with:
   ```bash
   python3 .agents/skills/chase-brand-assets/scripts/check_svg.py
   python3 .agents/skills/chase-brand-assets/scripts/gallery.py
   ```
   and actually look at the result on dark and light.

Never edit files in `base-images/`. Never hand-edit logo derivatives; rebuild them
with `scripts/build_logo_suite.py`.
