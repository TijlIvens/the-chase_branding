# Destination covers

Full-bleed 3:2 landscape illustrations for the app's country and city overview cards.

- 15 country folders: `<country>/<country>.jpg` contains the national panorama with its flag, foods, and landmarks.
- 38 city subfolders: `<country>/<city>/<city>.jpg` contains the city landmark cover.
- Example: `belgium/belgium.jpg`, `belgium/gent/gent.jpg`, and `czech-republic/prague/prague.jpg`.
- `index.html`: labeled browser gallery with individual downloads.
- `manifest.json`: image paths, place labels, and scene descriptions.
- `cover-briefs.json`: shared art direction, original project references, and every destination brief.
- `generation-prompts.json`: exact prompts and source-image records for the selected images.
- `preview-countries.jpg` and `preview-cities.jpg`: contact sheets.
- `preview-new-covers.jpg`: the latest batch of destination additions.

The painted architectural detail, blue-hour lighting, golden city lights, Aero design,
and cyan Diamond Beacons follow the existing project illustrations. Architecture is
the primary subject; Aero and the beacon are supporting foreground elements.
Panoramas are artistic compositions combining local landmarks, rather than literal
geographic viewpoints. Country scenes intentionally combine different cities.

Images contain no location names or logos, so the app can render localized titles.
Use a 3:2 image area to retain the complete composition. These are cover illustrations,
separate from the 64 px SVG game icons.

Generated with the built-in image-generation tool, using the project's original
illustrations and the initial Belgium cover as style/character references. Selected
images are delivered as high-quality JPEGs for convenient app use. Original reference
files in `base-images/` were left unchanged.

Rebuild the manifest and gallery after updating an image:

```sh
python3 scripts/build_cover_gallery.py
```

Create another cover with `$chase-cover-images`, for example: “Use
$chase-cover-images to make a country cover for Greece.” The reusable skill lives in
[`.agents/skills/chase-cover-images/SKILL.md`](../../.agents/skills/chase-cover-images/SKILL.md).
