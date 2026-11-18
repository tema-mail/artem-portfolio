"""Вертикальный фон сторис 1080x1920 из горизонтального nsk.png – кодом, бесплатно (Codex разлогинен 18.11).
Небо – градиент с мягким шумом, полоса города посередине (верх растворён – обрезанные кроны пальм), вода – нарисована."""
from PIL import Image, ImageFilter
import numpy as np
from pathlib import Path
R = Path(__file__).resolve().parent.parent
W, H, TOP = 1080, 1920, 420
src = Image.open(R / 'assets/raw/bg/nsk.png').convert('RGB')
sc = src.resize((1300, round(864 * 1300 / 1536)), Image.LANCZOS)
strip = np.asarray(sc.crop((110, 0, 110 + W, sc.height))).astype(float); sh = strip.shape[0]
# где начинается вода: ищем строку под городом по средней яркости центра (вода светлее набережной не всегда) – берём 0.9 высоты
wy = int(sh * 0.905)
deep = np.array([40, 12, 84], float); top_col = strip[:30].mean(axis=(0, 1))
c = np.zeros((H, W, 3), float)
for y in range(H):
    t = min(1, (y / (TOP + 60)) ** 1.2); c[y] = deep * (1 - t) + top_col * t
c[TOP:TOP + wy] = strip[:wy]
F = 260
for i in range(F):
    k = (i / F) ** 1.6; c[TOP + i] = strip[i] * k + c[TOP - 1] * (1 - k)
cut = TOP + wy; h = H - cut
c1 = strip[wy:wy + 8, 300:780].mean(axis=(0, 1)); c2 = np.array([30, 12, 52], float)
t = np.linspace(0, 1, h)[:, None]; water = (c1 * (1 - t) + c2 * t)[:, None, :].repeat(W, 1)
rng = np.random.default_rng(3); sunx = W // 2
for y in range(h):
    k = 1 - y / h
    for _ in range(3):
        if rng.random() < .5:
            w = int(rng.integers(30, 150) * (0.4 + k)); x0 = sunx + int(rng.normal(0, 25 + 110 * (1 - k))) - w // 2
            water[y, max(0, x0):min(W, x0 + w)] += np.array([110, 65, 20]) * k * rng.uniform(.3, .8)
c[cut:] = np.asarray(Image.fromarray(water.clip(0, 255).astype('uint8')).filter(ImageFilter.GaussianBlur(1.5))).astype(float)
for i in range(12):                                   # стык
    k = i / 12; c[cut + i] = c[cut - 1] * (1 - k) + c[cut + i] * k
n = Image.fromarray((np.random.default_rng(7).random((H // 24, W // 24)) * 255).astype('uint8')).resize((W, H), Image.BICUBIC).filter(ImageFilter.GaussianBlur(40))
nm = (np.asarray(n).astype(float) / 255 - .5) * 24; mask = np.clip(1 - np.arange(H) / TOP, 0, 1)[:, None]
out = Image.fromarray((c + (nm * mask)[:, :, None] * np.array([1, .6, 1])).clip(0, 255).astype('uint8'))
out.save(R / 'assets/raw/bg/nsk-story.png'); out.save(R / 'public/img/nsk-story.webp', 'WEBP', quality=80, method=6)
print('ok, вода с', cut)
