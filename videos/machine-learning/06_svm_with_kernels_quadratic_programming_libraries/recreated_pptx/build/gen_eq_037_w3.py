#!/usr/bin/env python3
"""Fresh 600-dpi mathtext PNGs for slide 037 fix-2 (display style, roomier boxes).

Equations from qa/reanalysis2/slide_037_analysis.txt section 8. Assets:
eq_037/s37w3_*.png + s37w3_manifest.json. All rows prefixed \\displaystyle so
summation limits stack above/below the sigma (professional 2-D format).
"""
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
EQDIR = os.path.join(HERE, "eq_037")
RENDER = os.path.join(HERE, "render_math.py")

EQS = [
    ("s37w3_lag_orig",
     r"#000000:\displaystyle L_D(\alpha) = \sum_{i=1}^{N} \alpha_i - \frac{1}{2} \sum_{i=1}^{N} \sum_{j=1}^{N} \alpha_i \alpha_j y_i y_j X_i^T X_j",
     [0.1, 0.19, 0.9, 0.285]),
    ("s37w3_w",
     r"#000000:\displaystyle w = \sum_{i=1}^{N} \alpha_i y_i X_i",
     [0.1, 0.3, 0.3, 0.35]),
    ("s37w3_b_orig",
     r"#000000:\displaystyle b = -\frac{1}{2}\left[\max_{i:y_i=-1} w^T X_i + \min_{i:y_i=+1} w^T X_i\right]",
     [0.35, 0.295, 0.9, 0.355]),
    ("s37w3_cls_orig",
     r"#000000:\displaystyle \mathrm{Class\ of\ vector}\ Z \Rightarrow \mathrm{sign}(w^T Z + b)",
     [0.2, 0.39, 0.8, 0.46]),
    ("s37w3_kernelize",
     r"#000000:\displaystyle \mathrm{Kernelize\ using}\ ||#000000:\displaystyle K(a,b) = [a^T b + 1]^d",
     [0.4, 0.5, 0.75, 0.55]),
    ("s37w3_lag_kern",
     r"#000000:\displaystyle L_D(\alpha) = \sum_{i=1}^{N} \alpha_i - \frac{1}{2} \sum_{i=1}^{N} \sum_{j=1}^{N} \alpha_i \alpha_j y_i y_j \left[X_i^T X_j + 1\right]^d",
     [0.1, 0.635, 0.9, 0.725]),
    ("s37w3_b_kern",
     r"#000000:\displaystyle b = -\frac{1}{2}\left[\max_{i:y_i=-1} [w^T X_i + 1]^d + \min_{i:y_i=+1} [w^T X_i + 1]^d\right]",
     [0.35, 0.72, 0.9, 0.79]),
    ("s37w3_cls_kern",
     r"#000000:\displaystyle \mathrm{Class\ of\ vector}\ Z\ \mathrm{is}\ \mathrm{sign}([w^T Z + 1]^d + b)",
     [0.2, 0.82, 0.8, 0.89]),
]

SIZE = 14.0


def main():
    os.makedirs(EQDIR, exist_ok=True)
    manifest = {}
    for name, row, box in EQS:
        x0, y0, x1, y1 = box
        maxw = (x1 - x0) * 13.33
        maxh = (y1 - y0) * 7.5
        out = os.path.join(EQDIR, name + ".png")
        js = os.path.join(EQDIR, name + ".json")
        subprocess.run([
            sys.executable, RENDER,
            "--out", out, "--size", str(SIZE),
            "--maxw", str(maxw), "--maxh", str(maxh),
            "--row", row,
            "--out-json", js,
        ], check=True, cwd=HERE)
        with open(js) as fh:
            info = json.load(fh)
        manifest[name] = {
            "image": name + ".png",
            "box": [round(x0 * 13.33, 4), round(y0 * 7.5, 4),
                    round((x1 - x0) * 13.33, 4), round((y1 - y0) * 7.5, 4)],
            "w_in": info["w_in"], "h_in": info["h_in"],
            "fontsize_pt": info["fontsize_pt"],
        }
        print(name, info["w_in"], "x", info["h_in"], "in @", info["fontsize_pt"], "pt")
    with open(os.path.join(EQDIR, "s37w3_manifest.json"), "w") as fh:
        json.dump(manifest, fh, indent=2)


if __name__ == "__main__":
    main()
