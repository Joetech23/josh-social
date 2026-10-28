"""Write the six slide HTML files for Joshua's Wed 28 Oct carousel (AI for academics).

    python3 design/personal/w44-wed-academics/build.py && for i in 1 2 3 4 5 6; do
      design/render.sh design/personal/w44-wed-academics/slide-$i.html; done
"""
import pathlib

HERE = pathlib.Path(__file__).parent
N = 6

HEAD = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<base href="../../../">
<meta name="es-size" content="1080x1350">
<title>Joshua · Wed · AI for academics · {n}</title>
<link rel="stylesheet" href="design/templates/shared.css">
<link rel="stylesheet" href="design/icons/icons.css">
<link rel="stylesheet" href="design/templates/notebook.css">
<link rel="stylesheet" href="design/templates/devices.css">
<link rel="stylesheet" href="design/personal/w44-wed-academics/academics.css">
</head>
<body>
<div class="canvas notebook">
"""

SIG = """  <div class="sig small">
    <div class="who"><div class="av"><img src="design/personal/photos/joshua-avatar.jpg" alt=""></div><div><b>Joshua Obaje</b><small>Founder &amp; CTO, EAGLESCROFT</small></div></div>
    <span class="page-n mono" style="font-size:16px;letter-spacing:.18em;color:var(--faint)">{n} / {N}{arrow}</span>
  </div>
</div>
</body>
</html>
"""


def tool(logo, name):
    return f'<span class="tool"><span class="lt"><img src="design/logos/{logo}.svg" alt=""></span>{name}</span>'


def prompt(text):
    return f'<div class="prompt"><span class="mono"><span class="ic i-copy"></span>Copy this prompt</span><p>{text}</p></div>'


SLIDES = {}

SLIDES[1] = """  <div class="eyebrow">AI for academics</div>
  <div class="page">
    <h1 class="hl" style="font-size:64px;margin:0"><span class="thin">AI won’t write your thesis.</span><span class="heavy">It can make you a<br><span class="mark-u">faster researcher.</span></span></h1>
    <p class="lead" style="margin-top:24px;max-width:540px;font-size:27px">A literature review workflow for students and lecturers, without cheating.</p>
  </div>
  <div class="disc" style="position:absolute;right:-110px;bottom:-170px;width:740px;height:740px;border-radius:50%;background:radial-gradient(60% 60% at 35% 30%,#3B82F6 0%,#1D4ED8 55%,#001E60 100%)"></div>
  <img src="design/personal/photos/joshua-cutout.png" alt="" style="position:absolute;right:-60px;bottom:0;width:660px;z-index:2;filter:drop-shadow(0 20px 30px rgba(0,10,34,.35))">
  <div class="logo-tile" style="position:absolute;right:440px;top:600px;width:132px;height:132px;transform:rotate(-8deg);z-index:3"><img src="design/logos/googlescholar.svg" alt="Google Scholar"></div>
  <div class="logo-tile" style="position:absolute;right:60px;top:560px;width:118px;height:118px;transform:rotate(7deg);z-index:3"><img src="design/logos/semanticscholar.svg" alt="Semantic Scholar"></div>
  <div class="note" style="position:absolute;left:130px;top:700px;width:330px;padding:18px 24px;transform:rotate(-3deg);z-index:3"><h3 style="font-size:25px;margin:0;display:flex;gap:10px;align-items:center"><span class="ic i-search" style="color:var(--accent)"></span>Find</h3></div>
  <div class="note" style="position:absolute;left:170px;top:810px;width:330px;padding:18px 24px;transform:rotate(2deg);z-index:3"><h3 style="font-size:25px;margin:0;display:flex;gap:10px;align-items:center"><span class="ic i-book-open" style="color:var(--accent)"></span>Skim</h3></div>
  <div class="note" style="position:absolute;left:125px;top:920px;width:330px;padding:18px 24px;transform:rotate(-1.5deg);z-index:3"><h3 style="font-size:25px;margin:0;display:flex;gap:10px;align-items:center"><span class="ic i-badge-check" style="color:var(--accent)"></span>Check</h3></div>
  <div class="note" style="position:absolute;left:180px;top:1030px;width:330px;padding:18px 24px;transform:rotate(2.5deg);z-index:3"><h3 style="font-size:25px;margin:0;display:flex;gap:10px;align-items:center"><span class="ic i-pen-line" style="color:var(--accent)"></span>Write, then disclose</h3></div>
"""

SLIDES[2] = f"""  <div class="eyebrow">Step one · Find</div>
  <div class="page">
    <div class="step-no">01</div>
    <h2 class="hl"><span class="heavy">Find <span class="mark-u">real papers,</span></span><span class="thin">faster.</span></h2>
    <p class="lead" style="margin-top:20px;max-width:800px">Ask in plain language. Research search tools only return published work.</p>
    <div class="search" style="margin-top:34px"><span class="ic i-search"></span>Does mobile money help small businesses grow in Africa?</div>
    <div class="res" style="margin-top:16px">
      <div style="display:flex;gap:10px"><span class="tag"><span class="ic i-badge-check"></span>Peer-reviewed</span><span class="tag" style="color:var(--navy);background:#EEF2FB">Link to the paper</span></div>
      <div class="skel b" style="width:78%"></div><div class="skel" style="width:92%"></div><div class="skel" style="width:60%"></div>
    </div>
    <div class="tools"><span class="lbl">Try</span>{tool("googlescholar", "Google Scholar")}{tool("semanticscholar", "Semantic Scholar")}<span class="tool txt">Consensus</span></div>
    {prompt("Find peer-reviewed studies on [my topic] from the last 10 years. Give title, authors, year and a link for each.")}
  </div>
"""

SLIDES[3] = f"""  <div class="eyebrow">Step two · Skim</div>
  <div class="page">
    <div class="step-no">02</div>
    <h2 class="hl"><span class="heavy">Summarise first.</span><span class="thin">Then <span class="mark-u">read properly.</span></span></h2>
    <div style="display:grid;grid-template-columns:330px 1fr;gap:34px;align-items:center;margin-top:30px">
      <div style="position:relative;height:300px">
        <div class="note" style="position:absolute;left:24px;top:24px;width:270px;height:290px;padding:28px;transform:rotate(5deg)"></div>
        <div class="note" style="position:absolute;left:12px;top:10px;width:270px;height:290px;padding:28px;transform:rotate(-2deg)"></div>
        <div class="note" style="position:absolute;left:0;top:0;width:270px;height:290px;padding:30px 28px;transform:rotate(-6deg);display:grid;gap:14px;align-content:start">
          <div class="skel b" style="width:80%;height:18px"></div><div class="skel" style="width:100%"></div><div class="skel" style="width:94%"></div><div class="skel" style="width:98%"></div><div class="skel" style="width:70%"></div><div class="skel" style="width:90%"></div>
          <span class="hand" style="font-size:34px;color:var(--accent);font-weight:700;margin-top:4px">12 papers…</span>
        </div>
      </div>
      <div>
        <div class="arrow"><span class="ic i-wand-sparkles"></span>AI gives you a map</div>
        <div class="card" style="margin-top:12px;padding:26px 28px;font-size:24px;line-height:1.6;color:var(--ink)">
          <b style="font-family:var(--font-display);color:var(--navy);font-size:26px">For each paper</b><br>
          • The question it asks<br>• Method and sample<br>• Main finding<br>• Limitations
        </div>
        <p class="hand" style="font-size:36px;color:var(--navy);margin:10px 0 0;font-weight:700;line-height:1.1">→ then read the best 3 in full</p>
      </div>
    </div>
    <div class="tools"><span class="lbl">Try</span>{tool("notebooklm", "NotebookLM")}{tool("claude", "Claude")}{tool("googlegemini", "Gemini")}</div>
    <style>.prompt{{margin-top:30px}} .tools{{margin-top:22px}}</style>
    {prompt("Summarise this paper in 5 bullets: research question, method, sample, main finding, limitations. Quote the page for each.")}
  </div>
"""

SLIDES[4] = f"""  <div class="eyebrow">Step three · Check</div>
  <div class="page">
    <div class="step-no">03</div>
    <h2 class="hl"><span class="thin">AI invents references.</span><span class="heavy"><span class="mark-u">Check every one.</span></span></h2>
    <div class="cite fake" style="margin-top:46px;transform:rotate(-1deg)"><span class="txt">Author, A. (2021). A title that sounds exactly right. <i>Journal of Real-Sounding Studies</i>, 4(2), 11–29.</span>
      <span class="stamp bad" style="right:26px;bottom:-26px">doesn’t exist</span></div>
    <div class="note" style="margin-top:58px;padding:34px 38px">
      <h3 style="font-size:30px">Before it goes in your references:</h3>
      <ul class="ticklist">
        <li><span class="ic i-search"></span><div>Search the exact title<small>Does the paper really exist?</small></div></li>
        <li><span class="ic i-eye"></span><div>Open it and find the claim<small>Does it actually say what AI said it says?</small></div></li>
        <li><span class="ic i-badge-check"></span><div>Save only what you verified<small>in a reference manager, so it formats itself</small></div></li>
      </ul>
    </div>
    <div class="tools"><span class="lbl">Save with</span>{tool("zotero", "Zotero")}{tool("mendeley", "Mendeley")}</div>
  </div>
"""

SLIDES[5] = f"""  <div class="eyebrow">Step four · Write</div>
  <div class="page">
    <div class="step-no">04</div>
    <h2 class="hl"><span class="heavy">Your words.</span><span class="heavy"><span class="mark-u">Your argument.</span></span></h2>
    <p class="lead" style="margin-top:20px;max-width:800px">Use AI as a strict examiner of your draft, not as its author.</p>
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:24px;margin-top:34px">
      <div class="note" style="padding:30px 32px;transform:rotate(-1.5deg)"><h3 style="font-size:28px">Fine</h3><ul class="ticklist">
        <li><span class="ic i-circle-check"></span>Finding papers</li><li><span class="ic i-circle-check"></span>Summaries to plan your reading</li><li><span class="ic i-circle-check"></span>Critique of your draft</li></ul></div>
      <div class="note" style="padding:30px 32px;transform:rotate(1.5deg)"><h3 style="font-size:28px">Not yours any more</h3><ul class="ticklist">
        <li class="no"><span class="ic i-x-circle"></span>Citations you didn’t check</li><li class="no"><span class="ic i-x-circle"></span>Paragraphs it wrote for you</li><li class="no"><span class="ic i-x-circle"></span>An argument you can’t defend</li></ul></div>
    </div>
    {prompt("Here is my literature review draft. Act as a strict examiner. Where is my argument weak, and what is missing? Do not rewrite it.")}
  </div>
"""

SLIDES[6] = f"""  <div class="eyebrow">Step five · Disclose</div>
  <div class="page" style="top:250px">
    <div class="step-no">05</div>
    <h2 class="hl" style="font-size:66px"><span class="thin">Be open about</span><span class="heavy"><span class="mark-u">how you used AI.</span></span></h2>
    <p class="lead" style="margin-top:24px;font-size:28px;max-width:800px">Check your institution’s AI policy, then add one honest line to your methods or acknowledgements.</p>
    <div class="cite" style="margin-top:30px;font-size:24px;transform:rotate(-1deg)"><span class="hand" style="font-size:30px;color:var(--accent);font-weight:700;display:block;margin-bottom:6px;font-family:Caveat,cursive">for example</span>AI tools were used to search for literature and to summarise papers. All sources were read and verified by the author, and all analysis and writing are the author’s own.</div>
    <div class="note" style="margin-top:70px;width:820px;padding:32px 38px;transform:rotate(-1.5deg);display:flex;gap:22px;align-items:center">
      <div class="logo-tile" style="width:110px;height:110px;flex:none;color:var(--accent)"><span class="ic i-graduation-cap" style="font-size:60px"></span></div>
      <div><h3 style="margin:0;font-size:34px">Academics: what rules is your department setting?</h3><p style="margin:8px 0 0;font-size:24px;color:var(--body);font-weight:500">Tell me in the comments. Save this for your next supervision meeting.</p></div>
    </div>
  </div>
"""

for n, body in SLIDES.items():
    if n == 1:  # the cover photo sits where the signature goes
        body = body + '  <style>.sig.small{display:none}</style>\n'
    html = HEAD.format(n=n) + body + SIG.format(n=n, N=N, arrow=" →" if n < N else "")
    (HERE / f"slide-{n}.html").write_text(html)
print(f"{len(SLIDES)} slides written")
