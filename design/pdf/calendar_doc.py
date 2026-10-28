"""Turn a calendar markdown file into simple HTML for Google Docs import.

    python3 design/pdf/calendar_doc.py <file.md> > out.html

4-byte emojis garble on Docs import, so status emojis become bracketed text labels.
"""
import re
import sys

import markdown

from mdtext import unwrap

LABELS = {"✅": "[READY]", "🛠": "[BUILD]", "📥": "[NEEDS YOU]", "✍️": "[YOUR WORDS]", "★": "*"}

text = unwrap(open(sys.argv[1]).read())
for k, v in LABELS.items():
    text = text.replace(k, v)
text = re.sub(r"`([^`]*)`", r"\1", text)                      # no code spans in Docs
text = re.sub(r"^(>\s*)#(?=\w)", r"\1\\#", text, flags=re.M)   # hashtags are not headings
html = markdown.markdown(text, extensions=["tables", "sane_lists", "nl2br"])
print('<html><head><meta charset="utf-8"></head><body style="font-family:Arial">' + html + "</body></html>")
