# Content Hub (private posting desk)

**Live page:** https://claude.ai/artifact/HfGcxW1yTp93NpGKjs6M6U (private to Joshua)

One page per week for both accounts: each day's graphics (swipe the carousel, tap to zoom),
download buttons for the PNGs and LinkedIn PDFs, captions per platform with a copy button,
posting times, and Joshua's decision on each post (approve, request changes, posted) with a note.
Below the posts, Joshua can drop files (screenshots, photos, logos) and leave notes for Claude.
This replaces the Drive inbox for anything that needs to come back to Claude.

## Where the data lives (artifact database)

| Collection | Written by | What |
| --- | --- | --- |
| `posts/<id>` | Claude only (rule: write = admin) | One record per post: week, account, date, title, format, build state, media, files, captions, times |
| `reviews/<id>` | Joshua, from the page | `status` (`approved` / `changes` / `posted` / empty), `note`, `updatedAt` |
| `inbox/<auto>` | Joshua, from the page | Uploaded file: `name`, `assetId`, `url`, `forPost`, `seen` |
| `messages/<auto>` | Joshua, from the page | Free-text note: `text`, `week`, `account`, `seen`, optional `reply` |

## Weekly routine (Claude)

1. **Start of session:** read `reviews`, `messages` and `inbox` with ArtifactData. Download any
   inbox file with `Artifact read` + `path: <assetId>` into `design/inbox/`, then set `seen: true`
   on the inbox row and message (add a short `reply` to a message when useful).
2. **When a graphic is finished:** upload its PNGs/PDF with `Artifact publish` + `asset: true` +
   `file_paths`, add the returned `/_blob/...` urls to `hub/assets-<week>.json`, add the files to
   `POSTS` in `build_seed.py`, then:
   ```bash
   python3 hub/build_seed.py 2026-W44 hub/assets-2026-W44.json <scratchpad>/seed
   ```
   and write the changed `posts/<id>` records with an ArtifactData batch (`set`, pinned with
   `if_version`).
3. **New week:** write the calendars, add the week to `POSTS`, `NEEDS` and `TIPS`, and seed it.
   The page shows the week holding the next upcoming post; arrows step between weeks.
4. **Page changes:** edit `hub/index.template.html`, run `python3 hub/build_page.py`, and publish
   `hub/index.html` to the same artifact.
