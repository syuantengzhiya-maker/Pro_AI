#!/usr/bin/env python3
"""Run in the same folder as index.html:  python patch.py
Makes index.html.bak first. If any anchor text is missing, nothing is written."""
import sys, shutil

SRC = "index.html"
html = open(SRC, encoding="utf-8").read()

CSS = '''
/* ===== v16 upgrades ===== */
.skip{position:absolute;left:-999px;top:8px;z-index:500;background:var(--sun);padding:8px 14px;border:2px solid var(--ink);border-radius:10px;font-weight:700;text-decoration:none}
.skip:focus{left:12px}
.tour{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin:0 0 28px}
.tour span{font:700 .85rem var(--mono);letter-spacing:.06em;margin-right:4px}
.tour a{padding:6px 14px;border:1.5px solid var(--ink);border-radius:99px;background:#fff;font-weight:600;font-size:.88rem;text-decoration:none;box-shadow:3px 3px 0 var(--ink);transition:transform .2s}
.tour a:hover{background:var(--sun);transform:translate(-2px,-2px)}
@media(max-width:720px){.tour{flex-wrap:nowrap;overflow-x:auto;padding:0 4px 10px}.tour a,.tour span{white-space:nowrap;flex:none}}
.mc{margin-top:16px;padding-top:14px;border-top:1.5px dashed var(--ink)}
.mc .bar i{background:var(--mint);opacity:.4}
.tldr{background:#fff3c4;border:1.5px dashed var(--ink);border-radius:10px;padding:8px 12px;margin:0 0 10px}
.rai{margin:12px 0 0;padding-left:18px}.rai li{margin:6px 0}
.road{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:14px;margin-top:26px}
.road div{background:#ffffff1f;border:1.5px solid #ffffff66;border-radius:14px;padding:14px 16px;font-size:.95rem}
.road b{display:block;font:700 .78rem var(--mono);letter-spacing:.1em;color:var(--sun);margin-bottom:4px}
.moments{grid-template-columns:repeat(auto-fit,minmax(min(520px,100%),1fr))}
@media(max-width:430px){.mcard.fb iframe{zoom:.62}}
</style>'''

HEAD = '''<meta property="og:type" content="website">
<meta property="og:title" content="Syuan — I build things you can break and understand">
<meta property="og:description" content="Student builder from Kuching. AI for education, physics simulators and games. Try a real ML model live.">
<meta property="og:image" content="https://pro-ai-33j2.onrender.com/photos/avatar.jpg">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#fff7ec">
<link rel="icon" href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><text y=%22.9em%22 font-size=%2290%22>⭐</text></svg>">
<link rel="preconnect" href="https://fonts.googleapis.com">'''

TOUR = '''<div class="tour" aria-label="Quick tour for judges"><span>⏱ 60-SECOND TOUR</span><a href="#about">Intro</a><a href="#edu">Education</a><a href="#edu">Skills</a><a href="#journey">Achievements</a><a href="#projects">Portfolio</a><a href="#ambition">Future ambition</a><a href="#ai">Responsible AI</a><a href="#ai">AI tools</a><a href="#ai">Reflection</a></div>
  <div class="nums" data-fx="rise">'''

MODEL = '''Open the full AuraStudy version</a>.</p>
      <div class="mc"><div class="tag3">// MODEL REPORT CARD</div>
        <p class="note" style="margin:0 0 6px">Expected-merit models, cross-validated. I compared Random Forest, Ridge and KNN; Ridge scored best in every stream. Higher R² is better.</p>
        <div class="bar"><i style="width:76%"></i><span><span>Art</span><span>R² 0.76 · error 4.7 · n=211</span></span></div>
        <div class="bar"><i style="width:67%"></i><span><span>Science</span><span>R² 0.67 · error 7.8 · n=99</span></span></div>
        <div class="bar"><i style="width:63%"></i><span><span>Semi Science</span><span>R² 0.63 · error 7.7 · n=91</span></span></div>
        <p class="note" style="margin-top:8px"><b>Be careful:</b> each stream has only 91 to 211 students, so treat the result as a suggestion to discuss with teachers and family, never a final decision.</p></div>'''

R = [
 ('<link rel="preconnect" href="https://fonts.googleapis.com">', HEAD),
 ('</style>', CSS),
 ('<div id="bar"></div>', '<a class="skip" href="#about">Skip to content</a>\n<div id="bar"></div>'),
 # nav: fewer links
 ('<a href="#projects">Projects</a><a href="#find">Find me</a><a href="#journey">Journey</a><a href="#activities">Activities</a><a href="#ai">AI &amp; reflection</a>',
  '<a href="#projects">Projects</a><a href="#journey">Journey</a><a href="#ambition">Future</a><a href="#ai">AI</a>'),
 ('<div class="nums" data-fx="rise">', TOUR),
 # Facebook embeds stay, but lazy-load + accessible titles
 ('<iframe src="https://www.facebook.com', '<iframe loading="lazy" title="Facebook post about my activities" src="https://www.facebook.com'),
 # explicit Future ambition section
 ('<section class="layer" style="--lb:#e8edff"><div class="wrap" data-fx="drop">',
  '<section id="ambition" class="layer" style="--lb:#e8edff"><div class="wrap" data-fx="drop"><h2>Future ambition</h2>'),
 ('I built this."</p>',
  'I built this."</p>\n    <div class="road"><div><b>NOW</b>Build and publish study tools that other Malaysian students really use.</div><div><b>NEXT</b>Study computing and AI at university, and keep learning how to teach it well.</div><div><b>GOAL</b>Teach and spread coding and AI to people around the world.</div></div>'),
 # demo: model report card + wake the API early
 ('Open the full AuraStudy version</a>.</p>', MODEL),
 ("const API='https://syuanteng315-spm-predictor.hf.space/predict';",
  "const API='https://syuanteng315-spm-predictor.hf.space/predict';\nsetTimeout(()=>{try{fetch(API.replace(/predict$/,''),{mode:'no-cors'}).catch(()=>{})}catch(e){}},1500);"),
 ("out.append(el('p','note','Asking the model…'))", "out.append(el('p','note','Asking the model… the first request can take about 20 seconds.'))"),
 # responsible AI: concrete practices
 ('and I say openly where I used it.</p></div>',
  'and I say openly where I used it.</p>'
  '<ul class="rai"><li><b>Privacy.</b> The predictor does not store your scores, and this site shares no address, IC, phone number or family details.</li>'
  '<li><b>Honest limits.</b> My model learned from only 91 to 211 students per stream, so I show its accuracy and call the result a suggestion.</li>'
  '<li><b>Checking.</b> I test every piece of code and every number AI gives me before I publish it.</li>'
  '<li><b>Credit.</b> Claude is named as my only AI tool. The ideas, choices and decisions are mine.</li></ul></div>'),
 # reflection one-liner
 ('<h4 style="margin-top:16px">Reflection</h4><p>Claude helped me a lot',
  '<h4 style="margin-top:16px">Reflection</h4><p class="tldr"><b>In one line:</b> AI is my builder\'s tool. The idea, the decisions and the checking stay with me.</p><p>Claude helped me a lot'),
 # search palette + tour links use the same jump logic
 ("['Find me online','#find'],", "['Find me online','#find'],['Future ambition','#ambition'],"),
 ("document.querySelectorAll('nav a[href^=\"#\"]')", "document.querySelectorAll('nav a[href^=\"#\"],.tour a[href^=\"#\"],a.skip')"),
]

missing = [o[:70] for o, _ in R if o not in html]
if missing:
    print("Could not find these anchors, nothing was changed:")
    for m in missing:
        print("  -", m)
    sys.exit(1)

shutil.copyfile(SRC, SRC + ".bak")
for old, new in R:
    html = html.replace(old, new)
open(SRC, "w", encoding="utf-8").write(html)
print("Done. Backup saved as index.html.bak. Open index.html to check.")
