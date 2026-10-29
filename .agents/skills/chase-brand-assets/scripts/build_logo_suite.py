#!/usr/bin/env python3
"""Regenerate every logo derivative from assets/logo/emblem.svg.

  python3 .agents/skills/chase-brand-assets/scripts/build_logo_suite.py

Writes (overwrites) in assets/:
  logo/emblem-flat.svg       emblem without blur filters (small sizes, email)
  logo/emblem-mono.svg       single colour, uses currentColor
  logo/wordmark.svg          "THE CHASE" + tagline, chrome on transparent
  logo/wordmark-ink.svg      same in midnight/shield blue, for light backgrounds
  logo/lockup-horizontal.svg emblem left, wordmark right
  logo/lockup-horizontal-ink.svg  flat emblem + ink wordmark, for light backgrounds
  logo/lockup-stacked.svg    emblem above wordmark (matches the original key art)
  app/app-icon.svg           1024x1024 store icon on the night-sky backdrop
  app/favicon.svg            simplified emblem for 16-48 px

Edit emblem.svg (or the MONO paths below) and rerun. Standard library only.
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from wordmark import text_path  # noqa: E402

ROOT = Path(__file__).resolve().parents[4]
LOGO = ROOT / "assets" / "logo"
APP = ROOT / "assets" / "app"

CHROME = ('<linearGradient id="{id}" x1="0" y1="0" x2="0" y2="1">'
          '<stop offset="0" stop-color="#F8F8FB"/><stop offset="0.55" stop-color="#DCDFE9"/>'
          '<stop offset="1" stop-color="#8E97B3"/></linearGradient>')

# Geometry shared with emblem.svg, used for the flat/mono variants.
SHIELD = "M88 92 L210 112 L256 52 L302 112 L424 92 L354 186 L366 234 L320 250 L342 308 L282 286 L256 332 L230 286 L170 308 L192 250 L146 234 L158 186 Z"
CORE = "M142 114 L222 132 L256 88 L290 132 L370 114 L326 182 L334 216 L298 228 L310 274 L274 262 L256 296 L238 262 L202 274 L214 228 L178 216 L186 182 Z"
RING = "M190 152 L234 160 L256 132 L278 160 L322 152 L298 196 L304 220 L256 236 L208 220 L214 196 Z"
BLADE = "M256 118 L270 196 L256 244 L242 196 Z"
PILLARS = "M236 248 h10 v34 l-10 -6 z M266 248 h10 v28 l-10 6 z"
SHARDS = "M120 222 L146 204 L146 236 Z M392 222 L366 204 L366 236 Z"
BEAM = "M60 236 L256 460 L452 236"
CITY = "M176 460V372h10v-12h10v-14h8v14h8v-30h12v30h6v-46l6-12 6 12v46h8v-26h12v26h6v-18h10v18h8v-36h12v36h10v22h12v-10h10v100z"


def svg(w, h, body, label, extra=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:g} {h:g}" width="{w:g}" height="{h:g}" '
            f'role="img" aria-label="{label}"{extra}>\n{body}\n</svg>\n')


def emblem_inner():
    """Body of emblem.svg (defs + shapes) without the outer <svg> and <title>."""
    src = (LOGO / "emblem.svg").read_text()
    body = re.search(r"<svg[^>]*>(.*)</svg>", src, re.S).group(1)
    return re.sub(r"\s*<title[^>]*>.*?</title>", "", body, flags=re.S).strip()


def flat_emblem(prefix):
    """Emblem without filters; ids prefixed so several copies can share a document."""
    return f'''<defs>
  {CHROME.format(id=prefix + "chrome")}
  <linearGradient id="{prefix}beam" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#2590D9"/><stop offset="0.45" stop-color="#4ADEF6"/><stop offset="0.75" stop-color="#9B6BFF"/><stop offset="1" stop-color="#662DC2"/></linearGradient>
  <linearGradient id="{prefix}city" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1F62BC"/><stop offset="1" stop-color="#4ADEF6"/></linearGradient>
  <clipPath id="{prefix}v"><path d="M72 240 L256 448 L440 240 Z"/></clipPath>
</defs>
<g clip-path="url(#{prefix}v)"><path fill="url(#{prefix}city)" d="{CITY}"/></g>
<path d="{BEAM}" fill="none" stroke="url(#{prefix}beam)" stroke-width="12"/>
<path fill="url(#{prefix}chrome)" d="{SHIELD}"/>
<path fill="#10386B" d="{CORE}"/>
<path fill="none" stroke="url(#{prefix}chrome)" stroke-width="14" d="{RING}"/>
<path fill="#F8F8FB" d="{BLADE}"/>
<path fill="url(#{prefix}chrome)" d="{PILLARS} {SHARDS}"/>'''


def mono_emblem():
    return f'''<g fill="currentColor">
  <path fill-rule="evenodd" d="{SHIELD} {CORE}"/>
  <path d="{BLADE} {PILLARS} {SHARDS}"/>
  <path d="{CITY}" clip-path="url(#mono-v)"/>
</g>
<defs><clipPath id="mono-v"><path d="M100 272 L256 448 L412 272 Z"/></clipPath></defs>
<path d="{RING}" fill="none" stroke="currentColor" stroke-width="14"/>
<path d="{BEAM}" fill="none" stroke="currentColor" stroke-width="12"/>'''


def text_block(prefix, cap=80, tag_cap=26, ink=False):
    """Two-line wordmark (ink=True for light backgrounds). Returns (svg_body, width, height)."""
    d1, w1, h1, s1 = text_path("THE CHASE", cap)
    d2, w2, h2, s2 = text_path("UNLOCK THE CITY", tag_cap, stroke=tag_cap * 0.14, tracking=0.55)
    gap = cap * 0.42
    w = max(w1, w2)
    main, tag = ("#0F1033", "#10386B") if ink else (f"url(#{prefix}wm)", "#DCDFE9")
    body = ("" if ink else f'<defs>{CHROME.format(id=prefix + "wm")}</defs>')
    body += (f'<g fill="none" stroke="{main}" stroke-width="{s1:.1f}" stroke-linecap="square">'
             f'<path transform="translate({(w - w1) / 2:.1f} 0)" d="{d1}"/></g>'
             f'<g fill="none" stroke="{tag}" stroke-width="{s2:.1f}" stroke-linecap="square">'
             f'<path transform="translate({(w - w2) / 2:.1f} {h1 + gap:.1f})" d="{d2}"/></g>')
    return body, w, h1 + gap + h2


def write(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)
    print("wrote", path.relative_to(ROOT))


def main():
    write(LOGO / "emblem-flat.svg", svg(512, 512, flat_emblem("ef-"), "The Chase emblem"))
    write(LOGO / "emblem-mono.svg", svg(512, 512, mono_emblem(), "The Chase emblem", ' fill="none" color="#F8F8FB"'))

    tb, tw, th = text_block("wm-")
    write(LOGO / "wordmark.svg", svg(round(tw), round(th), tb, "The Chase: Unlock the City"))
    write(LOGO / "wordmark-ink.svg", svg(round(tw), round(th), text_block("wi-", ink=True)[0], "The Chase: Unlock the City"))

    # Horizontal lockup: emblem height = 1.9x wordmark block height.
    em = th * 1.9
    sc = em / 512
    gap = em * 0.12
    body = (f'<g transform="scale({sc:.4f})">{emblem_inner()}</g>'
            f'<g transform="translate({em + gap:.1f} {(em - th) / 2:.1f})">{text_block("lh-")[0]}</g>')
    write(LOGO / "lockup-horizontal.svg", svg(round(em + gap + tw), round(em), body, "The Chase: Unlock the City"))
    body = (f'<g transform="scale({sc:.4f})">{flat_emblem("li-")}</g>'
            f'<g transform="translate({em + gap:.1f} {(em - th) / 2:.1f})">{text_block("li-", ink=True)[0]}</g>')
    write(LOGO / "lockup-horizontal-ink.svg", svg(round(em + gap + tw), round(em), body, "The Chase: Unlock the City"))

    # Stacked lockup.
    em = tw * 0.9
    sc = em / 512
    W = max(em, tw)
    body = (f'<g transform="translate({(W - em) / 2:.1f} 0) scale({sc:.4f})">{emblem_inner()}</g>'
            f'<g transform="translate({(W - tw) / 2:.1f} {em * 0.94:.1f})">{text_block("ls-")[0]}</g>')
    write(LOGO / "lockup-stacked.svg", svg(round(W), round(em * 0.94 + th), body, "The Chase: Unlock the City"))

    # App icon: 1024 square, iOS-style corner radius (masking is applied by the OS; keep the rect for previews).
    body = ('<defs><radialGradient id="ai-bg" cx="0.5" cy="0.42" r="0.75">'
            '<stop offset="0" stop-color="#201153"/><stop offset="0.55" stop-color="#0B0E24"/>'
            '<stop offset="1" stop-color="#05040B"/></radialGradient></defs>'
            '<rect width="1024" height="1024" rx="228" fill="url(#ai-bg)"/>'
            f'<g transform="translate(112 96) scale(1.5625)">{emblem_inner()}</g>')
    write(APP / "app-icon.svg", svg(1024, 1024, body, "The Chase app icon"))

    # Favicon: shield + blade + beam only, thick enough for 16 px.
    body = f'''<defs>{CHROME.format(id="fv-chrome")}
<linearGradient id="fv-beam" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#4ADEF6"/><stop offset="1" stop-color="#9B6BFF"/></linearGradient></defs>
<rect width="512" height="512" rx="96" fill="#0B0E24"/>
<path d="M60 236 L256 470 L452 236" fill="none" stroke="url(#fv-beam)" stroke-width="40"/>
<path fill="url(#fv-chrome)" d="{SHIELD}"/>
<path fill="#1F62BC" d="{CORE}"/>
<path fill="#F8F8FB" d="M256 100 L280 196 L256 260 L232 196 Z"/>'''
    write(APP / "favicon.svg", svg(512, 512, body, "The Chase"))


if __name__ == "__main__":
    main()
