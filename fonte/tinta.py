#!/usr/bin/env python3
"""Gera textura de aquarela / tinta de alcool em azul petroleo com folhas de ouro."""
import sys
import numpy as np
from scipy import ndimage
from PIL import Image, ImageFilter

W, H = int(sys.argv[1]) if len(sys.argv) > 1 else 1600, int(sys.argv[2]) if len(sys.argv) > 2 else 1000
SEED = int(sys.argv[3]) if len(sys.argv) > 3 else 7
OUT = sys.argv[4] if len(sys.argv) > 4 else "tinta.jpg"
rng = np.random.default_rng(SEED)

def fbm(h, w, oct=6, base=4, pers=.55):
    out = np.zeros((h, w)); amp = 1; tot = 0
    for o in range(oct):
        gh, gw = base * 2**o + 2, int((base * 2**o) * w / h) + 2
        g = rng.standard_normal((gh, gw))
        z = ndimage.zoom(g, (h / gh * 1.02, w / gw * 1.02), order=3)[:h, :w]
        out += amp * z; tot += amp; amp *= pers
    out /= tot
    return (out - out.mean()) / out.std()

yy, xx = np.mgrid[0:H, 0:W].astype(float)
# camadas de distorcao (domain warping) para o aspecto fluido
q1, q2 = fbm(H, W, 4, 2, .5), fbm(H, W, 4, 2, .5)
r1, r2 = fbm(H, W, 4, 3, .5), fbm(H, W, 4, 3, .5)
base = fbm(H, W, 4, 2, .45)
A = 160
wx = xx + A * q1 + 1.6 * A * r1 * q2
wy = yy + A * q2 + 1.6 * A * r2 * q1
f = ndimage.map_coordinates(base, [np.clip(wy, 0, H - 1), np.clip(wx, 0, W - 1)], order=1, mode="reflect")
f = (f - f.min()) / (f.max() - f.min())

# bordas de pigmento (linhas mais escuras nas curvas de nivel)
bandas = np.abs(((f * 3.2) % 1) - .5) * 2           # 1 no meio da banda, 0 na borda
borda = np.clip(1 - bandas * 9, 0, 1) ** 1.5        # fino
borda = ndimage.gaussian_filter(borda, 1.2)
f = ndimage.gaussian_filter(f, 3)

# rampa de cor: tinta funda -> azul da marca -> nevoa
stops = np.array([0, .30, .55, .78, 1.0])
cores = np.array([
    [24, 48, 60],     # #18303C
    [36, 66, 80],     # #244250
    [62, 106, 124],   # #3E6A7C
    [92, 140, 156],   # #5C8C9C
    [150, 187, 196],  # #96BBC4
], float)
v = np.clip(f ** 1.15, 0, 1)
rgb = np.stack([np.interp(v, stops, cores[:, c]) for c in range(3)], -1)
rgb *= (1 - .22 * borda[..., None])
rgb += (np.clip(bandas,0,1)**8)[..., None] * 10

# granulacao de papel
grao = ndimage.gaussian_filter(rng.standard_normal((H, W)), .6)
rgb += grao[..., None] * 4

# folha de ouro: manchas recortadas + respingos
m = fbm(H, W, 6, 5)
m2 = ndimage.map_coordinates(m, [np.clip(yy + 60 * q1, 0, H - 1), np.clip(xx + 60 * q2, 0, W - 1)], order=1)
zona = ndimage.gaussian_filter((f > .62).astype(float) + (f < .18), 30)   # ouro onde a tinta acumula
m3 = ndimage.gaussian_filter(m2, 1.5)
ouro_mask = ((m3 > 2.15) & (zona > .25)).astype(float)
# respingos pequenos
n = int(W * H / 5200)
sp = np.zeros((H, W))
cx, cy = rng.integers(0, W, n), rng.integers(0, H, n)
keep = zona[cy, cx] > .1
sp[cy[keep], cx[keep]] = 1
sp = ndimage.binary_dilation(sp, iterations=1).astype(float)
grandes = rng.random(n) < .03
sp2 = np.zeros((H, W)); sp2[cy[keep & grandes], cx[keep & grandes]] = 1
sp2 = ndimage.binary_dilation(sp2, iterations=3).astype(float)
rasgo = ndimage.gaussian_filter(rng.standard_normal((H, W)), 1.2)
ouro_mask = ouro_mask * (rasgo > -.9) + ouro_mask * (ndimage.gaussian_filter(m2, .6) > 1.95) * 0
ouro_mask = np.clip(ouro_mask + sp + sp2, 0, 1)
ouro_mask = ndimage.gaussian_filter(ouro_mask, .7)
brilho = .78 + .22 * ndimage.gaussian_filter(rng.standard_normal((H, W)), 1.0) + .3 * np.clip(fbm(H, W, 3, 10), -1.2, 1.2)
ouro = np.stack([212 * brilho, 168 * brilho, 96 * brilho], -1)
rgb = rgb * (1 - ouro_mask[..., None]) + ouro * ouro_mask[..., None]

img = Image.fromarray(np.clip(rgb, 0, 255).astype(np.uint8))
img.save(OUT, quality=80, optimize=True, progressive=True)
print(OUT, img.size)
