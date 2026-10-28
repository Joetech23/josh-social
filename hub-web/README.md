# Content Hub (website)

A simple website for posting: each day's graphics for both accounts, captions with a copy
button, downloads (PNGs and the LinkedIn PDF), posting times, and your decision on each post.
No database and no login. Hosted free on **Vercel**.

```
vercel.json              (repo root) build + security headers
hub-web/
├── public/              the site: index.html, app.js, styles.css, icons
│   └── data/posts.json  every post, built from the calendars
├── build_data.py        calendars -> public/data/posts.json   (Claude runs this)
└── build.mjs            Vercel build step: copies the graphics into the site
```

## How it works

- **Posts:** Claude updates `data/posts.json` and pushes. Vercel redeploys in about a minute.
- **Your decisions and notes** (Approve, Request changes, Posted, notes) are saved **on your
  device**. Tap **Copy feedback for Claude** at the bottom and paste it into the chat.
  Send screenshots and photos in the chat too.
- **Privacy:** the site isn't listed on search engines, but anyone with the link can open it.
  The posts become public anyway once they go out. Share the link only with people you trust,
  and keep this GitHub repo private.

## Deploy on Vercel (once)

1. vercel.com → **Add New → Project** → import `Joetech23/josh-social`.
2. Leave **Root Directory** empty and set **Framework Preset** to Other.
   `vercel.json` sets the build command and output folder.
3. **Deploy.** Every push to `main` redeploys.

On your phone, open the site and use **Add to Home Screen**. It opens like an app.

## Updating posts (Claude)

```bash
python3 hub-web/build_data.py      # after finishing or changing a post
git add -A && git commit -m "..." && git push
```

To preview locally: `node hub-web/build.mjs && python3 -m http.server -d hub-web/public 8080`.
