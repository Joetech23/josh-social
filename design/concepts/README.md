# Concepts

Exploratory posts in the "bold" style taken from the reference board (Oct 2026):
big weight-contrast Sora headlines, one hero visual per slide, floating UI chips,
grid texture and a pill footer bar with site and socials. Translated into the
Eaglescroft palette: the references' vivid purple becomes saturated navy-to-royal-blue,
and there are no warm accents.

| Folder | What |
| --- | --- |
| `ai-reply/` | 3-slide Ground School carousel: WhatsApp AI assistant (cover, audience question, CTA) |
| `3d-set/` | Three single posts led by real 3D renders: launch coin, data-safety lock, argue-with-AI bubble |

Render a slide: `design/render.sh design/concepts/ai-reply/slide-1.html`

Icons: `design/icons/icons.css` (`<span class="ic i-zap"></span>`). Add an SVG to
`design/icons/ui/` or `design/icons/social/`, then run `python3 design/icons/build-icons.py`.

## 3D objects

`design/3d/` renders brand objects with three.js in headless Chromium, as transparent PNGs:
`design/3d/render-3d.sh <eagle|coin|bubble|lock> [size]` → `design/3d/out/<asset>.png`.
The eagle is extruded from `design/brand/eagle-mark.svg` (traced from the official mark), so
the 3D eagle and coin always match the logo. Add new objects as another `asset` branch in
`design/3d/render.html`.

Shared styles for this look live in `design/templates/bold.css`.
