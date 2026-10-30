#!/usr/bin/env python3
"""S23 paren sweep driver: census renders + originals, match strokes, flag.

For each scope slide:
  1. census tall thin strokes on the certified 150dpi render
  2. census the same on the original 960x540 frame (scaled thresholds)
  3. map render bboxes to frame space (sx=2001/960, sy=1125/540), match by
     center distance + height similarity
  4. flag MISMATCH when matched strokes disagree on direction, and flag
     SAME-DIR-PAIR when two curved strokes in one horizontal band on the
     render share a verdict (possible mirrored pair)
Writes sweep_census.json + prints a compact report.
"""
import glob
import json
import os
import subprocess
import sys

import numpy as np
from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from scan_dir_render import load_ink, stroke_census

HERE = os.path.dirname(os.path.abspath(__file__))
DECK = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"

SLIDES = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 16, 17, 18, 20, 21, 22,
          23, 24, 26, 27, 28, 29, 30, 31, 32, 33, 35, 36, 37, 38, 39, 40, 41,
          42, 45, 46, 47, 49]

SX, SY = 2001 / 960.0, 1125 / 540.0  # render px per frame px


def render_for(n):
    d = os.path.join(DECK, f"recreated_pptx/qa/slide{n:03d}")
    certs = sorted(glob.glob(os.path.join(d, "render_[0-9]*.png")),
                   key=lambda p: int(os.path.basename(p).split("_")[1].split(".")[0]))
    return certs[-1] if certs else os.path.join(d, "render_regen.png")


def curved(s):
    return s["verdict"] in ("(", ")")


def band_key(s, tol=25):
    return int(s["bbox"][1] // tol)


def main():
    report = {}
    for n in SLIDES:
        rp = render_for(n)
        op = os.path.join(DECK, f"unique_slides/slide_{n:03d}.jpg")
        ren = stroke_census(load_ink(rp, 160), 18, 0.55)
        # original: frame px — scale min_h by 540/1125, allow up to 0.75 frac
        orig = stroke_census(load_ink(op, 160), 9, 0.75)

        # map render strokes to frame space
        ren_f = []
        for s in ren:
            x0, y0, x1, y1 = s["bbox"]
            f = dict(s)
            f["fbbox"] = [x0 / SX, y0 / SY, x1 / SX, y1 / SY]
            f["fcx"] = (x0 + x1) / 2 / SX
            f["fcy"] = (y0 + y1) / 2 / SY
            f["fh"] = (y1 - y0) / SY
            ren_f.append(f)
        for s in orig:
            x0, y0, x1, y1 = s["bbox"]
            s["fcx"] = (x0 + x1) / 2
            s["fcy"] = (y0 + y1) / 2
            s["fh"] = float(y1 - y0)

        pairs, unmatched_ren = [], []
        used = set()
        for r in ren_f:
            if not curved(r):
                continue
            best, bd = None, 1e9
            for i, o in enumerate(orig):
                if not curved(o) or i in used:
                    continue
                d = ((r["fcx"] - o["fcx"]) ** 2 + (r["fcy"] - o["fcy"]) ** 2) ** 0.5
                hr = abs(r["fh"] - o["fh"]) / max(r["fh"], o["fh"])
                if d < bd and hr < 0.45:
                    best, bd = i, d
            if best is not None and bd <= 9:
                used.add(best)
                o = orig[best]
                pairs.append({
                    "render": [r["bbox"], r["verdict"], round(r["delta"], 2)],
                    "orig": [o["bbox"], o["verdict"], round(o["delta"], 2)],
                    "dist": round(bd, 1),
                    "match": "OK" if r["verdict"] == o["verdict"] else "MISMATCH",
                })
            else:
                unmatched_ren.append([r["bbox"], r["verdict"], round(r["delta"], 2)])

        # same-direction curved pairs per band on the render (mirrored-pair hint)
        bands = {}
        for r in ren_f:
            if curved(r):
                bands.setdefault(band_key(r), []).append((r["bbox"], r["verdict"], round(r["delta"], 2)))
        samedir = []
        for b, items in sorted(bands.items()):
            items.sort()
            for a, c in zip(items, items[1:]):
                if a[1] == c[1]:
                    samedir.append({"band": b * 25, "pair": [a, c]})

        n_mism = sum(1 for p in pairs if p["match"] == "MISMATCH")
        report[n] = {
            "render": os.path.relpath(rp, DECK),
            "ren_curved": len([r for r in ren_f if curved(r)]),
            "ren_straight": len([r for r in ren_f if not curved(r)]),
            "orig_curved": len([o for o in orig if curved(o)]),
            "pairs": pairs, "unmatched_render_curved": unmatched_ren,
            "samedir_bands": samedir, "mismatches": n_mism,
        }
        print(f"slide {n:03d}: render curved={report[n]['ren_curved']} "
              f"straight={report[n]['ren_straight']} orig curved={report[n]['orig_curved']} "
              f"matched={len(pairs)} mismatch={n_mism} unmatched={len(unmatched_ren)} "
              f"samedir_bands={len(samedir)}")

    with open(os.path.join(HERE, "sweep_census.json"), "w") as f:
        json.dump(report, f, indent=1)
    print("# banked sweep_census.json")


if __name__ == "__main__":
    main()
