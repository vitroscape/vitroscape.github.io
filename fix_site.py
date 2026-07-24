#!/usr/bin/env python3
"""VITROSCAPE — targeted bug fixes + UX upgrades. Each replacement asserts exactly 1 match."""
import sys

def apply(path, pairs):
    with open(path, 'r', encoding='utf-8') as f:
        s = f.read()
    for i, (old, new) in enumerate(pairs):
        n = s.count(old)
        assert n == 1, f'{path} patch #{i}: expected 1 match, got {n}\n---OLD---\n{old[:200]}'
        s = s.replace(old, new)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(s)
    print(f'{path}: {len(pairs)} patches applied')

SEP = '// ' + '═' * 51

index_patches = [

# ── 1. og:url + og:image ──
('''  <meta property="og:url" content="https://vitroscape.com">
  <meta property="og:site_name" content="VITROSCAPE">''',
'''  <meta property="og:url" content="https://www.vitroscape.com">
  <meta property="og:site_name" content="VITROSCAPE">
  <meta property="og:image" content="https://www.vitroscape.com/assets/images/Desert_Star__insitu_3.jpg">'''),

# ── 2. twitter:image ──
('''  <meta name="twitter:description" content="A creative studio pushing the boundaries of imagination through cutting-edge technology.">''',
'''  <meta name="twitter:description" content="A creative studio pushing the boundaries of imagination through cutting-edge technology.">
  <meta name="twitter:image" content="https://www.vitroscape.com/assets/images/Desert_Star__insitu_3.jpg">'''),

# ── 3. section panel: hidden by default, fades via JS ──
('''    #section-panel {
      position: fixed;
      left: 44px;
      top: 44px;
      max-width: 320px;
      z-index: 5;
      pointer-events: none;
      text-align: left;
    }''',
'''    #section-panel {
      position: fixed;
      left: 44px;
      top: 44px;
      max-width: 320px;
      z-index: 5;
      pointer-events: none;
      text-align: left;
      opacity: 0;               /* hidden on landing/intro; animate() drives this */
      transition: opacity 0.45s ease;
    }'''),

# ── 4. progress dots: clickable, larger hit area ──
('''    .sp-dot {
      width: 5px;
      height: 5px;
      border-radius: 50%;
      background: #ccc;
      transition: all 0.35s ease;
      opacity: 0.4;
    }''',
'''    .sp-dot {
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
    }'''),

('''    .sp-dot.active {
      background: #111;
      opacity: 1;
      transform: scale(1.6);
    }''',
'''    .sp-dot.active {
      background: #111;
      opacity: 1;
      transform: scale(1.6);
    }
    .sp-dot:hover { opacity: 0.9; transform: scale(1.35); }'''),

# ── 5. dead CSS/JS/HTML: #loader-num, #counter ──
('''      #loader-num { font-size: 18px; }
''', ''),
('''    #counter { display: none; }
''', ''),
('''
<div id="counter"></div>
''', ''),
('''const cntEl        = document.getElementById('counter')
''', ''),

# ── 6. section split: S2 = cards 0–8, S3 = cards 9–11 (12/13 are invisible helix spacers) ──
('''const S2_COUNT = 11''', '''const S2_COUNT = 9'''),
('''// Panel switches to S3 content starting from card index 7 (Jeu de Mondes)
const PANEL_S3_FROM = 7''',
'''// Panel switches to S3 content starting from card index 9 (Temporary Soul: Λ-7)
const PANEL_S3_FROM = 9'''),

# ── 7. PAGE_H / TOTAL recomputed on resize ──
('''const PAGE_H = window.innerHeight
const TOTAL  = 4 * PAGE_H   // S1 + S-intro + S2 works + S3 works''',
'''let PAGE_H = window.innerHeight
let TOTAL  = 4 * PAGE_H   // S1 + S-intro + S2 works + S3 works'''),
('''function resize() {
  const s1 = document.getElementById('s1')''',
'''function resize() {
  PAGE_H = window.innerHeight
  TOTAL  = 4 * PAGE_H
  const s1 = document.getElementById('s1')'''),

# ── 8. shared state: lightbox flag declared early + openCard hook + panel dirty flag ──
('''let rawScroll  = 0
let lerpScroll = 0
let lerpCard    = -0.7  // = targetCard(0), correct initial helix position
let shownIdx   = -1''',
'''let rawScroll  = 0
let lerpScroll = 0
let lerpCard    = -0.7  // = targetCard(0), correct initial helix position
let shownIdx   = -1
let isLightboxOpen = false   // when true: helix videos stay paused, scroll input ignored
let openCard = null          // set by lightbox module: ripple → lightbox for a card index
let _panelWasVis = false'''),
('''let isLightboxOpen = false   // when true: all helix videos stay paused
''', ''),

# ── 9. ignore scroll/touch while lightbox is open ──
('''window.addEventListener('wheel', e => {
  e.preventDefault()
  const dpNow = ((lerpScroll % TOTAL) + TOTAL) % TOTAL''',
'''window.addEventListener('wheel', e => {
  if (isLightboxOpen) return
  e.preventDefault()
  const dpNow = ((lerpScroll % TOTAL) + TOTAL) % TOTAL'''),
('''window.addEventListener('touchmove', e => {
  e.preventDefault()
  rawScroll += (t0 - e.touches[0].clientY) * 1.8''',
'''window.addEventListener('touchmove', e => {
  if (isLightboxOpen) return
  e.preventDefault()
  rawScroll += (t0 - e.touches[0].clientY) * 1.8'''),

# ── 10. section panel visibility driven by scroll position ──
('''  showInfo(lerpCard)
  updateSectionPanel(Math.round(lerpCard))''',
'''  showInfo(lerpCard)
  updateSectionPanel(Math.round(lerpCard))

  // Section panel only while browsing works sections (never on landing / intro)
  const panelVis = dp > PAGE_H * 1.9 && dp < TOTAL - PAGE_H * 0.5
  if (panelVis !== _panelWasVis) {
    _panelWasVis = panelVis
    panelEl.style.opacity = panelVis ? '1' : '0'
  }'''),

# ── 11. hero logo: subtle mouse parallax on top of scroll rotation ──
('''  if (logoLoaded) {
    const rotTarget = rotT * Math.PI * LOGO.rotRange * LOGO.rotDir
    logoGroup.rotation.y += (rotTarget - logoGroup.rotation.y) * LOGO.rotSmooth
  }''',
'''  if (logoLoaded) {
    mouseX += (mouseTargetX - mouseX) * 0.04
    mouseY += (mouseTargetY - mouseY) * 0.04
    const rotTarget = rotT * Math.PI * LOGO.rotRange * LOGO.rotDir + mouseX * 0.10
    logoGroup.rotation.y += (rotTarget - logoGroup.rotation.y) * LOGO.rotSmooth
    logoGroup.rotation.x += (mouseY * 0.06 - logoGroup.rotation.x) * LOGO.rotSmooth
  }'''),

# ── 12. keyboard navigation + mouse tracking (was lost: improve_site.py patch #8 never matched) ──
('''renderText(currentLang)
resize()
animate()''',
SEP + '''
//  KEYBOARD NAVIGATION + MOUSE PARALLAX
''' + SEP + '''
let mouseX = 0, mouseY = 0, mouseTargetX = 0, mouseTargetY = 0
window.addEventListener('mousemove', e => {
  mouseTargetX = (e.clientX / window.innerWidth) * 2 - 1
  mouseTargetY = (e.clientY / window.innerHeight) * 2 - 1
}, { passive: true })

const kbHintEl = document.getElementById('kb-hint')
let kbHintTimer = null
function showKbHint() {
  if (!kbHintEl) return
  kbHintEl.classList.add('show')
  clearTimeout(kbHintTimer)
  kbHintTimer = setTimeout(() => kbHintEl.classList.remove('show'), 3200)
}
window.addEventListener('wheel', () => showKbHint(), { once: true })

window.addEventListener('keydown', e => {
  if (e.key === 'ArrowDown' || e.key === 'ArrowRight' || e.key === 'PageDown') {
    if (isLightboxOpen) return
    e.preventDefault(); rawScroll += PAGE_H * 0.35; showKbHint()
  } else if (e.key === 'ArrowUp' || e.key === 'ArrowLeft' || e.key === 'PageUp') {
    if (isLightboxOpen) return
    e.preventDefault(); rawScroll -= PAGE_H * 0.35; showKbHint()
  } else if (e.key === ' ' || e.key === 'Enter') {
    if (isLightboxOpen || !openCard) return
    const dpNow = ((lerpScroll % TOTAL) + TOTAL) % TOTAL
    if (dpNow < PAGE_H * 1.9) return
    e.preventDefault(); openCard(Math.round(lerpCard)); showKbHint()
  } else if (e.key === 'Escape') {
    const lbEl = document.getElementById('lightbox')
    if (lbEl.classList.contains('lb-open')) lbEl.click()
  }
})

// Progress dots: click to jump to a section
document.querySelectorAll('.sp-dot').forEach(dot => {
  dot.addEventListener('click', () => {
    const sec = +dot.dataset.sec
    const dpNow = ((lerpScroll % TOTAL) + TOTAL) % TOTAL
    rawScroll += (((sec * PAGE_H + PAGE_H * 0.1) - dpNow) % TOTAL + TOTAL) % TOTAL
  })
})

''' + SEP + '''
//  INIT
''' + SEP + '''
renderText(currentLang)
resize()
animate()'''),

# ── 13. lightbox: expose openCard for keyboard use ──
('''  // Click backdrop → close
  lbEl.addEventListener('click', closeLightbox)''',
'''  // Keyboard access: same ripple → lightbox flow as a canvas click
  openCard = idx => {
    const proj = PROJECTS[idx]
    if (!proj || proj.zh.title === '' || lbOpenIdx !== -1 || proj._ripple) return
    snapRawScrollToCard(idx)
    proj._ripple = { t: 0, cx: 0, cy: 0,
      onDone: () => openLightbox(proj, idx, innerWidth / 2, innerHeight / 2) }
  }

  // Click backdrop → close
  lbEl.addEventListener('click', closeLightbox)'''),

# ── 14. vendor three.js locally (drop unpkg CDN dependency) ──
('''    "three": "https://unpkg.com/three@0.160.0/build/three.module.js",
    "three/addons/": "https://unpkg.com/three@0.160.0/examples/jsm/"''',
'''    "three": "./assets/vendor/three.module.js",
    "three/addons/": "./assets/vendor/addons/"'''),
]

server_patches = [
('''const PORT = 3000''',
'''const argv = Object.fromEntries(
  process.argv.slice(2).filter(a => a.startsWith('--')).map(a => a.slice(2).split('='))
const PORT = Number(process.env.PORT || argv.port || 3000)
const HOST = argv.host || process.env.HOST || '127.0.0.1' '''),
('''}).listen(PORT, '127.0.0.1', () => {''',
'''}).listen(PORT, HOST, () => {'''),
('''  '.mp4':  'video/mp4',
  '.webm': 'video/webm',
}''',
'''  '.mp4':  'video/mp4',
  '.webm': 'video/webm',
  '.webp': 'image/webp',
  '.ico':  'image/x-icon',
  '.woff2': 'font/woff2',
}'''),
]

apply('index.html', index_patches)
apply('server.js', server_patches)
print('All patches OK.')
