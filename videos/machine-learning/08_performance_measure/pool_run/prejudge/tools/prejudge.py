#!/usr/bin/env python3
"""Pre-judge programmatic checks for 08_performance_measure slides 19-37.

Renders the slide's own pptx at 150dpi with a project-scratch LibreOffice
profile, then measures, against the ORIGINAL lecture frame:

  1. INK CONTAINMENT  - content ink inside the house frame
                        (frame x0.15 y0.15 w13.03 h7.2 @ 13.33x7.5in)
  2. TEXT OVERLAP     - overlapping text boxes (geometry) and overlapping
                        rendered text ink (pixels)
  3. CLIP/TRUNCATION  - rendered text ink vs its declared box
  4. REGION ALIGNMENT - coarse ink-map shift + per-color block bboxes
  5. CONTENT DELTA    - original-frame ink the render lacks (missing elements)
  6. BADGE            - numeral vs deck convention + cross-slide glyph IoU
  7. EQ-LINEAR        - linear-math text patterns that must be 2D images

Every finding cites measured numbers. Read-only on all work products.
"""
from __future__ import annotations

import argparse
import json
import math
import os
import re
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image

NS = Path("/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure")
TOOLS = Path(__file__).parent
FRAME = (0.15, 0.15, 13.03, 7.2)          # x, y, w, h  (house frame, inches)
BG = np.array([232, 232, 232])             # #E8E8E8
HOUSE_RED = np.array([192, 0, 0])          # #C00000 frame stroke
BADGE = (12.48, 0.30, 0.50, 0.50)         # x, y, w, h (inches)
PY = "/home/codespace/.pyenv/versions/3.15.2/bin/python3"

# ---------------------------------------------------------------- helpers

def inches_to_px(v, dpi):
    return v * dpi


def hex_to_rgb(h):
    h = h.lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    return np.array([int(h[i:i + 2], 16) for i in (0, 2, 4)])


def color_dist(c1, c2):
    return float(np.sqrt(((c1 - c2) ** 2).sum()))


def ink_mask(img, bg=BG, tol=40):
    a = np.asarray(img.convert("RGB")).astype(int)
    return np.abs(a - bg).sum(axis=2) > tol


def mask_near(img, color, tol=70):
    a = np.asarray(img.convert("RGB")).astype(int)
    return np.abs(a - color).max(axis=2) <= tol


def bbox(mask):
    ys, xs = np.where(mask)
    if len(xs) == 0:
        return None
    return int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())


def in2(px, dpi):
    return round(px / dpi, 3)


def rect_inter(a, b):
    """Intersection area (in^2) of two rects (x, y, w, h)."""
    ax, ay, aw, ah = a
    bx, by, bw, bh = b
    ix = max(0.0, min(ax + aw, bx + bw) - max(ax, bx))
    iy = max(0.0, min(ay + ah, by + bh) - max(ay, by))
    return ix * iy


# ---------------------------------------------------------------- geometry

def load_geometry(slide, scratch):
    build = NS / f"recreated_pptx/build/slide_{slide:03d}.js"
    out = Path(scratch) / f"geom_{slide}.json"
    subprocess.run(["node", str(TOOLS / "extract_geom.js"), str(build), str(out)],
                   check=True, cwd=str(NS))
    data = json.loads(out.read_text())
    return build, data


def norm_elements(geom):
    """Return flat list of {kind, text, rect(x,y,w,h), opts, index} for slide 0.

    Order is preserved (z-order): later elements are drawn on top.
    """
    out = []
    idx = 0
    for sl in geom.get("slides", []):
        for el in sl.get("elements", []):
            args = el.get("args", [])
            opts = {}
            if args and isinstance(args[-1], dict):
                opts = args[-1]
            kind = el["type"]
            text = None
            if args and isinstance(args[0], str):
                text = args[0]
            elif args and isinstance(args[0], list):
                text = "".join(str(r.get("text", "")) if isinstance(r, dict) else str(r)
                                for r in args[0])
            rect = None
            if "x" in opts and "y" in opts:
                rect = (opts.get("x"), opts.get("y"),
                        opts.get("w", 0.0), opts.get("h", 0.0))
            out.append({
                "kind": kind, "text": text, "rect": rect, "opts": opts,
                "fill": opts.get("fill", {}).get("color") if isinstance(opts.get("fill"), dict) else None,
                "index": idx,
            })
            idx += 1
    return out


# ---------------------------------------------------------------- patterns
LINEAR_MATH = [
    (r"\\[d]?frac|frac\s*\(", "explicit frac()"),
    (r"\bsum\s+from\b|\bfrom\s+i\s*=\s*1\b", "'sum from i=1' linear form"),
    (r"\b∫|∑\b", "inline sigma/integral glyph"),
    (r"\bsqrt\s*\(", "sqrt()"),
    (r"\)\s*/\s*\(", "linear fraction ')/( ' "),
    (r"\b[TPFN]{2,4}\s*/", "ratio as slash text e.g. TP/"),
    (r"\bp\s*=\s*[^.].*/.*\)", "probability written inline with /"),
    (r"\b[A-Za-z]\s*_\s*[0-9a-z]", "underscore subscript text"),
    (r"\b[A-Za-z]\s*\^\s*[0-9a-z]", "caret superscript text"),
    (r"\bsigma\b|\bmu\b|\balpha\b|\bbeta\b", "greek name spelled inline"),
]


def scan_linear_math(elements):
    hits = []
    for e in elements:
        t = e.get("text")
        if not t:
            continue
        for pat, label in LINEAR_MATH:
            m = re.search(pat, t, re.IGNORECASE)
            if m:
                hits.append({"text": t[:90], "pattern": label,
                             "match": m.group(0), "rect": e.get("rect")})
                break
    return hits


# ---------------------------------------------------------------- render parse

def parse_pptx_text(pptx):
    """Text nodes + image count from the pptx XML (single slide decks)."""
    import zipfile
    texts, pics, n_slides = [], 0, 0
    try:
        with zipfile.ZipFile(pptx) as z:
            names = z.namelist()
            n_slides = sum(1 for n in names if re.match(r"ppt/slides/slide\d+\.xml$", n))
            for n in names:
                if re.match(r"ppt/slides/slide\d+\.xml$", n):
                    xml = z.read(n).decode("utf8", "replace")
                    texts += re.findall(r"<a:t>(.*?)</a:t>", xml, re.S)
                    pics += xml.count("<p:pic")
    except Exception as e:
        return {"error": str(e)}
    return {"texts": texts, "pics": pics, "slides": n_slides}


# ---------------------------------------------------------------- main analysis

def analyse(slide: int, geom_data, render_path, orig_path, pptx_path):
    findings = []
    facts = {}

    def add(sev, tag, region, numbers, fix):
        findings.append({"severity": sev, "tag": tag, "region": region,
                         "measured": numbers, "fix": fix})

    # ---- render / original -------------------------------------------------
    rimg = Image.open(render_path).convert("RGB")
    oimg = Image.open(orig_path).convert("RGB")
    dpi = rimg.width / 13.33
    odpi = oimg.width / 13.33
    facts["render_px"] = [rimg.width, rimg.height]
    facts["render_dpi"] = round(dpi, 3)
    facts["orig_px"] = [oimg.width, oimg.height]

    elements = norm_elements(geom_data)

    # ---- 0. who renders text vs images -------------------------------------
    texts = [e for e in elements if e["kind"] == "addText"]
    images = [e for e in elements if e["kind"] in ("addImage", "addPicture", "addChart")]

    # ---- 1. geometry: outside the house frame -------------------------------
    for e in elements:
        r = e.get("rect")
        if not r or not r[2] or not r[3]:
            continue
        over_r = r[0] + r[2] - (FRAME[0] + FRAME[2])
        over_b = r[1] + r[3] - (FRAME[1] + FRAME[3])
        over = max(FRAME[0] - r[0], FRAME[1] - r[1], over_r, over_b)
        if over > 0.05:
            add("MAJOR", "GEOM-OUT-OF-FRAME",
                (e["text"] or e["kind"])[:60],
                f"declared rect {r} overhangs the house frame by {over:.3f}in "
                "(frame 0.15,0.15 -> 13.18,7.35)",
                "reposition/shrink so the element sits inside the frame")
        elif over > 0.0:
            add("MINOR", "GEOM-FRAME-TIGHT",
                (e["text"] or e["kind"])[:60],
                f"declared rect {r} overhangs the house frame by {over:.3f}in "
                "(ink may still be inside; pixel check is authoritative)",
                "trim the box flush inside the frame")

    # ---- 2b. z-order occlusion: an later opaque filled element covering an
    #          earlier one (e.g. a title bar swallowing the badge oval)
    opaque = [e for e in elements if e.get("fill") and e["kind"] == "addShape"]
    badge_el = None
    for e in elements:
        r = e.get("rect")
        if (e["kind"] == "addShape" and r
                and abs(r[0] - BADGE[0]) < 0.02 and abs(r[1] - BADGE[1]) < 0.02):
            badge_el = e
    if badge_el is not None:
        br = badge_el["rect"]
        for s in elements:
            if s["index"] <= badge_el["index"] or not s.get("fill"):
                continue
            sr = s.get("rect")
            if not sr:
                continue
            cov = rect_inter(br, sr) / (br[2] * br[3])
            if cov > 0.02:
                add("MAJOR", "BADGE-OCCLUDED", "slide-number badge oval",
                    f"later filled element (#{s['fill']} at {sr}) covers {cov*100:.0f}% of "
                    f"the badge oval {br} (drawn earlier)",
                    "draw the badge after the title bar, or shorten the title bar so it "
                    "stops left of x=12.48in")

    for i, e in enumerate(elements):
        if e["kind"] not in ("addShape", "addImage") or not e.get("fill"):
            continue
        r = e.get("rect")
        if not r or not r[2] or not r[3]:
            continue
        for s in elements:
            if s["index"] <= e["index"] or s["kind"] != "addShape" or not s.get("fill"):
                continue
            sr = s.get("rect")
            if not sr or not sr[2] or not sr[3]:
                continue
            cov = rect_inter(r, sr) / (r[2] * r[3])
            if cov > 0.25:
                add("MAJOR", "OCCLUSION",
                    f"element #{e['index']} ({e['kind']} #{e.get('fill')}) at {r}",
                    f"a later filled shape (#{s['fill']} at {sr}) covers {cov*100:.0f}% of it",
                    "reorder the draws or shrink the covering shape")

    # ---- 2. text-text box overlap -------------------------------------------
    for i in range(len(texts)):
        for j in range(i + 1, len(texts)):
            a, b = texts[i], texts[j]
            if not a["rect"] or not b["rect"]:
                continue
            area = rect_inter(a["rect"], b["rect"])
            if area > 0.002:
                add("BLOCKER" if area > 0.02 else "MAJOR", "TEXT-OVERLAP",
                    f"'{a['text'][:28]}' x '{b['text'][:28]}'",
                    f"boxes {a['rect']} and {b['rect']} overlap by {area:.4f} in^2",
                    "move/resize one box; boxes must not intersect")

    # ---- 3. contrast: text colour vs the fill it actually sits on -----------
    # z-order aware: the fill is the LAST shape drawn BEFORE the text that
    # contains the text's box.
    for t in texts:
        if not t["rect"] or not t.get("text"):
            continue
        tcol = t["opts"].get("color")
        if not tcol:
            continue
        tc = hex_to_rgb(tcol)
        under = None
        for s in elements:
            if s["kind"] not in ("addShape", "addTable"):
                continue
            if s["index"] >= t["index"]:
                continue
            sf = s.get("fill")
            sr = s.get("rect")
            if not sf or not sr:
                continue
            inside = (t["rect"][0] >= sr[0] - 0.02 and t["rect"][1] >= sr[1] - 0.02
                      and t["rect"][0] + t["rect"][2] <= sr[0] + sr[2] + 0.02
                      and t["rect"][1] + t["rect"][3] <= sr[1] + sr[3] + 0.02)
            if inside:
                under = s
        if under is None:
            continue
        d = color_dist(tc, hex_to_rgb(under["fill"]))
        if d < 110:
            add("MAJOR", "CONTRAST",
                f"text '{t['text'][:34]}'",
                f"text #{tcol} on the shape actually beneath it "
                f"(#{under['fill']}, rect {under['rect']}) - RGB distance {d:.0f} < 110",
                "darken the text or lighten the fill")

    # ---- 4. EQ-LINEAR scan ----------------------------------------------------
    for h in scan_linear_math(elements):
        add("BLOCKER", "EQ-LINEAR", h["text"][:60],
            f"text pattern '{h['match']}' ({h['pattern']}) in box {h['rect']}",
            "render this equation as a mathtext 2D PNG image (scripts/render_eq.py)")

    # ---- 5. render-side ink measurements -------------------------------------
    ink = ink_mask(rimg)
    not_red = ~mask_near(rimg, HOUSE_RED, 70)
    content_ink = ink & not_red

    # frame containment: ink outside the house frame rect
    fx, fy, fw, fh = FRAME
    X0, Y0, X1, Y1 = (round(fx * dpi), round(fy * dpi),
                      round((fx + fw) * dpi), round((fy + fh) * dpi))
    pad = 5
    outside = content_ink.copy()
    outside[Y0 - pad:Y1 + pad, X0 - pad:X1 + pad] = False
    n_out = int(outside.sum())
    facts["ink_outside_frame_px"] = n_out
    if n_out:
        bx = bbox(outside)
        rows = np.where(outside.any(axis=1))[0]
        cols = np.where(outside.any(axis=0))[0]
        add("MAJOR", "INK-OUTSIDE-FRAME",
            "content ink beyond house frame",
            f"{n_out} px outside (x{in2(cols.min(), dpi)}-{in2(cols.max(), dpi)}in, "
            f"y{in2(rows.min(), dpi)}-{in2(rows.max(), dpi)}in); house frame ends at "
            f"x{X1/dpi:.2f}in y{Y1/dpi:.2f}in",
            "move the offending element inside the frame (or shrink it)")

    # ---- 6. per-text rendered ink vs declared box ----------------------------
    rendered_texts = []
    for e in texts:
        r = e.get("rect")
        t = e.get("text")
        if not r or not t:
            continue
        col = e["opts"].get("color")
        if not col:
            continue
        tc = hex_to_rgb(col)
        bx0 = max(0, int(round(r[0] * dpi)) - 6)
        by0 = max(0, int(round(r[1] * dpi)) - 4)
        bx1 = min(rimg.width, int(round((r[0] + r[2]) * dpi)) + 6)
        by1 = min(rimg.height, int(round((r[1] + r[3]) * dpi)) + 10)
        if bx1 <= bx0 or by1 <= by0:
            continue
        sub = np.asarray(rimg).astype(int)[by0:by1, bx0:bx1]
        m = (np.abs(sub - tc).max(axis=2) <= 70)
        m = Image.fromarray((m * 255).astype(np.uint8))
        m = np.asarray(m) > 0
        if m.sum() < 6:
            add("MAJOR", "TEXT-MISSING", f"'{t[:40]}'",
                f"0 ink pixels of colour #{col} in declared box {r} at render",
                "check the element renders (colour/size/position)")
            continue
        bb = bbox(m)
        gx0, gy0, gx1, gy1 = (bb[0] + bx0, bb[1] + by0, bb[2] + bx0, bb[3] + by0)
        rendered_texts.append({"element": e, "ink_px": (gx0, gy0, gx1, gy1), "mask_n": int(m.sum())})
        rx0, ry0, rx1, ry1 = r[0] * dpi, r[1] * dpi, (r[0] + r[2]) * dpi, (r[1] + r[3]) * dpi
        spill_l, spill_t = rx0 - gx0, ry0 - gy0
        spill_r, spill_b = gx1 - rx1, gy1 - ry1
        if max(spill_l, spill_t, spill_r, spill_b) > 3:
            side = max([("left", spill_l), ("top", spill_t),
                        ("right", spill_r), ("bottom", spill_b)], key=lambda kv: kv[1])
            add("MAJOR", "TEXT-SPILL", f"'{t[:40]}'",
                f"ink bbox ({in2(gx0, dpi)},{in2(gy0, dpi)})-({in2(gx1, dpi)},{in2(gy1, dpi)})in "
                f"exceeds declared box {r} by {side[1]/dpi:.3f}in on the {side[0]}",
                "widen/heighten the box or shorten the text")
        elif (gx1 - gx0) > (rx1 - rx0) * 0.97 or (gy1 - gy0) > (ry1 - ry0) * 0.97:
            add("MINOR", "TEXT-TIGHT", f"'{t[:40]}'",
                f"ink fills >97% of box {r} (ink {in2(gx1-gx0, dpi)}x{in2(gy1-gy0, dpi)}in)",
                "give the text box a little slack to avoid clipping")

    # rendered text-ink collisions across DIFFERENT text elements
    for i in range(len(rendered_texts)):
        for j in range(i + 1, len(rendered_texts)):
            a, b = rendered_texts[i], rendered_texts[j]
            ax, ay, aw, ah = a["ink_px"]
            bx, by, bw, bh = b["ink_px"]
            ix = max(0, min(ax + aw, bx + bw) - max(ax, bx))
            iy = max(0, min(ay + ah, by + bh) - max(ay, by))
            if ix * iy > 30:
                add("BLOCKER", "TEXT-INK-COLLIDE",
                    f"'{a['element']['text'][:24]}' x '{b['element']['text'][:24]}'",
                    f"rendered ink boxes overlap {int(ix*iy)} px^2 at 150dpi "
                    f"({in2(ix, dpi)}x{in2(iy, dpi)}in)",
                    "resolve the collision - the two texts touch on the render")

    # ---- 7. badge -------------------------------------------------------------
    badge_num = None
    for e in texts:
        r = e.get("rect")
        if not r:
            continue
        if abs(r[0] - BADGE[0]) < 0.02 and abs(r[1] - BADGE[1]) < 0.02:
            badge_num = e.get("text")
    bx0 = int(BADGE[0] * dpi) - 6; by0 = int(BADGE[1] * dpi) - 6
    bx1 = int((BADGE[0] + BADGE[2]) * dpi) + 6; by1 = int((BADGE[1] + BADGE[3]) * dpi) + 6
    sub = np.asarray(rimg).astype(int)[by0:by1, bx0:bx1]
    dark = np.abs(sub - hex_to_rgb("333333")).max(axis=2) <= 90
    n_badge = int(dark.sum())
    badge_mask = dark.copy()
    facts["badge_num_declared"] = badge_num
    facts["badge_ink_px"] = n_badge
    if badge_num is None:
        add("MAJOR", "BADGE", "slide-number badge",
            "no addText found in the badge oval region (12.48,0.30,0.5,0.5)",
            "add the badge numeral text box on the oval")
    elif badge_num.strip() != str(slide):
        add("MAJOR", "BADGE", "slide-number badge",
            f"badge text renders '{badge_num.strip()}' but this slide is {slide}",
            f"set the badge numeral to {slide}")
    if n_badge < 20:
        add("MAJOR", "BADGE", "slide-number badge",
            f"only {n_badge} dark ink px inside the badge box "
            f"({BADGE[0]},{BADGE[1]},{BADGE[2]},{BADGE[3]})in",
            "check numeral size/colour renders inside the oval")

    # ---- 8. region alignment vs the original ----------------------------------
    oink = orig_ink_mask(oimg)
    # strip the render's house chrome so the maps are comparable
    rink = content_ink.copy()
    rink[Y0 - 8:Y1 + 8, X0 - 8:X1 + 8] = False     # frame stroke band
    rink[int(BADGE[1] * dpi) - 4:int((BADGE[1] + BADGE[3]) * dpi) + 4,
         int(BADGE[0] * dpi) - 4:int((BADGE[0] + BADGE[2]) * dpi) + 4] = False

    # coarse maps
    GC = 160
    def coarse(mask, w, h):
        W, H = mask.shape[1], mask.shape[0]
        cw, ch = max(1, W // GC), max(1, H // (GC // 2))
        rows = []
        for y in range(0, H - ch + 1, ch):
            row = [mask[y:y + ch, x:x + cw].mean() for x in range(0, W - cw + 1, cw)]
            rows.append(row)
        return np.array(rows)

    cr, co = coarse(rink, *rink.shape), coarse(oink, *oink.shape)
    # pad to same shape
    H = max(cr.shape[0], co.shape[0]); W = max(cr.shape[1], co.shape[1])
    crp = np.zeros((H, W)); crp[:cr.shape[0], :cr.shape[1]] = cr
    cop = np.zeros((H, W)); cop[:co.shape[0], :co.shape[1]] = co
    R = 8
    best, best_shift = -1, (0, 0)
    for dy in range(-R, R + 1):
        for dx in range(-R, R + 1):
            shifted = np.roll(np.roll(cop, dy, axis=0), dx, axis=1)
            score = (crp * shifted).sum() / (np.sqrt((crp ** 2).sum() * (shifted ** 2).sum()) + 1e-9)
            if score > best:
                best, best_shift = score, (dx, dy)
    shift_in = (best_shift[0] * (13.33 / crp.shape[1]), best_shift[1] * (7.5 / crp.shape[0]))
    facts["region_align_score"] = round(float(best), 3)
    facts["region_align_shift_in"] = [round(shift_in[0], 2), round(shift_in[1], 2)]
    if abs(shift_in[0]) > 0.4 or abs(shift_in[1]) > 0.4:
        add("MAJOR", "REGION-ALIGN", "global layout shift",
            f"best coarse-map correlation {best:.3f} at shift "
            f"({shift_in[0]:+.2f},{shift_in[1]:+.2f})in vs original",
            "shift content regions to match the original layout")

    # content delta: cells inked in the original but blank in the render
    o_hot = cop > 0.30
    r_cold = crp < 0.06
    delta = o_hot & r_cold
    facts["orig_only_cells"] = int(delta.sum())
    if delta.mean() > 0.004:
        from scipy import ndimage
        lab, n = ndimage.label(delta)
        sizes = ndimage.sum(delta, lab, range(1, n + 1))
        order = np.argsort(sizes)[::-1]
        for k in order[:4]:
            if sizes[k] <= 0:
                continue
            blob = lab == (k + 1)
            ys, xs = np.where(blob)
            bx = (xs.min() / W * 13.33, ys.min() / H * 7.5,
                  (xs.max() + 1) / W * 13.33, (ys.max() + 1) / H * 7.5)
            add("BLOCKER", "CONTENT-DELTA", "region present in original, blank in render",
                f"ink-block at inches ({bx[0]:.2f},{bx[1]:.2f})-({bx[2]:.2f},{bx[3]:.2f}) "
                f"({int(sizes[k])} coarse cells, >30% ink in original, <6% in render)",
                "an element of the original is missing from the recreation")

    # ---- 9. distinctive colour block alignment -------------------------------
    colors = {
        "blue": (0, 0, 128), "bright_blue": (0, 0, 255), "green": (0, 128, 0),
        "red": (255, 0, 0), "orange": (255, 165, 0), "purple": (128, 0, 128),
        "pink": (255, 153, 153), "yellow": (255, 249, 196),
    }
    for name, c in colors.items():
        cc = np.array(c)
        rm = mask_near(rimg, cc, 60)
        rm[Y0 - 8:Y1 + 8, X0 - 8:X1 + 8] = False
        om = mask_near(oimg, cc, 60)
        rb, ob = bbox(rm), bbox(om)
        if rb and ob and rm.sum() > 200 and om.sum() > 200:
            rx = ((rb[0] + rb[2]) / 2 / dpi, (rb[1] + rb[3]) / 2 / dpi)
            ox = ((ob[0] + ob[2]) / 2 / odpi, (ob[1] + ob[3]) / 2 / odpi)
            dr, drc = rx[0] - ox[0], rx[1] - ox[1]
            facts[f"block_{name}_render_in"] = [round(v, 2) for v in rx]
            facts[f"block_{name}_orig_in"] = [round(v, 2) for v in ox]
            if abs(dr) > 0.35 or abs(drc) > 0.35:
                add("MAJOR", "BLOCK-ALIGN", f"{name} block",
                    f"centroid render ({rx[0]:.2f},{rx[1]:.2f})in vs original "
                    f"({ox[0]:.2f},{ox[1]:.2f})in -> offset ({dr:+.2f},{drc:+.2f})in",
                    "align the block to the original's position")

    # ---- 10. image bounds + image overlap --------------------------------------
    for i in range(len(images)):
        for j in range(i + 1, len(images)):
            a, b = images[i], images[j]
            if not a["rect"] or not b["rect"]:
                continue
            area = rect_inter(a["rect"], b["rect"])
            if area > 0.01:
                add("MINOR", "IMAGE-OVERLAP", "images",
                    f"image rects {a['rect']} / {b['rect']} overlap {area:.3f} in^2",
                    "space the images apart")

    return findings, facts, elements, texts, images


def orig_ink_mask(oimg):
    """Original lecture frames: estimate the page background from border pixels."""
    a = np.asarray(oimg.convert("RGB")).astype(int)
    border = np.concatenate([a[:4].reshape(-1, 3), a[-4:].reshape(-1, 3),
                             a[:, :4].reshape(-1, 3), a[:, -4:].reshape(-1, 3)])
    bg = np.median(border, axis=0)
    return np.abs(a - bg).sum(axis=2) > 150


def orig_badge_zone(oimg):
    """Ink in the top-right corner where the house badge sits (original's own number)."""
    a = np.asarray(oimg.convert("RGB")).astype(int)
    x0, y0 = int(12.48 / 13.33 * oimg.width), int(0.30 / 7.5 * oimg.height)
    x1, y1 = int(12.98 / 13.33 * oimg.width), int(0.80 / 7.5 * oimg.height)
    sub = a[y0:y1, x0:x1]
    bg = np.median(sub.reshape(-1, 3), axis=0)
    ink = np.abs(sub - bg).sum(axis=2) > 150
    return int(ink.sum()), ink


# ---------------------------------------------------------------- CLI

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("slide", type=int)
    ap.add_argument("--geom", default=None)
    ap.add_argument("--render", default=None)
    args = ap.parse_args()
    slide = args.slide

    sdir = NS / f"pool_run/prejudge/slide{slide:03d}"
    sdir.mkdir(parents=True, exist_ok=True)

    build, geom = load_geometry(slide, NS / "pool_run/prejudge/scratch") if not args.geom \
        else (None, json.loads(Path(args.geom).read_text()))
    pptx = NS / f"recreated_pptx/slide_{slide:03d}_recreated.pptx"
    orig = NS / f"unique_slides/slide_{slide:03d}.jpg"
    if not orig.exists():
        orig = NS / "unique_slides/slide_028-.jpg"
    render = args.render or str(sdir / "render.png")
    if not args.render:
        subprocess.run(["bash", str(TOOLS / "render_slide.sh"), str(pptx),
                        str(sdir), "render"], check=True)

    findings, facts, elements, texts, images = analyse(slide, geom, render, orig, pptx)

    nb, bmask = orig_badge_zone(Image.open(orig))
    facts["orig_badge_zone_ink_px"] = nb

    out = {"slide": slide, "findings": findings, "facts": facts,
           "n_text_elements": len(texts), "n_image_elements": len(images),
           "pptx_md5": md5(pptx)}
    print(json.dumps(out, indent=2, default=str))


def md5(p):
    import hashlib
    return hashlib.md5(Path(p).read_bytes()).hexdigest()


if __name__ == "__main__":
    main()
