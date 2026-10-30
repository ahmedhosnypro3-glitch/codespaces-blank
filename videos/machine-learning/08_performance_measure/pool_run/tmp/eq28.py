from PIL import Image
import numpy as np
im = Image.open("/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure/unique_slides/slide_028-.jpg").convert("RGB")
a = np.asarray(im).astype(int)
R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]

def region(x0, y0, x1, y1, label):
    reg = a[y0:y1, x0:x1]
    mx = reg.max(axis=2); mn = reg.min(axis=2)
    ink = (mx < 215)
    redish = (R[y0:y1, x0:x1] - G[y0:y1, x0:x1] > 45) & (R[y0:y1, x0:x1] - B[y0:y1, x0:x1] > 45)
    darkish = (mx < 140) & ~redish
    for nm, m in (("all-ink", ink), ("red", redish), ("dark", darkish)):
        if m.sum() == 0:
            print(f"{label} {nm}: none"); continue
        idx = np.where(m.any(axis=0))[0]
        rows = np.where(m.any(axis=1))[0]
        print(f"{label} {nm}: x {idx.min()+x0}-{idx.max()+x0} (w {idx.max()-idx.min()+1}) y {rows.min()+y0}-{rows.max()+y0} (h {rows.max()-rows.min()+1}) n={m.sum()}")
    # row profile of dark ink (equation glyphs)
    cnt = darkish.sum(axis=1)
    print(f"   dark row profile:", " ".join(f"{y0+i}:{c}" for i, c in enumerate(cnt) if c > 0))

# TPR formula box interior (box 113-302 x, 252-314 y)
region(118, 257, 298, 309, "TPR-formula")
# FPR formula box interior (box 113-302, 364-425)
region(118, 369, 298, 420, "FPR-formula")

# underline detection: look under conclusion text (y 477-486) and under "recall"
print("=== conclusion underline scan (y 476-490) ===")
for y in range(476, 492):
    row = a[y, 80:690]
    dark = np.where(row.max(axis=1) < 190)[0]
    if len(dark):
        # contiguous runs
        runs = []; st = dark[0]; prev = dark[0]
        for v in dark[1:]:
            if v - prev > 4: runs.append((st, prev)); st = v
            prev = v
        runs.append((st, prev))
        print(f"  y={y}: " + ", ".join(f"{s+80}-{e+80}" for s, e in runs if e - s > 3))
print("=== recall underline scan (y 244-252, x 200-420) ===")
for y in range(244, 254):
    row = a[y, 150:450]
    dark = np.where(row.max(axis=1) < 190)[0]
    if len(dark):
        runs = []; st = dark[0]; prev = dark[0]
        for v in dark[1:]:
            if v - prev > 4: runs.append((st, prev)); st = v
            prev = v
        runs.append((st, prev))
        print(f"  y={y}: " + ", ".join(f"{s+150}-{e+150}" for s, e in runs if e - s > 3))
print("=== conclusion text per-word x (row profile) ===")
cnt = ((a[458:478, 80:690].max(axis=2) < 200)).sum(axis=0)
runs = []; inb = False
for i, c in enumerate(cnt):
    if c > 0 and not inb: st = i; inb = True
    elif c == 0 and inb: runs.append((st+80, i-1+80)); inb = False
if inb: runs.append((st+80, 689))
print("  glyph runs:", runs)
