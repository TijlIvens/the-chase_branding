# The Chase — branding

Brand source of truth for **The Chase — Unlock the City**. Read by every coding agent
(Claude Code, Codex, Cursor, Gemini CLI, Copilot, …).

## The app in 30 seconds

A mobile game blending storytelling, trivia and city exploration. Inventor **Mr. Arthur
Chase** and his mystical serpent companion **Aero** misfired their time machine, the
**Cerebrium Project**, scattering Aero and thousands of **Diamond Beacons** across timelines.
Aero now appears in the heart of each player's city and talks telepathically to Mr. Chase
in the future.

- Players walk to real locations, which unlock **multiple-choice questions** (city,
  general knowledge, pop culture).
- A correct answer earns points and collects that spot's (purely virtual) Diamond Beacon.
  A wrong answer costs **5 seconds**.
- **Every** player, win or lose, gets coupons or discounts at local businesses.

**Aero is the player's friendly guide, never a villain. Mr. Chase is the inventor, not an
antagonist.** Full story, cast, mechanics and naming rules: `BRAND_BOOK.md` §1.

| What | Where |
|---|---|
| Brand book (colours, logo, type, icons, voice) | `BRAND_BOOK.md` |
| Colour tokens (source of truth) | `tokens/colors.json`, mirrored in `tokens/colors.css` |
| Original key art (read-only reference) | `base-images/` |
| Logo, app icon, favicon | `assets/logo/`, `assets/app/` |
| UI icons (24 px, stroke, currentColor) | `assets/icons/ui/` |
| Game icons (64 px, full colour) | `assets/icons/game/` |
| Map markers (64 px pins) | `assets/icons/map/` |
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

## Committing and pushing

This repo is on GitHub: `TijlIvens/the-chase_branding` (branch `main`). When you finish a
task that changed files, **commit and push it** by following
**`.agents/skills/github-commit-push/SKILL.md`**:
stage only your own files by name, use a Conventional Commit message
(`feat(icons): add beacon-shard game icon`), then run
`.agents/skills/github-commit-push/scripts/push.sh`. Never force-push.
