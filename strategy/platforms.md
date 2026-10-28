# Platform playbooks

Based on the October 2026 trend notes in [`research/2026-10-trends.md`](../research/2026-10-trends.md).
Times are **WAT (Lagos/Abuja, UTC+1)**; adjust once we have our own analytics.

## LinkedIn: the primary platform

**Who's there:** founders, professionals, NYSC/graduates, diaspora, international clients.

| Item | Setting |
| --- | --- |
| Cadence | 3–4 posts/week on the company page; Joshua reshares 2 with his own comment |
| Best formats | Document carousels (PDF, 6–10 slides, 1080×1350), portrait image + story caption, native short video |
| Caption | Hook in the first 2 lines (before "…see more"), 150–250 words, short paragraphs, one question at the end |
| Links | Never in the post body. Put the link in the first comment |
| Hashtags | 3–5 |
| Timing | Tue–Thu, 8:00–10:00 WAT (also catches UK morning) |
| First hour | Reply to every comment, with substance. Early conversation drives reach |
| Avoid | Engagement bait ("comment YES"), polls for reach, pods |

**Image sizes:** portrait post 1080×1350 · square 1080×1080 · carousel 1080×1350 per slide ·
company cover 1128×191 · logo 400×400.

## Facebook: community and local reach

**Who's there:** Nigerian SME owners, traders, community and family networks.

| Item | Setting |
| --- | --- |
| Cadence | 3 posts/week, at least 1 Reel |
| Best formats | Reels (they reach non-followers), portrait images, behind-the-scenes photos |
| Caption | Warmer and shorter than LinkedIn, 40–120 words; Pidgin-friendly phrasing is fine where natural |
| Links | OK in body but reach is better in comments |
| Hashtags | 2–4 |
| Timing | Weekdays 12:00–14:00 or 19:00–21:00 WAT |
| Extras | Reply fast; share Ground School posts into relevant business Groups (with value, not spam) |
| Paid | Boost only posts that already performed organically |

**Image sizes:** portrait 1080×1350 · Reel 1080×1920 · cover 1640×624 (displays ~820×312, keep
text in the centre safe area) · profile 720×720.

## X: conversation and build-in-public

**Who's there:** builders, tech community, AI practitioners, journalists.

| Item | Setting |
| --- | --- |
| Cadence | 1 post/day on weekdays + 1–2 threads/week. More posts ≠ more reach |
| Best formats | Threads (hook + image in post 1), native video, sharp single opinions, replies to bigger accounts |
| Links | Never in the main post. Put the link in the first reply |
| Hashtags | 0–2 |
| Timing | 8:00–9:00 and 18:00–20:00 WAT |
| Engagement | 15 min/day of thoughtful replies in AI/tech conversations; reply to everyone who replies to us |
| Avoid | Hot takes that invite mutes or blocks (they suppress reach broadly) |

**Image sizes:** in-feed 1600×900 or 1080×1350 · header 1500×500 · profile 400×400.

## Graphic template map

| Template | Size | Use on |
| --- | --- | --- |
| `design/templates/post-square.html` | 1080×1080 | All three |
| `design/templates/post-portrait.html` | 1080×1350 | LinkedIn, Facebook, X |
| `design/templates/chat-card.html` | 1080×1350 | Cockpit Chat posts on all three |
| `design/templates/carousel.html` | 1080×1350 × N, PDF | LinkedIn document post; slides reused on FB/X |
| `design/templates/linkedin-cover.html` | 1128×191 | LinkedIn company page |
| `design/templates/facebook-cover.html` | 1640×624 | Facebook page |
| `design/templates/x-header.html` | 1500×500 | X profile |
| `design/templates/avatar.html` | 800×800 | Profile picture on all three |
