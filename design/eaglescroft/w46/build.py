"""EAGLESCROFT · Thu 12 – Wed 18 Nov 2026 · seven posts in the Blue Glass look.

    python3 design/eaglescroft/w46/build.py            # writes <post>/slide-N.html
    python3 design/eaglescroft/w46/build.py --render   # also renders every slide to PNG
"""
import pathlib
import subprocess
import sys

HERE = pathlib.Path(__file__).parent
ROOT = HERE.parents[2]

HEAD = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<base href="../../../../">
<meta name="es-size" content="1080x1350">
<title>EAGLESCROFT · {title} · {n}</title>
<link rel="stylesheet" href="design/templates/shared.css">
<link rel="stylesheet" href="design/icons/icons.css">
<link rel="stylesheet" href="design/templates/glass.css">
<link rel="stylesheet" href="design/eaglescroft/w46/w46.css">
</head>
<body>
<div class="canvas glass {tone}">
{bubbles}
"""

FOOT = """  <div class="g-brand"><img class="mk" src="design/brand/eagle-{mark}-mark.png" alt=""><span class="wm">EAGLESCROFT</span>{pg}</div>
</div>
</body>
</html>
"""

MARKER = ('<svg viewBox="0 0 30 18" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round">'
          '<circle cx="15" cy="11" r="4.6"/><path d="M1.5 11H10.2M19.8 11H28.5M15 6.4V1.6"/></svg>')
STAR = '<svg class="spark" style="{s}" viewBox="0 0 24 24"><path d="M12 0c.9 6.2 5.1 10.6 12 12-6.9 1.4-11.1 5.8-12 12-.9-6.2-5.1-10.6-12-12C6.9 10.6 11.1 6.2 12 0z"/></svg>'


def cursor(tone="vivid"):
    fill, stroke = ("#fff", "#1D4ED8") if tone == "vivid" else ("#2F6BFF", "#fff")
    return f'<svg class="cur" viewBox="0 0 24 24"><path d="M4 3l16 7-7 2-3 7z" fill="{fill}" stroke="{stroke}" stroke-width="1.6" stroke-linejoin="round"/></svg>'


def bubbles(tone):
    if tone == "vivid":
        return ('  <div class="bubble-bg" style="width:420px;height:420px;left:-160px;top:-140px"></div>\n'
                '  <div class="bubble-bg" style="width:300px;height:300px;right:-110px;bottom:180px"></div>')
    return ('  <div class="bubble-bg" style="width:360px;height:360px;right:-150px;top:-120px"></div>\n'
            '  <div class="bubble-bg" style="width:260px;height:260px;left:-120px;bottom:240px"></div>')


def kicker(text):
    return f'<div class="g-kicker">{MARKER}{text}</div>'


def num(n, label):
    return f'<div class="g-num"><b>{n:02d}</b>{label}</div>'


def centred(inner, top=120, bottom=170):
    return (f'  <div style="position:absolute;left:96px;right:96px;top:{top}px;bottom:{bottom}px;'
            f'display:flex;flex-direction:column;justify-content:center">\n{inner}\n  </div>')


def row(icon, title, text, extra_cls="", tile_cls=""):
    if icon.startswith("logo:"):
        ti = f'<span class="ti logo"><img src="design/logos/{icon[5:]}.svg" alt=""></span>'
    elif icon.startswith("letter:"):
        ti = f'<span class="ti letter {tile_cls}">{icon[7:]}</span>'
    else:
        ti = f'<span class="ti {tile_cls}"><span class="ic i-{icon}"></span></span>'
    return f'<div class="row-c {extra_cls}">{ti}<div><h3>{title}</h3><p>{text}</p></div></div>'


POSTS = {}


def post(folder, title):
    def deco(fn):
        POSTS[folder] = (title, fn)
        return fn
    return deco


def page(title, n, total, tone, body, pg=True):
    pg_html = f'<span class="pg">{n} / {total}</span>' if pg and total > 1 else ""
    return (HEAD.format(title=title, n=n, tone=tone, bubbles=bubbles(tone)) + body + "\n" +
            FOOT.format(mark="white" if tone == "vivid" else "navy", pg=pg_html))


# ---------------------------------------------------------------- Thu 12 · lead engine
@post("012-lead-engine", "Flight Report · lead engine")
def lead_engine(t):
    T = 6
    s = {}
    s[1] = page(t, 1, T, "vivid", centred(f"""
    {kicker("Flight Report · CRM + outreach")}
    <h1 class="g-hl" style="margin-top:28px;font-size:86px"><b>13,000</b> raw records.<br><span class="boxword"><b>12,000+</b>{cursor()}</span> <span class="acc">scored leads.</span></h1>
    <p class="g-sub">How we turned a list nobody could use into a ranked call sheet, step by step.</p>
    <div class="stats" style="margin-top:56px">
      <div class="stat-c"><b>13,000</b><span>raw records in</span></div>
      <div class="stat-c hi"><b>12,000+</b><span>scored and ranked</span></div>
      <div class="stat-c"><b>1</b><span>tailored opening line per lead</span></div>
      <div class="stat-c"><b>100%</b><span>approved by a human</span></div>
    </div>""") + STAR.format(s="right:110px;top:150px;width:46px;height:46px"))
    s[2] = page(t, 2, T, "light", centred(f"""
    {num(1, "The problem")}
    <h2 class="g-hl" style="margin-top:30px;font-size:74px">A huge list.<br><b class="acc">No one knew who to call first.</b></h2>
    <div class="sheet" style="margin-top:50px">
      <div class="bar"><span>PROSPECTS.xlsx</span><span>13,000 rows</span></div>
      <table>
        <tr><th>Company</th><th>Sector</th><th>Email</th><th>Phone</th></tr>
        <tr><td class="dup">Company A Ltd</td><td>Catering</td><td>info@…</td><td class="bad">—</td></tr>
        <tr><td class="dup">Company A Ltd</td><td>Catering</td><td>info@…</td><td class="bad">—</td></tr>
        <tr><td>Company B</td><td class="bad">?</td><td class="bad">bounced</td><td>+44 …</td></tr>
        <tr><td>Company C</td><td>Retail</td><td class="bad">—</td><td>+44 …</td></tr>
      </table>
    </div>
    <div class="g-card" style="margin-top:30px"><div class="lbl"><span class="ic i-message-circle"></span>Every message started the same</div><p>"Dear Sir/Madam, we are a leading company…"</p></div>"""))
    s[3] = page(t, 3, T, "vivid", centred(f"""
    {num(2, "Clean")}
    <h2 class="g-hl" style="margin-top:30px;font-size:76px">Clean it first.<br><span class="acc">Then trust it.</span></h2>
    <div class="rows" style="margin-top:50px">
      {row("copy", "Remove duplicates", "Same company, five rows? Merged into one.")}
      {row("wand-sparkles", "Fix broken fields", "Bounced emails, bad numbers and empty sectors flagged and repaired.")}
      {row("database", "Fill the gaps", "Missing details enriched, so every lead can be scored fairly.")}
    </div>"""))
    s[4] = page(t, 4, T, "light", centred(f"""
    {num(3, "Score")}
    <h2 class="g-hl" style="margin-top:30px;font-size:74px">Rank every lead on<br><b class="acc">fit and intent.</b></h2>
    <div class="lb" style="margin-top:50px">
      <div class="lb-r"><div><b>Lead #0412</b><small>Catering · UK</small></div><div class="bar"><i style="width:92%"></i></div><span class="tag hot">Call today</span></div>
      <div class="lb-r"><div><b>Lead #1187</b><small>Hospitality · UK</small></div><div class="bar"><i style="width:84%"></i></div><span class="tag hot">Call today</span></div>
      <div class="lb-r"><div><b>Lead #0093</b><small>Events · Ireland</small></div><div class="bar"><i style="width:68%"></i></div><span class="tag warm">This week</span></div>
      <div class="lb-r"><div><b>Lead #2240</b><small>Retail · UK</small></div><div class="bar"><i style="width:38%"></i></div><span class="tag cool">Nurture</span></div>
    </div>
    <p class="g-sub" style="margin-top:28px">The team starts every morning at the top of the list, not at row one.</p>"""))
    s[5] = page(t, 5, T, "vivid", centred(f"""
    {num(4, "Write")}
    <h2 class="g-hl" style="margin-top:30px;font-size:74px">AI drafts the opener.<br><span class="boxword"><b>A human</b>{cursor()}</span> <span class="acc">approves it.</span></h2>
    <div class="draft" style="margin-top:60px">
      <div class="lbl">AI draft · example</div>
      <p>"Congrats on opening your second kitchen this year. Most caterers we speak to at that stage are drowning in enquiry emails. Worth a quick chat about automating the first reply?"</p>
      <div class="acts"><span class="ok"><span class="ic i-check-check"></span>Approve</span><span class="ed"><span class="ic i-pen-line"></span>Edit</span></div>
    </div>
    <p class="g-sub" style="margin-top:30px">Nothing goes out without a person reading it first. That part stays human.</p>"""))
    s[6] = page(t, 6, T, "light", centred(f"""
    {kicker("The lesson")}
    <h2 class="g-hl" style="margin-top:28px;font-size:84px">Your list is worth<br><span class="boxword"><b>more</b>{cursor("light")}</span> <b class="acc">than you think.</b></h2>
    <p class="g-sub">It doesn't need more leads. It needs a system: clean, score, write, approve.</p>
    <div style="margin-top:60px;display:flex;flex-direction:column;gap:20px;align-items:flex-start">
      <div class="g-pill"><span>Want us to look at yours?</span><span class="ic i-arrow-right" style="font-size:28px"></span></div>
      <div class="g-pill"><span>eaglescroft.com.ng</span><span class="ic i-globe" style="font-size:28px"></span></div>
    </div>""") + STAR.format(s="right:130px;top:330px;width:46px;height:46px"))
    return s


# ---------------------------------------------------------------- Fri 13 · website check
@post("013-website-check", "Ground School · website check")
def website_check(t):
    T = 6
    s = {}
    s[1] = page(t, 1, T, "vivid", centred(f"""
    {kicker("Ground School · websites")}
    <h1 class="g-hl" style="margin-top:28px;font-size:88px">Is your website<br><span class="boxword"><b>losing</b>{cursor()}</span> <span class="acc">customers?</span></h1>
    <p class="g-sub">The 7-point check we run on every site. Fewer than 6 ticks? That's where your leads leak.</p>
    <div class="browser" style="margin-top:56px;width:760px">
      <div class="bar"><i></i><i></i><i></i><span class="url"><span class="ic i-shield-check" style="color:#15803D"></span>yourbusiness.com</span></div>
      <div class="pg" style="display:grid;gap:14px">
        <div style="height:26px;width:70%;border-radius:8px;background:#DCE8FF"></div>
        <div style="height:16px;width:90%;border-radius:8px;background:#EEF2FA"></div>
        <div style="height:16px;width:82%;border-radius:8px;background:#EEF2FA"></div>
        <div style="display:flex;gap:12px;margin-top:8px"><span style="padding:12px 22px;border-radius:10px;background:#2F6BFF;color:#fff;font-weight:700;font-size:20px">Chat on WhatsApp</span><span style="padding:12px 22px;border-radius:10px;border:2px solid #2F6BFF;color:#2F6BFF;font-weight:700;font-size:20px">Call us</span></div>
      </div>
    </div>""") +
        '<div class="chip-ui" style="right:96px;top:840px;transform:rotate(4deg)"><span class="ic i-timer"></span>3s load</div>'
        '<div class="chip-ui" style="right:150px;top:960px;transform:rotate(-3deg)"><span class="ic i-circle-check"></span>7-point check</div>')
    s[2] = page(t, 2, T, "light", centred(f"""
    {num(1, "Checks 1–2")}
    <h2 class="g-hl" style="margin-top:30px;font-size:78px">Fast and <b class="acc">thumb-friendly.</b></h2>
    <div class="rows" style="margin-top:50px">
      {row("timer", "1 · Speed", "Open it on mobile data. Does it load in about 3 seconds? Slow pages lose people before they read a word.")}
      {row("store", "2 · Mobile", "Can you read and tap everything without zooming or pinching? Most of your visitors are on a phone.")}
    </div>"""))
    s[3] = page(t, 3, T, "vivid", centred(f"""
    {num(3, "Checks 3–4")}
    <h2 class="g-hl" style="margin-top:30px;font-size:78px">Clear in <span class="acc">5 seconds.</span></h2>
    <div class="rows" style="margin-top:50px">
      {row("eye", "3 · Headline", "Does a stranger know what you do, and for whom, within 5 seconds of landing?")}
      {row("mouse-pointer-2", "4 · One action", "Is there one obvious next step: call, WhatsApp, book or buy? Too many buttons means no clicks.")}
    </div>"""))
    s[4] = page(t, 4, T, "light", centred(f"""
    {num(5, "Checks 5–6")}
    <h2 class="g-hl" style="margin-top:30px;font-size:78px">Easy to reach.<br><b class="acc">Easy to find.</b></h2>
    <div class="rows" style="margin-top:50px">
      {row("logo:whatsapp", "5 · One tap to talk", "WhatsApp or click-to-call visible on every page, not hidden in a contact form.")}
      {row("logo:google", "6 · Google Business Profile", "Complete, with hours, photos, reviews and your website link. It's often the first page people see.")}
    </div>"""))
    s[5] = page(t, 5, T, "vivid", centred(f"""
    {num(7, "Check 7")}
    <h2 class="g-hl" style="margin-top:30px;font-size:78px">Does it feel <span class="boxword"><b>safe</b>{cursor()}</span><br><span class="acc">to buy from you?</span></h2>
    <div class="rows" style="margin-top:56px">
      {row("shield-check", "Padlock (HTTPS)", "The browser shows your site as secure.")}
      {row("camera", "Real photos", "Your team, your work, your premises. Not just stock images.")}
      {row("star", "Reviews you can see", "Recent reviews on the site or on Google, with replies.")}
    </div>"""))
    s[6] = page(t, 6, T, "light", centred(f"""
    {kicker("Your score")}
    <h2 class="g-hl" style="margin-top:28px;font-size:86px">Fewer than<br><span class="boxword"><b>6 ticks?</b>{cursor("light")}</span></h2>
    <p class="g-sub" style="font-size:32px">That's where your leads are leaking. Save this and run the check today.</p>
    <div style="margin-top:60px;display:flex;flex-direction:column;gap:20px;align-items:flex-start">
      <div class="g-pill"><span>Book a free call with EAGLESCROFT</span><span class="ic i-arrow-right" style="font-size:28px"></span></div>
      <div class="g-pill"><span>eaglescroft.com.ng</span><span class="ic i-globe" style="font-size:28px"></span></div>
    </div>""") + STAR.format(s="right:150px;top:300px;width:50px;height:50px"))
    return s


# ---------------------------------------------------------------- Sat 14 · brief AI like a new hire
@post("014-brief-ai", "Cockpit Chat · brief AI")
def brief_ai(t):
    body = centred(f"""
    {kicker("Cockpit Chat · how we use AI")}
    <h1 class="g-hl" style="margin-top:26px;font-size:80px">Brief AI like a<br><span class="boxword"><b>new hire.</b>{cursor("light")}</span></h1>
    <div class="rows" style="margin-top:44px;gap:14px">
      {row("letter:R", "Role", "<em>You're a copywriter for a bakery in Abuja.</em>", "ex")}
      {row("letter:C", "Context", "<em>Customers order birthday cakes on WhatsApp.</em>", "ex")}
      {row("letter:T", "Task", "<em>Write 3 captions for our new red velvet cake.</em>", "ex")}
      {row("letter:F", "Format", "<em>Under 40 words each. Warm, simple, one emoji max.</em>", "ex")}
      {row("letter:R", "Rules", "<em>No prices. No made-up offers or claims.</em>", "ex")}
    </div>
    <p class="g-sub" style="margin-top:26px;font-size:26px">Five lines in, a far better first draft out. Then a human edits it. Every time.</p>""", top=100, bottom=150)
    return {1: page(t, 1, 1, "light", body.replace('class="row-c ex"', 'class="row-c ex" style="padding:16px 22px"'), pg=False)}


# ---------------------------------------------------------------- Sun 15 · how we work
@post("015-how-we-work", "Hangar Notes · how we work")
def how_we_work(t):
    pts = [("search", "Discover", "Your business, customers and goals", 14, 86),
           ("pen-line", "Design", "Brand, pages and journeys, approved by you", 50, 72),
           ("zap", "Build", "Websites, apps, CRMs and content", 86, 58),
           ("bot", "Automate", "AI and workflows take the repetitive work", 14, 38),
           ("send", "Launch", "Tested, tracked, handed over properly", 50, 24),
           ("shield-check", "Support", "We stay on after take-off", 86, 10)]
    wps = "".join(
        f'<div class="wp" style="left:{x}%;top:{y}%"><div class="t"><span class="ic i-{ic}"></span></div>'
        f'<span class="no">0{i + 1}</span><b>{name}</b><span>{txt}</span></div>'
        for i, (ic, name, txt, x, y) in enumerate(pts))
    path = ('<svg class="path" viewBox="0 0 888 760" preserveAspectRatio="none" fill="none">'
            '<path d="M124 650 C 300 640, 330 560, 444 545 S 700 470, 764 440 C 820 400, 300 330, 124 290 S 330 200, 444 182 S 700 110, 764 76" '
            'stroke="rgba(255,255,255,.55)" stroke-width="5" stroke-dasharray="4 16" stroke-linecap="round"/></svg>')
    body = f"""  <div style="position:absolute;left:96px;right:96px;top:110px">
    {kicker("Hangar Notes · how we work")}
    <h1 class="g-hl" style="margin-top:24px;font-size:76px">How a project <span class="boxword"><b>flies</b>{cursor()}</span><br><span class="acc">with EAGLESCROFT.</span></h1>
    <div class="fp">{path}{wps}</div>
  </div>
  <div class="chip-ui" style="left:96px;bottom:150px"><span class="ic i-globe"></span>Abuja to the world</div>
  <div class="chip-ui" style="right:96px;bottom:150px">We Help Businesses Fly Online</div>
  {STAR.format(s="right:120px;top:140px;width:44px;height:44px")}"""
    return {1: page(t, 1, 1, "vivid", body, pg=False)}


# ---------------------------------------------------------------- Mon 16 · automation objections
@post("016-automation-objections", "Ground School · automation objections")
def objections(t):
    T = 6
    s = {}
    s[1] = page(t, 1, T, "vivid", centred(f"""
    {kicker("Ground School · AI automation")}
    <h1 class="g-hl" style="margin-top:28px;font-size:86px"><b>4 reasons</b><br>businesses haven't<br>automated yet.</h1>
    <p class="g-sub" style="font-size:32px">And our <span class="boxword" style="font-weight:700">honest answers.{cursor()}</span></p>
    <div style="position:relative;height:420px;margin-top:40px">
      <div class="chip-ui" style="left:0;top:20px;transform:rotate(-3deg);font-size:27px">"I don't know where to start."</div>
      <div class="chip-ui" style="left:360px;top:120px;transform:rotate(2deg);font-size:27px">"It sounds expensive."</div>
      <div class="chip-ui" style="left:30px;top:220px;transform:rotate(-1.5deg);font-size:27px">"My customers want a human."</div>
      <div class="chip-ui" style="left:300px;top:320px;transform:rotate(2.5deg);font-size:27px">"I don't trust AI with my data."</div>
    </div>""") + STAR.format(s="right:120px;top:160px;width:46px;height:46px"))
    items = [
        ("light", "“I don't know<br>where to start.”", "Start with the question you answer 20 times a day.",
         ["One workflow, not a whole system", "e.g. instant replies to price or delivery questions", "Measure the hours saved in week one"]),
        ("vivid", "“It sounds<br>expensive.”", "Start small, with tools you already pay for.",
         ["Most email, CRM and WhatsApp tools already include automation", "Prove the time saved first", "Then decide what's worth spending on"]),
        ("light", "“My customers<br>want a human.”", "Good. Automate the waiting, not the relationship.",
         ["Instant first reply, any time of day", "A person takes over the real conversation", "Customers notice speed, not the bot"]),
        ("vivid", "“I don't trust AI<br>with my data.”", "Fair. Ask before you plug anything in:",
         ["Who can see our data, and where is it stored?", "Is it used to train the model?", "Never paste customer data into public AI tools"]),
    ]
    for i, (tone, q, ans, ticks) in enumerate(items):
        li = "".join(f'<li><span class="ic i-circle-check"></span>{x}</li>' for x in ticks)
        s[i + 2] = page(t, i + 2, T, tone, centred(f"""
    {num(i + 1, "Reason")}
    <div class="quote-c" style="margin-top:34px">{q}</div>
    <div class="g-card" style="margin-top:44px"><div class="lbl"><span class="ic i-message-circle"></span>Our honest answer</div>
      <p style="font-size:36px">{ans}</p>
      <ul class="ticks" style="gap:20px">{li.replace('<li>', '<li style="font-size:30px">')}</ul>
    </div>"""))
    s[6] = page(t, 6, T, "light", centred(f"""
    {kicker("Your turn")}
    <h2 class="g-hl" style="margin-top:28px;font-size:86px">Which one<br>is <span class="boxword"><b>yours?</b>{cursor("light")}</span></h2>
    <p class="g-sub" style="font-size:32px">Comment 1, 2, 3 or 4. We'll answer every one.</p>
    <div style="display:flex;gap:18px;margin-top:50px">
      {''.join(f'<span class="tile-g" style="position:static;width:120px;height:120px;font-family:var(--font-display);font-weight:700;font-size:56px">{n}</span>' for n in range(1, 5))}
    </div>
    <div class="g-pill" style="margin-top:56px"><span>Or book a free call: eaglescroft.com.ng</span><span class="ic i-arrow-right" style="font-size:28px"></span></div>"""))
    return s


# ---------------------------------------------------------------- Tue 17 · On the Radar
@post("017-ai-agents-radar", "On the Radar · AI agents on WhatsApp and Google")
def radar(t):
    T = 4
    s = {}
    s[1] = page(t, 1, T, "vivid", centred(f"""
    {kicker("On the Radar · November")}
    <h1 class="g-hl" style="margin-top:28px;font-size:80px">AI can now answer<br>your customers on<br><b>WhatsApp</b> and <b>Google.</b></h1>
    <p class="g-sub" style="font-size:34px;margin-top:34px">Should you <span class="boxword" style="font-weight:700">switch it on?{cursor()}</span></p>
    <div style="height:300px"></div>""") +
        '<div class="logo-g" style="left:150px;top:880px;transform:rotate(-8deg)"><img src="design/logos/whatsapp.svg" alt="WhatsApp"></div>'
        '<div class="logo-g" style="left:420px;top:940px;transform:rotate(6deg)"><img src="design/logos/google.svg" alt="Google"></div>'
        '<div class="chip-ui" style="right:110px;top:900px;transform:rotate(3deg)"><span class="ic i-bot"></span>AI replies</div>'
        '<div class="chip-ui" style="right:150px;top:1010px;transform:rotate(-2deg)"><span class="ic i-users"></span>Human handoff</div>'
        + STAR.format(s="right:120px;top:160px;width:46px;height:46px"))
    s[2] = page(t, 2, T, "light", centred(f"""
    {num(1, "WhatsApp")}
    <h2 class="g-hl" style="margin-top:30px;font-size:72px">Meta <b class="acc">Business Agent</b></h2>
    <div class="chat" style="margin-top:40px">
      <div class="h"><img src="design/logos/whatsapp.svg" alt=""><div>Your Business<small>AI agent · replies instantly</small></div></div>
      <div class="b in">Do you have this in size 42?</div>
      <div class="b ai wa"><small>AI agent</small>Yes, in black and brown. Would you like to book a fitting for Saturday?</div>
    </div>
    <p class="illus" style="margin-top:12px">Illustration</p>
    <ul class="ticks">
      <li><span class="ic i-circle-check"></span>Answers questions, recommends products, books appointments</li>
      <li><span class="ic i-circle-check"></span>Hands over to your team when you decide it should</li>
      <li><span class="ic i-circle-check"></span>Launched globally in June 2026; check pricing in your account</li>
    </ul>"""))
    s[3] = page(t, 3, T, "vivid", centred(f"""
    {num(2, "Google")}
    <h2 class="g-hl" style="margin-top:30px;font-size:72px">AI messaging on<br><span class="acc">Business Profiles</span></h2>
    <div class="chat" style="margin-top:40px">
      <div class="h"><img src="design/logos/google.svg" alt=""><div>Your Business · Search and Maps<small>Chat · answered by AI</small></div></div>
      <div class="b in">Are you open on Sunday?</div>
      <div class="b ai"><small>AI agent</small>Yes, from 12pm to 5pm. Want me to pass a message to the team?</div>
    </div>
    <p class="illus" style="margin-top:12px">Illustration</p>
    <ul class="ticks">
      <li><span class="ic i-circle-check"></span>Answers routine questions from people who find you on Search and Maps</li>
      <li><span class="ic i-circle-check"></span>Hands the rest to you; you can take over any time</li>
      <li><span class="ic i-circle-check"></span>A pilot that started opening to more businesses in late October</li>
    </ul>"""))
    s[4] = page(t, 4, T, "light", centred(f"""
    {kicker("Our take")}
    <h2 class="g-hl" style="margin-top:28px;font-size:78px">Switch it on <span class="boxword"><b>when…</b>{cursor("light")}</span></h2>
    <ul class="ticks" style="margin-top:46px;gap:22px">
      <li style="font-size:30px"><span class="ic i-circle-check"></span>Your answers are written down: prices, hours, delivery, policies</li>
      <li style="font-size:30px"><span class="ic i-circle-check"></span>Someone reads the conversations every day</li>
      <li style="font-size:30px"><span class="ic i-circle-check"></span>You've checked what it costs in your account</li>
      <li class="no" style="font-size:30px"><span class="ic i-x-circle"></span>Not yet if your information changes daily and lives in your head</li>
    </ul>
    <div class="g-pill" style="margin-top:56px"><span>Want it set up properly? eaglescroft.com.ng</span><span class="ic i-arrow-right" style="font-size:28px"></span></div>"""))
    return s


# ---------------------------------------------------------------- Wed 18 · ads checklist
@post("018-ads-checklist", "Ground School · before you boost")
def ads(t):
    T = 6
    s = {}
    s[1] = page(t, 1, T, "vivid", centred(f"""
    {kicker("Ground School · digital marketing")}
    <h1 class="g-hl" style="margin-top:28px;font-size:88px">Before you<br><span class="boxword"><b>boost</b>{cursor()}</span> that post…</h1>
    <p class="g-sub" style="font-size:32px">5 checks so your ad money isn't wasted.</p>
    <div style="height:330px"></div>""") +
        '<div style="position:absolute;left:96px;top:930px;z-index:3;padding:22px 40px;border-radius:14px;background:#fff;color:#1D4ED8;font-weight:700;font-size:30px;box-shadow:0 30px 50px -20px rgba(0,10,60,.7);transform:rotate(-3deg)">Boost post</div>'
        '<div class="logo-g" style="right:330px;top:860px;transform:rotate(7deg);width:150px;height:150px"><img src="design/logos/meta.svg" alt="Meta"></div>'
        '<div class="logo-g" style="right:110px;top:960px;transform:rotate(-6deg);width:150px;height:150px"><img src="design/logos/google.svg" alt="Google"></div>'
        + STAR.format(s="right:120px;top:160px;width:46px;height:46px"))
    s[2] = page(t, 2, T, "light", centred(f"""
    {num(1, "Audience")}
    <h2 class="g-hl" style="margin-top:30px;font-size:78px">Who is it for?<br><b class="acc">Not "everyone".</b></h2>
    <div style="position:relative;height:300px;margin-top:40px">
      <div class="chip-ui" style="left:0;top:0;font-size:27px"><span class="ic i-globe"></span>Location: Abuja + 20km</div>
      <div class="chip-ui" style="left:420px;top:60px;font-size:27px"><span class="ic i-users"></span>Age 25–44</div>
      <div class="chip-ui" style="left:40px;top:130px;font-size:27px"><span class="ic i-heart-handshake"></span>Interests: weddings, events</div>
      <div class="chip-ui" style="left:330px;top:210px;font-size:27px"><span class="ic i-x-circle"></span>Not: the whole country</div>
    </div>
    <p class="g-sub">The tighter the audience, the cheaper every result.</p>"""))
    s[3] = page(t, 3, T, "vivid", centred(f"""
    {num(2, "Goal")}
    <h2 class="g-hl" style="margin-top:30px;font-size:78px">Pick <span class="boxword"><b>one</b>{cursor()}</span> goal.</h2>
    <div class="rows" style="margin-top:50px;gap:16px">
      {row("message-circle", "Messages", "People start a WhatsApp or Messenger chat", "", "")}
      <div class="row-c" style="opacity:.55"><span class="ti"><span class="ic i-clock"></span></span><div><h3>Calls</h3><p>Your phone rings</p></div></div>
      <div class="row-c" style="opacity:.55"><span class="ti"><span class="ic i-globe"></span></span><div><h3>Website visits</h3><p>Traffic to one page</p></div></div>
      <div class="row-c" style="opacity:.55"><span class="ti"><span class="ic i-store"></span></span><div><h3>Sales</h3><p>Purchases you can track</p></div></div>
    </div>"""))
    s[4] = page(t, 4, T, "light", centred(f"""
    {num(3, "Landing")}
    <h2 class="g-hl" style="margin-top:30px;font-size:78px">Is the landing spot<br><b class="acc">ready?</b></h2>
    <div class="rows" style="margin-top:50px">
      {row("logo:whatsapp", "A WhatsApp someone answers", "Quick replies saved, someone on duty, an away message after hours.")}
      {row("timer", "Or a page that loads fast", "One offer, one button, and it works on a phone on mobile data.")}
    </div>
    <p class="g-sub">Ads don't fix a broken journey. They make it more expensive.</p>"""))
    s[5] = page(t, 5, T, "vivid", centred(f"""
    {num(4, "Track · test")}
    <h2 class="g-hl" style="margin-top:30px;font-size:76px">Measure it.<br><span class="acc">Then scale the winner.</span></h2>
    <div class="rows" style="margin-top:46px">
      {row("logo:meta", "4 · Tracking on", "Meta Pixel or the Google tag installed, so you know what actually worked.")}
      {row("zap", "5 · Test small", "Two versions, a small budget, a few days. Then put the money behind the winner.")}
    </div>"""))
    s[6] = page(t, 6, T, "light", centred(f"""
    {kicker("Before you press the button")}
    <h2 class="g-hl" style="margin-top:28px;font-size:84px">Ads amplify<br>what's <span class="boxword"><b>already there.</b>{cursor("light")}</span></h2>
    <p class="g-sub" style="font-size:32px">Get the 5 checks right and every naira works harder.</p>
    <div style="margin-top:56px;display:flex;flex-direction:column;gap:20px;align-items:flex-start">
      <div class="g-pill"><span>Want us to set up your next campaign?</span><span class="ic i-arrow-right" style="font-size:28px"></span></div>
      <div class="g-pill"><span>eaglescroft.com.ng</span><span class="ic i-globe" style="font-size:28px"></span></div>
    </div>""") + STAR.format(s="right:140px;top:330px;width:46px;height:46px"))
    return s


# ---------------------------------------------------------------- Sat 14 · branding
@post("019-brand-not-logo", "Ground School · your logo isn't your brand")
def brand(t):
    T = 6
    s = {}
    s[1] = page(t, 1, T, "vivid", centred(f"""
    {kicker("Ground School · branding")}
    <h1 class="g-hl" style="margin-top:28px;font-size:92px">Your <span class="boxword"><b>logo</b>{cursor()}</span><br>isn't your brand.</h1>
    <p class="g-sub" style="font-size:32px">A logo is a signature. A brand is the whole handwriting.</p>
    <div style="display:grid;grid-template-columns:200px 1fr;gap:22px;margin-top:56px;align-items:stretch">
      <div class="tile-g white" style="position:static;width:200px;height:200px;border-radius:44px;font-family:var(--font-display);font-weight:700;font-size:96px;color:#1D4ED8">Aa</div>
      <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:12px">
        <div class="swatch" style="background:#001E60;color:#fff">NAVY</div><div class="swatch" style="background:#2563EB;color:#fff">BLUE</div>
        <div class="swatch" style="background:#93C5FD;color:#0B2A7A">SKY</div><div class="swatch" style="background:#fff;color:#0B2A7A">WHITE</div>
        <div class="chip-ui" style="position:static;grid-column:span 2;justify-content:center">Voice: warm · clear</div>
        <div class="chip-ui" style="position:static;grid-column:span 2;justify-content:center">Same everywhere</div>
      </div>
    </div>""") + STAR.format(s="right:120px;top:150px;width:46px;height:46px"))
    s[2] = page(t, 2, T, "light", centred(f"""
    {num(1, "The logo")}
    <h2 class="g-hl" style="margin-top:30px;font-size:80px">The logo is just<br>the <b class="acc">signature.</b></h2>
    <div class="rows" style="margin-top:50px">
      {row("eye", "It helps people recognise you", "On a signboard, a profile picture, a receipt.")}
      {row("x-circle", "It can't tell them why to choose you", "That's the job of everything around it: how you look, sound and behave.")}
    </div>
    <p class="g-sub">That's why a new logo rarely fixes a brand.</p>"""))
    s[3] = page(t, 3, T, "vivid", centred(f"""
    {num(2, "Colour & type")}
    <h2 class="g-hl" style="margin-top:30px;font-size:78px">Colours and type,<br><span class="acc">used everywhere.</span></h2>
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:22px;margin-top:50px">
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px">
        <div class="swatch" style="background:#001E60;color:#fff;height:150px">#001E60</div><div class="swatch" style="background:#2563EB;color:#fff;height:150px">#2563EB</div>
        <div class="swatch" style="background:#93C5FD;color:#0B2A7A;height:150px">#93C5FD</div><div class="swatch" style="background:#F4F6FB;color:#0B2A7A;height:150px">#F4F6FB</div>
      </div>
      <div class="type-spec"><b>Aa</b><p style="margin:14px 0 0;font-size:22px;color:#48526E">One headline font. One body font. The same sizes on every page, post and document.</p></div>
    </div>
    <p class="g-sub">Pick a few. Write them down. Never improvise.</p>"""))
    s[4] = page(t, 4, T, "light", centred(f"""
    {num(3, "Voice")}
    <h2 class="g-hl" style="margin-top:30px;font-size:76px">How you <b class="acc">sound</b> matters<br>as much as how you look.</h2>
    <div style="display:grid;gap:18px;margin-top:46px">
      <div class="msg-card" style="background:#F3F4F6;color:#6B7280;border:2px dashed #CBD2E0"><span class="g-kicker" style="color:#9CA3AF;font-size:14px">Off-brand</span><br>"Dear valued customer, kindly be informed that your order has been processed accordingly."</div>
      <div class="msg-card" style="background:#fff;border:2px solid #2F6BFF;color:#0B1530"><span class="g-kicker" style="font-size:14px">On-brand</span><br>"Hi Ada, your order is on its way and should arrive by 4pm. Track it here."</div>
    </div>
    <p class="g-sub">Write down 3 words for how you sound. Use them on every message.</p>"""))
    tps = ["Website", "WhatsApp", "Invoices", "Signboard", "Instagram", "Email signature", "Packaging", "Proposals"]
    chips = "".join(f'<div class="chip-ui" style="position:static;justify-content:center;font-size:25px">{x}</div>' for x in tps)
    s[5] = page(t, 5, T, "vivid", centred(f"""
    {num(4, "Consistency")}
    <h2 class="g-hl" style="margin-top:30px;font-size:78px">Same look. Same voice.<br><span class="boxword"><b>Every</b>{cursor()}</span> <span class="acc">touchpoint.</span></h2>
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-top:56px">{chips}</div>
    <p class="g-sub">When everything matches, people trust you before they've met you.</p>"""))
    s[6] = page(t, 6, T, "light", centred(f"""
    {kicker("Your turn")}
    <h2 class="g-hl" style="margin-top:28px;font-size:86px">Is your brand<br><span class="boxword"><b>consistent?</b>{cursor("light")}</span></h2>
    <p class="g-sub" style="font-size:30px">We build brand systems: positioning, visuals, voice and guidelines, so every touchpoint looks like it came from the same business.</p>
    <div style="margin-top:56px;display:flex;flex-direction:column;gap:20px;align-items:flex-start">
      <div class="g-pill"><span>Book a free call with EAGLESCROFT</span><span class="ic i-arrow-right" style="font-size:28px"></span></div>
      <div class="g-pill"><span>eaglescroft.com.ng</span><span class="ic i-globe" style="font-size:28px"></span></div>
    </div>""") + STAR.format(s="right:140px;top:320px;width:46px;height:46px"))
    return s


# ---------------------------------------------------------------- Mon 16 · UX fixes
@post("020-ux-fixes", "Ground School · 5 small UX fixes")
def ux(t):
    T = 7
    s = {}
    s[1] = page(t, 1, T, "vivid", centred(f"""
    {kicker("Ground School · UI/UX design")}
    <h1 class="g-hl" style="margin-top:28px;font-size:86px"><b>5 small UX fixes</b><br>that make your website<br><span class="boxword"><b>easier</b>{cursor()}</span> <span class="acc">to buy from.</span></h1>
    <p class="g-sub" style="font-size:30px">Customers rarely leave because they dislike you. They leave because something felt like hard work.</p>
    <div style="height:240px"></div>""") +
        '<div class="chip-ui" style="left:96px;top:1000px;transform:rotate(-3deg)"><span class="ic i-mouse-pointer-2"></span>One clear button</div>'
        '<div class="chip-ui" style="left:420px;top:1060px;transform:rotate(2deg)"><span class="ic i-list-checks"></span>Shorter forms</div>'
        '<div class="chip-ui" style="left:700px;top:980px;transform:rotate(-1deg)"><span class="ic i-eye"></span>Readable text</div>'
        + STAR.format(s="right:120px;top:150px;width:46px;height:46px"))
    fixes = [
        ("light", "One main button.<br><b class=\"acc\">Make it look like one.</b>", "Fix 1 · buttons",
         '<span class="mock-link">Learn more</span><span class="mock-link">Details</span><span class="mock-link">Contact</span><span class="mock-link">Info</span>',
         '<span class="mock-btn pri">Book a free call</span><p style="margin:16px 0 0;font-size:19px;color:#5A6685">or <u>see our work</u></p>',
         "Four equal links compete. One clear button wins."),
        ("vivid", "Ask for less.<br><span class=\"acc\">Get more sign-ups.</span>", "Fix 2 · forms",
         "".join(f'<div class="field">{x}</div>' for x in ["Title", "First name", "Middle name", "Surname", "Company", "Job title", "Address", "Phone", "Email", "How did you hear…"]),
         "".join(f'<div class="field">{x}</div>' for x in ["Your name", "WhatsApp number", "What do you need?"]) + '<span class="mock-btn pri" style="margin-top:8px">Send</span>',
         "Every extra field is one more reason to give up."),
        ("light", "Text people can<br><b class=\"acc\">actually read.</b>", "Fix 3 · readability",
         '<p style="font-size:18px;color:#A3A9B6;line-height:1.3">We are a leading provider of innovative solutions across multiple verticals delivering value to stakeholders through synergy and best-in-class excellence in all we do every day.</p>',
         '<p style="font-size:30px;font-weight:700;margin:0;color:#0B1530">Websites that win you customers.</p><p style="font-size:22px;color:#48526E;line-height:1.5;margin:12px 0 0">Fast, clear and built for phones. Live in weeks.</p>',
         "Bigger text, stronger contrast, shorter lines."),
        ("vivid", "Buttons made<br><span class=\"acc\">for thumbs.</span>", "Fix 4 · tap targets",
         '<div style="display:flex;gap:4px;flex-wrap:wrap">' + "".join(f'<span style="font-size:16px;border:1px solid #CBD2E0;padding:4px 7px">{x}</span>' for x in ["Home", "About", "Services", "Work", "Blog", "FAQ", "Contact", "Call"]) + '</div>',
         '<div style="display:grid;gap:14px">' + "".join(f'<span class="mock-btn" style="border:2px solid #2F6BFF;color:#1D4ED8;text-align:center">{x}</span>' for x in ["Services", "Our work"]) + '<span class="mock-btn pri" style="text-align:center">WhatsApp us</span></div>',
         "Big enough to hit first time, with space between them."),
        ("light", "Show people<br><b class=\"acc\">where they are.</b>", "Fix 5 · progress",
         '<p style="font-size:26px;margin:0">Submitting…</p><p style="font-size:21px;margin:16px 0 0">(no message, no progress, no idea if it worked)</p>',
         '<p style="font-size:20px;font-family:var(--font-mono);letter-spacing:.12em;color:#2F6BFF;margin:0">STEP 2 OF 3</p><div style="height:16px;border-radius:99px;background:#E6EEFF;margin-top:10px"><div style="width:66%;height:100%;border-radius:99px;background:#2F6BFF"></div></div><p style="font-size:27px;margin:28px 0 0;font-weight:700;color:#15803D">✓ Received! We reply within 24 hours.</p>',
         "Steps, loading states and clear confirmations calm people down."),
    ]
    for i, (tone, hl, lab, before, after, note) in enumerate(fixes):
        s[i + 2] = page(t, i + 2, T, tone, centred(f"""
    {num(i + 1, lab.split(" · ")[1])}
    <h2 class="g-hl" style="margin-top:30px;font-size:76px">{hl}</h2>
    <div class="ba"><div class="bf"><div class="tag-ba"><span class="ic i-x-circle"></span>Before</div>{before}</div><div class="af"><div class="tag-ba"><span class="ic i-circle-check"></span>After</div>{after}</div></div>
    <p class="g-sub">{note}</p>"""))
    s[7] = page(t, 7, T, "vivid", centred(f"""
    {kicker("The rule")}
    <h2 class="g-hl" style="margin-top:28px;font-size:84px">Good design feels<br><span class="boxword"><b>invisible.</b>{cursor()}</span><br><span class="acc">Bad design feels like work.</span></h2>
    <div style="margin-top:56px;display:flex;flex-direction:column;gap:20px;align-items:flex-start">
      <div class="g-pill"><span>Want a UX review of your site or app?</span><span class="ic i-arrow-right" style="font-size:28px"></span></div>
      <div class="g-pill"><span>eaglescroft.com.ng</span><span class="ic i-globe" style="font-size:28px"></span></div>
    </div>""") + STAR.format(s="right:140px;top:200px;width:46px;height:46px"))
    return s


# ---------------------------------------------------------------- Tue 17 · five videos
@post("021-five-videos", "Ground School · 5 videos every business should have")
def five_videos(t):
    T = 7
    s = {}
    s[1] = page(t, 1, T, "vivid", centred(f"""
    {kicker("Ground School · video & motion")}
    <h1 class="g-hl" style="margin-top:28px;font-size:92px"><b>5 videos</b><br>every business<br>should <span class="boxword"><b>have.</b>{cursor()}</span></h1>
    <p class="g-sub" style="font-size:30px">If customers can't see what you do in 30 seconds, they'll find someone who shows them.</p>
    <div style="height:260px"></div>""") +
        '<div class="tile-g" style="right:130px;top:820px;transform:rotate(-8deg);width:180px;height:180px;border-radius:48px"><span class="ic i-play" style="font-size:80px"></span></div>'
        '<div class="chip-ui" style="left:96px;top:1010px;transform:rotate(-3deg)"><span class="ic i-clapperboard"></span>Brand film</div>'
        '<div class="chip-ui" style="left:360px;top:1070px;transform:rotate(2deg)"><span class="ic i-film"></span>Reels</div>'
        '<div class="chip-ui" style="left:560px;top:990px;transform:rotate(-1deg)"><span class="ic i-captions"></span>Captions on</div>'
        + STAR.format(s="right:120px;top:150px;width:46px;height:46px"))
    vids = [
        ("light", "Brand film", "Who you are and why you exist.", "60–90s", "Website hero · LinkedIn · pitches", "16/9", "Abuja to the world."),
        ("vivid", "Demo", "Your product or service in action, start to finish.", "30–60s", "Website · sales chats · ads", "16/9", "How it works"),
        ("light", "Customer story", "Real results, in the customer's own words (with permission).", "45–90s", "Website · LinkedIn · proposals", "16/9", "In their own words."),
        ("vivid", "Explainer", "How it works, step by step. Motion graphics shine here.", "45–75s", "Website · onboarding · YouTube", "16/9", "Step 1 of 3"),
        ("light", "Short-form reels", "Weekly, captioned, made for the scroll: tips, behind the scenes, results.", "15–35s", "TikTok · Reels · Shorts · Status", "9/16", "Stop scrolling."),
    ]
    for i, (tone, name, what, length, where, ratio, cap) in enumerate(vids):
        w = "100%" if ratio == "16/9" else "420px"
        s[i + 2] = page(t, i + 2, T, tone, centred(f"""
    {num(i + 1, "Video")}
    <h2 class="g-hl" style="margin-top:30px;font-size:86px"><b class="acc">{name}</b></h2>
    <p class="g-sub" style="font-size:32px;margin-top:18px">{what}</p>
    <div class="vframe" style="margin-top:40px;aspect-ratio:{ratio};width:{w};{'max-height:520px;' if ratio == '9/16' else ''}"><span class="len">{length}</span><span class="playb"><span class="ic i-play"></span></span><span class="cap">{cap}</span></div>
    <div class="g-card" style="margin-top:30px"><div class="lbl"><span class="ic i-send"></span>Where it works</div><p>{where}</p></div>"""))
    s[7] = page(t, 7, T, "vivid", centred(f"""
    {kicker("Start this month")}
    <h2 class="g-hl" style="margin-top:28px;font-size:84px">One a month =<br>a full <span class="boxword"><b>video library</b>{cursor()}</span><br><span class="acc">by mid-year.</span></h2>
    <p class="g-sub" style="font-size:30px">We script, shoot, edit and animate.</p>
    <div style="margin-top:56px;display:flex;flex-direction:column;gap:20px;align-items:flex-start">
      <div class="g-pill"><span>Need video that sells? Book a free call</span><span class="ic i-arrow-right" style="font-size:28px"></span></div>
      <div class="g-pill"><span>eaglescroft.com.ng</span><span class="ic i-globe" style="font-size:28px"></span></div>
    </div>""") + STAR.format(s="right:140px;top:200px;width:46px;height:46px"))
    return s


def main():
    render = "--render" in sys.argv
    only = [a for a in sys.argv[1:] if not a.startswith("--")]
    for folder, (title, fn) in POSTS.items():
        if only and not any(o in folder for o in only):
            continue
        d = HERE / folder
        d.mkdir(exist_ok=True)
        for n, html in fn(title).items():
            f = d / f"slide-{n}.html"
            f.write_text(html)
            if render:
                subprocess.run([str(ROOT / "design" / "render.sh"), str(f)], check=True, capture_output=True)
        print(folder, len(fn(title)), "slides")


if __name__ == "__main__":
    main()
