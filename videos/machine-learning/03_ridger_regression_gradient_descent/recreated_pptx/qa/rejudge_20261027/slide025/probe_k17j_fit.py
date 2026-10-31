#!/usr/bin/env python3
"""Fast analytic fit of mplot3d (elev, azim, z-aspect) to the orig BR silhouette.

No figures: build the projection matrix exactly like Axes3D.get_proj with
focal_length=inf (orthographic), box_aspect rolled to vertical, then
proj_transform the 8 box corners and compare silhouette extremes to measured.
"""
import numpy as np
from PIL import Image
import matplotlib
matplotlib.use("Agg")
from mpl_toolkits.mplot3d import proj3d

NS = "/home/codespace/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
orig = np.array(Image.open(NS + "/unique_slides/slide_025.jpg").convert("RGB")).astype(np.int32)
X0, Y0, X1, Y1 = 615, 344, 881, 532
p = orig[Y0:Y1, X0:X1]
H, W = p.shape[:2]


def colmask(a):
    mx, mn = a.max(2), a.min(2)
    red = (a[:, :, 0] > 170) & (a[:, :, 1] < 90) & (a[:, :, 2] < 90)
    return ((mx - mn) > 60) & (mx > 90) & ~red


m = colmask(p)
m[:8] = False; m[-8:] = False; m[:, :8] = False; m[:, -8:] = False
ys, xs = np.nonzero(m)
iL, iR, iT, iB = xs.argmin(), xs.argmax(), ys.argmin(), ys.argmax()
MEAS = dict(bbox=(xs.min(), xs.max(), ys.min(), ys.max()),
            L=np.array([xs[iL], ys[iL]], float), R=np.array([xs[iR], ys[iR]], float),
            T=np.array([xs[iT], ys[iT]], float), B=np.array([xs[iB], ys[iB]], float))
print("measured local bbox=%s L=%s R=%s T=%s B=%s colored%%=%.1f" % (
    MEAS["bbox"], MEAS["L"], MEAS["R"], MEAS["T"], MEAS["B"], 100 * m.mean()))

# z-axis vertical line scan
lum = 0.299 * p[:, :, 0] + 0.587 * p[:, :, 1] + 0.114 * p[:, :, 2]
sat = p.max(2) - p.min(2)
dark = (lum < 120) & (sat < 90)
print("\nz-axis scan slide x725..748 (run>=15):")
for lx in range(725 - X0, 749 - X0):
    col = dark[:, lx]
    best = 0; besty = 0; cur = 0
    for y in range(H):
        if col[y]:
            cur += 1
            if cur > best:
                best = cur; besty = y - cur + 1
        else:
            cur = 0
    if best >= 8:
        print("  slide x%d run=%d slide y %d..%d" % (X0 + lx, best, Y0 + besty, Y0 + besty + best - 1))


def proj_matrix(elev, azim, xlim, ylim, zlim, box_aspect, dist=10.0):
    """Mirror of Axes3D.get_proj for orthographic (focal_length=inf)."""
    xmin, xmax = xlim; ymin, ymax = ylim; zmin, zmax = zlim
    ba = np.asarray(box_aspect, float)
    worldM = proj3d.world_transformation(xmin, xmax, ymin, ymax, zmin, zmax, pb_aspect=ba)
    R = 0.5 * ba
    e = np.deg2rad(elev); a = np.deg2rad(azim)
    p0 = np.cos(e) * np.cos(a)
    p1 = np.cos(e) * np.sin(a)
    p2 = np.sin(e)
    # _roll_to_vertical with default z-axis: identity for [p0,p1,p2] (vertical z)
    ps = np.array([p0, p1, p2])
    eye = R + dist * ps
    # _calc_view_axes: w = eye - R normalized (out of screen), u = cross(v_up?..)
    # mpl: u,v,w = _calc_view_axes(eye): uses world up (0,0,1)? replicate:
    # from axes3d source:
    #   w = eye - R; w = w/norm
    #   u = cross([0,0,1]? , w)... let's just call the private helpers:
    import mpl_toolkits.mplot3d.axes3d as a3
    u, v, w = a3.Axes3D._calc_view_axes(None, eye) if False else _calc_view_axes(eye, R)
    viewM = proj3d._view_transformation_uvw(u, v, w, eye)
    projM = proj3d._ortho_transformation(-dist, dist)
    M0 = viewM @ worldM
    return projM @ M0


def _calc_view_axes(eye, R):
    # copy of Axes3D._calc_view_axes static logic (vertical z)
    w = eye - R
    w = w / np.linalg.norm(w)
    # u = normalize(cross(up, w)) with up = (0,0,1) rolled -> (0,0,1)
    up = np.array([0.0, 0.0, 1.0])
    u = np.cross(up, w)
    u = u / np.linalg.norm(u)
    v = np.cross(w, u)
    return u, v, w


def proj_box(elev, azim, xlim, ylim, zlim, box_aspect):
    M = proj_matrix(elev, azim, xlim, ylim, zlim, box_aspect)
    cs = np.array([[x, y, z] for x in xlim for y in ylim for z in zlim], float)
    x2, y2, _ = proj3d.proj_transform(cs[:, 0], cs[:, 1], cs[:, 2], M)
    return np.stack([x2, y2], 1)


xlim = (-3, 3); ylim = (-3, 3)
results = []
for elev in range(10, 61, 2):
    for azim in range(-120, -9, 3):
        for zr in np.arange(1.5, 8.01, 0.25):
            P = proj_box(elev, azim, xlim, ylim, (0.0, zr), (6, 6, zr))
            mn, mx = P.min(0), P.max(0)
            span = mx - mn
            if span[0] < 1e-9 or span[1] < 1e-9:
                continue
            tspan = np.array([MEAS["bbox"][1] - MEAS["bbox"][0],
                              MEAS["bbox"][3] - MEAS["bbox"][2]], float)
            s = tspan / span
            Pn = (P - mn) * s
            Pn[:, 1] = tspan[1] - Pn[:, 1]   # flip y to image coords
            Pn[:, 0] += MEAS["bbox"][0]; Pn[:, 1] += MEAS["bbox"][2]
            iL2, iR2 = Pn[:, 0].argmin(), Pn[:, 0].argmax()
            iT2, iB2 = Pn[:, 1].argmin(), Pn[:, 1].argmax()
            err = (np.hypot(*(Pn[iL2] - MEAS["L"])) + np.hypot(*(Pn[iR2] - MEAS["R"]))
                   + np.hypot(*(Pn[iT2] - MEAS["T"])) + np.hypot(*(Pn[iB2] - MEAS["B"])))
            results.append((err, elev, azim, float(zr)))
results.sort()
print("\ntop 20 fits (err, elev, azim, zr):")
for r in results[:20]:
    print("  err=%6.2f elev=%2d azim=%4d zr=%.2f" % r)

# detail for the best: predicted corner map
err, elev, azim, zr = results[0]
P = proj_box(elev, azim, xlim, ylim, (0.0, zr), (6, 6, zr))
mn, mx = P.min(0), P.max(0)
tspan = np.array([MEAS["bbox"][1] - MEAS["bbox"][0], MEAS["bbox"][3] - MEAS["bbox"][2]], float)
s = tspan / (mx - mn)
Pn = (P - mn) * s
Pn[:, 1] = tspan[1] - Pn[:, 1]
Pn[:, 0] += MEAS["bbox"][0]; Pn[:, 1] += MEAS["bbox"][2]
names = ["xlo,ylo,zlo", "xlo,ylo,zhi", "xlo,yhi,zlo", "xlo,yhi,zhi",
         "xhi,ylo,zlo", "xhi,ylo,zhi", "xhi,yhi,zlo", "xhi,yhi,zhi"]
print("\nbest fit elev=%d azim=%d zr=%.2f err=%.2f — corner projections (local px):" % (elev, azim, zr, err))
for n_, q in zip(names, Pn):
    print("  %-12s (%6.1f, %6.1f)" % (n_, q[0], q[1]))
print("measured: bbox=%s L=%s R=%s T=%s B=%s" % (MEAS["bbox"], MEAS["L"], MEAS["R"], MEAS["T"], MEAS["B"]))
