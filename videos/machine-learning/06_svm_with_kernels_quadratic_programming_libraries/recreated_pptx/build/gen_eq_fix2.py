#!/usr/bin/env python3
"""Regenerate eq_031/ and eq_032/ PNGs with eq_render_fix (single-figure
baseline-aligned segments). Same manifest schemas as before:
eq_031: x,y = spec box top-left; eq_032: x,y = centered inside spec box."""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import eq_render_fix as R
from PIL import Image

BUILD = os.path.dirname(os.path.abspath(__file__))
W, H = 13.33, 7.5

EQS_031 = {
    "eq1": ("CC0000:\\boldsymbol{K}||000000:(a,b)=||CC0000:a^{T}b",
            (0.121, 0.246, 0.217, 0.289), 2.80),
    "eq2": ("CC0000:\\boldsymbol{K}||000000:(a,b)=[||CC0000:a^{T}b||000000:]^{2}",
            (0.125, 0.387, 0.235, 0.431), 2.60),
    "eq3": ("CC0000:\\boldsymbol{K}||000000:(a,b)=[||CC0000:a^{T}b||000000: + 1]^{2}",
            (0.408, 0.387, 0.535, 0.431), 3.30),
    "eq4": ("CC0000:\\boldsymbol{K}||000000:(a,b)=[||CC0000:a^{T}b||CC0000:]^{d}",
            (0.121, 0.533, 0.238, 0.580), 2.70),
    "eq5": ("CC0000:\\boldsymbol{K}||000000:(a,b)=[||CC0000:a^{T}b||000000: + 1||CC0000:]^{d}",
            (0.408, 0.533, 0.560, 0.580), 3.30),
    "eq6": ("CC0000:\\boldsymbol{K}||000000:(a,b)=[||CC0000:e^{-\\gamma\\|a-b\\|^{2}}||000000:]",
            (0.129, 0.717, 0.333, 0.770), 4.60),
    "eq_phi": ("CC0000:\\mathrm{No\\ Mapping,\\ }\\varphi(x)=\\ x",
               (0.344, 0.250, 0.517, 0.291), 2.30),
}

EQS_032 = {
    "eq1": ("0000FF:K(a,b)||000000: = ||008000:K_{1}(a,b)||000000: + ||FF0000:K_{2}(a,b)",
            (0.10, 0.29, 0.90, 0.41), 8.0),
    "eq2": ("0000FF:K(a,b)||000000: = ||FF0000:\\alpha\\,||008000:K_{1}(a,b)",
            (0.10, 0.51, 0.75, 0.58), 6.5),
    "eq3": ("0000FF:K(a,b)||000000: = ||008000:K_{1}(a,b)||000000: \\ast ||FF0000:K_{2}(a,b)",
            (0.10, 0.67, 0.85, 0.75), 7.5),
    "eq4": ("0000FF:K(a,b)||000000: = ||008000:K_{1}(a,b)||000000: \\ast ||FF0000:K_{2}(a,b)||000000: + ||FF0000:\\alpha\\,K_{3}(a,b)",
            (0.10, 0.84, 0.92, 0.92), 8.5),
}


def fit_pt(row, box_w, box_h, cap_w, probe_pt=22.0):
    c = R.render_row(row, probe_pt)
    ink = c[:, :, 3] > 40
    ys, xs = np.nonzero(ink)
    ink_w = (xs.max() - xs.min() + 1) / R.DPI
    ink_h = (ys.max() - ys.min() + 1) / R.DPI
    pt_h = probe_pt * (0.85 * box_h) / ink_h
    pt_w = probe_pt * min(cap_w, box_w) / ink_w
    return min(pt_h, pt_w, 42.0)


def gen(out_dir, eqs, center):
    os.makedirs(out_dir, exist_ok=True)
    manifest = {}
    for name, (row, b, cap_w) in eqs.items():
        bx, by = b[0] * W, b[1] * H
        bw, bh = (b[2] - b[0]) * W, (b[3] - b[1]) * H
        pt = fit_pt(row, bw, bh, cap_w)
        path = os.path.join(out_dir, name + ".png")
        w_in, h_in = R.save_png(row, pt, path)
        x, y = (bx + (bw - w_in) / 2, by + (bh - h_in) / 2) if center else (bx, by)
        manifest[name] = {"file": name + ".png", "x": round(x, 4), "y": round(y, 4),
                          "w_in": round(w_in, 5), "h_in": round(h_in, 5), "pt": round(pt, 2)}
        print(name, "w_in=%.3f h_in=%.3f pt=%.1f" % (w_in, h_in, pt))
    with open(os.path.join(out_dir, "manifest.json"), "w") as fh:
        json.dump(manifest, fh, indent=2)


gen(os.path.join(BUILD, "eq_031"), EQS_031, center=False)
gen(os.path.join(BUILD, "eq_032"), EQS_032, center=True)
