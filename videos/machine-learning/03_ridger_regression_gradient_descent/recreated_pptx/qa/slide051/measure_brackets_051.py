#!/usr/bin/env python3
"""Measure vertical-stroke (bracket) geometry on the original frame and the render.

Frame space: original 960x540 (1px=1pt); render 2001x1125 -> scale sx=2001/960,
sy=1125/540. All output in frame px.
"""
import json
import sys
from PIL import Image

ORIG = "videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_051.jpg"
REND = sys.argv[1] if len(sys.argv) > 1 else \
    "videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide051/render_2.png"

THR = 170  # ink = darker than this

REGIONS = {
    # name: (x0, y0, x1, y1, band_y0, band_y1)
    "sample": (78, 54, 240, 130, 70, 112),
    "centre_w": (255, 54, 440, 112, 55, 110),
    "z": (585, 54, 670, 118, 72, 114),
    "aug": (78, 140, 235, 250, 175, 230),
    "dec1": (330, 141, 470, 197, 141, 197),
    "dec2": (330, 207, 470, 263, 207, 263),
    "dec3": (330, 273, 470, 329, 273, 329),
}


def ink_mask(img, thr=THR):
    return img.convert("L").point(lambda p: 255 if p < thr else 0)


def measure(path, region, is_render):
    x0, y0, x1, y1, by0, by1 = region
    img = Image.open(path)
    m = ink_mask(img)
    if is_render:
        sx, sy = img.width / 960.0, img.height / 540.0
    else:
        sx = sy = 1.0
    W, H = img.width, img.height

    px = m.load()
    cols = []
    for fx in range(x0, x1):
        # count ink rows in band, and find min/max row of ink
        c = 0
        top = None
        bot = None
        run = 0
        best_run = 0
        for fy in range(by0, by1):
            X = min(W - 1, int(round(fx * sx)))
            Y = min(H - 1, int(round(fy * sy)))
            if px[X, Y] > 0:
                c += 1
                run += 1
                best_run = max(best_run, run)
                if top is None:
                    top = fy
                bot = fy
            else:
                run = 0
        cols.append((fx, c, top, bot, best_run))
    return cols


def strokes(cols, band_h, min_frac=0.55):
    """Group columns whose ink count / band height >= min_frac into strokes."""
    need = band_h * min_frac
    out = []
    cur = None
    for fx, c, top, bot, br in cols:
        if c >= need:
            if cur is None:
                cur = {"x0": fx, "x1": fx, "count": c, "top": top, "bot": bot, "best_run": br}
            else:
                cur["x1"] = fx
                cur["count"] = max(cur["count"], c)
                cur["top"] = min(cur["top"], top) if cur["top"] is not None else top
                cur["bot"] = max(cur["bot"], bot) if cur["bot"] is not None else bot
                cur["best_run"] = max(cur["best_run"], br)
        else:
            if cur is not None:
                out.append(cur)
                cur = None
    if cur is not None:
        out.append(cur)
    return out


def main():
    result = {}
    for name, region in REGIONS.items():
        band_h = region[5] - region[4]
        oc = measure(ORIG, region, False)
        rc = measure(REND, region, True)
        result[name] = {
            "region": region,
            "orig_strokes": strokes(oc, band_h),
            "rend_strokes": strokes(rc, band_h),
            "orig_cols": oc,
            "rend_cols": rc,
        }
        print("=" * 70)
        print("REGION", name, region, "band_h", band_h)
        for tag, key in (("ORIG", "orig_strokes"), ("REND", "rend_strokes")):
            print(f"  {tag} tall strokes (count >= {band_h*0.55:.0f} of band):")
            for st in result[name][key]:
                print("    x %3d..%3d  inkcount=%2d  top=%s bot=%s  bestrun=%s"
                      % (st["x0"], st["x1"], st["count"], st["top"], st["bot"], st["best_run"]))
    with open("videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide051/"
              "measure_brackets_051.json", "w") as f:
        json.dump({k: {"region": v["region"], "orig_strokes": v["orig_strokes"],
                       "rend_strokes": v["rend_strokes"]} for k, v in result.items()}, f, indent=1)
    print("\nwrote measure_brackets_051.json")


if __name__ == "__main__":
    main()
