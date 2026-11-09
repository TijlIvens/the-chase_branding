# Shared generation prompt

Replace bracketed fields with concrete details; omit inapplicable lines. The references
are actual image inputs, not textual placeholders. Use the same reference order for a batch.

```text
Use case: illustration-story.
Deliverable: one full-bleed app overview cover, landscape 3:2, 1536 × 1024.
Destination: [place and country if needed].

References: Image 1 is the existing The Chase destination cover for collection style,
lighting, composition, and Aero scale. Image 2 is original project drawing style.
Image 3 supplies Aero's identity. They are reference material, not scenes to copy.
[For an edit, instead explicitly identify the edit target and what must stay unchanged.]

Scene: [country panorama or city vista with named buildings, landmark sculpture,
landscape, and foreground]. Harmonize the subjects into one deliberately composed
vista; retain recognizable architecture and sculpture. Landmarks dominate.

[COUNTRY ONLY: correct flag and its specific layout, on one modest left-side flagpole,
unfurled and unobstructed. A small foreground table with 2–3 named local foods;
no packaging labels. Accurate natural flag/food colors.]
[CITY ONLY: named local statue/fountain/monument/public sculpture, secondary to
architecture. No food table or flag unless requested.]

Match the references' detailed semi-realistic painted adventure-game style, crisp
architectural drawing, soft painted shading, natural stone and foliage, atmospheric
depth, blue-hour sky, gently gold-lit city, deep navy shadows, cyan magic, and violet
haze. Keep lighting, detail, and character size consistent with the cover collection.

Small friendly Aero at lower right: teal beaked head, slate blue scaled serpent body,
lavender belly, exactly two swept-back golden horns, purple eyes, cyan rune lines,
smiling closed mouth, no limbs or wings. Roughly 15% image area maximum. One small
faceted blue Diamond Beacon hovers over a thin cyan ring nearby. Architecture receives
about 75% of visual attention. Quieter darker lower-left space for an app-rendered title.

Compose for the 3:2 frame. No typography, location names, logos, watermarks, borders,
badge frames, or separate collage panels. No flat vector icons, photorealism, oversized
people, aggressive Aero, or sci-fi replacements of historic buildings.
```

## Easy invocations

- “Use $chase-cover-images to make a country cover for Greece.”
- “Use $chase-cover-images to create a city cover for Athens, including the Acropolis and a landmark statue.”
- “Use $chase-cover-images to make covers for Austria, Vienna, and Salzburg.”
- “Use $chase-cover-images to add local foods and the flag to this country cover; keep its landmarks and composition.”
- “Use $chase-cover-images for a daytime Lisbon cover in the same drawing style.”

The first and third examples imply flags and local foods on country covers, and local
buildings and sculptures on city covers. Do not make the user repeat the established defaults.
