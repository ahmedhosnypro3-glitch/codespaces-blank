import sys
from PIL import Image, ImageChops

def metrics(im):
    w, h = im.size
    px = im.load()
    sx = 13.333 / w  # inch per px (x)
    sy = 7.5 / h     # inch per px (y)
    def isred(x, y):
        r, g, b = px[x, y]
        return r > 110 and r - g > 45 and r - b > 45
    # frame chrome
    vcols = [x for x in range(w) if sum(1 for y in range(h) if isred(x, y)) > h * 0.8]
    hrows = [y for y in range(h) if sum(1 for x in range(w) if isred(x, y)) > w * 0.8]
    # title lines excluding frame strokes
    rows = [y for y in range(h) if y not in hrows and sum(1 for x in range(w) if x not in vcols and isred(x, y)) > 2]
    lines = []
    for y in rows:
        if lines and y - lines[-1][1] <= 2:
            lines[-1][1] = y
        else:
            lines.append([y, y])
    lines = [l for l in lines if l[1] - l[0] > 8]
    out = []
    for a, b in lines:
        xs = [x for x in range(w) if x not in vcols and any(isred(x, y) for y in range(a, b + 1))]
        cols = sorted(set(xs))
        cap = min(b for b0, b1 in [(a, b)] for y in range(b0, b1 + 1))  # placeholder
        out.append(dict(r0=a, r1=b, c0=cols[0], c1=cols[-1]))
    # band
    bandrows = [y for y in range(h) if sum(1 for x in range(w) if sum(px[x, y]) / 3 < 60) > w * 0.3]
    band = None
    if bandrows:
        y0, y1 = min(bandrows), max(bandrows)
        mid = bandrows[len(bandrows) // 2]
        xs = [x for x in range(w) if sum(px[x, mid]) / 3 < 60]
        band = dict(r0=y0, r1=y1, c0=min(xs), c1=max(xs))
    # bg mean (interior sample away from frame/title/band)
    samples = [px[int(w * 0.3), int(h * 0.75)], px[int(w * 0.7), int(h * 0.75)], px[int(w * 0.5), int(h * 0.85)]]
    bg = tuple(sum(c[i] for c in samples) // 3 for i in range(3))
    return dict(w=w, h=h, sx=sx, sy=sy, lines=out, band=band, bg=bg, vcols=vcols, hrows=hrows)

def show(m, name):
    print(f"--- {name} {m['w']}x{m['h']}")
    for i, l in enumerate(m["lines"], 1):
        print(f"  title line {i}: rows {l['r0']}-{l['r1']}  ({l['r0']*m['sy']:.2f}-{(l['r1']+1)*m['sy']:.2f} in)  "
              f"cols {l['c0']}-{l['c1']}  ({l['c0']*m['sx']:.2f}-{(l['c1']+1)*m['sx']:.2f} in)  "
              f"w={(l['c1']-l['c0']+1)*m['sx']:.2f} in  center_x={((l['c0']+l['c1']+1)/2)*m['sx']:.2f} in  ink_h={(l['r1']-l['r0']+1)*m['sy']:.2f} in")
    l1, l2 = m["lines"]
    pitch_in = (l2["r0"] - l1["r0"]) * m["sy"]
    gap_in = (l2["r0"] - l1["r1"] - 1) * m["sy"]
    print(f"  ink-top pitch = {pitch_in:.3f} in ; blank inter-line gap = {gap_in:.3f} in")
    b = m["band"]
    print(f"  black band: rows {b['r0']}-{b['r1']} ({b['r0']*m['sy']:.2f}-{(b['r1']+1)*m['sy']:.2f} in) "
          f"cols {b['c0']}-{b['c1']} ({b['c0']*m['sx']:.2f}-{(b['c1']+1)*m['sx']:.2f} in) "
          f"w={(b['c1']-b['c0']+1)*m['sx']:.2f} in h={(b['r1']-b['r0']+1)*m['sy']:.2f} in")
    print(f"  frame verticals {m['vcols']} horizontals {m['hrows']} ; bg sample RGB={m['bg']}")
    return m

o = show(metrics(Image.open(sys.argv[1]).convert("RGB")), "ORIGINAL")
r = show(metrics(Image.open(sys.argv[2]).convert("RGB")), "RENDER")

print("\n=== TOLERANCE CHECK (4px @150dpi = 0.0267in; house-chrome items excluded)")
TOL = 4 / 150
def cmp(label, ov, rv, unit="in"):
    d = rv - ov
    px150 = d / (1 / 150)
    verdict = "OK" if abs(px150) <= TOL * 150 else "** OUT OF TOLERANCE **"
    print(f"  {label:34s} orig={ov:7.3f}  render={rv:7.3f}  Δ={d:+.3f} in ({px150:+.0f}px@150dpi)  {verdict}")

l1o, l2o = o["lines"]; l1r, l2r = r["lines"]
cmp("title line1 width", (l1o['c1']-l1o['c0']+1)*o['sx'], (l1r['c1']-l1r['c0']+1)*r['sx'])
cmp("title line2 width", (l2o['c1']-l2o['c0']+1)*o['sx'], (l2r['c1']-l2r['c0']+1)*r['sx'])
cmp("title line1 ink height", (l1o['r1']-l1o['r0']+1)*o['sy'], (l1r['r1']-l1r['r0']+1)*r['sy'])
cmp("title line2 ink height", (l2o['r1']-l2o['r0']+1)*o['sy'], (l2r['r1']-l2r['r0']+1)*r['sy'])
cmp("line ink-top pitch", (l2o['r0']-l1o['r0'])*o['sy'], (l2r['r0']-l1r['r0'])*r['sy'])
cmp("inter-line blank gap", (l2o['r0']-l1o['r1']-1)*o['sy'], (l2r['r0']-l1r['r1']-1)*r['sy'])
cmp("line2 horizontal center", ((l2o['c0']+l2o['c1']+1)/2)*o['sx'], ((l2r['c0']+l2r['c1']+1)/2)*r['sx'])
bo, br = o["band"], r["band"]
cmp("band width", (bo['c1']-bo['c0']+1)*o['sx'], (br['c1']-br['c0']+1)*r['sx'])
cmp("band height", (bo['r1']-bo['r0']+1)*o['sy'], (br['r1']-br['r0']+1)*r['sy'])
print(f"  {'band top edge':34s} orig={bo['r0']*o['sy']:.3f}  render={br['r0']*r['sy']:.3f} in "
      f"(render frame bottom = {(r['hrows'][-1]+1)*r['sy']:.2f} in — house chrome; band placed at/below it by rule)")
print("  HOUSE-CHROME (overridden by rule, not tolerance-checked):")
print(f"    frame: orig x {o['vcols'][0]*o['sx']:.2f}-{o['vcols'][-1]*o['sx']:.2f} y {o['hrows'][0]*o['sy']:.2f}-{o['hrows'][-1]*o['sy']:.2f} in")
print(f"    frame: render x {r['vcols'][0]*r['sx']:.2f}-{r['vcols'][-1]*r['sx']:.2f} y {r['hrows'][0]*r['sy']:.2f}-{r['hrows'][-1]*r['sy']:.2f} in (house rule 0.15/0.15/13.03/7.2)")
print(f"    title block ink: orig rows {l1o['r0']*o['sy']:.2f}-{l2o['r1']*o['sy']:.2f} in (mid-slide); render rows {l1r['r0']*r['sy']:.2f}-{l2r['r1']*r['sy']:.2f} in (house title-y=0.28 override)")
