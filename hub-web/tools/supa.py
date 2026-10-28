"""Minimal Supabase REST + Storage client for Claude's hub tools (standard library only).

Reads SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY from the environment. The service-role key
bypasses row-level security, so it stays in the environment: never in git, never in the browser.
"""
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

BUCKET = "hub"


class Supa:
    def __init__(self):
        self.url = os.environ.get("SUPABASE_URL", "").rstrip("/")
        key = os.environ.get("SUPABASE_SERVICE_ROLE_KEY", "")
        if not self.url or not key:
            sys.exit("Set SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY in the environment first.")
        self.headers = {"apikey": key}
        if key.count(".") == 2:  # legacy JWT keys also go in Authorization; new sb_secret_ keys don't
            self.headers["Authorization"] = f"Bearer {key}"

    def _req(self, method, path, body=None, headers=None, raw=False):
        h = dict(self.headers, **(headers or {}))
        data = body
        if body is not None and not isinstance(body, bytes):
            data = json.dumps(body).encode()
            h.setdefault("Content-Type", "application/json")
        req = urllib.request.Request(self.url + path, data=data, method=method, headers=h)
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                out = r.read()
        except urllib.error.HTTPError as e:
            raise SystemExit(f"{method} {path} failed: {e.code} {e.read().decode(errors='replace')[:500]}")
        if raw:
            return out
        return json.loads(out) if out else None

    # Tables (PostgREST)
    def select(self, table, query="select=*"):
        return self._req("GET", f"/rest/v1/{table}?{query}")

    def upsert(self, table, rows, on_conflict="id"):
        return self._req("POST", f"/rest/v1/{table}?on_conflict={on_conflict}", rows,
                         {"Prefer": "resolution=merge-duplicates,return=minimal"})

    def update(self, table, match, values):
        q = "&".join(f"{k}=eq.{urllib.parse.quote(str(v))}" for k, v in match.items())
        return self._req("PATCH", f"/rest/v1/{table}?{q}", values, {"Prefer": "return=minimal"})

    # Storage
    def upload(self, path, data, content_type):
        p = urllib.parse.quote(path)
        return self._req("POST", f"/storage/v1/object/{BUCKET}/{p}", data,
                         {"Content-Type": content_type, "x-upsert": "true", "Cache-Control": "max-age=3600"})

    def download(self, path):
        return self._req("GET", f"/storage/v1/object/{BUCKET}/{urllib.parse.quote(path)}", raw=True)
