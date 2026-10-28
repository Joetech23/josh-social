"""Pull official-colour brand logos from simple-icons into design/logos/.

    npm pack simple-icons && tar -xzf simple-icons-*.tgz   (anywhere)
    python3 design/logos/build-logos.py <path-to/package> slug [slug ...]

Writes <slug>.svg (filled with the brand's own hex) and updates logos.json with title,
hex and the brand's usage-guidelines URL. Logos are used to *refer* to products only:
never recolour them into Eaglescroft blue, never lock them up beside our logo.
Not in simple-icons (removed at the brands' request): OpenAI/ChatGPT, Canva, CapCut,
LinkedIn. Get those from the brands' official press/brand pages.
"""
import json
import pathlib
import re
import sys

here = pathlib.Path(__file__).parent
pkg = pathlib.Path(sys.argv[1])
data = json.loads((pkg / "data" / "simple-icons.json").read_text())
icons = data["icons"] if isinstance(data, dict) else data


def slug_of(icon):
    if icon.get("slug"):
        return icon["slug"]
    s = icon["title"].lower().replace("+", "plus").replace(".", "dot").replace("&", "and")
    return re.sub(r"[^a-z0-9]", "", s)


index = {slug_of(i): i for i in icons}
meta_path = here / "logos.json"
meta = json.loads(meta_path.read_text()) if meta_path.exists() else {}
for slug in sys.argv[2:]:
    icon = index[slug]
    svg = (pkg / "icons" / f"{slug}.svg").read_text()
    svg = svg.replace("<svg ", f'<svg fill="#{icon["hex"]}" ', 1)
    svg = re.sub(r"<title>.*?</title>", "", svg)
    (here / f"{slug}.svg").write_text(svg)
    meta[slug] = {"title": icon["title"], "hex": icon["hex"], "guidelines": icon.get("guidelines", "")}
meta_path.write_text(json.dumps(meta, indent=2) + "\n")
print(f"{len(sys.argv) - 2} logos -> {here}")
