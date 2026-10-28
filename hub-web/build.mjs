// Vercel build step: copy the graphics that data/posts.json points at into the site.
import { readFileSync, mkdirSync, copyFileSync, existsSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const root = join(dirname(fileURLToPath(import.meta.url)), "..");
const site = join(root, "hub-web", "public");
const { posts } = JSON.parse(readFileSync(join(site, "data", "posts.json"), "utf8"));
const paths = new Set(posts.flatMap((p) => [...p.media, ...p.files].map((f) => f.url)));
let missing = 0;
for (const p of paths) {
  const src = join(root, p);
  if (!existsSync(src)) { console.warn("missing", p); missing++; continue; }
  mkdirSync(dirname(join(site, p)), { recursive: true });
  copyFileSync(src, join(site, p));
}
console.log(`${paths.size - missing} files copied into the site${missing ? `, ${missing} missing` : ""}`);
