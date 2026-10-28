# Content Hub (web): Vercel + Supabase

The private posting desk as a real website: each day's graphics, captions with a copy button,
downloads, approve / request changes / posted, notes for Claude and a file drop.
Static files on **Vercel**, with sign-in, data and file storage on **Supabase**. Both free tiers are enough.

```
hub-web/
├── public/             the site (index.html, app.js, styles.css, vendored supabase-js, icons)
├── scripts/            write-config.mjs: Vercel build step, turns env vars into public/config.js
├── supabase/schema.sql tables, access rules and the private "hub" storage bucket
├── tools/              Claude's side: hub_sync.py (publish posts), hub_feedback.py (read your feedback)
└── vercel.json         build settings + security headers (noindex, no framing, strict CSP)
```

## Who can see what

- Only emails listed in the `hub_members` table see anything: posts, graphics, notes, files.
  Anyone else, even signed in, gets an empty page. Graphics sit in a **private** bucket and
  load through links that expire after an hour.
- You can approve, write notes, send notes and upload files (uploads go only into `inbox/`).
  You can't change or delete posts: only Claude publishes them.
- Claude publishes with the service-role key, which lives only in Claude's environment.
  It never goes in git, Vercel or the browser.
- The site isn't indexed by search engines and can't be embedded in other sites.

## Setup (about 15 minutes, once)

### 1. Supabase

1. Create a project at supabase.com (free plan). Pick the region closest to you, for example `eu-west`.
2. **SQL Editor → New query**: paste all of `supabase/schema.sql` → **Run**.
3. In the same editor, add yourself (use the email you'll sign in with, in lower case):
   ```sql
   insert into public.hub_members (email) values ('your@email.com') on conflict do nothing;
   ```
4. **Authentication → Users → Add user → Create new user**: same email, a strong password,
   tick *Auto Confirm User*.
5. **Authentication → Sign In / Providers**: turn **off** *Allow new users to sign up*.
6. **Project Settings → API Keys**: note the **Project URL**, the **anon / publishable** key
   (safe for the browser) and the **service_role / secret** key (Claude only, step 3).

### 2. Vercel

1. vercel.com → **Add New → Project** → import the GitHub repo `Joetech23/josh-social`.
2. **Root Directory:** `hub-web` · **Framework Preset:** Other
   (the build and output settings come from `vercel.json`).
3. **Environment Variables:**
   - `SUPABASE_URL`: the Project URL
   - `SUPABASE_ANON_KEY`: the anon / publishable key (the build refuses a secret key)
4. **Deploy.** Vercel builds production from `main`; every push redeploys.
5. Back in Supabase, **Authentication → URL Configuration**: set **Site URL** to your Vercel
   address (for example `https://eaglescroft-hub.vercel.app`) so sign-in links land on the hub.

On your phone, open the site and use **Add to Home Screen**. It opens like an app.

### 3. Let Claude publish and read feedback

In Claude's cloud environment settings (environment menu → Edit):

- **Network access:** add your Supabase host (`<project-ref>.supabase.co`, or `*.supabase.co`)
  to Allowed domains.
- **Secrets / environment variables:** `SUPABASE_URL` and `SUPABASE_SERVICE_ROLE_KEY`.
  Never paste the secret key into a chat.

A new session picks these up. From then on:

```bash
python3 hub-web/tools/hub_sync.py 2026-W44              # publish the week (or: 2026-W44 J04 008)
python3 hub-web/tools/hub_sync.py 2026-W44 --dry-run    # preview without sending
python3 hub-web/tools/hub_feedback.py                   # your decisions, new notes, new files
python3 hub-web/tools/hub_feedback.py --download --mark-seen
python3 hub-web/tools/hub_feedback.py --reply <message-id> "Done, it's in Thursday's post."
```

Post records come from the weekly calendars through `hub/build_seed.py`, the same source the
claude.ai hub uses, so both stay in step.

## Changing the site

Edit `public/` and push: Vercel redeploys on every push. `public/config.js` is generated at build
time and is git-ignored. To run it locally:

```bash
SUPABASE_URL=... SUPABASE_ANON_KEY=... node scripts/write-config.mjs
python3 -m http.server -d public 8080
```
