"""Generate slide_016 assets: F1 equation PNG + small stacked fractions.

Geometry measured from unique_slides/slide_016.jpg (960x540 frame, 1px = 1pt):
  F1 green box   x 93..498  y 329..388   (equation ink centered inside)
  Precision box  x 749..899 y 111..182   fraction centered ~y 150..172
  Recall box     x 749..899 y 183..230   fraction centered ~y 190..222
"""
import json
import os
import subprocess
import sys

import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = "/home/codespace/ai_llm_slides"
OUT_MANIFEST = os.path.join(HERE, "eq_016_manifest.json")

DARK_RED = "A50000"


def render_eq(latex, out_png, fontsize, color):
    proc = subprocess.run(
        [sys.executable, os.path.join(ROOT, "scripts/render_eq.py"), latex,
         out_png, str(fontsize), "#" + color],
        capture_output=True, text=True, check=True)
    for line in proc.stdout.splitlines():
        if line.strip().startswith("{"):
            return json.loads(line)
    raise RuntimeError("no json from render_eq for " + latex)


def ink_box(png):
    a = np.array(Image.open(png).convert("RGBA"))
    ink = a[:, :, 3] > 8
    rows = np.nonzero(ink.any(axis=1))[0]
    cols = np.nonzero(ink.any(axis=0))[0]
    h, w = ink.shape
    return {
        "ink_top_frac": float(rows.min()) / h,
        "ink_left_frac": float(cols.min()) / w,
        "ink_h_frac": float(rows.max() - rows.min() + 1) / h,
        "ink_w_frac": float(cols.max() - cols.min() + 1) / w,
    }


EQS = [
    ("f1", r"\frac{1}{\mathrm{F1\ Score}} = \frac{1}{2} \times \left( \frac{1}{\mathrm{Precision}} + \frac{1}{\mathrm{Recall}} \right)", 21, DARK_RED),
    ("prec", r"\frac{\mathrm{TP}}{\mathrm{TP} + \mathrm{FP}}", 17, DARK_RED),
    ("rec", r"\frac{\mathrm{TP}}{\mathrm{TP} + \mathrm{FN}}", 17, DARK_RED),
]

manifest = {}
for name, latex, size, color in EQS:
    png = os.path.join(HERE, "eq_016_%s.png" % name)
    meta = render_eq(latex, png, size, color)
    meta.update(ink_box(png))
    manifest[name] = meta
    print(name, meta["w_px"], "x", meta["h_px"], "px ->", meta["w_in"], "x", meta["h_in"], "in")

with open(OUT_MANIFEST, "w") as fh:
    json.dump(manifest, fh, indent=1)
print("OK", OUT_MANIFEST)
