#!/usr/bin/env python3
"""worker-016-finish-20261024 — independent verification (PIL-first) for slide 016.

Verifies, against unique_slides/slide_016.jpg and the banked renders:
  DEFECT (a) BLOCKER  — 4 of 12 body lines missing (original L7-L10, y332..447,
                        incl. both blue key terms L2/L1 regularization)
  DEFECT (b) MAJOR    — 2nd black underline x675..877 crossing the inner box border x830
  WORDING MAJOR       — attempt-4 judge: original reads "the generalization term",
                        render reads "the regularization term" (glyph-level adjudication)

All coordinates in frame px (960x540, 1px=1pt) unless stated.
"""
import numpy as np
from PIL import Image, ImageDraw, ImageFont

QA = ("/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/"
      "03_ridger_regression_gradient_descent/recreated_pptx/qa/slide016")
ORIG = ("/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/"
        "03_ridger_regression_gradient_descent/unique_slides/slide_016.jpg")
R1 = f"{QA}/render_1.png"      # attempt-1 render (defective baseline)
R4 = f"{QA}/render_4.png"      # current render (= render_3 bytes)
FONT = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"

o = Image.open(ORIG).convert("RGB")
oa = np.asarray(o).astype(int)
r1 = Image.open(R1).convert("RGB"); r1a = np.asarray(r1).astype(int)
r4 = Image.open(R4).convert("RGB"); r4a = np.asarray(r4).astype(int)
S = r4a.shape[0] / 540.0
print(f"original {o.size}  render_1 {r1.size}  render_4 {r4.size}  scale={S:.4f}")


def ink(a):
    return a.min(axis=2) < 160


def clusters(mask, gap=2, min_w=2):
    """column-ink clusters: list of (x0, x1, width)."""
    col = mask.any(axis=0)
    out, x, W = [], 0, mask.shape[1]
    while x < W:
        if col[x]:
            x0 = x
            gaprun = 0
            x1 = x0
            while x < W and (col[x] or gaprun < gap):
                if col[x]:
                    x1 = x
                    gaprun = 0
                else:
                    gaprun += 1
                x += 1
            if x1 - x0 + 1 >= min_w:
                out.append((x0, x1, x1 - x0 + 1))
        else:
            x += 1
    return out


def band_clusters(arr, y0, y1, x0=0, x1=960, gap=2):
    m = ink(arr)[y0:y1, x0:x1]
    return [(a + x0, b + x0, w) for a, b, w in clusters(m, gap=gap)]


def glyph_mask(text, size):
    f = ImageFont.truetype(FONT, size)
    im = Image.new("L", (1400, 120), 0)
    d = ImageDraw.Draw(im)
    d.text((10, 20), text, font=f, fill=255)
    return np.asarray(im) > 0


print("\n" + "=" * 72)
print("DEFECT (a) — MISSING BAND: original L7-L10, frame y332..447, x88..828")
print("=" * 72)
y0, y1, x0, x1 = 332, 447, 88, 828
o_band = int(ink(oa)[y0:y1, x0:x1].sum())
r1_band = int(ink(np.asarray(r1.resize((960, 540), Image.LANCZOS)).astype(int))[y0:y1, x0:x1].sum())
r4_band = int(ink(np.asarray(r4.resize((960, 540), Image.LANCZOS)).astype(int))[y0:y1, x0:x1].sum())
print(f"  original ink px            = {o_band}")
print(f"  render_1 (attempt-1) ink px = {r1_band}   <- the BLOCKER baseline")
print(f"  render_4 (current) ink px   = {r4_band}")
print(f"  FIX VERIFIED: {r4_band > 0.85 * o_band}  (current render carries the band)")
for tag, yb, in [("b3a", (330, 350)), ("b3b", (355, 376)), ("b4a", (406, 426)), ("b4b", (432, 448))]:
    ob = int(ink(oa)[yb[0]:yb[1], x0:x1].sum())
    rb = int(ink(np.asarray(r4.resize((960, 540), Image.LANCZOS)).astype(int))[yb[0]:yb[1], x0:x1].sum())
    print(f"    line {tag}: y{yb}  original {ob} px  render_4 {rb} px")

print("\n  blue key-term spans in the band (colour px, native render resolution):")
low = np.asarray(r4.resize((960, 540), Image.LANCZOS)).astype(int)
blue = (low[:, :, 2].astype(int) - low[:, :, 0].astype(int) > 60) & (low[:, :, 2] > 100)
for name, ya, yb, xa, xb in [("L2 regularization (b3b)", 355, 376, 250, 395),
                             ("L1 regularization (b4b)", 432, 448, 250, 395)]:
    print(f"    {name}: render blue px = {int(blue[ya:yb, xa:xb].sum())}  at x{xa}..{xb} y{ya}..{yb}")

print("\n" + "=" * 72)
print("DEFECT (b) — UNDERLINE CROSSING THE INNER BOX BORDER (x830)")
print("=" * 72)
print("  inner box border: original x82..83 / x832..833; render x82..83 / x832..833 (selfcheck_4)")
for tag, path, arr in [("render_1", R1, None), ("render_4", R4, None)]:
    f = np.asarray(Image.open(path).resize((960, 540), Image.LANCZOS)).astype(int)
    b = f.min(axis=2) < 100          # dark strokes only
    rows = [y for y in range(495, 535) if b[y, 100:830].sum() > 40]
    for y in rows:
        cols = np.where(b[y, 95:900])[0] + 95
        # split into runs
        runs, start, prev = [], cols[0], cols[0]
        for c in cols[1:]:
            if c - prev > 3:
                runs.append((start, prev))
                start = c
            prev = c
        runs.append((start, prev))
        wide = [(a, b2) for a, b2 in runs if b2 - a > 20]
        crosses = any(b2 >= 830 for a, b2 in wide)
        print(f"    {tag} y={y}: wide dark runs (x>20px): {wide}"
              + ("   <-- CROSSES BOX BORDER x830 (DEFECT)" if crosses else ""))
print("  red underline under 'customized weigh factor' (original x110..300, y296..297):")
f4 = np.asarray(Image.open(R4).resize((960, 540), Image.LANCZOS)).astype(int)
red = (f4[:, :, 0].astype(int) - f4[:, :, 1].astype(int) > 60) & (f4[:, :, 0] > 120)
m = red[294:299, 100:320]
cols = np.where(m.any(axis=0))[0] + 100
print(f"    render_4 red underline x{cols.min()}..{cols.max()} y294..298 "
      f"({'inside original extent 110..300' if cols.max() <= 305 else 'OUTSIDE'})")
print("  dark underline under 'Length' (original x109..163, y525):")
d = f4.min(axis=2) < 100
m = d[523:528, 100:260]
cols = np.where(m.any(axis=0))[0] + 100
print(f"    render_4 dark underline x{cols.min()}..{cols.max()} y523..527 "
      f"({'matches original 109..163' if abs(cols.min()-109) <= 3 and abs(cols.max()-163) <= 3 else 'DEVIATES'})")

print("\n" + "=" * 72)
print("WORDING — attempt-4 MAJOR: original b2b 'regularization term' or 'generalization term'?")
print("=" * 72)
# b2b band in both images, frame px
yb0, yb1 = 254, 276
o_cl = band_clusters(oa, yb0, yb1, 100, 770, gap=2)
r_cl = band_clusters(np.asarray(Image.open(R4).resize((960, 540), Image.LANCZOS)).astype(int),
                     yb0, yb1, 100, 770, gap=2)
print("  original b2b clusters:", o_cl)
print("  render_4 b2b clusters:", r_cl)

# synthesize candidate word widths at a size calibrated on the agreed first word
# original first cluster (generalization,) vs render's
o_first = o_cl[0]; r_first = r_cl[0]
print(f"\n  calibration: first cluster original x{o_first[0]}..{o_first[1]} w={o_first[2]}"
      f" | render x{r_first[0]}..{r_first[1]} w={r_first[2]}")
w_gen = glyph_mask("generalization", 18).sum(axis=0)
wnz = np.where(w_gen)[0]
print(f"  synth 'generalization' @18px em: w={wnz.max()-wnz.min()+1}")
for w in ("the", "regularization", "generalization", "term", "is", "added"):
    m = glyph_mask(w, 18)
    c = np.where(m.any(axis=0))[0]
    print(f"    synth {w!r:18} w = {c.max()-c.min()+1}")

# disputed word: the 3rd cluster of the original line (after 'generalization,' and 'the')
if len(o_cl) >= 3:
    a, b, w = o_cl[2]
    print(f"\n  DISPUTED WORD cluster: original x{a}..{b} w={w} (frame px)")
    # render's corresponding cluster: match by rank — render line starts identically
    print(f"  (render clusters for mapping: {r_cl})")
    size_ok = None
    # scale synthesis to the original's measured first word
    first_w_synth = np.where(glyph_mask('generalization', 18).any(axis=0))[0]
    fs = first_w_synth.max() - first_w_synth.min() + 1
    scale = o_first[2] / fs
    print(f"  synthesis scale from first word: {scale:.4f} (orig first {o_first[2]} / synth {fs})")
    for cand in ("regularization", "generalization"):
        m = glyph_mask(cand, 18)
        c = np.where(m.any(axis=0))[0]
        pred = (c.max() - c.min() + 1) * scale
        err = abs(pred - w)
        print(f"    {cand:18} predicted at original scale = {pred:6.1f} px  | measured {w} | err {err:5.1f}")
print("\nVERIFICATION SCRIPT COMPLETE")
