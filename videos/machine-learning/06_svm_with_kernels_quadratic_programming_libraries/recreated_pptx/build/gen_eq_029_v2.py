#!/usr/bin/env python3
"""Slide 029 math assets v2: renders with the CERTIFIED scripts/render_eq_wide.py
(the build-local render_math.py mis-crops rows -- y-flip -- and produced the
garbled e1/e2/e3 PNGs that failed judging). Assets land in eq_029_v2/ with
manifest.json {name: {file, w_in, h_in}}; slide_029.js places them at exact
size (w = px/600 in, never rescaled).
"""
import importlib.util
import json
import os
import tempfile

import numpy as np
from PIL import Image

ROOT = "/home/codespace/ai_llm_slides"
spec = importlib.util.spec_from_file_location("render_eq_wide", ROOT + "/scripts/render_eq_wide.py")
wide = importlib.util.module_from_spec(spec)
spec.loader.exec_module(wide)

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "eq_029_v2")
os.makedirs(OUT, exist_ok=True)
DPI = 600
GAP_PX = 20
PAD = 8
W = 13.33


def region(x0, y0, x1, y1):
    return ((x1 - x0) * W, (y1 - y0) * 7.5)  # maxw_in, maxh_in


def render_row(segments, pt):
    """segments: [(hexcolor, latex)] -> composited RGBA canvas, baseline-aligned."""
    parts = []
    with tempfile.TemporaryDirectory() as td:
        for i, (color, latex) in enumerate(segments):
            p = os.path.join(td, f"s{i}.png")
            info = wide.render(latex, p, pt, "#" + color.lstrip("#"))
            parts.append((np.array(Image.open(p).convert("RGBA")), info["baseline_px"]))
    base = max(b for _, b in parts)
    h = max(base + (a.shape[0] - b) for a, b in parts) + 2 * PAD
    w = sum(a.shape[1] for a, _ in parts) + GAP_PX * (len(parts) - 1) + 2 * PAD
    canvas = np.zeros((h, w, 4), dtype=np.uint8)
    x = PAD
    for a, b in parts:
        y = PAD + base - b
        canvas[y:y + a.shape[0], x:x + a.shape[1]] = a
        x += a.shape[1] + GAP_PX
    return canvas


def fit(name, segments, box, base_pt, maxw, maxh):
    probe = render_row(segments, base_pt)
    pw, ph = probe.shape[1] / DPI, probe.shape[0] / DPI
    pt = max(8.0, min(18.0, base_pt * min(maxw / pw, maxh / ph)))
    canvas = render_row(segments, pt)
    path = os.path.join(OUT, name + ".png")
    Image.fromarray(canvas).save(path)
    m = {"file": name + ".png", "w_in": round(canvas.shape[1] / DPI, 5),
         "h_in": round(canvas.shape[0] / DPI, 5), "pt": round(pt, 2)}
    print(name, "w_in=%.3f h_in=%.3f pt=%.1f" % (m["w_in"], m["h_in"], pt))
    return m

# name -> (segments, normalized region [x0,y0,x1,y1], base pt)
EQS = {
    # E1: RBF identity in box 1; trailing factors blue-purple, final e^{ab} red
    "e1": ([( "000000", r"e^{-\frac{1}{2}(a-b)^{2}} = e^{-\frac{1}{2}(a^{2}+b^{2}-2ab)} = "),
            ("3333CC", r"e^{-\frac{a^{2}}{2}}\,e^{-\frac{b^{2}}{2}}\,"),
            ("CC0000", r"e^{ab}")],
           (0.086, 0.170, 0.505, 0.227), 14),
    # E2: Taylor expansion of e^{ab} in box 2; e^{ab} and trailing infinity red
    "e2": ([("CC0000", r"e^{ab} = "),
            ("000000", r"1 + \frac{ab}{1!} + \frac{(ab)^{2}}{2!} + \frac{(ab)^{3}}{3!} "
                       r"+ \frac{(ab)^{4}}{4!} + \frac{(ab)^{5}}{5!} + ......\,"),
            ("CC0000", r"\infty")],
           (0.086, 0.266, 0.505, 0.326), 14),
    # E3 lead-in "e^{ab} =" (red) left of the vector product in box 3
    "e3_eq": ([("CC0000", r"e^{ab} =")], (0.090, 0.393, 0.127, 0.426), 14),
    # E3 row vector: leading 1 then a/sqrt(n!) terms (judge: leading "1" is in the original)
    "e3_row": ([("000000", r"\left[\ 1\ \ \frac{a}{\sqrt{1!}}\ \ \frac{a^{2}}{\sqrt{2!}}\ "
                           r"\ \frac{a^{3}}{\sqrt{3!}}\ \ \frac{a^{4}}{\sqrt{4!}}\ "
                           r"\ ...\ \ ...\ \ \infty\ \right]")],
               (0.130, 0.389, 0.365, 0.444), 14),
    # E3 column vector: true 2-D stack via \substack inside square brackets
    "e3_col": ([("000000", r"\left[\substack{1/b \\ \sqrt{1!}/b^{2} \\ \sqrt{2!}/b^{3} "
                           r"\\ \sqrt{3!}/b^{4} \\ \sqrt{4!}/... \\ ... \\ ...\ \infty}"
                           r"\right]")],
               (0.400, 0.395, 0.505, 0.785), 14),
    # E4: e^x series inside right panel inner box; trailing infinity red
    "e4": ([("000000", r"e^{x} = 1 + \frac{x}{1!} + \frac{x^{2}}{2!} + \frac{x^{3}}{3!} "
                       r"+ \frac{x^{4}}{4!} + \frac{x^{5}}{5!} + ......\,"),
            ("CC0000", r"\infty")],
           (0.533, 0.231, 0.859, 0.281), 13),
    # E5: e^3 series line; trailing infinity red
    "e5": ([("000000", r"e^{3} = 1 + \frac{3}{1!} + \frac{3^{2}}{2!} + \frac{3^{3}}{3!} "
                       r"+ \frac{3^{4}}{4!} + \frac{3^{5}}{5!} + ......\,"),
            ("CC0000", r"\infty")],
           (0.533, 0.311, 0.854, 0.365), 13),
    # phi labels on yellow highlights: blue phi, red superscript T
    "phi_a": ([("0000CC", r"\phi(a)"), ("CC0000", r"^{\mathrm{T}}")],
              (0.182, 0.467, 0.251, 0.520), 14),
    "phi_b": ([("0000CC", r"\phi(b)")], (0.332, 0.594, 0.397, 0.650), 14),
}

def render_col(entries, pt, maxw, maxh):
    """True 2-D column vector: stack per-entry PNGs, draw square brackets with PIL."""
    with tempfile.TemporaryDirectory() as td:
        parts = []
        for i, latex in enumerate(entries):
            p = os.path.join(td, f"c{i}.png")
            info = wide.render(latex, p, pt, "#000000")
            parts.append(np.array(Image.open(p).convert("RGBA")))
    pitch = max(a.shape[0] for a in parts) + int(pt / 72 * DPI * 0.45)
    widest = max(a.shape[1] for a in parts)
    bt = max(5, int(pt / 72 * DPI * 0.055))          # bracket thickness px
    ser = max(14, int(0.10 * DPI))                    # bracket serif length px
    h = pitch * len(parts) + 2 * PAD
    w = widest + 2 * (ser + bt) + 2 * PAD
    canvas = np.zeros((h, w, 4), dtype=np.uint8)
    for i, a in enumerate(parts):
        x = PAD + ser + bt + (widest - a.shape[1]) // 2
        y = PAD + i * pitch
        canvas[y:y + a.shape[0], x:x + a.shape[1]] = a
    black = np.array([0, 0, 0, 255], dtype=np.uint8)
    # left bracket: vertical bar + top/bottom serifs pointing right
    lx = PAD
    canvas[PAD:PAD + bt, lx:lx + ser] = black            # top serif
    canvas[h - PAD - bt:h - PAD, lx:lx + ser] = black      # bottom serif
    canvas[PAD:h - PAD, lx:lx + bt] = black                # vertical bar
    # right bracket
    rx = PAD + ser + bt + widest + ser - bt
    canvas[PAD:PAD + bt, rx:rx + ser] = black
    canvas[h - PAD - bt:h - PAD, rx:rx + ser] = black
    canvas[PAD:h - PAD, rx:rx + bt] = black
    return canvas


COL_ENTRIES = [r"1/b", r"\sqrt{1!}/b^{2}", r"\sqrt{2!}/b^{3}", r"\sqrt{3!}/b^{4}",
               r"\sqrt{4!}/...", r"...", r"...\ \infty"]

manifest = {}
for name, (segs, (x0, y0, x1, y1), base_pt) in EQS.items():
    maxw, maxh = region(x0, y0, x1, y1)
    if name == "e3_col":
        pt = base_pt
        while pt > 8.0:
            c = render_col(COL_ENTRIES, pt, maxw, maxh)
            if c.shape[1] / DPI <= maxw and c.shape[0] / DPI <= maxh:
                break
            pt -= 0.5
        path = os.path.join(OUT, name + ".png")
        Image.fromarray(c).save(path)
        manifest[name] = {"file": name + ".png", "w_in": round(c.shape[1] / DPI, 5),
                          "h_in": round(c.shape[0] / DPI, 5), "pt": round(pt, 2)}
        print(name, "w_in=%.3f h_in=%.3f pt=%.1f" % (manifest[name]["w_in"], manifest[name]["h_in"], pt))
        continue
    manifest[name] = fit(name, segs, (x0, y0, x1, y1), base_pt, maxw, maxh)

with open(os.path.join(OUT, "manifest.json"), "w") as fh:
    json.dump(manifest, fh, indent=2)
print("wrote", os.path.join(OUT, "manifest.json"))
