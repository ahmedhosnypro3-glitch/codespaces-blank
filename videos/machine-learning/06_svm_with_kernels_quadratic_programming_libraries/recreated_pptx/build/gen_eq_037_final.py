#!/usr/bin/env python3
"""Slide 037 final equation PNGs: braced side-limit sums ({sum}_{i=1}^{N})
match the original's wide/short equation aspect; each PNG is sized to fill its
spec box height so the original-measured highlight rects land on the terms.
Assets: eq_037/s37f_*.png + s37f_manifest.json. Content verbatim from
qa/reanalysis2/slide_037_analysis.txt section 8.
"""
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
EQDIR = os.path.join(HERE, "eq_037")
RENDER = os.path.join(HERE, "render_math.py")

# name, latex row, spec box [x0,y0,x1,y1] norm, left-x of original ink (norm)
EQS = [
    ("s37f_lag_orig",
     r"#000000:L_D(\alpha) = {\sum}_{i=1}^{N} \alpha_i - \frac{1}{2} {\sum}_{i=1}^{N}{\sum}_{j=1}^{N} \alpha_i \alpha_j y_i y_j X_i^T X_j",
     [0.1, 0.2, 0.9, 0.28], 0.103),
    ("s37f_w",
     r"#000000:w = {\sum}_{i=1}^{N} \alpha_i y_i X_i",
     [0.1, 0.3, 0.3, 0.35], 0.106),
    ("s37f_b_orig",
     r"#000000:b = -\frac{1}{2}\left[\max_{i:y_i=-1} w^T X_i + \min_{i:y_i=+1} w^T X_i\right]",
     [0.35, 0.3, 0.9, 0.35], 0.380),
    ("s37f_cls_orig",
     r"#000000:\mathrm{Class\ of\ vector}\ Z \Rightarrow \mathrm{sign}(w^T Z + b)",
     [0.2, 0.4, 0.8, 0.45], 0.205),
    ("s37f_kernelize",
     r"#000000:\mathrm{Kernelize\ using}\ K(a,b) = [a^T b + 1]^d",
     [0.4, 0.5, 0.75, 0.55], 0.312),
    ("s37f_lag_kern",
     r"#000000:L_D(\alpha) = {\sum}_{i=1}^{N} \alpha_i - \frac{1}{2} {\sum}_{i=1}^{N}{\sum}_{j=1}^{N} \alpha_i \alpha_j y_i y_j [X_i^T X_j + 1]^d",
     [0.1, 0.64, 0.9, 0.72], 0.103),
    ("s37f_b_kern",
     r"#000000:b = -\frac{1}{2}\left[\max_{i:y_i=-1} [w^T X_i + 1]^d + \min_{i:y_i=+1} [w^T X_i + 1]^d\right]",
     [0.35, 0.73, 0.9, 0.78], 0.358),
    ("s37f_cls_kern",
     r"#000000:\mathrm{Class\ of\ vector}\ Z\ \mathrm{is}\ \mathrm{sign}([w^T Z + 1]^d + b)",
     [0.2, 0.83, 0.8, 0.88], 0.205),
]

W, H = 13.33, 7.5


def main():
    os.makedirs(EQDIR, exist_ok=True)
    manifest = {}
    for name, row, box, ink_x0 in EQS:
        x0, y0, x1, y1 = box
        maxw = (x1 - x0) * W
        maxh = (y1 - y0) * H
        out = os.path.join(EQDIR, name + ".png")
        js = os.path.join(EQDIR, name + ".json")
        subprocess.run([
            sys.executable, RENDER, "--out", out, "--size", "40",
            "--maxw", str(maxw), "--maxh", str(maxh * 0.98),
            "--row", row, "--out-json", js,
        ], check=True, cwd=HERE)
        with open(js) as fh:
            info = json.load(fh)
        w_in, h_in = info["w_in"], info["h_in"]
        x = ink_x0 * W
        y = y0 * H + ((y1 - y0) * H - h_in) / 2
        manifest[name] = {"image": name + ".png", "x": round(x, 4),
                          "y": round(y, 4), "w_in": w_in, "h_in": h_in}
        print(name, "w_in=%.3f h_in=%.3f x=%.3f y=%.3f" % (w_in, h_in, x, y))
    with open(os.path.join(EQDIR, "s37f_manifest.json"), "w") as f:
        json.dump(manifest, f, indent=2)


if __name__ == "__main__":
    main()
