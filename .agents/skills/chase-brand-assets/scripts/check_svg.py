#!/usr/bin/env python3
"""Validate SVG assets against The Chase brand rules.

  python3 .agents/skills/chase-brand-assets/scripts/check_svg.py            # every SVG in assets/
  python3 .agents/skills/chase-brand-assets/scripts/check_svg.py path.svg   # specific files

Exit code 0 = all pass, 1 = at least one error. Standard library only.

Rules
  all       well-formed XML, <svg> root with xmlns + viewBox, accessible name
            (aria-label or <title>), no <script>/<image>/<foreignObject>,
            no external references, every hex colour in tokens/colors.json
  icons/ui  viewBox 0 0 24 24, colour only via currentColor, stroke-width 2
  icons/*   (other icon sets) viewBox 0 0 64 64, every id prefixed "<filename>-"
"""
import json
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
NS = "{http://www.w3.org/2000/svg}"
HEX = re.compile(r"#([0-9A-Fa-f]{6}|[0-9A-Fa-f]{3})\b")


def palette():
    def walk(node):
        if isinstance(node, dict):
            if "$value" in node and isinstance(node["$value"], str):
                yield from HEX.findall(node["$value"])
            for v in node.values():
                yield from walk(v)
    tokens = json.loads((ROOT / "tokens" / "colors.json").read_text())
    return {"#" + h.upper() for h in walk(tokens)}


def check(path, allowed):
    errors, warnings = [], []
    text = path.read_text()
    try:
        root = ET.fromstring(text)
    except ET.ParseError as e:
        return [f"not well-formed XML: {e}"], []
    if root.tag != NS + "svg":
        errors.append("root element is not <svg> in the SVG namespace (missing xmlns?)")
    vb = root.get("viewBox")
    if not vb:
        errors.append("missing viewBox")
    if not root.get("aria-label") and root.find(NS + "title") is None:
        errors.append("no accessible name: add aria-label or <title>")
    for bad in ("script", "image", "foreignObject"):
        if any(True for _ in root.iter(NS + bad)):
            errors.append(f"<{bad}> is not allowed")
    if re.search(r'(href|src)\s*=\s*"(https?:|data:|//)', text) or "@import" in text:
        errors.append("external or embedded reference (href/src/@import) is not allowed")

    colours = {"#" + h.upper() for h in HEX.findall(text)}
    off = sorted(c for c in colours if len(c) == 7 and c not in allowed)
    if off:
        errors.append("colours not in tokens/colors.json: " + ", ".join(off))

    rel = path.resolve().as_posix()
    if "/icons/ui/" in rel:
        if vb != "0 0 24 24":
            errors.append(f'UI icon viewBox must be "0 0 24 24" (got {vb!r})')
        if colours:
            errors.append("UI icons use currentColor only, no hex colours")
        if root.get("stroke") != "currentColor":
            errors.append('UI icon root needs stroke="currentColor"')
        if root.get("stroke-width") != "2":
            errors.append('UI icon root needs stroke-width="2"')
    elif "/icons/" in rel:
        if vb != "0 0 64 64":
            errors.append(f'game icon viewBox must be "0 0 64 64" (got {vb!r})')
        stem = path.stem
        for el in root.iter():
            i = el.get("id")
            if i and not i.startswith(stem + "-"):
                errors.append(f'id "{i}" must start with "{stem}-" so icons can be inlined together')
    if len(text) > 20_000 and "/icons/" in rel:
        warnings.append(f"{len(text)} bytes; icons should stay under 20 KB")
    return errors, warnings


def main(argv):
    allowed = palette()
    files = [Path(a) for a in argv] or sorted((ROOT / "assets").rglob("*.svg"))
    failed = 0
    for f in files:
        errors, warnings = check(f, allowed)
        name = f.resolve().relative_to(ROOT) if f.resolve().is_relative_to(ROOT) else f
        for w in warnings:
            print(f"WARN  {name}: {w}")
        if errors:
            failed += 1
            for e in errors:
                print(f"FAIL  {name}: {e}")
    print(f"{len(files) - failed}/{len(files)} SVGs pass")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
