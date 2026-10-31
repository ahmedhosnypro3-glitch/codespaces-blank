src = open("mini_br_k17h.py").read().split("combos =")[0]
ns = {}
exec(src, ns)
render_br, score = ns["render_br"], ns["score"]
for c in [(-55,30,0.04,0.95,0.97,0.35), (-55,30,0.04,0.95,0.97,0.25), (-55,34,0.04,0.95,0.97,0.35), (-60,30,0.04,0.95,0.97,0.35)]:
    buf = render_br(*c)
    pe, bbox, wind, prof = score(buf)
    print("c=%s prof=%.2f wind=%.2f bbox=%s" % (c, pe, wind, bbox), flush=True)
    print("  prof:", " ".join("%.0f" % v for v in prof), flush=True)
