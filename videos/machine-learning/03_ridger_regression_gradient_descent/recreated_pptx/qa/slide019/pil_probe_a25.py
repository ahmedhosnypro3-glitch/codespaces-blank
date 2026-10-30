#!/usr/bin/env python3
"""S4b probe: (A) original g1 outlier delimiter zone x74..116 y190..292 at
loose threshold (sum<420) — settles the small-arc nature + delimiter stroke
RGB. (B) NO-REG group-1 cells (x250..400, y215..265) ink census original vs
render_24 — settles judge-A24 MINOR#2 (row-1 ink blue-vs-red, ~0.6 conf)."""
from PIL import Image
from collections import Counter

V = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
Q = f"{V}/recreated_pptx/qa/slide019"

def classify(px):
    r, g, b = px
    s = r + g + b
    if s >= 420: return None
    if b > r + 25 and b > g + 25: return "BLUE"
    if r > g + 40 and r > b + 40: return "REDD"
    if g > r + 30 and g > b + 30: return "GREEN"
    return "DARK"

orig = Image.open(f"{V}/unique_slides/slide_019.jpg").convert("RGB")
rend = Image.open(f"{Q}/render_24.png").convert("RGB")
SX = rend.size[0] / orig.size[0]; SY = rend.size[1] / orig.size[1]

print("== (A) ORIG g1 zone x74..116 y190..292, ASCII: '#'=BLUE 'r'=REDD 'g'=GREEN 'd'=DARK '.'=loose-skipped ==")
op = orig.load()
print("    " + "".join(str(x % 10) for x in range(74, 117)))
for y in range(190, 293):
    row = []
    for x in range(74, 117):
        c = classify(op[x, y])
        row.append({"BLUE": "#", "REDD": "r", "GREEN": "g", "DARK": "d", None: "."}[c])
    print(f"y{y:3d} " + "".join(row))
cnt = Counter()
samples = {}
for y in range(190, 293):
    for x in range(74, 117):
        c = classify(op[x, y])
        if c:
            cnt[c] += 1
            samples.setdefault(c, []).append(op[x, y])
print("  class counts:", dict(cnt))
for c, ss in samples.items():
    n = len(ss)
    print(f"  {c}: mean RGB = ({sum(p[0] for p in ss)//n},{sum(p[1] for p in ss)//n},{sum(p[2] for p in ss)//n})")
# explicit RGB of the delimiter strokes (x83..85, y217..264 and x113..114)
for tag, xs, ys in [("g1 left delim", range(82, 87), range(215, 267)),
                    ("g1 right delim", range(112, 116), range(217, 267)),
                    ("g1 small-arc zone", range(91, 111), range(217, 236))]:
    ss = [op[x, y] for y in ys for x in xs if classify(op[x, y])]
    if ss:
        n = len(ss)
        print(f"  {tag}: n={n} mean=({sum(p[0] for p in ss)//n},{sum(p[1] for p in ss)//n},{sum(p[2] for p in ss)//n})")
    else:
        print(f"  {tag}: no loose-ink pixels")

print()
print("== (B) NO-REG group-1 cells x250..400 y215..265: ink class census ==")
for name, img, sc in [("ORIG", orig, (1.0, 1.0)), ("REND24", rend, (SX, SY))]:
    ip = img.load()
    cc = Counter(); samples = {}
    for y in range(215, 265):
        for x in range(250, 400):
            sx, sy = int(x * sc[0]), int(y * sc[1])
            r, g, b = ip[sx, sy]
            c = classify((r, g, b))
            if c:
                cc[c] += 1
                samples.setdefault(c, []).append((r, g, b))
    out = []
    for c, n in cc.most_common():
        ss = samples[c]; m = len(ss)
        out.append(f"{c}:{n} rgb({sum(p[0] for p in ss)//m},{sum(p[1] for p in ss)//m},{sum(p[2] for p in ss)//m})")
    print(f"  {name}: " + " | ".join(out) if out else f"  {name}: no ink")
# per-row-band split: x1 row band vs 30-40-50 band
for name, img, sc in [("ORIG", orig, (1.0, 1.0)), ("REND24", rend, (SX, SY))]:
    ip = img.load()
    for tag, y0, y1 in [("x1-row", 228, 242), ("304050", 243, 258)]:
        cc = Counter(); samples = {}
        for y in range(y0, y1):
            for x in range(250, 400):
                sx, sy = int(x * sc[0]), int(y * sc[1])
                c = classify(ip[sx, sy])
                if c:
                    cc[c] += 1
                    samples.setdefault(c, []).append(ip[sx, sy])
        out = []
        for c, n in cc.most_common():
            ss = samples[c]; m = len(ss)
            out.append(f"{c}:{n} rgb({sum(p[0] for p in ss)//m},{sum(p[1] for p in ss)//m},{sum(p[2] for p in ss)//m})")
        print(f"  {name} {tag}: " + (" | ".join(out) if out else "no ink"))
