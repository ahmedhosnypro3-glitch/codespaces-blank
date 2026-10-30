#!/usr/bin/env python3
"""Second-difference ripple check for the four slide-025 curves.

Every surface/curve on the slide must be ONE smooth analytic/dense-sampled
curve: rebuild each function from the same closed form used in
generate_plots_025.py and assert its second difference stays within tolerance
along every axis (no sawtooth / ripple / per-sample noise).
"""
import numpy as np

TOL = 0.35


def d2max(f, lo, hi, n):
    x = np.linspace(lo, hi, n)
    return float(np.abs(np.diff(f(x), 2)).max())


results = []
# TL concave dome: z = 4*exp(-0.62 r^2) along any radial cut
results.append(("TL dome radial z=4exp(-0.62 r^2)", d2max(lambda r: 4 * np.exp(-0.62 * r * r), -2, 2, 200)))
# TR convex bowl: z = 1.5(x^2+y^2)/10000 along x at y=0
results.append(("TR bowl x-cut z=1.5x^2/10000", d2max(lambda x: 1.5 * x * x / 10000.0, -100, 100, 200)))
# BL non-convex: 3sin(1.35x)cos(1.35y) + 1.05 sin(2.7x)cos(2.7y), y=0
results.append(("BL non-convex x-cut", d2max(lambda x: 3 * np.sin(1.35 * x) + 1.05 * np.sin(2.7 * x), -3, 3, 240)))
# BR bowl surface x-cut
results.append(("BR bowl x-cut z=0.55(x-.6)^2", d2max(lambda x: 0.55 * ((x - 0.6) ** 2), -3, 3, 240)))

# BR analytic gradient-descent trajectory: must keep turning one way
px, py, lr = -2.35, 2.30, 0.22
path = []
for _ in range(240):
    path.append((px, py))
    gx, gy = 1.1 * (px - 0.6), 1.1 * (py + 0.5)
    px -= lr * gx
    py -= lr * gy
path = np.array(path)
seg = np.diff(path, axis=0)
cos = []
for i in range(len(seg) - 1):
    a, b = seg[i], seg[i + 1]
    na, nb = np.linalg.norm(a), np.linalg.norm(b)
    if na > 1e-12 and nb > 1e-12:
        cos.append(float(np.dot(a, b) / (na * nb)))
cos = np.array(cos)
results.append(("BR GD path turn cos (must be >0)", float(cos.min())))
results.append(("BR GD path turn monotone (max diff)", float(np.diff(cos).max())))

print("=== second-difference ripple check (tol %.2f) ===" % TOL)
fails = 0
for name, v in results:
    if "turn cos" in name:
        ok = v > 0.0
    elif "monotone" in name:
        ok = v <= 1e-9
    else:
        ok = v <= TOL
    if not ok:
        fails += 1
    print("  %-34s = %.6f  %s" % (name, v, "OK" if ok else "FAIL"))
print("ALL SMOOTH" if fails == 0 else "RIPPLE DETECTED in %d curve(s)" % fails)
raise SystemExit(1 if fails else 0)
