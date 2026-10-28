"""Write the six slide HTML files for EAGLESCROFT's Wed 28 Oct carousel (AI-assisted video edit).

    python3 design/eaglescroft/w44-wed-video/build.py && for i in 1 2 3 4 5 6; do
      design/render.sh design/eaglescroft/w44-wed-video/slide-$i.html; done
"""
import math
import pathlib
import random

HERE = pathlib.Path(__file__).parent
N = 6

HEAD = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<base href="../../../">
<meta name="es-size" content="1080x1350">
<title>EAGLESCROFT · Wed · AI video workflow · {n}</title>
<link rel="stylesheet" href="design/templates/shared.css">
<link rel="stylesheet" href="design/icons/icons.css">
<link rel="stylesheet" href="design/templates/bold.css">
<link rel="stylesheet" href="design/eaglescroft/w44-wed-video/video.css">
</head>
<body>
<div class="canvas {cls}">
  <div class="topbar">
    <div class="brand"><img src="design/brand/{mark}" alt=""><span>EAGLESCROFT</span></div>
    <div class="eyebrow">{eyebrow}</div>
  </div>
"""

FOOT = """  <div class="footbar">
    <div class="site"><span class="ic i-globe"></span>eaglescroft.com.ng</div>
    <div class="socials">
      <span><span class="ic i-linkedin"></span></span>
      <span><span class="ic i-facebook"></span></span>
      <span><span class="ic i-x"></span></span>
    </div>
  </div>
</div>
</body>
</html>
"""


def head(n, eyebrow, vivid):
    cls = "vivid grid" if vivid else "paper grid on-light on-light-bar"
    mark = "eagle-white-mark.png" if vivid else "eagle-navy-mark.png"
    return HEAD.format(n=n, cls=cls, mark=mark, eyebrow=eyebrow)


def wave(count, seed, clean=True, amp=1.0, colour=None):
    rnd = random.Random(seed)
    bars = []
    for i in range(count):
        if clean:
            # speech: phrases with real pauses
            phrase = math.sin(i / 3.1) * 0.5 + 0.5
            h = 0.08 if (i // 9) % 4 == 3 else 0.25 + 0.7 * phrase * rnd.uniform(0.6, 1)
        else:
            h = 0.35 + 0.6 * rnd.random()  # hiss and hum fill every gap
        style = f"height:{max(6, int(h * 100 * amp))}%"
        if colour:
            style += f";background:{colour}"
        bars.append(f'<i style="{style}"></i>')
    return f'<div class="wave">{"".join(bars)}</div>'


def tool(logo, name):
    return f'<span class="tool"><span class="lt"><img src="design/logos/{logo}.svg" alt=""></span>{name}</span>'


def editor(style, scale_caps=True, gaps=False, playhead="58%"):
    """Generic editing window: viewer with a burnt-in caption, then caption/video/voice/music tracks."""
    vid = ('<span class="clip vid" style="width:26%"></span><span class="clip gap" style="width:7%"></span>'
           '<span class="clip vid" style="width:30%"></span><span class="clip gap" style="width:5%"></span>'
           '<span class="clip vid" style="width:28%"></span>') if gaps else \
          ('<span class="clip vid" style="width:31%"></span><span class="clip vid" style="width:36%"></span>'
           '<span class="clip vid" style="width:31%"></span>')
    caps = ('<span class="clip cap" style="width:20%">We help</span><span class="clip cap" style="width:24%">businesses</span>'
            '<span class="clip cap" style="width:16%">fly</span><span class="clip cap" style="width:22%">online.</span>')
    return f"""<div class="editor" style="{style}">
    <div class="bar"><i></i><i></i><i></i><span>brand-film_v3 · 00:00:42</span></div>
    <div class="viewer"><img src="design/personal/photos/joshua-portrait.jpg" alt=""><span class="cap">We help businesses <em>fly online.</em></span></div>
    <div class="tracks">
      <div class="track"><span class="lbl">CC</span><div class="lane">{caps}</div></div>
      <div class="track"><span class="lbl">V1</span><div class="lane">{vid}</div></div>
      <div class="track"><span class="lbl">A1</span><div class="lane">{wave(70, 7)}</div></div>
      <div class="track"><span class="lbl">A2</span><div class="lane"><span class="clip mus" style="width:100%"></span></div></div>
      <span class="playhead" style="left:calc(52px + {playhead})"></span>
    </div>
  </div>"""


SLIDES = {}

SLIDES[1] = head(1, "Ground school", True) + f"""
  <h1 class="hl"><span class="thin">Edit faster.</span><span class="heavy">Without cutting</span><span class="heavy blue">corners.</span></h1>
  <p class="lead" style="max-width:520px">The AI-assisted video workflow we use at EAGLESCROFT, step by step.</p>
  {editor("right:-60px;top:500px;width:700px;transform:rotate(-4deg)")}
  <div class="float" style="left:70px;top:690px"><span class="tile"><span class="ic i-captions"></span></span><div>Captions written<small>automatically, then checked</small></div></div>
  <div class="float" style="left:110px;top:820px"><span class="tile" style="background:var(--navy)"><span class="ic i-scissors"></span></span><div>Silences removed<small>in the rough cut</small></div></div>
  <div class="swipe" style="position:absolute;left:84px;top:960px;color:rgba(255,255,255,.75);display:flex;gap:10px;align-items:center">Swipe <span class="ic i-arrow-right"></span></div>
""" + FOOT

SLIDES[2] = head(2, "Ground school", False) + f"""
  <div class="step"><b>01</b>Script</div>
  <h2 class="hl"><span class="thin">AI drafts the script.</span><span class="heavy blue">We write the hook.</span></h2>
  <div class="card-w" style="margin-top:56px;padding:40px 42px;position:relative">
    <div style="display:flex;justify-content:space-between;align-items:center"><span class="mono" style="font-size:14px;letter-spacing:.16em;color:var(--faint)">SCRIPT · 45-SECOND BRAND FILM</span><span class="chip n" style="font-size:13px">Draft 2</span></div>
    <p style="margin:22px 0 0;font-size:25px;color:#8A93A8;text-decoration:line-through;text-decoration-thickness:3px;text-decoration-color:rgba(0,30,96,.5)">In today’s fast-paced digital world, video is more important than ever…</p>
    <p style="margin:12px 0 0;font-family:var(--font-display);font-weight:700;font-size:34px;letter-spacing:-.02em;color:var(--navy);line-height:1.2">Your customers stopped reading.<br>They watch.</p>
    <span class="mono" style="display:inline-flex;align-items:center;gap:8px;margin-top:14px;font-size:13px;letter-spacing:.14em;color:var(--accent)"><span class="ic i-pen-line"></span>REWRITTEN BY OUR TEAM</span>
    <div style="display:grid;gap:12px;margin-top:22px"><div class="skel" style="height:14px;border-radius:8px;background:#E3E9F5;width:94%"></div><div style="height:14px;border-radius:8px;background:#E3E9F5;width:88%"></div><div style="height:14px;border-radius:8px;background:#E3E9F5;width:66%"></div></div>
  </div>
  <div class="rule" style="margin-top:30px"><span class="ic i-timer"></span><div><b style="color:var(--navy)">The first 3 seconds decide if anyone keeps watching.</b> That line is always written by a person.</div></div>
  <div class="tools" style="margin-top:30px"><span class="lbl">Tools that do this</span>{tool("claude", "Claude")}{tool("googlegemini", "Gemini")}<span class="tool txt">ChatGPT</span></div>
""" + FOOT

SLIDES[3] = head(3, "Ground school", True) + f"""
  <div class="step"><b>02</b>Voice</div>
  <h2 class="hl"><span class="thin">Studio-clean voice,</span><span class="heavy blue">without the studio.</span></h2>
  <div class="card-w" style="margin-top:56px;padding:32px 34px">
    <div class="mono" style="font-size:14px;letter-spacing:.16em;color:var(--faint)">BEFORE · PHONE RECORDING</div>
    <div class="lane" style="margin-top:12px;height:130px;background:#F2F5FB;border-radius:12px">{wave(124, 3, clean=False, colour="#9AA9C8")}</div>
    <div class="mono" style="font-size:14px;letter-spacing:.16em;color:var(--accent);margin-top:22px;display:flex;align-items:center;gap:8px"><span class="ic i-wand-sparkles"></span>AFTER · AI CLEAN-UP</div>
    <div class="lane" style="margin-top:12px;height:130px;background:#EFF6FF;border-radius:12px">{wave(124, 3, colour="#2563EB")}</div>
  </div>
  <div class="rule" style="margin-top:30px"><span class="ic i-shield-check"></span><div>Background noise and room echo out, the speaker’s voice stays. <b style="color:#fff">An AI voice only with consent,</b> and only when the brief calls for it.</div></div>
  <div class="tools" style="margin-top:30px"><span class="lbl">Tools that do this</span>{tool("elevenlabs", "ElevenLabs")}<span class="tool txt">Adobe Podcast</span></div>
""" + FOOT

SLIDES[4] = head(4, "Ground school", False) + f"""
  <div class="step"><b>03</b>Rough cut</div>
  <h2 class="hl"><span class="thin">Captions and silence cuts.</span><span class="heavy blue">Done automatically.</span></h2>
  {editor("left:80px;width:760px;top:440px", gaps=True, playhead="34%")}
  <div class="float" style="right:60px;top:930px"><span class="tile"><span class="ic i-scissors"></span></span><div>Pauses and “umm”s removed<small>ready for a human pass</small></div></div>
  <div class="tools" style="position:absolute;left:80px;top:1120px"><span class="lbl">Tools that do this</span>{tool("davinciresolve", "DaVinci Resolve")}<span class="tool txt">CapCut</span><span class="tool txt">Descript</span></div>
""" + FOOT

SLIDES[5] = head(5, "Ground school", True) + """
  <div class="step"><b>04</b>Polish</div>
  <h2 class="hl"><span class="thin">AI does the heavy lifting.</span><span class="heavy blue">Taste is still human.</span></h2>
  <div style="display:grid;grid-template-columns:1fr 1fr;gap:20px;margin-top:52px">
    <div class="rule"><span class="ic i-film"></span><div><b style="color:#fff">B-roll that fits</b><br>picked for the story, not just the keyword</div></div>
    <div class="rule"><span class="ic i-sparkles"></span><div><b style="color:#fff">Motion graphics</b><br>timed to the voice, beat by beat</div></div>
    <div class="rule"><span class="ic i-wand-sparkles"></span><div><b style="color:#fff">Brand colour and type</b><br>so it looks like you in the feed</div></div>
    <div class="rule"><span class="ic i-eye"></span><div><b style="color:#fff">A final watch</b><br>with fresh eyes and sound on</div></div>
  </div>
  <div class="card-w" style="margin-top:44px;padding:26px 30px;display:flex;align-items:center;gap:22px">
    <div style="display:flex;gap:10px">
      <span style="width:62px;height:62px;border-radius:16px;background:#001E60"></span><span style="width:62px;height:62px;border-radius:16px;background:#2563EB"></span><span style="width:62px;height:62px;border-radius:16px;background:#93C5FD"></span><span style="width:62px;height:62px;border-radius:16px;background:#F4F6FB;border:1px solid #E3E9F5"></span>
    </div>
    <div style="font-size:23px;line-height:1.4;font-weight:500;color:var(--body)"><b style="color:var(--navy);font-family:var(--font-display)">Signed off by a human editor.</b><br>Every video, every time.</div>
    <span class="ic i-badge-check" style="font-size:52px;color:var(--accent);margin-left:auto"></span>
  </div>
""" + FOOT

SLIDES[6] = head(6, "Your turn", False) + """
  <h2 class="hl" style="margin-top:90px"><span class="thin">Need video that sells?</span><span class="heavy blue">We make it.</span></h2>
  <p class="lead">Brand films, product explainers and short-form content, made faster with AI and finished by people.</p>
  <div style="display:grid;gap:18px;margin-top:50px">
    <div class="rule"><b style="font-family:var(--font-mono);color:var(--accent);font-size:24px">1</b><div><b style="color:var(--navy)">Script</b> · AI drafts, we write the hook</div></div>
    <div class="rule"><b style="font-family:var(--font-mono);color:var(--accent);font-size:24px">2</b><div><b style="color:var(--navy)">Voice</b> · clean-up, AI voice only with consent</div></div>
    <div class="rule"><b style="font-family:var(--font-mono);color:var(--accent);font-size:24px">3</b><div><b style="color:var(--navy)">Rough cut</b> · captions and silence cuts</div></div>
    <div class="rule"><b style="font-family:var(--font-mono);color:var(--accent);font-size:24px">4</b><div><b style="color:var(--navy)">Polish</b> · B-roll, motion, brand, human sign-off</div></div>
  </div>
  <p style="margin-top:40px;font-family:var(--font-display);font-weight:600;font-size:34px;letter-spacing:-.02em;color:var(--navy)">Which step eats most of your time?<br><span style="color:var(--accent)">Comment 1, 2, 3 or 4.</span></p>
""" + FOOT

for n, html in SLIDES.items():
    (HERE / f"slide-{n}.html").write_text(html)
print(f"{len(SLIDES)} slides written")
