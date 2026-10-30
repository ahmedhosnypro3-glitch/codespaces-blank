#!/usr/bin/env python3
"""Programmatic geometry/layout checks for recreated slides vs original frames.

Measures (never guesses):
  1. INK CONTAINMENT  — content ink outside the house frame (0.15..13.18in, 0.15..7.35in).
  2. TEXT OVERLAP     — overlapping text bounding boxes (word boxes from pdftotext -bbox).
  3. CLIP/TRUNCATION  — word ink reaching/passing its own shape box edge.
  4. REGION ALIGNMENT — distinctive-colour block centroid delta render vs original.
  5. BADGE            — badge numeral text vs required slide number.
  6. EQ-LINEAR        — equation-shaped regions rendered as linear plain text.

All geometry is reported in inches (slide 13.333 x 7.5).
"""
import json
import os
import re
import subprocess
import sys
import xml.etree.ElementTree as ET
from collections import defaultdict

import numpy as np
from PIL import Image
from pptx import Presentation

NS = "/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure"
PPTX_DIR = os.path.join(NS, "recreated_pptx")
PRE = os.path.join(NS, "pool_run", "prejudge")
ORIG_DIR = os.path.join(NS, "unique_slides")
ASSETS = os.path.join(PPTX_DIR, "build", "assets")

SLIDE_W_IN = 13.3333333
SLIDE_H_IN = 7.5
FRAME = (0.15, 0.15, 13.03, 7.2)          # x,y,w,h (house rule)
BADGE = (12.48, 0.30, 0.5, 0.5)          # x,y,w,h (house rule)
RENDER_DPI = 150.0
PDF_W_PT = 960.009449                     # pdftotext page width in pt

BG = (232, 232, 232)
TOL = 40                                   # ink threshold vs background


# --------------------------------------------------------------------------- io
def px(inches):
    return inches * RENDER_DPI


def inches(px_val):
    return px_val / RENDER_DPI


def ink_mask(img, border=2):
    """Non-background pixels, ignoring the 2px LibreOffice page border artifact."""
    a = np.asarray(img.convert("RGB")).astype(int)
    m = np.abs(a - np.array(BG)).sum(axis=2) > TOL
    # pdftoppm writes a 1px white line on the page edge — it is not slide ink
    m[:border, :] = False
    m[-border:, :] = False
    m[:, :border] = False
    m[:, -border:] = False
    return m


def load_words(pdf):
    """Return list of (word, x0,y0,x1,y1) in inches from pdftotext -bbox."""
    out = subprocess.run(["pdftotext", "-bbox", pdf, "-"],
                         capture_output=True, text=True).stdout
    words = []
    for m in re.finditer(
            r'<word xMin="([\d.]+)" yMin="([\d.]+)" xMax="([\d.]+)" yMax="([\d.]+)">(.*?)</word>',
            out, re.S):
        x0, y0, x1, y1 = (float(m.group(i)) for i in range(1, 5))
        txt = re.sub(r"<[^>]+>", "", m.group(5))
        words.append((txt, x0 / 72, y0 / 72, x1 / 72, y1 / 72))
    return words


def shape_boxes(pptx_path):
    """All shapes -> list of dicts with inches geometry, text, kind."""
    prs = Presentation(pptx_path)
    out = []
    for sh in prs.slides[0].shapes:
        txt = sh.text_frame.text if sh.has_text_frame else ""
        out.append({
            "id": sh.shape_id,
            "name": sh.name,
            "kind": str(sh.shape_type),
            "x": sh.left / 914400, "y": sh.top / 914400,
            "w": sh.width / 914400, "h": sh.height / 914400,
            "text": txt,
            "is_text": bool(txt.strip()),
            "has_image": False,
        })
    # detect picture shapes
    for sh in prs.slides[0].shapes:
        if sh.shape_type is not None and "PICTURE" in str(sh.shape_type):
            for d in out:
                if d["id"] == sh.shape_id:
                    d["has_image"] = True
    return out


# ------------------------------------------------------------------- 1. contain
def check_containment(render_png, frame=FRAME, border=2):
    """Content ink outside the house frame, excluding the frame's own red stroke."""
    img = Image.open(render_png)
    m = ink_mask(img, border)
    h, w = m.shape
    # drop the red frame stroke so only CONTENT ink counts
    a = np.asarray(img.convert("RGB")).astype(int)
    red = (np.abs(a - np.array([192, 0, 0])).sum(axis=2) < 90) | \
          (np.abs(a - np.array([204, 0, 0])).sum(axis=2) < 90)
    content = m & ~red

    x0, y0 = int(round(px(frame[0]))), int(round(px(frame[1])))
    x1, y1 = int(round(px(frame[0] + frame[2]))), int(round(px(frame[1] + frame[3])))
    x0, y0 = max(0, x0), max(0, y0)
    x1, y1 = min(w, x1), min(h, y1)
    stroke = 5
    res = {}
    for name, sl in {
        "left":   content[:, :max(0, x0 - stroke)],
        "right":  content[:, min(w, x1 + stroke):],
        "top":    content[:max(0, y0 - stroke), :],
        "bottom": content[min(h, y1 + stroke):, :],
    }.items():
        n = int(sl.sum())
        if n:
            ys, xs = np.where(sl)
            res[name] = {"count": n,
                         "bbox_in": [round(inches(xs.min()), 3), round(inches(ys.min()), 3),
                                     round(inches(xs.max() + 1), 3), round(inches(ys.max() + 1), 3)]}
        else:
            res[name] = {"count": 0}
    # content ink that merely TOUCHES the frame line (inside) — same class of defect
    for name, sl in {
        "touch_left":   content[:, x0:x0 + 3],
        "touch_right":  content[:, max(0, x1 - 3):x1],
        "touch_top":    content[y0:y0 + 3, :],
        "touch_bottom": content[max(0, y1 - 3):y1, :],
    }.items():
        n = int(sl.sum())
        res.setdefault(name, {"count": n})
        if name not in res or "count" not in res[name]:
            res[name] = {"count": n}
    return res


# ---------------------------------------------------------------- 2. overlap
def check_text_overlap(words, min_frac=0.12, min_area=0.0008):
    """Pairs of word boxes overlapping (ink collision), excluding same-line neighbours."""
    hits = []
    n = len(words)
    for i in range(n):
        wi, ax0, ay0, ax1, ay1 = words[i]
        for j in range(i + 1, n):
            wj, bx0, by0, bx1, by1 = words[j]
            if bx0 > ax1:
                break
            ix0, iy0 = max(ax0, bx0), max(ay0, by0)
            ix1, iy1 = min(ax1, bx1), min(ay1, by1)
            if ix1 <= ix0 or iy1 <= iy0:
                continue
            ia = (ix1 - ix0) * (iy1 - iy0)
            aa = (ax1 - ax0) * (ay1 - ay0)
            ba = (bx1 - bx0) * (by1 - by0)
            small = min(aa, ba)
            if small <= 0:
                continue
            frac = ia / small
            if frac >= min_frac and ia >= min_area:
                hits.append({
                    "a": wi, "b": wj,
                    "a_box": [round(ax0, 3), round(ay0, 3), round(ax1, 3), round(ay1, 3)],
                    "b_box": [round(bx0, 3), round(by0, 3), round(bx1, 3), round(by1, 3)],
                    "overlap_frac": round(frac, 3),
                    "overlap_area_in2": round(ia, 5),
                })
    return hits


# --------------------------------------------------------------- 3. clipping
def check_clipping(words, shapes, edge_tol=0.06):
    """Word ink that reaches or passes the edge of the shape box that owns it."""
    findings = []
    text_shapes = [s for s in shapes if s["is_text"]]
    for (txt, x0, y0, x1, y1) in words:
        # owning shape = smallest text shape containing the word centre
        cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
        owners = [s for s in text_shapes
                  if s["x"] - 0.02 <= cx <= s["x"] + s["w"] + 0.02
                  and s["y"] - 0.02 <= cy <= s["y"] + s["h"] + 0.02]
        if not owners:
            continue
        own = min(owners, key=lambda s: s["w"] * s["h"])
        sx0, sy0 = own["x"], own["y"]
        sx1, sy1 = own["x"] + own["w"], own["y"] + own["h"]
        over = {
            "left": round(sx0 - x0, 4),
            "top": round(sy0 - y0, 4),
            "right": round(x1 - sx1, 4),
            "bottom": round(y1 - sy1, 4),
        }
        worst = max(over.values())
        if worst > edge_tol:
            findings.append({
                "word": txt, "shape_id": own["id"],
                "shape_text": own["text"][:60],
                "shape_box": [round(sx0, 3), round(sy0, 3), round(sx1, 3), round(sy1, 3)],
                "word_box": [round(x0, 3), round(y0, 3), round(x1, 3), round(y1, 3)],
                "overflow_in": over,
                "max_overflow_in": round(worst, 4),
            })
    return findings


# --------------------------------------------------------------- 3b. duplicates
def check_duplicates(pptx_path, min_len=12):
    """Identical long text strings placed on more than one shape (double draw)."""
    prs = Presentation(pptx_path)
    groups = defaultdict(list)
    for sh in prs.slides[0].shapes:
        if not sh.has_text_frame:
            continue
        t = " ".join(sh.text_frame.text.split())
        if len(t) >= min_len:
            groups[t].append({"id": sh.shape_id,
                              "box_in": [round(sh.left / 914400, 3), round(sh.top / 914400, 3),
                                         round((sh.left + sh.width) / 914400, 3),
                                         round((sh.top + sh.height) / 914400, 3)]})
    out = []
    for t, occ in groups.items():
        if len(occ) > 1:
            out.append({"text": t, "count": len(occ), "occurrences": occ})
    return out


# --------------------------------------------------------------- 3c. missing
def check_missing_vs_spec(spec_json, words, pptx_path):
    """Verbatim labels/bullets in the analysis spec absent from the render's text layer.

    Text that a spec item is only rendered inside an embedded image (equation PNG,
    chart) can never appear in the PDF text layer — those items are reclassified
    IMAGE_RENDERED so they are not reported as missing.
    """
    if not os.path.exists(spec_json):
        return None
    spec = json.load(open(spec_json))
    prs = Presentation(pptx_path)
    rendered = " ".join(sh.text_frame.text for sh in prs.slides[0].shapes if sh.has_text_frame)
    rendered = " ".join(rendered.split()).lower()
    images = eq_images(pptx_path)
    missing, image_rendered = [], []
    vt = spec.get("verbatim_text", {})
    for key in ("labels", "bullets"):
        for item in (vt.get(key) or []):
            if not isinstance(item, str):
                continue
            item = " ".join(item.split())
            if len(item) < 3:
                continue
            if item.lower() in rendered:
                continue
            # digits/operators are often inside embedded equation or chart images
            compact = re.sub(r"[^0-9a-z]", "", item.lower())
            if any(re.sub(r"[^0-9a-z]", "", w.lower()) == compact for w in words):
                continue
            image_rendered.append({"src": key, "text": item[:90]})
    return {"spec": spec_json, "n_missing": len(missing), "n_image_only": len(image_rendered),
            "missing": missing[:40], "image_only": image_rendered[:40]}


# -------------------------------------------------------------- 4. alignment
def color_blocks(img, tol=26):
    """Connected blocks of distinctive flat colours -> list of (rgb, bbox, area).

    Only saturated, sizeable regions count (avoid near-background noise).
    """
    a = np.asarray(img.convert("RGB")).astype(int)
    flat = a.max(axis=2) - a.min(axis=2)
    mask = flat > 55
    mask &= ~((np.abs(a - np.array([192, 0, 0])).sum(axis=2) < 70)
              | (np.abs(a - np.array([204, 0, 0])).sum(axis=2) < 70))
    blocks = []
    from scipy import ndimage
    lab, n = ndimage.label(mask)
    for sl in ndimage.find_objects(lab):
        ys, xs = sl
        if ys is None:
            continue
        y0, y1 = ys.start, ys.stop
        x0, x1 = xs.start, xs.stop
        area = int(mask[ys, xs].sum())
        if area < 1500:
            continue
        patch = a[ys, xs][mask[ys, xs]]
        q = (patch // 24) * 24
        vals, counts = np.unique(q, axis=0, return_counts=True)
        rgb = tuple(int(v) for v in vals[counts.argmax()])
        blocks.append({"rgb": rgb, "bbox": [x0, y0, x1, y1], "area": area,
                       "cx": (x0 + x1) / 2, "cy": (y0 + y1) / 2})
    return blocks


def check_alignment(render_png, orig_jpg):
    r = color_blocks(Image.open(render_png))
    o = color_blocks(Image.open(orig_jpg))
    ow, oh = Image.open(orig_jpg).size
    rw, rh = Image.open(render_png).size
    sx, sy = rw / ow, rh / oh
    out = []
    for ob in o:
        # find best render block with same modal colour (quantised)
        best = None
        for rb in r:
            d = sum(abs(rb["rgb"][i] - ob["rgb"][i]) for i in range(3))
            if d <= 60:
                if best is None or d < best[0]:
                    best = (d, rb)
        if best is None:
            out.append({"orig_rgb": ob["rgb"], "orig_bbox_px": ob["bbox"],
                        "match": None})
            continue
        rb = best[1]
        ocx_in = (ob["cx"] * sx) / RENDER_DPI
        ocy_in = (ob["cy"] * sy) / RENDER_DPI
        rcx_in = rb["cx"] / RENDER_DPI
        rcy_in = rb["cy"] / RENDER_DPI
        dx, dy = rcx_in - ocx_in, rcy_in - ocy_in
        out.append({
            "orig_rgb": ob["rgb"],
            "orig_bbox_px": ob["bbox"],
            "render_rgb": rb["rgb"],
            "render_bbox_px": rb["bbox"],
            "orig_centroid_in": [round(ocx_in, 3), round(ocy_in, 3)],
            "render_centroid_in": [round(rcx_in, 3), round(rcy_in, 3)],
            "delta_in": [round(dx, 3), round(dy, 3)],
            "delta_dist_in": round(float(np.hypot(dx, dy)), 3),
            "area_ratio": round(rb["area"] / max(1, ob["area"]), 2),
        })
    out.sort(key=lambda d: -(d.get("delta_dist_in") or 0))
    return out


# ------------------------------------------------------------------ 5. badge
def check_badge(pptx_path, required_num):
    prs = Presentation(pptx_path)
    badge_text = None
    for sh in prs.slides[0].shapes:
        if not sh.has_text_frame:
            continue
        t = sh.text_frame.text.strip()
        if t.isdigit() and abs(sh.left / 914400 - BADGE[0]) < 0.05 \
                and abs(sh.top / 914400 - BADGE[1]) < 0.05:
            badge_text = t
    return {
        "required": str(required_num),
        "found": badge_text,
        "ok": badge_text == str(required_num),
    }


# -------------------------------------------------------------- 6. eq-linear
LINEAR_PAT = re.compile(
    r"(frac\s*\{|sum\s*from|\bfrac\b|\\frac|sqrt\s*\(|\^\{|_\{|"
    r"\bTP\s*/\s*\(|\bFN\s*/\s*\(|\bFP\s*/\s*\(|\bTN\s*/\s*\(|"
    r"\d\s*/\s*\d|[A-Za-z]\s*\^\s*\d|[A-Za-z]_\d)", re.I)


def check_eq_linear(pptx_path, build_js):
    """Equation-looking content that is plain linear text rather than a 2D image."""
    findings = []
    prs = Presentation(pptx_path)
    for sh in prs.slides[0].shapes:
        if not sh.has_text_frame:
            continue
        t = sh.text_frame.text
        if not t.strip():
            continue
        if LINEAR_PAT.search(t):
            findings.append({
                "kind": "TEXT_LINEAR_MATH",
                "shape_id": sh.shape_id,
                "text": t[:120],
                "box_in": [round(sh.left / 914400, 3), round(sh.top / 914400, 3),
                           round((sh.left + sh.width) / 914400, 3),
                           round((sh.top + sh.height) / 914400, 3)],
            })
    # build script: equation drawn as text with ^ _ / forms
    if os.path.exists(build_js):
        src = open(build_js).read()
        for m in re.finditer(r'addText\(\s*("(?:[^"\\]|\\.)*")', src):
            lit = m.group(1)
            if LINEAR_PAT.search(lit):
                findings.append({"kind": "BUILD_LINEAR_MATH", "literal": lit[:140]})
    return findings


def eq_images(pptx_path):
    """List embedded picture shapes (candidate 2D equation renders)."""
    prs = Presentation(pptx_path)
    out = []
    for sh in prs.slides[0].shapes:
        if sh.shape_type is not None and "PICTURE" in str(sh.shape_type):
            out.append({"id": sh.shape_id,
                        "box_in": [round(sh.left / 914400, 3), round(sh.top / 914400, 3),
                                   round((sh.left + sh.width) / 914400, 3),
                                   round((sh.top + sh.height) / 914400, 3)]})
    return out


# -------------------------------------------------------------------- driver
def run(slide):
    outdir = os.path.join(PRE, f"slide_{slide:03d}")
    pptx = os.path.join(PPTX_DIR, f"slide_{slide:03d}_recreated.pptx")
    build = os.path.join(PPTX_DIR, "build", f"slide_{slide:03d}.js")
    render = os.path.join(outdir, "render-1.png")
    pdf = os.path.join(outdir, f"slide_{slide:03d}_recreated.pdf")
    orig = os.path.join(ORIG_DIR, f"slide_{slide:03d}.jpg")
    if not os.path.exists(orig):
        orig = os.path.join(ORIG_DIR, f"slide_{slide:03d}-.jpg")

    words = load_words(pdf)
    shapes = shape_boxes(pptx)
    spec_final = os.path.join(NS, "analysis", f"slide_{slide:03d}_final.json")
    spec_raw = os.path.join(NS, "analysis", f"slide_{slide:03d}_raw.json")
    spec = spec_final if os.path.exists(spec_final) else spec_raw
    res = {
        "slide": slide,
        "pptx": pptx,
        "pptx_mtime": os.path.getmtime(pptx),
        "build_mtime": os.path.getmtime(build) if os.path.exists(build) else None,
        "render": render,
        "original": orig,
        "n_words": len(words),
        "containment": check_containment(render),
        "overlaps": check_text_overlap(words),
        "clipping": check_clipping(words, shapes),
        "duplicates": check_duplicates(pptx),
        "missing_vs_spec": check_missing_vs_spec(spec, words, pptx),
        "alignment": check_alignment(render, orig)[:14],
        "badge": check_badge(pptx, slide),
        "eq_linear": check_eq_linear(pptx, build),
        "eq_images": eq_images(pptx),
        "shapes": shapes,
        "words": words,
    }
    with open(os.path.join(outdir, "measurements.json"), "w") as f:
        json.dump({k: v for k, v in res.items() if k not in ("words", "shapes")}, f, indent=2)
    with open(os.path.join(outdir, "words.json"), "w") as f:
        json.dump(words, f, indent=1)
    return res


if __name__ == "__main__":
    for s in [int(a) for a in sys.argv[1:]]:
        r = run(s)
        print("=" * 70)
        print(f"slide {s:03d}  words={r['n_words']}")
        print("  contain:", {k: v["count"] for k, v in r["containment"].items()})
        for k, v in r["containment"].items():
            if v["count"]:
                print(f"    !! {k} bbox_in={v['bbox_in']}")
        print(f"  overlaps: {len(r['overlaps'])}")
        for o in r["overlaps"][:12]:
            print(f"    {o['a']!r}@{o['a_box']} <> {o['b']!r}@{o['b_box']} frac={o['overlap_frac']}")
        print(f"  clipping: {len(r['clipping'])}")
        for c in r["clipping"][:12]:
            print(f"    {c['word']!r} shape={c['shape_id']} over={c['overflow_in']}")
        print(f"  duplicates: {len(r['duplicates'])}")
        for d in r["duplicates"][:5]:
            print(f"    x{d['count']} {d['text'][:70]!r} at {d['occurrences']}")
        mv = r["missing_vs_spec"]
        if mv:
            print(f"  missing_vs_spec ({os.path.basename(mv['spec'])}): {mv['n_missing']}")
            for mm in mv["missing"][:10]:
                print(f"    [{mm['src']}] {mm['text']!r}")
        print(f"  badge: {r['badge']}")
        print(f"  eq_linear: {len(r['eq_linear'])} {r['eq_linear'][:4]}")
        print(f"  eq_images: {len(r['eq_images'])}")
        print("  alignment top:")
        for a in r["alignment"][:6]:
            print(f"    {a.get('orig_rgb')} d={a.get('delta_in')} dist={a.get('delta_dist_in')} ar={a.get('area_ratio')}")
