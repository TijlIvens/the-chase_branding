#!/usr/bin/env python3
"""Build destination badges from the game-icon template and existing character art."""
from pathlib import Path
import json, re, html
R=Path(__file__).resolve().parents[1]
# Landmark silhouettes are deliberately simplified for a 64 px game-icon grid.
L={
'brussels':('Atomium','M16 18 32 12 46 21 43 38 24 40 16 18M32 12v20l14-11M16 18l16 14 11 6M24 40l8-8'),
'antwerp':('Cathedral of Our Lady','M21 44V26h5V18h2V11l2-7 2 7v7h2v8h5v18M18 44V33l4-5 4 5v11M34 44V30l6-5 7 5v14'),
'bruges':('Belfry of Bruges','M24 44V23h2V13h3V8h2V5h2v3h2v5h3v10h2v21M20 44V31h24v13M28 18h8M28 26h8'),
'amsterdam':('Canal houses','M12 44V25l5-6 5 6v19M23 44V22l6-7 6 7v22M36 44V27l5-7 6 7v17M14 30h5m7-3h6m7 5h5M12 46h36'),
'rotterdam':('Erasmus Bridge','M12 42h39M33 13l-6 29h9l-3-29 16 29M33 18 14 42M32 24 20 42M32 31 25 42'),
'london':('Elizabeth Tower','M22 44V23h3V15l5-9 5 9v8h3v21M24 23h12M24 35h12M27 15h6M30 26v5l3 1M40 44V31h9v13'),
'edinburgh':('Edinburgh Castle','M13 43V28h5v-7h6v7h5V17h5v-5h6v5h4v11h6v15M13 39l12-3 12 2 13-1M31 24h4m4 7h4m-25 0h4'),
'paris':('Eiffel Tower','M17 45 25 32 29 18l3-12 3 12 4 14 8 13h-8l-7-9-7 9zM24 32h16M27 23h10M22 39h20'),
'lyon':('Fourviere Basilica','M16 44V23h4V13l2-5 2 5v10h4v-6h8v6h4V13l2-5 2 5v10h4v21M20 30h24M28 44V34h8v10'),
'berlin':('Brandenburg Gate','M12 25h40l-5-5H17zM15 44V28h4v16m5 0V28h4v16m8 0V28h4v16m5 0V28h4v16M12 45h40M28 20v-6h8v6M32 14V9'),
'munich':('Frauenkirche','M17 44V20h2v-6q4-9 8 0v6h2v24M35 44V20h2v-6q4-9 8 0v6h2v24M29 30h6M21 24h4m14 0h4M21 32h4m14 0h4'),
'rome':('Colosseum','M12 43V26q19-13 40-2v19zM12 32q20-10 40-3M12 39q20-8 40-3M18 27v14m7-17v16m8-18v18m8-17v18m7-15v16'),
'milan':('Milan Cathedral','M12 44V32l4-5 3 5 4-9 4 6 5-17 5 17 4-6 4 9 3-5 4 5v12zM19 37v7m7-9v9m6-14v14m6-9v9m7-7v7'),
'madrid':('Puerta de Alcala','M12 44V24h40v20M17 44V32q4-7 8 0v12m3 0V30q4-7 8 0v14m3 0V32q4-7 8 0v12M15 24v-5h34v5M28 19v-6h8v6'),
'barcelona':('Sagrada Familia','M16 44l2-18 3-13 3 13 2 18M27 44l1-23 4-15 4 15 1 23M39 44l2-18 3-13 3 13 2 18M19 35h27M23 44V33h18v11'),
'lisbon':('Belem Tower','M18 44V30h8V14h3v-4h6v4h4v16h9v14M26 20h13M26 25h13M17 30h32M22 37v7m8-9v9m8-9v9m6-7v7'),
'porto':('Dom Luis I Bridge','M12 25h40M12 42h40M13 42q19-31 38 0M17 25v12m7-12v5m8-5v3m8-3v5m7-5v12'),
'new-delhi':('India Gate','M18 44V20h28v24h-9V30q-5-6-10 0v14zM16 20h32v-5H16zM22 15V10h20v5M15 44h34'),
'mumbai':('Gateway of India','M13 44V24h5V14h5v10h18V14h5v10h5v20H38V32q-6-8-12 0v12zM18 18h5m18 0h5M26 24v-8h12v8'),
'new-york':('Empire State Building','M23 44V25h4V15h3V8h2V4h1v4h2v7h3v10h4v19M12 44V31h8v13M45 44V27h6v17M29 22v18m6-18v18'),
'san-francisco':('Golden Gate Bridge','M12 30q8 4 13-9 7 15 15 0 6 11 12 9M24 44V15h4v29m11 0V15h4v29M12 37h40M16 31v6m19-9v9m13-7v7'),
'rio-de-janeiro':('Christ the Redeemer','M28 13h8v7l17 5-1 4-16-2 2 15h-4l-2-12-2 12h-4l2-15-16 2-1-4 17-5zM20 45l12-5 13 5'),
'sao-paulo':('Sao Paulo Museum of Art','M12 22h40v15H12zM15 18h4v26h-4zM45 18h4v26h-4zM20 26h24M20 31h24M12 45h40'),
'beijing':('Temple of Heaven','M13 43h38M16 39h32l-5-5H21zM18 30h28l-6-5H24zM22 21h20l-8-8h-4zM24 34v-4m16 4v-4M28 25v-4m8 4v-4M32 13V8'),
'shanghai':('Oriental Pearl Tower','M28 44l2-11-5-6 2-6 4-3V9h2v9l4 3 2 6-5 6 2 11M29 11h6M28 23h8M41 44V19l6-7 4 32M14 44V29h7v15'),
'tokyo':('Tokyo Tower','M17 45l9-16 4-15 2-9 2 9 4 15 9 16M23 33h18M26 25h12M28 17h8M21 39h22M23 33l18 6m-15-10 12-4'),
'kyoto':('Toji Pagoda','M12 43h40l-7-5H19zM15 34h34l-7-5H22zM18 25h28l-7-5H25zM23 16h18l-9-7zM26 38v-4m12 4v-4M28 29v-4m8 4v-4M30 20v-4m4 4v-4M32 9V4'),
'bangkok':('Wat Arun','M14 44l5-7 3-15 3 15 3 7M26 44l2-22 4-17 4 17 2 22M38 44l3-7 3-15 3 15 5 7M28 29h8M27 35h10M30 18h4'),
'chiang-mai':('Doi Suthep','M15 44h34l-6-6H21zM21 38l5-9h12l5 9M26 29l3-9h6l3 9M29 20l3-13 3 13M20 42h24M28 25h8'),
}
COUNTRIES=[('Belgium','BE',['brussels','antwerp','bruges']),('The Netherlands','NL',['amsterdam','rotterdam']),('United Kingdom','GB',['london','edinburgh']),('France','FR',['paris','lyon']),('Germany','DE',['berlin','munich']),('Italy','IT',['rome','milan']),('Spain','ES',['madrid','barcelona']),('Portugal','PT',['lisbon','porto']),('India','IN',['new-delhi','mumbai']),('USA','US',['new-york','san-francisco']),('Brazil','BR',['rio-de-janeiro','sao-paulo']),('China','CN',['beijing','shanghai']),('Japan','JP',['tokyo','kyoto']),('Thailand','TH',['bangkok','chiang-mai'])]
T=(R/'.agents/skills/chase-brand-assets/templates/game-icon.svg').read_text()
def inner(file,prefix):
 s=(R/f'assets/icons/game/{file}.svg').read_text()
 s=re.sub(r'^<svg[^>]*>|</svg>\s*$','',s).strip()
 return s.replace(f'{file}-',f'{prefix}-{file}-')
OUT=R/'assets/icons/game'; entries=[]
def build(name,label,city,kind):
 defs=T[T.index('  <defs>'):T.index('  <!-- Body:')].replace('name-',name+'-')
 landmark,path=L[city]
 # Country hexagonal crest and city chamfered tile share a family but different silhouettes.
 frame='M32 3 57 16v31L32 61 7 47V16z' if kind=='country' else 'M14 4h36l10 10v36L50 60H14L4 50V14z'
 nodes=''.join(f'<circle cx="{x}" cy="{y}" r="2.5" fill="#DCDFE9" stroke="#1F2534" stroke-width="0.6"/>' for x,y in [(16,18),(32,12),(46,21),(43,38),(24,40),(32,32)]) if city=='brussels' else ''
 s=f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="64" height="64" role="img" aria-label="{html.escape(label)} — Aero and Diamond Beacon at {landmark}">
{defs}
<path d="{frame}" fill="#0B0E24" stroke="url(#{name}-chrome)" stroke-width="1.5"/>
<path d="M10 17 32 54 54 17" fill="none" stroke="url(#{name}-beam)" stroke-width="1.5"/>
<path d="M13 46V33h6v13m22 0V30h6v16M11 47h42" fill="#10386B" stroke="#10386B" stroke-width="2"/>
<path d="{path}" fill="none" stroke="#DCDFE9" stroke-width="1.5" stroke-linecap="square" stroke-linejoin="miter"/>
{nodes}
<path d="M11 48h42" stroke="url(#{name}-beam)" stroke-width="1.5"/>
<g transform="translate(5 28) scale(0.4)">{inner('aero',name)}</g>
<g transform="translate(29 29) scale(0.48)">{inner('beacon',name)}</g>
<path d="M47 10v6m-3-3h6" stroke="#E8F6FC" stroke-width="1"/>
</svg>'''
 (OUT/f'{name}.svg').write_text(s)
 entries.append(dict(name=name,label=label,kind=kind,landmark=landmark,city=city))
for country,code,cities in COUNTRIES:
 slug={'The Netherlands':'netherlands','United Kingdom':'united-kingdom','USA':'usa'}.get(country,country.lower())
 build('country-'+slug,country,cities[0],'country')
 for city in cities: build('city-'+city,city.replace('-',' ').title(),city,'city')
(R/'assets/destinations.json').write_text(json.dumps(entries,indent=2)+'\n')
# Labels live outside the tiny artwork so the icon remains useful at 64 px.
rows=[]
for country,code,cities in COUNTRIES:
 slug={'The Netherlands':'netherlands','United Kingdom':'united-kingdom','USA':'usa'}.get(country,country.lower())
 cards=[]
 for name in ['country-'+slug]+['city-'+c for c in cities]:
  e=next(e for e in entries if e['name']==name)
  cards.append(f'<article><div class="pair"><img src="icons/game/{name}.svg" alt="{e["label"]}"><img class="light" src="icons/game/{name}.svg" alt="{e["label"]} on light"></div><h3>{e["label"]}</h3><p>{"Country badge" if e["kind"]=="country" else "City badge"} · {e["landmark"]}</p><a href="icons/game/{name}.svg" download>Download SVG</a></article>')
 rows.append(f'<section><h2>{country} <small>{code}</small></h2><div class="grid">'+''.join(cards)+'</div></section>')
(R/'assets/destinations.html').write_text('''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>The Chase · Destinations</title><style>
*{box-sizing:border-box}body{background:#0B0E24;color:#F8F8FB;font:16px/1.5 system-ui;margin:0;padding:48px;max-width:1440px;margin-inline:auto}header{border-bottom:1px solid #395073;padding-bottom:32px}header img{width:280px;max-width:100%}h1{font-size:40px;margin-bottom:8px}p{color:#8E97B3}h2{margin-top:40px}small{color:#4ADEF6;font-size:12px;margin-left:12px}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:16px}article{background:#0F1033;border:1px solid #395073;padding:18px}h3{margin:16px 0 4px}article p{font-size:12px;min-height:36px}.pair{display:flex;gap:8px}.pair img{width:calc(50% - 4px);padding:10px;background:#05040B}.pair .light{background:#E8F6FC}a{color:#4ADEF6;font-size:13px}@media(max-width:600px){body{padding:20px}h1{font-size:28px}}</style><header><img src="logo/lockup-horizontal.svg" alt="The Chase — Unlock the City"><h1>Unlock a world of cities.</h1><p>14 country crests. 29 city badges. Aero and Diamond Beacons, wherever you explore.</p><p>Country crests feature a representative landmark. City badges feature their own skyline. Each is shown on dark and light.</p></header>'''+''.join(rows)+'</html>')
print(f'Built {len(entries)} destination icons.')
