#!/usr/bin/env python3
"""PIL adjudication of crop_13 findings (mathzone F1/F3/F4/F5, tableeq F3, chart F5-hue/F7,
redstop F3/F4) against render_13 vs slide_050.jpg. Complements w050_chartfix_pil.py (F1/F2/F3/
F4/F6) and w050_arrow_redstop_pil.py (arrow ascii, redstop ascii). All coords in ORIG space."""
from PIL import Image
import numpy as np
import json

ROOT = "/home/ahmed/Projects/ai_llm_slides"
NS = f"{ROOT}/videos/machine-learning/03_ridger_regression_gradient_descent"
QA = f"{NS}/recreated_pptx/qa/slide050"
OUT = f"{QA}/w050_crop13_adj_raw.txt"

IMGS = {}
for name, path in (("ORIG", f"{NS}/unique_slides/slide_050.jpg"),
                   ("RENDER", f"{QA}/render_13.png")):
    im = Image.open(path).convert("RGB")
    IMGS[name] = (np.asarray(im).astype(int), im.size[0] / 960.0)

lines = []
def P(*a):
    t = " ".join(str(x) for x in a); lines.append(t); print(t)

def zone(name, x0, x1, y0, y1):
    img, s = IMGS[name]
    return img[int(y0*s):int(y1*s), int(x0*s):int(x1*s)], s

def lum(z): return 0.299*z[:,:,0] + 0.587*z[:,:,1] + 0.114*z[:,:,2]
def masks(z):
    R, G, B = z[:,:,0], z[:,:,1], z[:,:,2]
    red = (R > 110) & (R-G > 50) & (R-B > 40)
    ink = lum(z) < 200
    return ink, red

P("== crop_13 adjudication probes, scales:", {k: round(v, 4) for k, v in [(n, IMGS[n][1]) for n in IMGS]})

# ---- A. Initial-W construct: digit-row count on CURRENT bytes (mathzone F1 / tableeq F1)
P("\n## A. Initial-W zone x262..395 y55..100 — dark-ink row projection + ascii (lum<190)")
for name, step in (("ORIG", 1), ("RENDER", 2)):
    z, s = zone(name, 262, 395, 55, 100)
    ink = lum(z) < 190
    rows = ink.sum(axis=1)
    bands, st = [], None
    for i, v in enumerate(rows > 0):
        if v and st is None: st = i
        if not v and st is not None:
            if i - st >= 2: bands.append((round(55+st/s, 1), round(55+i/s, 1)))
            st = None
    if st is not None: bands.append((round(55+st/s, 1), round(55+len(rows)/s, 1)))
    P(f" {name}: ink-row bands (orig y): {bands}")
    P(f" {name} ascii (char={step/s:.2f}px, x262 y55):")
    for yy in range(0, ink.shape[0], step):
        P(f"{55+yy/s:3.0f} " + "".join("#" if ink[yy, xx:xx+step].any() else "." for xx in range(0, ink.shape[1], step)))

# ---- B. eta zone re-bank on render_13 (mathzone F2 / tableeq F2)
P("\n## B. eta zone x531..642 y58..84 ink counts (lum<210/200/190)")
for name in IMGS:
    z, s = zone(name, 531, 642, 58, 84)
    for th in (210, 200, 190):
        P(f" {name}: ink(lum<{th})={int((lum(z) < th).sum())}")

# ---- C. REPEAT underline check: red phrase rows + band below (mathzone F3 / tableeq F3)
P("\n## C. REPEAT red phrase x424..532 y56..96 — red rows + band-below ink")
for name in IMGS:
    z, s = zone(name, 424, 532, 56, 96)
    _, red = masks(z)
    rrows = np.where(red.any(axis=1))[0]
    if not len(rrows):
        P(f" {name}: NO red phrase found"); continue
    top, bot = 56 + rrows.min()/s, 56 + rrows.max()/s
    cols = np.where(red.any(axis=0))[0]
    P(f" {name}: red phrase y{top:.1f}..{bot:.1f} x{424+cols.min()/s:.1f}..{424+cols.max()/s:.1f}")
    band = red[int((bot+1-56)*s):, int((426-424)*s):int((460-424)*s)]
    P(f" {name}: red px in band below phrase (x426..460, y>{bot+1:.0f}): {int(band.sum())}")

# ---- D. eq sidecars: what the render's Initial-W / finalW actually contain
P("\n## D. eq sidecar mathtext strings")
for n in ("eq_050_initialW", "eq_050_finalW"):
    try:
        d = json.load(open(f"{NS}/recreated_pptx/build/assets/{n}.json"))
        P(f" {n}: mathtext={d.get('mathtext')!r} w_in={d.get('w_in')} h_in={d.get('h_in')} px={d.get('px') or d.get('px_wh')}")
    except Exception as e:
        P(f" {n}: ERROR {e}")

# ---- E. augmented-vectors panel: paren-structure (tableeq F3)
P("\n## E. augmented panel x66..248 y136..248 — dark-ink ascii + tall-paren column runs")
for name, step in (("ORIG", 1), ("RENDER", 2)):
    z, s = zone(name, 66, 248, 136, 248)
    ink = lum(z) < 170
    P(f" {name} ascii (char={step/s:.2f}px, x66 y136):")
    for yy in range(0, ink.shape[0], step*2):
        P(f"{136+yy/s:3.0f} " + "".join("#" if ink[yy, xx:xx+step].any() else "." for xx in range(0, ink.shape[1], step)))
for name in IMGS:
    z, s = zone(name, 85, 232, 155, 245)
    ink = lum(z) < 170
    runs_per_col = []
    for xx in range(ink.shape[1]):
        col = ink[:, xx]
        best, cur = 0, 0
        for v in col:
            cur = cur + 1 if v else 0
            best = max(best, cur)
        runs_per_col.append(best / s)
    tall = [85 + i/s for i, v in enumerate(runs_per_col) if v >= 25]
    med = [85 + i/s for i, v in enumerate(runs_per_col) if 8 <= v < 25]
    P(f" {name}: columns with continuous dark run >=25px (tall-paren candidates): "
      f"n={len(tall)} x={' '.join(f'{v:.0f}' for v in tall[:40])}")
    P(f" {name}: columns with max run 8..25px (cell-paren scale): n={len(med)}")

# ---- F. decision-line hue + gridline weight (chart F5 hue / F7)
P("\n## F1. line mid-stroke RGB at x=450 (line y~329) and x=550 (y~319), 3px window median")
for cx, cy in ((450, 329), (550, 319)):
    for name in IMGS:
        z, s = zone(name, cx-2, cx+2, cy-3, cy+3)
        R, G, B = z[:,:,0], z[:,:,1], z[:,:,2]
        red = (R > 110) & (R-G > 50) & (R-B > 40)
        if red.sum() < 3:
            P(f" ({cx},{cy}) {name}: no red stroke found in window"); continue
        med = np.median(z[red].reshape(-1, 3), axis=0).astype(int)
        P(f" ({cx},{cy}) {name}: line red median #{med[0]:02X}{med[1]:02X}{med[2]:02X} n={int(red.sum())}")
P("\n## F2. gridline profile at data y=1 (py 397.8): min-lum per image across x420..760")
for name in IMGS:
    z, s = zone(name, 420, 760, 394, 402)
    l = lum(z)
    P(f" {name}: darkest row min-lum={l.min():.0f} mean-of-row-min={l.min(axis=1).mean():.0f} "
      f"dark(<215)px={int((l < 215).sum())}")

# ---- G. banner red + Stop red medians (redstop F3/F4)
P("\n## G. red fills: banner 'Iteration 2' box x125..175 y284..298; 'Stop' glyphs x88..130 y376..396")
for name in IMGS:
    z, s = zone(name, 125, 175, 284, 298)
    R, G, B = z[:,:,0], z[:,:,1], z[:,:,2]
    red = (R > 110) & (R-G > 50) & (R-B > 40)
    med = np.median(z[red].reshape(-1, 3), axis=0).astype(int)
    P(f" {name}: banner red median #{med[0]:02X}{med[1]:02X}{med[2]:02X} n={int(red.sum())}")
for name in IMGS:
    z, s = zone(name, 88, 130, 376, 396)
    R, G, B = z[:,:,0], z[:,:,1], z[:,:,2]
    red = (R > 110) & (R-G > 50) & (R-B > 40)
    if red.sum() < 5:
        P(f" {name}: Stop-zone red px<5 (n={int(red.sum())})"); continue
    med = np.median(z[red].reshape(-1, 3), axis=0).astype(int)
    P(f" {name}: Stop red median #{med[0]:02X}{med[1]:02X}{med[2]:02X} n={int(red.sum())}")

# ---- H. L4 caption 'positive'/'negative' slant metric (mathzone F5)
P("\n## H. caption words: per-row centroid drift over word bboxes (italic => drift grows with row)")
WORDS = {"positive": (288, 344, 108, 126), "negative": (390, 450, 108, 126)}
for wname, (x0, x1, y0, y1) in WORDS.items():
    for name in IMGS:
        z, s = zone(name, x0, x1, y0, y1)
        ink = lum(z) < 190
        if ink.sum() < 20:
            P(f" {wname} {name}: ink<20 (n={int(ink.sum())}) — zone miss"); continue
        rows = np.where(ink.any(axis=1))[0]
        top, bot = rows.min(), rows.max()
        c_top = np.where(ink[top:top+3].any(axis=0))[0]
        c_bot = np.where(ink[bot-2:bot+1].any(axis=0))[0]
        drift = ((c_bot.mean() if len(c_bot) else np.nan) - (c_top.mean() if len(c_top) else np.nan)) / s
        P(f" {wname} {name}: y{y0+top/s:.0f}..{y0+bot/s:.0f} centroid-drift bottom-vs-top={drift:+.1f}px")

with open(OUT, "w") as f:
    f.write("\n".join(lines) + "\n")
P(f"\n[saved {OUT}]")
