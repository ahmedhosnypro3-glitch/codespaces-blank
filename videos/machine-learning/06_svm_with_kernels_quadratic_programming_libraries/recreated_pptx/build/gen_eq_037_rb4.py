#!/usr/bin/env python3
"""Slide 037 rebuild wave 4: segmented 2-D mathtext PNGs.

Each equation is rendered as horizontal segments at ONE shared font size so
the green highlight rects can sit exactly behind the highlighted term
segments (judge BLOCKER fix: no empty green placeholder boxes). Class-of-
vector lines additionally get a peach background rect behind the whole row.

Manifest: eq_037/s37rb4_manifest.json with per-segment absolute inch boxes.
"""
import importlib.util
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location(
    "render_math", os.path.join(HERE, "render_math.py"))
rm = importlib.util.module_from_spec(spec)
spec.loader.exec_module(rm)

EQDIR = os.path.join(HERE, "eq_037")
W_IN, H_IN = 13.33, 7.5
BASE_PT = 14.0
MAX_PT = 20.0

# name, spec box [x0,y0,x1,y1] normalized, segments [(latex, hl)] hl in {None,"green"};
# peach=True -> peach rect behind whole row
EQS = [
    ("s37rb4_lag_orig", [0.1, 0.2, 0.9, 0.28], [
        (r"L_D(\alpha) = \sum_{i=1}^{N} \alpha_i - \frac{1}{2} \sum_{i=1}^{N} \sum_{j=1}^{N} \alpha_i \alpha_j y_i y_j\;", None),
        (r"X_i^T X_j", "green"),
    ], False),
    ("s37rb4_w", [0.1, 0.3, 0.3, 0.35], [
        (r"w = \sum_{i=1}^{N} \alpha_i y_i X_i", None),
    ], False),
    ("s37rb4_b_orig", [0.35, 0.3, 0.9, 0.35], [
        (r"b = -\frac{1}{2}[\max_{i:y_i=-1}", None),
        (r"w^T X_i", "green"),
        (r"+ \min_{i:y_i=+1}", None),
        (r"w^T X_i", "green"),
        (r"]", None),
    ], False),
    ("s37rb4_cls_orig", [0.2, 0.4, 0.8, 0.45], [
        (r"\mathrm{Class\ of\ vector}\ Z \Rightarrow \mathrm{sign}(", None),
        (r"w^T Z", "green"),
        (r"+ b)", None),
    ], True),
    ("s37rb4_kernelize", [0.30, 0.50, 0.63, 0.56], [
        (r"\mathrm{Kernelize\ using}\;", None),
        (r"K(a,b) = [a^T b + 1]^d", None),
    ], False),
    ("s37rb4_lag_kern", [0.1, 0.64, 0.9, 0.72], [
        (r"L_D(\alpha) = \sum_{i=1}^{N} \alpha_i - \frac{1}{2} \sum_{i=1}^{N} \sum_{j=1}^{N} \alpha_i \alpha_j y_i y_j\;", None),
        (r"[X_i^T X_j + 1]^d", "green"),
    ], False),
    ("s37rb4_b_kern", [0.35, 0.73, 0.9, 0.78], [
        (r"b = -\frac{1}{2}[\max_{i:y_i=-1}", None),
        (r"[w^T X_i + 1]^d", "green"),
        (r"+ \min_{i:y_i=+1}", None),
        (r"[w^T X_i + 1]^d", "green"),
        (r"]", None),
    ], False),
    ("s37rb4_cls_kern", [0.2, 0.83, 0.8, 0.88], [
        (r"\mathrm{Class\ of\ vector}\ Z\ \mathrm{is}\ \mathrm{sign}(", None),
        (r"[w^T Z + 1]^d", "green"),
        (r"+ b)", None),
    ], True),
]


def main():
    os.makedirs(EQDIR, exist_ok=True)
    manifest = {}
    for name, box, segs, peach in EQS:
        x0, y0, x1, y1 = box
        bx, by = x0 * W_IN, y0 * H_IN
        bw, bh = (x1 - x0) * W_IN, (y1 - y0) * H_IN
        measured = [rm.measure_segment(latex, "#000000", BASE_PT) for latex, _ in segs]
        tot_w = sum(w for w, _ in measured)
        tot_h = max(h for _, h in measured)
        scale = min(bw / tot_w, bh / tot_h)
        pt = min(MAX_PT, BASE_PT * scale * 0.995)
        parts = [rm.render_segment(latex, "#000000", pt) for latex, _ in segs]
        parts = [(a, b / rm.DPI) for a, b in parts]  # baseline px -> inches
        base_max = max(b for _, b in parts)
        row_h = max(b + (a.shape[0] / rm.DPI - b) for a, b in parts)
        row_y = by + (bh - row_h) / 2.0
        seg_out, hl_out = [], []
        cx = bx
        for (arr, base), (latex, hl) in zip(parts, segs):
            w_in, h_in = arr.shape[1] / rm.DPI, arr.shape[0] / rm.DPI
            sy = row_y + (base_max - base)
            img = f"{name}_s{len(seg_out)}.png"
            rm.Image.fromarray(arr).save(os.path.join(EQDIR, img))
            seg_out.append({"image": img, "x": round(cx, 4), "y": round(sy, 4),
                            "w": round(w_in, 4), "h": round(h_in, 4)})
            if hl == "green":
                hl_out.append({"x": round(cx - 0.06, 4), "y": round(row_y, 4),
                               "w": round(w_in + 0.12, 4), "h": round(row_h, 4),
                               "color": "90EE90"})
            cx += w_in
        entry = {"box": [round(bx, 4), round(by, 4), round(bw, 4), round(bh, 4)],
                 "row": {"x": round(bx, 4), "y": round(row_y, 4),
                         "w": round(cx - bx, 4), "h": round(row_h, 4)},
                 "segments": seg_out, "highlights": hl_out, "pt": round(pt, 2)}
        if peach:
            entry["peach"] = {"x": round(bx - 0.30, 4), "y": round(row_y - 0.12, 4),
                              "w": round(cx - bx + 0.60, 4), "h": round(row_h + 0.24, 4),
                              "color": "FFDAB9"}
        manifest[name] = entry
        print(name, "pt", entry["pt"], "row_w", entry["row"]["w"], "x", entry["row"]["h"])
    with open(os.path.join(EQDIR, "s37rb4_manifest.json"), "w") as fh:
        json.dump(manifest, fh, indent=2)


if __name__ == "__main__":
    main()
