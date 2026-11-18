"""Исходники из assets/raw → WebP в public/img. Запуск: python3 scripts/webp.py"""
from PIL import Image
from pathlib import Path
R = Path(__file__).resolve().parent.parent
raw, out = R / "assets/raw", R / "public/img"
(out / "works").mkdir(parents=True, exist_ok=True)

def save(im, p, w, q=82):
    im = im.copy()
    if im.width > w: im = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
    im.save(p, "WEBP", quality=q, method=6); print(p.relative_to(R), im.size, p.stat().st_size // 1024, "КБ")

hero = Image.open(raw / "portrait/hero-cut.png").convert("RGBA")
save(hero, out / "artem.webp", 1000); save(hero, out / "artem-600.webp", 600)
sun = Image.open(raw / "bg/sunset.png").convert("RGB")
save(sun, out / "sunset.webp", 1672, 78); save(sun, out / "sunset-900.webp", 900, 75)
# скрины: берём pf-*.jpg (без куки-плашки), иначе *.png; кадр 16:10 → 960x600
import sys; sys.path.insert(0, str(R))
# только те, что на сайте (src/data/works.ts)
import re
names = re.findall(r"id: '(\w+)'", (R / "src/data/works.ts").read_text())
for n in names:
    src = raw / f"works/pf-{n}.jpg"
    if not src.exists(): src = raw / f"works/{n}.png"
    im = Image.open(src).convert("RGB").crop((0, 0, 1440, 900))
    save(im, out / f"works/{n}.webp", 960, 80)
# превью для соцсетей
og = sun.resize((1200, 675)).crop((0, 22, 1200, 652)).convert("RGBA")
h = hero.resize((round(hero.width * 600 / hero.height), 600)); og.alpha_composite(h, ((1200 - h.width) // 2, 30))
og.convert("RGB").save(out / "og-cover.jpg", quality=85); print("og-cover.jpg")

# --- концепт TEYES Sibir (/teyes/): команда и фон Новосибирска
from PIL import ImageFilter
import numpy as np
from collections import deque
t = Image.open(raw / "team/team1.png").convert("RGB"); t = t.resize((1600, round(t.height * 1600 / t.width)), Image.LANCZOS)
a = np.asarray(t).astype(int); h, w, _ = a.shape
bg = np.median(np.concatenate([a[0], a[:, 0], a[:, -1]]), axis=0); d = np.sqrt(((a - bg) ** 2).sum(2))
mask = np.zeros((h, w), bool); q = deque([(0, x) for x in range(w)] + [(y, 0) for y in range(h)] + [(y, w - 1) for y in range(h)])
while q:
    y, x = q.popleft()
    if mask[y, x] or d[y, x] > 22: continue
    mask[y, x] = True
    for yy, xx in ((y - 1, x), (y + 1, x), (y, x - 1), (y, x + 1)):
        if 0 <= yy < h and 0 <= xx < w and not mask[yy, xx]: q.append((yy, xx))
alpha = Image.fromarray(((~mask) * 255).astype("uint8")).filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(1.2))
t.putalpha(alpha); save(t, out / "teyes-team.webp", 1600); save(t, out / "teyes-team-800.webp", 800)
n = Image.open(raw / "bg/nsk.png").convert("RGB"); save(n, out / "nsk.webp", 1536, 78); save(n, out / "nsk-900.webp", 900, 75)
