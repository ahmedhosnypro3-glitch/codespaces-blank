#!/usr/bin/env python3
"""Render the slide-036 box-3 equation asset (attempt 8) — PIL composite at 600 dpi.

Why a new renderer: the attempt-7 asset (scratch/tmp/eq036_v4.py) carried four
crop-leg defects, all measured against the ORIGINAL frame
(unique_slides/slide_036.jpg, 960x540, 1 frame px = 1 pt = 72 dpi):

  1. UNMATCHED OPENING PAREN in the first term — v4 emitted "(W" at x=304 while
     the original has W ink at x=304 (no parens on the first term; its closing
     paren was dropped in v4 but the opening one was left behind).
  2. LITERAL UNDERSCORE SUBSCRIPT — v4 emitted the string "_i", so the render
     showed "X_i" (underscore + baseline i) instead of a raised/lowered
     subscript. Founder math rule: subscripts must be spatially aligned, never
     caret/underscore text.
  3. NO GAP BEFORE "take" — the second group's ")" ended at frame x=499 and the
     phrase ink started at 502 (original: ")" at 496..498, phrase at 507).
  4. SUMMATION LIMIT UNCOLORED — the original's limit is italic with
     "misclassified" and "(i)" in red; v4 drew it black upright at 12pt.

Measured original targets (frame px, this script prints the same census for the
rendered canvas so the two can be compared line by line):
  "Error ="        ink x 84..151   baseline 390
  Sigma            ink x 220..239  y 369..396
  limit            ink x 162..297  baseline 411  (red: "misclassified", "(i)")
  term1            W 304..322, T 322..332 (raised), X 338..350 (green),
                   i 354..356 (lowered, red)
  arrow "=>"       ink x 396..410
  term2            ( 445..446, W 451..464, T 468..473, X 478..487,
                   i 490..492 (lowered, red), ) 496..498
  phrase           ink x 507..733  baseline 393 (italic narrow)

Output: build/assets/eq_036_error.png (tight crop + 3 device px pad, transparent)
        + build/assets/eq_036_error.json sidecar
"""
import json

import numpy as np
from PIL import Image, ImageDraw, ImageFont

V = "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
OUT_PNG = f"{V}/recreated_pptx/build/assets/eq_036_error.png"
OUT_JSON = f"{V}/recreated_pptx/build/assets/eq_036_error.json"
ORIG = f"{V}/unique_slides/slide_036.jpg"

DPI = 600
SC = DPI / 72.0                      # device px per frame px
FD = "/usr/share/fonts/truetype/liberation"
SANS = f"{FD}/LiberationSans-Regular.ttf"
SANS_I = f"{FD}/LiberationSans-Italic.ttf"
NARROW_I = f"{FD}/LiberationSansNarrow-Italic.ttf"
DEJAVU = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

RED = (192, 0, 0, 255)               # C00000, the deck's red
GREEN = (0, 128, 0, 255)             # 008000
BLACK = (0, 0, 0, 255)

# frame-px canvas (room for the whole equation row)
FX0, FY0, FX1, FY1 = 70, 360, 760, 425
CW, CH = int((FX1 - FX0) * SC), int((FY1 - FY0) * SC)
canvas = Image.new("RGBA", (CW, CH), (0, 0, 0, 0))
draw = ImageDraw.Draw(canvas)


def font(path, pt):
    return ImageFont.truetype(path, max(1, int(round(pt * SC))))


def dev(x_frame, y_frame):
    return ((x_frame - FX0) * SC, (y_frame - FY0) * SC)


def measure(text, fpath, pt):
    """Ink bbox size (device px) of `text` drawn with anchor 'ls'."""
    f = font(fpath, pt)
    tmp = Image.new("RGBA", (6000, 1000), (0, 0, 0, 0))
    ImageDraw.Draw(tmp).text((300, 700), text, font=f, fill=BLACK, anchor="ls")
    bb = tmp.getbbox()
    return bb[2] - bb[0], bb[3] - bb[1], bb


def solve_pt(text, fpath, target_frame_w, lo=6.0, hi=60.0):
    """Font pt whose ink width == target_frame_w frame px (bounded search)."""
    best = None
    pt = lo
    while pt <= hi:
        w, h, _ = measure(text, fpath, pt)
        err = abs(w - target_frame_w * SC)
        if best is None or err < best[0]:
            best = (err, pt)
        pt += 0.25
    return best[1]


def draw_ink_left(text, fpath, pt, color, ink_left, baseline):
    """Draw `text` so its INK left edge sits at frame x=ink_left, baseline y."""
    f = font(fpath, pt)
    tmp = Image.new("RGBA", (6000, 1000), (0, 0, 0, 0))
    ImageDraw.Draw(tmp).text((300, 700), text, font=f, fill=color, anchor="ls")
    bb = tmp.getbbox()
    dx, dy = dev(ink_left, baseline)   # target ink-left / baseline on the canvas
    draw.text((dx - (bb[0] - 300), dy), text, font=f, fill=color, anchor="ls")
    return f


def draw_run(pieces, ink_left, baseline):
    """Colored run: list of (text, fpath, pt, color); ink left pinned."""
    f0 = font(pieces[0][1], pieces[0][2])
    tmp = Image.new("RGBA", (6000, 1000), (0, 0, 0, 0))
    d = ImageDraw.Draw(tmp)
    x = 300
    for text, fpath, pt, color in pieces:
        d.text((x, 700), text, font=font(fpath, pt), fill=color, anchor="ls")
        x += font(fpath, pt).getlength(text)
    bb = tmp.getbbox()
    dx = dev(ink_left, 0)[0] - (bb[0] - 300)
    x = dx
    for text, fpath, pt, color in pieces:
        f = font(fpath, pt)
        draw.text((x, dev(0, baseline)[1]), text, font=f, fill=color, anchor="ls")
        x += f.getlength(text)


MAIN = 21.0
MAIN_BASE = 390
T_SIZE = 13.0
T_BASE = 379          # raised: original superscript-T ink y 371..379
I_SIZE = 9.0
I_BASE = 394          # lowered subscript baseline (original ink bottom 394)

# --- "Error =" -------------------------------------------------------------
pt_err = solve_pt("Error =", SANS, 151 - 84)
draw_ink_left("Error =", SANS, pt_err, BLACK, 84, MAIN_BASE)
print(f"Error =         size {pt_err:.2f}pt (target ink width {151-84} frame px)")

# --- large Sigma + colored limit ------------------------------------------
pt_sig = 37.5
w, h, _ = measure("\u03a3", SANS, pt_sig)
best = None
pt = 30.0
while pt <= 44.0:
    w, h, _ = measure("\u03a3", SANS, pt)
    err = abs(h - (396 - 369) * SC)
    if best is None or err < best[0]:
        best = (err, pt)
    pt += 0.25
pt_sig = best[1]
draw_ink_left("\u03a3", SANS, pt_sig, BLACK, 220, 396)
print(f"Sigma           size {pt_sig:.2f}pt (target ink height {396-369} frame px)")

limit_pieces = [("all ", SANS_I, 12.0, BLACK),
                ("misclassified", SANS_I, 12.0, RED),
                (" vectors", SANS_I, 12.0, BLACK),
                ("(i)", SANS_I, 12.0, RED)]
# solve the shared limit size on the composite run
best = None
for k in range(80, 160):
    pt_l = k / 8.0
    pieces = [(t, f, pt_l, c) for (t, f, _, c) in limit_pieces]
    f0 = font(SANS_I, pt_l)
    tmp = Image.new("RGBA", (6000, 1000), (0, 0, 0, 0))
    d = ImageDraw.Draw(tmp)
    x = 300
    for t, f, _, c in pieces:
        d.text((x, 700), t, font=font(f, pt_l), fill=c, anchor="ls")
        x += font(f, pt_l).getlength(t)
    bb = tmp.getbbox()
    err = abs((bb[2] - bb[0]) - (297 - 162) * SC)
    if best is None or err < best[0]:
        best = (err, pt_l)
pt_limit = best[1]
draw_run([(t, f, pt_limit, c) for (t, f, _, c) in limit_pieces], 162, 411)
print(f"Sigma limit     size {pt_limit:.2f}pt (target ink width {297-162} frame px)")

# --- term 1: W (no parens) + raised T + green italic X + lowered red i -----
draw_ink_left("W", SANS, MAIN, BLACK, 304, MAIN_BASE)
draw_ink_left("T", SANS, T_SIZE, BLACK, 322, T_BASE)
draw_ink_left("X", SANS_I, MAIN, GREEN, 338, MAIN_BASE)
draw_ink_left("i", SANS_I, I_SIZE, RED, 353, I_BASE)

# --- "=>" ------------------------------------------------------------------
draw_ink_left("\u21d2", DEJAVU, MAIN, BLACK, 396, MAIN_BASE)

# --- term 2: ( W + T + X + i ) --------------------------------------------
draw_ink_left("(", SANS, MAIN, BLACK, 443, MAIN_BASE)
draw_ink_left("W", SANS, MAIN, BLACK, 451, MAIN_BASE)
draw_ink_left("T", SANS, T_SIZE, BLACK, 468, T_BASE)
draw_ink_left("X", SANS_I, MAIN, GREEN, 478, MAIN_BASE)
draw_ink_left("i", SANS_I, I_SIZE, RED, 489, I_BASE)
draw_ink_left(")", SANS, MAIN, BLACK, 494, MAIN_BASE)

# --- trailing phrase: italic narrow, ink x 507..733 --------------
PHRASE = "take positive and negative values"
best = None
for k in range(120, 260):
    pt_p = k / 8.0
    w, h, _ = measure(PHRASE, NARROW_I, pt_p)
    err = abs(w - (733 - 507) * SC)
    if best is None or err < best[0]:
        best = (err, pt_p)
pt_phrase = best[1]
draw_ink_left(PHRASE, NARROW_I, pt_phrase, BLACK, 507, 393)
print(f"phrase          size {pt_phrase:.2f}pt (target ink width {733-507} frame px)")

# --- crop, save, census ----------------------------------------------------
a = np.array(canvas)
ink = a[:, :, 3] > 8
ys, xs = np.where(ink)
y0, y1 = max(ys.min() - 3, 0), min(ys.max() + 4, a.shape[0])
x0, x1 = max(xs.min() - 3, 0), min(xs.max() + 4, a.shape[1])
out = canvas.crop((x0, y0, x1, y1))
out.save(OUT_PNG)
w_px, h_px = out.size
ink_left_frame = FX0 + xs.min() / SC
ink_top_frame = FY0 + ys.min() / SC
ink_right_frame = FX0 + xs.max() / SC
ink_bot_frame = FY0 + ys.max() / SC
print(f"\nPNG {OUT_PNG}  {w_px}x{h_px}px = {w_px/DPI:.5f}x{h_px/DPI:.5f} in")
print(f"ink in frame px: x {ink_left_frame:.1f}..{ink_right_frame:.1f} "
      f"y {ink_top_frame:.1f}..{ink_bot_frame:.1f}")

with open(OUT_JSON, "w") as fh:
    json.dump({
        "rel_id": None,
        "image": "recreated_pptx/build/assets/eq_036_error.png",
        "mathtext": ("Error = \\sum_{all misclassified vectors(i)} W^T X_i "
                     "\\Rightarrow (W^T X_i) take positive and negative values"),
        "font_size_pt": MAIN,
        "color": "000000",
        "w_in": round(w_px / DPI, 5),
        "h_in": round(h_px / DPI, 5),
        "w_px": w_px,
        "h_px": h_px,
        "dpi": DPI,
        "baseline_frac": 0.5,
        "note": ("PIL composite renderer (qa/slide036/eq036_v5.py, attempt 8). "
                 "Sigma display glyph + italic lower limit with red 'misclassified'/'(i)'; "
                 "first term has NO parentheses (matches the frame); X_i uses true lower "
                 "subscripts (no underscore text); raised superscript T; second group "
                 "'(W^T X_i)'; trailing phrase italic narrow pinned to ink x507..733."),
    }, fh, indent=2)

# --- verify the rendered ink census against the original -------------------
orig = np.array(Image.open(ORIG).convert("RGB")).astype(int)


def census(arr, scale, x0f, x1f, y0f, y1f, thr=170):
    sub = arr[int(y0f * scale):int(y1f * scale), int(x0f * scale):int(x1f * scale)]
    lum = sub.mean(axis=2)
    cols = (lum < thr).any(axis=0)
    runs_, i = [], 0
    while i < len(cols):
        if cols[i]:
            j = i
            while j + 1 < len(cols) and cols[j + 1]:
                j += 1
            runs_.append((round(x0f + i / scale), round(x0f + j / scale)))
            i = j + 1
        else:
            i += 1
    merged = []
    for r in runs_:
        if merged and r[0] - merged[-1][1] <= 2:
            merged[-1] = (merged[-1][0], r[1])
        else:
            merged.append(list(r))
    return merged


print("\nmain-band run census (frame px) — orig vs new asset")
print("  orig:", " ".join(f"{a}-{b}" for a, b in census(orig, 1.0, 80, 760, 366, 398)))
new = np.array(Image.open(OUT_PNG).convert("RGBA"))
# map the PNG back to frame space (its left/top edge = ink_left-0.36 etc.)
scale_png = DPI / 72.0
print("  new :", " ".join(
    f"{a}-{b}" for a, b in [
        (round(ink_left_frame - 0.36 + a), round(ink_left_frame - 0.36 + b))
        for a, b in census(new[:, :, :3].astype(int), scale_png, 0,
                           w_px / scale_png, 0, h_px / scale_png)
    ] if False))
# simpler: census the PNG's own frame-space mapping
sub = new[:, :, :3].astype(int)
lum = sub.mean(axis=2)
band = lum[int((366 - (ink_top_frame - 0.36)) * scale_png):
           int((398 - (ink_top_frame - 0.36)) * scale_png), :]
cols = (band < 170).any(axis=0)
runs_, i = [], 0
fx0 = ink_left_frame - 0.36
while i < len(cols):
    if cols[i]:
        j = i
        while j + 1 < len(cols) and cols[j + 1]:
            j += 1
        runs_.append((round(fx0 + i / scale_png), round(fx0 + j / scale_png)))
        i = j + 1
    else:
        i += 1
merged = []
for r in runs_:
    if merged and r[0] - merged[-1][1] <= 2:
        merged[-1] = (merged[-1][0], r[1])
    else:
        merged.append(list(r))
print("  new :", " ".join(f"{a}-{b}" for a, b in merged))
