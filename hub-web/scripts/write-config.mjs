// Vercel build step: writes public/config.js from the project's environment variables,
// so the Supabase URL and anon key never live in git. Run locally the same way:
//   SUPABASE_URL=... SUPABASE_ANON_KEY=... node scripts/write-config.mjs
import { writeFileSync } from "node:fs";

const url = (process.env.SUPABASE_URL || "").trim().replace(/\/+$/, "");
const key = (process.env.SUPABASE_ANON_KEY || "").trim();
if (!url || !key) {
  console.warn("SUPABASE_URL or SUPABASE_ANON_KEY is not set: the page will show a setup message.");
}
// The browser must only ever get the public key: refuse a secret / service-role key.
if (key && (key.startsWith("sb_secret_") || /service_role/.test(Buffer.from(key.split(".")[1] || "", "base64").toString()))) {
  throw new Error("SUPABASE_ANON_KEY holds a secret key. Use the anon / publishable key here.");
}
writeFileSync(new URL("../public/config.js", import.meta.url),
  `window.HUB_CONFIG = ${JSON.stringify({ supabaseUrl: url, supabaseAnonKey: key })};\n`);
console.log("public/config.js written");
