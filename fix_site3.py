#!/usr/bin/env python3
# fix_site3.py — VITROSCAPE round-3 patches
# 1) remove island-page link feature
# 2) fix progress-track click jump (shortest path around loop)
# 3) add scroll tail so last S3 works are fully reachable (was: cut off by S1 wrap)
# 4) redesign custom cursor: smaller ring + velocity stretch + RGB dispersion
# 5) visual: particle colours, card facing dim, Klein-blue accents
import io, sys

path = 'index.html'
src = io.open(path, encoding='utf-8').read()

patches = []

# ── 1a. remove #lb-link CSS ──
patches.append(('lb-link css', '''    /* ══ LIGHTBOX PROJECT LINK ══ */
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

''', ''))

# ── 1b. remove link:true from Standing project ──
patches.append(('link:true', "Standing_at_the_Center_of_the_Continental_Shelf.webp', link:true },",
                "Standing_at_the_Center_of_the_Continental_Shelf.webp' },"))

# ── 1c. remove lb-link JS block ──
patches.append(('lb-link js', '''    if (proj.link) {
      const a = document.createElement('a')
      a.id = 'lb-link'
      a.href = 'Immersion_Rupestre/' + (currentLang === 'zh' ? 'cn' : currentLang) + '/'
      a.target = '_blank'
      a.rel = 'noopener'
      a.textContent = { zh: '进入项目页面 ↗', fr: 'Voir le projet ↗', en: 'Enter project ↗' }[currentLang]
      lbInner.appendChild(a)
    }

''', ''))

# ── 2. progress-track click: shortest path around the loop ──
patches.append(('progress click', '''document.getElementById('progress-track').addEventListener('click', e => {
  const r = e.currentTarget.getBoundingClientRect()
  const frac = Math.min(1, Math.max(0, (e.clientY - r.top) / r.height))
  const dpNow = ((lerpScroll % TOTAL) + TOTAL) % TOTAL
  rawScroll += ((frac * TOTAL - dpNow) % TOTAL + TOTAL) % TOTAL
})''', '''document.getElementById('progress-track').addEventListener('click', e => {
  const r = e.currentTarget.getBoundingClientRect()
  const frac = Math.min(1, Math.max(0, (e.clientY - r.top) / r.height))
  const dpNow = ((lerpScroll % TOTAL) + TOTAL) % TOTAL
  // shortest path around the loop (may scroll backwards)
  let delta = (frac * TOTAL - dpNow) % TOTAL
  if (delta >  TOTAL / 2) delta -= TOTAL
  if (delta < -TOTAL / 2) delta += TOTAL
  rawScroll += delta
})'''))

# ── 3a. TOTAL gains a tail region ──
patches.append(('TOTAL init', '''let PAGE_H = window.innerHeight
let TOTAL  = 4 * PAGE_H   // S1 + S-intro + S2 works + S3 works''',
'''let PAGE_H = window.innerHeight
const TAIL_FRAC = 0.7   // extra scroll room after the last card so S3 tail works stay fully visible before the loop wraps
let TOTAL  = (4 + TAIL_FRAC) * PAGE_H   // S1 + S-intro + S2 + S3 + tail'''))

patches.append(('TOTAL resize', '''  PAGE_H = window.innerHeight
  TOTAL  = 4 * PAGE_H''',
'''  PAGE_H = window.innerHeight
  TOTAL  = (4 + TAIL_FRAC) * PAGE_H'''))

# ── 3b. S3 cards centred inside their page with padding ──
patches.append(('targetCard S3', '''  if (dp < 3 * PAGE_H) return (dp - 2*PAGE_H) / PAGE_H * (S2_COUNT - 1)
  const t = (dp - 3 * PAGE_H) / PAGE_H
  return S2_COUNT + t * (S3_COUNT - 1)''',
'''  if (dp < 3 * PAGE_H) return (dp - 2*PAGE_H) / PAGE_H * (S2_COUNT - 1)
  const t = (dp - 3 * PAGE_H) / PAGE_H
  // centre cards mid-page with padding at both ends; clamp holds the last
  // card on screen through the tail region before the loop wraps
  return S2_COUNT + Math.max(0, Math.min(S3_COUNT - 1, t * S3_COUNT - 0.5))'''))

# ── 3c. snap targets (auto / idle / click) use the same mapping ──
patches.append(('snap auto S3',
  "          snapDp = 3 * PAGE_H + (nearCard - S2_COUNT) / (S3_COUNT - 1) * PAGE_H",
  "          snapDp = 3 * PAGE_H + (nearCard - S2_COUNT + 0.5) / S3_COUNT * PAGE_H"))
patches.append(('snap idle S3',
  "          targetDp = 3 * PAGE_H + (nearCard - S2_COUNT) / (S3_COUNT - 1) * PAGE_H",
  "          targetDp = 3 * PAGE_H + (nearCard - S2_COUNT + 0.5) / S3_COUNT * PAGE_H"))
patches.append(('snap click S3', '''    const snapDp = idx < S2_COUNT
      ? 2 * PAGE_H + Math.min(idx / (S2_COUNT - 1), 0.9999) * PAGE_H
      : 3 * PAGE_H + (idx - S2_COUNT) / (S3_COUNT - 1) * PAGE_H''',
'''    const snapDp = idx < S2_COUNT
      ? 2 * PAGE_H + Math.min(idx / (S2_COUNT - 1), 0.9999) * PAGE_H
      : 3 * PAGE_H + (idx - S2_COUNT + 0.5) / S3_COUNT * PAGE_H'''))

# ── 3d. helix fade-out only across the tail ──
patches.append(('workA fade', '''  let workA
  const FADE = PAGE_H
  if (dp < FADE) {
    workA = dp / FADE
  } else if (dp < TOTAL - FADE) {
    workA = 1
  } else {
    workA = (TOTAL - dp) / FADE
  }''',
'''  let workA
  const FADE = PAGE_H
  const FADE_OUT = 0.6 * PAGE_H   // tail-only fade — S3 cards keep full opacity
  if (dp < FADE) {
    workA = dp / FADE
  } else if (dp < TOTAL - FADE_OUT) {
    workA = 1
  } else {
    workA = (TOTAL - dp) / FADE_OUT
  }'''))

# ── 3e. tick marks follow real section starts (0/1/2/3 pages of 4.7) ──
patches.append(('ticks', '''  <div class="pt-tick active" style="top: 0%"></div>
  <div class="pt-tick" style="top: 33.333%"></div>
  <div class="pt-tick" style="top: 66.666%"></div>
  <div class="pt-tick" style="top: 100%"></div>''',
'''  <div class="pt-tick active" style="top: 0%"></div>
  <div class="pt-tick" style="top: 21.28%"></div>
  <div class="pt-tick" style="top: 42.55%"></div>
  <div class="pt-tick" style="top: 63.83%"></div>'''))

# ── 4a. cursor CSS: smaller ring + chromatic ghosts ──
patches.append(('cursor css', '''    /* ══ CUSTOM CURSOR ══ */
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
    }''',
'''    /* ══ CUSTOM CURSOR — dot + chromatic velocity ring ══ */
    #cursor-dot, #cursor-ring, #cursor-ring-r, #cursor-ring-c {
      position: fixed;
      top: 0; left: 0;
      border-radius: 50%;
      pointer-events: none;
      z-index: 3000;
      opacity: 0;
    }
    #cursor-dot {
      width: 5px; height: 5px;
      background: #fff;
      mix-blend-mode: difference;
      transition: opacity 0.3s ease;
    }
    #cursor-ring {
      width: 26px; height: 26px;
      border: 1px solid rgba(255,255,255,0.85);
      mix-blend-mode: difference;
      transition: opacity 0.3s ease, width 0.25s ease, height 0.25s ease,
                  background-color 0.25s ease;
    }
    #cursor-ring.hovering {
      width: 44px; height: 44px;
      background: rgba(255,255,255,0.16);
    }
    /* chromatic ghosts: trail apart with velocity, vanish at rest */
    #cursor-ring-r, #cursor-ring-c {
      width: 26px; height: 26px;
      border: 1px solid transparent;
      mix-blend-mode: multiply;
      transition: width 0.25s ease, height 0.25s ease;
    }
    #cursor-ring-r { border-color: rgba(255,45,85,0.85); }
    #cursor-ring-c { border-color: rgba(0,160,255,0.85); }
    #cursor-ring-r.hovering, #cursor-ring-c.hovering { width: 44px; height: 44px; }
    html.has-cursor, html.has-cursor * { cursor: none !important; }
    html.has-cursor:has(#lightbox.lb-open), html.has-cursor:has(#lightbox.lb-open) * { cursor: auto !important; }
    html.has-cursor:has(#lightbox.lb-open) #cursor-dot,
    html.has-cursor:has(#lightbox.lb-open) #cursor-ring,
    html.has-cursor:has(#lightbox.lb-open) #cursor-ring-r,
    html.has-cursor:has(#lightbox.lb-open) #cursor-ring-c { display: none; }
    @media (hover: none), (pointer: coarse) {
      #cursor-dot, #cursor-ring, #cursor-ring-r, #cursor-ring-c { display: none; }
    }'''))

# ── 4b. cursor HTML: two extra ghost rings ──
patches.append(('cursor html', '''<div id="cursor-dot"></div>
<div id="cursor-ring"></div>''',
'''<div id="cursor-dot"></div>
<div id="cursor-ring"></div>
<div id="cursor-ring-r"></div>
<div id="cursor-ring-c"></div>'''))

# ── 4c. cursor JS: velocity stretch + dispersion ──
patches.append(('cursor js', '''// Custom cursor: instant dot + inertial ring, difference blend works on any bg
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
}''',
'''// Custom cursor: instant dot + main ring + two chromatic ghost rings.
// Velocity stretches the ring along the motion axis while the red/cyan
// ghosts trail apart — a dispersion/smear that settles back at rest.
if (window.matchMedia('(hover: hover) and (pointer: fine)').matches) {
  document.documentElement.classList.add('has-cursor')
  const cDot = document.getElementById('cursor-dot')
  const cM   = document.getElementById('cursor-ring')
  const cR   = document.getElementById('cursor-ring-r')
  const cC   = document.getElementById('cursor-ring-c')
  let mx = innerWidth / 2, my = innerHeight / 2
  const pos = { m: [mx, my], r: [mx, my], c: [mx, my] }
  let smStretch = 0, smAngle = 0
  window.addEventListener('mousemove', e => {
    mx = e.clientX; my = e.clientY
    cDot.style.opacity = '1'
    cM.style.opacity   = '1'
    cDot.style.transform = `translate(${mx}px, ${my}px) translate(-50%, -50%)`
    const hov = e.target.closest && e.target.closest(
      'button, a, input, #progress-track, #scroll-cue, #helix-canvas'
    )
    for (const el of [cM, cR, cC]) el.classList.toggle('hovering', !!hov)
  }, { passive: true })
  document.addEventListener('mouseleave', () => {
    cDot.style.opacity = '0'
    cM.style.opacity   = '0'
  })
  const follow = (p, k) => { p[0] += (mx - p[0]) * k; p[1] += (my - p[1]) * k }
  ;(function cursorLoop() {
    follow(pos.m, 0.22); follow(pos.r, 0.10); follow(pos.c, 0.15)
    // velocity estimate from the main ring's lag behind the pointer
    const vx = mx - pos.m[0], vy = my - pos.m[1]
    const speed = Math.hypot(vx, vy)
    smStretch += (Math.min(speed * 0.022, 0.55) - smStretch) * 0.18
    if (speed > 0.6) {
      const a = Math.atan2(vy, vx)
      let da = a - smAngle
      while (da >  Math.PI) da -= 2 * Math.PI
      while (da < -Math.PI) da += 2 * Math.PI
      smAngle += da * 0.2
    }
    const deg = smAngle * 180 / Math.PI
    const sx  = 1 + smStretch
    const sy  = 1 - smStretch * 0.45
    cM.style.transform = `translate(${pos.m[0]}px, ${pos.m[1]}px) translate(-50%, -50%) rotate(${deg}deg) scale(${sx}, ${sy})`
    cR.style.transform = `translate(${pos.r[0]}px, ${pos.r[1]}px) translate(-50%, -50%) rotate(${deg}deg) scale(${sx}, ${sy})`
    cC.style.transform = `translate(${pos.c[0]}px, ${pos.c[1]}px) translate(-50%, -50%) rotate(${deg}deg) scale(${sx}, ${sy})`
    // ghosts appear only while moving
    const ghost = Math.min(speed * 0.05, 1) * 0.9
    cR.style.opacity = ghost.toFixed(3)
    cC.style.opacity = ghost.toFixed(3)
    requestAnimationFrame(cursorLoop)
  })()
}'''))

# ── 5a. particles: cool ink tones + Klein-blue accents ──
patches.append(('particle colors', '''  // gray: lighter toward top of thread, random variation
  const g = 0.20 + t * 0.45 + Math.random() * 0.20
  pColArr[i * 3] = pColArr[i * 3 + 1] = pColArr[i * 3 + 2] = Math.min(g, 0.88)''',
'''  // cool ink monochrome (blue-shifted shadows) + Klein-blue accents
  const g  = 0.16 + t * 0.42 + Math.random() * 0.20
  const gg = Math.min(g, 0.82)
  if (Math.random() < 0.12) {
    const kb = 0.55 + t * 0.45   // International Klein Blue, brighter upward
    pColArr[i * 3]     = 0.10
    pColArr[i * 3 + 1] = 0.18 * kb + 0.08
    pColArr[i * 3 + 2] = 0.65 * kb + 0.25
  } else {
    pColArr[i * 3]     = gg * 0.92
    pColArr[i * 3 + 1] = gg * 0.96
    pColArr[i * 3 + 2] = Math.min(gg * 1.08, 0.88)
  }'''))

# ── 5b. gallery focus: dim cards as they turn away ──
patches.append(('card dim', '''    proj._mesh.rotation.y  = proj._theta * (1 - blend) + angle * blend
    proj._mesh.scale.setScalar(0.60 + 0.55 * blend)''',
'''    proj._mesh.rotation.y  = proj._theta * (1 - blend) + angle * blend
    proj._mesh.scale.setScalar(0.60 + 0.55 * blend)
    // gallery focus: dim cards as they turn away from the camera
    if (proj._mesh.material.map) {
      proj._mesh.material.color.setScalar(0.42 + 0.58 * blend)
    }'''))

# ── 5c. Klein-blue accents on the progress track ──
patches.append(('thumb accent', '''    .pt-tick.active { background: #111; transform: scale(1.5); }''',
'''    .pt-tick.active { background: #002fa7; transform: scale(1.5); }'''))
patches.append(('thumb accent 2', '''      border-radius: 50%;
      background: #111;
      box-shadow: 0 0 0 5px rgba(0,0,0,0.05);
      pointer-events: none;''',
'''      border-radius: 50%;
      background: #002fa7;
      box-shadow: 0 0 0 5px rgba(0,47,167,0.10);
      pointer-events: none;'''))

applied, failed = [], []
for name, old, new in patches:
    n = src.count(old)
    if n == 1:
        src = src.replace(old, new)
        applied.append(name)
    else:
        failed.append((name, n))

if failed:
    print('FAILED patches (occurrences found):')
    for name, n in failed:
        print(f'  {name}: {n}')
    sys.exit(1)

io.open(path, 'w', encoding='utf-8', newline='').write(src)
print(f'OK — {len(applied)} patches applied:')
for name in applied:
    print(f'  ✓ {name}')
