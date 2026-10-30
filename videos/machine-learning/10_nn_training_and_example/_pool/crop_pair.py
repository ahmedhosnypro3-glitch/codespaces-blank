#!/usr/bin/env python3
"""Make a matched-effective-scale crop pair: render (IMG1) vs original frame (IMG2).

Usage:
  crop_pair.py <render.png> <original.jpg> <out_prefix> <x0> <y0> <x1> <y1> [--scale N]

x0..y1 are normalized [0..1] fractions of the slide. The original crop is
resampled to the render crop's pixel size so both crops show the content at
the same effective scale (dense-region-crop-compare pattern).
"""
import sys
from PIL import Image


def main():
    args = sys.argv[1:]
    scale = None
    if "--scale" in args:
        i = args.index("--scale")
        scale = int(args[i + 1])
        args = args[:i] + args[i + 2:]
    render_p, orig_p, out_prefix, x0, y0, x1, y1 = args
    x0, y0, x1, y1 = float(x0), float(y0), float(x1), float(y1)

    r = Image.open(render_p).convert("RGB")
    o = Image.open(orig_p).convert("RGB")
    rc = r.crop((int(x0 * r.width), int(y0 * r.height),
                 int(x1 * r.width), int(y1 * r.height)))
    oc = o.crop((int(x0 * o.width), int(y0 * o.height),
                 int(x1 * o.width), int(y1 * o.height)))
    if scale and scale > 1:
        oc = oc.resize((oc.width * scale, oc.height * scale), Image.LANCZOS)
    else:
        oc = oc.resize(rc.size, Image.LANCZOS)
    rc.save(out_prefix + "_render.png")
    oc.save(out_prefix + "_orig.png")
    print(f"render crop {rc.size} | orig crop {oc.size} -> {out_prefix}_render.png / _orig.png")


if __name__ == "__main__":
    main()
