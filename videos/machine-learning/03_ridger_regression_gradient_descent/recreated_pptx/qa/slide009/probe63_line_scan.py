# probe63_line_scan.py — hunt for the measurement-arrow shaft and the
# founder-reported "red line parallel to the blue line" in the ORIGINAL frame.
# Method: redness = r - max(g,b) (positive for red/pink ink, ~0 for grey/white,
# strongly positive for orange). Score candidate straight lines by mean redness
# sampled along them, and report the best parallel/perpendicular fits.
import numpy as np
from PIL import Image

FR = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_009.jpg"
a = np.asarray(Image.open(FR).convert("RGB")).astype(int)
r, g, b = a[..., 0], a[..., 1], a[..., 2]
redness = r - np.maximum(g, b)
sat = a.max(axis=2) - a.min(axis=2)

def line_score(p0, p1, xlo, xhi, ylo, yhi, use="red"):
    m = redness if use == "red" else sat
    (x0, y0), (x1, y1) = p0, p1
    n = max(int(np.hypot(x1 - x0, y1 - y0)) * 2, 2)
    xs = np.linspace(x0, x1, n); ys = np.linspace(y0, y1, n)
    vals = []
    for x, y in zip(xs, ys):
        if not (xlo <= x <= xhi and ylo <= y <= yhi):
            continue
        xi, yi = int(round(x)), int(round(y))
        if 0 <= xi < a.shape[1] and 0 <= yi < a.shape[0]:
            vals.append(m[yi, xi])
    if len(vals) < 8:
        return None
    vals = np.array(vals)
    return float(vals.mean()), float(np.percentile(vals, 90)), float(vals.max()), len(vals)

PANEL = {
    "LEFT":  dict(xlo=100, xhi=460, ylo=115, yhi=468, out=(197.5, 145.0), slope=-0.52129, icpt=425.31,
                  orange=[(197.5,145.0),(188.5,355.5),(176.5,380.5),(242.5,327.5),(260.5,333.5),
                          (294.0,333.5),(324.0,290.0),(328.5,332.0),(381.5,301.5),(397.5,249.0),
                          (421.5,255.0),(233.5,362.0)], disc=(232.5,241.0)),
    "RIGHT": dict(xlo=495, xhi=862, ylo=115, yhi=468, out=(611.0, 145.0), slope=-0.48190, icpt=656.82,
                  orange=[(611.0,145.0),(601.5,355.5),(589.5,380.5),(656.0,327.0),(674.0,333.5),
                          (707.5,333.5),(737.5,290.0),(741.5,332.0),(794.0,302.0),(810.0,249.0),
                          (834.5,255.0),(647.0,362.0)], disc=None),
}

for name, P in PANEL.items():
    ox, oy = P["out"]
    print(f"\n########## {name}  outlier=({ox},{oy})  blue slope={P['slope']:.5f} ##########")

    # A) PARALLEL lines to the blue line, sweeping the intercept.
    #    A line through the outlier has b = oy - slope*ox.
    b_out = oy - P["slope"] * ox
    best = []
    for d in np.arange(-260, 261, 2.0):          # offset in y at x=ox
        bb = b_out + d
        xa = max(P["xlo"], 110); xb = min(P["xhi"], 855)
        p0 = (xa, P["slope"] * xa + bb); p1 = (xb, P["slope"] * xb + bb)
        s = line_score(p0, p1, P["xlo"], P["xhi"], P["ylo"], P["yhi"])
        if s:
            best.append((s[0], s[1], s[2], round(d, 1), s[3]))
    best.sort(reverse=True)
    print("  A) best PARALLEL-to-blue lines (mean redness, p90, max, y-offset-at-outlier, n):")
    for row in best[:8]:
        print(f"     mean={row[0]:6.2f} p90={row[1]:6.2f} max={row[2]:6.1f} offset_y={row[3]:7.1f} n={row[4]}")

    # B) PERPENDICULAR lines through the outlier, sweeping the angle.
    bestp = []
    for ang in np.arange(45.0, 80.01, 0.25):
        t = np.radians(ang)
        dx, dy = np.cos(t), np.sin(t)
        L = 260
        p0 = (ox - dx * 20, oy - dy * 20); p1 = (ox + dx * L, oy + dy * L)
        s = line_score(p0, p1, P["xlo"], P["xhi"], P["ylo"], P["yhi"])
        if s:
            bestp.append((s[0], s[1], s[2], round(ang, 2), s[3]))
    bestp.sort(reverse=True)
    print("  B) best lines THROUGH THE OUTLIER (mean redness, p90, max, angle, n):")
    for row in bestp[:8]:
        print(f"     mean={row[0]:6.2f} p90={row[1]:6.2f} max={row[2]:6.1f} angle={row[3]:6.2f} n={row[4]}")

    # C) same sweep but with SATURATION (catches pale pink lines that redness may miss)
    bests = []
    for ang in np.arange(45.0, 80.01, 0.25):
        t = np.radians(ang)
        dx, dy = np.cos(t), np.sin(t)
        L = 260
        p0 = (ox - dx * 20, oy - dy * 20); p1 = (ox + dx * L, oy + dy * L)
        s = line_score(p0, p1, P["xlo"], P["xhi"], P["ylo"], P["yhi"], use="sat")
        if s:
            bests.append((s[0], s[1], s[2], round(ang, 2), s[3]))
    bests.sort(reverse=True)
    print("  C) best-through-outlier by SATURATION:")
    for row in bests[:6]:
        print(f"     mean={row[0]:6.2f} p90={row[1]:6.2f} max={row[2]:6.1f} angle={row[3]:6.2f} n={row[4]}")

    # D) perpendicular foot + length of the true orthogonal projection
    #    (least-squares refit of the blue line inside the panel)
    xs, ys = [], []
    for x in range(P["xlo"], P["xhi"]):
        for y in range(P["ylo"], P["yhi"]):
            if b[y, x] > 110 and r[y, x] < 100 and g[y, x] < 100:
                xs.append(x); ys.append(y)
    A = np.vstack([xs, np.ones(len(xs))]).T
    sol, *_ = np.linalg.lstsq(A, ys, rcond=None)
    m, c = sol
    qx, qy = ox, oy
    t = ((qx - 555) * 1 + 0)  # placeholder
    # foot via projection onto direction (1,m)
    x0 = xs[0]
    px, py = (0, 0)
    # use two points on the fitted line: x=min/max
    x_a, x_b = min(xs), max(xs)
    pa = (x_a, m * x_a + c); pb = (x_b, m * x_b + c)
    dxv, dyv = pb[0] - pa[0], pb[1] - pa[1]
    tt = ((qx - pa[0]) * dxv + (qy - pa[1]) * dyv) / (dxv * dxv + dyv * dyv)
    foot = (pa[0] + tt * dxv, pa[1] + tt * dyv)
    length = np.hypot(foot[0] - qx, foot[1] - qy)
    perp_ang = np.degrees(np.arctan2(foot[1] - qy, foot[0] - qx))
    print(f"  D) blue refit: y={m:.5f}x+{c:.2f}; ORTHOGONAL foot=({foot[0]:.1f},{foot[1]:.1f}) "
          f"length={length:.1f}px angle={perp_ang:.1f}deg")
    print(f"     implied mm/px from label: {(50.85 if name=='LEFT' else 63.64)}/{length:.1f} = "
          f"{(50.85 if name=='LEFT' else 63.64)/length:.4f} mm/px")
