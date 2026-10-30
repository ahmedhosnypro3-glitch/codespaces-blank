#!/usr/bin/env python3
# pil_adjud_a29_rgb.py — exact RGB samples + render header census + lambda10 dividers.
from PIL import Image
from collections import Counter

ROOT = "/home/ahmed/Projects/ai_llm_slides"
oi = Image.open(ROOT + "/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_019.jpg").convert("RGB")
ri = Image.open(ROOT + "/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide019/render_27.png").convert("RGB")
op, rp = oi.load(), ri.load()
S = ri.size[0] / 960.0

def modal(get, xs, ys, skip_white=True):
    c = Counter()
    for x in xs:
        for y in ys:
            p = get[int(x), int(y)]
            if skip_white and sum(p) > 700: continue
            c[p] += 1
    return c.most_common(4)

print("== ORIG edge RGB samples (modal ink) ==")
pts = {
    "anomaly left x65": ([65], [220, 260, 340, 460]),
    "anomaly right x117-124": ([117, 124], [220, 340, 460]),
    "NO REG right x377-378": ([377, 378], [220, 260, 340, 460]),
    "L3 rect left x383-384": ([383, 384], [220, 260, 340, 460]),
    "L3 rect right x637-639": ([637, 638, 639], [220, 260, 340, 460]),
    "L10 rect left x643": ([643], [220, 260, 340, 460]),
    "L10 rect right x894": ([894], [220, 260, 340, 460]),
    "W-box left x130 (g1)": ([130], [230, 260]),
    "W-box left x130 (g2)": ([130], [330, 360]),
    "divider x236 (g1)": ([236, 237], [210, 230, 250, 265]),
    "divider x269": ([269, 270], [210, 230, 250, 265]),
    "divider x302": ([302, 303], [210, 230, 250, 265]),
    "divider x335": ([335, 336], [210, 230, 250, 265]),
    "divider x368": ([368, 369], [210, 230, 250, 265]),
    "L3 div x496": ([496], [210, 230, 250, 265]),
    "L3 div x629": ([629], [210, 230, 250, 265]),
    "L10 div x724": ([724], [210, 230, 250, 265]),
    "W right x206 (g1)": ([206, 207], [210, 230, 250, 265]),
    "L3 W right x466": ([466, 467], [210, 230, 250, 265]),
    "L10 W right x724?": ([724, 725], [330, 360]),
}
for nm, (xs, ys) in pts.items():
    print(f"{nm}: {modal(op, xs, ys)}")

print()
print("== ORIG horizontal rule RGB (modal ink) ==")
for nm, xs, ys in [
    ("top rule y170 x130..370", range(130, 370, 7), [169, 170, 171]),
    ("top rule y170 x390..630", range(390, 630, 7), [169, 170, 171]),
    ("top rule y170 x650..890", range(650, 890, 7), [169, 170, 171]),
    ("top rule y170 x70..112 (anomaly)", range(70, 112, 3), [169, 170, 171]),
    ("bottom y524 x130..370", range(130, 370, 7), [523, 524, 525]),
    ("bottom y523-524 x390..630", range(390, 630, 7), [522, 523, 524]),
    ("bottom y522 x650..890", range(650, 890, 7), [521, 522, 523, 524]),
    ("bottom y524 x70..112 (anomaly)", range(70, 112, 3), [523, 524, 525]),
    ("grid rules g1 y224 x240..365", range(240, 365, 5), [224]),
    ("grid rules g1 y248 x240..365", range(240, 365, 5), [248]),
    ("grid rules g1 y272 x240..365", range(240, 365, 5), [272]),
    ("grid rules g2 y327/351/375 x240..365", range(240, 365, 5), [327, 351, 375]),
    ("grid rules g3 y439/463/487 x240..365", range(240, 365, 5), [439, 463, 487]),
]:
    print(f"{nm}: {modal(op, xs, ys)}")

print()
print("== ORIG grid-rule row presence (ink count x238..366) ==")
def rowink(y, x0=238, x1=366):
    n = 0
    for x in range(x0, x1):
        r, g, b = op[x, y]
        if not (r > 225 and g > 225 and b < 165) and not (r > 200 and g > 200 and b > 200):
            if abs(r - g) < 60 or r + g + b < 500:
                n += 1
    return n
for y in [222, 223, 224, 225, 226, 246, 247, 248, 249, 250, 270, 271, 272, 273, 274,
          325, 326, 327, 328, 349, 350, 351, 352, 373, 374, 375, 376,
          437, 438, 439, 440, 461, 462, 463, 464, 485, 486, 487, 488]:
    print(f"  y{y}: {rowink(y)}")

print()
print("== ORIG lambda10 grid dividers (x740..890, ink counts per column, y210..265) ==")
for x in range(740, 892, 2):
    n = 0
    for y in list(range(210, 265)) + list(range(315, 370)) + list(range(425, 480)):
        r, g, b = op[x, y]
        if r + g + b < 640 and not (r > 225 and g > 225):
            n += 1
    if n > 40:
        print(f"  x={x}: {n}")

print()
print("== RENDER header ink census y173..203 (frame coords) ==")
def rcls(p):
    r, g, b = p
    if r > 180 and g < 110 and b < 110: return "R"
    if b > 140 and r < 110 and g < 110: return "B"
    if g > 110 and r < 110 and b < 110: return "G"
    return None
for nm, x0, x1 in [("NO REG", 126, 378), ("RIDGE 3", 386, 636), ("RIDGE 10", 646, 892)]:
    dom = {}
    xs_by = {}
    for x in range(x0, x1):
        for y in range(173, 203):
            c = rcls(rp[min(int(x * S), ri.size[0] - 1), min(int(y * S), ri.size[1] - 1)])
            if c:
                dom[c] = dom.get(c, 0) + 1
                xs_by.setdefault(c, []).append(x)
    parts = [f"{c}={n} x{min(v)}..{max(v)}" for c, n in sorted(dom.items(), key=lambda kv: -kv[1]) for v in [xs_by[c]]]
    print(f"{nm}: " + " | ".join(parts) if parts else f"{nm}: no sat ink")

print()
print("== RENDER grid-rule presence check (are 3 h-rules drawn? g1) ==")
def rrowink(yf, x0=238, x1=366):
    n = 0
    for x in range(x0, x1):
        p = rp[min(int(x * S), ri.size[0] - 1), min(int(yf * S), ri.size[1] - 1)]
        r, g, b = p
        if r + g + b < 640:
            n += 1
    return n
for y in [222, 224, 226, 228, 246, 248, 250, 268, 270, 272, 274, 276]:
    print(f"  y{y}: {rrowink(y)}")
