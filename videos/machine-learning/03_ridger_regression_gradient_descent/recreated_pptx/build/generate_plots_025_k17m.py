#!/usr/bin/env python3
"""k17m: slide 025 BR-only regeneration (attempt M) + carried tl/tr/bl.

Judge finding being fixed: render BR reads flat/top-down, no z-ticks/grid.
Orig (unique_slides/slide_025.jpg BR panel): z-axis vline slide x~731-738
with ticks 0/0.5/1/1.5; surf bbox x624..864 y355..523; colored 42.6%;
jet hist [1647,0,0,555,813,0,1140,5098,3272,3597,4,1517,2066,401,72,1127];
main-diag jet-t mean 0.55 std 0.125; bottom band rows y472..528 taper
75%->16%.

k17m BR: mplot3d plot_surface WITH AXES ON — view_init(elev=38, azim=-80)
(banked best), x/y in -100..100 (xticks -100..100), zlim with ticks
[0,0.5,1,1.5], panes ON (grid walls), grid ON, cmap jet with vmin tuned so
the lowest jet bin holds ~1647/45k (~3.7% of crop px), geometry from
br_search_k17_results.txt best (band=1.000): zoom=1.8164 pad_lo=0.40
zfac=1.3. PNG saved at the promoted build/assets/plot_025_br.png pixel size
(1103x779). tl/tr/bl copied from build/assets/; tr patched with the red
segment (652,189)->(667,165) mapped via the slide_025.js TR rect
(x616 y115 263x202). Output: build/assets_k17m/.
"""
import os
import shutil
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
from matplotlib.lines import Line2D
from matplotlib.patches import FancyArrowPatch
from mpl_toolkits.mplot3d import proj3d
from PIL import Image, ImageDraw

ROOT = "/home/codespace/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx"
# carried tl/tr/bl come from the banked copy of the currently promoted
# build/assets set (build/assets is rewritten by a concurrent promoter; this
# snapshot holds the same md5s: tl cd62022f, tr b45c723a, bl 7a8e7210)
SRC_ASSETS = os.path.join(
    ROOT, "qa", "rejudge_20261027", "slide025", "assets_k17g")
OUT = os.path.join(ROOT, "build", "assets_k17m")
os.makedirs(OUT, exist_ok=True)

DPI = 300
JET = plt.get_cmap("jet")
RED = (0.75, 0.0, 0.0)
TICKC = "#333333"

# promoted BR asset pixel size (PIL-checked): 1103x779
BR_W, BR_H = 1103, 779

# slide_025.js measured figure boxes (frame px)
PLOTS = {
    "tl": dict(x0=85,  y0=115, w=180, h=173),
    "tr": dict(x0=616, y0=115, w=263, h=202),
    "bl": dict(x0=83,  y0=290, w=293, h=237),
    "br": dict(x0=615, y0=344, w=265, h=187),
}


def br_surface(X, Y):
    return (3.2 * np.exp(-(((X - 0.5) ** 2 + (Y + 0.7) ** 2) / 1.6))
            + 2.0 * np.exp(-(((X + 1.8) ** 2 + (Y - 1.3) ** 2) / 1.2))
            + 1.3 * np.exp(-(((X - 2.3) ** 2 + (Y - 1.9) ** 2) / 0.7))
            - 2.3 * np.exp(-(((X + 0.9) ** 2 + (Y + 1.6) ** 2) / 1.0))
            - 1.8 * np.exp(-(((X - 2.0) ** 2 + (Y + 1.7) ** 2) / 0.8))
            - 1.7 * np.exp(-(((X - 0.9) ** 2 + (Y - 2.2) ** 2) / 1.1))
            + 0.38 * np.sin(2.1 * X) * np.cos(2.3 * Y))


# winding GD route in -3..3 space; scaled x33.333 into the -100..100 domain
BR_WAYPOINTS = np.array([
    (2.4, 1.9), (1.7, 1.1), (0.9, 1.45), (0.2, 0.6), (-0.5, 0.95),
    (-1.0, 0.3), (-0.6, -0.6), (-1.3, -0.9), (-0.8, -1.7), (-1.5, -2.2),
]) * (100.0 / 3.0)


def redrect(fig, w_px, h_px, inset=3):
    x0 = inset / w_px
    x1 = 1.0 - inset / w_px
    y0 = 1.0 - inset / h_px
    y1 = inset / h_px
    for (a0, b0, a1, b1) in ((x0, y0, x0, y1), (x1, y0, x1, y1),
                             (x0, y0, x1, y0), (x0, y1, x1, y1)):
        fig.add_artist(Line2D([a0, a1], [b0, b1], transform=fig.transFigure,
                              color=RED, lw=0.7, zorder=40, solid_capstyle="butt"))


def proj_xy(ax, x, y, z):
    x2, y2, _ = proj3d.proj_transform(x, y, z, ax.get_proj())
    disp = ax.transData.transform([(x2, y2)])[0]
    W = ax.figure.get_size_inches()[0] * DPI
    H = ax.figure.get_size_inches()[1] * DPI
    return (disp[0] / W, 1.0 - disp[1] / H)


def plot_br():
    spec = PLOTS["br"]
    fig = plt.figure(figsize=(BR_W / DPI, BR_H / DPI), dpi=DPI)
    ax = fig.add_axes([0.0, 0.0, 1.0, 1.0], projection="3d")
    ax.view_init(elev=38, azim=-80)  # banked best

    x = np.linspace(-100, 100, 120)
    X, Y = np.meshgrid(x, x)
    Z = br_surface(X / (100.0 / 3.0), Y / (100.0 / 3.0))
    # normalize into the orig z-tick range 0..1.5
    zmin, zmax = float(Z.min()), float(Z.max())
    rng = zmax - zmin
    Z = (Z - zmin) / rng * 1.55
    zmax = 1.55

    # jet norm: vmin sweep-measured so the lowest jet bin holds ~1647/45k of
    # crop px (~7.6% of colored, orig 1480/19416) — more dark blue than the
    # k17i2 axis-off render. Full-render sweep: vmin = 0.12 * zmax hits the
    # bin0 share target (0.10 -> 0.062, 0.13 -> 0.082).
    vmin = 0.12 * zmax
    vmax = zmax
    norm = Normalize(vmin, vmax)

    ax.plot_surface(X, Y, Z, cmap=JET, norm=norm, shade=False, antialiased=True,
                    rstride=3, cstride=3, linewidth=0.22,
                    edgecolor=(0.05, 0.05, 0.05, 0.35))

    # winding GD path (data coords -100..100), z hugging the surface
    from scipy.interpolate import CubicSpline
    t = np.linspace(0, 1, len(BR_WAYPOINTS))
    ts = np.linspace(0, 1, 240)
    sx = CubicSpline(t, BR_WAYPOINTS[:, 0])(ts)
    sy = CubicSpline(t, BR_WAYPOINTS[:, 1])(ts)
    sz = np.array([float(br_surface(np.array(a) / (100.0 / 3.0),
                                    np.array(b) / (100.0 / 3.0))) for a, b in zip(sx, sy)])
    sz = (sz - zmin) / rng * 1.55 + 0.06
    ax.plot(sx, sy, sz, color="black", lw=1.8, zorder=100, solid_capstyle="round")
    (ex, ey), (ex2, ey2) = proj_xy(ax, sx[-1], sy[-1], sz[-1]), \
        proj_xy(ax, sx[-12], sy[-12], sz[-12])
    ar = FancyArrowPatch(posA=(ex2, ey2), posB=(ex, ey), transform=fig.transFigure,
                         arrowstyle="-|>", mutation_scale=9, color="black",
                         lw=0.8, zorder=101)
    fig.add_artist(ar)

    # axes ON: limits, ticks, labels
    ax.set_xlim(-100, 100); ax.set_ylim(-100, 100)
    ax.set_zlim(-0.25, 1.6)  # low pad keeps the floor below 0 so bin0 stays reachable
    ax.set_xticks([-100, -50, 0, 50, 100]); ax.set_yticks([-100, -50, 0, 50, 100])
    ax.set_zticks([0, 0.5, 1, 1.5])
    ax.set_zticklabels(["0", "0.5", "1", "1.5"])
    ax.set_xlabel("x", fontsize=5.5, color=TICKC, labelpad=0)
    ax.set_ylabel("y", fontsize=5.5, color=TICKC, labelpad=0)

    # panes ON (grid walls) + grid ON, house axis styling
    for axis in (ax.xaxis, ax.yaxis, ax.zaxis):
        axis.pane.set_visible(True)
        axis.pane.set_facecolor((1.0, 1.0, 1.0, 1.0))
        axis.pane.set_edgecolor((0.75, 0.75, 0.75, 1.0))
        axis._axinfo["grid"].update(color="#D8D8D8", linewidth=0.45, linestyle=":")
        axis.line.set_linewidth(0.4)
    ax.grid(True)
    ax.set_facecolor("white")
    ax.tick_params(pad=0.5, labelsize=6.0, length=2.2, width=0.6)
    for t_ in ax.get_xticklabels() + ax.get_yticklabels() + ax.get_zticklabels():
        t_.set_fontsize(6.0)
        t_.set_color(TICKC)

    # banked geometry: zoom 1.8164, zfac 1.3 folded into the box z ratio
    ax.set_box_aspect((6, 6, 6 * 1.3 * 1.19), zoom=1.8164)

    redrect(fig, BR_W, BR_H)
    out = os.path.join(OUT, "plot_025_br.png")
    fig.savefig(out, dpi=DPI, facecolor="white")
    plt.close(fig)
    im = Image.open(out).convert("RGB")
    im.save(out)
    print("wrote", out, im.size)
    return Z, norm


def carry_and_patch_tr():
    for n in ("tl", "tr", "bl"):
        shutil.copyfile(os.path.join(SRC_ASSETS, "plot_025_%s.png" % n),
                        os.path.join(OUT, "plot_025_%s.png" % n))
        print("copied", n)
    # patch tr with red segment (652,189)->(667,165) via the slide_025.js
    # TR rect x616 y115 w263 h202, onto the PNG pixel grid
    tr = PLOTS["tr"]
    p = os.path.join(OUT, "plot_025_tr.png")
    im = Image.open(p).convert("RGBA")
    W, H = im.size
    # image pixel y grows downward: slide fraction from the box top maps
    # directly to the pixel row
    s1 = ((652 - tr["x0"]) / tr["w"] * W, (189 - tr["y0"]) / tr["h"] * H)
    s2 = ((667 - tr["x0"]) / tr["w"] * W, (165 - tr["y0"]) / tr["h"] * H)
    d = ImageDraw.Draw(im)
    d.line([s1, s2], fill=(192, 0, 0, 255), width=5)
    im.save(p)
    print("patched tr red segment %s -> %s on %s (%dx%d)" % (s1, s2, p, W, H))


if __name__ == "__main__":
    plot_br()
    carry_and_patch_tr()
    print("assets_k17m complete")
