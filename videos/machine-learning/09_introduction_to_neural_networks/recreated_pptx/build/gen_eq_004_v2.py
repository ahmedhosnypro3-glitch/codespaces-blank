#!/usr/bin/env python3
"""Slide-004 equation PNGs (600 dpi, tight transparent, 2D professional format).
Each Sigma limit is composed as a RED ITALIC label under the Sigma glyph.
Auto-fits fontsize so the composed ink width equals the measured original ink width.
Emits eq_004_metrics.json (ink bbox in px) consumed by slide_004.js.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
import os
import json

OUT = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/recreated_pptx/build"
DPI = 600
CW, CH = 9.0, 3.0          # fixed canvas (inches) -- cropped to ink afterwards
AX, AY = 0.10, 0.55        # text anchor: left/baseline
RED = "#c00000"

plt.rcParams["font.family"] = "DejaVu Sans"


def _fig():
    fig = plt.figure(figsize=(CW, CH), dpi=DPI)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    return fig, ax


def _render(ax, tex, fs, color, x=AX, y=AY, ha="left", va="baseline"):
    ax.text(x, y, tex, ha=ha, va=va, fontsize=fs, color=color)


def ink_bbox_of(fig):
    fig.canvas.draw()
    tmp = os.path.join(OUT, "_tmp_004.png")
    fig.savefig(tmp, dpi=DPI, transparent=True)
    plt.close(fig)
    im = Image.open(tmp).convert("RGBA")
    a = np.asarray(im)[:, :, 3]
    ys, xs = np.nonzero(a > 8)
    if len(xs) == 0:
        return None, None
    return im, [int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())]


def render_small(tex, fs, color="#000000"):
    """Render one mathtext string on the fixed canvas; return (img, inkbbox)."""
    fig, ax = _fig()
    _render(ax, tex, fs, color)
    return ink_bbox_of(fig)


def render_marker(tex, fs):
    """Render main-with-dummy-subscript to locate the Sigma subscript box."""
    fig, ax = _fig()
    _render(ax, tex, fs, "#000000")
    return ink_bbox_of(fig)


def column_runs(bb, gap=6):
    if bb is None:
        return []
    cols = range(bb[0], bb[2] + 1)
    runs, cur = [], None
    for c in cols:
        if cur is None:
            cur = [c, c]
        elif c - cur[1] <= gap + 1:
            cur[1] = c
        else:
            runs.append(tuple(cur)); cur = [c, c]
    if cur:
        runs.append(tuple(cur))
    return runs


# key -> (main mathtext, limit mathtext or None, target ink LEFT x in, target ink WIDTH in)
SPECS = {
    "eq_error": (r"$\mathrm{Error} = \sum \delta_i W^T X_i$",
                 r"$\mathit{all\ misclassified\ vectors\ }(i)$", 1.11, 3.64),
    "eq_gradient": (r"$\frac{\partial \mathrm{Error}}{\partial W} = \sum \delta_i X_i$",
                    r"$\mathit{misclassified\ vectors}$", 7.10, 3.47),
    "eq_update_batch": (r"$W^{\mathrm{(updated)}} = W^{\mathrm{(old)}} - \eta \sum \delta_i X_i$",
                        r"$\mathit{misclassified\ vectors\ ONLY\ }(i)$", 1.19, 4.86),
    "eq_update": (r"$W^{\mathrm{(updated)}} = W^{\mathrm{(old)}} - \eta \frac{\partial \mathrm{Error}}{\partial W}$",
                  None, 1.15, 3.52),
    "eq_update_online": (r"$W^{\mathrm{(updated)}} = W^{\mathrm{(old)}} - \eta \delta_i X_i$",
                         None, 9.14, 3.03),
}


def compose(key, main_tex, limit_tex, target_w, fs=22.0, iters=4):
    """Auto-fit fontsize so composed ink width == target_w inches."""
    for _ in range(iters):
        if limit_tex:
            sigma_img, sigma_bb = render_small(r"$\sum$", fs)
            _, marker_bb = render_marker(main_tex.replace(r"\sum", r"\sum_{\mathrm{X}}"), fs)
            # dummy subscript box: ink strictly below the Sigma's bottom row
            rows_below = marker_bb[3]
            _, xsub_bb = render_marker(main_tex.replace(r"\sum", r"\sum_{\mathrm{X}}"), fs)
            # locate the X: rows below sigma bottom
            fig, ax = _fig()
            _render(ax, main_tex.replace(r"\sum", r"\sum_{\mathrm{X}}"), fs, "#000000")
            fig.canvas.draw()
            tmp = os.path.join(OUT, "_tmp_004.png")
            fig.savefig(tmp, dpi=DPI, transparent=True)
            plt.close(fig)
            m = np.asarray(Image.open(tmp).convert("RGBA"))[:, :, 3]
            y0 = sigma_bb[3] + 3
            sub = m[y0:, :]
            ys2, xs2 = np.nonzero(sub > 8)
            xL, xR = xs2.min(), xs2.max()
            yT = y0 + ys2.min()
            sig_w = sigma_bb[2] - sigma_bb[0]
            lim_x = sigma_bb[0] + 0.45 * sig_w     # limit sits under the Sigma centre
            lim_y = yT
            fig, ax = _fig()
            _render(ax, main_tex, fs, "#000000")
            _render(ax, limit_tex, fs * 0.60, RED, x=lim_x / (DPI * CW), y=1.0 - lim_y / (DPI * CH),
                    ha="left", va="top")
            im, bb = ink_bbox_of(fig)
        else:
            fig, ax = _fig()
            _render(ax, main_tex, fs, "#000000")
            im, bb = ink_bbox_of(fig)
        if bb is None:
            raise RuntimeError(key + ": no ink")
        w_in = (bb[2] - bb[0]) / DPI
        if abs(w_in - target_w) < 0.004:
            break
        fs *= target_w / w_in
    return im, bb, fs


meta = {}
for key, (main_tex, limit_tex, tx0, tw) in SPECS.items():
    im, bb, fs = compose(key, main_tex, limit_tex, tw)
    pxW, pxH = im.size
    path = os.path.join(OUT, key + ".png")
    im.save(path)
    meta[key] = {
        "file": key + ".png",
        "pxW": pxW, "pxH": pxH,
        "inkLeft": bb[0], "inkTop": bb[1], "inkRight": bb[2], "inkBottom": bb[3],
        "inkW_in": (bb[2] - bb[0]) / DPI, "inkH_in": (bb[3] - bb[1]) / DPI,
        "fontsize": round(fs, 2),
        "targetX": tx0, "targetW": tw,
        "hasLimit": bool(limit_tex),
    }
    print(f"{key}: {pxW}x{pxH}px ink x {bb[0]}-{bb[2]} y {bb[1]}-{bb[3]} "
          f"= {meta[key]['inkW_in']:.3f}x{meta[key]['inkH_in']:.3f} in  (fs={fs:.1f}, limit={bool(limit_tex)})")

if os.path.exists(os.path.join(OUT, "_tmp_004.png")):
    os.remove(os.path.join(OUT, "_tmp_004.png"))

with open(os.path.join(OUT, "eq_004_metrics.json"), "w") as f:
    json.dump(meta, f, indent=2)
print("wrote eq_004_metrics.json")
