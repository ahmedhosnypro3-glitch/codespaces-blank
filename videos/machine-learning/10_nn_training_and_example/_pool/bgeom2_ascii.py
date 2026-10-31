#!/usr/bin/env python3
"""Lane G: 60x15 slide-inch structure maps (ASCII) for the original frame and the
150dpi render, from the same chrome-free content masks used for the measurement."""
import importlib.util, numpy as np
s=importlib.util.spec_from_file_location('g','_pool/bgeom2_geom.py')
g=importlib.util.module_from_spec(s); s.loader.exec_module(g)
for slide in ("008","009","010","012","013"):
    print("="*78); print("SLIDE", slide)
    for tag, path, kind in (("ORIG", f"unique_slides/slide_{slide}.jpg","orig"),
                            ("REND", f"_pool/tmp_geom_b_geom_2/{slide}/render-1.png","rend")):
        mask, mp, size = g.chrome_free_mask(path, kind)
        h, w = mask.shape
        yy, xx = np.mgrid[0:h, 0:w]
        sx, sy = mp["x"](xx), mp["y"](yy)
        print(f"  --- {tag}")
        for r in range(15):
            ya, yb = r*0.5, (r+1)*0.5
            line = ""
            for c in range(60):
                xa, xb = c*13.3333/60, (c+1)*13.3333/60
                sel = (sy>=ya)&(sy<yb)&(sx>=xa)&(sx<xb)
                n = int((mask&sel).sum())
                line += " .:-=+*#"[min(7, (n // 40))]
            print(f"   {ya:4.1f}|{line}|")
