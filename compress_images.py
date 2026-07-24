#!/usr/bin/env python3
"""Generate hi-res lightbox images + recompress Immersion_Rupestre images."""
from PIL import Image
from pathlib import Path
import shutil

# ── 1. Lightbox large images (max 1920px, webp q88) ──
CARD_STEMS = [
    'gongpyeong_1', 'isynbio', 'Standing_at_the_Center_of_the_Continental_Shelf',
    'yunyi', 'UKI_1', 'Jeu_de_Mondes_1', 'VirtualTherapia',
    'they_dig_in_suitable_soil_the_mycological_2',
]
src_dir = Path('assets/images')
out_dir = src_dir / 'large'
out_dir.mkdir(exist_ok=True)
for stem in CARD_STEMS:
    orig = None
    for ext in ('.jpg', '.jpeg', '.png'):
        p = src_dir / f'{stem}{ext}'
        if p.exists():
            orig = p
            break
    if not orig:
        print(f'  !! original not found for {stem}')
        continue
    im = Image.open(orig).convert('RGB')
    if max(im.size) > 1920:
        r = 1920 / max(im.size)
        im = im.resize((round(im.width * r), round(im.height * r)), Image.LANCZOS)
    out = out_dir / f'{stem}.webp'
    im.save(out, 'WEBP', quality=88, method=6)
    print(f'  large/{stem}.webp  {orig.stat().st_size//1024}KB -> {out.stat().st_size//1024}KB')

# ── 2. IR textures: recompress JPEG in place (q80, keep 2K) ──
tex_dir = Path('Immersion_Rupestre/assets/mine_rock_wall_uebmddyn_2k')
total_before = total_after = 0
for p in sorted(tex_dir.glob('*.jpg')):
    b = p.stat().st_size
    im = Image.open(p)
    im.save(p, 'JPEG', quality=80, optimize=True, progressive=True)
    a = p.stat().st_size
    total_before += b; total_after += a
    print(f'  {p.name}  {b//1024}KB -> {a//1024}KB')
print(f'  textures total: {total_before//1024//1024}MB -> {total_after//1024//1024}MB')

# ── 3. IR PNGs 3-7 -> webp, move originals to backup ──
backup = Path('.review/ir-backup')
backup.mkdir(parents=True, exist_ok=True)
ir_assets = Path('Immersion_Rupestre/assets')
for n in range(3, 8):
    p = ir_assets / f'{n}.png'
    im = Image.open(p)
    if max(im.size) > 1920:
        r = 1920 / max(im.size)
        im = im.resize((round(im.width * r), round(im.height * r)), Image.LANCZOS)
    out = ir_assets / f'{n}.webp'
    im.save(out, 'WEBP', quality=88, method=6)
    shutil.move(str(p), backup / p.name)
    print(f'  IR {n}.png {p.stat().st_size if p.exists() else "?"} -> {out.stat().st_size//1024}KB webp')

# ── 4. Update references ../assets/N.png -> ../assets/N.webp in 3 IR pages ──
for lang in ('en', 'fr', 'cn'):
    hp = Path(f'Immersion_Rupestre/{lang}/index.html')
    s = hp.read_text(encoding='utf-8')
    for n in range(3, 8):
        s = s.replace(f'../assets/{n}.png', f'../assets/{n}.webp')
    hp.write_text(s, encoding='utf-8')
    print(f'  updated refs in {lang}/index.html')

print('Image compression done.')
