import importlib.util, numpy as np, json
s=importlib.util.spec_from_file_location('g','_pool/bgeom2_geom.py')
g=importlib.util.module_from_spec(s); s.loader.exec_module(g)
NS="."
# Hypothesis A (house-fiducial, per-axis) -- in the library
# Hypothesis B: red rect == slide edge, uniform scale
FID_B = {"x": (57.0, 904.0), "y": (42.0, 518.0)}
def mapB(p, ax):
    a0, a1 = FID_B[ax]
    v = a0 if ax == "x" else a0
    span = (a1 - a0) / (NSLIM[ax] if False else 0)
    return None
NSLIM = {"x": 13.3333, "y": 7.5}
def mkB():
    x0, x1 = FID_B["x"]; y0, y1 = FID_B["y"]
    sx = NSLIM["x"] / (x1 - x0); sy = NSLIM["y"] / (y1 - y0)
    return {"x": lambda p: (p - x0) * sx, "y": lambda p: (p - y0) * sy}

for slide in ("008", "009", "012"):
    print("="*70, slide)
    rm, rmap, _ = g.chrome_free_mask(f"_pool/tmp_geom_b_geom_2/{slide}/render-1.png", "rend")
    omA, omapA, _ = g.chrome_free_mask(f"unique_slides/slide_{slide}.jpg", "orig")
    # B: rebuild original mask with a different map, reuse content + chrome logic
    arr = np.asarray(__import__("PIL.Image", fromlist=["Image"]).open(f"unique_slides/slide_{slide}.jpg").convert("RGB"))
    h, w = arr.shape[:2]
    m = g.content_mask(arr); m = g.strip_frame_lines(m, arr)
    from scipy import ndimage as ndi
    m = ndi.binary_opening(m, structure=np.ones((3,3)))
    yy, xx = np.mgrid[0:h, 0:w]
    bmp = mkB()
    sx, sy = bmp["x"](xx), bmp["y"](yy)
    ins = (sx>=0)&(sx<=13.3333)&(sy>=0)&(sy<=7.5)
    bgd = ((sx>=g.BADGE[0])&(sx<=g.BADGE[2])&(sy>=g.BADGE[1])&(sy<=g.BADGE[3]))
    omB = m & ins & ~bgd
    for nm,(y0,y1) in g.REGIONS.items():
        a = g.region_box(rm, rmap, y0, y1); bA = g.region_box(omA, omapA, y0, y1); bB = g.region_box(omB, bmp, y0, y1)
        if not (a and bA and bB):
            print(f"  {nm:7s} missing on one side"); continue
        dA = g.deltas_px150(a, bA); dB = g.deltas_px150(a, bB)
        print(f"  {nm:7s} A worst={max(abs(v) for v in dA.values()):6.1f}  B worst={max(abs(v) for v in dB.values()):6.1f}   (A left/top={dA['left']:+.0f}/{dA['top']:+.0f}) (B left/top={dB['left']:+.0f}/{dB['top']:+.0f})")
