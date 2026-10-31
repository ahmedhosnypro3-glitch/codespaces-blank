#!/usr/bin/env python3
"""PIL verifier r1 for candidate BL assets (slide 025, deck 03).

Ground truth (original frame px, 960x540). Asset mapping per task spec:
  scale s = asset_width / 411, origin frame (60, 296)
  asset = (frame - origin) * s   (uniform s on both axes)

Anchors (frame px, inclusive):
  Global Maxima x242..268 y304..319
  Local Maxima  x286..315 y337..352
  Local Minima  x286..311 y390..399
  Global Minima x145..201 y439..465
  red X markers at (199,445), (270,482)
  red hline y418 x124..381
  red rect x80..472 y292..527

Checks per candidate asset:
  C1 ink density > 0.01 in each of the 4 label anchor boxes (asset px)
  C2 red X px (>=8 in +-12 asset px window) near both markers AND zero red px
     inside any label box
  C3 red hline at y418 (band y+-2 frame px, x124..381): red column coverage > 0.8
  C4 diff vs baseline build/assets/plot_025_bl.png (md5 7a8e7210...): fraction of
     asset px changed (|d|>10 any channel) < 0.08, and reported outside the
     annotation regions (label boxes + marker windows + hline band, padded)
  C5 text height in each label box (ink row extent) ~= 15 frame px * s
     (PASS within [0.5x, 1.5x] of expected)

Modes:
  verify <png> [tag]   verify one asset, print + append to bl_verify_r1.md
  watch                poll assets_k17r/k17s/k17t3 every 60s up to 90 min,
                       verify each new candidate (by md5), maintain the md
Read-only wrt build files; never deletes anything.
"""
import hashlib
import os
import sys
import time
from datetime import datetime

import numpy as np
from PIL import Image

NS = "/home/codespace/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
RJ = os.path.join(NS, "recreated_pptx/qa/rejudge_20261027/slide025")
BASELINE = os.path.join(NS, "recreated_pptx/build/assets/plot_025_bl.png")
BASELINE_MD5 = "7a8e7210f118b728245d268552a7d32d"
MD = os.path.join(RJ, "bl_verify_r1.md")
LEG = os.path.join(RJ, "bl_labels_leg.txt")
WATCH_DIRS = ["assets_k17r", "assets_k17s", "assets_k17t3"]

ORIGIN = (60.0, 296.0)
FRAME_W = 411.0

ANCHORS = [
    ("Global Maxima", 242, 268, 304, 319),
    ("Local Maxima", 286, 315, 337, 352),
    ("Local Minima", 286, 311, 390, 399),
    ("Global Minima", 145, 201, 439, 465),
]
RED_X = [(199, 445), (270, 482)]
RED_HLINE = (418, 124, 381)  # y, x0, x1
RED_RECT = (80, 472, 292, 527)

INK_DENSITY_THR = 0.01
X_WIN = 12          # asset px half-window around converted marker center
X_MIN_PX = 8
HLINE_COVER_THR = 0.80
DIFF_THR = 0.08
DIFF_DELTA = 10
EXP_TEXT_FRAME_PX = 15.0


def md5(path):
    h = hashlib.md5()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def redmask(a):
    r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
    return (r > 110) & (r - g > 50) & (r - b > 50)


def darkmask(a):
    lum = 0.299 * a[:, :, 0] + 0.587 * a[:, :, 1] + 0.114 * a[:, :, 2]
    return lum < 100


def to_asset_box(s, x0, y0, x1, y1):
    ax0 = int(np.floor((x0 - ORIGIN[0]) * s))
    ay0 = int(np.floor((y0 - ORIGIN[1]) * s))
    ax1 = int(np.ceil((x1 + 1 - ORIGIN[0]) * s))
    ay1 = int(np.ceil((y1 + 1 - ORIGIN[1]) * s))
    return ax0, ay0, ax1, ay1


def verify(png, tag=""):
    im = Image.open(png).convert("RGB")
    a = np.asarray(im).astype(np.int32)
    H, W = a.shape[:2]
    s = W / FRAME_W
    rm = redmask(a)
    dm = darkmask(a)
    res = {"path": png, "tag": tag, "md5": md5(png), "size": (W, H), "scale": s,
           "time": datetime.now().isoformat(timespec="seconds"), "checks": {}}

    # C1 + C2-collision + C5 per label box
    c1_ok = True
    c5_ok = True
    c2_coll_ok = True
    labels = []
    for name, x0, x1, y0, y1 in ANCHORS:
        ax0, ay0, ax1, ay1 = to_asset_box(s, x0, y0, x1, y1)
        ax1 = min(ax1, W)
        ay1 = min(ay1, H)
        box_dm = dm[ay0:ay1, ax0:ax1]
        box_rm = rm[ay0:ay1, ax0:ax1]
        dens = float(box_dm.mean())
        red_n = int(box_rm.sum())
        ink = dens > INK_DENSITY_THR
        nored = red_n == 0
        rows = np.nonzero(box_dm.any(1))[0]
        th = int(rows.max() - rows.min() + 1) if rows.size else 0
        exp = EXP_TEXT_FRAME_PX * s
        th_ok = (0.5 * exp) <= th <= (1.5 * exp) if rows.size else False
        c1_ok &= ink
        c2_coll_ok &= nored
        c5_ok &= th_ok
        labels.append({"name": name, "frame": (x0, x1, y0, y1),
                       "asset": (ax0, ay0, ax1, ay1), "ink_density": dens,
                       "red_px": red_n, "ink_ok": ink, "nored_ok": nored,
                       "text_h_px": th, "text_h_exp_px": exp, "text_h_ok": th_ok})
    res["checks"]["C1_ink"] = {"ok": c1_ok, "labels": labels}
    res["checks"]["C2_collision"] = {"ok": c2_coll_ok}
    res["checks"]["C5_text_height"] = {"ok": c5_ok}

    # C2 markers
    c2_x_ok = True
    xs = []
    for fx, fy in RED_X:
        ax = int((fx - ORIGIN[0]) * s)
        ay = int((fy - ORIGIN[1]) * s)
        sub = rm[max(0, ay - X_WIN):ay + X_WIN + 1, max(0, ax - X_WIN):ax + X_WIN + 1]
        n = int(sub.sum())
        ok = n >= X_MIN_PX
        c2_x_ok &= ok
        xs.append({"frame": (fx, fy), "asset": (ax, ay), "red_px": n, "ok": ok})
    res["checks"]["C2_xmarkers"] = {"ok": c2_x_ok, "markers": xs}

    # C3 hline
    ly, lx0, lx1 = RED_HLINE
    ax0, ay0, ax1, ay1 = to_asset_box(s, lx0, ly - 2, lx1, ly + 2)
    ax1 = min(ax1, W)
    ay1 = min(ay1, H)
    band = rm[ay0:ay1, ax0:ax1]
    cols = band.any(0) if band.size else np.zeros(0, bool)
    cover = float(cols.mean()) if cols.size else 0.0
    c3_ok = cover > HLINE_COVER_THR
    res["checks"]["C3_hline"] = {"ok": c3_ok, "asset_box": (ax0, ay0, ax1, ay1),
                                  "col_coverage": cover}

    # C4 diff vs baseline
    b = np.asarray(Image.open(BASELINE).convert("RGB")).astype(np.int32)
    note = ""
    if b.shape[:2] != (H, W):
        note = "size mismatch vs baseline %dx%d; candidate resized for diff" % (b.shape[1], b.shape[0])
        a2 = np.asarray(im.resize((b.shape[1], b.shape[0]), Image.LANCZOS)).astype(np.int32)
    else:
        a2 = a
    diff = (np.abs(a2 - b).max(2) > DIFF_DELTA)
    frac = float(diff.mean())
    # annotation regions: label boxes padded, marker windows, hline band
    regions = []
    for lb in labels:
        x0, y0, x1, y1 = lb["asset"]
        pad = int(0.35 * max(x1 - x0, y1 - y0))
        regions.append((max(0, x0 - pad), max(0, y0 - pad),
                        min(b.shape[1], x1 + pad), min(b.shape[0], y1 + pad)))
    for m in xs:
        ax, ay = m["asset"]
        regions.append((max(0, ax - 3 * X_WIN), max(0, ay - 3 * X_WIN),
                        min(b.shape[1], ax + 3 * X_WIN), min(b.shape[0], ay + 3 * X_WIN)))
    hx0, hy0, hx1, hy1 = res["checks"]["C3_hline"]["asset_box"]
    regions.append((hx0, max(0, hy0 - 10), hx1, min(b.shape[0], hy1 + 10)))
    ann = np.zeros(b.shape[:2], bool)
    for x0, y0, x1, y1 in regions:
        ann[y0:y1, x0:x1] = True
    outside = float((diff & ~ann).mean())
    c4_ok = frac < DIFF_THR
    res["checks"]["C4_diff"] = {"ok": c4_ok, "changed_frac": frac,
                                "changed_outside_annotation_frac": outside, "note": note}

    res["verdict"] = "PASS" if all(res["checks"][k]["ok"] for k in
                                    ("C1_ink", "C2_collision", "C2_xmarkers", "C3_hline", "C4_diff", "C5_text_height")) else "FAIL"
    return res


def fmt_res(res):
    L = []
    c = res["checks"]
    L.append("### candidate %s — %s" % (res["tag"] or os.path.basename(os.path.dirname(res["path"])),
                                         os.path.basename(res["path"])))
    L.append("- path: %s" % res["path"])
    L.append("- md5: %s  size: %dx%d  scale s=%.4f  verified: %s" %
             (res["md5"], res["size"][0], res["size"][1], res["scale"], res["time"]))
    L.append("- C1 ink density (>%.3f) per label box:" % INK_DENSITY_THR)
    for lb in c["C1_ink"]["labels"]:
        L.append("  - %-13s frame x%d..%d y%d..%d -> asset x%d..%d y%d..%d  ink=%.4f  %s" %
                 (lb["name"], lb["frame"][0], lb["frame"][1], lb["frame"][2], lb["frame"][3],
                  lb["asset"][0], lb["asset"][2], lb["asset"][1], lb["asset"][3],
                  lb["ink_density"], "OK" if lb["ink_ok"] else "MISSING"))
    L.append("  C1: %s" % ("PASS" if c["C1_ink"]["ok"] else "FAIL"))
    L.append("- C2 red X markers (>=%d red px in +-%d asset px window):" % (X_MIN_PX, X_WIN))
    for m in c["C2_xmarkers"]["markers"]:
        L.append("  - frame (%d,%d) -> asset (%d,%d)  red_px=%d  %s" %
                 (m["frame"][0], m["frame"][1], m["asset"][0], m["asset"][1], m["red_px"],
                  "OK" if m["ok"] else "MISSING"))
    reds = [lb["red_px"] for lb in c["C1_ink"]["labels"]]
    L.append("  C2 markers: %s | C2 collision (red px inside label boxes %s): %s" %
             ("PASS" if c["C2_xmarkers"]["ok"] else "FAIL", reds,
              "PASS" if c["C2_collision"]["ok"] else "FAIL"))
    h = c["C3_hline"]
    L.append("- C3 red hline y418 x124..381 -> asset x%d..%d y%d..%d  col_coverage=%.3f (thr %.2f): %s" %
             (h["asset_box"][0], h["asset_box"][2], h["asset_box"][1], h["asset_box"][3],
              h["col_coverage"], HLINE_COVER_THR, "PASS" if h["ok"] else "FAIL"))
    d = c["C4_diff"]
    L.append("- C4 diff vs baseline %s (%s): changed=%.4f (<%.2f) outside-annotation=%.4f  %s" %
             (BASELINE_MD5[:8], d["note"] or "same size", d["changed_frac"], DIFF_THR,
              d["changed_outside_annotation_frac"], "PASS" if d["ok"] else "FAIL"))
    L.append("- C5 text height (expect ~%.1f asset px = 15 frame px * s):" %
             (EXP_TEXT_FRAME_PX * res["scale"]))
    for lb in c["C1_ink"]["labels"]:
        L.append("  - %-13s measured=%d px  expected=%.1f  %s" %
                 (lb["name"], lb["text_h_px"], lb["text_h_exp_px"],
                  "OK" if lb["text_h_ok"] else "OFF"))
    L.append("  C5: %s" % ("PASS" if c["C5_text_height"]["ok"] else "FAIL"))
    L.append("**VERDICT: %s**" % res["verdict"])
    L.append("")
    return "\n".join(L)


def table_row(res):
    c = res["checks"]
    dens = ",".join("%.3f" % lb["ink_density"] for lb in c["C1_ink"]["labels"])
    ths = ",".join("%d" % lb["text_h_px"] for lb in c["C1_ink"]["labels"])
    xp = ",".join("%d" % m["red_px"] for m in c["C2_xmarkers"]["markers"])
    reds = sum(lb["red_px"] for lb in c["C1_ink"]["labels"])
    return ("| %s | %s | %dx%d | C1 %s (dens %s) | C2 X %s (%s) coll %s (redpx %d) | C3 %.2f %s | C4 %.4f %s | C5 h %s %s | **%s** |"
            % (res["tag"], res["md5"][:8], res["size"][0], res["size"][1],
               "PASS" if c["C1_ink"]["ok"] else "FAIL", dens,
               "PASS" if c["C2_xmarkers"]["ok"] else "FAIL", xp,
               "PASS" if c["C2_collision"]["ok"] else "FAIL", reds,
               c["C3_hline"]["col_coverage"], "PASS" if c["C3_hline"]["ok"] else "FAIL",
               c["C4_diff"]["changed_frac"], "PASS" if c["C4_diff"]["ok"] else "FAIL",
               ths, "PASS" if c["C5_text_height"]["ok"] else "FAIL", res["verdict"]))


HEADER = """# bl_verify_r1 — PIL verification of candidate BL assets, slide 025 (deck 03)

- NS: `videos/machine-learning/03_ridger_regression_gradient_descent`
- Work dir: `recreated_pptx/qa/rejudge_20261027/slide025` (`$W`)
- Baseline (current build): `recreated_pptx/build/assets/plot_025_bl.png` md5 `7a8e7210f118b728245d268552a7d32d` (1220x987)
- Watched candidate dirs: `assets_k17r/`, `assets_k17s/`, `assets_k17t3/` (poll 60 s, up to 90 min)
- Transform (task spec): `s = asset_width / 411`, origin frame (60, 296); `asset = (frame - origin) * s`
- Ground truth (frame px): labels Global Maxima x242..268 y304..319, Local Maxima x286..315 y337..352,
  Local Minima x286..311 y390..399, Global Minima x145..201 y439..465; red X at (199,445),(270,482);
  red hline y418 x124..381; red rect x80..472 y292..527
- Thresholds: C1 ink density > %.3f (dark lum<100) per label box; C2 >=%d red px in +-%d asset px
  window per marker and 0 red px in label boxes; C3 hline red col coverage > %.2f over x124..381 at y418+-2;
  C4 changed-px fraction < %.2f vs baseline; C5 ink row height in [0.5x,1.5x] of %.0f frame px * s
- Red mask: r>110, r-g>50, r-b>50. Diff: |delta|>%d on any channel.

| candidate | md5 | size | C1 ink | C2 markers/collision | C3 hline | C4 diff | C5 text h | VERDICT |
|---|---|---|---|---|---|---|---|---|
""" % (INK_DENSITY_THR, X_MIN_PX, X_WIN, HLINE_COVER_THR, DIFF_THR, EXP_TEXT_FRAME_PX, DIFF_DELTA)


def leg_section():
    if not os.path.exists(LEG):
        return "\n## Original-side transcription (bl_labels_leg.txt)\n\nNot landed yet.\n"
    txt = open(LEG).read()
    if "FINAL VERDICT" not in txt:
        return "\n## Original-side transcription (bl_labels_leg.txt)\n\nFile present but no FINAL VERDICT yet; first 40 lines:\n\n```\n%s\n```\n" % "\n".join(txt.splitlines()[:40])
    return "\n## Original-side transcription (bl_labels_leg.txt — FINAL VERDICT present)\n\n```\n%s\n```\n" % txt.strip()


def write_md(results):
    with open(MD, "w") as f:
        f.write(HEADER)
        for r in results:
            f.write(table_row(r) + "\n")
        f.write("\n## Per-candidate detail\n\n")
        for r in results:
            f.write(fmt_res(r) + "\n")
        f.write(leg_section())
        f.write("\n-- last update: %s --\n" % datetime.now().isoformat(timespec="seconds"))


def watch():
    seen = {}
    results = []
    t0 = time.time()
    deadline = t0 + 90 * 60
    print("watch start %s deadline %s" % (datetime.now().isoformat(), datetime.fromtimestamp(deadline).isoformat()), flush=True)
    while time.time() < deadline:
        for d in WATCH_DIRS:
            p = os.path.join(RJ, d)
            if not os.path.isdir(p):
                continue
            for fn in sorted(os.listdir(p)):
                if not fn.lower().endswith(".png"):
                    continue
                full = os.path.join(p, fn)
                m = md5(full)
                key = (d, fn, m)
                if key in seen:
                    continue
                seen[key] = True
                try:
                    r = verify(full, tag="%s/%s" % (d, fn))
                except Exception as e:
                    r = {"tag": "%s/%s" % (d, fn), "path": full, "md5": m, "size": (0, 0),
                         "scale": 0, "time": datetime.now().isoformat(timespec="seconds"),
                         "checks": {}, "verdict": "ERROR: %s" % e}
                results.append(r)
                write_md(results)
                print("[%s] verified %s -> %s" % (r["time"], key, r["verdict"]), flush=True)
        time.sleep(60)
    print("watch end (90 min elapsed)", flush=True)
    with open(os.path.join(RJ, "bl_verify_r1.done"), "w") as f:
        f.write("watch completed %s\n" % datetime.now().isoformat())


if __name__ == "__main__":
    if sys.argv[1] == "verify":
        r = verify(sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else "")
        print(fmt_res(r))
        write_md([r])
    elif sys.argv[1] == "watch":
        watch()
