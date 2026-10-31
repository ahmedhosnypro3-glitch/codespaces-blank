import importlib.util

NS = "/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example"
spec = importlib.util.spec_from_file_location(
    "m2", f"{NS}/_pool/geom_b_geom_3/report_gen2.py")
m2 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m2)
for n in m2.SLIDES:
    om = m2.m2.orig_ink(n, f"{NS}/unique_slides/slide_{n}.jpg")
    rp = f"{NS}/_pool/lo_geom_b_geom_3/out/slide_{n}_150.png"
    rm = m2.m2.render_ink(rp)
    sx, sy = 960 / 2001.0, 540 / 1125.0
    print(f"### {n}")
    for i, (y0, y1) in enumerate(m2.m2.region_windows(m2.m2.bands_of(om))):
        ob, opx = m2.region_box(om, y0, y1, "f")
        rb, rpx = m2.region_box(rm, y0, y1, "r")
        if ob is None or rb is None:
            print(f"  {m2.REGIONS[i]:6s} y{y0}..{y1} NOT MEASURABLE "
                  f"orig={ob} render={rb}")
            continue
        rbf = (rb[0] * sx, rb[1] * sy, rb[2] * sx, rb[3] * sy)
        d = [ob[0] - rbf[0], ob[1] - rbf[1],
             ob[2] - rbf[2], ob[3] - rbf[3]]
        w = max(abs(v) for v in d)
        print(f"  {m2.REGIONS[i]:6s} y{y0}..{y1}  {'PASS' if w <= 2 else 'EXCEEDS'}"
              f" w{w:6.2f} | orig[{ob[0]},{ob[1]}]-[{ob[2]},{ob[3]}] "
              f"rend[{rbf[0]:.1f},{rbf[1]:.1f}]-[{rbf[2]:.1f},{rbf[3]:.1f}]"
              f" | dx0={d[0]:+.2f} dy0={d[1]:+.2f} dx1={d[2]:+.2f} "
              f"dy1={d[3]:+.2f} dw={d[2]-d[0]:+.2f} dh={d[3]-d[1]:+.2f}")
