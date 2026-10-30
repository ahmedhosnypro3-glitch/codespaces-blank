#!/usr/bin/env python3
"""Independent PIL verification of slide 009 render_5 vs the original frame (worker
w009-root-20261024, verification round). 960x540 frame = 1px=1pt; render_5 is 150dpi
(2001x1125, scale 2.08333 render-px per frame-px). Verifies the geometry the certified
full-slide verdict (judge_attempt_5.txt) asserts, element by element, BEFORE spending
gateway slots. Every number printed here is banked evidence."""
import numpy as np
from PIL import Image

Q = "videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide009"
ORIG = "videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_009.jpg"
S = 2001 / 540.0

orig = np.asarray(Image.open(ORIG).convert("RGB")).astype(np.int16)
rnd = np.asarray(Image.open(f"{Q}/render_5.png").convert("RGB")).astype(np.int16)


def ink(a):
    """non-white-ish ink mask (panel E9E9E7 sums to 699; require <680 to exclude panel)"""
    return a.sum(axis=2) < 680


def bbox(mask, x0, y0, x1, y1):
    sub = mask[y0:y1, x0:x1]
    ys, xs = np.nonzero(sub)
    if not len(xs):
        return None
    return (int(xs.min()) + x0, int(ys.min()) + y0, int(xs.max()) + x0, int(ys.max()) + y0)


# colour families (measured cores from the certified verdict)
def near(a, rgb, tol=40):
    return (np.abs(a - np.array(rgb)).max(axis=2) <= tol)


def census(mask):
    ys, xs = np.nonzero(mask)
    return len(xs), (int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())) if len(xs) else None


o_ink, r_ink = ink(orig), ink(rnd)
print(f"scale={S:.5f}  render={rnd.shape[1]}x{rnd.shape[0]}")

# --- 1. house chrome: no top stroke, panel bounds ---
top_band_o = near(orig, (192, 0, 0), 30)[0:60, :].sum()
top_band_r = near(rnd, (192, 0, 0), 30)[0:150, :].sum()
print(f"[chrome] red px in TOP band: original={top_band_o} render={150 and top_band_r} (both must be 0: no top stroke)")
left_r = near(rnd, (192, 0, 0), 30)[:, 118:126].sum()
right_r = near(rnd, (192, 0, 0), 30)[:, 1875:1883].sum()
print(f"[chrome] render stroke columns L117..125={left_r} R1875..1882={right_r} (present)")

# --- 2. equation boxes: ink inside box with padding, no border touch ---
for name, (ex0, ey0, ex1, ey1) in (("eq_left", (216, 148, 317, 175)), ("eq_right", (631, 148, 734, 175))):
    # render coords
    rx0, ry0, rx1, ry1 = [int(round(v * S)) for v in (ex0, ey0, ex1, ey1)]
    sub = r_ink[ry0:ry1, rx0:rx1]
    ys, xs = np.nonzero(sub)
    assert len(xs), f"{name}: EMPTY equation region in render (BLOCKER)"
    bb = (int(xs.min()) + rx0, int(ys.min()) + ry0, int(xs.max()) + rx0, int(ys.max()) + ry0)
    pad_l = bb[0] - rx0; pad_r = rx1 - bb[2]; pad_t = bb[1] - ry0; pad_b = ry1 - bb[3]
    # dark ink only (equation glyphs are near-black/navy on pale-cyan fill)
    dark = (rnd.sum(axis=2) < 300)[ry0:ry1, rx0:rx1]
    dys, dxs = np.nonzero(dark)
    dbb = (int(dxs.min()) + rx0, int(dys.min()) + ry0, int(dxs.max()) + rx0, int(dys.max()) + ry0)
    print(f"[{name}] ink in box=YES nonzero={int(sub.sum())} pad L/R/T/B={pad_l}/{pad_r}/{pad_t}/{pad_b}px(render) "
          f"dark-glyph bbox={dbb} (all pads >0 -> no border touch)")
    # original side: dark ink bbox in the same frame region
    odark = (orig.sum(axis=2) < 300)[ey0:ey1, ex0:ex1]
    oys, oxs = np.nonzero(odark)
    obb = (int(oxs.min()) + ex0, int(oys.min()) + ey0, int(oxs.max()) + ex0, int(oys.max()) + ey0)
    print(f"[{name}] original dark bbox={obb} render dark bbox(frame px)="
          f"{tuple(round(v / S) for v in dbb)}")

# --- 3. fitted lines: per-column core spans (render), slope on original ---
blue_o = near(orig, (0, 0, 255), 60)
blue_r = near(rnd, (0, 0, 255), 60)


def line_span(mask, x0, x1, y0, y1):
    sub = mask[y0:y1, x0:x1]
    cols = []
    for c in range(sub.shape[1]):
        ys = np.nonzero(sub[:, c])[0]
        if len(ys):
            cols.append((c + x0, int(ys.mean()) + y0, len(ys)))
    return cols


for name, (x0, x1, y0, y1) in (("LEFT", (95, 466, 107, 474)), ("RIGHT", (486, 871, 107, 474))):
    cols_o = line_span(blue_o, x0, x1, y0, y1)
    rx0, rx1, ry0, ry1 = [int(round(v * S)) for v in (x0, x1, y0, y1)]
    cols_r = line_span(blue_r, rx0, rx1, ry0, ry1)
    if cols_o and cols_r:
        (cx0, cy0, _), (cx1, cy1, _) = cols_o[0], cols_o[-1]
        (rx0c, ry0c, _), (rx1c, ry1c, _) = cols_r[0], cols_r[-1]
        slope_o = (cy1 - cy0) / (cx1 - cx0)
        slope_r = (ry1c - ry0c) / (rx1c - rx0c)
        print(f"[{name}] fitted line: orig endpoints ({cx0},{cy0})->({cx1},{cy1}) slope={slope_o:.4f} | "
              f"render endpoints (frame px) ({rx0c/S:.1f},{ry0c/S:.1f})->({rx1c/S:.1f},{ry1c/S:.1f}) slope={slope_r:.4f} "
              f"| |dslope|={abs(slope_o-slope_r):.4f}")

# --- 4. orange point census per chart ---
orange_o = near(orig, (255, 165, 0), 45)
orange_r = near(rnd, (255, 165, 0), 45)
for name, (x0, x1, y0, y1) in (("LEFT", (95, 466, 107, 474)), ("RIGHT", (486, 871, 107, 474))):
    sub = orange_o[y0:y1, x0:x1]
    # count connected blobs roughly via horizontal runs
    lbl = np.zeros_like(sub, dtype=int)
    n = 0
    from collections import deque
    seen = np.zeros_like(sub, dtype=bool)
    for i in range(sub.shape[0]):
        for j in range(sub.shape[1]):
            if sub[i, j] and not seen[i, j]:
                n += 1
                q = deque([(i, j)]); seen[i, j] = True
                while q:
                    a, b = q.popleft()
                    for da in (-1, 0, 1):
                        for db in (-1, 0, 1):
                            na, nb = a + da, b + db
                            if 0 <= na < sub.shape[0] and 0 <= nb < sub.shape[1] and sub[na, nb] and not seen[na, nb]:
                                seen[na, nb] = True; q.append((na, nb))
    rx0, rx1, ry0, ry1 = [int(round(v * S)) for v in (x0, x1, y0, y1)]
    subr = orange_r[ry0:ry1, rx0:rx1]
    # render points: use erosion-resistant blob count on downscaled
    small = np.asarray(Image.fromarray((subr * 255).astype(np.uint8)).resize(
        (subr.shape[1] // 4, subr.shape[0] // 4), Image.BOX)).astype(bool)
    seenr = np.zeros_like(small, dtype=bool); nr = 0
    for i in range(small.shape[0]):
        for j in range(small.shape[1]):
            if small[i, j] and not seenr[i, j]:
                nr += 1
                q = deque([(i, j)]); seenr[i, j] = True
                while q:
                    a, b = q.popleft()
                    for da in (-1, 0, 1):
                        for db in (-1, 0, 1):
                            na, nb = a + da, b + db
                            if 0 <= na < small.shape[0] and 0 <= nb < small.shape[1] and small[na, nb] and not seenr[na, nb]:
                                seenr[na, nb] = True; q.append((na, nb))
    print(f"[{name}] orange points: original blobs={n} render blobs(4x-box)={nr}")

# --- 5. dashed residual connectors present in render (periwinkle family) ---
peri_r = near(rnd, (180, 178, 210), 35)
cnt, bb = census(peri_r)
print(f"[connectors] periwinkle B4B2D2-family ink in render: px={cnt} bbox={bb} (present if >1000)")

# --- 6. frame containment: content ink must stay inside house panel x54..903 y45..540 (frame px) ---
panel_r = r_ink.copy()
panel_r[:, :int(54 * S)] = False; panel_r[:, int(903 * S):] = False
panel_r[:int(45 * S), :] = False
outside = panel_r.sum()
print(f"[containment] render content ink OUTSIDE house panel (x<54/x>903/y<45 frame px): {outside} px (must be 0)")

# --- 7. captions: two-line bands inside caption boxes ---
for name, (x0, y0, x1, y1) in (("cap_left", (95, 479, 434, 529)), ("cap_right", (501, 479, 842, 529))):
    bb = bbox(r_ink, int(x0 * S), int(y0 * S), int(x1 * S), int(y1 * S))
    bb_o = bbox(o_ink, x0, y0, x1, y1)
    print(f"[{name}] render ink bbox(frame px)={tuple(round(v / S, 1) for v in bb) if bb else None} "
          f"original={bb_o} inside box: {bb and x0 <= bb[0] / S and bb[2] / S <= x1 and y0 <= bb[1] / S and bb[3] / S <= y1}")

print("VERIFY DONE")
