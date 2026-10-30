#!/usr/bin/env python3
"""Generate the four loss-function-shape plots for slide 025.

Regions measured from unique_slides/slide_025.jpg (960x540, 1px = 1pt = 1/72in).
The original does NOT stretch each plot image over its whole quadrant: every plot
is a SMALL white figure with a red border inset ~3px inside its own image edge,
and the label boxes sit in the gutters beside them. Measured figure boxes:

  TL concave dome   x 85..265  y 115..288   (180x173 px)
  TR convex bowl    x 616..879 y 115..317   (263x202 px)
  BL non-convex     x 83..376  y 290..527   (293x237 px)
  BR gradient path  x 615..880 y 344..531   (265x187 px)

and the red rectangles measured inside them are exactly those boxes inset by 3px
on every side (TL x88..262 y118..285, TR x619..876 y118..314,
BL x86..373 y293..524, BR x618..877 y347..528).

Each PNG is 300dpi with figsize = box_px/72, placed on the slide at box_px/72
inches, so 1 slide px = 1 PNG px: no rescale, no resampling ripple.

Red reference lines in the original are pure HORIZONTAL 2-D strokes (measured:
uniform 1-2px runs at constant frame y, x-extents below). They extend PAST the
figure image's own bounds (e.g. TL y186 reaches x281 while its image ends at
x265), so they cannot be drawn as figure-fraction artists inside the PNG --
they clip at the image edge. They are drawn as slide-level shapes in
slide_025.js at these measured frame-px coordinates instead:

  TL  y168 x119..267   y186 x109..281
  TR  y226 x633..875   y234 x644..867
  BL  y418 x124..382
  BR  none

BL annotations measured in the original (two-line text bands + leader strokes):
  "Global Maxima"  x242..265 y304..309  + leaders x187..204 y319..340, x178..184 y347..364
  "Local Maxima"   x282..342 y386..405
  "Local Minima"   x301..326 y450..465
  "Global Minima"  x145..167 y439..470

The 3-D cube is auto-fitted so the surface fills the small figure (the
originals' jet surfaces span ~97-99% of their figure boxes, measured
saturated-ink extents); without the zoom the default margins leave the cube at
~25% of the box, which is what made attempt 1's surfaces read as "a small bowl
floating in white".
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import os
from matplotlib.lines import Line2D

OUT = "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/build/assets"
os.makedirs(OUT, exist_ok=True)

DPI = 300
JET = plt.get_cmap("jet")
RED = (0.75, 0.0, 0.0)          # C00000 family nominal
BLK = "black"

PLOTS = {
    "tl": dict(x0=85,  y0=115, w=180, h=173, elev=34, azim=-64),
    "tr": dict(x0=616, y0=115, w=263, h=202, elev=34, azim=-64),
    "bl": dict(x0=83,  y0=290, w=293, h=237, elev=30, azim=-62),
    "br": dict(x0=615, y0=344, w=265, h=187, elev=30, azim=-62),
}

FIT_TARGET = 0.95                # content fraction of the figure box
FIT_ZOOMS = {"tl": 1.0, "tr": 1.0, "bl": 1.0, "br": 1.0}


def figure(spec):
    fig = plt.figure(figsize=(spec["w"] / 72.0, spec["h"] / 72.0), dpi=DPI)
    ax = fig.add_axes([0.0, 0.0, 1.0, 1.0], projection="3d")
    ax.view_init(elev=spec["elev"], azim=spec["azim"])
    return fig, ax


def axis_style(ax):
    for axis in (ax.xaxis, ax.yaxis, ax.zaxis):
        axis.set_pane_color((1, 1, 1, 1))
        axis._axinfo["grid"].update(color="#DDDDDD", linewidth=0.4)
        axis.line.set_linewidth(0.5)
        axis.set_tick_params(pad=-3, labelsize=7.5)
    for t in ax.get_xticklabels() + ax.get_yticklabels() + ax.get_zticklabels():
        t.set_fontsize(7.5)
        t.set_color("#444444")


def surface_box(fig):
    """Bounding box of the 3-D surface's own projection (jet-chroma pixels).

    Measured against the original at the same chroma threshold (chroma > 45,
    with the red C00000 strokes masked out): the original's surfaces occupy
    only a central core of their white figures, surrounded by white margin.
    """
    fig.canvas.draw()
    buf = np.asarray(fig.canvas.buffer_rgba())
    rgb = buf[:, :, :3].astype(int)
    mx = rgb.max(axis=2); mn = rgb.min(axis=2)
    surf = (mx - mn) > 45
    ys, xs = np.where(surf)
    if not len(xs):
        return None
    return xs.min(), xs.max(), ys.min(), ys.max(), buf.shape[1], buf.shape[0]


def data_aspect(ax, xys=1.0, zscale=1.0):
    (x0, x1), (y0, y1), (z0, z1) = (ax.get_xlim(), ax.get_ylim(), ax.get_zlim())
    xr, yr, zr = (max(x1 - x0, 1e-6), max(y1 - y0, 1e-6), max(z1 - z0, 1e-6))
    return (xr * xys, yr * xys, zr * zscale)


TARGETS = {"tl": (0.70, 0.54),   # jet-core fill of the white figure box
           "tr": (0.62, 0.53),
           "bl": (0.80, 0.51),
           "br": (0.95, 0.70)}


def fill_at(fig, ax, xys, zscale, zoom):
    ax.set_box_aspect(data_aspect(ax, xys, zscale), zoom=zoom)
    bb = surface_box(fig)
    if bb is None:
        return None
    x0, x1, y0, y1, W, H = bb
    return (x1 - x0 + 1) / W, (y1 - y0 + 1) / H


def max_zoom(fig, ax, xys, zscale, cap=1.0, rounds=12):
    """Largest zoom at which the surface still fits inside the figure box."""
    lo, hi = 0.05, 60.0
    for _ in range(rounds):
        mid = 0.5 * (lo + hi)
        f = fill_at(fig, ax, xys, zscale, mid)
        if f is not None and f[0] <= cap and f[1] <= cap:
            lo = mid
        else:
            hi = mid
    return lo


def fit_zoom(fig, ax, name, cap=0.995):
    """Scale the surface so its jet core fills the same fraction of the white
    figure box that the original's does (TARGETS, measured from the frame).

    A uniform zoom alone cannot hit a 2-D target: the projected box has its own
    aspect, so the x/y spread and the z spread of the box aspect are searched
    alongside the zoom, keeping the candidate nearest the target.
    """
    tx, ty = TARGETS[name]
    best = None
    # deliberately narrow grid: extreme x/y spread or z squash flattens the
    # surface and destroys the 3-D read, so stay near the natural box aspect
    # and accept a small residual against the fill target.
    for xys in (1.0, 1.25, 1.5):
        for zs in (1.0, 0.8):
            z = max_zoom(fig, ax, xys, zs, cap)
            f = fill_at(fig, ax, xys, zs, z)
            if f is None:
                continue
            fx, fy = f
            # scale the fill toward the target by trimming the zoom
            z *= max(min(tx / max(fx, 1e-3), ty / max(fy, 1e-3)), 1e-3)
            f = fill_at(fig, ax, xys, zs, z)
            if f is None:
                continue
            err = abs(f[0] - tx) + abs(f[1] - ty)
            if best is None or err < best[0]:
                best = (err, z, f[0], f[1], xys, zs)
    if best is None:
        FIT_ZOOMS[name] = 1.0
        return 1.0
    _, z, fx, fy, xys, zs = best
    fill_at(fig, ax, xys, zs, z)
    FIT_ZOOMS[name] = z
    print("  fit %-3s zoom=%.2f xys=%.1f zs=%.2f core %.2fx%.2f (target %.2fx%.2f)"
          % (name, z, xys, zs, fx, fy, tx, ty))
    return z


def redrect(fig, spec, inset=3):
    """Thin red border inset `inset` px from the PNG's own bounds.

    A rectangle drawn at or outside the image edge gets clipped and half the
    frame vanishes; the original's borders sit ~3px inside their image.
    """
    x0 = inset / spec["w"]
    x1 = 1.0 - inset / spec["w"]
    y0 = 1.0 - inset / spec["h"]
    y1 = inset / spec["h"]
    for (a0, b0, a1, b1) in ((x0, y0, x0, y1), (x1, y0, x1, y1),
                             (x0, y0, x1, y0), (x0, y1, x1, y1)):
        fig.add_artist(Line2D([a0, a1], [b0, b1], transform=fig.transFigure,
                              color=RED, lw=1.4, zorder=20, solid_capstyle="butt"))


def save(fig, name):
    fig.savefig(os.path.join(OUT, "plot_025_%s.png" % name), dpi=DPI, facecolor="white")
    plt.close(fig)
    print("wrote plot_025_%s.png" % name)


# ── TL: concave dome — one maximum, two red maximum-level lines ───────────────
def plot_tl():
    spec = PLOTS["tl"]
    fig, ax = figure(spec)
    x = np.linspace(-2, 2, 90)
    X, Y = np.meshgrid(x, x)
    Z = np.clip(4.0 * np.exp(-0.62 * (X ** 2 + Y ** 2)), 0, 4)
    ax.plot_surface(X, Y, Z, cmap=JET, rstride=1, cstride=1,
                    linewidth=0, antialiased=True, shade=True)
    ax.set_xlim(-2, 2); ax.set_ylim(-2, 2); ax.set_zlim(0, 5)
    ax.set_xticks([-2, 0]); ax.set_yticks([-2, 0]); ax.set_zticks([0, 2, 4])
    ax.set_zticklabels(["0", "2", "5"])
    axis_style(ax)
    fit_zoom(fig, ax, "tl")
    redrect(fig, spec)
    save(fig, "tl")


# ── TR: convex bowl — one minimum, two red minimum-level lines ───────────────
def plot_tr():
    spec = PLOTS["tr"]
    fig, ax = figure(spec)
    x = np.linspace(-100, 100, 90)
    X, Y = np.meshgrid(x, x)
    Z = (X ** 2 + Y ** 2) / 10000.0 * 1.5
    ax.plot_surface(X, Y, Z, cmap=JET, rstride=1, cstride=1,
                    linewidth=0, antialiased=True, shade=True)
    ax.set_xlim(-100, 100); ax.set_ylim(-100, 100); ax.set_zlim(0, 1.5)
    ax.set_xticks([-100, 0, 100]); ax.set_yticks([-100, 0, 100])
    ax.set_zticks([0, 0.5, 1, 1.5])
    ax.set_zticklabels(["0", "0.5", "1", "1.5"])
    ax.text2D(0.012, 0.66, r"$\times 10^{4}$", transform=ax.transAxes,
              fontsize=8.5, color="#444444")
    axis_style(ax)
    fit_zoom(fig, ax, "tr")
    redrect(fig, spec)
    save(fig, "tr")


# ── BL: non-convex — four annotated features, one red reference line ─────────
def plot_bl():
    spec = PLOTS["bl"]
    fig, ax = figure(spec)
    x = np.linspace(-3, 3, 120)
    X, Y = np.meshgrid(x, x)
    Z = (3.0 * np.sin(X * 1.35) * np.cos(Y * 1.35)
         + 1.5 * np.sin(2 * X * 1.35) * np.cos(2 * Y * 1.35) * 0.7)
    ax.plot_surface(X, Y, Z, cmap=JET, rstride=1, cstride=1,
                    linewidth=0, antialiased=True, shade=True)

    # measured original: x,y in [-3,3] with tick STEP 1.5, a "y" axis label,
    # and z from -4 to 8.
    ax.set_xlim(-3, 3); ax.set_ylim(-3, 3); ax.set_zlim(-4, 8)
    ax.set_xticks([-3.0, -1.5, 0.0, 1.5, 3.0])
    ax.set_yticks([-3.0, -1.5, 0.0, 1.5, 3.0])
    ax.set_xticklabels(["-3", "-1.5", "0", "1.5", "3"])
    ax.set_yticklabels(["-3", "-1.5", "0", "1.5", "3"])
    ax.set_zticks([-4, -2, 0, 2, 4, 6, 8])
    ax.set_zlabel("y", fontsize=7.5, color="#444444", labelpad=-4)
    axis_style(ax)

    # annotation label ink centres in SLIDE px (measured) -> 3-D feature points
    ANCH = {
        "Global":  (0, 0),
        "LocalMx": (-2.1, 0),
        "LocalMn": (-1.1, -1.1),
        "GlobalMn": (1.4, 1.4),
    }
    LABELS = {
        "Global":   ("Global Maxima",  254, 307),
        "LocalMx":  ("Local Maxima",   312, 396),
        "LocalMn":  ("Local Minima",   313, 458),
        "GlobalMn": ("Global Minima",  156, 455),
    }

    def extremum(key, want_max):
        cx, cy = ANCH[key]
        d = (X - cx) ** 2 + (Y - cy) ** 2
        m = d < 1.2 ** 2
        masked = np.where(m, Z, -1e9 if want_max else 1e9)
        i = np.argmax(masked) if want_max else np.argmin(masked)
        return X.flat[i], Y.flat[i], Z.flat[i]

    PEAK = {"Global": extremum("Global", True), "LocalMx": extremum("LocalMx", True),
            "LocalMn": extremum("LocalMn", False), "GlobalMn": extremum("GlobalMn", False)}

    for key, (label, sx, sy) in LABELS.items():
        # 3-D text placed just above the feature, leader line to the label side
        fx, fy, fz = PEAK[key]
        ax.text(fx, fy, fz + 0.12, "", fontsize=8)
        dirx = -1.0 if sx < 265 else 1.0
        diry = -1.0 if sy < 346 else 1.0
        ex, ey = fx + dirx * 0.85, fy + diry * 0.85
        ax.plot([fx, ex], [fy, ey], [fz + 0.12, 1.2], color=BLK, lw=0.9, zorder=25)
        ax.text(ex, ey, 1.2, label, fontsize=8.5, color=BLK, ha="center",
                va="bottom", zorder=30, linespacing=1.05)

    fit_zoom(fig, ax, "bl")
    redrect(fig, spec)
    save(fig, "bl")


# ── BR: gradient-descent path into a valley, no reference line ───────────────
def plot_br():
    spec = PLOTS["br"]
    fig, ax = figure(spec)
    x = np.linspace(-3, 3, 120)
    X, Y = np.meshgrid(x, x)
    Z = 0.55 * ((X - 0.6) ** 2 + (Y + 0.5) ** 2)
    ax.plot_surface(X, Y, Z, cmap=JET, rstride=1, cstride=1,
                    linewidth=0, antialiased=True, shade=True, alpha=0.94)

    # analytic dense gradient-descent trajectory (one smooth curve)
    def grad(px, py):
        return 1.1 * (px - 0.6), 1.1 * (py + 0.5)

    px, py = -2.35, 2.30
    lr = 0.22
    path = []
    for _ in range(240):
        path.append((px, py))
        gx, gy = grad(px, py)
        px -= lr * gx
        py -= lr * gy
    path = np.array(path)
    pz = 0.55 * ((path[:, 0] - 0.6) ** 2 + (path[:, 1] + 0.5) ** 2) \
        + 0.35 * np.sin(1.1 * path[:, 0]) * np.cos(1.1 * path[:, 1])

    # second-difference ripple check: one smooth analytic curve -- successive
    # step directions must keep turning consistently (no zig-zag oscillation).
    seg = np.diff(path, axis=0)
    ang = []
    for i in range(len(seg) - 1):
        a, b = seg[i], seg[i + 1]
        na, nb = np.linalg.norm(a), np.linalg.norm(b)
        if na > 1e-12 and nb > 1e-12:
            ang.append(float(np.dot(a, b) / (na * nb)))
    ang = np.array(ang)
    assert ang.min() > 0.0, "gradient path zig-zags (min cos = %.3f)" % ang.min()
    assert np.all(np.diff(ang) <= 1e-9), "gradient path turn rate is not monotone"

    ax.plot(path[:, 0], path[:, 1], pz, color="black", lw=2.2,
            zorder=25, solid_capstyle="round")

    for idx in (28, 62, 96, 130, 168, 205, 232):
        a = np.array([path[idx, 0], path[idx, 1], pz[idx]])
        bb = np.array([path[idx + 1, 0], path[idx + 1, 1], pz[idx + 1]])
        d = bb - a
        n = np.linalg.norm(d)
        if n > 0:
            ax.quiver(a[0], a[1], a[2],
                      d[0] / n * 0.30, d[1] / n * 0.30, d[2] / n * 0.30,
                      color="black", arrow_length_ratio=0.55, linewidth=2.0, zorder=26)

    ax.set_xlim(-3, 3); ax.set_ylim(-3, 3); ax.set_zlim(-1, 6.5)
    ax.set_xticks([]); ax.set_yticks([]); ax.set_zticks([])
    axis_style(ax)
    fit_zoom(fig, ax, "br")
    redrect(fig, spec)
    save(fig, "br")


plot_tl()
plot_tr()
plot_bl()
plot_br()
print("all four plots written", FIT_ZOOMS)
