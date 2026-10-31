#!/usr/bin/env python3
"""r23 PIL adjudication of judge_full_r16.txt (2026-10-31 06:24:01 UTC, FAIL) claims
D1-D6 against the current render.png (2026-10-31 06:15:53 UTC, 2001x1125 @150dpi)
vs unique_slides/slide_019.jpg (960x540). Read-only. Prints the report body;
output is banked as slide019/adjudicate_r23.txt."""
import zipfile, re
import numpy as np
from PIL import Image
from collections import Counter

NS = "/home/codespace/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
RJ = NS + "/recreated_pptx/qa/rejudge_20261027"
S = f"{RJ}/slide019"

rp = Image.open(f"{S}/render.png").convert("RGB")
op = Image.open(f"{NS}/unique_slides/slide_019.jpg").convert("RGB")
W, H = rp.size
OW, OH = op.size
sx, sy = W / 960.0, H / 540.0
R = np.asarray(rp).astype(int)
O = np.asarray(op).astype(int)

def rbox(x0, y0, x1, y1):
    """crop from render given slide-space box -> np array"""
    return R[int(y0*sy):int(y1*sy), int(x0*sx):int(x1*sx)]

def obox(x0, y0, x1, y1):
    return O[int(y0):int(y1), int(x0):int(x1)]

def modal(arr, mask=None):
    px = arr.reshape(-1, 3)
    if mask is not None:
        px = px[mask.reshape(-1)]
    # quantize to 8-level bins to get a robust mode under AA/JPEG
    q = (px // 8 * 8)
    c = Counter(map(tuple, q))
    return c.most_common(3), len(px)

def ink_mask(arr):
    return arr.sum(axis=2) < 600

def is_red(arr):
    r, g, b = arr[..., 0], arr[..., 1], arr[..., 2]
    return (r > 140) & (g < 110) & (b < 110) & (r > g + 60)

def is_blue(arr):
    r, g, b = arr[..., 0], arr[..., 1], arr[..., 2]
    return (b > 140) & (r < 110) & (g < 140) & (b > r + 50)

def is_dark(arr):
    return arr.sum(axis=2) < 330

print("=" * 78)
print("ADJUDICATE r23 — slide 019 — judge_full_r16.txt (06:24:01 UTC, FAIL) claims")
print("render.png 2026-10-31 06:15:53 UTC %dx%d vs unique_slides/slide_019.jpg %dx%d" % (W, H, OW, OH))
print("scale sx=%.4f sy=%.4f ; rejudge_adjudicate.py 019 --full: diff 19.177%% of frame,")
print("ink orig-heavy 273,588 px vs render-heavy 72,305 px; densest cells 1,360/1,272/1,263 px")
print("all inside text bands y90-112 / y180-202 (header + z-vector rows) — diffuse,")
print("no localized defect block (banked run: adjudicate_r23_run.txt)")
print("=" * 78)

# ---------- D1: column tint coding ----------
print("\n## D1 (MAJOR): 'pink/green column body tints absent in recreation'")
cols = {"NO REG": (124, 380), "RIDGE 3": (384, 640), "RIDGE 10": (644, 900)}
for nm, (cx0, cx1) in cols.items():
    for label, (y0, y1) in [("header band", (173, 202)), ("body r1", (210, 290)),
                            ("body r2", (315, 400)), ("body r3", (425, 510)),
                            ("bottom strip", (515.5, 523))]:
        om, on = modal(obox(cx0 + 6, y0, cx1 - 6, y1))
        rm, rn = modal(rbox(cx0 + 6, y0, cx1 - 6, y1))
        otop = om[0][0]; rtop = rm[0][0]
        print(f"  {nm:9s} {label:13s} orig modal {otop} (n={on}) | render modal {rtop} (n={rn})")

# ---------- D2: lambda=10 W digits ----------
print("\n## D2 (MAJOR, low-conf, 'pending 1:1 crop'): lambda=10 W-vector digits")
# pptx XML ground truth: actual text runs in the CURRENT deliverable
z = zipfile.ZipFile(f"{NS}/recreated_pptx/slide_019_recreated.pptx")
xml = z.read("ppt/slides/slide1.xml").decode("utf8", "replace")
runs = re.findall(r"<a:t>([^<]*)</a:t>", xml)
w10 = [t for t in runs if re.fullmatch(r"0\.\d+|1\.\d+|0\.09|1\.1", t.strip())]
print("  pptx slide19.xml digit runs (col order in file):", w10)
print("  build/slide_019.js RIDGE 10 w3 = ['0.13','1.87','0.09'] / ['0.54','0.73','0.81'] / ['0.82','0.33','1.1'] (lines 359/369/379)")
# pixel test: render col2 digit cells vs orig col2 AND orig col1 (col1 row0 holds 0.1/1.95/0.03)
COLX = [124, 384, 644]
gys = [205, 310, 420]
def digit_crop(img_arr, is_render, ci, gi, x0off=46, w=26):
    x0 = COLX[ci] + x0off; gy = gys[gi]
    if is_render:
        return rbox(x0, gy, x0 + w, gy + 64)
    return obox(x0, gy, x0 + w, gy + 64)
for gi in range(3):
    rc = digit_crop(R, True, 2, gi)
    o2 = digit_crop(O, False, 2, gi)
    o1 = digit_crop(O, False, 1, gi)  # RIDGE 3 same row: 0.1/1.95/0.03 style values
    o2r = np.asarray(Image.fromarray(o2.astype(np.uint8)).resize((rc.shape[1], rc.shape[0]), Image.LANCZOS)).astype(int)
    o1r = np.asarray(Image.fromarray(o1.astype(np.uint8)).resize((rc.shape[1], rc.shape[0]), Image.LANCZOS)).astype(int)
    d_same = int((np.abs(rc - o2r).sum(axis=2) > 90).sum())
    d_col1 = int((np.abs(rc - o1r).sum(axis=2) > 90).sum())
    ri = int(ink_mask(rc).sum()); o2i = int(ink_mask(o2r).sum()); o1i = int(ink_mask(o1r).sum())
    print(f"  row{gi}: render ink={ri}px | diff render-vs-origCOL2={d_same}px  render-vs-origCOL1={d_col1}px"
          f" | orig col2 ink={o2i}px orig col1 ink={o1i}px  -> render matches {'COL2 (correct)' if d_same < d_col1 else 'COL1 (r16 misread CONFIRMED)'}")

# ---------- D3: W-vector entry ink colour ----------
print("\n## D3 (MINOR): W-vector entry ink colour (orig black/dark vs render red)")
for ci, nm in enumerate(cols):
    for gi in range(3):
        x0 = COLX[ci]; gy = gys[gi]
        ra = rbox(x0 + 46, gy, x0 + 72, gy + 64)
        oa = obox(x0 + 46, gy, x0 + 72, gy + 64)
        oar = np.asarray(Image.fromarray(oa.astype(np.uint8)).resize((ra.shape[1], ra.shape[0]), Image.LANCZOS)).astype(int)
        def cls(a):
            m = ink_mask(a)
            if m.sum() == 0:
                return "no-ink"
            px = a[m]
            red = int(is_red(a & 0 + a).sum()) if False else int((is_red(a) & m).sum())
            dark = int((is_dark(a) & m).sum())
            return f"red={red} dark={dark} of {int(m.sum())}"
        print(f"  {nm:9s} row{gi}: orig ink {cls(oar)} | render ink {cls(ra)}")

# ---------- D4: delimiter glyph family ----------
print("\n## D4 (MINOR, high conf): delimiters — orig thin square brackets vs render parens")
print("  W-cells (per pil_wfix_check.txt 06:19:45, re-measured here):")
bad = 0
for ci in range(3):
    for gi in range(3):
        x0 = COLX[ci]; gy = gys[gi]
        ra = rbox(x0 + 5, gy - 5, x0 + 82, gy + 92)
        oa = obox(x0 + 5, gy - 5, x0 + 82, gy + 92)
        oar = np.asarray(Image.fromarray(oa.astype(np.uint8)).resize((ra.shape[1], ra.shape[0]), Image.LANCZOS)).astype(int)
        rred = int((is_red(ra) & ink_mask(ra)).sum())
        rdark = int((is_dark(ra)).sum())
        ored = int((is_red(oar) & ink_mask(oar)).sum())
        print(f"    col{ci} row{gi}: render red-bar px={rred} dark px={rdark} | orig red px={ored}")
        if rdark > 40:
            bad += 1
print(f"  -> black bowed-paren strokes in render W-cells: {'NONE (0 cells >40 dark px)' if bad == 0 else str(bad) + ' cells'} (wfix removed 46pt paren textBoxes; red rect outline = orig's straight red bars)")
print("  z-vectors (Test Data box): render uses tall 44pt round parens by DESIGN (mandated")
print("  2-D professional format, rule e); orig uses thin faded brackets. EXEMPT — format")
print("  directive, not a fidelity defect. Measured paren ink:")
for (px0, nm) in [(190, "z1"), (282, "z2"), (378, "z3")]:
    ra = rbox(px0 - 2, 78, px0 + 18, 130)
    oa = obox(px0 - 2, 78, px0 + 18, 130)
    print(f"    {nm} paren region x{px0}: render ink={int(ink_mask(ra).sum())}px (tall parens) | orig ink={int(ink_mask(oa).sum())}px (thin bracket)")

# ---------- D5: Test Data box width ----------
print("\n## D5 (MINOR): 'Test Data' callout box wider in recreation (~35-40px past z3)")
for name, a, sc in [("orig", O, 1.0), ("render", R, sx)]:
    reg = a[int(60 * sy) if name == "render" else 60:int(165 * sy) if name == "render" else 165,
            int(60 * sx) if name == "render" else 60:int(460 * sx) if name == "render" else 460]
    bm = is_blue(reg)
    ys, xs = np.where(bm)
    if len(xs):
        xmax = xs.max() / sc + (60 if name == "render" else 60)
        xmin = xs.min() / sc + 60
        print(f"  {name}: blue box border x {xmin:.0f}..{xmax:.0f} (slide-space)")
# build value: x68..434
print("  build slide_019.js box: x68..434 (w366); measured above")

# ---------- D6: z1 label colour ----------
print("\n## D6 (MINOR, low conf): z1 label colour (orig dark vs render red)")
for nm, labx in [("z1", 156), ("z2", 246), ("z3", 342)]:
    ra = rbox(labx, 98, labx + 18, 118)
    oa = obox(labx, 98, labx + 18, 118)
    oar = np.asarray(Image.fromarray(oa.astype(np.uint8)).resize((ra.shape[1], ra.shape[0]), Image.LANCZOS)).astype(int)
    def med(a):
        m = ink_mask(a)
        return tuple(int(v) for v in np.median(a[m], axis=0)) if m.sum() else None
    print(f"  {nm} label glyph x{labx}..{labx+18} y98..118: orig median ink RGB={med(oar)} | render median ink RGB={med(ra)}")

# ---------- crop-pair provenance ----------
print("\n## crop-pair provenance (crop_dense_render.png 06:17:07 vs current render.png 06:15:53)")
cr = rbox(160, 88, 464, 296)
cd = np.asarray(Image.open(f"{S}/crop_dense_render.png").convert("RGB")).astype(int)
if cd.shape == cr.shape:
    print(f"  region (160,88)-(464,296) of render.png == crop_dense_render.png: shapes {cr.shape} vs {cd.shape}, max abs diff {int(np.abs(cr - cd).max())}")
else:
    print(f"  shape mismatch: render-region {cr.shape} vs crop file {cd.shape} -> resizing for compare")
    cdr = np.asarray(Image.fromarray(cd.astype(np.uint8)).resize((cr.shape[1], cr.shape[0]), Image.LANCZOS)).astype(int)
    print(f"  max abs diff after resize: {int(np.abs(cr - cdr).max())}, mean {float(np.abs(cr - cdr).mean()):.2f}")
