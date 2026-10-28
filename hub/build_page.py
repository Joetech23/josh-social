"""Render hub/index.html from the template (inlines the traced eagle mark)."""
import pathlib

HUB = pathlib.Path(__file__).resolve().parent
svg = (HUB.parent / "design" / "brand" / "eagle-mark.svg").read_text().strip()
svg = svg.replace('fill="#001E60"', 'fill="currentColor"').replace("<svg ", '<svg class="eagle" aria-hidden="true" ', 1)
page = (HUB / "index.template.html").read_text().replace("__EAGLE__", svg)
(HUB / "index.html").write_text(page)
print("hub/index.html", len(page), "bytes")
