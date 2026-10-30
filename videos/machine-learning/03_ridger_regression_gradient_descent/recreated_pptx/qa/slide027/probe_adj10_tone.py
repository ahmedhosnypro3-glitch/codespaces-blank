"""Third pass: the whole diagram's ink tone + the 'Cost' label position.

axis_top probe 2 found the ORIGINAL's y-axis shaft is grey (core RGB 80,81,79, width
3.00 fpx) while the render's is black (36,36,36, 2.40 fpx) and the arrowhead likewise
grey (96,98,95) vs black (1,1,1). Before deciding whether that is a fix, measure the
SAME tone for the x-axis and the curve core, and locate the 'Cost' label that both
judges saw in the crop."""
import numpy as np
from PIL import Image

QA = "videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide027/"
ORIG = "videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_027.jpg"
REND = QA + "render_10.png"


def load(p):
    a = np.asarray(Image.open(p).convert("RGB")).astype(float)
    return a, a.shape[1] / 960.0


def lum(a):
    return 0.299 * a[:, :, 0] + 0.587 * a[:, :, 1] + 0.114 * a[:, :, 2]


oa, so = load(ORIG)
ra, sr = load(REND)

print("### x-axis shaft tone (frame y 432..442, x 300..680 — no dots there)")
for tag, im, s in (("ORIG", oa, so), ("REND", ra, sr)):
    y0, y1, x0, x1 = (int(v * s) for v in (432, 442, 300, 680))
    L = lum(im)[y0:y1, x0:x1]
    S = im[y0:y1, x0:x1].max(axis=2) - im[y0:y1, x0:x1].min(axis=2)
    ink = (L < 160) & (S < 60)
    rowfrac = ink.sum(axis=1) / ink.shape[1]
    r = int(np.argmax(rowfrac))
    px = im[y0:y1, x0:x1][rowfrac > 0.5]
    print(f"  {tag}: strongest row (frame y {r/s+432:.0f}) covers {rowfrac.max()*100:.0f}%"
          f" | ink px n={len(px)} mean RGB ({px[:,0].mean():.0f},{px[:,1].mean():.0f},"
          f"{px[:,2].mean():.0f}) | lum p50 "
          f"{np.median(0.299*px[:,0]+0.587*px[:,1]+0.114*px[:,2]) if len(px) else float('nan'):.0f}")

print("\n### curve core tone (frame x 300..560, y 360..395 — the flat bowl bottom, no dots)")
for tag, im, s in (("ORIG", oa, so), ("REND", ra, sr)):
    y0, y1, x0, x1 = (int(v * s) for v in (360, 395, 300, 560))
    sub = im[y0:y1, x0:x1]
    L = lum(sub); S = sub.max(axis=2) - sub.min(axis=2)
    ink = (L < 90) & (S < 45)
    px = sub[ink]
    print(f"  {tag}: n={len(px)} mean RGB ({px[:,0].mean():.0f},{px[:,1].mean():.0f},"
          f"{px[:,2].mean():.0f}) | lum p50 {np.median(0.299*px[:,0]+0.587*px[:,1]+0.114*px[:,2]) if len(px) else float('nan'):.0f}")

print("\n### 'Cost' label: scan the whole crop region frame(190,170)-(332,292) for ink")
for tag, im, s in (("ORIG", oa, so), ("REND", ra, sr)):
    L = lum(im)[int(170 * s):int(292 * s), int(190 * s):int(332 * s)]
    m = L < 160
    ys, xs = np.where(m)
    if not len(xs):
        print(f"  {tag}: NO ink at all in the crop")
        continue
    print(f"  {tag}: ink bbox x {xs.min()/s+190:.0f}..{xs.max()/s+190:.0f} "
          f"y {ys.min()/s+170:.0f}..{ys.max()/s+170:.0f} n={len(xs)}")
    # histogram of ink rows to see the separate bands
    rows, cnt = np.unique(ys / s + 170, return_counts=True)
    bands, k0 = [], 0
    for i in range(1, len(rows)):
        if rows[i] - rows[i - 1] > 2:
            bands.append((rows[k0], rows[i - 1], cnt[k0:i].sum())); k0 = i
    bands.append((rows[k0], rows[-1], cnt[k0:].sum()))
    print(f"       row bands: {[(round(a), round(b), int(c)) for a, b, c in bands]}")

print("\n### black vs grey ink census of the crop (spread<45)")
for tag, im, s in (("ORIG", oa, so), ("REND", ra, sr)):
    L = lum(im)[int(170 * s):int(292 * s), int(190 * s):int(332 * s)]
    S = im[int(170 * s):int(292 * s), int(190 * s):int(332 * s)].max(axis=2) - \
        im[int(170 * s):int(292 * s), int(190 * s):int(332 * s)].min(axis=2)
    for name, m in (("black lum<60", (L < 60) & (S < 45)),
                    ("grey 60..150", (L >= 60) & (L < 150) & (S < 45)),
                    ("light 150..210", (L >= 150) & (L < 210) & (S < 45))):
        print(f"  {tag} {name:15s}: n={int(m.sum())}")

print("\n### orange/violet in the crop (the purple dots) — tone check")
for tag, im, s in (("ORIG", oa, so), ("REND", ra, sr)):
    sub = im[int(170 * s):int(292 * s), int(190 * s):int(332 * s)]
    R, G, B = sub[:, :, 0], sub[:, :, 1], sub[:, :, 2]
    m = (B > 140) & (B - R > 40) & (G < 150)
    px = sub[m]
    if len(px):
        print(f"  {tag}: n={len(px)} mean RGB ({px[:,0].mean():.0f},{px[:,1].mean():.0f},{px[:,2].mean():.0f})")
    else:
        print(f"  {tag}: none")
    yl = (R > 200) & (G > 190) & (B < 110) & (R - B > 110)
    pxy = sub[yl]
    if len(pxy):
        print(f"  {tag} yellow: n={len(pxy)} mean RGB ({pxy[:,0].mean():.0f},{pxy[:,1].mean():.0f},{pxy[:,2].mean():.0f})")
