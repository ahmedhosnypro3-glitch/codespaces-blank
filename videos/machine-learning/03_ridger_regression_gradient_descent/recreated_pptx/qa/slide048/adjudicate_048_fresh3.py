#!/usr/bin/env python3
"""Third adjudication pass (fresh lane, w048-fresh-20261024):
   - red census in the ORIGINAL calc band, per box, with a proper red filter
   - arrow-glyph census in cols 430..504 of every calc box, both images
   - ASCII dump of the box-1 right expression (orig cols 640..810, rows 140..200)
   - render C1 red re-verify
"""
import json
from PIL import Image

ROOT = "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
ORIG = Image.open(f"{ROOT}/unique_slides/slide_048.jpg").convert("RGB")
REND = Image.open(f"{ROOT}/recreated_pptx/qa/slide048/render_3.png").convert("RGB")
OG = ORIG.convert("L"); RG = REND.convert("L")
OP, RP = OG.load(), RG.load()
S = 1125 / 540.0
rep = {}

BOXES = [(139, 197), (197, 272), (272, 330), (330, 395), (404, 461), (461, 528)]

def is_red(p):
    r, g, b = p
    return r - g > 30 and r - b > 30

def is_green(p):
    r, g, b = p
    return g - r > 25 and g - b > 25

def is_blue(p):
    r, g, b = p
    return b - r > 25 and b - g > 25

# ---------- 1. red census per calc box in the ORIGINAL ----------
red_detail = []
for y in range(139, 529):
    for x in range(275, 854):
        if is_red(ORIG.getpixel((x, y))):
            red_detail.append((x, y))
rep["orig_calc_red_total"] = len(red_detail)
per_box = []
for i, (t, b) in enumerate(BOXES):
    pts = [(x, y) for x, y in red_detail if t <= y <= b]
    per_box.append({"box": i + 1, "rows": [t, b], "red_px": len(pts)})
rep["orig_calc_red_per_box"] = per_box
# clusters of red in original calc band (group by col)
rc = {}
for x, y in red_detail:
    rc.setdefault(x, []).append(y)
clusters = []
for x in sorted(rc):
    ys = sorted(rc[x])
    s = p = ys[0]
    for y in ys[1:]:
        if y == p + 1: p = y
        else:
            clusters.append({"cols": [s, p]})  # placeholder
            s = p = y
    clusters.append((x, s, p))
# proper 2D clustering: bucket by (col,row) adjacency
pix = set(red_detail)
seen = set(); comps = []
for pt in red_detail:
    if pt in seen: continue
    stack = [pt]; seen.add(pt); comp = []
    while stack:
        c = stack.pop(); comp.append(c)
        for dx in range(-3, 4):
            for dy in range(-3, 4):
                q = (c[0] + dx, c[1] + dy)
                if q in pix and q not in seen:
                    seen.add(q); stack.append(q)
    comps.append(comp)
comp_out = []
for comp in comps:
    xs = [c[0] for c in comp]; ys = [c[1] for c in comp]
    comp_out.append({"cols": [min(xs), max(xs)], "rows": [min(ys), max(ys)], "px": len(comp)})
comp_out.sort(key=lambda d: (d["rows"][0], d["cols"][0]))
rep["orig_calc_red_clusters"] = comp_out

# ---------- 2. arrow census cols 425..508 per box (both images) ----------
def ink_cols(img, px, rows, x0, x1, thresh=150):
    cols = []
    for x in range(x0, x1):
        n = sum(1 for y in rows if px[x, y] < thresh)
        if n >= 2: cols.append(x)
    out = []
    if cols:
        s = p = cols[0]
        for x in cols[1:]:
            if x <= p + 2: p = x
            else: out.append([s, p]); s = p = x
        out.append([s, p])
    return out

arrow = []
for i, (t, b) in enumerate(BOXES):
    mid = range(t + 8, b - 8)
    arrow.append({"box": i + 1,
                  "orig_cols_425_508": ink_cols(OG, OP, mid, 425, 509),
                  "render_cols_425_508": ink_cols(RG, RP, range(int((t + 8) * S), int((b - 8) * S)),
                                                   int(425 * S), int(509 * S))})
rep["arrow_col_census"] = arrow

# ---------- 3. ASCII dump of original box-1 right expression ----------
def ascii_dump(img, x0, x1, y0, y1, redmark=True):
    lines = []
    for y in range(y0, y1):
        s = ""
        for x in range(x0, x1):
            p = img.getpixel((x, y))
            if img.mode == "L":
                v = p
                s += "#" if v < 100 else ("+" if v < 180 else ".")
            else:
                if is_red(p): s += "R"
                elif is_green(p): s += "G"
                elif is_blue(p): s += "B"
                else:
                    v = sum(p) / 3
                    s += "#" if v < 100 else ("+" if v < 180 else ".")
        lines.append(f"{y:3d} {s}")
    return lines

rep["orig_box1_right_ascii"] = ascii_dump(ORIG, 640, 810, 145, 195)
rep["render_box1_right_ascii"] = ascii_dump(
    REND, int(640 * S), int(810 * S), int(145 * S), int(195 * S))

# ---------- 4. render C1 red re-verify (top-left input table class row) ----------
def redcount(img, x0, x1, y0, y1):
    n = 0
    for y in range(y0, y1):
        for x in range(x0, x1):
            if is_red(img.getpixel((x, y))): n += 1
    return n
rep["render_input_C1_row_red_px"] = redcount(REND, int(85 * S), int(140 * S), int(108 * S), int(126 * S))
rep["orig_input_C1_row_red_px"] = redcount(ORIG, 85, 140, 108, 126)
rep["render_aug_C1_row_red_px"] = redcount(REND, int(85 * S), int(140 * S), int(228 * S), int(245 * S))
rep["orig_aug_C1_row_red_px"] = redcount(ORIG, 85, 140, 228, 245)

with open(f"{ROOT}/scratch/tmp/adjudicate_048_fresh3_out.json", "w") as f:
    json.dump(rep, f, indent=1)
print(json.dumps({k: v for k, v in rep.items() if not k.endswith("ascii")}, indent=1))
print("=== ORIG BOX1 RIGHT ASCII (cols 640..810, rows 145..195) ===")
print("\n".join(rep["orig_box1_right_ascii"]))
