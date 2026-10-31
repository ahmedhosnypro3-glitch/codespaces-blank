#!/usr/bin/env python3
"""Lane G (b_geom_1) — finer structure probe: fine bands + horizontal panel-edge rows."""
import sys
import numpy as np
from PIL import Image
from scipy import ndimage

sys.path.insert(0, "/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example/_pool")
import importlib.util
spec = importlib.util.spec_from_file_location(
    "gf", "/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example/_pool/geom_b_geom_1_final.py")
gf = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gf)


def fine_bands(m, minpx=20, gap=2):
    rows = np.nonzero(m.sum(axis=1) > 0)[0]
    if rows.size == 0:
        return []
    out = []
    start = prev = rows[0]
    for y in rows[1:]:
        if y - prev > gap:
            out.append((start, prev + 1))
            start = y
        prev = y
    out.append((start, prev + 1))
    res = []
    for y0, y1 in out:
        sub = m[y0:y1]
        ys, xs = np.nonzero(sub)
        if xs.size >= minpx:
            res.append((int(y0), int(y1), int(xs.min()), int(xs.max()) + 1, int(xs.size)))
    return res


def edge_rows(m, frac=0.15):
    """rows that look like a drawn horizontal border (long ink run)."""
    out = []
    for y in range(m.shape[0]):
        c = int(m[y].sum())
        if c > frac * m.shape[1]:
            xs = np.nonzero(m[y])[0]
            out.append((y, c, int(xs.min()), int(xs.max()) + 1))
    return out


def main():
    for n in (sys.argv[1:] or ["001", "004", "005", "006", "007"]):
        o, r = gf.load(n)
        obr, rbr = gf.red_rect(o), gf.red_rect(r)
        om = gf.apply_chrome(gf.structure(o), obr, gf.badge_box(o), 517)
        rm = gf.apply_chrome(gf.structure(r), rbr, gf.HOUSE_BADGE, None)
        print("\n===== slide_%s" % n)
        print(" ORIG fine bands:", fine_bands(om))
        print(" REND fine bands:", fine_bands(rm))
        print(" ORIG edge rows:", edge_rows(om))
        print(" REND edge rows:", edge_rows(rm))


if __name__ == "__main__":
    main()
