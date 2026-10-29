#!/usr/bin/env python3
"""Build assets/gallery.html: every SVG in assets/ on dark and light tiles, plus the palette.

  python3 .agents/skills/chase-brand-assets/scripts/gallery.py
  open assets/gallery.html

Use it to eyeball new assets next to the existing set. Standard library only.
"""
import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
ASSETS = ROOT / "assets"


def swatches():
    tokens = json.loads((ROOT / "tokens" / "colors.json").read_text())
    out = []
    for group, items in tokens.items():
        if group.startswith("$") or group == "gradients":
            continue
        cells = "".join(
            f'<div class="sw"><span style="background:{v["$value"]}"></span><b>{k}</b><code>{v["$value"]}</code></div>'
            for k, v in items.items())
        out.append(f"<h3>{group}</h3><div class=swatches>{cells}</div>")
    return "".join(out)


def tiles():
    out = []
    for folder in sorted({p.parent for p in ASSETS.rglob("*.svg")}):
        rel = folder.relative_to(ASSETS).as_posix()
        ui = rel.endswith("icons/ui")
        cells = []
        for svg in sorted(folder.glob("*.svg")):
            src = svg.relative_to(ASSETS).as_posix()
            img = (f'<span class="mask" style="-webkit-mask-image:url({src});mask-image:url({src})"></span>'
                   if ui else f'<img src="{src}" alt="">')
            cells.append(f'<figure><div class="pair"><div class="dark">{img}</div><div class="light">{img}</div></div>'
                         f'<figcaption>{html.escape(svg.stem)}</figcaption></figure>')
        out.append(f'<h2>{rel}</h2><div class="grid{" small" if ui else ""}">{"".join(cells)}</div>')
    return "".join(out)


PAGE = """<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Chase Asset Gallery</title>
<style>
:root{{--bg:#0B0E24;--fg:#F8F8FB;--muted:#8E97B3;--card:#0F1033}}
body{{margin:0;padding:24px 16px 64px;background:var(--bg);color:var(--fg);font:14px/1.4 system-ui,sans-serif;max-width:1200px;margin-inline:auto}}
h1{{font-size:24px;letter-spacing:.08em}} h2{{margin-top:40px;font-size:16px;color:var(--muted);text-transform:uppercase;letter-spacing:.12em}}
h3{{font-size:13px;color:var(--muted);margin:20px 0 8px}}
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:12px}}
.grid.small{{grid-template-columns:repeat(auto-fill,minmax(120px,1fr))}}
figure{{margin:0;background:var(--card);border-radius:10px;padding:8px}}
figcaption{{font-size:12px;color:var(--muted);margin-top:6px;text-align:center}}
.pair{{display:grid;grid-template-columns:1fr 1fr;gap:4px}}
.pair>div{{aspect-ratio:1;display:grid;place-items:center;border-radius:6px;padding:8px}}
.dark{{background:#05040B}} .light{{background:#F2F3F8}}
img{{max-width:100%;max-height:100%}}
.mask{{width:28px;height:28px;-webkit-mask-size:contain;mask-size:contain;-webkit-mask-repeat:no-repeat;mask-repeat:no-repeat}}
.dark .mask{{background:#F8F8FB}} .light .mask{{background:#10386B}}
.swatches{{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:8px}}
.sw{{display:grid;grid-template-columns:36px 1fr;column-gap:8px;align-items:center;font-size:12px}}
.sw span{{grid-row:span 2;width:36px;height:36px;border-radius:8px;border:1px solid #ffffff22}}
.sw code{{color:var(--muted)}}
</style></head><body>
<h1>THE CHASE — ASSETS</h1>
<h2>Palette</h2>{swatches}
{tiles}
</body></html>
"""

if __name__ == "__main__":
    (ASSETS / "gallery.html").write_text(PAGE.format(swatches=swatches(), tiles=tiles()))
    print("wrote", (ASSETS / "gallery.html").relative_to(ROOT))
