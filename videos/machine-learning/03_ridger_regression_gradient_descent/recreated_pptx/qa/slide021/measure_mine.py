#!/usr/bin/env python3
"""measure_mine.py — Clean geometry/color measurement for slide 021 build.
Frame px, 1px = 1pt = 1/72in. Output feeds build/slide_021.js.
"""
from PIL import Image
import numpy as np

F = "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_021.jpg"
im = Image.open(F).convert("RGB")
a = np.asarray(im).astype(int)
r, g, b = a[..., 0], a[..., 1], a[..., 2]

# Color masks
blue = (b > 120) & (b - r > 60) & (b - g > 60)   # panel borders, arrows
red  = (r > 100) & (r - g > 60) & (r - b > 60)    # title, red labels, red conclusions
green = (g > 100) & (g - r > 50) & (g - b > 50)   # λ=3
yellow = (r > 170) & (g > 170) & (b < 150)        # badge fill, table diagonal highlights
dark = (r < 110) & (g < 110) & (b < 110)          # black text, gridlines
ink = (r < 215) | (g < 215) | (b < 215)           # any non-white

def bbox(mask, x0, y0, x1, y1):
    """Return (xmin, ymin, xmax, ymax) in frame px within the window."""
    sub = mask[y0:y1+1, x0:x1+1]
    ys, xs = np.where(sub)
    if not len(ys):
        return None
    return (xs.min() + x0, ys.min() + y0, xs.max() + x0, ys.max() + y0)

def core(mask, x0, y0, x1, y1, n=8):
    """Median color of darkest n pixels in the window."""
    sub = mask[y0:y1+1, x0:x1+1]
    ys, xs = np.where(sub)
    if not len(ys):
        return None
    pts = a[ys + y0, xs + x0]
    srt = pts[np.argsort(pts.sum(axis=1))][:n]
    return tuple(np.median(srt, axis=0).astype(int))

def runs(vec):
    out = []; s = None
    for i, v in enumerate(vec):
        if v and s is None: s = i
        elif not v and s is not None: out.append((s, i-1)); s = None
    if s is not None: out.append((s, len(vec)-1))
    return out

print("=== 1. TITLE (red ink) ===")
# Title is dark red #8B0000 → JPEG-darkened ~C00000 family
# Exclude badge area (x>830)
t = red.copy()
t[:, 830:] = False
t[:, :200] = False
t[:60, :] = False
t[110:, :] = False
ys, xs = np.where(t)
if len(xs):
    print(f" title red ink bbox: x {xs.min()}..{xs.max()} y {ys.min()}..{ys.max()} (w {xs.max()-xs.min()+1}, h {ys.max()-ys.min()+1})")
    # Row runs
    for y in range(ys.min(), ys.max()+1):
        rr = runs(t[y])
        cl = []
        for s, e in rr:
            if e - s >= 3:
                if cl and s - cl[-1][1] <= 12: cl[-1] = (cl[-1][0], e)
                else: cl.append((s, e))
        if cl:
            print(f"   y={y}: {cl}")
    # Cap height: first/last rows with >=20 red px
    rows = [y for y in range(ys.min(), ys.max()+1) if t[y].sum() >= 20]
    print(f" title cap-height rows: {rows[0]}..{rows[-1]} (h={rows[-1]-rows[0]+1})")
    print(f" title darkest core: {core(t, 0, 0, 959, 539, 6)}")
    # Ink center
    cx = (xs.min() + xs.max()) / 2
    cy = (ys.min() + ys.max()) / 2
    print(f" title ink center: ({cx:.1f}, {cy:.1f})")

print("\n=== 2. PANEL OUTLINES (blue) ===")
# Scan for panel border positions manually
print(" blue horizontal lines (row, x-range):")
for y in range(120, 530, 5):
    rr = runs(blue[y, 50:900])
    long = [(s+50, e+50) for s,e in rr if e-s >= 100]
    if long:
        print(f"   y={y}: {long}")
print(" blue vertical lines (col, y-range):")
for x in [55, 880]:
    col = blue[120:530, x]
    rr = runs(col)
    long = [(s+120, e+120) for s,e in rr if e-s >= 50]
    if long:
        print(f"   x={x}: {long}")

# Panel borders: look for large horizontal/vertical bands at y~140, 280, 420, x~50..880
# Measure panel fill interior color (sample away from borders)
print("\n panel interior samples:")
# Top panel interior: x~150..800, y~150..220
print(f"  P1 interior x300 y160: {tuple(a[160, 300])}")
print(f"  P1 left border x60 y160: {tuple(a[160, 60])}")
print(f"  P1 right border x880 y160: {tuple(a[160, 880])}")
# Middle panel
print(f"  P2 interior x300 y300: {tuple(a[300, 300])}")
print(f"  P2 left border x60 y300: {tuple(a[300, 60])}")
print(f"  P2 right border x880 y300: {tuple(a[300, 880])}")
# Bottom panel
print(f"  P3 interior x300 y480: {tuple(a[480, 300])}")
print(f"  P3 left border x60 y480: {tuple(a[480, 60])}")
print(f"  P3 right border x880 y480: {tuple(a[480, 880])}")
# Blue border core
print(f"  blue border core (P1 left): {core(blue, 50, 130, 80, 230, 8)}")
print(f"  blue border core (P1 right): {core(blue, 850, 130, 880, 230, 8)}")

print("\n=== 3. TABLES (gridlines via dark mask) ===")
# Three tables: top, middle, bottom
# TOP table: x~95..305, y~170..230
print(" TOP TABLE (x95..305, y170..230):")
# Vertical gridlines (columns with long vertical dark runs)
for x in range(95, 306):
    col_dark = dark[170:231, x]
    rr = runs(col_dark)
    for s, e in rr:
        if e - s >= 25:
            core_col = tuple(np.median(a[170+s:170+e+1, x], axis=0).astype(int))
            print(f"   v-grid x={x}: rows {170+s}..{170+e} core {core_col}")
            break
# Horizontal gridlines
for y in range(170, 231):
    row_dark = dark[y, 95:306]
    rr = runs(row_dark)
    for s, e in rr:
        if e - s >= 180:
            core_row = tuple(np.median(a[y, 95+s:95+e+1], axis=0).astype(int))
            print(f"   h-grid y={y}: cols {95+s}..{95+e} core {core_row}")
            break

print("\n MIDDLE TABLE (x85..300, y335..400):")
for x in range(85, 301):
    col_dark = dark[335:401, x]
    rr = runs(col_dark)
    for s, e in rr:
        if e - s >= 25:
            core_col = tuple(np.median(a[335+s:335+e+1, x], axis=0).astype(int))
            print(f"   v-grid x={x}: rows {335+s}..{335+e} core {core_col}")
            break
for y in range(335, 401):
    row_dark = dark[y, 85:301]
    rr = runs(row_dark)
    for s, e in rr:
        if e - s >= 180:
            core_row = tuple(np.median(a[y, 85+s:85+e+1], axis=0).astype(int))
            print(f"   h-grid y={y}: cols {85+s}..{85+e} core {core_row}")
            break

print("\n BOTTOM TABLE (x415..630, y450..515):")
for x in range(415, 631):
    col_dark = dark[450:516, x]
    rr = runs(col_dark)
    for s, e in rr:
        if e - s >= 25:
            core_col = tuple(np.median(a[450+s:450+e+1, x], axis=0).astype(int))
            print(f"   v-grid x={x}: rows {450+s}..{450+e} core {core_col}")
            break
for y in range(450, 516):
    row_dark = dark[y, 415:631]
    rr = runs(row_dark)
    for s, e in rr:
        if e - s >= 180:
            core_row = tuple(np.median(a[y, 415+s:415+e+1], axis=0).astype(int))
            print(f"   h-grid y={y}: cols {415+s}..{415+e} core {core_row}")
            break

print("\n=== 4. PER-CELL DIGIT INK BBOXES (dark) ===")
# From predecessor's cell grids:
cells_top = {
    'cols': [98, 166, 234, 302], 'rows': [174, 191, 209, 226],
    'values': [[14,10,15],[10,40,46],[20,80,92]]
}
cells_mid = {
    'cols': [90, 158, 226, 294], 'rows': [342, 360, 377, 395],
    'values': [[17,10,15],[10,43,46],[20,80,95]]
}
cells_bot = {
    'cols': [422, 490, 558, 625], 'rows': [458, 475, 493, 511],
    'values': [[0.07,0.04,-0.03],[-0.01,0.23,-0.11],[-0.01,-0.2,0.11]]
}

for name, cd in [("top", cells_top), ("mid", cells_mid), ("bot", cells_bot)]:
    print(f" {name}:")
    for ri in range(3):
        for ci in range(3):
            xa, xb = cd['cols'][ci], cd['cols'][ci+1]
            ya, yb = cd['rows'][ri], cd['rows'][ri+1]
            d = dark[ya:yb+1, xa:xb+1]
            ys2, xs2 = np.where(d)
            if len(ys2):
                val = cd['values'][ri][ci]
                print(f"   r{ri+1}c{ci+1} ({val}): x {xs2.min()+xa}..{xs2.max()+xa} y {ys2.min()+ya}..{ys2.max()+ya} n={len(ys2)}")
            else:
                print(f"   r{ri+1}c{ci+1}: NO INK")

print("\n=== 5. MIDDLE TABLE YELLOW HIGHLIGHT (diagonal cells) ===")
# Yellow in diagonal cells (r1c1, r2c2, r3c3)
for ci, (xa, xb) in enumerate(zip(cells_mid['cols'][:-1], cells_mid['cols'][1:])):
    for ri, (ya, yb) in enumerate(zip(cells_mid['rows'][:-1], cells_mid['rows'][1:])):
        if ri == ci:
            sub = yellow[ya:yb+1, xa:xb+1]
            n = int(sub.sum())
            if n > 10:
                ys2, xs2 = np.where(sub)
                c = core(yellow, xa, ya, xb, yb, 12)
                print(f"   cell r{ri+1}c{ci+1}: yellow n={n} bbox x {xs2.min()+xa}..{xs2.max()+xa} y {ys2.min()+ya}..{ys2.max()+ya} core {c}")

print("\n=== 6. CHAIN TEXT + LABELS (ink bboxes + cores) ===")
# Using dark/red/blue/green masks
labels = {
    "top_label_XTX_red":    (red,  90,  120,  130,  165),
    "top_chain_eq0_red":    (red,  320, 340,  175,  225),
    "top_chain_eq0_dark":   (dark, 340, 380,  175,  225),
    "top_chain_singular":   (dark, 460, 600,  175,  225),
    "top_chain_noinv_red":  (red,  680, 800,  175,  225),
    "mid_label_paren_red":  (red,  85,  120,  290,  335),
    "mid_label_plus_dark":  (dark, 145, 175,  290,  335),
    "mid_label_lambda_blue":(blue, 175, 220,  290,  335),
    "mid_label_lambda3_grn":(green,240, 300,  285,  325),
    "mid_chain_eq5685_red": (red,  320, 350,  340,  390),
    "mid_chain_eq5685_dark":(dark, 350, 430,  340,  390),
    "mid_chain_nonsing":    (dark, 480, 680,  340,  390),
    "mid_chain_invex_red":  (red,  720, 880,  340,  390),
    "bot_expr_paren_red":   (red,  140, 220,  450,  510),
    "bot_expr_plus_dark":   (dark, 210, 235,  450,  510),
    "bot_expr_lambda_blue": (blue, 235, 300,  450,  510),
    "bot_expr_sup_dark":    (dark, 300, 330,  450,  510),
}
for name, (mask, x0, x1, y0, y1) in labels.items():
    b = bbox(mask, x0, y0, x1, y1)
    c = core(mask, x0, y0, x1, y1, 6)
    print(f" {name}: bbox={b} core={c}")

# Dark parens (not covered by red/blue)
parens = {
    "mid_label_parens_dark":  (85, 220, 290, 335),
    "bot_expr_parens_sup":    (140, 330, 450, 510),
}
for name, (x0, x1, y0, y1) in parens.items():
    b = bbox(dark, x0, y0, x1, y1)
    c = core(dark, x0, y0, x1, y1, 6)
    print(f" {name}: bbox={b} core={c}")

print("\n=== 7. ARROWS (dark/blue) ===")
# Top arrows: between eq0 and Singular, between Singular and No Inverse
# Mid arrows: between eq5685 and Non-Singular, between Non-Singular and Inverse Exists
# Bottom arrow: long from expression to inverse table
arrows = {
    "top_arrow1": (dark, 430, 470, 185, 220),
    "top_arrow2": (dark, 610, 650, 185, 220),
    "mid_arrow1": (dark, 450, 490, 355, 380),
    "mid_arrow2": (dark, 680, 720, 355, 380),
    "bot_arrow":  (dark, 310, 410, 465, 495),
}
for name, (mask, x0, x1, y0, y1) in arrows.items():
    b = bbox(mask, x0, y0, x1, y1)
    c = core(mask, x0, y0, x1, y1, 8)
    print(f" {name}: bbox={b} core={c}")

print("\n=== 8. BADGE ===")
by, bx = np.where(yellow[55:95, 850:900])
if len(by):
    print(f" badge yellow px: n={len(by)} bbox x {bx.min()+850}..{bx.max()+850} y {by.min()+55}..{by.max()+55}")
d = dark[55:95, 850:900]
ys2, xs2 = np.where(d)
if len(ys2):
    print(f" badge numeral dark ink: x {xs2.min()+850}..{xs2.max()+850} y {ys2.min()+55}..{ys2.max()+55}")

print("\n=== 9. FONT PROBE — serif check (terminals) ===")
# Sample a few glyphs at high resolution
def ascii_map(x0, x1, y0, y1, label):
    print(f" -- {label} (x{x0}..{x1}, y{y0}..{y1})")
    for y in range(y0, y1 + 1):
        row = ''.join(
            '#' if dark[y, x] else
            'B' if blue[y, x] else
            'R' if red[y, x] else
            'G' if green[y, x] else
            'Y' if yellow[y, x] else
            '+' if ink[y, x] else '.'
            for x in range(x0, x1 + 1)
        )
        print(f"   {y:3d} {row}")

# Top table r1c2 '10' (should show serif feet on '1' if serif)
ascii_map(166, 190, 174, 191, "top-table r1c2 '10'")
# Top table r2c2 '40'
ascii_map(192, 212, 193, 208, "top-table r2c2 '40'")
# Chain 'Mat' of 'Matrix' at top
ascii_map(570, 600, 190, 212, "chain 'Mat' of 'Matrix'")
# Mid chain '5685'
ascii_map(420, 470, 356, 378, "mid chain '= 5685' digits")
# Bot table r1c1 '0.07'
ascii_map(422, 470, 458, 475, "bot-table r1c1 '0.07'")

print("\n=== 10. KEY COLORS (darkest cores) ===")
print(f" title red: {core(red, 250, 70, 730, 110, 6)}")
print(f" label red: {core(red, 90, 125, 150, 165, 6)}")
print(f" chain red (no inverse): {core(red, 680, 175, 800, 225, 6)}")
print(f" green (λ=3): {core(green, 240, 285, 300, 325, 6)}")
print(f" yellow (diag): {core(yellow, 100, 340, 200, 380, 12)}")
print(f" top-table digits: {core(dark, 120, 175, 300, 225, 6)}")
print(f" bot-table digits: {core(dark, 420, 455, 630, 510, 6)}")
print(f" gridline gray (top h-grid y191): {tuple(np.median(a[191, 100:300], axis=0).astype(int))}")
print(f" gridline gray (bot v-grid x490): {tuple(np.median(a[460:510, 490], axis=0).astype(int))}")
print(f" panel fill (P1 interior): {tuple(a[160, 300])}")
print(f" panel border blue: {core(blue, 50, 130, 80, 230, 8)}")
print(f" arrow blue: {core(blue, 430, 185, 470, 220, 6)}")

print("\n=== 11. PANEL EXACT BOUNDS (blue borders) ===")
# Scan for top-left of each panel
for y in range(120, 180):
    if blue[y, 55]:
        print(f" P1 left border starts y={y} at x=55")
        break
for y in range(120, 180):
    if blue[y, 880]:
        print(f" P1 right border starts y={y} at x=880")
        break
for x in range(55, 900):
    if blue[130, x]:
        print(f" P1 top border at y=130 x={x}")
        break
for x in range(55, 900):
    if blue[230, x]:
        print(f" P1 bottom border at y=230 x={x}")
        break

for y in range(260, 320):
    if blue[y, 55]:
        print(f" P2 left border starts y={y} at x=55")
        break
for y in range(260, 320):
    if blue[y, 880]:
        print(f" P2 right border starts y={y} at x=880")
        break
for x in range(55, 900):
    if blue[270, x]:
        print(f" P2 top border at y=270 x={x}")
        break
for x in range(55, 900):
    if blue[395, x]:
        print(f" P2 bottom border at y=395 x={x}")
        break

for y in range(410, 470):
    if blue[y, 55]:
        print(f" P3 left border starts y={y} at x=55")
        break
for y in range(410, 470):
    if blue[y, 880]:
        print(f" P3 right border starts y={y} at x=880")
        break
for x in range(55, 900):
    if blue[415, x]:
        print(f" P3 top border at y=415 x={x}")
        break
for x in range(55, 900):
    if blue[520, x]:
        print(f" P3 bottom border at y=520 x={x}")
        break

print("\n=== 12. FRAME BACKGROUND SAMPLES ===")
print(f" bg top-left (10,10): {tuple(a[10,10])}")
print(f" bg top-right (940,10): {tuple(a[10,940])}")
print(f" bg center (480,270): {tuple(a[270,480])}")
print(f" bg bottom-left (10,520): {tuple(a[520,10])}")