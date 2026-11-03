"""Joshua · Tue 3 Nov · AI for traders: "5 WhatsApp messages AI can write for you" (Blue Glass).

    python3 design/personal/w45-tue-traders-whatsapp/build.py && for i in 1 2 3 4 5 6 7; do
      design/render.sh design/personal/w45-tue-traders-whatsapp/slide-$i.html; done
"""
import pathlib

HERE = pathlib.Path(__file__).parent
N = 7

HEAD = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<base href="../../../">
<meta name="es-size" content="1080x1350">
<title>Joshua · Tue 3 Nov · AI for traders · {n}</title>
<link rel="stylesheet" href="design/templates/shared.css">
<link rel="stylesheet" href="design/icons/icons.css">
<link rel="stylesheet" href="design/templates/glass.css">
</head>
<body>
<div class="canvas glass {tone}">
"""

FOOT = """  <div class="g-brand"><div><b>JOSHUA</b> <span>OBAJE</span></div><span class="pg">{n} / {N}</span></div>
</div>
</body>
</html>
"""

SPARK = '<svg class="spark" style="{s}" viewBox="0 0 24 24"><path d="M12 0c.9 6.2 5.1 10.6 12 12-6.9 1.4-11.1 5.8-12 12-.9-6.2-5.1-10.6-12-12C6.9 10.6 11.1 6.2 12 0z"/></svg>'
CURSOR = '<svg class="cur" viewBox="0 0 24 24"><path d="M4 3l16 7-7 2-3 7z" fill="#fff" stroke="#1D4ED8" stroke-width="1.6" stroke-linejoin="round"/></svg>'
CURSOR_DARK = '<svg class="cur" viewBox="0 0 24 24"><path d="M4 3l16 7-7 2-3 7z" fill="#2F6BFF" stroke="#fff" stroke-width="1.6" stroke-linejoin="round"/></svg>'
WA_HEAD = ('<div class="hd"><div class="av"><img src="design/logos/whatsapp.svg" alt=""></div>'
           '<div><b>Ade Stores</b><small>business account</small></div></div>')


def bubbles(tone):
    if tone == "vivid":
        return ('<div class="bubble-bg" style="width:420px;height:420px;left:-160px;top:-140px"></div>'
                '<div class="bubble-bg" style="width:300px;height:300px;right:-110px;bottom:180px"></div>')
    return ('<div class="bubble-bg" style="width:360px;height:360px;right:-150px;top:-120px"></div>'
            '<div class="bubble-bg" style="width:260px;height:260px;left:-120px;bottom:240px"></div>')


def chat(msgs):
    out = []
    for kind, text, time in msgs:
        tick = ' <span class="tick">✓✓</span>' if kind == "out" else ""
        out.append(f'<div class="m {kind}">{text}<span class="t">{time}{tick}</span></div>')
    return f'<div class="wa">{WA_HEAD}<div class="body">{"".join(out)}</div></div>'


def prompt(text):
    return f'<div class="g-card" style="margin-top:40px"><div class="lbl"><span class="ic i-copy"></span>Copy this prompt</div><p>{text}</p></div>'


def step(n, tone, kicker, headline, msgs, prompt_text):
    return (HEAD.format(n=n, tone=tone) + bubbles(tone) +
            '  <div style="position:absolute;left:96px;right:96px;top:110px;bottom:170px;display:flex;flex-direction:column;justify-content:center">\n'
            f'  <div class="g-num"><b>0{n - 1}</b>{kicker}</div>\n'
            f'  <h2 class="g-hl" style="font-size:78px;margin-top:34px">{headline}</h2>\n'
            f'  <div style="margin-top:56px">{chat(msgs)}</div>\n'
            f'  {prompt(prompt_text)}\n'
            '  </div>\n'
            + FOOT.format(n=n, N=N))


SLIDES = {}

SLIDES[1] = HEAD.format(n=1, tone="vivid") + bubbles("vivid") + f"""
  <div class="g-kicker" style="margin-top:20px">AI for traders</div>
  <h1 class="g-hl" style="margin-top:28px;font-size:88px"><b>5 WhatsApp</b><br><b>messages</b> AI can<br>write for you <span class="boxword"><b>today.</b>{CURSOR}</span></h1>
  <p class="g-sub" style="max-width:600px">For shops, market traders and online sellers. Copy the prompts. Free AI apps are enough.</p>
  <div class="tile-g white" style="right:110px;top:640px;transform:rotate(8deg);width:170px;height:170px;border-radius:44px"><img src="design/logos/whatsapp.svg" alt="WhatsApp"></div>
  <div class="chip-ui" style="left:96px;top:860px;transform:rotate(-3deg)"><span class="ic i-tag"></span>Price list</div>
  <div class="chip-ui" style="left:330px;top:940px;transform:rotate(2deg)"><span class="ic i-truck"></span>Delivery</div>
  <div class="chip-ui" style="left:600px;top:830px;transform:rotate(-2deg)"><span class="ic i-message-circle"></span>“Last price?”</div>
  <div class="chip-ui" style="left:150px;top:1020px;transform:rotate(1.5deg)"><span class="ic i-heart-handshake"></span>Thank you</div>
  <div class="chip-ui" style="left:600px;top:990px;transform:rotate(-1deg)"><span class="ic i-bell-ring"></span>New stock</div>
  {SPARK.format(s="right:330px;top:600px;width:54px;height:54px")}
  {SPARK.format(s="right:90px;top:880px;width:30px;height:30px")}
  {SPARK.format(s="left:860px;top:150px;width:36px;height:36px")}
""" + FOOT.format(n=1, N=N)

SLIDES[2] = step(2, "light", "Price list", 'Your <b class="acc">price list</b>,<br>sorted in seconds.',
                 [("out", "🛒 <b>Ade Stores · Today’s prices</b>\nRice (50kg): ₦72,000\nBeans (paint): ₦6,500\nGarri (bag): ₦38,000\nVeg oil (25L): ₦58,000\n📦 To order: send item + quantity", "9:02 AM")],
                 "Turn my price list into a neat WhatsApp message for customers. Group the items, show prices in naira, and end with how to order. <i>(Paste the list or snap a photo of it.)</i>")

SLIDES[3] = step(3, "vivid", "Delivery", 'Explain <b class="acc">delivery</b><br>once. Reuse forever.',
                 [("in", "Do you deliver to Ikeja?", "11:40 AM"),
                  ("out", "🚚 <b>Delivery</b>\nLagos (Island &amp; Mainland): ₦3,000, same day\nOutside Lagos: ₦6,000, 2–3 days\n✅ Pay on delivery or by transfer\nSend your address to book 👇", "11:41 AM")],
                 "Write a short WhatsApp message about my delivery: areas, fees, timing and payment options. Friendly and clear.")

SLIDES[4] = step(4, "light", "“Last price?”", 'Answer <b class="acc">“last price?”</b><br>without losing money.',
                 [("in", "Last price?", "2:15 PM"),
                  ("out", "Our price is already our best, so you get quality you can trust 🙏 Buy today and I’ll add free delivery 🚚", "2:16 PM")],
                 "A customer asked “last price?”. Write a polite reply that keeps my price but offers free delivery if they buy today.")

SLIDES[5] = step(5, "vivid", "Thank you", 'Say thank you,<br>and get <b class="acc">a review.</b>',
                 [("out", "Thank you for buying from Ade Stores! 🙏 We hope you love it. Could you send a quick photo or a one-line review? It really helps us grow 💚", "6:05 PM"),
                  ("in", "Love it! Sending pictures now 😍", "6:12 PM")],
                 "Write a warm thank-you message for a customer who just bought [item], asking for a quick photo or a one-line review.")

SLIDES[6] = step(6, "light", "New stock", 'New stock?<br>Make them <b class="acc">want it.</b>',
                 [("out", "🔥 <b>New stock just landed!</b>\nAnkara fabric (6 yards): ₦15,000\nOnly 20 pieces. First come, first served.\nReply YES to reserve yours 👇", "8:30 AM")],
                 "Write a WhatsApp broadcast for new stock: [items + prices]. Create urgency without sounding desperate. 5 lines max.")

SLIDES[7] = HEAD.format(n=7, tone="vivid") + bubbles("vivid") + f"""
  <div class="g-kicker" style="margin-top:120px">Your turn</div>
  <h2 class="g-hl" style="margin-top:28px;font-size:84px">Let AI do<br>the <span class="boxword"><b>typing.</b>{CURSOR}</span><br><span class="acc">You do the selling.</span></h2>
  <p class="g-sub" style="max-width:780px">Works with the free versions of ChatGPT, Gemini or Claude. Always check prices and names before you send.</p>
  <div style="margin-top:70px;display:flex;flex-direction:column;gap:22px;align-items:flex-start">
    <div class="g-pill"><span>Save this for later</span><span class="ic i-sparkle" style="font-size:30px"></span></div>
    <div class="g-pill"><span>Send it to a trader you know</span><span class="ic i-send" style="font-size:28px"></span></div>
  </div>
  <div class="tile-g" style="right:110px;top:820px;transform:rotate(-8deg)"><span class="ic i-message-circle"></span></div>
  {SPARK.format(s="right:120px;top:300px;width:48px;height:48px")}
  {SPARK.format(s="right:260px;top:1010px;width:28px;height:28px")}
  <div class="chip-ui" style="left:96px;top:1090px">Follow for daily AI, made simple</div>
""" + FOOT.format(n=7, N=N)

for n, html in SLIDES.items():
    (HERE / f"slide-{n}.html").write_text(html)
print(f"{len(SLIDES)} slides written")
