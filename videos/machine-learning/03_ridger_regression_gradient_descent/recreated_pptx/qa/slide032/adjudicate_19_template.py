#!/usr/bin/env python3
"""Slide 032 — decisive '?' vs '7' test on the right chord-endpoint label.

Original (960x540, 1px=1pt) vs render_10 (2001x1125, 2.0833 px/pt).
Both label regions are extracted BLACK-ink-only (the original's curve is
gray-blue, the dot is black but lies LEFT of the label; the render's chord/dot
are at frame x<=727), normalized to frame scale, and compared glyph-by-glyph
against '?' / '7' / ',' / '(' / ')' / '2' / '0' templates rendered from the
build's own serif family. A validated control run on the original's known
"(2, 10)" label proves the matcher works before it is trusted on the unknown.
"""
import os
from PIL import Image, ImageDraw, ImageFont

ROOT = "/worksp""aces/codespaces-blank/ai_llm_slides"
DECK = os.path.join(ROOT, "videos/machine-learning/03_ridger_regression_gradient_descent")
ORIG = os.path.join(DECK, "unique_slides/slide_032.jpg")
REND = os.path.join(DECK, "recreated_pptx/qa/slide032/render_10.png")
FONTS = [
    "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
]
FONTS = [f for f in FONTS if os.path.exists(f)]

# ---- ORIGINAL label region (frame px) ----
O_X0, O_X1, O_Y0, O_X1 = 726, 754, 138, 155
O_Y1 = 152
# ORIGINAL control label "(2, 10)"
C_X0, C_X1, C_Y0, C_Y1 = 617, 662, 138, 160
# ---- RENDER label region (render px) ----
R_X0, R_X1, R_Y0, R_Y1 = 1513, 1570, 292, 320

def gray(path):
    return Image.open(path).convert("L")

def bmp(im, x0, y0, x1, y1, thr):
    px = im.load()
    return [[1 if px[x, y] < thr else 0 for x in range(x0, x1 + 1)] for y in range(y0, y1 + 1)]

def cols_groups(bm, x0, gap=1):
    n = len(bm[0])
    ink = [any(bm[i][j] for i in range(len(bm))) for j in range(n)]
    out, run, empt = [], None, 0
    for j, v in enumerate(ink):
        if v:
            if run is None:
                run = [j, j]
            else:
                run[1] = j
            empt = 0
        elif run is not None:
            empt += 1
            if empt > gap:
                out.append((x0 + run[0], x0 + run[1]))
                run = None
    if run is not None:
        out.append((x0 + run[0], x0 + run[1]))
    return out

def trim(bm):
    rows = [r for r in bm if any(r)]
    if not rows:
        return None
    cols = [j for j in range(len(rows[0])) if any(r[j] for r in rows)]
    return [[r[j] for j in range(cols[0], cols[-1] + 1)] for r in rows]

def iou(a, b):
    a = trim(a); b = trim(b)
    if a is None or b is None:
        return 0.0
    H, W = max(len(a), len(b)), max(len(a[0]), len(b[0]))
    A = [[0] * W for _ in range(H)]; B = [[0] * W for _ in range(H)]
    for i, r in enumerate(a):
        for j, v in enumerate(r):
            A[i][j] = v
    for i, r in enumerate(b):
        for j, v in enumerate(r):
            B[i][j] = v
    inter = sum(A[i][j] and B[i][j] for i in range(H) for j in range(W))
    union = sum(A[i][j] or B[i][j] for i in range(H) for j in range(W))
    return inter / union if union else 0.0

def best_iou(box, tmpl, dxs=range(-4, 5), dys=range(-4, 5)):
    """slide tmpl over box (both bitmaps), return best IoU"""
    best = 0.0
    H, W = len(box), len(box[0])
    h, w = len(tmpl), len(tmpl[0])
    for dy in dys:
        for dx in dxs:
            for yi in range(0, max(1, H - h + 1)):
                for xi in range(0, max(1, W - w + 1)):
                    if yi + h > H or xi + w > W:
                        continue
                    sub = [[box[yi + yy][xi + xx] for xx in range(w)] for yy in range(h)]
                    v = iou(sub, tmpl)
                    if v > best:
                        best = v
    return best

def render_char(ch, fontpath, size):
    f = ImageFont.truetype(fontpath, size)
    im = Image.new("L", (60, 60), 255)
    d = ImageDraw.Draw(im)
    d.text((10, 10), ch, fill=0, font=f)
    bm = [[1 if im.getpixel((x, y)) < 128 else 0 for x in range(60)] for y in range(60)]
    return trim(bm)

def render_str(s, fontpath, size):
    f = ImageFont.truetype(fontpath, size)
    im = Image.new("L", (200, 60), 255)
    d = ImageDraw.Draw(im)
    d.text((10, 10), s, fill=0, font=f)
    bm = [[1 if im.getpixel((x, y)) < 128 else 0 for x in range(200)] for y in range(60)]
    return trim(bm)

def show(bm, x0, y0, title, hdr=True):
    print(f"--- {title}  x{x0}..{x0+(len(bm[0])-1)} y{y0}..{y0+(len(bm)-1)} "
          f"({len(bm[0])}x{len(bm)})")
    if hdr:
        print("     " + "".join(str((x0 + j) % 10) for j in range(len(bm[0]))))
    for i, r in enumerate(bm):
        print(f"{y0+i:4d} " + "".join("#" if v else "." for v in r))
    print()

def signature(bm, title):
    rows = [sum(r) for r in bm]
    top = next((i for i, v in enumerate(rows) if v), None)
    bot = len(rows) - 1 - next((i for i, v in enumerate(reversed(rows)) if v), None)
    blanks = [i for i in range(top, bot + 1) if rows[i] == 0]
    def span(i):
        idx = [k for k, v in enumerate(bm[i]) if v]
        return (idx[0], idx[-1], len(idx)) if idx else None
    print(f"  {title}: {len(bm[0])}w x {bot-top+1}h  rows={rows[top:bot+1]} "
          f"inner_blank_rows={blanks}")
    print(f"      top_span={span(top)}  bot_span={span(bot)}  mid_span={span((top+bot)//2)}")
    return {"w": len(bm[0]), "h": bot - top + 1, "rows": rows[top:bot+1],
            "blanks": blanks, "top": span(top), "bot": span(bot)}

def main():
    o = gray(ORIG)
    r = gray(REND)
    print("############ ORIGINAL unknown label (thr 190) ############")
    ob = bmp(o, O_X0, O_Y0, O_X1, O_Y1, 190)
    show(ob, O_X0, O_Y0, "ORIGINAL label")
    for gx0, gx1 in cols_groups(ob, O_X0, 1):
        sub = [[ob[i][j] for j in range(gx0 - O_X0, gx1 - O_X0 + 1)] for i in range(len(ob))]
        sub = trim(sub)
        if sub and len(sub) >= 2:
            signature(sub, f"glyph x{gx0}..{gx1}")

    print("############ ORIGINAL control '(2, 10)' (thr 190) ############")
    cb = bmp(o, C_X0, C_Y0, C_X1, C_Y1, 190)
    show(cb, C_X0, C_Y0, "ORIGINAL control")
    for gx0, gx1 in cols_groups(cb, C_X0, 1):
        sub = [[cb[i][j] for j in range(gx0 - C_X0, gx1 - C_X0 + 1)] for i in range(len(cb))]
        sub = trim(sub)
        if sub and len(sub) >= 2:
            signature(sub, f"ctrlglyph x{gx0}..{gx1}")

    print("############ RENDER_10 label '(?, ?)' rescaled to frame scale ############")
    # render region -> frame scale by box-averaging
    rr = im_r = r.crop((R_X0, R_Y0, R_X1 + 1, R_Y1 + 1))
    w, h = rr.size
    fw = 2.0833
    nw = int(round(w / fw))
    small = rr.resize((nw, int(round(h / fw))), Image.BOX)
    rbm = [[1 if small.getpixel((x, y)) < 190 else 0 for x in range(nw)] for y in range(small.size[1])]
    fx0 = R_X0 / fw
    show(rbm, round(fx0), int(R_Y0 / fw), "RENDER label at frame scale")
    for gx0, gx1 in cols_groups(rbm, 0, 1):
        print(f"  (render) glyph group at scaled col {gx0}..{gx1} = frame x {fx0 + gx0/fw:.1f}..{fx0 + (gx1+1)/fw:.1f}")
    print(f"  render label scaled: {len(rbm[0])} x {len(rbm)} px at frame scale; "
          f"frame x {fx0:.1f}..{fx0 + len(rbm[0])/fw:.1f}")

    print("############ CONTROL-VALIDATED STRING MATCH ############")
    # control: the original's "(2, 10)" ink, cropped to its true bbox
    cbox = trim(cb)
    show(cbox, 0, 0, "control ink bbox (normalised)", hdr=False)
    cands = ["(2, 10)", "(5, 1)", "(?, ?)", "(7, 7)", "(8, 8)", "(8, 10)", "(2, 5)",
             "(10, 2)", "(0, 0)", "(5, 5)", "(9, 9)", "(?, ?)", "(?, 10)", "(?, 5)"]
    rows = []
    for fp in FONTS:
        for size in range(8, 18):
            for s in dict.fromkeys(cands):
                t = render_str(s, fp, size)
                if t is None:
                    continue
                sc = best_iou(cbox, t, dxs=(0, 1, 2), dys=(0, 1, 2))
                rows.append((sc, os.path.basename(fp), size, s))
    rows.sort(reverse=True)
    print("  CONTROL best 12 (font, size, string):")
    for sc, fn, sz, s in rows[:12]:
        print(f"    {sc:.4f}  {fn} {sz}pt  {s!r}")

    print("############ UNKNOWN label string match ############")
    ubox = trim(ob)
    rows2 = []
    for fp in FONTS:
        for size in range(8, 18):
            for s in dict.fromkeys(cands):
                t = render_str(s, fp, size)
                if t is None:
                    continue
                sc = best_iou(ubox, t, dxs=(0, 1, 2), dys=(0, 1, 2))
                rows2.append((sc, os.path.basename(fp), size, s))
    rows2.sort(reverse=True)
    print("  UNKNOWN best 15 (font, size, string):")
    for sc, fn, sz, s in rows2[:15]:
        print(f"    {sc:.4f}  {fn} {sz}pt  {s!r}")
    print("  control top1:", rows[0], " unknown top1:", rows2[0])

if __name__ == "__main__":
    main()
