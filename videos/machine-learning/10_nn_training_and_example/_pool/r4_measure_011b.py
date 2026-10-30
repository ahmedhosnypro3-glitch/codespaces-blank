#!/usr/bin/env python3
"""scope_r4 adjudication part 2 — slide 011 refined M1, M2, M3."""
import numpy as np
from PIL import Image

VID = "/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example"
DPI = 150
R = np.asarray(Image.open(f"{VID}/qa/slide011/rejudge/render-1.png").convert("RGB")).astype(int)
Ot = np.asarray(Image.open(f"{VID}/unique_slides/slide_011.jpg").convert("RGB")
                .resize((2001, 1125), Image.LANCZOS)).astype(int)


def box(a, x0, y0, x1, y1):
    return a[int(y0 * DPI):int(y1 * DPI), int(x0 * DPI):int(x1 * DPI)]


def near(a, rgb, tol):
    return np.abs(a - np.array(rgb)).max(axis=2) <= tol


def comp_bbox(m):
    ys, xs = np.nonzero(m)
    return None if len(xs) == 0 else (int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max()))


def fmt(name, bb):
    return (f"{name}: ({bb[0]/DPI:.2f},{bb[1]/DPI:.2f})-({bb[2]/DPI:.2f},{bb[3]/DPI:.2f})in" if bb
            else f"{name}: none")


print("### M1 refined: yellow 'Output' word vs red title glyphs ###")
for tag, ob in (("RENDER", R), ("ORIGINAL", Ot)):
    t = box(ob, 0.0, 0.2, 10.6, 0.95)          # exclude badge (x>10.6in)
    yellow = near(t, (255, 215, 0), 70)
    red = near(t, (192, 0, 0), 90)
    yb, rb = comp_bbox(yellow), comp_bbox(red)
    print(tag, f"'Output' highlight {fmt('', yb)} | title glyphs {fmt('', rb)}")
    if yb and rb:
        inside = int(red[yb[1]:yb[3] + 1, yb[0]:yb[2] + 1].sum())
        print(f"   red glyph px INSIDE highlight bbox: {inside} -> "
              f"{'word sits over red glyphs (collision)' if inside else 'word clear of red glyphs'}")

print("\n### M2: red 'Sigmoid' overlay vs bottom equation strip ###")
strip = box(R, 0.3, 6.4, 13.0, 7.2)
red_s = near(strip, (192, 0, 0), 60)
dark = (strip.mean(axis=2) < 140)
rb_s, db_s = comp_bbox(red_s), comp_bbox(dark)
print("RENDER strip red", fmt("", rb_s), "| dark ink", fmt("", db_s))
strip_o = box(Ot, 0.3, 6.4, 13.0, 7.2)
red_o = near(strip_o, (192, 0, 0), 60)
dark_o = (strip_o.mean(axis=2) < 120)
print("ORIGINAL strip red", fmt("", comp_bbox(red_o)), "| dark ink", fmt("", comp_bbox(dark_o)))

print("\n### M2b: is the full equation image rendered? render crop vs eq3.png asset ###")
eq3 = Image.open(f"{VID}/recreated_pptx/build/eq_slide_011/eq3.png").convert("RGBA")
bg = Image.new("RGBA", eq3.size, (253, 245, 230, 255))
eq3 = Image.alpha_composite(bg, eq3).convert("L").resize((1176, 35), Image.LANCZOS)
eq3 = np.asarray(eq3).astype(float)
crop = box(R, 0.5, 6.65, 8.34167, 6.88333).mean(axis=2).astype(float)
asset_prof = eq3.sum(axis=0)
render_prof = crop.sum(axis=0)
c = np.corrcoef(asset_prof, render_prof)[0, 1]
print(f"column-ink-profile Pearson r (asset vs render): {c:.4f}")
for name, a, b in (("left third", asset_prof[:392], render_prof[:392]),
                   ("mid third", asset_prof[392:784], render_prof[392:784]),
                   ("right third", asset_prof[784:], render_prof[784:])):
    print(f"  {name}: r={np.corrcoef(a, b)[0, 1]:.3f}")
bad = np.where(np.abs(asset_prof - render_prof) > 20000)[0]
print(f"  columns where render diverges from asset by >20k: "
      f"{len(bad)} cols, x-range "
      f"{(0.5 + bad.min()/DPI):.2f}-{(0.5 + bad.max()/DPI):.2f}in" if len(bad) else "  none")

print("\n### M3: network wiring between node columns ###")
bands = [(2.7, 3.8), (4.2, 5.5), (5.9, 7.2), (7.6, 9.0)]
bgc = np.array([253, 245, 230])
for tag, ob, thr in (("RENDER", R, 55), ("ORIGINAL", Ot, 45)):
    tot = 0
    for x0, x1 in bands:
        b = box(ob, x0, 2.6, x1, 5.8)
        m = (np.abs(b - bgc).max(axis=2) > thr) if tag == "RENDER" else (b.mean(axis=2) < 150)
        tot += int(m.sum())
    print(f"{tag}: dark/non-bg px in the 4 inter-column bands: {tot} "
          f"(band area each 1.1x3.2in = {int(1.1*150)*int(3.2*150)} px)")
