"""Panel 3's Error-function equation as 2D mathtext PNGs at 600 dpi.

Original frame (960x540, 1 frame px = 1pt) measured with PIL:
  "Error="   x 84-151           cap 14px, black
  sigma      x 219-240 y 354-380 black, 22x27 px
  limits     x 162-298 y 384-396 "all"(black) "misclassified"(red)
             "vectors"(black) "(i)"(red); band baseline ~393
  "W^T X_i"  x 305-356          X green
  "=>"       x 384-410
  "(W^T X_i)"x 444-498
  tail       x 542-733          same 9px x-height as the 21pt body
  red X      x 762-786 y 352-374 cap 23px

mathtext has no inline \\color (parse error, measured), so every colored span is
rendered on its own with va="baseline" (its baseline row inside the tight crop is
exact) and laid out by measured extents; the limits are centered under the sigma.
The limit band and the tail phrase are condensed in the original, so both are
squeezed horizontally until the whole strip is exactly 650 px of ink (x 84..733).
The PNGs stay transparent, but their RGB is pre-composited on the panel gray
(#E8E8E8) so a renderer's alpha handling cannot leave a dark fringe.
"""
import json

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from PIL import Image

DPI = 600
PXPT = DPI / 72.0  # 600 dpi pixels per typographic point

matplotlib.rcParams["mathtext.fontset"] = "stix"

FS = 22.0        # body: cap height 14px => 21pt
LIM_FS = 14.0    # sigma limits band: 13px ascender-to-descender
TAIL_FS = 19.0   # tail phrase: 9px x-height like the 21pt body
FX_FS = 34.0     # trailing red X: cap height 23px => 34.7pt

RED = "#E00000"
GREEN = "#008000"
BLACK = "#000000"
PANEL_GRAY = (232, 232, 232)

ASSETS = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/recreated_pptx/build/assets/"

# gaps between successive main-line ink clusters, in slide px
G_ERROR_SIGMA = 11   # "Error=" right edge -> limits band left edge
G_SIGMA_W = 7        # limits band right edge -> "W"
G_W_X = 5
G_X_ARROW = 28
G_ARROW_PAREN = 34
G_PAREN_GAP = 5
G_X_GAP = 5
G_PAREN_R = 2
G_R_TAIL = 44
LIM_WORD_GAP = 4     # inside the limits band
# original: sigma ink bottom 380, limits band ink top 384 (ascenders), band
# baseline 393 -> the band baseline sits 13px below the sigma's ink bottom
LIM_BASELINE_DROP = 13

LIMITS = [
    (r"\mathit{all}", BLACK),
    (r"\mathit{misclassified}", RED),
    (r"\mathit{vectors}", BLACK),
    (r"(i)", RED),
]

ANCHOR = 900
FIG_H_IN = 6.0


def render(mathtext, fs, color):
    """Tight RGBA crop of a mathtext string; base_off = baseline row in it."""
    fig = plt.figure(figsize=(12, FIG_H_IN), dpi=DPI)
    fig.patch.set_alpha(0.0)
    fig.text(0.1, 1.0 - ANCHOR / (FIG_H_IN * DPI), "${}$".format(mathtext),
             fontsize=fs, color=color, ha="left", va="baseline")
    fig.canvas.draw()
    buf = np.asarray(fig.canvas.buffer_rgba())
    plt.close(fig)
    alpha = buf[..., 3]
    ys, xs = np.nonzero(alpha)
    if not len(xs):
        raise RuntimeError("empty render: " + mathtext)
    box = (int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max()))
    img = Image.fromarray(buf[box[1]:box[3] + 1, box[0]:box[2] + 1])
    return {"img": img, "w": img.size[0], "h": img.size[1],
            "base_off": ANCHOR - box[1], "mt": mathtext}


def squeeze(item, factor):
    """Horizontal-only condensation; the baseline row is unchanged."""
    if abs(factor - 1.0) < 1e-9:
        return item
    w = max(1, int(round(item["w"] * factor)))
    return {"img": item["img"].resize((w, item["h"]), Image.LANCZOS),
            "w": w, "h": item["h"], "base_off": item["base_off"],
            "mt": item["mt"]}


def on_gray(img):
    """Keep the alpha, but pre-composite the RGB on the panel gray."""
    arr = np.asarray(img).astype(np.float32)
    a = arr[..., 3:4] / 255.0
    rgb = arr[..., :3] * a + np.array(PANEL_GRAY, dtype=np.float32) * (1.0 - a)
    out = np.dstack([rgb, arr[..., 3]]).astype(np.uint8)
    return Image.fromarray(out, "RGBA")


def build():
    sigma = render(r"\sum", FS, BLACK)
    eye = render(r"\mathbf{Error=}", FS, BLACK)
    wts = [render(r"\mathbf{W}^{T}", FS, BLACK), render(r"\mathbf{W}^{T}", FS, BLACK)]
    xis = [render(r"\underline{X}_{i}", FS, GREEN),
           render(r"\underline{X}_{i}", FS, GREEN)]
    arrow = render(r"\mathbf{\Rightarrow}", FS, BLACK)
    lpar = render("(", FS, BLACK)
    rpar = render(")", FS, BLACK)
    tail = render(r"\mathit{take\ positive\ and\ negative\ values}", TAIL_FS, BLACK)
    limits = [dict(item=render(mt, LIM_FS, c), color=c) for mt, c in LIMITS]

    core = [eye["w"], G_ERROR_SIGMA * PXPT, 0, G_SIGMA_W * PXPT,
            wts[0]["w"], G_W_X * PXPT, xis[0]["w"], G_X_ARROW * PXPT,
            arrow["w"], G_ARROW_PAREN * PXPT, lpar["w"], G_PAREN_GAP * PXPT,
            wts[1]["w"], G_X_GAP * PXPT, xis[1]["w"], G_PAREN_R * PXPT, rpar["w"],
            G_R_TAIL * PXPT]

    def total(f):
        """Full strip ink width in 600 dpi px for a given condensation factor."""
        lim_band = (max(item["item"]["w"] for item in limits) * f
                    + LIM_WORD_GAP * PXPT * (len(limits) - 1))
        group = max(sigma["w"], lim_band)
        return sum(core) + group + tail["w"] * f

    target = 650 * PXPT
    lo, hi = 0.4, 1.0
    for _ in range(40):
        mid = (lo + hi) / 2
        if total(mid) > target:
            hi = mid
        else:
            lo = mid
    f = lo

    squeezed_limits = [squeeze(item["item"], f) for item in limits]
    squeezed_tail = squeeze(tail, f)
    lim_band_w = (max(item["w"] for item in squeezed_limits)
                  + LIM_WORD_GAP * PXPT * (len(squeezed_limits) - 1))
    group_w = max(sigma["w"], lim_band_w)

    x = 80 * PXPT
    BL = 500.0
    cuts = []
    e_above, e_below = eye["base_off"], eye["h"] - eye["base_off"]
    sigma_center = BL + (e_below - e_above) / 2.0

    def put(item, x_left, y_top):
        cuts.append((x_left, y_top, item["img"]))

    put(eye, x, BL - eye["base_off"])
    x += eye["w"] + G_ERROR_SIGMA * PXPT
    g_left = x
    put(sigma, g_left + (group_w - sigma["w"]) / 2, sigma_center - sigma["h"] / 2)
    x += group_w + G_SIGMA_W * PXPT
    put(wts[0], x, BL - wts[0]["base_off"]); x += wts[0]["w"] + G_W_X * PXPT
    put(xis[0], x, BL - xis[0]["base_off"]); x += xis[0]["w"] + G_X_ARROW * PXPT
    put(arrow, x, BL - arrow["base_off"]); x += arrow["w"] + G_ARROW_PAREN * PXPT
    put(lpar, x, BL - lpar["base_off"]); x += lpar["w"] + G_PAREN_GAP * PXPT
    put(wts[1], x, BL - wts[1]["base_off"]); x += wts[1]["w"] + G_X_GAP * PXPT
    put(xis[1], x, BL - xis[1]["base_off"]); x += xis[1]["w"] + G_PAREN_R * PXPT
    put(rpar, x, BL - rpar["base_off"]); x += rpar["w"] + G_R_TAIL * PXPT
    put(squeezed_tail, x, BL - squeezed_tail["base_off"])
    x += squeezed_tail["w"]

    lim_bl = sigma_center + sigma["h"] / 2 + LIM_BASELINE_DROP * PXPT
    lx = g_left + (group_w - lim_band_w) / 2
    for item in squeezed_limits:
        put(item, lx, lim_bl - item["base_off"])
        lx += item["w"] + LIM_WORD_GAP * PXPT

    xs0 = min(c[0] for c in cuts)
    ys0 = min(c[1] for c in cuts)
    xs1 = max(c[0] + c[2].size[0] for c in cuts)
    ys1 = max(c[1] + c[2].size[1] for c in cuts)
    canvas = Image.new("RGBA", (int(xs1 - xs0) + 8, int(ys1 - ys0) + 8), (0, 0, 0, 0))
    for x_left, y_top, img in cuts:
        canvas.alpha_composite(img, dest=(int(round(x_left - xs0)) + 4,
                                          int(round(y_top - ys0)) + 4))
    arr = np.asarray(canvas)
    ys, xs = np.nonzero(arr[..., 3])
    out = canvas.crop((int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1))
    return on_gray(out), f


def sidecar(img, name, slide_x, slide_y, slide_w):
    tw, th = img.size
    w_in = slide_w / 72.0
    return {"image": "assets/" + name, "size_px": [tw, th],
            "x": slide_x / 72.0, "y": slide_y / 72.0,
            "w": w_in, "h": w_in * th / tw}


def main():
    strip, f = build()
    p_main = ASSETS + "eq_error_main.png"
    strip.save(p_main)
    red = on_gray(render(r"\mathbf{X}", FX_FS, RED)["img"])
    p_x = ASSETS + "eq_error_x.png"
    red.save(p_x)

    places = [sidecar(strip, "eq_error_main.png", 84, 354, 650),
              sidecar(red, "eq_error_x.png", 762, 352, 25)]
    with open(ASSETS + "eq_error_place.json", "w") as fh:
        json.dump(places, fh, indent=1)
    for p in places:
        print("%-20s %4dx%-4d px   x=%.5f y=%.5f w=%.5f h=%.5f"
              % (p["image"], *p["size_px"], p["x"], p["y"], p["w"], p["h"]))
    print("condense factor f=%.4f (1.0 = natural width)" % f)


if __name__ == "__main__":
    main()
