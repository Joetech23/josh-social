"""Publish a week's posts (graphics + captions) to the Content Hub in Supabase.

    python3 hub-web/tools/hub_sync.py 2026-W44            # upload files and upsert every post
    python3 hub-web/tools/hub_sync.py 2026-W44 J04 008    # only these posts
    python3 hub-web/tools/hub_sync.py 2026-W44 --dry-run  # show what would be sent

Post records come from the calendars through hub/build_seed.py (the same source as the
claude.ai hub). Files are stored in the private "hub" bucket at their repo path.
"""
import json
import mimetypes
import pathlib
import sys
import tempfile
from datetime import datetime, timezone

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "hub"))
import build_seed  # noqa: E402


def rows_for(week, only):
    files = sorted({f for _, fs in build_seed.POSTS[week].values() for f in fs if (ROOT / f).exists()})
    asset_map = {f: f for f in files}  # storage path = repo path
    with tempfile.TemporaryDirectory() as tmp:
        written = build_seed.build(week, asset_map, tmp)
        rows = []
        for pid, path in written:
            if only and pid not in only:
                continue
            d = json.loads(pathlib.Path(path).read_text())
            rows.append({
                "id": pid, "week": d["week"], "account": d["account"], "date": d["date"], "ord": d["order"],
                "series": d["series"], "title": d["title"], "format": d["format"], "build": d["build"],
                "needs": d["needs"], "tip": d["tip"], "times": d["times"],
                "media": [{"path": m["url"], "name": m["name"]} for m in d["media"]],
                "files": [{"path": f["url"], "name": f["name"], "label": f["label"]} for f in d["files"]],
                "captions": d["captions"],
                "updated_at": datetime.now(timezone.utc).isoformat(),
            })
    return rows


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    dry = "--dry-run" in sys.argv
    week, only = args[0], set(args[1:])
    rows = rows_for(week, only)
    uploads = sorted({f["path"] for r in rows for f in r["files"]})
    if dry:
        for r in rows:
            print(f'{r["id"]:4} {r["date"]} {r["build"]:9} {len(r["media"])} img {len(r["files"])} files  {r["title"][:60]}')
        print(f"{len(uploads)} files would upload")
        return
    from supa import Supa
    sb = Supa()
    for f in uploads:
        ctype = mimetypes.guess_type(f)[0] or "application/octet-stream"
        sb.upload(f, (ROOT / f).read_bytes(), ctype)
        print("uploaded", f)
    sb.upsert("posts", rows)
    print(f"{len(rows)} posts published to the hub")


if __name__ == "__main__":
    main()
