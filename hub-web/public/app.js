// EAGLESCROFT Content Hub: a static page. Posts come from data/posts.json (built from the
// calendars by hub-web/build_data.py); decisions and notes are kept on this device only.
(() => {
  const $ = (s, el = document) => el.querySelector(s);
  const esc = (s) => String(s ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
  const ICON = {
    copy: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="8" y="8" width="14" height="14" rx="2"/><path d="M4 16V4a2 2 0 0 1 2-2h12"/></svg>',
    down: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3v12"/><path d="m7 10 5 5 5-5"/><path d="M5 21h14"/></svg>',
    brush: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="m14.6 3.4 6 6L9 21H3v-6L14.6 3.4Z"/><path d="m11 7 6 6"/></svg>',
    prev: '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"><path d="m15 18-6-6 6-6"/></svg>',
    next: '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"><path d="m9 18 6-6-6-6"/></svg>',
  };
  const BUILD = { ready: ["ready", "Graphic ready"], design: ["design", "In design"], "needs-you": ["needs", "Needs you"] };
  const STATUS = [["approved", "Approve"], ["changes", "Request changes"], ["posted", "Posted"]];
  const LABEL = { approved: "APPROVED", changes: "CHANGES", posted: "POSTED" };

  const state = { posts: [], account: "eaglescroft", week: null, capTab: {}, reviews: {}, general: {} };

  // Device storage: may be unavailable (private mode), so every access is guarded
  const store = {
    get(k, d) { try { const v = localStorage.getItem(k); return v == null ? d : JSON.parse(v); } catch (e) { return d; } },
    set(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); return true; } catch (e) { return false; } },
  };
  state.account = store.get("hub.account", state.account);
  state.reviews = store.get("hub.reviews", {});
  state.general = store.get("hub.general", {});

  const toast = (msg) => { const t = $("#toast"); t.textContent = msg; t.classList.add("show"); clearTimeout(toast.h); toast.h = setTimeout(() => t.classList.remove("show"), 2400); };
  const notice = (html) => { const n = $("#notice"); if (!html) { n.hidden = true; return; } n.innerHTML = html; n.hidden = false; };
  const fmtDay = (iso) => new Date(iso + "T12:00:00").toLocaleDateString("en-GB", { weekday: "short", day: "numeric", month: "short" });
  const fmtWhen = (ts) => ts ? new Date(ts).toLocaleString("en-GB", { weekday: "short", hour: "2-digit", minute: "2-digit" }) : "";

  const weeks = () => [...new Set(state.posts.map((p) => p.week))].sort();
  function pickWeek() {
    const ws = weeks();
    if (!ws.length) { state.week = null; return; }
    if (state.week && ws.includes(state.week)) return;
    const today = new Date().toISOString().slice(0, 10);
    state.week = ws.find((w) => state.posts.some((p) => p.week === w && p.date >= today)) || ws[ws.length - 1];
  }
  const visiblePosts = () => state.posts.filter((p) => p.week === state.week && p.account === state.account)
    .sort((a, b) => (a.date + String(a.order).padStart(3, "0")).localeCompare(b.date + String(b.order).padStart(3, "0")));

  // ---------- Render ----------
  function renderHeader() {
    const ws = weeks(), i = ws.indexOf(state.week);
    $("#weekLabel").textContent = state.week ? state.week.replace(/^\d{4}-/, "") : "—";
    $("#prevWeek").disabled = i <= 0; $("#nextWeek").disabled = i < 0 || i >= ws.length - 1;
    const dates = state.posts.filter((p) => p.week === state.week).map((p) => p.date).sort();
    $("#weekRange").textContent = dates.length ? `${fmtDay(dates[0])} – ${fmtDay(dates[dates.length - 1])} · all times WAT` : "No posts yet.";
    document.querySelectorAll(".seg button").forEach((b) => b.setAttribute("aria-pressed", String(b.dataset.acc === state.account)));
  }

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
    const imgs = m.map((x, i) => `<img src="${esc(x.url)}" alt="${esc(p.title)}, slide ${i + 1} of ${m.length}" loading="lazy" data-full="${esc(x.url)}">`).join("");
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
    return `<div class="row">${all}${files.map((f) => `<a class="btn" href="${esc(f.url)}" download="${esc(f.name)}">${ICON.down}${esc(f.label || f.name)}</a>`).join("")}</div>`;
  }

  function reviewHTML(p) {
    const r = state.reviews[p.id] || {};
    const btns = STATUS.map(([s, l]) => `<button data-s="${s}" aria-pressed="${r.status === s}">${l}</button>`).join("");
    return `<div class="review"><div class="status" role="group" aria-label="Your decision">${btns}</div>
      <label class="sr" for="note-${esc(p.id)}">Notes or changes</label>
      <textarea id="note-${esc(p.id)}" data-note placeholder="Changes you want, the live post link, or how it did…">${esc(r.note || "")}</textarea>
      <div class="row"><span class="saved">${r.at ? "Saved on this device " + esc(fmtWhen(r.at)) : ""}</span></div></div>`;
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

  function feedbackText() {
    const lines = [`Content Hub feedback · ${state.week || ""}`];
    const ps = state.posts.filter((p) => p.week === state.week).sort((a, b) => (a.date + a.account).localeCompare(b.date + b.account));
    for (const p of ps) {
      const r = state.reviews[p.id];
      if (!r || (!r.status && !r.note)) continue;
      lines.push(`${p.id} · ${p.account === "joshua" ? "Joshua" : "EAGLESCROFT"} · ${fmtDay(p.date)} · ${LABEL[r.status] || "NOTE"}${r.note ? ": " + r.note : ""}`);
    }
    const g = (state.general[state.week] || "").trim();
    if (g) lines.push("", g);
    return lines.length > 1 ? lines.join("\n") : "";
  }

  function renderFeedback() {
    const t = feedbackText();
    $("#fbText").value = t || "Approve or comment on a post above, and your feedback appears here.";
    $("#fbCopy").disabled = !t;
    if (document.activeElement !== $("#general")) $("#general").value = state.general[state.week] || "";
  }

  function render() {
    renderHeader();
    const ps = visiblePosts();
    renderStats(ps);
    const act = document.activeElement, focusId = act && act.matches("[data-note]") ? act.closest("article").dataset.id : null;
    const caret = focusId ? [act.selectionStart, act.selectionEnd] : null;
    const scroll = {}; document.querySelectorAll("article.post .track").forEach((tr) => { scroll[tr.closest("article").dataset.id] = tr.scrollLeft; });
    $("#list").innerHTML = ps.length ? ps.map(postHTML).join("") : `<div class="panel empty">No posts for this account and week yet.</div>`;
    document.querySelectorAll("article.post").forEach((a) => {
      const tr = $(".track", a); if (tr && scroll[a.dataset.id]) tr.scrollLeft = scroll[a.dataset.id];
      if (a.dataset.id === focusId) { const t = $("[data-note]", a); t.focus(); t.setSelectionRange(caret[0], caret[1]); }
    });
    renderFeedback();
  }

  // ---------- Actions ----------
  async function copyText(text) {
    try { await navigator.clipboard.writeText(text); return true; } catch (e) {}
    const ta = document.createElement("textarea"); ta.value = text; ta.setAttribute("readonly", ""); ta.style.position = "fixed"; ta.style.opacity = "0";
    document.body.appendChild(ta); ta.select();
    let ok = false; try { ok = document.execCommand("copy"); } catch (e) {}
    ta.remove(); return ok;
  }

  function saveReview(id, patch) {
    const r = { ...(state.reviews[id] || {}), ...patch, at: Date.now() };
    if (!r.status && !r.note) delete state.reviews[id]; else state.reviews[id] = r;
    if (!store.set("hub.reviews", state.reviews)) toast("This browser isn't saving notes (private mode?). Copy your feedback before leaving.");
  }

  document.addEventListener("click", async (ev) => {
    const t = ev.target.closest("button, img[data-full]");
    if (!t) return;
    const card = t.closest("article.post"), p = card && state.posts.find((x) => x.id === card.dataset.id);

    if (t.matches(".seg button")) { state.account = t.dataset.acc; store.set("hub.account", state.account); render(); return; }
    if (t.id === "prevWeek" || t.id === "nextWeek") { const ws = weeks(); const i = ws.indexOf(state.week) + (t.id === "nextWeek" ? 1 : -1); if (ws[i]) { state.week = ws[i]; render(); } return; }
    if (t.matches("img[data-full]")) { $("#lbImg").src = t.dataset.full; $("#lbImg").alt = t.alt; $("#lb").classList.add("open"); return; }
    if (t.id === "lbClose") { $("#lb").classList.remove("open"); return; }
    if (t.id === "fbCopy") { const ok = await copyText(feedbackText()); $("#fbState").textContent = ok ? "Copied. Paste it into our chat." : "Select the text above and copy it."; return; }
    if (!p) return;

    if (t.dataset.nav) { const tr = $(".track", card); tr.scrollBy({ left: tr.clientWidth * Number(t.dataset.nav), behavior: "smooth" }); return; }
    if (t.dataset.cap !== undefined) { state.capTab[p.id] = Number(t.dataset.cap); render(); return; }
    if (t.dataset.copy !== undefined) { const c = p.captions[Number(t.dataset.copy)]; toast((await copyText(c.text)) ? `${c.label} caption copied` : "Press and hold the caption to copy it"); return; }
    if (t.hasAttribute("data-dlall")) {
      t.disabled = true;
      for (const a of card.querySelectorAll("a[download]")) { a.click(); await new Promise((r) => setTimeout(r, 700)); } // browsers drop rapid-fire downloads
      t.disabled = false; return;
    }
    if (t.dataset.s) {
      const cur = state.reviews[p.id]?.status;
      saveReview(p.id, { status: cur === t.dataset.s ? "" : t.dataset.s });
      render(); toast(cur === t.dataset.s ? "Cleared" : "Saved on this device"); return;
    }
  });

  // Notes save as you type (after a short pause)
  let noteTimer = null;
  document.addEventListener("input", (ev) => {
    const a = ev.target.closest("article.post");
    if (a && ev.target.matches("[data-note]")) {
      clearTimeout(noteTimer);
      const id = a.dataset.id, v = ev.target.value;
      noteTimer = setTimeout(() => { saveReview(id, { note: v.trim() }); const s = $(".saved", a); if (s) s.textContent = "Saved on this device " + fmtWhen(Date.now()); renderStats(visiblePosts()); renderFeedback(); }, 500);
    }
    if (ev.target.id === "general") { state.general[state.week] = ev.target.value; store.set("hub.general", state.general); renderFeedback(); }
  });
  document.addEventListener("keydown", (ev) => { if (ev.key === "Escape") $("#lb").classList.remove("open"); });
  $("#lb").addEventListener("click", (ev) => { if (ev.target.id === "lb") $("#lb").classList.remove("open"); });
  document.addEventListener("scroll", (ev) => {
    const tr = ev.target; if (!(tr instanceof Element) || !tr.matches(".track")) return;
    const c = tr.parentElement.querySelector(".count"); if (!c) return;
    const n = tr.children.length, i = Math.round(tr.scrollLeft / Math.max(1, tr.clientWidth));
    c.textContent = `${Math.min(n, i + 1)} / ${n}`;
  }, true);

  fetch("data/posts.json", { cache: "no-cache" })
    .then((r) => { if (!r.ok) throw new Error(r.status); return r.json(); })
    .then((data) => { state.posts = data.posts || []; pickWeek(); render(); })
    .catch(() => { $("#list").innerHTML = ""; notice("Couldn't load the posts. Refresh the page to try again."); });
})();
