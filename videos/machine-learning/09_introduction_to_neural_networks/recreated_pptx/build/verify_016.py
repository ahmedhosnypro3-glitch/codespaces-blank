#!/usr/bin/env python3
"""verify_016.py - measurement-based check of the slide 016 recreation.

Original frame is 960x540 (1 px = 1 pt on the 13.33x7.5in build canvas); the render
is 2001x1125 @150dpi (1 render px = 0.48 pt). All deltas are reported in ORIGINAL
frame px. Targets are measured from unique_slides/slide_016.jpg with PIL.

House chrome (frame rect, badge, title box position) is asserted against the founder's
house frame rule, NOT against the original - the house rule overrides judge findings.
Text positions are compared against the house-centred expectation (the house title box
centres the block at 479.9px, the original centred its text at 500px).
"""
from PIL import Image
import numpy as np

V = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks"
REND = f"{V}/recreated_pptx/build/slide_016_rejudge_rendered-1.png"
ORIG = f"{V}/unique_slides/slide_016.jpg"

TOL = 4.0  # original-frame px
HOUSE_CX = (0.6 + 12.13 / 2) * 72  # 479.9 px - house title box centre

r = np.asarray(Image.open(REND).convert("RGB")).astype(int)
o = np.asarray(Image.open(ORIG).convert("RGB")).astype(int)
H, W = r.shape[:2]
SC = W / 13.33 / 72.0  # render px per pt
print(f"recreation render {W}x{H} @150dpi ; px/pt={SC:.4f} ; original frame {o.shape[1]}x{o.shape[0]}")
print(f"(1 original px = 1 pt on the build canvas)")

fails = []


def check(name, got, want, tol=TOL, unit="px"):
    ok = abs(got - want) <= tol
    print(f"  [{'OK ' if ok else 'FAIL'}] {name:<44} got {got:8.2f}{unit}  want {want:8.2f}{unit}"
          f"  (delta {got - want:+.2f}{unit})")
    if not ok:
        fails.append(f"{name}: got {got:.2f}, want {want:.2f} (tol {tol})")
    return ok


def to_orig_px(v, axis):
    """Convert a render px coordinate to original-frame px."""
    return v * (960.0 / W if axis == "x" else 540.0 / H)


# ---------- HOUSE FRAME RULE (overrides judge findings) ----------
print("\n-- house chrome, asserted against the house frame rule --")
bg = (r[..., 0] == 0xE8) & (r[..., 1] == 0xE8) & (r[..., 2] == 0xE8)
print(f"  background #E8E8E8: {int(bg.sum())} px")
if int(bg.sum()) < 100000:
    fails.append("background is not #E8E8E8")

fc = (r[..., 0] == 0xC0) & (r[..., 1] == 0) & (r[..., 2] == 0)
fr_v = np.where(fc.sum(axis=0) > 0.4 * H)[0]
fr_h = np.where(fc.sum(axis=1) > 0.4 * W)[0]
print(f"  #C00000 outer frame verts x(in) {[round(x / SC / 72, 3) for x in fr_v[:1]]}"
      f"..{[round(x / SC / 72, 3) for x in fr_v[-1:]]}"
      f" ; horiz y(in) {[round(y / SC / 72, 3) for y in fr_h[:1]]}"
      f"..{[round(y / SC / 72, 3) for y in fr_h[-1:]]}")
if len(fr_v) < 2 or len(fr_h) < 2:
    fails.append("house red frame lines missing/incomplete")
# frame line is 1.5pt wide centred on the 0.15in path -> ink spans 10.05..11.55pt
check("frame left ink edge (0.15in = 10.8pt)", to_orig_px(fr_v[0], "x"), 10.8, tol=1.6)
check("frame top ink edge  (0.15in = 10.8pt)", to_orig_px(fr_h[0], "y"), 10.8, tol=1.6)
check("frame right ink edge (0.15+13.03 = 13.18in = 948.9pt)",
      to_orig_px(fr_v[-1], "x"), 948.9, tol=1.6)

badge = (r[..., 0] == 0xFF) & (r[..., 1] == 0xF9) & (r[..., 2] == 0xC4)
bys, bxs = np.where(badge)
print(f"  badge #FFF9C4 oval ink bbox x {round(bxs.min() / SC / 72, 3)}..{round(bxs.max() / SC / 72, 3)} in"
      f" x y {round(bys.min() / SC / 72, 3)}..{round(bys.max() / SC / 72, 3)} in")
check("badge oval left x (in)", bxs.min() / SC / 72, 12.48, tol=0.05, unit="in")
check("badge oval top y (in)", bys.min() / SC / 72, 0.30, tol=0.05, unit="in")
check("badge oval width (in)", (bxs.max() - bxs.min() + 1) / SC / 72, 0.50, tol=0.06, unit="in")
check("badge oval height (in)", (bys.max() - bys.min() + 1) / SC / 72, 0.50, tol=0.06, unit="in")
num = (r[..., 0] == 0x33) & (r[..., 1] == 0x33) & (r[..., 2] == 0x33)
nys, nxs = np.where(num)
print(f"  badge numeral #333333 ink bbox x {round(nxs.min() / SC / 72, 3)}..{round(nxs.max() / SC / 72, 3)} in"
      f" x y {round(nys.min() / SC / 72, 3)}..{round(nys.max() / SC / 72, 3)} in")
check("numeral center x (in)", (nxs.min() + nxs.max()) / 2 / SC / 72, 12.73, tol=0.07, unit="in")
check("numeral center y (in)", (nys.min() + nys.max()) / 2 / SC / 72, 0.55, tol=0.07, unit="in")
print("  [info] badge numeral is '16' = number printed on the original (no zero padding)")

# ---------- TEXT vs ORIGINAL ----------
print("\n-- text geometry vs the original frame --")
redm = (r[..., 0] > 150) & (r[..., 0] - r[..., 1] > 40) & (r[..., 0] - r[..., 2] > 40)
bluem = (r[..., 2] > 150) & (r[..., 2] - r[..., 0] > 40) & (r[..., 2] - r[..., 1] > 40)
# position-based masking of non-glyph ink (render px @2001x1125):
# outer house frame, the original's two content-border verticals, the badge corner.
redm[:40, :] = False          # outer frame top
redm[1090:, :] = False        # outer frame bottom
redm[:, :40] = False          # outer frame left
redm[:, 1960:] = False        # outer frame right
redm[:, 115:130] = False      # content border left vertical  (x=58pt -> 121px)
redm[:, 1870:1886] = False    # content border right vertical (x=901pt -> 1878px)
redm[84:96, :] = False        # content border top edge band (y=43pt -> 90px), if any
redm[1035:1075, :] = False    # black-bar band
redm[:60, 1850:] = False      # badge corner
bluem[:60, 1850:] = False     # badge corner

rows = np.where(redm.sum(axis=1) > 3)[0]
gaps = np.where(np.diff(rows) > 20)[0]
if len(gaps):
    bands = [(rows[0], rows[gaps[0]]), (rows[gaps[-1] + 1], rows[-1])]
else:
    bands = [(rows[0], rows[-1])]
print(f"  text bands (render px) -> original px: "
      f"{[(round(to_orig_px(b[0], 'y'), 1), round(to_orig_px(b[1], 'y'), 1)) for b in bands]}")

meas = {}
for nm, (y0, y1) in zip(("title", "subtitle"), bands):
    sub = redm[y0:y1 + 1]
    cols = np.where(sub.any(axis=0))[0]
    meas[nm] = (to_orig_px(y0, "y"), to_orig_px(y1, "y"),
                to_orig_px(cols.min(), "x"), to_orig_px(cols.max(), "x"))
    print(f"  {nm}: ink y {meas[nm][0]:.2f}..{meas[nm][1]:.2f}px  x {meas[nm][2]:.2f}..{meas[nm][3]:.2f}px")

if len(meas) == 2:
    t, s = meas["title"], meas["subtitle"]
    # SIZE (judge findings 1 & 2): the FAIL build was 12pt/12pt -> ~189px / ~114px wide
    check("TITLE ink width  (orig 674 ; pre-fix 12pt build 189)", t[3] - t[2] + 1, 674.0, tol=25)
    check("SUBTITLE ink width (orig 401 ; pre-fix 12pt build 114)", s[3] - s[2] + 1, 401.0, tol=25)
    check("title/subtitle ink-width ratio", (t[3] - t[2]) / (s[3] - s[2]), 674.0 / 401.0, tol=0.15, unit="")
    # cap-height proxy: the ink band of the title (cap + descender)
    check("title band height (cap+desc, orig 37)", t[1] - t[0] + 1, 37.0, tol=6)
    # finding 3, second half: inter-line separation
    check("inter-line ink gap (subtitle top - title bottom)", s[0] - t[1], 29.0, tol=8)
    print("  [info] finding 3 vertical placement: DISMISSED - the house frame rule mandates the")
    print("         title box at y=0.28in, which fixes the title block in the upper band.")

# subtitle colour spans (judge: three spans, one baseline)
sband = bands[-1]
bsub = bluem[sband[0]:sband[1] + 1]
bcol = np.where(bsub.any(axis=0))[0]
brow = np.where(bsub.any(axis=1))[0]
if len(bcol):
    rsub = redm[sband[0]:sband[1] + 1]
    rcol = np.where(rsub.any(axis=0))[0]
    sleft, sright = s[2], s[3]
    sw = sright - sleft

    def exp(ox):
        """Original-frame x -> house-centred expectation for the recreated block."""
        return sleft + (ox - 300.0) * (sw / 401.0)

    check("blue 'Activation' span left", to_orig_px(bcol.min(), "x"), exp(312.0), tol=12)
    check("blue 'Activation' span right", to_orig_px(bcol.max(), "x"), exp(494.0), tol=12)
    check("BLUE 'Activation' cap height (orig 29)", to_orig_px(brow[-1] - brow[0] + 1, "y"), 29.0, tol=10)
    check("blue span top vs subtitle band top", to_orig_px(brow[0] + sband[0], "y"), s[0], tol=8)
    check("red '(' left edge", to_orig_px(rcol.min(), "x"), exp(300.0), tol=12)
    check("red ' Functions)' right edge", to_orig_px(rcol.max(), "x"), exp(700.0), tol=12)
    # title/subtitle must both be centred on the house title box centre
    tcx = (meas["title"][2] + meas["title"][3]) / 2
    scx = (sleft + sright) / 2
    check("title horizontal centre (house box centre)", tcx, HOUSE_CX, tol=8)
    check("subtitle horizontal centre (house box centre)", scx, HOUSE_CX, tol=8)
    print("  [info] the original centres both lines at x=500; the house title box centres at")
    print(f"         {HOUSE_CX:.1f}px, so the recreated block sits {500 - HOUSE_CX:.1f}px to the left.")

# ---------- ORIGINAL'S OWN CONTENT BORDER + BLACK STRIP (finding 7) ----------
print("\n-- original's own content border (#8B0000) and bottom strip --")
dred = (r[..., 0] == 0x8B) & (r[..., 1] == 0) & (r[..., 2] == 0)
dv = np.where(dred.sum(axis=0) > 0.3 * H)[0]
if len(dv) >= 2:
    top_rows = np.where(dred[:, dv[0]])[0]
    check("content border left x  (measured 58)", to_orig_px(dv[0], "x"), 58.0, tol=2)
    check("content border right x (measured 901)", to_orig_px(dv[-1], "x"), 901.0, tol=2)
    check("content border vertical starts y (measured 43)", to_orig_px(top_rows.min(), "y"), 43.0, tol=3)
    print("  [info] the original's top edge at y=43 is left off: at the house-mandated title")
    print("         band it would strike through the title text.")
else:
    fails.append("original's #8B0000 content border not detected in the render")

black = (r[..., 0] == 0) & (r[..., 1] == 0) & (r[..., 2] == 0)
brows = np.where(black.sum(axis=1) > 0.9 * W)[0]
if len(brows):
    check("black strip top y    (measured 518)", to_orig_px(brows[0], "y"), 518.0, tol=8)
    check("black strip bottom y (measured 540, flush)", to_orig_px(brows[-1], "y"), 540.0, tol=8)
else:
    fails.append("full-width black bottom strip not detected")

print("\n-- background tone (finding 6) --")
print(f"  recreation #E8E8E8 vs original interior samples:")
for frac in (0.15, 0.35, 0.55, 0.75, 0.93):
    ry, oy = int(frac * H), int(frac * o.shape[0])
    ox, rx = int(0.5 * o.shape[1]), int(0.5 * W)
    print(f"    y={int(frac * 100)}%  original {tuple(o[oy, ox])}   recreation {tuple(r[ry, rx])}")

print()
if fails:
    print(f"VERIFY RESULT: FAIL ({len(fails)} problem(s))")
    for f in fails:
        print("  - " + f)
    raise SystemExit(1)
print("VERIFY RESULT: PASS - text sizes/spans and measured elements within tolerance;"
      " house chrome verified")
