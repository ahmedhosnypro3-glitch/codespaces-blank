#!/usr/bin/env python3
"""render_21 outlier-column verify: digit clusters/colors, yellow bands, rule hues (frame space 960x540)."""
from PIL import Image
import numpy as np

V = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
ri = Image.open(f"{V}/recreated_pptx/qa/slide019/render_21.png").convert("RGB")
oi = Image.open(f"{V}/unique_slides/slide_019.jpg").convert("RGB")
ra = np.asarray(ri).astype(int)
oa = np.asarray(oi).astype(int)
RS = ri.size[0] / 960.0
print(f"render_21 {ri.size} scale {RS:.4f}")


def zone(a, x0, y0, x1, y1, s=1.0):
    return a[int(y0 * s):int(y1 * s), int(x0 * s):int(x1 * s)]


def masks(c):
    r, g, b = c[..., 0], c[..., 1], c[..., 2]
    return {
        "yellow": (r > 200) & (g > 200) & (b < 160),
        "blue":   (b > 120) & (b - r > 50) & (b - g > 40),
        "red":    (r > 110) & (r - g > 55) & (r - b > 55),
        "green":  (g > 80) & (g - r > 30) & (g - b > 30),
        "dark":   c.sum(axis=2) < 300,
    }


EXPECT = [
    ("G1 '11'", 196, 216, "blue"),
    ("G1 '3'",  216, 240, "blue"),
    ("G1 '22'", 266, 292, "green"),
    ("G2 '30'", 322, 344, "red"),
    ("G2 '3'",  347, 368, "blue"),
    ("G2 '22'", 372, 398, "green"),
    ("G3 '60'", 425, 447, "red"),
    ("G3 '3'",  451, 472, "blue"),
    ("G3 '22'", 477, 502, "green"),
]

for tag, a, s in (("ORIG", oa, 1.0), ("REND21", ra, RS)):
    print(f"=== {tag}: outlier digit windows x82..118 ===")
    for name, y0, y1, want in EXPECT:
        z = zone(a, 82, y0, 118, y1, s)
        m = masks(z)
        got = None
        for col in ("red", "blue", "green"):
            if m[col].sum() >= 3:
                got = col
                xs = np.nonzero(m[col].any(axis=0))[0]
                xc = (82 + xs.mean() / s) if s == 1.0 else (82 + (xs.mean() + int(82 * s)) / s)
                ok = "OK" if col == want else f"WANT {want}"
                print(f"  {name:8s} y{y0}..{y1}: {col:5s} n={int(m[col].sum()):4d} xspan {82+xs[0]/s:.0f}..{82+xs[-1]/s:.0f}  [{ok}]")
                break
        if got is None:
            print(f"  {name:8s} y{y0}..{y1}: NO colored ink (want {want})  <<<<")

print("=== YELLOW BAND ROW RUNS x80..116, y190..510 ===")
for tag, a, s in (("ORIG", oa, 1.0), ("REND21", ra, RS)):
    z = zone(a, 80, 190, 116, 510, s)
    m = masks(z)
    rows = np.nonzero(m["yellow"].sum(axis=1) >= 2)[0]
    runs, st = [], None
    for i, yv in enumerate(rows):
        if st is None:
            st = yv
        elif yv != rows[i - 1] + 1:
            runs.append((st, rows[i - 1])); st = yv
    if st is not None:
        runs.append((st, rows[-1]))
    print(f"  {tag}: " + ", ".join(f"y{190 + a_ / s:.0f}..{190 + b_ / s:.0f}(h{(b_ - a_) / s:.0f})" for a_, b_ in runs))

print("=== BRACKET dark ink x58..78, y195..270 (G1) ===")
for tag, a, s in (("ORIG", oa, 1.0), ("REND21", ra, RS)):
    z = zone(a, 58, 195, 78, 270, s)
    m = masks(z)
    print(f"  {tag}: dark n={int(m['dark'].sum())}")

print("=== STRAY CHECK: colored ink x118..140 (right of outlier col), y190..510 ===")
for tag, a, s in (("ORIG", oa, 1.0), ("REND21", ra, RS)):
    z = zone(a, 118, 190, 140, 510, s)
    m = masks(z)
    tot = sum(int(m[k].sum()) for k in ("blue", "red", "green"))
    print(f"  {tag}: colored n={tot}")

print("=== RULE-HUE STRIPS (want maroonish in REND21 for the four rect edges) ===")


def huecount(c):
    r, g, b = c[..., 0].astype(int), c[..., 1].astype(int), c[..., 2].astype(int)
    dark = c.sum(axis=2) < 480
    out = {"n": int(dark.sum())}
    if dark.sum() == 0:
        return out
    rr, gg, bb = r[dark], g[dark], b[dark]
    out["mar"] = int(((rr - gg > 15) & (rr - bb > 15) & (bb - gg < 30)).sum())
    out["nav"] = int(((bb - rr > 15) & (bb - gg > 10)).sum())
    out["neu"] = out["n"] - out["mar"] - out["nav"]
    out["rgb"] = (int(rr.mean()), int(gg.mean()), int(bb.mean()))
    return out


STRIPS = [
    ("W-enclos left edge",   127.5, 215, 132.5, 285),
    ("W-enclos top edge",    132, 212, 200, 216),
    ("grid outer left edge", 205, 215, 209, 285),
    ("grid outer top edge",  210, 214, 360, 218),
    ("grid hline gy+21",     220, 224.5, 360, 228.5),
    ("grid hline gy+43",     220, 246.5, 360, 250.5),
    ("intercol rule x390",   388.5, 215, 392.5, 285),
]
print(f"{'strip':22s} {'ORIG':44s} {'REND21':44s}")
for name, x0, y0, x1, y1 in STRIPS:
    ho = huecount(zone(oa, x0, y0, x1, y1))
    hr = huecount(zone(ra, x0, y0, x1, y1, RS))
    fo = f"n={ho['n']:4d} mar={ho.get('mar', 0):4d} nav={ho.get('nav', 0):3d} neu={ho.get('neu', 0):4d} rgb{ho.get('rgb', '-')}"
    fr = f"n={hr['n']:4d} mar={hr.get('mar', 0):4d} nav={hr.get('nav', 0):3d} neu={hr.get('neu', 0):4d} rgb{hr.get('rgb', '-')}"
    print(f"{name:22s} {fo:44s} {fr:44s}")
