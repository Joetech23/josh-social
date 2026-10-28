"""Shared markdown clean-up for calendar exports (PDF and Google Docs)."""
import re

# A line that starts like this is an intentional new line inside a caption
KEEP = re.compile(r"^(→|✓|✗|\d+\.\s|-\s|\[|#|\*\*|What (worked|broke|I learned)|The one I)")


def unwrap(text):
    """Join hard-wrapped lines back into sentences; keep list-like breaks."""
    out = []
    for line in text.split("\n"):
        if out:
            prev = out[-1]
            pq, lq = prev.startswith(">"), line.startswith(">")
            body = line[1:].strip() if lq else line.strip()
            prev_body = prev[1:].strip() if pq else prev.strip()
            joinable = (pq == lq and body and prev_body and not KEEP.match(body)
                        and not prev_body.startswith(("|", "#")) and not body.startswith("|")
                        and not prev_body.endswith(":"))
            if joinable:
                out[-1] = prev.rstrip() + " " + body
                continue
        out.append(line)
    return "\n".join(out)
