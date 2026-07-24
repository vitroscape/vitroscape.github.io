#!/usr/bin/env python3
"""VITROSCAPE website improvements script"""
import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# ── 1. Add SEO meta tags after <title> ──
seo_block = '''  <meta name="description" content="VITROSCAPE — Immersive Hybrid Realities Studio. A creative studio dedicated to pushing the boundaries of imagination through VR, AR, AI generation, and interactive projection.">
  <meta name="keywords" content="VITROSCAPE, immersive experience, VR, AR, AI, interactive projection, digital art, Le Fresnoy">
  <meta name="author" content="VITROSCAPE">
  <meta name="theme-color" content="#ffffff">
  <!-- Open Graph -->
  <meta property="og:title" content="VITROSCAPE — Immersive Hybrid Realities Studio">
  <meta property="og:description" content="A creative studio pushing the boundaries of imagination through cutting-edge technology.">
  <meta property="og:type" content="website">
  <meta property="og:url" content="https://vitroscape.com">
  <meta property="og:site_name" content="VITROSCAPE">
  <!-- Twitter Card -->
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="VITROSCAPE — Immersive Hybrid Realities Studio">
  <meta name="twitter:description" content="A creative studio pushing the boundaries of imagination through cutting-edge technology.">
  <!-- Favicon -->
  <link rel="icon" type="image/svg+xml" href="assets/svg/VITROSCAPE_vector.svg">'''

html = html.replace('  <title>VITROSCAPE</title>', '  <title>VITROSCAPE</title>\n' + seo_block)

# ── 2. Replace loader CSS ──
old_loader_css = '''    /* ══ LOADER ══ */
    #loader {
      position: fixed;
      inset: 0;
      z-index: 2000;
      background: #fff;
      display: flex;
      align-items: center;
      justify-content: center;
      transition: opacity 0.8s ease;
    }
    #loader.done { opacity: 0; pointer-events: none; }
    #loader-num {
      font-family: 'Calibri', sans-serif;
      font-size: 23px;
      font-weight: 400;
      color: #aaa;
      letter-spacing: 0.08em;
      min-width: 3ch;
      text-align: center;
    }'''

new_loader_css = '''    /* ══ LOADER ══ */
    #loader {
      position: fixed;
      inset: 0;
      z-index: 2000;
      background: #fff;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      transition: opacity 0.8s ease;
    }
    #loader.done { opacity: 0; pointer-events: none; }
    .loader-brand {
      font-family: 'Calibri', sans-serif;
      font-size: 13px;
      font-weight: 400;
      letter-spacing: 0.35em;
      color: #111;
      text-transform: uppercase;
      margin-bottom: 24px;
      overflow: hidden;
    }
    .loader-brand span {
      display: inline-block;
      opacity: 0;
      transform: translateY(12px);
      animation: loader-letter-in 0.5s ease forwards;
    }
    @keyframes loader-letter-in {
      to { opacity: 1; transform: translateY(0); }
    }
    .loader-bar-wrap {
      width: 120px;
      height: 1px;
      background: #e0e0e0;
      border-radius: 1px;
      overflow: hidden;
      position: relative;
    }
    .loader-bar {
      position: absolute;
      left: 0; top: 0; bottom: 0;
      width: 0%;
      background: #111;
      border-radius: 1px;
      transition: width 0.3s ease;
    }
    .loader-pct {
      font-family: 'Calibri', sans-serif;
      font-size: 10px;
      font-weight: 400;
      letter-spacing: 0.15em;
      color: #aaa;
      margin-top: 12px;
      min-width: 3ch;
      text-align: center;
      font-variant-numeric: tabular-nums;
    }'''

html = html.replace(old_loader_css, new_loader_css)

# ── 3. Replace loader HTML ──
old_loader_html = '<!-- \u2550\u2550 LOADER \u2550\u2550 -->\n<div id="loader"><span id="loader-num">0</span></div>'
new_loader_html = '''<!-- \u2550\u2550 LOADER \u2550\u2550 -->
<div id="loader">
  <div class="loader-brand" id="loader-brand"></div>
  <div class="loader-bar-wrap"><div class="loader-bar" id="loader-bar"></div></div>
  <div class="loader-pct" id="loader-pct">0</div>
</div>'''
html = html.replace(old_loader_html, new_loader_html)

# ── 4. Add scroll progress indicator CSS ──
progress_css = '''    /* ══ SCROLL PROGRESS ══ */
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
      transition: all 0.35s ease;
      opacity: 0.4;
    }
    .sp-dot.active {
      background: #111;
      opacity: 1;
      transform: scale(1.6);
    }
    @media (max-width: 768px) {
      #scroll-progress { right: 10px; gap: 7px; }
      .sp-dot { width: 4px; height: 4px; }
    }'''

# Insert before mobile media query
html = html.replace('    /* \u2550\u2550 MOBILE', progress_css + '\n\n    /* \u2550\u2550 MOBILE')

# ── 5. Add keyboard nav hint CSS ──
keyboard_css = '''    /* ══ KEYBOARD HINT ══ */
    #kb-hint {
      position: fixed;
      bottom: 14px;
      right: 18px;
      z-index: 150;
      font-size: 9px;
      letter-spacing: 0.12em;
      color: #bbb;
      opacity: 0;
      transition: opacity 0.6s ease;
      pointer-events: none;
      text-transform: uppercase;
    }
    #kb-hint.show { opacity: 1; }
    @media (max-width: 768px) { #kb-hint { display: none; } }'''

html = html.replace('    /* \u2550\u2550 MOBILE', keyboard_css + '\n\n    /* \u2550\u2550 MOBILE')

# ── 6. Add scroll progress HTML before closing body ──
progress_html = '''<!-- \u2550\u2550 SCROLL PROGRESS ══ -->
<div id="scroll-progress">
  <div class="sp-dot active" data-sec="0"></div>
  <div class="sp-dot" data-sec="1"></div>
  <div class="sp-dot" data-sec="2"></div>
  <div class="sp-dot" data-sec="3"></div>
</div>
<!-- ══ KEYBOARD HINT ══ -->
<div id="kb-hint">\u2191 \u2193 navigate &middot; space play</div>
'''

# Insert before </body>
html = html.replace('</body>', progress_html + '</body>')

# ── 7. Replace loader JS logic ──
old_loader_js = ''';(function () {
  const loaderEl = document.getElementById('loader')
  const numEl    = document.getElementById('loader-num')

  // Resources to preload: all project images + SVG logo
  const imageUrls = PROJECTS
    .map(p => p.src)
    .filter(s => s && !s.endsWith('.mp4'))

  const total   = imageUrls.length + 1   // +1 for SVG
  let   loaded  = 0
  let   display = 0   // smoothly animated number

  function tick(actual) {
    // Animate display number toward actual
    const step = () => {
      display += (actual - display) * 0.12 + 0.3
      if (display >= actual) display = actual
      numEl.textContent = Math.floor(display)
      if (display < actual) requestAnimationFrame(step)
    }
    requestAnimationFrame(step)
  }

  function onLoad() {
    loaded++
    const pct = Math.round(loaded / total * 100)
    tick(pct)
    if (loaded >= total) {
      tick(100)
      setTimeout(() => {
        loaderEl.classList.add('done')
        setTimeout(() => loaderEl.remove(), 900)
      }, 300)
    }
  }

  // Preload images
  imageUrls.forEach(url => {
    const img = new Image()
    img.onload = img.onerror = onLoad
    img.src = url
  })

  // SVG counts as one resource — resolved when logoLoaded flag is set
  const svgCheck = setInterval(() => {
    if (logoLoaded) { clearInterval(svgCheck); onLoad() }
  }, 50)
})()'''

new_loader_js = ''';(function () {
  const loaderEl   = document.getElementById('loader')
  const brandEl    = document.getElementById('loader-brand')
  const barEl      = document.getElementById('loader-bar')
  const pctEl      = document.getElementById('loader-pct')

  // Build letter animation: V I T R O S C A P E
  const letters = 'VITROSCAPE'.split('')
  brandEl.innerHTML = letters.map((ch, i) =>
    `<span style="animation-delay:${0.1 + i * 0.07}s">${ch}</span>`
  ).join('')

  // Resources to preload: all project images + SVG logo
  const imageUrls = PROJECTS
    .map(p => p.src)
    .filter(s => s && !s.endsWith('.mp4'))

  const total   = imageUrls.length + 1   // +1 for SVG
  let   loaded  = 0

  function updateLoader(pct) {
    barEl.style.width = pct + '%'
    pctEl.textContent = Math.round(pct)
  }

  function onLoad() {
    loaded++
    const pct = Math.min(100, Math.round(loaded / total * 100))
    updateLoader(pct)
    if (loaded >= total) {
      updateLoader(100)
      setTimeout(() => {
        loaderEl.classList.add('done')
        setTimeout(() => loaderEl.remove(), 900)
      }, 400)
    }
  }

  // Preload images
  imageUrls.forEach(url => {
    const img = new Image()
    img.onload = img.onerror = onLoad
    img.src = url
  })

  // SVG counts as one resource — resolved when logoLoaded flag is set
  const svgCheck = setInterval(() => {
    if (logoLoaded) { clearInterval(svgCheck); onLoad() }
  }, 50)
})()'''

html = html.replace(old_loader_js, new_loader_js)

# ── 8. Add keyboard navigation + progress update in animate() ──
# Find the animate() function and inject progress update + keyboard listener
# First, add keyboard event listener before the animate() function
old_before_animate = '''// \u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\n//  INIT\n// \u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\nrenderText(currentLang)\nresize()\nanimate()'''

new_before_animate = '''// \u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\n//  KEYBOARD NAVIGATION\n// \u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\nconst kbHintEl = document.getElementById('kb-hint')
let kbHintTimer = null
function showKbHint() {
  kbHintEl.classList.add('show')
  clearTimeout(kbHintTimer)
  kbHintTimer = setTimeout(() => kbHintEl.classList.remove('show'), 3000)
}
window.addEventListener('keydown', e => {
  if (e.key === 'ArrowDown' || e.key === 'ArrowRight' || e.key === 'PageDown') {
    e.preventDefault()
    rawScroll += PAGE_H * 0.35
    showKbHint()
  } else if (e.key === 'ArrowUp' || e.key === 'ArrowLeft' || e.key === 'PageUp') {
    e.preventDefault()
    rawScroll -= PAGE_H * 0.35
    showKbHint()
  } else if (e.key === ' ' || e.key === 'Enter') {
    e.preventDefault()
    const idx = Math.round(lerpCard)
    const proj = PROJECTS[idx]
    if (proj && proj.zh.title !== '' && !isLightboxOpen) {
      // Trigger ripple + lightbox on current card
      if (!proj._ripple) {
        proj._ripple = { t: 0, cx: 0, cy: 0, onDone: () => {
          const event = new Event('click')
          helixCanvas.dispatchEvent(event)
        }}
      }
    }
    showKbHint()
  } else if (e.key === 'Escape') {
    const lbEl = document.getElementById('lightbox')
    if (lbEl.classList.contains('lb-open')) lbEl.click()
  }
})

// Show keyboard hint briefly on first wheel
window.addEventListener('wheel', () => { showKbHint() }, { once: true })

// \u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\n//  INIT\n// \u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\nrenderText(currentLang)\nresize()\nanimate()'''

html = html.replace(old_before_animate, new_before_animate)

# ── 9. Add scroll progress update inside animate() ──
# Find a good spot inside animate() to add progress indicator update
old_anim_section = '''  // Position sections
  const s1Yt = sectionY(0, dp)
  s1El.style.transform       = `translateY(${s1Yt}px)`
  logoCanvas.style.transform  = `translateY(${s1Yt}px)`
  sIntroEl.style.transform   = `translateY(${sectionY(1, dp)}px)`
  s2El.style.transform       = `translateY(${sectionY(2, dp)}px)`
  s3El.style.transform       = `translateY(${sectionY(3, dp)}px)`'''

new_anim_section = '''  // Position sections
  const s1Yt = sectionY(0, dp)
  s1El.style.transform       = `translateY(${s1Yt}px)`
  logoCanvas.style.transform  = `translateY(${s1Yt}px)`
  sIntroEl.style.transform   = `translateY(${sectionY(1, dp)}px)`
  s2El.style.transform       = `translateY(${sectionY(2, dp)}px)`
  s3El.style.transform       = `translateY(${sectionY(3, dp)}px)`

  // Update scroll progress dots
  const dots = document.querySelectorAll('.sp-dot')
  let activeSec = 0
  if (dp < PAGE_H * 0.5) activeSec = 0
  else if (dp < PAGE_H * 1.5) activeSec = 1
  else if (dp < PAGE_H * 2.5) activeSec = 2
  else activeSec = 3
  dots.forEach((d, i) => d.classList.toggle('active', i === activeSec))'''

html = html.replace(old_anim_section, new_anim_section)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print('Done! index.html updated.')
