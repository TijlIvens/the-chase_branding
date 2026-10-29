---
name: chase-brand-assets
description: Create on-brand SVG assets for The Chase — Unlock the City (game app). Use when asked to make, edit or review an icon, logo variant, badge, wordmark, title lettering, app icon, map marker, achievement, or any graphic for The Chase, or to check an asset against the brand book. Covers UI icons (24px stroke), game icons (64px full colour), logo lockups and display lettering.
---

# Chase brand assets

Everything lives in the branding repo root (the folder holding `BRAND_BOOK.md`).
Paths below are relative to it. Scripts need only `python3` (3.9+, standard library).

## Before you draw

1. Read `BRAND_BOOK.md` §1 (story, cast, game mechanics), then sections 2 (colour),
   5 (iconography) and, for logos, 3. Get the story right: Aero is the player's friendly
   guide (never shown as a threat or in `danger` red), Mr. Chase is the inventor, the
   collectibles are **Diamond Beacons**, a wrong answer costs 5 seconds, and every player
   gets a coupon.
2. Use colours **only** from `tokens/colors.json`. Need a new one? Add it to
   `tokens/colors.json` and `tokens/colors.css` with a `$description`, and say so in your reply.
3. Look at 2–3 existing files of the same kind and match them.

## Pick the asset type

| Asking for… | Type | Start from | Save to |
|---|---|---|---|
| Interface glyph (nav, buttons, toolbar) | UI icon | `templates/ui-icon.svg` | `assets/icons/ui/<name>.svg` |
| Item, reward, character, power-up, achievement | Game icon | `templates/game-icon.svg` | `assets/icons/game/<name>.svg` |
| Something placed on the map | Map marker | copy any `assets/icons/map/marker-*.svg`, keep the pin path | `assets/icons/map/marker-<name>.svg` |
| Title, banner text, event name | Lettering | `scripts/wordmark.py` | `assets/lettering/<name>.svg` |
| Logo change | Logo | edit `assets/logo/emblem.svg`, then `scripts/build_logo_suite.py` | `assets/logo/`, `assets/app/` |
| Larger illustration, badge, splash | Illustration | `templates/game-icon.svg`, bigger viewBox | `assets/illustrations/<name>.svg` |

Names are lowercase kebab-case nouns using the game's own words: `beacon-gold`, `aero-cheering`, `coupon-cafe`.

## Rules by type

**UI icon** (checked by the validator)
- `viewBox="0 0 24 24"`, keep shapes inside 2–22.
- Root has `fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="square" stroke-linejoin="miter"`. No hex colours anywhere.
- Angular: prefer diamonds, chamfered corners, hexagons. Circles only when the object is round (coin, compass).
- One idea per icon, at most ~4 paths. It must read at 16 px.

**Game icon** (checked by the validator)
- `viewBox="0 0 64 64"`, object fills ~52–60 px.
- Every `id` starts with `<filename>-` (e.g. `gem-chrome`) so icons can be inlined together.
- Light from the top-left. Gradients from `tokens/colors.json → gradients`.
- Separate the object from any background with a thin `ice` (#E8F6FC) or `aero-shade` (#1F2534) outline.
- Magic is cool (cyan → violet); warmth only from gold (`horn-gold` family).

**Map marker** (checked like a game icon)
- Keep the shared pin path and `#0B0E24` fill unchanged; only change the rim colour and the symbol.
- Pick the rim colour by meaning from `BRAND_BOOK.md` §5 (danger = threat, gold = places, …).
- Keep the symbol inside x 18–46, y 8–40 so it stays clear of the rim.

**Lettering**
```bash
python3 .agents/skills/chase-brand-assets/scripts/wordmark.py "DISTRICT UNLOCKED" > assets/lettering/district-unlocked.svg
python3 .agents/skills/chase-brand-assets/scripts/wordmark.py "+250 XP" --height 40 --fill "#4ADEF6" --group   # <g> to paste inside another SVG
```
Supports A–Z, 0–9, space and `. , : ! ? - ' /` (`+` is not supported — use words or another glyph). Default fill is the chrome gradient; on light backgrounds use `--fill "#0F1033"`.

**Logo**
Never hand-edit the derivative files. Change `assets/logo/emblem.svg` (and the matching path constants at the top of `build_logo_suite.py` if geometry moved), then:
```bash
python3 .agents/skills/chase-brand-assets/scripts/build_logo_suite.py
```

**All SVGs**
- `xmlns`, `viewBox`, and an accessible name (`role="img" aria-label="…"` or `<title>`).
- No `<script>`, `<image>`, `<foreignObject>`, external `href`, embedded rasters or web fonts. Text must be paths (use `wordmark.py`).
- Hand-written, readable paths; round coordinates to ≤ 1 decimal. Icons under 20 KB.

## Finish (always)

```bash
python3 .agents/skills/chase-brand-assets/scripts/check_svg.py          # must print "N/N SVGs pass"
python3 .agents/skills/chase-brand-assets/scripts/gallery.py            # rebuilds assets/gallery.html
```
Then **look at it**: serve `assets/` (`python3 -m http.server -d assets 8765`) and open
`http://localhost:8765/gallery.html`, or render the file with any SVG viewer you have
(browser, `qlmanage -t` on macOS, `rsvg-convert`, Inkscape). Check it on both the dark and light
tiles and at small size. If you cannot view images, say so in your reply instead of claiming it looks right.

If you add a new icon, also add its name to the set list in `BRAND_BOOK.md` §5.

## Working with several agents

- Split work by file: one agent per asset file; nobody edits another agent's file.
- Only one agent at a time edits `tokens/colors.json`, `assets/logo/emblem.svg` or `BRAND_BOOK.md`.
- `check_svg.py` is the shared contract: an asset is done when it passes and has been viewed.
- Regenerate `gallery.html` last; it is a build output, safe to overwrite.
