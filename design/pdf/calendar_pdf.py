"""Export weekly calendar markdown to a branded A4 PDF.

    python3 design/pdf/calendar_pdf.py <theme> <out.pdf> <file.md> [more.md ...]

theme: "brand" (Eaglescroft navy cover band) or "personal" (Joshua's notebook header).
Status emojis become text badges so the PDF never depends on an emoji font.
Needs: pip install markdown; Chromium (same lookup as design/render.sh).
"""
import pathlib
import re
import subprocess
import sys

import markdown

from mdtext import unwrap

ROOT = pathlib.Path(__file__).resolve().parents[2]  # eaglescroft-socials/

BADGES = {
    "✅": ('ready', 'Ready'),
    "🛠": ('build', 'Build'),
    "📥": ('needs', 'Needs you'),
    "✍️": ('words', 'Your words'),
}


def badge(md_text):
    for emoji, (cls, label) in BADGES.items():
        md_text = md_text.replace(emoji, f'<span class="b {cls}">{label}</span>')
    return md_text.replace("★", '<span class="star">●</span>')


def body_html(paths):
    parts = []
    for i, p in enumerate(paths):
        text = badge(unwrap(pathlib.Path(p).read_text()))
        # A caption line starting with a hashtag is not a heading
        text = re.sub(r"^(>\s*)#(?=\w)", r"\1\\#", text, flags=re.M)
        html = markdown.markdown(text, extensions=["tables", "sane_lists", "nl2br"])
        if i == 0:
            m = re.search(r"<h1>(.*?)</h1>", html)
            title = m.group(1) if m else ""
            html = html.replace(m.group(0), "", 1) if m else html
        else:
            html = html.replace("<h1>", '<h1 class="section">', 1)
        parts.append(f'<section class="doc{" first" if i == 0 else ""}">{html}</section>')
    return title, "\n".join(parts)


def header(theme, title):
    if theme == "brand":
        return f"""<header class="band">
  <img class="wm" src="{ROOT}/design/brand/eagle-white-mark.png" alt="">
  <div class="brand"><img src="{ROOT}/design/brand/eagle-white-mark.png" alt=""><span>EAGLESCROFT</span></div>
  <div class="eyebrow"><span class="fm"></span>Content calendar</div>
  <h1>{title}</h1>
  <p class="sub">LinkedIn · Facebook · X  —  Abuja to the world</p>
</header>"""
    return f"""<header class="note-head">
  <img class="av" src="{ROOT}/design/personal/photos/joshua-avatar.jpg" alt="">
  <div><div class="eyebrow"><span class="fm"></span>Personal content calendar</div>
  <h1>{title}</h1>
  <p class="sub">Joshua Obaje · Founder &amp; CTO, EAGLESCROFT</p></div>
</header>"""


CSS = """
@page { size: A4; margin: 16mm 15mm 18mm; }
@page :first { margin-top: 0; }
* { box-sizing: border-box; }
html { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
body { margin: 0; font-family: Raleway, sans-serif; font-size: 10pt; line-height: 1.5; color: #48526E; }
:root { --fm: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 30 18' fill='none' stroke='%23000' stroke-width='2.2' stroke-linecap='round'%3E%3Ccircle cx='15' cy='11' r='4.6'/%3E%3Cpath d='M1.5 11H10.2M19.8 11H28.5M15 6.4V1.6'/%3E%3C/svg%3E"); }
.fm { display: inline-block; width: 1.75em; height: 1.05em; background: currentColor; -webkit-mask: var(--fm) center/contain no-repeat; mask: var(--fm) center/contain no-repeat; margin-right: .6em; vertical-align: -0.15em; }
.eyebrow { font-family: 'JetBrains Mono', monospace; font-size: 8pt; letter-spacing: .2em; text-transform: uppercase; font-weight: 500; }
h1, h2, h3 { font-family: Sora, sans-serif; color: #001E60; letter-spacing: -0.02em; line-height: 1.2; }
h1.section { font-size: 17pt; margin: 0 0 4mm; padding-top: 2mm; break-before: page; }
h2 { font-size: 13pt; margin: 8mm 0 2.5mm; padding-top: 3mm; border-top: 1px solid #E7EAF3; break-after: avoid; }
h3 { font-size: 10.5pt; margin: 5mm 0 2mm; break-after: avoid; }
p { margin: 0 0 2.5mm; }
strong { color: #0B1530; }
a { color: #2563EB; text-decoration: none; }
hr { border: 0; height: 0; margin: 2mm 0; }
code { font-family: 'JetBrains Mono', monospace; font-size: 8.5pt; background: #EEF2FB; color: #001E60; padding: .5mm 1.2mm; border-radius: 1.5mm; }
blockquote { margin: 2mm 0 4mm; padding: 3.5mm 4.5mm; background: #F4F6FB; border-left: 2.5px solid #2563EB; border-radius: 0 3mm 3mm 0; color: #0B1530; break-inside: avoid; }
blockquote p { margin: 0 0 1.6mm; }
blockquote p:last-child { margin: 0; }
ul, ol { margin: 0 0 3mm; padding-left: 5mm; }
li { margin: .6mm 0; }
table { width: 100%; border-collapse: separate; border-spacing: 0; margin: 3mm 0 5mm; font-size: 8.8pt; border: 1px solid #E7EAF3; border-radius: 3mm; overflow: hidden; break-inside: auto; }
th { background: #001E60; color: #fff; text-align: left; font-family: Sora, sans-serif; font-weight: 600; padding: 2.2mm 2.6mm; font-size: 8.5pt; }
td { padding: 2mm 2.6mm; border-top: 1px solid #E7EAF3; vertical-align: top; color: #0B1530; }
tr:nth-child(even) td { background: #F8F9FD; }
tr { break-inside: avoid; }
.b { display: inline-block; font-family: 'JetBrains Mono', monospace; font-size: 6.8pt; letter-spacing: .08em; text-transform: uppercase; font-weight: 500; padding: .5mm 1.8mm; border-radius: 9999px; margin: 0 .6mm; white-space: nowrap; vertical-align: .2mm; }
.b.ready { background: #DBEAFE; color: #1D4ED8; }
.b.build { background: #E6EBF5; color: #001E60; }
.b.needs { background: #001E60; color: #fff; }
.b.words { background: #fff; color: #001E60; border: 1px solid #8DA7D1; }
.star { color: #2563EB; font-size: 7pt; vertical-align: 1mm; }
.doc.first > p:first-of-type { font-size: 10.5pt; }

/* brand cover band */
.band { position: relative; overflow: hidden; margin: 0 -15mm 8mm; padding: 16mm 15mm 11mm; color: #fff;
  background: radial-gradient(70% 60% at 85% 0%, rgba(37,99,235,.35), transparent 60%), linear-gradient(160deg, #000F33 0%, #001E60 55%, #0A2F86 100%); }
.band .wm { position: absolute; right: -18mm; bottom: -20mm; width: 95mm; opacity: .07; }
.band .brand { display: flex; align-items: center; gap: 3mm; margin-bottom: 9mm; }
.band .brand img { height: 7mm; }
.band .brand span { font-family: Sora, sans-serif; font-weight: 600; letter-spacing: .14em; font-size: 9pt; }
.band .eyebrow { color: #93C5FD; }
.band h1 { color: #fff; font-size: 22pt; margin: 3mm 0 2mm; max-width: 150mm; }
.band .sub { color: rgba(255,255,255,.7); margin: 0; font-size: 9.5pt; }

/* personal notebook header */
.note-head { display: flex; gap: 6mm; align-items: center; margin: 0 -15mm 8mm; padding: 16mm 15mm 9mm 15mm;
  background-color: #F7F8FC; background-image: repeating-linear-gradient(180deg, transparent 0 7mm, rgba(0,30,96,.07) 7mm 7.15mm);
  border-bottom: 2px solid #2563EB; }
.note-head .av { width: 26mm; height: 26mm; border-radius: 50%; object-fit: cover; box-shadow: 0 0 0 1.2mm #fff, 0 0 0 1.6mm rgba(37,99,235,.4); }
.note-head .eyebrow { color: #2563EB; }
.note-head h1 { font-size: 20pt; margin: 2mm 0 1.5mm; }
.note-head .sub { margin: 0; font-family: 'JetBrains Mono', monospace; font-size: 7.5pt; letter-spacing: .14em; text-transform: uppercase; color: #7A86A3; }
"""


def main():
    theme, out, *paths = sys.argv[1:]
    title, body = body_html(paths)
    html = f"""<!doctype html><html><head><meta charset="utf-8">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500&family=Sora:wght@500;600;700&family=Raleway:wght@400;500;600&display=swap">
<style>{CSS}</style></head><body>{header(theme, title)}{body}</body></html>"""
    tmp = pathlib.Path(out).with_suffix(".html")
    tmp.write_text(html)
    browser = subprocess.run(
        "command -v chrome-headless-shell || ls /opt/pw-browsers/chromium_headless_shell-*/*/headless_shell 2>/dev/null | tail -1 || command -v chromium",
        shell=True, capture_output=True, text=True).stdout.strip().splitlines()[-1]
    subprocess.run([browser, "--headless", "--no-sandbox", "--disable-gpu", "--no-pdf-header-footer",
                    "--virtual-time-budget=5000", f"--print-to-pdf={pathlib.Path(out).resolve()}",
                    f"file://{tmp.resolve()}"], check=True, capture_output=True)
    tmp.unlink()
    print(out)


if __name__ == "__main__":
    main()
