#!/usr/bin/env python3
"""Equation/vector asset generator for slide 044 (12-item prephase rebuild).

Renders 2D dot-product equation fragments as 600 dpi transparent PNGs + sidecars
(same contract as scripts/render_eq.py, plus a bare "image" field; the build uses
ASSETS + m.image). Multi-color equations are emitted as separate fragment PNGs
placed cumulatively by build/slide_044.js.

Content is the PIL-arbitrated frame ground truth (qa/slide044/prephase/delta_vs_related.md
per-band table + orig_judges transcripts): dot-product form, class-colored raised
row vectors (RED boxes 1-3 / BLUE boxes 4-6), GREEN W/result columns, RED "+ 2 *"
on update rows, box 6 prints -112 verbatim (the original's own typo).

Run: python3 gen_eq_044.py   (from anywhere; paths are __file__-relative)
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
FW, FH = 12.0, 3.0
OUTDIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")
os.makedirs(OUTDIR, exist_ok=True)

BLACK, RED, BLUE, GREEN = "000000", "C00000", "0000C8", "009A4A"
FS = 14.0


def render_text(latex, fontsize, color):
    fig = plt.figure(figsize=(FW, FH), dpi=DPI)
    fig.patch.set_alpha(0.0)
    fig.text(0.05, 0.5, f"${latex}$", fontsize=fontsize, color=color,
             ha="left", va="baseline")
    probe = fig.text(0.01, 0.5, "x", fontsize=fontsize, color=color,
                     ha="left", va="baseline")
    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()
    pb = probe.get_window_extent(renderer=renderer)
    buf = np.asarray(fig.canvas.buffer_rgba()).copy()
    plt.close(fig)
    H = buf.shape[0]
    ink = buf[:, :, 3] > 8
    px0 = max(int(pb.x0) - 2, 0)
    px1 = int(pb.x1) + 2
    rows = np.where(ink[:, px0:px1].any(axis=1))[0]
    baseline_row = int(rows[-1])
    ink[:, :px1] = False  # drop the probe entirely (it sits left of the equation)
    er = np.where(ink.any(axis=1))[0]
    cols = np.where(ink.any(axis=0))[0]
    y0, y1 = max(er[0] - PAD, 0), min(er[-1] + PAD, H)
    x0, x1 = max(cols[0] - PAD, 0), min(cols[-1] + PAD, buf.shape[1])
    return buf[y0:y1, x0:x1], baseline_row - y0


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
        col = "#" + s.get("color", spec.get("color", BLACK)).lstrip("#")
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
        y0 = above - p["bl"]
        canvas[y0:y0 + p["arr"].shape[0], x:x + p["arr"].shape[1]] = p["arr"]
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
    out = os.path.join(OUTDIR, spec["name"] + ".png")
    Image.fromarray(canvas).save(out)
    info.update(image=spec["name"] + ".png", path=out,
                color=spec.get("color", "multi"), mathtext=spec.get("note", ""))
    with open(os.path.join(OUTDIR, spec["name"] + ".json"), "w") as fh:
        json.dump(info, fh, indent=1)
    print(f"{spec['name']}: {w}x{h}px ({info['w_in']}x{info['h_in']}in) bf={info['baseline_frac']}")


# Per-band frame ground truth: (subscript, row vector, W column, result, class color)
DX = [
    ("1", ["1", "1", "1"], ["8", "-12", "-8"], "-12", RED),
    ("2", ["1", "2", "1"], ["10", "-10", "-6"], "-16", RED),
    ("3", ["1", "1", "2"], ["12", "-6", "-4"], "-2", RED),
    ("4", ["1", "5", "4"], ["14", "-4", "0"], "-6", BLUE),
    ("5", ["1", "6", "5"], ["14", "-4", "0"], "-10", BLUE),
    ("6", ["1", "6", "6"], ["14", "-4", "0"], "-112", BLUE),  # original's own typo, verbatim
]
# Update equations rows 1-3: (old W, x column, result)
WU = [
    (["8", "-12", "-8"], ["1", "1", "1"], ["10", "-10", "-6"]),
    (["10", "-10", "-6"], ["1", "2", "1"], ["12", "-6", "-4"]),
    (["12", "-6", "-4"], ["1", "1", "2"], ["14", "-4", "0"]),
]

SPECS = []
for i, (sub, row, wcol, val, cls) in enumerate(DX, 1):
    SPECS.append({"name": f"eq_044_dx{i}_a", "fontsize": FS, "color": BLACK,
                  "segments": [{"t": f"d(x_{{{sub}}}) ="}]})
    SPECS.append({"name": f"eq_044_dx{i}_b", "fontsize": FS, "color": cls,
                  "segments": [{"t": "(" + "\\;\\;".join(row) + ")"}]})
    SPECS.append({"name": f"eq_044_dx{i}_c", "fontsize": FS, "color": GREEN,
                  "segments": [{"col": wcol}]})
    SPECS.append({"name": f"eq_044_dx{i}_d", "fontsize": FS, "color": BLACK,
                  "segments": [{"t": f"= {val}"}]})

for j, (old, xcol, res) in enumerate(WU, 1):
    SPECS.append({"name": f"eq_044_w{j}_a", "fontsize": FS, "color": BLACK,
                  "segments": [{"t": "\\underline{W} ="}]})
    SPECS.append({"name": f"eq_044_w{j}_b", "fontsize": FS, "color": BLACK,
                  "segments": [{"col": old}]})
    SPECS.append({"name": f"eq_044_w{j}_c", "fontsize": FS, "color": RED,
                  "segments": [{"t": "+ 2 *"}]})
    SPECS.append({"name": f"eq_044_w{j}_d", "fontsize": FS, "color": BLACK,
                  "segments": [{"col": xcol}]})
    SPECS.append({"name": f"eq_044_w{j}_e", "fontsize": FS, "color": BLACK,
                  "segments": [{"t": "="}]})
    SPECS.append({"name": f"eq_044_w{j}_f", "fontsize": FS, "color": GREEN,
                  "segments": [{"col": res}]})

for j in (4, 5, 6):
    SPECS.append({"name": f"eq_044_w{j}_a", "fontsize": FS, "color": BLACK,
                  "segments": [{"t": "\\underline{W} = "}, {"col": ["14", "-4", "0"]}]})

SPECS.append({"name": "eq_044_arrD", "fontsize": FS, "color": RED,
              "segments": [{"t": "\\Rightarrow"}]})
SPECS.append({"name": "eq_044_arrDk", "fontsize": FS, "color": BLACK,
              "segments": [{"t": "\\Rightarrow"}]})
SPECS.append({"name": "eq_044_arrL", "fontsize": FS, "color": RED,
              "segments": [{"t": "\\Leftarrow"}]})

if __name__ == "__main__":
    for s in SPECS:
        compose(s)
    print("OK", len(SPECS), "assets")
