#!/usr/bin/env python3
"""Slide 004: replace the baked black stacked Sigma-limit captions with the small
red italic caption the original shows, at the original's measured ink position,
and render the centre red left-pointing arrow.

Method: re-render each mathtext (600 dpi, tight, transparent) with and without
the subscript, left-anchored so the main row does not shift; the pixel diff is
exactly the baked caption ink, which is erased; a red italic caption is then
font-fitted to the original's measured caption ink width and pasted at the
measured position (converted into image px via the v3 placement scale).
"""
import io
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from PIL import Image, ImageFilter

B = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/recreated_pptx/build"
DPI = 600
BLACK = "#000000"
RED = "#C00000"
ARR_RED = "#FF0000"

JOBS = [
    dict(
        name="eq_error_v3.png",
        wl=r"$\mathrm{Error} = \sum_{\mathrm{all\ misclassified\ vectors\ }(i)} \delta_i W^T X_i$",
        nl=r"$\mathrm{Error} = \sum \delta_i W^T X_i$",
        label=r"$\mathit{all\ misclassified\ vectors\ }(i)$",
        orig=(165, 229, 283, 289),            # original ink box, px on 960x540
        img_xy=(1.104, 3.441), scale=4.664 / (2989 / 600.0),
    ),
    dict(
        name="eq_gradient_v3.png",
        wl=r"$\frac{\partial \mathrm{Error}}{\partial W} = \sum_{\mathrm{misclassified\ vectors}} \delta_i X_i$",
        nl=r"$\frac{\partial \mathrm{Error}}{\partial W} = \sum \delta_i X_i$",
        label=r"$\mathit{misclassified\ vectors}$",
        orig=(610, 664, 421, 436),
        img_xy=(7.084, 5.342), scale=3.503 / (2297 / 600.0),
    ),
    dict(
        name="eq_update_batch_v3.png",
        wl=r"$W^{\mathrm{(updated)}} = W^{\mathrm{(old)}} - \eta \sum_{\mathrm{misclassified\ vectors\ ONLY\ }(i)} \delta_i X_i$",
        nl=r"$W^{\mathrm{(updated)}} = W^{\mathrm{(old)}} - \eta \sum \delta_i X_i$",
        label=r"$\mathit{misclassified\ vectors\ ONLY\ }(i)$",
        orig=(262, 342, 484, 495),
        img_xy=(1.149, 6.250), scale=3.731 / (4113 / 600.0),
    ),
]


def render(mathtext, fontsize, color=BLACK):
    fig, ax = plt.subplots(figsize=(1, 1), dpi=DPI)
    ax.text(0.4, 0.5, mathtext, ha="left", va="center", fontsize=fontsize,
            color=color, fontfamily="DejaVu Sans")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    fig.tight_layout(pad=0)
    buf = io.BytesIO()
    fig.savefig(buf, dpi=DPI, transparent=True, bbox_inches="tight", pad_inches=0.01)
    plt.close(fig)
    buf.seek(0)
    return Image.open(buf).convert("RGBA")


def render_label(label, fontsize):
    try:
        return render(label, fontsize, RED)
    except Exception:
        fig, ax = plt.subplots(figsize=(1, 1), dpi=DPI)
        ax.text(0.4, 0.5, label.replace("\\ ", " "), ha="left", va="center",
                fontsize=fontsize, color=RED, fontfamily="DejaVu Sans",
                style="italic")
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis("off")
        fig.tight_layout(pad=0)
        buf = io.BytesIO()
        fig.savefig(buf, dpi=DPI, transparent=True, bbox_inches="tight", pad_inches=0.01)
        plt.close(fig)
        buf.seek(0)
        return Image.open(buf).convert("RGBA")


def ink_bbox(im):
    return im.getchannel("A").getbbox()


def fit_font(label, color, target_px, lo=3.0, hi=40.0, iters=16):
    for _ in range(iters):
        mid = (lo + hi) / 2.0
        im = render_label(label, mid)
        bb = ink_bbox(im)
        w = bb[2] - bb[0]
        if w > target_px:
            hi = mid
        else:
            lo = mid
    return (lo + hi) / 2.0


def caption_mask(wl, nl, grow=5):
    wa = np.asarray(wl.getchannel("A"))
    na = np.asarray(nl.getchannel("A"))
    wb, nb = ink_bbox(wl), ink_bbox(nl)
    dx, dy = wb[0] - nb[0], wb[1] - nb[1]
    H, W = wa.shape
    al = np.zeros((H, W), dtype=np.uint8)
    nh, nw = na.shape
    ys, ye = max(0, dy), min(H, dy + nh)
    xs, xe = max(0, dx), min(W, dx + nw)
    if ye > ys and xe > xs:
        al[ys:ye, xs:xe] = na[ys - dy:ys - dy + (ye - ys), xs - dx:xs - dx + (xe - xs)]
    diff = (wa > 50) & (al <= 45)
    m = Image.fromarray((diff * 255).astype(np.uint8))
    m = m.filter(ImageFilter.MaxFilter(2 * grow + 1))
    return np.asarray(m) > 0, (dx, dy)


def row_bands(im):
    a = np.asarray(im.getchannel("A"))
    on = (a > 60).any(axis=1)
    bands, y = [], 0
    while y < len(on):
        if on[y]:
            y0 = y
            while y < len(on) and on[y]:
                y += 1
            bands.append((y0, y))
        else:
            y += 1
    return bands


def merge_bands(bands, gap=8):
    out = []
    for b in bands:
        if out and b[0] - out[-1][1] <= gap:
            out[-1] = (out[-1][0], b[1])
        else:
            out.append((b[0], b[1]))
    return out


def main():
    for j in JOBS:
        wl = render(j["wl"], 22)
        nl = render(j["nl"], 22)
        mask, shift = caption_mask(wl, nl)
        ys, xs = np.where(mask)
        mbb = (xs.min(), ys.min(), xs.max() + 1, ys.max() + 1) if len(xs) else None
        arr = np.asarray(wl)
        arr[..., 3][mask] = 0
        wl = Image.fromarray(arr)

        x0, x1, y0, y1 = j["orig"]
        scale = j["scale"]
        imgx, imgy = j["img_xy"]
        px_left = int(round((x0 / 72.0 - imgx) / scale * 600))
        py_top = int(round((y0 / 72.0 - imgy) / scale * 600))
        tgt_w = int(round((x1 - x0) / scale * 600))

        fs = fit_font(j["label"], RED, tgt_w)
        lab = render_label(j["label"], fs)
        lb = ink_bbox(lab)
        lab = lab.crop(lb)
        W, H = wl.size
        need_w = max(W, px_left + lab.width + 12)
        need_h = max(H, py_top + lab.height + 12)
        if need_w > W or need_h > H:
            canvas = Image.new("RGBA", (need_w, need_h), (0, 0, 0, 0))
            canvas.paste(wl, (0, 0), wl)
            wl = canvas
        wl.alpha_composite(lab, (px_left, py_top))
        out = B + "/" + j["name"]
        wl.save(out)

        fb = ink_bbox(wl)
        slide_w = wl.width / 600.0 * scale
        print("%-24s wl=%s mask=%s shift=%s  paste=(%d,%d) tgt_w=%d label=%dx%d fit=%.2fpt  final=%s (%.2fx%.2f in on slide)"
              % (j["name"], ink_bbox(render(j["wl"], 22)), str(mbb), str(shift),
                 px_left, py_top, tgt_w, lab.width, lab.height, fs, str(fb), slide_w, wl.height / 600.0 * scale))
        print("    row bands (px): %s" % merge_bands(row_bands(wl)))
        print("    slide ink: y %.2f..%.2f  (orig caption y %.2f..%.2f)"
              % (fb[1] / 600.0 * scale + imgy, fb[3] / 600.0 * scale + imgy, y0 / 72.0, y1 / 72.0))

    # ---- centre red left-pointing arrow: x 6.51..7.95 in, y 6.53..6.66 in ----
    BW, BH = 1.44, 0.17
    fig, ax = plt.subplots(figsize=(BW, BH), dpi=DPI)
    ax.set_xlim(0, BW)
    ax.set_ylim(0, BH)
    ax.axis("off")
    cy = 0.085
    t = 0.020
    ax.add_patch(Polygon([(0.16, cy - t / 2), (1.05, cy - t / 2), (1.05, cy + t / 2), (0.16, cy + t / 2)],
                         closed=True, color=ARR_RED, lw=0))
    ax.add_patch(Polygon([(0.02, cy), (0.16, cy - 0.055), (0.16, cy + 0.055)],
                         closed=True, color=ARR_RED, lw=0))
    ax.add_patch(Polygon([(0.98, cy - t / 2), (1.32, cy + 0.030), (1.32, cy + 0.050), (0.98, cy + t / 2)],
                         closed=True, color=ARR_RED, lw=0))
    fig.savefig(B + "/eq_arrow_v3.png", dpi=DPI, transparent=True,
                bbox_inches="tight", pad_inches=0.004)
    plt.close(fig)
    ar = Image.open(B + "/eq_arrow_v3.png").convert("RGBA")
    ab = ink_bbox(ar)
    ar = ar.crop(ab)
    ar.save(B + "/eq_arrow_v3.png")
    print("eq_arrow_v3.png %dx%d = %.3f x %.3f in  (orig ink x 6.51..7.95, y 6.53..6.66)"
          % (ar.width, ar.height, ar.width / 600.0, ar.height / 600.0))


main()
