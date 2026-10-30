#!/usr/bin/env python3
"""Outlier-column geometry (orig vs render_20) + rule-hue strips, frame space 960x540."""
from PIL import Image
import numpy as np

V = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
ri = Image.open(f"{V}/recreated_pptx/qa/slide019/render_20.png").convert("RGB")
oi = Image.open(f"{V}/unique_slides/slide_019.jpg").convert("RGB")
ra = np.asarray(ri).astype(int)
oa = np.asarray(oi).astype(int)
RS = ri.size[0] / 960.0
print(f"render {ri.size} scale {RS:.4f}")

def zone(a, x0, y0, x1, y1, s=1.0):
    return a[int(y0*s):int(y1*s), int(x0*s):int(x1*s)]

def masks(c):
    r, g, b = c[..., 0], c[..., 1], c[..., 2]
    return {
        "yellow": (r > 200) & (g > 200) & (b < 160),
        "blue":   (b > 120) & (b - r > 50) & (b - g > 40),
        "red":    (r > 110) & (r - g > 55) & (r - b > 55),
        "green":  (g > 80) & (g - r > 30) & (g - b > 30),
        "dark":   c.sum(axis=2) < 300,
    }

print("=== A. OUTLIER COLUMN x78..118, y190..510 (frame space) ===")
for tag, a, s in (("ORIG", oa, 1.0), ("REND", ra, RS)):
    z = zone(a, 78, 190, 118, 510, s)
    m = masks(z)
    h = z.shape[0]
    print(f"-- {tag} (rows rel. y190):")
    for name in ("yellow", "blue", "red", "green"):
        rows = np.nonzero(m[name].sum(axis=1) > (2 if name == "yellow" else 0))[0]
        if len(rows) == 0:
            print(f"   {name}: none"); continue
        # cluster contiguous row runs
        runs, st = [], rows[0]
        for i in range(1, len(rows)):
            if rows[i] != rows[i-1] + 1:
                runs.append((st, rows[i-1])); st = rows[i]
        runs.append((st, rows[-1]))
        desc = ", ".join(f"{190+a_:.0f}..{190+b_:.0f}(h{b_-a_+1})" for a_, b_ in runs if b_-a_ >= 1)
        print(f"   {name}: {desc}")
    # dark ink clusters (bracket + digits' dark parts)
    rows = np.nonzero(m["dark"].sum(axis=1) > 1)[0]
    if len(rows):
        runs, st = [], rows[0]
        for i in range(1, len(rows)):
            if rows[i] != rows[i-1] + 2:
                runs.append((st, rows[i-1])); st = rows[i]
        runs.append((st, rows[-1]))
        desc = ", ".join(f"{190+a_:.0f}..{190+b_:.0f}" for a_, b_ in runs if b_-a_ >= 2)
        print(f"   dark: {desc}")

print("=== B. RULE-HUE STRIPS (dark-ink hue at rule-only positions) ===")
def huecount(c):
    out = {}
    r, g, b = c[..., 0].astype(int), c[..., 1].astype(int), c[..., 2].astype(int)
    dark = c.sum(axis=2) < 480
    out["n_dark"] = int(dark.sum())
    if dark.sum() == 0:
        return out
    rr, gg, bb = r[dark], g[dark], b[dark]
    out["maroonish"] = int(((rr - gg > 15) & (rr - bb > 15) & (bb - gg < 30)).sum())
    out["navyish"]   = int(((bb - rr > 15) & (bb - gg > 10)).sum())
    out["neutral"]   = int(dark.sum()) - out["maroonish"] - out["navyish"]
    out["mean_rgb"]  = (int(rr.mean()), int(gg.mean()), int(bb.mean()))
    return out

STRIPS = [
    ("W-enclos left edge",   127.5, 215, 132.5, 285),
    ("W-enclos top edge",    132, 212, 200, 216),
    ("grid outer left edge", 205, 215, 209, 285),
    ("grid outer top edge",  210, 214, 360, 218),
    ("grid hline gy+21",     220, 224.5, 360, 228.5),
    ("grid hline gy+43",     220, 246.5, 360, 250.5),
    ("valcol vline x304",    303, 232, 306, 260),
    ("intercol rule x390",   388.5, 215, 392.5, 285),
]
print(f"{'strip':22s} {'ORIG':46s} {'RENDER_20':46s}")
for name, x0, y0, x1, y1 in STRIPS:
    ho = huecount(zone(oa, x0, y0, x1, y1))
    hr = huecount(zone(ra, x0, y0, x1, y1, RS))
    fo = f"n={ho['n_dark']:4d} mar={ho.get('maroonish',0):4d} nav={ho.get('navyish',0):4d} neu={ho.get('neutral',0):4d} rgb{ho.get('mean_rgb','-')}"
    fr = f"n={hr['n_dark']:4d} mar={hr.get('maroonish',0):4d} nav={hr.get('navyish',0):4d} neu={hr.get('neutral',0):4d} rgb{hr.get('mean_rgb','-')}"
    print(f"{name:22s} {fo:46s} {fr:46s}")
