# Posts

One folder per post: `posts/YYYY-MM/<id>-<slug>/`

```
posts/2026-10/001-lift-off/
  copy.md          ← from templates/<pillar>.md, filled in and approved
  graphic.html     ← copied from design/templates/, copy edited
  graphic.png      ← rendered with design/render.sh
  carousel.pdf     ← (carousel posts only)
```

When you copy a template here, change its `<base href="../../">` to `<base href="../../../">`
so the shared CSS and brand marks still resolve.

The `id` matches the row in `pipeline/tracker.csv`.
