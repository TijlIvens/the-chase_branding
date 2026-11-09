---
name: chase-cover-images
description: Create or edit The Chase — Unlock the City illustrated country and city covers in the established painted landmark style. Use for app overview covers, destination panoramas, and matching location artwork with Aero and Diamond Beacons; use chase-brand-assets for small SVG icons and logos.
---

# The Chase cover images

Create full-bleed painted location artwork matching the existing destination collection.
Default to **3:2 landscape, 1536 × 1024**, unless the user requests another format.

## Find the project and references

Work in the branding checkout containing `BRAND_BOOK.md` and `assets/covers/`.
When invoked outside it, check `/Users/sumikshah/The-Chase/branding`; if unavailable,
locate the user's checkout before requesting missing reference images. A global
installation can link to this repo skill; resolve symlinks before deriving relative paths.

Read `BRAND_BOOK.md` §1, §2, §6 and the applicable repository instructions. For the
current collection and prior scene choices, use `assets/covers/manifest.json` and
`assets/covers/cover-briefs.json`. Do not load the entire generation history by default.

Inspect these local images with the image viewer before generating:

1. **Collection style/composition:** `assets/covers/countries/belgium.jpg` for a country,
   or `assets/covers/cities/antwerp.jpg` for a city. A geographically closer existing
   cover can also guide architecture and scenery.
2. **Original project drawing style:** `base-images/PHOTO-2026-02-18-06-49-01 4.jpg`.
3. **Aero identity:** `base-images/PHOTO-2026-02-18-06-52-19.jpg`; use the brand book
   and finished covers for the golden horns, purple eyes, and friendly expression.

Keep `base-images/` unchanged. Use the reference files themselves as image-generation
inputs, not merely a written description of their style.

## Compose the new location

Infer country versus city from the request when clear. Ask only for an ambiguous
location or a missing choice that materially changes the result. A new location does
not require the user to specify landmarks, food, flags, or dimensions from scratch.

- **Country:** compose 3–5 prominent national landmarks into one harmonious panorama;
  add its correct flag on a modest left-side flagpole and a small foreground arrangement
  of 2–3 recognizable local foods. Keep the flag legible and the food secondary.
- **City:** combine 2–4 local landmark buildings with a recognizable statue, fountain,
  monument, or public sculpture. Use that city's own landmarks. Do not add a country
  food table or flag unless requested. Do not invent a statue to fill a quota; prefer
  an existing landmark sculpture or building sculpture when suitable.
- Treat these as art-directed vistas, not maps or claims of a literal viewpoint.
  Keep distinctive building shapes and sculptural identities recognizable. Verify
  uncertain landmark identities, food associations, or flag details before using them.

**The shared look:** detailed semi-realistic painted adventure-game illustration,
clean architectural edges, soft painted shading, rich stone and foliage, atmospheric
perspective, blue-hour sky, gently gold-lit architecture, deep navy shadows, cyan magic,
and subtle violet distance. Avoid photorealism and flat vector treatment. Match the
collection's palette and grading; render flags and foods in their recognizable natural
colors rather than recoloring national symbols to the brand palette.

Landmarks take about 75% of visual attention. Keep a small friendly Aero at lower right
(roughly 15% of the image area or less), with a single small faceted blue Diamond Beacon
hovering over a thin cyan ring nearby. Aero has a teal beaked head, slate scaled serpent
body, lavender belly, **two swept-back golden horns**, purple eyes, and cyan rune lines;
no wings or limbs. Match scale and design across the collection.

Leave a quieter darker lower-left area where practical for app-rendered titles. Compose
for the actual 3:2 frame from the start. No painted location names, promotional copy,
logos, badge frames, borders, or separate collage panels. User-specified content and
lighting changes override these defaults while retaining the established drawing style.

## Generate and review

Read [references/prompt-template.md](references/prompt-template.md) for the reusable
prompt and short invocation examples. Fill in only the requested destination(s); do
not expand a request for one image into the entire country/city collection.

Use the built-in `image_gen` tool for raster generation and edits. Pass the inspected
local reference paths when the tool supports them. Distinguish style/identity references
from edit targets. For an edit, preserve the existing scene and change only the requested
parts. Prefer one generation call per distinct deliverable; use the same style references
and shared art direction across a batch. Do not substitute SVG icons or code-drawn scenery.
If the generation tool is unavailable, report that limitation instead of silently choosing
another paid service or requiring an API key.

Inspect the result for coherent style, requested content, flag layout, recognizable foods,
landmarks, Aero's anatomy, absence of unwanted text, and 3:2 proportions. For batches,
review the set together for consistent lighting and character scale. Make targeted fixes
when a visible error matters; do not run paid generations solely to test this skill.

## Save and register

Save project-bound selected artwork into the checkout, not only the generator's output
folder. Use lowercase kebab-case names under `assets/covers/countries/<place>.jpg` or
`assets/covers/cities/<place>.jpg`. Preserve the generated master when useful; high-quality
JPEG conversion is suitable for app delivery. Check actual pixel dimensions. Do not stretch
or silently crop an incorrectly composed image. Use a versioned sibling for unrequested
replacements, and tell the user its path.

For an addition to the app cover collection:

- Add its brief to the matching `countries` or `cities` array in
  `assets/covers/cover-briefs.json`. Each entry is `[group, slug, label, scene]`.
- For a city, also add `cityCountries[citySlug] = countrySlug`.
- Append the actual prompt and selected file to `assets/covers/generation-prompts.json`,
  preserving existing history.
- Run `python3 scripts/build_cover_gallery.py` to rebuild the manifest and gallery.
  The builder discovers files through the briefs and expects `<slug>.jpg`; for a
  versioned variant, keep it separate or deliberately update the consuming entry.

Follow the repository's validation and commit/push instructions when files change.
Return a visual preview and links to the image(s) or gallery, plus the prompt record.
Do not claim an app was updated when only artwork files were created.
