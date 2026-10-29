#!/usr/bin/env python3
"""Set text in the Chase display lettering (angular monoline caps) as SVG paths.

No fonts needed: every glyph is a polyline on a unit grid, so output renders
identically everywhere. Standard library only.

  python3 wordmark.py "THE CHASE" > chase.svg
  python3 wordmark.py "UNLOCK THE CITY" --height 40 --stroke 5 --fill "#DCDFE9"
  python3 wordmark.py "DISTRICT 7" --group     # bare <g> to paste into another SVG

Supported: A-Z, 0-9, space and . , : ! ? - ' /
"""
import argparse
import sys

# Each glyph: (advance width as a fraction of cap height, [polylines]).
# Points are (x, y) in 0..1 of the glyph box, y pointing down. A trailing "Z"
# closes the polyline. Chamfers of 0.2 give the faceted look of the emblem.
C = 0.2
GLYPHS = {
    "A": (0.78, [[(0, 1), (0, C), (C, 0), (1 - C, 0), (1, C), (1, 1)], [(0, 0.58), (1, 0.58)]]),
    "B": (0.78, [[(0, 0), (0.8, 0), (1, C), (1, 0.32), (0.85, 0.48), (1, 0.64), (1, 1 - C), (0.8, 1), (0, 1), "Z"], [(0, 0.48), (0.85, 0.48)]]),
    "C": (0.78, [[(1, 0), (C, 0), (0, C), (0, 1 - C), (C, 1), (1, 1)]]),
    "D": (0.78, [[(0, 0), (0.75, 0), (1, 0.25), (1, 0.75), (0.75, 1), (0, 1), "Z"]]),
    "E": (0.72, [[(1, 0), (0, 0), (0, 1), (1, 1)], [(0, 0.5), (0.8, 0.5)]]),
    "F": (0.72, [[(1, 0), (0, 0), (0, 1)], [(0, 0.5), (0.8, 0.5)]]),
    "G": (0.78, [[(1, 0), (C, 0), (0, C), (0, 1 - C), (C, 1), (1, 1), (1, 0.55), (0.55, 0.55)]]),
    "H": (0.78, [[(0, 0), (0, 1)], [(1, 0), (1, 1)], [(0, 0.5), (1, 0.5)]]),
    "I": (0.14, [[(0.5, 0), (0.5, 1)]]),
    "J": (0.66, [[(1, 0), (1, 1 - C), (1 - C, 1), (C, 1), (0, 1 - C)]]),
    "K": (0.76, [[(0, 0), (0, 1)], [(1, 0), (0.4, 0.5), (0, 0.5)], [(0.4, 0.5), (1, 1)]]),
    "L": (0.66, [[(0, 0), (0, 1), (1, 1)]]),
    "M": (0.92, [[(0, 1), (0, 0), (0.5, 0.55), (1, 0), (1, 1)]]),
    "N": (0.8, [[(0, 1), (0, 0), (1, 1), (1, 0)]]),
    "O": (0.82, [[(C, 0), (1 - C, 0), (1, C), (1, 1 - C), (1 - C, 1), (C, 1), (0, 1 - C), (0, C), "Z"]]),
    "P": (0.76, [[(0, 1), (0, 0), (0.8, 0), (1, C), (1, 0.4), (0.8, 0.56), (0, 0.56)]]),
    "Q": (0.82, [[(C, 0), (1 - C, 0), (1, C), (1, 1 - C), (1 - C, 1), (C, 1), (0, 1 - C), (0, C), "Z"], [(0.6, 0.7), (1, 1.1)]]),
    "R": (0.78, [[(0, 1), (0, 0), (0.8, 0), (1, C), (1, 0.4), (0.8, 0.56), (0, 0.56)], [(0.55, 0.56), (1, 1)]]),
    "S": (0.78, [[(1, 0), (0.15, 0), (0, 0.15), (0, 0.38), (0.15, 0.5), (0.85, 0.5), (1, 0.62), (1, 0.85), (0.85, 1), (0, 1)]]),
    "T": (0.76, [[(0, 0), (1, 0)], [(0.5, 0), (0.5, 1)]]),
    "U": (0.78, [[(0, 0), (0, 1 - C), (C, 1), (1 - C, 1), (1, 1 - C), (1, 0)]]),
    "V": (0.82, [[(0, 0), (0.5, 1), (1, 0)]]),
    "W": (1.06, [[(0, 0), (0.22, 1), (0.5, 0.35), (0.78, 1), (1, 0)]]),
    "X": (0.78, [[(0, 0), (1, 1)], [(1, 0), (0, 1)]]),
    "Y": (0.78, [[(0, 0), (0.5, 0.5), (1, 0)], [(0.5, 0.5), (0.5, 1)]]),
    "Z": (0.76, [[(0, 0), (1, 0), (0, 1), (1, 1)]]),
    "0": (0.78, [[(C, 0), (1 - C, 0), (1, C), (1, 1 - C), (1 - C, 1), (C, 1), (0, 1 - C), (0, C), "Z"], [(0.3, 0.7), (0.7, 0.3)]]),
    "1": (0.4, [[(0, 0.2), (0.6, 0), (0.6, 1)]]),
    "2": (0.76, [[(0, 0), (0.85, 0), (1, 0.15), (1, 0.38), (0.85, 0.5), (0.15, 0.5), (0, 0.62), (0, 1), (1, 1)]]),
    "3": (0.76, [[(0, 0), (0.85, 0), (1, 0.15), (1, 0.85), (0.85, 1), (0, 1)], [(0.25, 0.5), (1, 0.5)]]),
    "4": (0.76, [[(0.8, 1), (0.8, 0), (0, 0.66), (1, 0.66)]]),
    "5": (0.76, [[(1, 0), (0, 0), (0, 0.5), (0.85, 0.5), (1, 0.62), (1, 0.85), (0.85, 1), (0, 1)]]),
    "6": (0.76, [[(1, 0), (C, 0), (0, C), (0, 1 - C), (C, 1), (1 - C, 1), (1, 1 - C), (1, 0.62), (0.85, 0.5), (0, 0.5)]]),
    "7": (0.72, [[(0, 0), (1, 0), (0.35, 1)]]),
    "8": (0.78, [[(C, 0), (1 - C, 0), (1, 0.15), (1, 0.35), (0.85, 0.5), (1, 0.65), (1, 0.85), (1 - C, 1), (C, 1), (0, 0.85), (0, 0.65), (0.15, 0.5), (0, 0.35), (0, 0.15), "Z"], [(0.15, 0.5), (0.85, 0.5)]]),
    "9": (0.76, [[(0, 1), (1 - C, 1), (1, 1 - C), (1, C), (1 - C, 0), (C, 0), (0, C), (0, 0.38), (0.15, 0.5), (1, 0.5)]]),
    ".": (0.14, [[(0.5, 0.86), (0.5, 1)]]),
    ",": (0.18, [[(0.6, 0.86), (0.6, 1), (0.2, 1.15)]]),
    ":": (0.14, [[(0.5, 0.2), (0.5, 0.34)], [(0.5, 0.86), (0.5, 1)]]),
    "!": (0.14, [[(0.5, 0), (0.5, 0.66)], [(0.5, 0.86), (0.5, 1)]]),
    "?": (0.7, [[(0, 0.15), (0.15, 0), (0.85, 0), (1, 0.15), (1, 0.35), (0.5, 0.55), (0.5, 0.68)], [(0.5, 0.86), (0.5, 1)]]),
    "-": (0.5, [[(0, 0.55), (1, 0.55)]]),
    "'": (0.14, [[(0.5, 0), (0.5, 0.25)]]),
    "/": (0.6, [[(1, 0), (0, 1)]]),
    " ": (0.42, []),
}


def text_path(text, height=100, stroke=None, tracking=0.22):
    """Return (path_d, width, height_with_padding) for text set at the given cap height."""
    stroke = stroke if stroke is not None else height * 0.13
    pad = stroke / 2
    x = pad
    parts = []
    for ch in text.upper():
        if ch not in GLYPHS:
            raise SystemExit(f"wordmark.py: unsupported character {ch!r}")
        adv, lines = GLYPHS[ch]
        w = adv * height
        for line in lines:
            closed = line[-1] == "Z"
            pts = [p for p in line if p != "Z"]
            seg = " L".join(f"{x + px * w:.1f} {pad + py * height:.1f}" for px, py in pts)
            parts.append("M" + seg + (" Z" if closed else ""))
        x += w + tracking * height
    width = x - tracking * height + pad
    return " ".join(parts), width, height + 2 * pad, stroke


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("text")
    ap.add_argument("--height", type=float, default=100, help="cap height in px (default 100)")
    ap.add_argument("--stroke", type=float, help="stroke width (default 13%% of height)")
    ap.add_argument("--tracking", type=float, default=0.22, help="letter spacing as a fraction of height")
    ap.add_argument("--fill", default="url(#wm-chrome)", help='stroke colour; default is the chrome gradient')
    ap.add_argument("--group", action="store_true", help="print only a <g> element for embedding")
    a = ap.parse_args()

    d, w, h, s = text_path(a.text, a.height, a.stroke, a.tracking)
    g = (f'<g fill="none" stroke="{a.fill}" stroke-width="{s:.1f}" stroke-linejoin="miter" '
         f'stroke-linecap="square" stroke-miterlimit="4" aria-label="{a.text}">'
         f'<path d="{d}"/></g>')
    if a.group:
        print(g)
        return
    defs = ""
    if a.fill == "url(#wm-chrome)":
        defs = ('<defs><linearGradient id="wm-chrome" x1="0" y1="0" x2="0" y2="1">'
                '<stop offset="0" stop-color="#F8F8FB"/><stop offset="0.55" stop-color="#DCDFE9"/>'
                '<stop offset="1" stop-color="#8E97B3"/></linearGradient></defs>')
    sys.stdout.write(
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:.0f} {h:.0f}" width="{w:.0f}" height="{h:.0f}" '
        f'role="img" aria-label="{a.text}">{defs}{g}</svg>\n')


if __name__ == "__main__":
    main()
