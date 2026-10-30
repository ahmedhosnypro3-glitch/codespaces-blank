#!/usr/bin/env python3
"""PIL adjudication helper for scope_r1 re-judge (REJUDGE_PROTOCOL step 5).

Usage:
  r1_pil.py stats <NNN>
      Ink/geometry stats for render vs original, plus global diff.
  r1_pil.py crop <NNN> <x0> <y0> <x1> <y1> [tag]
      Crop-pair at matched effective scale (fractions of frame, 0-1).
"""
import sys
from PIL import Image, ImageChops, ImageStat

VD = "/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example"


def paths(n):
    return (f"{VD}/qa/slide{n}/rejudge/render-1.png",
            f"{VD}/unique_slides/slide_{n}.jpg")


def load(n):
    rp, op = paths(n)
    r = Image.open(rp).convert("RGB")
    o = Image.open(op).convert("RGB")
    return r, o


def stats(n):
    r, o = load(n)
    W, H = r.size
    o2 = o.resize((W, H), Image.LANCZOS)
    d = ImageChops.difference(r, o2)
    st = ImageStat.Stat(d)
    print(f"slide {n}: render={r.size} original={o.size}")
    print(f"  global mean abs diff per ch: {[round(v,2) for v in st.mean]}")
    print(f"  render mean={[round(v,1) for v in ImageStat.Stat(r).mean]}")
    print(f"  orig   mean={[round(v,1) for v in ImageStat.Stat(o2).mean]}")
    # ink coverage (non-background pixels)
    for label, im in (("render", r), ("orig  ", o2)):
        g = im.convert("L")
        hist = g.histogram()
        dark = sum(hist[:128])
        white = sum(hist[224:])
        print(f"  {label} dark%={100*dark/(W*H):.1f} white%={100*white/(W*H):.1f}")
    # row profile of difference to spot vertical offsets
    rows = []
    for y in range(0, H, H//30):
        band = d.crop((0, y, W, min(y+H//30, H))).convert("L")
        rows.append((y, round(ImageStat.Stat(band).mean[0], 2)))
    print("  row-band diff profile (y, meandiff):", rows)


def crop(n, x0, y0, x1, y1, tag="crop"):
    r, o = load(n)
    W, H = r.size
    box = (int(x0*W), int(y0*H), int(x1*W), int(y1*H))
    rc = r.crop(box)
    # matched effective scale: original crop resized to render crop dims
    ow, oh = o.size
    obox = (int(x0*ow), int(y0*oh), int(x1*ow), int(y1*oh))
    oc = o.crop(obox).resize(rc.size, Image.LANCZOS)
    out = f"{VD}/qa/slide{n}/rejudge/{tag}_render.png"
    out2 = f"{VD}/qa/slide{n}/rejudge/{tag}_orig.png"
    rc.save(out); oc.save(out2)
    d = ImageChops.difference(rc, oc)
    print(f"crop {box} -> {rc.size}")
    print(f"  render={out}\n  orig  ={out2}")
    print(f"  mean abs diff={[round(v,2) for v in ImageStat.Stat(d).mean]}")


if __name__ == "__main__":
    if sys.argv[1] == "stats":
        stats(sys.argv[2])
    elif sys.argv[1] == "crop":
        crop(sys.argv[2], *[float(x) for x in sys.argv[3:7]],
             sys.argv[7] if len(sys.argv) > 7 else "crop")
