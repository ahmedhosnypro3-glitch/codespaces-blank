#!/usr/bin/env python3
"""S4b fresh finisher: PIL-first adjudication of the banked attempt-21 findings
(slide 019). All coordinates in 960x540 frame space; per-image scale factor.
Never mutates banked evidence."""
from PIL import Image
import numpy as np

V = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
QA = f"{V}/recreated_pptx/qa/slide019"

IMGS = {
    "ORIG": (np.asarray(Image.open(f"{V}/unique_slides/slide_019.jpg").convert("RGB")).astype(int), 1.0),
    "R21": (np.asarray(Image.open(f"{QA}/render_21.png").convert("RGB")).astype(int), 2001 / 960.0),
}


def zone(a, s, x0, y0, x1, y1):
    return a[int(y0 * s):int(y1 * s), int(x0 * s):int(x1 * s)]


def ink_masks(z):
    r, g, b = z[..., 0], z[..., 1], z[..., 2]
    lum = z.sum(axis=2)
    dark = lum < 300
    blue = (b > 90) & (b - r > 30) & (b - g > 20) & ~dark
    red = (r > 100) & (r - g > 45) & (r - b > 45)
    green = (g > 80) & (g - r > 30) & (g - b > 30)
    yellow = (r > 190) & (g > 190) & (b < 170) & (r - b > 60)
    return dark, blue, red, green, yellow


HEADS = [("NO REG", 124, 380), ("RIDGE3", 384, 640), ("RIDGE10", 644, 900)]

print("=== 1. header-band ink census per column (y178..200) ===")
for tag, (a, s) in IMGS.items():
    for nm, hx0, hx1 in HEADS:
        z = zone(a, s, hx0, hx1 and hx1, 178, 200) if False else zone(a, s, hx0, 178, hx1, 200)
        d, bl, rd, gr, ye = ink_masks(z)
        # x-extent of blue and red ink
        def runs(m):
            cols = np.nonzero(m.sum(axis=0) > 0)[0]
            if not len(cols):
                return "none"
            out, st = [], cols[0]
            for i in range(1, len(cols)):
                if cols[i] != cols[i - 1] + 1 and cols[i] - cols[i - 1] > 3:
                    out.append(f"{hx0 + st / s:.0f}..{hx0 + cols[i - 1] / s:.0f}")
                    st = cols[i]
            out.append(f"{hx0 + st / s:.0f}..{hx0 + cols[-1] / s:.0f}")
            return ",".join(out[:8])
        print(f"  {tag} {nm}: blue {int(bl.sum()):5d} px  red {int(rd.sum()):5d} px"
              f"  blue-x[{runs(bl)}]  red-x[{runs(rd)}]")

print("=== 2. lambda=10 right-edge geometry (rows y210..520, x860..910) ===")
for tag, (a, s) in IMGS.items():
    z = zone(a, s, 860, 210, 912, 520)
    d, bl, rd, gr, ye = ink_masks(z)
    colsum_g = gr.sum(axis=0)
    colsum_d = d.sum(axis=0)
    gcols = np.nonzero(colsum_g > 20)[0]
    dcols = np.nonzero(colsum_d > 60)[0]
    print(f"  {tag}: green-rule cols " + (", ".join(f"{860 + c / s:.1f}" for c in gcols) if len(gcols) else "none")
          + f" | dark(cols>60) " + (", ".join(f"{860 + c / s:.1f}" for c in dcols) if len(dcols) else "none"))

print("=== 3. y-row green-value right extent vs green rule (R10 rows) ===")
YROWS = [(272, 296, "95.6"), (379, 403, "57.4"), (487, 511, "44.1")]
for tag, (a, s) in IMGS.items():
    for y0, y1, lbl in YROWS:
        z = zone(a, s, 830, y0, 912, y1)
        d, bl, rd, gr, ye = ink_masks(z)
        gcols = np.nonzero(gr.sum(axis=0) > 0)[0]
        ycols = np.nonzero(ye.sum(axis=0) > 0)[0]
        gext = f"{830 + gcols[-1] / s:.1f}" if len(gcols) else "-"
        yext = f"{830 + ycols[-1] / s:.1f}" if len(ycols) else "-"
        print(f"  {tag} y-row({lbl}): green-text right-extent x{gext}  yellow-band right-extent x{yext}")

print("=== 4. yellow band right edge, lambda=10 full band rows ===")
for tag, (a, s) in IMGS.items():
    for y0, y1, lbl in YROWS:
        z = zone(a, s, 700, y0, 912, y1)
        d, bl, rd, gr, ye = ink_masks(z)
        ycols = np.nonzero(ye.sum(axis=0) > 8)[0]
        print(f"  {tag} band({lbl}): yellow right x{700 + ycols[-1] / s:.1f}" if len(ycols)
              else f"  {tag} band({lbl}): no yellow")

print("=== 5. outlier bracket vs top value vertical alignment (x58..118) ===")
for tag, (a, s) in IMGS.items():
    for gy, lbl in [(199, "grp1 11/3/22"), (321, "grp2 30/3/22"), (424, "grp3 60/3/22")]:
        zb = zone(a, s, 58, gy - 8, 78, gy + 72)
        zv = zone(a, s, 80, gy - 8, 118, gy + 72)
        db, _, _, _, _ = ink_masks(zb)
        dv, _, _, _, _ = ink_masks(zv)
        brows = np.nonzero(db.sum(axis=1) > 0)[0]
        vrows = np.nonzero(dv.sum(axis=1) > 0)[0]
        btop = f"{gy - 8 + brows[0] / s:.1f}" if len(brows) else "-"
        bbot = f"{gy - 8 + brows[-1] / s:.1f}" if len(brows) else "-"
        vtop = f"{gy - 8 + vrows[0] / s:.1f}" if len(vrows) else "-"
        print(f"  {tag} {lbl}: bracket ink y{btop}..{bbot}  values top y{vtop}")

print("=== 6. outlier header glyph crop (for s-vs-8 read) ===")
for tag, (a, s) in IMGS.items():
    z = zone(a, s, 60, 172, 130, 200)
    d, bl, rd, gr, ye = ink_masks(z)
    rows = np.nonzero(d.sum(axis=1) + bl.sum(axis=1) > 0)[0]
    cols = np.nonzero(d.sum(axis=0) + bl.sum(axis=0) > 0)[0]
    if len(rows):
        print(f"  {tag}: header ink y{172 + rows[0] / s:.1f}..{172 + rows[-1] / s:.1f}"
              f"  x{60 + cols[0] / s:.1f}..{60 + cols[-1] / s:.1f}")
        crop = Image.open(f"{V}/unique_slides/slide_019.jpg" if tag == "ORIG" else f"{QA}/render_21.png").convert("RGB")
        cs = s
        box = (int(88 * cs), int(172 * cs), int(126 * cs), int(200 * cs))
        up = crop.crop(box).resize(((box[2] - box[0]) * 6, (box[3] - box[1]) * 6), Image.LANCZOS)
        up.save(f"{QA}/pil_a21_{tag.lower()}_subscript_x8.png")

print("=== 7. title-box underline extent (red ink y~112..122, x150..410) ===")
for tag, (a, s) in IMGS.items():
    z = zone(a, s, 150, 106, 415, 124)
    d, bl, rd, gr, ye = ink_masks(z)
    rcols = np.nonzero(rd.sum(axis=0) > 0)[0]
    if len(rcols):
        runs, st = [], rcols[0]
        for i in range(1, len(rcols)):
            if rcols[i] != rcols[i - 1] + 1 and rcols[i] - rcols[i - 1] > 4:
                runs.append((st, rcols[i - 1])); st = rcols[i]
        runs.append((st, rcols[-1]))
        print(f"  {tag}: red-ink col runs " + ", ".join(f"{150 + x / s:.0f}..{150 + y / s:.0f}" for x, y in runs[:10]))
    else:
        print(f"  {tag}: no red ink in band")

print("=== 8. third W entries minus-sign check (R3 g1 + R10 g1: entry-3 cells) ===")
# RIDGE3 g1 third entry ~x0+49..x0+65 x 467..483*  y gy+44..gy+60 ; R3 x0=384
for tag, (a, s) in IMGS.items():
    for x0, gy, lbl in [(384, 205, "R3g1 0.03"), (644, 205, "R10g1 0.09")]:
        z = zone(a, s, x0 + 42, gy + 40, x0 + 72, gy + 62)
        d, bl, rd, gr, ye = ink_masks(z)
        cols = np.nonzero(d.sum(axis=0) > 0)[0]
        if len(cols):
            print(f"  {tag} {lbl}: dark cols x{x0 + 42 + cols[0] / s:.0f}..{x0 + 42 + cols[-1] / s:.0f}"
                  f"  ink {int(d.sum())}")
            crop = Image.open(f"{V}/unique_slides/slide_019.jpg" if tag == "ORIG" else f"{QA}/render_21.png").convert("RGB")
            box = (int((x0 + 40) * s), int((gy + 38) * s), int((x0 + 74) * s), int((gy + 64) * s))
            up = crop.crop(box).resize(((box[2] - box[0]) * 8, (box[3] - box[1]) * 8), Image.LANCZOS)
            up.save(f"{QA}/pil_a21_{tag.lower()}_entry3_{lbl.split()[0]}.png")
