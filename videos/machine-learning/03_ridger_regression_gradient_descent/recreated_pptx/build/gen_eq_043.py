#!/usr/bin/env python3
"""Equation/vector asset generator for slide 043 (attempt 3 rebuild).

Renders 2D stacked-vector equations as 600 dpi transparent PNGs from segments:
  {"t": latex}            inline mathtext run
  {"col": [..]}           stacked column vector inside drawn curved parens
Each segment carries its own color. Output + JSON sidecar (same contract as
scripts/render_eq.py: w_px/h_px/w_in/h_in/baseline_frac/fontsize_pt/color).

The FRAME (unique_slides/slide_043.jpg) is the transcription source; several
analysis-spec equations are wrong vs the frame (see build header), so the
values below are the frame-read ones.

Run: python3 gen_eq_043.py
"""
import json
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageDraw

DPI = 600
PAD = 8
FW, FH = 10.0, 2.5
OUTDIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")
os.makedirs(OUTDIR, exist_ok=True)


def render_text(latex, fontsize, color):
    fig = plt.figure(figsize=(FW, FH), dpi=DPI)
    fig.patch.set_alpha(0.0)
    fig.text(0.05, 0.5, f"${latex}$", fontsize=fontsize, color=color,
             ha="left", va="baseline")
    fig.canvas.draw()
    buf = np.asarray(fig.canvas.buffer_rgba()).copy()
    plt.close(fig)
    H = buf.shape[0]
    base = int(round(H * 0.5))
    ink = buf[:, :, 3] > 8
    rows = np.where(ink.any(axis=1))[0]
    cols = np.where(ink.any(axis=0))[0]
    if len(rows) == 0:
        raise SystemExit(f"no ink for {latex!r}")
    y0, y1 = max(rows[0] - PAD, 0), min(rows[-1] + PAD, H)
    x0, x1 = max(cols[0] - PAD, 0), min(cols[-1] + PAD, buf.shape[1])
    return buf[y0:y1, x0:x1], base - y0


def paren_layer(h, w, stroke, side):
    lay = Image.new("RGBA", (2 * w + h // 3, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    bbox = (0, 0, 2 * w, h - 1)
    if side < 0:
        d.arc(bbox, 90, 270, fill=(0, 0, 0, 255), width=stroke)
    else:
        d.arc(bbox, -90, 90, fill=(0, 0, 0, 255), width=stroke)
    return np.asarray(lay.crop(lay.getbbox()))


def compose(spec):
    fs = spec["fontsize"]
    parts = []
    for s in spec["segments"]:
        col = "#" + s.get("color", "000000").lstrip("#")
        if "t" in s:
            arr, bl = render_text(s["t"], fs, col)
            parts.append({"arr": arr, "bl": bl})
        elif "col" in s:
            entries = [render_text(e, fs, col) for e in s["col"]]
            efs_px = fs / 72 * DPI
            gap = max(3, int(round(efs_px * spec.get("col_gap_frac", 0.10))))
            wmax = max(a.shape[1] for a, b in entries)
            H = sum(a.shape[0] for a, b in entries) + gap * (len(entries) - 1)
            stack = np.zeros((H, wmax, 4), dtype=np.uint8)
            bls = []
            y = 0
            for a, b in entries:
                xoff = (wmax - a.shape[1]) // 2
                stack[y:y + a.shape[0], xoff:xoff + a.shape[1]] = a
                bls.append(y + b)
                y += a.shape[0] + gap
            stroke = max(3, int(round(efs_px * spec.get("col_stroke_frac", 0.09))))
            pw = max(6, int(round(efs_px * spec.get("col_bow_frac", 0.18))))
            pad = spec.get("col_pad", 4)
            span = stack.shape[0] + 2 * pad
            lp = paren_layer(span, pw, stroke, -1)
            rp = paren_layer(span, pw, stroke, 1)
            colw = lp.shape[1] + 4 + stack.shape[1] + 4 + rp.shape[1]
            arr = np.zeros((span, colw, 4), dtype=np.uint8)
            top = (span - stack.shape[0]) // 2
            arr[:, :lp.shape[1]] = lp
            xs = lp.shape[1] + 4
            arr[top:top + stack.shape[0], xs:xs + stack.shape[1]] = stack
            arr[:, xs + stack.shape[1] + 4:xs + stack.shape[1] + 4 + rp.shape[1]] = rp
            bl = top + bls[len(bls) // 2]
            parts.append({"arr": arr, "bl": bl})
        else:
            raise SystemExit(f"bad segment {s}")

    above = max(p["bl"] for p in parts)
    below = max(p["arr"].shape[0] - p["bl"] for p in parts)
    H = above + below
    W = sum(p["arr"].shape[1] for p in parts)
    canvas = np.zeros((H, W, 4), dtype=np.uint8)
    x = 0
    for p in parts:
        canvas[above - p["bl"]:above - p["bl"] + p["arr"].shape[0],
               x:x + p["arr"].shape[1]] = p["arr"]
        x += p["arr"].shape[1]
    a = canvas[:, :, 3] > 8
    rows = np.where(a.any(axis=1))[0]
    cols = np.where(a.any(axis=0))[0]
    canvas = canvas[rows[0]:rows[-1] + 1, cols[0]:cols[-1] + 1]
    h, w = canvas.shape[:2]
    base_row = above - rows[0]
    info = {"w_px": w, "h_px": h, "w_in": round(w / DPI, 5),
            "h_in": round(h / DPI, 5), "dpi": DPI, "fontsize_pt": fs,
            "baseline_px": int(base_row),
            "baseline_frac": round(base_row / h, 5)}
    tw = spec.get("target_w_in")
    if tw:
        nw = int(round(tw * DPI))
        nh = max(1, int(round(h * nw / w)))
        canvas = np.asarray(Image.fromarray(canvas).resize((nw, nh), Image.LANCZOS))
        info.update(w_px=nw, h_px=nh, w_in=round(nw / DPI, 5),
                    h_in=round(nh / DPI, 5),
                    baseline_px=int(round(base_row * nh / h)),
                    baseline_frac=round(base_row * nh / h / nh, 5))
    out = os.path.join(OUTDIR, spec["name"] + ".png")
    Image.fromarray(canvas).save(out)
    info.update(image=spec["name"] + ".png", path=out,
                color=spec.get("color", "multi"))
    with open(os.path.join(OUTDIR, spec["name"] + ".json"), "w") as fh:
        json.dump(info, fh, indent=1)
    print(f"{spec['name']}: {info['w_px']}x{info['h_px']}px "
          f"({info['w_in']}x{info['h_in']}in)")


BLACK, RED, BLUE, GREEN = "000000", "C00000", "0000FF", "008000"
FS = 11.0

SPECS = [
    # ---- d(x_i) equations (frame values; 3-entry column vectors) ----
    {"name": "eq043_dx1", "fontsize": FS, "target_w_in": 166 / 72,
     "segments": [{"t": "d(x_1) = "}, {"t": "\\left|1\\;1\\;1\\right|", "color": RED},
                  {"col": ["4", "-10", "-8"], "color": GREEN}, {"t": " = -14"}]},
    {"name": "eq043_dx2", "fontsize": FS, "target_w_in": 160 / 72,
     "segments": [{"t": "d(x_2) = "}, {"t": "\\left|1\\;2\\;1\\right|", "color": RED},
                  {"col": ["6", "-8", "-6"], "color": GREEN}, {"t": " = -14"}]},
    {"name": "eq043_dx3", "fontsize": FS, "target_w_in": 155 / 72,
     "segments": [{"t": "d(x_3) = "}, {"t": "\\left|1\\;1\\;2\\right|", "color": RED},
                  {"col": ["8", "-4", "-4"], "color": GREEN}, {"t": " = -4"}]},
    {"name": "eq043_dx4", "fontsize": FS, "target_w_in": 145 / 72,
     "segments": [{"t": "d(x_4) = "}, {"t": "\\left|1\\;5\\;4\\right|", "color": BLUE},
                  {"col": ["10", "-2", "0"], "color": GREEN}, {"t": " = 0"}]},
    {"name": "eq043_dx5", "fontsize": FS, "target_w_in": 173 / 72,
     "segments": [{"t": "d(x_5) = "}, {"t": "\\left|1\\;6\\;5\\right|", "color": BLUE},
                  {"col": ["8", "-12", "-8"], "color": GREEN}, {"t": " = -104"}]},
    # frame prints d(x_5) again on row 6 (course typo) — verbatim per frame
    {"name": "eq043_dx6", "fontsize": FS, "target_w_in": 173 / 72,
     "segments": [{"t": "d(x_5) = "}, {"t": "\\left|1\\;6\\;6\\right|", "color": BLUE},
                  {"col": ["8", "-12", "-8"], "color": GREEN}, {"t": " = -112"}]},
    # ---- W update equations ----
    {"name": "eq043_w1", "fontsize": FS, "target_w_in": 156 / 72,
     "segments": [{"t": "\\underline{W} = "}, {"col": ["4", "-10", "-8"]},
                  {"t": "+ 2 ", "color": RED}, {"t": "\\,*"},
                  {"col": ["1", "1", "1"]},
                  {"t": " = "}, {"col": ["6", "-8", "-6"], "color": GREEN}]},
    {"name": "eq043_w2", "fontsize": FS, "target_w_in": 147 / 72,
     "segments": [{"t": "\\underline{W} = "}, {"col": ["6", "-8", "-6"]},
                  {"t": "+ 2 ", "color": RED}, {"t": "\\,*"},
                  {"col": ["1", "2", "1"]},
                  {"t": " = "}, {"col": ["8", "-4", "-4"], "color": GREEN}]},
    {"name": "eq043_w3", "fontsize": FS, "target_w_in": 148 / 72,
     "segments": [{"t": "\\underline{W} = "}, {"col": ["8", "-4", "-4"]},
                  {"t": "+ 2 ", "color": RED}, {"t": "\\,*"},
                  {"col": ["1", "1", "2"]},
                  {"t": " = "}, {"col": ["10", "-2", "-0"], "color": GREEN}]},
    {"name": "eq043_w4", "fontsize": FS, "target_w_in": 143 / 72,
     "segments": [{"t": "\\underline{W} = "}, {"col": ["10", "02", "0"]},
                  {"t": "- 2 ", "color": BLUE}, {"t": "\\,*", "color": BLUE},
                  {"col": ["1", "5", "4"]},
                  {"t": " = "}, {"col": ["8", "-12", "-8"], "color": GREEN}]},
    {"name": "eq043_w5", "fontsize": FS, "target_w_in": 56 / 72,
     "segments": [{"t": "\\underline{W} = "}, {"col": ["8", "-12", "-8"]}]},
    {"name": "eq043_w6", "fontsize": FS, "target_w_in": 56 / 72,
     "segments": [{"t": "\\underline{W} = "}, {"col": ["8", "-12", "-8"]}]},
    # ---- Initial W = (4; -2; -2) ----
    {"name": "eq043_initw", "fontsize": FS, "target_w_in": 24 / 72,
     "segments": [{"col": ["4", "-2", "-2"]}]},
    # ---- class-check matrix columns (0;0) (7;6) (3;2) ----
    {"name": "eq043_mx1", "fontsize": FS, "target_w_in": 15 / 72,
     "segments": [{"col": ["0", "0"]}]},
    {"name": "eq043_mx2", "fontsize": FS, "target_w_in": 15 / 72,
     "segments": [{"col": ["7", "6"]}]},
    {"name": "eq043_mx3", "fontsize": FS, "target_w_in": 15 / 72,
     "segments": [{"col": ["3", "2"]}]},
]

# ---- augmented-vector columns (6, all 3-entry) ----
AUG = [("a1", ["1", "1", "1"]), ("a2", ["1", "2", "1"]), ("a3", ["1", "1", "2"]),
       ("a4", ["1", "5", "4"]), ("a5", ["1", "6", "5"]), ("a6", ["1", "6", "6"])]
for tag, vals in AUG:
    SPECS.append({"name": "eq043_aug_" + tag, "fontsize": FS,
                  "target_w_in": 14 / 72, "segments": [{"col": vals}]})

if __name__ == "__main__":
    for s in SPECS:
        compose(s)
