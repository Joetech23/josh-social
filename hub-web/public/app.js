// EAGLESCROFT Content Hub (web). Data lives in Supabase: see ../supabase/schema.sql.
(() => {
  const $ = (s, el = document) => el.querySelector(s);
  const esc = (s) => String(s ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
  const ICON = {
    copy: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="8" y="8" width="14" height="14" rx="2"/><path d="M4 16V4a2 2 0 0 1 2-2h12"/></svg>',
    down: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3v12"/><path d="m7 10 5 5 5-5"/><path d="M5 21h14"/></svg>',
    brush: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="m14.6 3.4 6 6L9 21H3v-6L14.6 3.4Z"/><path d="m11 7 6 6"/></svg>',
    file: '<svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6"/></svg>',
    prev: '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"><path d="m15 18-6-6 6-6"/></svg>',
    next: '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"><path d="m9 18 6-6-6-6"/></svg>',
  };
  const BUILD = { ready: ["ready", "Graphic ready"], design: ["design", "In design"], "needs-you": ["needs", "Needs you"] };
  const STATUS = [["approved", "Approve"], ["changes", "Request changes"], ["posted", "Posted"]];
  const BUCKET = "hub";
  const URL_TTL = 60 * 60; // signed image links last an hour; refresh renews them

  const state = { posts: [], reviews: {}, inbox: [], messages: [], urls: {}, account: "eaglescroft", week: null, capTab: {}, drafts: {}, user: null };
  try { const a = localStorage.getItem("hub.account"); if (a) state.account = a; } catch (e) {}

  const toast = (msg) => { const t = $("#toast"); t.textContent = msg; t.classList.add("show"); clearTimeout(toast.h); toast.h = setTimeout(() => t.classList.remove("show"), 2400); };
  const notice = (html) => { const n = $("#notice"); if (!html) { n.hidden = true; return; } n.innerHTML = html; n.hidden = false; };
  const fmtDay = (iso) => new Date(iso + "T12:00:00").toLocaleDateString("en-GB", { weekday: "short", day: "numeric", month: "short" });
  const fmtWhen = (ts) => ts ? new Date(ts).toLocaleString("en-GB", { weekday: "short", day: "numeric", month: "short", hour: "2-digit", minute: "2-digit" }) : "";

  // ---------- Supabase ----------
  const cfg = window.HUB_CONFIG || {};
  if (!cfg.supabaseUrl || !cfg.supabaseAnonKey || !window.supabase) {
    document.body.innerHTML = '<div class="auth"><div class="card"><h1>Content Hub</h1><p>This deployment has no Supabase settings yet. Add <b>SUPABASE_URL</b> and <b>SUPABASE_ANON_KEY</b> in Vercel (Settings → Environment Variables), then redeploy.</p></div></div>';
    return;
  }
  const sb = window.supabase.createClient(cfg.supabaseUrl, cfg.supabaseAnonKey, { auth: { persistSession: true, autoRefreshToken: true, detectSessionInUrl: true } });

  // ---------- Sign-in ----------
  let magicMode = false;
  function showAuth(msg = "", err = false) {
    $("#app").hidden = true; $("#auth").hidden = false;
    $("#authMsg").textContent = msg; $("#authMsg").classList.toggle("err", err);
  }
  $("#magic").addEventListener("click", () => {
    magicMode = !magicMode;
    $("#pwField").hidden = magicMode;
    $("#password").required = !magicMode;
    $("#authBtn").textContent = magicMode ? "Email me a link" : "Sign in";
    $("#magic").textContent = magicMode ? "Use my password instead" : "Email me a sign-in link instead";
    $("#authMsg").textContent = "";
  });
  $("#password").required = true;
  $("#authForm").addEventListener("submit", async (ev) => {
    ev.preventDefault();
    const email = $("#email").value.trim().toLowerCase();
    $("#authBtn").disabled = true; $("#authMsg").classList.remove("err"); $("#authMsg").textContent = magicMode ? "Sending…" : "Signing in…";
    try {
      if (magicMode) {
        const { error } = await sb.auth.signInWithOtp({ email, options: { shouldCreateUser: false, emailRedirectTo: location.origin + location.pathname } });
        if (error) throw error;
        $("#authMsg").textContent = "Check your inbox for the sign-in link.";
      } else {
        const { error } = await sb.auth.signInWithPassword({ email, password: $("#password").value });
        if (error) throw error;
      }
    } catch (e) { $("#authMsg").textContent = e.message || "Couldn't sign in."; $("#authMsg").classList.add("err"); }
    $("#authBtn").disabled = false;
  });
  $("#signOut").addEventListener("click", async () => { await sb.auth.signOut(); });

  let started = false;
  sb.auth.onAuthStateChange((_event, session) => {
    state.user = session?.user || null;
    if (!state.user) { started = false; showAuth(); return; }
    $("#auth").hidden = true; $("#app").hidden = false;
    if (!started) { started = true; loadAll(); }
  });

  // ---------- Data ----------
  async function loadAll() {
    notice("");
    const [posts, reviews, inbox, messages] = await Promise.all([
      sb.from("posts").select("*").order("date").order("ord"),
      sb.from("reviews").select("*"),
      sb.from("inbox").select("*").order("created_at", { ascending: false }).limit(20),
      sb.from("messages").select("*").order("created_at", { ascending: false }).limit(10),
    ]);
    const err = posts.error || reviews.error || inbox.error || messages.error;
    if (err) { notice("Couldn't load the hub: " + esc(err.message)); }
    state.posts = posts.data || [];
    state.reviews = Object.fromEntries((reviews.data || []).map((r) => [r.post_id, r]));
    state.inbox = inbox.data || [];
    state.messages = messages.data || [];
    if (!err && !state.posts.length) {
      notice("You're signed in, but no posts are visible. If posts have been published, add your email to <b>hub_members</b> in Supabase (see the setup guide).");
    }
    pickWeek();
    await signWeek();
    render();
  }

  // Images live in a private bucket: sign the current week's paths in one call
  async function signWeek() {
    const paths = [];
    state.posts.filter((p) => p.week === state.week).forEach((p) => (p.media || []).forEach((m) => { if (!state.urls[m.path]) paths.push(m.path); }));
    state.inbox.forEach((f) => { if (/^image\//.test(f.content_type) && !state.urls[f.path]) paths.push(f.path); });
    if (!paths.length) return;
    const { data, error } = await sb.storage.from(BUCKET).createSignedUrls(paths, URL_TTL);
    if (error) { notice("Couldn't load the graphics: " + esc(error.message)); return; }
    (data || []).forEach((d) => { if (d.signedUrl) state.urls[d.path] = d.signedUrl; });
  }

  const weeks = () => [...new Set(state.posts.map((p) => p.week))].sort();
  function pickWeek() {
    const ws = weeks();
    if (!ws.length) { state.week = null; return; }
    if (state.week && ws.includes(state.week)) return;
    const today = new Date().toISOString().slice(0, 10);
    const current = ws.find((w) => state.posts.some((p) => p.week === w && p.date >= today));
    state.week = current || ws[ws.length - 1];
  }

  // ---------- Render ----------
  function renderHeader() {
    const ws = weeks(), i = ws.indexOf(state.week);
    $("#weekLabel").textContent = state.week ? state.week.replace(/^\d{4}-/, "") : "—";
    $("#prevWeek").disabled = i <= 0; $("#nextWeek").disabled = i < 0 || i >= ws.length - 1;
    const dates = state.posts.filter((p) => p.week === state.week).map((p) => p.date).sort();
    $("#weekRange").textContent = dates.length ? `${fmtDay(dates[0])} – ${fmtDay(dates[dates.length - 1])} · all times WAT` : "No posts yet.";
    document.querySelectorAll(".seg button").forEach((b) => b.setAttribute("aria-pressed", String(b.dataset.acc === state.account)));
  }

  const visiblePosts = () => state.posts.filter((p) => p.week === state.week && p.account === state.account)
    .sort((a, b) => (a.date + String(a.ord).padStart(3, "0")).localeCompare(b.date + String(b.ord).padStart(3, "0")));

  function renderStats(ps) {
    const n = (f) => ps.filter(f).length, st = (p) => state.reviews[p.id]?.status;
    $("#stats").innerHTML = [
      [n((p) => p.build === "ready"), "graphics ready"], [n((p) => st(p) === "approved"), "approved"],
      [n((p) => st(p) === "posted"), "posted"], [n((p) => p.build === "needs-you"), "need you"],
    ].map(([v, l]) => `<span class="stat"><b>${v}</b>${l}</span>`).join("");
  }

  function mediaHTML(p) {
    const m = p.media || [];
    if (!m.length) return `<div class="placeholder"><div>${ICON.brush}<div><b style="color:var(--ink)">Graphic in progress</b></div><div style="font-size:14px">${esc(p.format)}</div></div></div>`;
    const imgs = m.map((x, i) => { const u = state.urls[x.path] || ""; return `<img src="${esc(u)}" alt="${esc(p.title)}, slide ${i + 1} of ${m.length}" loading="lazy" data-full="${esc(u)}">`; }).join("");
    const arrows = m.length > 1 ? `<div class="arrows"><button data-nav="-1" aria-label="Previous slide">${ICON.prev}</button><button data-nav="1" aria-label="Next slide">${ICON.next}</button></div>` : "";
    return `<div class="track">${imgs}</div>${m.length > 1 ? `<span class="count mono">1 / ${m.length}</span>` : ""}${arrows}`;
  }

  function captionsHTML(p) {
    const caps = p.captions || [];
    if (!caps.length) return "";
    const sel = Math.min(state.capTab[p.id] ?? 0, caps.length - 1), c = caps[sel];
    const tabs = caps.map((x, i) => `<button role="tab" aria-selected="${i === sel}" data-cap="${i}">${esc(x.label)}</button>`).join("");
    return `<div class="caps"><div class="tabs" role="tablist">${tabs}</div><div class="captext" role="tabpanel">${esc(c.text)}</div>
      <div class="capfoot"><span>${c.text.trim().split(/\s+/).length} words · ${c.text.length} characters</span><button class="btn" data-copy="${sel}">${ICON.copy}Copy caption</button></div></div>`;
  }

  function filesHTML(p) {
    const files = p.files || [];
    if (!files.length) return "";
    const all = files.length > 2 ? `<button class="btn primary" data-dlall>${ICON.down}Download all (${files.length})</button>` : "";
    return `<div class="row">${all}${files.map((f, i) => `<button class="btn" data-dl="${i}">${ICON.down}${esc(f.label || f.name)}</button>`).join("")}</div>`;
  }

  function reviewHTML(p) {
    const r = state.reviews[p.id] || {}, draft = state.drafts[p.id] ?? r.note ?? "";
    const btns = STATUS.map(([s, l]) => `<button data-s="${s}" aria-pressed="${r.status === s}">${l}</button>`).join("");
    return `<div class="review"><div class="status" role="group" aria-label="Your decision">${btns}</div>
      <label class="sr" for="note-${esc(p.id)}">Notes or changes</label>
      <textarea id="note-${esc(p.id)}" data-note placeholder="Changes you want, the live post link, or how it did…">${esc(draft)}</textarea>
      <div class="row"><button class="btn" data-savenote>Save note</button><span class="saved">${r.updated_at ? "Saved " + esc(fmtWhen(r.updated_at)) : ""}</span></div></div>`;
  }

  function postHTML(p) {
    const [cls, label] = BUILD[p.build] || ["", p.build || ""];
    const times = (p.times || []).map((t) => `${esc(t.platform)} ${esc(t.time)}`).join(" · ");
    return `<article class="panel post" data-id="${esc(p.id)}">
      <div class="media">${mediaHTML(p)}</div>
      <div class="body">
        <div class="meta"><span class="day">${esc(fmtDay(p.date))}</span>${p.series ? `<span class="chip">${esc(p.series)}</span>` : ""}<span class="chip ${cls}">${esc(label)}</span></div>
        <h2>${esc(p.title)}</h2>
        <div class="facts">${p.format ? `<div><b>Format</b> · ${esc(p.format)}</div>` : ""}${times ? `<div><b>Post at</b> · ${times}</div>` : ""}</div>
        ${p.needs ? `<div class="callout"><b>Needed from you:</b> ${esc(p.needs)}</div>` : ""}
        ${p.tip ? `<div class="tipline">${esc(p.tip)}</div>` : ""}
        ${filesHTML(p)}${captionsHTML(p)}${reviewHTML(p)}
      </div></article>`;
  }

  function render() {
    renderHeader();
    const ps = visiblePosts();
    renderStats(ps);
    // Keep the focused note and each carousel's slide across re-renders
    const act = document.activeElement, focusId = act && act.matches("[data-note]") ? act.closest("article").dataset.id : null;
    const caret = focusId ? [act.selectionStart, act.selectionEnd] : null;
    const scroll = {}; document.querySelectorAll("article.post .track").forEach((tr) => { scroll[tr.closest("article").dataset.id] = tr.scrollLeft; });
    $("#list").innerHTML = ps.length ? ps.map(postHTML).join("") : `<div class="panel empty">No posts for this account and week yet.</div>`;
    document.querySelectorAll("article.post").forEach((a) => {
      const tr = $(".track", a); if (tr && scroll[a.dataset.id]) tr.scrollLeft = scroll[a.dataset.id];
      if (a.dataset.id === focusId) { const t = $("[data-note]", a); t.focus(); t.setSelectionRange(caret[0], caret[1]); }
    });
    const sel = $("#inboxFor"), cur = sel.value;
    sel.innerHTML = `<option value="">General (not for one post)</option>` + state.posts.filter((p) => p.week === state.week)
      .sort((a, b) => (a.account + a.date).localeCompare(b.account + b.date))
      .map((p) => `<option value="${esc(p.id)}">${p.account === "joshua" ? "Joshua" : "EAGLESCROFT"} · ${esc(fmtDay(p.date))} · ${esc(p.title.slice(0, 48))}</option>`).join("");
    sel.value = cur;
    renderInbox(); renderMessages();
  }

  function renderInbox() {
    $("#inboxList").innerHTML = state.inbox.slice(0, 12).map((f) => {
      const forPost = state.posts.find((p) => p.id === f.for_post), u = state.urls[f.path];
      return `<div class="item">${u ? `<img src="${esc(u)}" alt="">` : `<span class="ico">${ICON.file}</span>`}
        <div class="t"><b>${esc(f.name)}</b><span>${forPost ? esc(fmtDay(forPost.date)) + " · " : ""}${esc(fmtWhen(f.created_at))}${f.seen ? " · picked up" : ""}</span></div></div>`;
    }).join("");
  }

  function renderMessages() {
    $("#msgList").innerHTML = state.messages.slice(0, 8).map((m) => `<div class="msg">${esc(m.text)}<small>${esc(fmtWhen(m.created_at))}${m.seen ? " · read by Claude" : ""}${m.reply ? " · Reply: " + esc(m.reply) : ""}</small></div>`).join("");
  }

  // ---------- Actions ----------
  async function copyText(text) {
    try { await navigator.clipboard.writeText(text); return true; } catch (e) {}
    const ta = document.createElement("textarea"); ta.value = text; ta.setAttribute("readonly", ""); ta.style.position = "fixed"; ta.style.opacity = "0";
    document.body.appendChild(ta); ta.select();
    let ok = false; try { ok = document.execCommand("copy"); } catch (e) {}
    ta.remove(); return ok;
  }

  async function saveFile(f) {
    const { data, error } = await sb.storage.from(BUCKET).createSignedUrl(f.path, 300, { download: f.name });
    if (error) { toast("Couldn't download " + f.name); return false; }
    const a = document.createElement("a"); a.href = data.signedUrl; a.rel = "noopener"; document.body.appendChild(a); a.click(); a.remove();
    return true;
  }

  async function setReview(id, patch) {
    const prev = state.reviews[id] || {};
    const next = { post_id: id, status: prev.status || "", note: prev.note || "", ...patch, updated_at: new Date().toISOString() };
    state.reviews[id] = next; render();
    const { error } = await sb.from("reviews").upsert(next, { onConflict: "post_id" });
    if (error) { state.reviews[id] = prev; render(); toast("Couldn't save: " + error.message); return false; }
    return true;
  }

  async function sendMessage() {
    const ta = $("#msgText"), text = ta.value.trim();
    if (!text) return;
    $("#msgSend").disabled = true; $("#msgState").textContent = "Sending…";
    const { data, error } = await sb.from("messages").insert({ text, week: state.week || "", account: state.account }).select().single();
    if (error) { $("#msgState").textContent = "Not sent: " + error.message; }
    else { ta.value = ""; $("#msgState").textContent = "Sent"; state.messages.unshift(data); renderMessages(); toast("Note sent"); }
    $("#msgSend").disabled = false;
  }

  async function uploadFiles(list) {
    const forPost = $("#inboxFor").value || null;
    for (const file of list) {
      toast(`Uploading ${file.name}…`);
      const safe = file.name.normalize("NFKD").replace(/[^\w.\-]+/g, "-").replace(/-+/g, "-").slice(-120);
      const path = `inbox/${new Date().toISOString().slice(0, 10)}/${Date.now()}-${safe}`;
      const up = await sb.storage.from(BUCKET).upload(path, file, { contentType: file.type || undefined, upsert: false });
      if (up.error) { toast(`${file.name} didn't upload: ${up.error.message}`); continue; }
      const { data, error } = await sb.from("inbox").insert({ name: file.name, path, content_type: file.type || "", size_bytes: file.size, for_post: forPost }).select().single();
      if (error) { toast(`${file.name} uploaded but wasn't logged: ${error.message}`); continue; }
      state.inbox.unshift(data);
      toast(`${file.name} sent to Claude`);
    }
    await signWeek(); renderInbox();
  }

  document.addEventListener("click", async (ev) => {
    const t = ev.target.closest("button, img[data-full]");
    if (!t || t.closest("#authForm")) return;
    const card = t.closest("article.post"), p = card && state.posts.find((x) => x.id === card.dataset.id);

    if (t.matches(".seg button")) { state.account = t.dataset.acc; try { localStorage.setItem("hub.account", state.account); } catch (e) {} render(); return; }
    if (t.id === "prevWeek" || t.id === "nextWeek") { const ws = weeks(); const i = ws.indexOf(state.week) + (t.id === "nextWeek" ? 1 : -1); if (ws[i]) { state.week = ws[i]; await signWeek(); render(); } return; }
    if (t.id === "refresh") { t.disabled = true; state.urls = {}; await loadAll(); t.disabled = false; toast("Up to date"); return; }
    if (t.matches("img[data-full]")) { if (!t.dataset.full) return; $("#lbImg").src = t.dataset.full; $("#lbImg").alt = t.alt; $("#lb").classList.add("open"); return; }
    if (t.id === "lbClose") { $("#lb").classList.remove("open"); return; }
    if (t.id === "pick") { $("#file").click(); return; }
    if (t.id === "msgSend") { sendMessage(); return; }
    if (!p) return;

    if (t.dataset.nav) { const tr = $(".track", card); tr.scrollBy({ left: tr.clientWidth * Number(t.dataset.nav), behavior: "smooth" }); return; }
    if (t.dataset.cap !== undefined) { state.capTab[p.id] = Number(t.dataset.cap); render(); return; }
    if (t.dataset.copy !== undefined) { const c = p.captions[Number(t.dataset.copy)]; toast((await copyText(c.text)) ? `${c.label} caption copied` : "Press and hold the caption to copy it"); return; }
    if (t.dataset.dl !== undefined) { t.disabled = true; await saveFile(p.files[Number(t.dataset.dl)]); t.disabled = false; return; }
    if (t.hasAttribute("data-dlall")) {
      t.disabled = true;
      for (const f of p.files) { await saveFile(f); await new Promise((r) => setTimeout(r, 700)); } // browsers drop rapid-fire downloads
      t.disabled = false; return;
    }
    if (t.dataset.s) { const cur = state.reviews[p.id]?.status; if (await setReview(p.id, { status: cur === t.dataset.s ? "" : t.dataset.s })) toast(cur === t.dataset.s ? "Cleared" : "Saved"); return; }
    if (t.hasAttribute("data-savenote")) { const v = $("[data-note]", card).value.trim(); delete state.drafts[p.id]; if (await setReview(p.id, { note: v })) toast("Note saved"); return; }
  });

  document.addEventListener("input", (ev) => { const a = ev.target.closest("article.post"); if (a && ev.target.matches("[data-note]")) state.drafts[a.dataset.id] = ev.target.value; });
  document.addEventListener("keydown", (ev) => { if (ev.key === "Escape") $("#lb").classList.remove("open"); });
  $("#lb").addEventListener("click", (ev) => { if (ev.target.id === "lb") $("#lb").classList.remove("open"); });
  document.addEventListener("scroll", (ev) => {
    const tr = ev.target; if (!(tr instanceof Element) || !tr.matches(".track")) return;
    const c = tr.parentElement.querySelector(".count"); if (!c) return;
    const n = tr.children.length, i = Math.round(tr.scrollLeft / Math.max(1, tr.clientWidth));
    c.textContent = `${Math.min(n, i + 1)} / ${n}`;
  }, true);
  $("#file").addEventListener("change", (ev) => { uploadFiles([...ev.target.files]); ev.target.value = ""; });
  const drop = $("#drop");
  ["dragenter", "dragover"].forEach((n) => drop.addEventListener(n, (e) => { e.preventDefault(); drop.classList.add("over"); }));
  ["dragleave", "drop"].forEach((n) => drop.addEventListener(n, (e) => { e.preventDefault(); drop.classList.remove("over"); }));
  drop.addEventListener("drop", (e) => uploadFiles([...(e.dataTransfer?.files || [])]));

  // Coming back to the tab after a while: links may have expired, so reload quietly
  let hiddenAt = 0;
  document.addEventListener("visibilitychange", () => {
    if (document.hidden) { hiddenAt = Date.now(); return; }
    if (state.user && hiddenAt && Date.now() - hiddenAt > 10 * 60 * 1000) { state.urls = {}; loadAll(); }
  });
})();
