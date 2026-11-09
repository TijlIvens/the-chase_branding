#!/usr/bin/env python3
"""Build the destination cover manifest and a standalone local preview."""
import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COVERS = ROOT / 'assets/covers'

def main():
    briefs = json.loads((COVERS / 'cover-briefs.json').read_text())
    entries = []
    for kind in ['countries', 'cities']:
        for group, slug, label, scene in briefs[kind]:
            country = slug if kind == 'countries' else briefs['cityCountries'][slug]
            path = COVERS / country / (slug + '.jpg') if kind == 'countries' else COVERS / country / slug / (slug + '.jpg')
            if not path.exists():
                continue
            relative = path.relative_to(COVERS).as_posix()
            entry = {'id': slug, 'name': label, 'type': kind, 'image': relative,
                     'aspectRatio': '3:2', 'description': scene,
                     'countryId': country}
            entries.append(entry)
    sections = []
    country_labels = {slug: label for _, slug, label, _ in briefs['countries']}
    for country in dict.fromkeys(entry['countryId'] for entry in entries):
        country_label = country_labels.get(country, country.replace('-', ' ').title())
        cards = []
        for entry in entries:
            if entry['countryId'] != country:
                continue
            relative = entry['image']
            label = html.escape(entry['name'])
            scene = html.escape(entry['description'])
            category = 'Country cover' if entry['type'] == 'countries' else 'City cover'
            cards.append(f'<article><a href="{relative}" download><img src="{relative}" '
                         f'alt="Illustrated {label} destination cover" loading="lazy"></a>'
                         f'<div><h3>{label}</h3><p>{category} · {scene}</p>'
                         f'<a href="{relative}" download>Download cover</a></div></article>')
        sections.append(f'<section><h2>{html.escape(country_label)}</h2><div class="grid">'+''.join(cards)+'</div></section>')
    (COVERS / 'manifest.json').write_text(json.dumps(entries, indent=2) + '\n')
    page = '''<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>The Chase — destination covers</title>
<style>*{box-sizing:border-box}body{margin:0;background:#0B0E24;color:#F8F8FB;font:15px/1.5 system-ui;padding:40px;max-width:1600px;margin:auto}header img{width:300px;max-width:100%}h1{font-size:36px}h2{margin-top:48px;color:#79DCF4}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(320px,1fr));gap:24px}article{background:#0F1033;border:1px solid #395073;overflow:hidden}article img{width:100%;aspect-ratio:3/2;object-fit:cover;display:block}article div{padding:18px}h3{font-size:22px;margin:0 0 8px}p{color:#ACBDC9}article p{font-size:13px}a{color:#4ADEF6}@media(max-width:600px){body{padding:18px}.grid{grid-template-columns:1fr}}</style></head><body>
<header><img src="../logo/lockup-horizontal.svg" alt="The Chase — Unlock the City"><h1>A world waiting to be unlocked.</h1><p>3:2 landscape covers · painted landmark vistas · Aero and Diamond Beacons</p><p>Country scenes combine landmarks, a national flag, and local foods. City scenes feature their own buildings and landmark sculptures.</p></header>'''
    (COVERS / 'index.html').write_text(page + ''.join(sections) + '</body></html>')
    print(f'Built cover gallery with {len(entries)} images.')

if __name__ == '__main__':
    main()
