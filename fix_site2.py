#!/usr/bin/env python3
"""VITROSCAPE round 2 — font, cursor, progress track, lightbox, landing polish."""

def apply(path, pairs, label):
    with open(path, 'r', encoding='utf-8') as f:
        s = f.read()
    for i, (old, new, cnt) in enumerate(pairs):
        n = s.count(old)
        assert n == cnt, f'{label} patch #{i}: expected {cnt}, got {n}\n---OLD---\n{old[:200]}'
        s = s.replace(old, new)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(s)
    print(f'{label}: {len(pairs)} patches applied')

# ── @font-face block (latin-ext first with unicode-range, latin as default) ──
FONTS = ''
for w in (300, 400, 500, 700):
    FONTS += (
        f"    @font-face {{ font-family: 'Space Grotesk'; font-style: normal; font-weight: {w}; font-display: swap;\n"
        f"      unicode-range: U+0100-024F, U+1E00-1EFF, U+2020, U+20A0-20AB;\n"
        f"      src: url('assets/fonts/space-grotesk-latin-ext-{w}.woff2') format('woff2'); }}\n"
        f"    @font-face {{ font-family: 'Space Grotesk'; font-style: normal; font-weight: {w}; font-display: swap;\n"
        f"      src: url('assets/fonts/space-grotesk-latin-{w}.woff2') format('woff2'); }}\n"
    )

NEW_CSS = '''
    /* ══ CUSTOM CURSOR ══ */
    #cursor-dot, #cursor-ring {
      position: fixed;
      top: 0; left: 0;
      border-radius: 50%;
      pointer-events: none;
      z-index: 3000;
      opacity: 0;
      transition: opacity 0.3s ease;
      mix-blend-mode: difference;
    }
    #cursor-dot { width: 6px; height: 6px; background: #fff; }
    #cursor-ring {
      width: 32px; height: 32px;
      border: 1px solid rgba(255,255,255,0.75);
      transition: opacity 0.3s ease, width 0.28s ease, height 0.28s ease,
                  background-color 0.28s ease;
    }
    #cursor-ring.hovering {
      width: 54px; height: 54px;
      background: rgba(255,255,255,0.14);
    }
    html.has-cursor, html.has-cursor * { cursor: none !important; }
    html.has-cursor:has(#lightbox.lb-open), html.has-cursor:has(#lightbox.lb-open) * { cursor: auto !important; }
    html.has-cursor:has(#lightbox.lb-open) #cursor-dot,
    html.has-cursor:has(#lightbox.lb-open) #cursor-ring { display: none; }
    @media (hover: none), (pointer: coarse) {
      #cursor-dot, #cursor-ring { display: none; }
    }

    /* ══ LANDING ENTRANCE ══ */
    .s1-tagline, .s1-subtitle {
      opacity: 0;
      transform: translateY(18px);
      transition: opacity 1s ease, transform 1.1s cubic-bezier(0.22, 1, 0.36, 1);
    }
    body.site-ready .s1-tagline { opacity: 1; transform: none; transition-delay: 0.15s; }
    body.site-ready .s1-subtitle { opacity: 1; transform: none; transition-delay: 0.4s; }

    /* ══ INTRO CONTACT ══ */
    #s-intro-contact {
      margin-top: 44px;
      font-size: 11px;
      letter-spacing: 0.24em;
      text-transform: uppercase;
      color: #999;
    }

    /* ══ LIGHTBOX PROJECT LINK ══ */
    #lb-link {
      display: inline-block;
      margin-top: 16px;
      padding: 9px 22px;
      border: 1px solid rgba(255,255,255,0.28);
      border-radius: 24px;
      color: #eee;
      font-size: 11px;
      letter-spacing: 0.18em;
      text-transform: uppercase;
      text-decoration: none;
      transition: background 0.25s ease;
    }
    #lb-link:hover { background: rgba(255,255,255,0.14); }

    @media (prefers-reduced-motion: reduce) {
      body::after { animation: none; }
      #scroll-cue { animation: none; }
      .s1-tagline, .s1-subtitle { transition: none; opacity: 1; transform: none; }
    }

    /* ══ MOBILE / SMALL SCREEN ══ */'''

index_patches = [

# ── 1. fonts + base font stack ──
("""    *, *::before, *::after { margin: 0; padding: 0; box-sizing: border-box; }

    html, body {
      width: 100%; height: 100%;
      overflow: hidden;
      background: #fff;
      font-family: 'Calibri', 'Calibri Light', sans-serif;""",
FONTS + """
    *, *::before, *::after { margin: 0; padding: 0; box-sizing: border-box; }

    html, body {
      width: 100%; height: 100%;
      overflow: hidden;
      background: #fff;
      font-family: 'Space Grotesk', 'Calibri', 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', sans-serif;""", 1),

# ── 2. film grain overlay ──
("""    canvas { display: block; }""",
"""    canvas { display: block; }

    /* ══ FILM GRAIN OVERLAY ══ */
    body::after {
      content: '';
      position: fixed;
      inset: -50%;
      z-index: 250;
      pointer-events: none;
      opacity: 0.04;
      background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='240' height='240'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='2' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)' opacity='0.5'/%3E%3C/svg%3E");
      animation: grain-shift 0.9s steps(4) infinite;
    }
    @keyframes grain-shift {
      0% { transform: translate(0, 0); }
      25% { transform: translate(-2%, 1.4%); }
      50% { transform: translate(1.6%, -1%); }
      75% { transform: translate(-1%, -1.8%); }
      100% { transform: translate(0, 0); }
    }""", 1),

# ── 3. replace dots CSS with continuous track CSS ──
("""    /* ══ SCROLL PROGRESS ══ */
    #scroll-progress {
      position: fixed;
      right: 18px;
      top: 50%;
      transform: translateY(-50%);
      z-index: 150;
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 10px;
      pointer-events: none;
    }
    .sp-dot {
      width: 5px;
      height: 5px;
      border-radius: 50%;
      background: #ccc;
      background-clip: content-box;   /* padding = bigger hit area, dot stays 5px */
      padding: 6px;
      transition: all 0.35s ease;
      opacity: 0.4;
      pointer-events: auto;
      cursor: pointer;
    }
    .sp-dot.active {
      background: #111;
      opacity: 1;
      transform: scale(1.6);
    }
    .sp-dot:hover { opacity: 0.9; transform: scale(1.35); }
    @media (max-width: 768px) {
      #scroll-progress { right: 10px; gap: 7px; }
      .sp-dot { width: 4px; height: 4px; }
    }""",
"""    /* ══ SCROLL PROGRESS — continuous track ══ */
    #progress-track {
      position: fixed;
      right: 22px;
      top: 50%;
      transform: translateY(-50%);
      height: 200px;
      width: 24px;
      z-index: 150;
      cursor: pointer;
    }
    #pt-line {
      position: absolute;
      left: 50%;
      top: 0; bottom: 0;
      width: 1px;
      background: #dcdcdc;
    }
    .pt-tick {
      position: absolute;
      left: 50%;
      width: 5px; height: 5px;
      margin: -2.5px 0 0 -2.5px;
      border-radius: 50%;
      background: #c2c2c2;
      transition: all 0.3s ease;
      pointer-events: none;
    }
    .pt-tick.active { background: #111; transform: scale(1.5); }
    #pt-thumb {
      position: absolute;
      left: 50%;
      top: 0%;
      width: 9px; height: 9px;
      margin: -4.5px 0 0 -4.5px;
      border-radius: 50%;
      background: #111;
      box-shadow: 0 0 0 5px rgba(0,0,0,0.05);
      pointer-events: none;
    }
    @media (max-width: 768px) {
      #progress-track { right: 10px; height: 130px; width: 20px; }
    }""", 1),

# ── 4. insert cursor/entrance/contact/link CSS before mobile block ──
("""    /* ══ MOBILE / SMALL SCREEN ══ */""", NEW_CSS, 1),

# ── 5. drop remaining Calibri overrides (loader + kali panel inherit site font) ──
("""      font-family: 'Calibri', sans-serif;
""", '', 2),
("""      font-family: 'Calibri', 'Calibri Light', sans-serif;
      color: #ccc; font-size: 10px; user-select: none;""",
"""      color: #ccc; font-size: 10px; user-select: none;""", 1),

# ── 6. intro contact element ──
("""  <div id="s-intro-body">
    <div class="s-intro-text" id="s-intro-text"></div>
  </div>""",
"""  <div id="s-intro-body">
    <div class="s-intro-text" id="s-intro-text"></div>
    <p id="s-intro-contact"></p>
  </div>""", 1),
("""  document.getElementById('s-intro-text').innerHTML  = d.sIntroText.split('\\n\\n').map(p => `<p>${p}</p>`).join('')""",
"""  document.getElementById('s-intro-text').innerHTML  = d.sIntroText.split('\\n\\n').map(p => `<p>${p}</p>`).join('')
  document.getElementById('s-intro-contact').textContent = d.s1contact""", 1),

# ── 7. bigger lightbox + centered link ──
("""    #lb-inner {
      max-width: 88vw; max-height: 84vh;
      transform: scale(0.05); opacity: 0;""",
"""    #lb-inner {
      max-width: 92vw; max-height: 88vh;
      text-align: center;
      transform: scale(0.05); opacity: 0;""", 1),
("""      max-width: 88vw; max-height: 84vh;
      width: auto; height: auto;""",
"""      max-width: 92vw; max-height: 88vh;
      width: auto; height: auto;""", 1),

# ── 8. lightbox: hi-res large image + optional project link ──
("""    } else {
      const img = document.createElement('img')
      img.src = proj.src
      lbInner.appendChild(img)
    }

    lbOpenIdx = idx""",
"""    } else {
      const img = document.createElement('img')
      img.src = proj.src.replace('assets/images/web/', 'assets/images/large/')
      lbInner.appendChild(img)
    }

    if (proj.link) {
      const a = document.createElement('a')
      a.id = 'lb-link'
      a.href = 'Immersion_Rupestre/' + (currentLang === 'zh' ? 'cn' : currentLang) + '/'
      a.target = '_blank'
      a.rel = 'noopener'
      a.textContent = { zh: '进入项目页面 ↗', fr: 'Voir le projet ↗', en: 'Enter project ↗' }[currentLang]
      lbInner.appendChild(a)
    }

    lbOpenIdx = idx""", 1),

# ── 9. flag Continental Shelf card with link to the (former) island page ──
("""src:'assets/images/web/Standing_at_the_Center_of_the_Continental_Shelf.webp' },""",
"""src:'assets/images/web/Standing_at_the_Center_of_the_Continental_Shelf.webp', link:true },""", 1),

# ── 10. continuous progress thumb in animate() ──
("""  // Update scroll progress dots
  const dots = document.querySelectorAll('.sp-dot')
  let activeSec = 0
  if (dp < PAGE_H * 0.5) activeSec = 0
  else if (dp < PAGE_H * 1.5) activeSec = 1
  else if (dp < PAGE_H * 2.5) activeSec = 2
  else activeSec = 3
  dots.forEach((d, i) => d.classList.toggle('active', i === activeSec))""",
"""  // Continuous scroll progress (sliding thumb + section ticks)
  ptThumbEl.style.top = (dp / TOTAL * 100) + '%'
  let activeSec = 0
  if (dp < PAGE_H * 0.5) activeSec = 0
  else if (dp < PAGE_H * 1.5) activeSec = 1
  else if (dp < PAGE_H * 2.5) activeSec = 2
  else activeSec = 3
  ptTickEls.forEach((d, i) => d.classList.toggle('active', i === activeSec))""", 1),

# ── 11. track click + custom cursor JS ──
("""// Progress dots: click to jump to a section
document.querySelectorAll('.sp-dot').forEach(dot => {
  dot.addEventListener('click', () => {
    const sec = +dot.dataset.sec
    const dpNow = ((lerpScroll % TOTAL) + TOTAL) % TOTAL
    rawScroll += (((sec * PAGE_H + PAGE_H * 0.1) - dpNow) % TOTAL + TOTAL) % TOTAL
  })
})""",
"""// Progress track: continuous thumb + click-to-jump
const ptThumbEl = document.getElementById('pt-thumb')
const ptTickEls = document.querySelectorAll('.pt-tick')
document.getElementById('progress-track').addEventListener('click', e => {
  const r = e.currentTarget.getBoundingClientRect()
  const frac = Math.min(1, Math.max(0, (e.clientY - r.top) / r.height))
  const dpNow = ((lerpScroll % TOTAL) + TOTAL) % TOTAL
  rawScroll += ((frac * TOTAL - dpNow) % TOTAL + TOTAL) % TOTAL
})

// Custom cursor: instant dot + inertial ring, difference blend works on any bg
if (window.matchMedia('(hover: hover) and (pointer: fine)').matches) {
  document.documentElement.classList.add('has-cursor')
  const cursorDot  = document.getElementById('cursor-dot')
  const cursorRing = document.getElementById('cursor-ring')
  let curX = innerWidth / 2, curY = innerHeight / 2, ringX = curX, ringY = curY
  window.addEventListener('mousemove', e => {
    curX = e.clientX; curY = e.clientY
    cursorDot.style.opacity  = '1'
    cursorRing.style.opacity = '1'
    cursorDot.style.transform = `translate(${curX}px, ${curY}px) translate(-50%, -50%)`
    const hov = e.target.closest && e.target.closest(
      'button, a, input, #progress-track, #scroll-cue, #helix-canvas'
    )
    cursorRing.classList.toggle('hovering', !!hov)
  }, { passive: true })
  document.addEventListener('mouseleave', () => {
    cursorDot.style.opacity  = '0'
    cursorRing.style.opacity = '0'
  })
  ;(function cursorLoop() {
    ringX += (curX - ringX) * 0.16
    ringY += (curY - ringY) * 0.16
    cursorRing.style.transform = `translate(${ringX}px, ${ringY}px) translate(-50%, -50%)`
    requestAnimationFrame(cursorLoop)
  })()
}""", 1),

# ── 12. loader completion → trigger landing entrance ──
("""        setTimeout(() => loaderEl.remove(), 900)""",
"""        setTimeout(() => { loaderEl.remove(); document.body.classList.add('site-ready') }, 900)""", 1),

# ── 13. progress track + cursor HTML ──
("""<!-- ══ SCROLL PROGRESS ══ -->
<div id="scroll-progress">
  <div class="sp-dot active" data-sec="0"></div>
  <div class="sp-dot" data-sec="1"></div>
  <div class="sp-dot" data-sec="2"></div>
  <div class="sp-dot" data-sec="3"></div>
</div>""",
"""<!-- ══ SCROLL PROGRESS — continuous track ══ -->
<div id="progress-track">
  <div id="pt-line"></div>
  <div class="pt-tick active" style="top: 0%"></div>
  <div class="pt-tick" style="top: 33.333%"></div>
  <div class="pt-tick" style="top: 66.666%"></div>
  <div class="pt-tick" style="top: 100%"></div>
  <div id="pt-thumb"></div>
</div>
<!-- ══ CUSTOM CURSOR ══ -->
<div id="cursor-dot"></div>
<div id="cursor-ring"></div>""", 1),
]

apply('index.html', index_patches, 'index.html')
print('Round 2 patches OK.')
