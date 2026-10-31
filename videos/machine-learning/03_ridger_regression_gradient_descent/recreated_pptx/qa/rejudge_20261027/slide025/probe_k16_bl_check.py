#!/usr/bin/env python3
"""Replicate pil_k15_render_check.py CHECK2/CHECK3 on a synthetic canvas carrying
only the k16 BL png (built with candidate params). usage: probe_k16_bl_check.py
"""
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy import ndimage
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from mpl_toolkits.mplot3d import proj3d

NS = "/home/codespace/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
ORIG = np.asarray(Image.open(NS + "/unique_slides/slide_025.jpg").convert("RGB")).astype(np.int32)
DPI = 300
X0, Y0, BW, BH = 83, 290, 293, 237
RED = (0.75, 0.0, 0.0)
BLK = "black"
TICKC = "#333333"
JET = plt.get_cmap("jet")


def proj_xy(ax, x, y, z):
    x2, y2, _ = proj3d.proj_transform(x, y, z, ax.get_proj())
    disp = ax.transData.transform([(x2, y2)])[0]
    W = ax.figure.get_size_inches()[0] * DPI
    H = ax.figure.get_size_inches()[1] * DPI
    return (disp[0] / W, 1.0 - disp[1] / H)


def build_bl(mesh, lw, labels, fs=6.2):
    fig = plt.figure(figsize=(BW / 72.0, BH / 72.0), dpi=DPI)
    ax = fig.add_axes([0.05, 0.09, 0.90, 0.88], projection="3d")
    ax.view_init(elev=28, azim=-62)
    x = np.linspace(-3, 3, 100)
    X, Y = np.meshgrid(x, x)
    Z = (4.6 * np.exp(-((X - 0.2) ** 2 + (Y - 0.4) ** 2) * 0.9)
         + 3.4 * np.exp(-((X + 1.9) ** 2 + (Y - 1.7) ** 2) * 1.5)
         - 4.8 * np.exp(-((X + 0.7) ** 2 + (Y + 1.6) ** 2) * 1.1)
         - 3.6 * np.exp(-((X - 1.8) ** 2 + (Y + 1.3) ** 2) * 1.4))
    ax.plot_surface(X, Y, Z, cmap=JET, shade=False, antialiased=True,
                    rstride=4, cstride=4, linewidth=lw, edgecolor=mesh)
    ax.set_xlim(-3, 3); ax.set_ylim(-3, 3); ax.set_zlim(-6, 8)
    ax.set_xticks([-3, -2, -1, 0, 1, 2, 3]); ax.set_yticks([-3, -2, -1, 0, 1, 2, 3])
    ax.set_zticks([-6, -4, -2, 0, 2, 4, 6, 8])
    for axis in (ax.xaxis, ax.yaxis, ax.zaxis):
        axis.set_pane_color((1, 1, 1, 0.0))
        axis._axinfo["grid"].update(color="#E4E4E4", linewidth=0.3, linestyle=":")
        axis.line.set_linewidth(0.4)
        axis.line.set_color("#BBBBBB")
    ax.tick_params(pad=0.5, labelsize=5.5, length=1.5, width=0.4)
    for t in ax.get_xticklabels() + ax.get_yticklabels() + ax.get_zticklabels():
        t.set_fontsize(5.5); t.set_color(TICKC)
    ax.set_xlabel("X", fontsize=5.5, color=TICKC, labelpad=0)
    ax.set_ylabel("Y", fontsize=5.5, color=TICKC, labelpad=0)
    ax.set_box_aspect((1, 1, 0.95), zoom=1.00)

    def extremum(cx, cy, want_max):
        d = (X - cx) ** 2 + (Y - cy) ** 2
        m = d < 0.9 ** 2
        masked = np.where(m, Z, -1e9 if want_max else 1e9)
        i = np.argmax(masked) if want_max else np.argmin(masked)
        return X.flat[i], Y.flat[i], Z.flat[i]

    PEAKS = {"GM": extremum(0.2, 0.4, True), "LMx": extremum(-1.9, 1.7, True),
             "LMn": extremum(1.8, -1.3, False), "GMn": extremum(-0.7, -1.6, False)}
    MARKED = {"LMn", "GMn"}
    for key, (txt, sx, sy, ha) in labels.items():
        fxp = (sx - X0) / BW
        fyp = 1.0 - (sy - Y0) / BH
        fig.text(fxp, fyp, txt, fontsize=fs, color=BLK, ha=ha, va="center", zorder=45,
                 linespacing=1.15)
        px_, py_, pz_ = PEAKS[key]
        ex, ey = proj_xy(ax, px_, py_, pz_)
        dx, dy = ex - fxp, ey - fyp
        L = max(np.hypot(dx, dy), 1e-6)
        ox, oy = fxp + dx / L * 0.045, fyp + dy / L * 0.045
        fig.add_artist(Line2D([ox, ex], [oy, ey], transform=fig.transFigure,
                              color=(0.78, 0.78, 0.78), lw=0.3, zorder=42))
        if key in MARKED:
            fig.add_artist(Line2D([ex], [ey], transform=fig.transFigure,
                                  marker="x", color=RED, markersize=4,
                                  markeredgewidth=1.3, zorder=46, linestyle="none"))
    for (a0, b0, a1, b1) in ((3 / BW, 1 - 3 / BH, 3 / BW, 3 / BH),
                             (1 - 3 / BW, 1 - 3 / BH, 1 - 3 / BW, 3 / BH),
                             (3 / BW, 1 - 3 / BH, 1 - 3 / BW, 1 - 3 / BH),
                             (3 / BW, 3 / BH, 1 - 3 / BW, 3 / BH)):
        fig.add_artist(Line2D([a0, a1], [b0, b1], transform=fig.transFigure,
                              color=RED, lw=0.7, zorder=40, solid_capstyle="butt"))
    fig.canvas.draw()
    buf = np.asarray(fig.canvas.buffer_rgba())[:, :, :3].astype(np.uint8)
    plt.close(fig)
    return buf


def canvas_with(buf):
    im = Image.fromarray(buf).resize((BW, BH), Image.BILINEAR)
    c = np.full((540, 960, 3), 255, np.int32)
    c[Y0:Y0 + BH, X0:X0 + BW] = np.asarray(im).astype(np.int32)
    return c


# ---- replicate check logic ----
def darkmask(a, thr=145, sat=80):
    return (a.max(2) < thr) & ((a.max(2) - a.min(2)) < sat)


def redmask(a):
    r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
    return (r > 110) & (r - g > 50) & (r - b > 50)


def lum(a):
    return (0.299 * a[:, :, 0] + 0.587 * a[:, :, 1] + 0.114 * a[:, :, 2])


def comps(mask, min_area=5):
    lab, n = ndimage.label(mask, structure=np.ones((3, 3)))
    out = []
    for i in range(1, n + 1):
        ys, xs = np.nonzero(lab == i)
        if len(xs) >= min_area:
            out.append([len(xs), int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max()), i])
    return out


BL = (83, 290, 377, 528)
x0, y0, x1, y1 = BL
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
CANDS = ["Global Maxima", "Local Maxima", "Local Minima", "Global Minima"]


def render_cand(s, fs):
    f = ImageFont.truetype(FONT, fs)
    im = Image.new("L", (300, 60), 255)
    ImageDraw.Draw(im).text((4, 4), s, font=f, fill=0)
    a = np.array(im)
    ys, xs = np.nonzero(a < 128)
    return a[ys.min():ys.max() + 1, xs.min():xs.max() + 1]


def ncc(a, b):
    a = a - a.mean(); b = b - b.mean()
    den = np.sqrt((a * a).sum() * (b * b).sum())
    return float((a * b).sum() / den) if den > 0 else -1.0


def find_labels(a):
    bl = a[y0:y1, x0:x1]
    dm = darkmask(bl)
    dm[:8, :] = False; dm[-8:, :] = False; dm[:, :8] = False; dm[:, -8:] = False
    dm[413 - y0:423 - y0, :] = False
    words = []
    for area, wx0, wy0, wx1, wy1, _ in comps(dm, min_area=5):
        w, h = wx1 - wx0 + 1, wy1 - wy0 + 1
        if w > 25 and h <= 9:
            continue
        if w > 40 and h < 3 * w // 4:
            continue
        words.append([wx0, wy0, wx1, wy1])
    lines = []
    for b in sorted(words, key=lambda b: (b[1], b[0])):
        hit = None
        for L in lines:
            if abs((b[1] + b[3]) / 2 - (L[1] + L[3]) / 2) < 6 and (b[0] - L[2] < 14 or L[0] - b[2] < 14):
                hit = L
                break
        if hit:
            hit[0] = min(hit[0], b[0]); hit[1] = min(hit[1], b[1])
            hit[2] = max(hit[2], b[2]); hit[3] = max(hit[3], b[3])
        else:
            lines.append(list(b))
    out = []
    for L in sorted(lines, key=lambda l: l[1]):
        w, h = L[2] - L[0] + 1, L[3] - L[1] + 1
        if w < 40 or h < 5:
            continue
        crop = lum(bl[L[1]:L[3] + 1, L[0]:L[2] + 1]).astype(np.float32)
        best = (-2, "?")
        for s in CANDS:
            for fs in range(7, 16):
                c = render_cand(s, fs)
                cr = np.array(Image.fromarray(c.astype(np.uint8)).resize((w, h), Image.BILINEAR)).astype(np.float32)
                v = ncc(crop, cr)
                if v > best[0]:
                    best = (v, s)
        out.append((L[0] + x0, L[1] + y0, L[2] + x0, L[3] + y0, best[1], round(best[0], 3)))
    return out


def markers(a):
    bl = a[y0:y1, x0:x1]
    rm = redmask(bl)
    rm[:8, :] = False; rm[-8:, :] = False; rm[:, :8] = False; rm[:, -8:] = False
    rm[413 - y0:423 - y0, :] = False
    out = []
    for area, rx0, ry0, rx1, ry1, _ in comps(rm, min_area=8):
        w, h = rx1 - rx0 + 1, ry1 - ry0 + 1
        if 12 <= area <= 200 and 4 <= w <= 16 and 4 <= h <= 16 and area / (w * h) > 0.3:
            out.append((area, (rx0 + rx1) // 2 + x0, (ry0 + ry1) // 2 + y0))
    return out


LABELS = {
    "GM":  ("Global\nMaxima", 257, 312, "center"),
    "LMx": ("Local\nMaxima",  300, 345, "center"),
    "LMn": ("Local\nMinima",  171, 454, "center"),
    "GMn": ("Global\nMinima", 323, 459, "center"),
}

for mesh, lw, tag in (((0.72, 0.72, 0.72, 0.45), 0.2, "light"),
                      ((0.55, 0.55, 0.55, 0.5), 0.22, "mid"),
                      ((0.05, 0.05, 0.05, 0.55), 0.28, "k15dark")):
    buf = build_bl(mesh, lw, LABELS)
    ren = canvas_with(buf)
    rlab = find_labels(ren)
    print("== mesh=%s ==" % tag)
    for t in rlab:
        print("   render line x%d..%d y%d..%d -> '%s' ncc=%.3f" % t)
    bottom2 = rlab[-2:] if len(rlab) >= 2 else []
    ok2 = False
    if len(bottom2) == 2:
        upper, lower = bottom2
        ok2 = (upper[4] == "Local Minima" and lower[4] == "Global Minima"
               and upper[1] < 470 and lower[1] >= 450 and upper[0] < 350 and lower[0] < 350)
    print("   CHECK2:", "PASS" if ok2 else "FAIL", "| markers:", markers(ren),
          "orig:", markers(ORIG))
