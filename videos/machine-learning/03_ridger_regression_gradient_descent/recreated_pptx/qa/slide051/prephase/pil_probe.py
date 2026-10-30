from PIL import Image
import sys
D = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"

def ink(img, box, thr=200):
    """ink pixels (<thr) inside box; returns list of (x,y,r,g,b)"""
    x0,y0,x1,y1 = box
    px = img.load()
    hits = []
    for y in range(y0,y1):
        for x in range(x0,x1):
            r,g,b = px[x,y][:3]
            if (r+g+b)/3 < thr: hits.append((x,y,r,g,b))
    return hits

def cluster_summary(hits):
    if not hits: return "NO INK"
    xs=[h[0] for h in hits]; ys=[h[1] for h in hits]
    rs=sum(h[2] for h in hits)//len(hits); gs=sum(h[3] for h in hits)//len(hits); bs=sum(h[4] for h in hits)//len(hits)
    cores=[h for h in hits if (h[2]+h[3]+h[4])/3 < 120]
    cr = sum(h[2] for h in cores)//len(cores) if cores else None
    cg = sum(h[3] for h in cores)//len(cores) if cores else None
    cb = sum(h[4] for h in cores)//len(cores) if cores else None
    return f"n={len(hits)} bbox=x{min(xs)}..{max(xs)} y{min(ys)}..{max(ys)} mean=({rs},{gs},{bs}) core=({cr},{cg},{cb}) n_dark={len(cores)}"

which = sys.argv[1]
if which == "048":
    im = Image.open(f"{D}/unique_slides/slide_048.jpg").convert("RGB")
    # cursor region per spec: x 70-76% (672..730), y 20-26% (108..140)
    print("048 cursor region (672..730,108..140):", cluster_summary(ink(im,(672,108,730,140))))
    # wider: right of legend to Z table, below check grid
    print("048 legend->badge strip (600..740,100..140):", cluster_summary(ink(im,(600,100,740,140))))
    # green arrow region per spec: x 93-97% (893..931), y 30-36% (162..194)
    print("048 green-arrow region (893..931,162..194):", cluster_summary(ink(im,(893,162,931,194))))
    # right edge of calc panel row 1 (x853..900, y150..190)
    print("048 right of calc row1 (853..900,150..190):", cluster_summary(ink(im,(853,150,900,190))))
elif which == "050":
    im = Image.open(f"{D}/unique_slides/slide_050.jpg").convert("RGB")
    # right of "REPEAT using Step" (measured red ink x415..537 y59..77): zone x540..717 y55..90
    print("050 eta zone (540..717,55..90):", cluster_summary(ink(im,(540,55,717,90))))
    # the red text itself for reference
    print("050 REPEAT ink (415..537,55..80):", cluster_summary(ink(im,(415,55,537,80))))
elif which == "051":
    im = Image.open(f"{D}/unique_slides/slide_051.jpg").convert("RGB")
    # cursor region per spec: x 88-94% (845..902), y 84-90% (454..486)
    print("051 cursor region (845..902,454..486):", cluster_summary(ink(im,(845,454,902,486))))
    # Z header band y64..76 x595..665
    print("051 Z-header band (595..665,62..78):", cluster_summary(ink(im,(595,62,665,78))))
    # column-glyph gaps in that band
    hits = ink(im,(595,62,665,78))
    cols = sorted(set(h[0] for h in hits))
    gaps=[]; 
    if cols:
        run=[cols[0]]
        for c in cols[1:]:
            if c-run[-1]<=2: run.append(c)
            else: gaps.append((run[0],run[-1])); run=[c]
        gaps.append((run[0],run[-1]))
    print("051 Z-header x-clusters:", gaps)
