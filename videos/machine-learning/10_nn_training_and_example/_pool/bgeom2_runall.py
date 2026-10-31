import importlib.util, json
s=importlib.util.spec_from_file_location('g','_pool/bgeom2_geom.py')
g=importlib.util.module_from_spec(s); s.loader.exec_module(g)
out=[]
for sl in ("008","009","010","012","013"):
    r=g.measure(sl)
    if r is None:
        print(sl,"MISSING"); continue
    out.append(r)
    print(sl, "mean",r["render_mean"], "dim_ok",r["dim_ok"], "blank_ok",r["blank_ok"])
    for nm,rec in r["regions"].items():
        rb,ob=rec["render"],rec["orig"]
        if rb is None or ob is None:
            print(f"   {nm:7s} {rec['status']:20s} {rec.get('note')} render={rb} orig={ob}")
        else:
            d=rec["deltas"]
            print(f"   {nm:7s} {rec['status']:20s} worst={rec['worst_px150']:6.1f} px150 "
                  f"L/T/R/B={d['left']:+.0f}/{d['top']:+.0f}/{d['right']:+.0f}/{d['bottom']:+.0f}")
            print(f"          rend x[{rb['left']:.2f},{rb['right']:.2f}] y[{rb['top']:.2f},{rb['bottom']:.2f}] ink={rb['ink_px']}"
                  f"  orig x[{ob['left']:.2f},{ob['right']:.2f}] y[{ob['top']:.2f},{ob['bottom']:.2f}] ink={ob['ink_px']}")
json.dump(out, open("_pool/bgeom2_measurements.json","w"), indent=1)
print("saved")
