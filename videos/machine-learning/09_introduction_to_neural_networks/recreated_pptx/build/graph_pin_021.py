"""Pin axis line extents, scales, and curve core colours for all 4 graphs."""
import numpy as np
from PIL import Image
from collections import Counter

V = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/"
im = Image.open(V + "unique_slides/slide_021.jpg").convert("RGB")
a = np.asarray(im).astype(int)

PANELS = {
    "TL": (121, 109, 400, 271, (-10, 10), (0, 10)),
    "TR": (564, 109, 842, 274, (-4, 4), (-1, 3)),
    "BL": (122, 346, 400, 508, (-3, 3), (-1, 3)),
    "BR": (564, 346, 842, 508, (-4, 4), (0, 3)),
}

for name, (x0, y0, x1, y1, xlim, ylim) in PANELS.items():
    print(f"\n##### {name} #####")
    sub = a[y0:y1, x0:x1]
    h, w, _ = sub.shape
    r, g, b = sub[:, :, 0], sub[:, :, 1], sub[:, :, 2]

    # ink = departure from white
    ink = (np.abs(sub - 255).max(axis=2) > 30)
    # find long horizontal dark/gray lines: rows where ink spans a long contiguous run
    best_r, best_c = None, None
    for i in range(h):
        row = ink[i]
        # longest contiguous run
        runs = []
        st = None
        for j in range(w):
            if row[j] and st is None: st = j
            elif not row[j] and st is not None:
                runs.append((st, j)); st = None
        if st is not None: runs.append((st, w))
        runs = [rr for rr in runs if rr[1] - rr[0] > 40]
        for rr in runs:
            if best_r is None or rr[1] - rr[0] > best_r[2]:
                best_r = (i, rr[0], rr[1] - rr[0], rr[1] - 1)
    for j in range(w):
        col = ink[:, j]
        runs = []
        st = None
        for i in range(h):
            if col[i] and st is None: st = i
            elif not col[i] and st is not None:
                runs.append((st, i)); st = None
        if st is not None: runs.append((st, h))
        runs = [rr for rr in runs if rr[1] - rr[0] > 40]
        for rr in runs:
            if best_c is None or rr[1] - rr[0] > best_c[2]:
                best_c = (j, rr[0], rr[1] - rr[0], rr[1] - 1)

    print("  longest horizontal ink line:", best_r, "-> global y", y0 + best_r[0],
          "px x", x0 + best_r[1], "..", x0 + best_r[3])
    print("  longest vertical  ink line:", best_c, "-> global x", x0 + best_c[0],
          "px y", y0 + best_c[1], "..", y0 + best_c[3])

    # curve core colour: darkest saturated reddish pixel
    red = (r - g > 40) & (r - b > 25) & (r > 80)
    if red.sum():
        ys, xs = np.where(red)
        px = sub[red]
        dark = px[np.argmin(px.sum(axis=1))]
        print("  curve core colour:", tuple(dark), " n=", int(red.sum()),
              " bbox x", x0 + xs.min(), "..", x0 + xs.max(), " y", y0 + ys.min(), "..", y0 + ys.max())
    else:
        print("  curve: no red found; saturated-ink census:")
        sat = (sub.max(axis=2) - sub.min(axis=2)) > 60
        print("   ", Counter(map(tuple, (sub[sat] // 24 * 24))).most_common(5))
    # grid colour
    grid = (np.abs(r - g) < 10) & (np.abs(g - b) < 10) & (r > 195) & (r < 228)
    if grid.sum():
        print("  grid colour:", Counter(map(tuple, (sub[grid] // 8 * 8))).most_common(3))
