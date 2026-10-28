"""Write hub-web/public/data/posts.json from the weekly calendars (all weeks in hub/build_seed.py).

    python3 hub-web/build_data.py

Run it after finishing or changing a post, then commit and push: Vercel redeploys the hub.
Graphics are referenced by their repo path (posts/...); hub-web/build.mjs copies them into the
site at deploy time, so they are not duplicated in git.
"""
import json
import pathlib
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "hub"))
import build_seed  # noqa: E402

posts = []
for week, mapping in build_seed.POSTS.items():
    files = {f: f for _, fs in mapping.values() for f in fs if (ROOT / f).exists()}
    with tempfile.TemporaryDirectory() as tmp:
        for pid, path in build_seed.build(week, files, tmp):
            posts.append({"id": pid, **json.loads(pathlib.Path(path).read_text())})

out = ROOT / "hub-web" / "public" / "data" / "posts.json"
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps({"posts": posts}, ensure_ascii=False, indent=1) + "\n")
ready = sum(p["build"] == "ready" for p in posts)
print(f"{len(posts)} posts ({ready} ready) -> {out.relative_to(ROOT)}")
