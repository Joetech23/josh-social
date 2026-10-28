"""Build Content Hub post records from a week's calendars.

    python3 hub/build_seed.py 2026-W44 hub/assets-2026-W44.json out_dir/

Reads calendar/<week>-eaglescroft.md and calendar/<week>-joshua.md, attaches the uploaded
asset URLs from the JSON map ({"<local file path>": "<asset url>"}), and writes one JSON file
per post into out_dir (posts/<id>.json) for ArtifactData batch writes.
"""
import datetime
import json
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "design" / "pdf"))
from mdtext import KEEP  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parents[1]
BUILD = {"✅": "ready", "🛠": "design", "📥": "needs-you", "✍️": "needs-you"}
DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

TIMES = {
    "eaglescroft": [("LinkedIn", "08:30"), ("Facebook", "12:30"), ("X", "08:00 + 18:30")],
    "joshua": [("LinkedIn", "08:00"), ("X", "08:30"), ("Facebook", "12:30")],
}

# Post ids and graphics per (account, weekday). Files are repo-relative.
POSTS = {
    "2026-W44": {
        ("eaglescroft", "Mon"): ("005", ["posts/2026-10/005-w44-mon-launch-coin/eaglescroft-mon-26-oct.png"]),
        ("eaglescroft", "Tue"): ("006", []),
        ("eaglescroft", "Wed"): ("007", [f"posts/2026-10/007-w44-wed-video-workflow/eaglescroft-wed-28-oct-{i}.png" for i in range(1, 7)]
                                 + ["posts/2026-10/007-w44-wed-video-workflow/eaglescroft-wed-28-oct-linkedin.pdf"]),
        ("eaglescroft", "Thu"): ("008", []),
        ("eaglescroft", "Fri"): ("009", ["posts/2026-10/009-w44-fri-argue-bubble/eaglescroft-fri-30-oct.png"]),
        ("eaglescroft", "Sat"): ("010", [f"posts/2026-10/010-w44-sat-whatsapp-ai/eaglescroft-sat-31-oct-{i}.png" for i in (1, 2, 3)]
                                 + ["posts/2026-10/010-w44-sat-whatsapp-ai/eaglescroft-sat-31-oct-linkedin.pdf"]),
        ("eaglescroft", "Sun"): ("011", ["posts/2026-10/011-w44-sun-5-questions/eaglescroft-sun-1-nov.png"]),
        ("joshua", "Mon"): ("J01", ["posts/2026-10/J01-w44-mon-intro/joshua-mon-26-oct.png"]),
        ("joshua", "Tue"): ("J02", [f"posts/2026-10/J02-w44-tue-traders/joshua-tue-27-oct-{i}.png" for i in range(1, 6)]
                            + ["posts/2026-10/J02-w44-tue-traders/joshua-tue-27-oct-linkedin.pdf"]),
        ("joshua", "Wed"): ("J03", [f"posts/2026-10/J03-w44-wed-academics/joshua-wed-28-oct-{i}.png" for i in range(1, 7)]
                            + ["posts/2026-10/J03-w44-wed-academics/joshua-wed-28-oct-linkedin.pdf"]),
        ("joshua", "Thu"): ("J04", []),
        ("joshua", "Fri"): ("J05", []),
        ("joshua", "Sat"): ("J06", []),
        ("joshua", "Sun"): ("J07", []),
    },
}

# What each unfinished post is waiting on, in plain words.
NEEDS = {
    "007": "2 screenshots of a video edit in progress (timeline, captions panel) and our real before/after edit time, if known.",
    "J04": "A screenshot of the AI video agent, plus one line each: what worked, what broke, what's next.",
    "J06": "One line each on the October AI updates you tried: useful for ___ / not yet because ___.",
    "J07": "Your edits to the Sunday opinion draft below, or your own version.",
}
TIPS = {
    "007": "Facebook and X: post the 6 slides as a carousel. LinkedIn: upload the PDF as a document post (title: \"Edit faster without cutting corners\").",
    "J03": "LinkedIn: upload the PDF as a document post (title: \"AI for your literature review, without cheating\"). X: post slides 1, 4 and 5 with the X caption.",
    "008": "Re-check HighLevel's current AI Employee pricing and language support before this goes out.",
    "010": "Facebook and X: post the 3 slides as a carousel. LinkedIn: upload the PDF as a document post.",
    "J02": "Facebook and X: post the 5 slides as a carousel. LinkedIn: upload the PDF as a document post (title: \"3 free ways to use AI on WhatsApp today\").",
    "005": "Pin this as the intro post on every profile.",
    "J01": "Pin this as the intro post on your profiles.",
}


def week_dates(week):
    year, wk = week.split("-W")
    monday = datetime.date.fromisocalendar(int(year), int(wk), 1)
    return {d: monday + datetime.timedelta(days=i) for i, d in enumerate(DAYS)}


def parse_table(md):
    """Rows of the summary table keyed by weekday."""
    lines = [l for l in md.splitlines() if l.startswith("|")]
    head = [c.strip().lower() for c in lines[0].strip("|").split("|")]
    rows = {}
    for l in lines[2:]:
        cells = [c.strip() for c in l.strip("|").split("|")]
        if len(cells) != len(head):
            continue
        row = dict(zip(head, cells))
        rows[row["day"].split()[0]] = row
    return rows


def clean_label(label):
    label = label.strip().rstrip(":").strip()
    label = re.sub(r"\(draft[^)]*\)", "(draft)", label)
    label = label.replace("(Pidgin-friendly)", "(Pidgin)")
    return label


def unwrap_caption(lines):
    """Join hard-wrapped caption lines. A line ending a sentence keeps its break."""
    out = []
    for body in lines:
        prev = out[-1] if out else ""
        if prev and body and not KEEP.match(body) and not re.search(r"[.?!:\"”)]$", prev):
            out[-1] = prev + " " + body
        else:
            out.append(body)
    return "\n".join(out)


def parse_captions(section):
    """([(label, text)], [x notes]) for the caption blocks in a day section."""
    caps, notes, lines, i = [], [], section.splitlines(), 0
    while i < len(lines):
        m = re.match(r"^\*\*([^*]+)\*\*\s*(.*)$", lines[i].strip())
        if not m:
            i += 1
            continue
        label, rest = m.group(1), m.group(2).strip()
        low = label.lower()
        if low.startswith(("graphic", "topic", "your", "needs", "candidate")) or not re.search(r"linkedin|facebook|\bx\b", low):
            i += 1
            continue
        if "thread" in low:
            notes.append(f"{clean_label(label)}: {rest}")
            i += 1
            continue
        if rest:  # inline caption: **X:** "text"
            if rest.startswith(('"', "“")):
                caps.append((clean_label(label), rest.strip('"“”')))
            else:
                notes.append(f"{clean_label(label)}: {rest}")
            i += 1
            continue
        block = []
        i += 1
        while i < len(lines) and lines[i].startswith(">"):
            block.append(lines[i])
            i += 1
        if block:
            bodies = [l[1:].strip() for l in block]
            # Drop internal reminders like *(Before posting: ...)*, they are not part of the caption
            bodies = [b for b in bodies if not (b.startswith("*(") and b.endswith(")*"))]
            caps.append((clean_label(label), unwrap_caption(bodies).strip()))
    return caps, notes


def title_from(row):
    t = row["post"].strip().strip('"“”')
    return re.sub(r"\s+", " ", t)


def build(week, asset_map, out_dir):
    dates = week_dates(week)
    out = pathlib.Path(out_dir) / "posts"
    out.mkdir(parents=True, exist_ok=True)
    written = []
    for account in ("eaglescroft", "joshua"):
        md = (ROOT / "calendar" / f"{week}-{account}.md").read_text()
        rows = parse_table(md)
        sections = {}
        for sec in re.split(r"^## ", md, flags=re.M)[1:]:
            day = sec.split()[0]
            if day in DAYS:
                sections[day] = sec
        for order, day in enumerate(DAYS):
            row = rows.get(day)
            if not row:
                continue
            pid, files = POSTS[week][(account, day)]
            status = row["status"]
            build_state = "needs-you" if ("📥" in status or "✍️" in status) else ("ready" if "✅" in status else "design")
            if files and build_state != "ready" and all(f in asset_map for f in files):
                build_state = "ready"
            times = TIMES[account]
            if account == "joshua" and "★" not in rows[day]["day"]:
                times = [t for t in times if t[0] != "Facebook"]
            caps, notes = parse_captions(sections.get(day, ""))
            media, downloads = [], []
            for f in files:
                url = asset_map.get(f)
                if not url:
                    continue
                name = pathlib.Path(f).name
                if f.endswith(".png") or f.endswith(".jpg"):
                    media.append({"url": url, "name": name})
                    m = re.search(r"-(\d)\.png$", name)
                    label = f"Slide {m.group(1)}" if m else "Image (PNG)"
                else:
                    label = "LinkedIn PDF"
                downloads.append({"url": url, "name": name, "label": label})
            doc = {
                "week": week,
                "account": account,
                "date": dates[day].isoformat(),
                "order": order,
                "series": row.get("series", ""),
                "title": title_from(row),
                "format": row.get("format", ""),
                "build": build_state,
                "needs": NEEDS.get(pid, "") if build_state != "ready" else "",
                "tip": " ".join(filter(None, [TIPS.get(pid, "")] + notes)),
                "times": [{"platform": p, "time": t} for p, t in times],
                "media": media,
                "files": downloads,
                "captions": [{"label": l, "text": t} for l, t in caps],
            }
            path = out / f"{pid}.json"
            path.write_text(json.dumps(doc, ensure_ascii=False, indent=1))
            written.append((pid, str(path)))
    return written


if __name__ == "__main__":
    week, amap, out_dir = sys.argv[1:4]
    asset_map = json.loads(pathlib.Path(amap).read_text()) if pathlib.Path(amap).exists() else {}
    for pid, path in build(week, asset_map, out_dir):
        print(pid, path)
