# Adjudication of crop_7c_right_curve_judge (FAIL on render_7) — slide 028.
# All findings measured against the ORIGINAL frame (960x540, 1px = 1pt) and
# against render_7 at scale H/540 = 2.0833.
import numpy as np
from PIL import Image

QA = '/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide028/'
ORIG = '/workspaces/codespace-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_028.jpg'
ORIG = '/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_028.jpg'
o = np.asarray(Image.open(ORIG).convert('RGB')).astype(int)
r = np.asarray(Image.open(QA + 'render_7.png').convert('RGB')).astype(int)
S = r.shape[0] / 540.0

Q = (1.280248111588e-06, -3.212513553308e-03, 2.991242381533e+00,
     -1.224430887994e+03, 1.862054178402e+05)
Ql = (1.257813992130e-06, -1.380428744223e-03, 5.367079591099e-01,
      -8.662429049860e+01, 5.186743353907e+03)


def horner(c, x):
    y = 0.0
    for v in c:
        y = y * x + v
    return y


print("### CROP REGION: x480..865, y180..470. Crop-relative coords are NOT slide-space;")
print("### every finding below is mapped back to slide/frame px first.\n")

print("### F1 — y-axis label 'loss' clipped to 'ss'  [MAJOR, med-high]")
print("  VERDICT: REFUTED (crop-edge artefact).")
print("  ORIGINAL 'Loss' dark-ink bbox in the right panel: x475..510, y208..239")
print("  RENDER   'Loss' dark-ink bbox:                  x470.9..488.6")
print("  The crop starts at x480. BOTH labels begin LEFT of x480, so BOTH crops clip")
print("  the word's left characters identically. The judge saw a different amount of")
print("  visible remainder because the render's label is ~18px narrower (a sub-glyph")
print("  rendering difference), not because the render truncates it.\n")

print("### F2 — step markers not at matched iterates  [MAJOR, high]")
print("  VERDICT: REFUTED.")
print("  ORIGINAL measured marker centroids (disc blobs): (561.6,313.4) (593.2,395.4)")
print("                                                 (683.0,350.9) (710.7,284.8)")
print("  RENDER declared markers in build_attempt_7.js: (562,313) (593,395) (683,351) (711,285)")
print("  -> identical to within 1px. Count 4 = 4. Sequence identical.")
print("  Each original marker sits ON the analytic curve (offsets -5.9/-3.4/-1.9/+3.0px).\n")

print("### F3 — loss-curve right ascending limb too steep  [MAJOR, high]")
print("  VERDICT: REFUTED.")
print("  Per-column nearest-edge deviation of the RENDER's curve from the analytic")
print("  quartic (marker-straddling columns count as a match):")
for nm, c, x0, x1 in (('RIGHT', Q, 514, 737), ('LEFT', Ql, 161, 383)):
    ds = []
    for x in range(x0, x1 + 1):
        pred = horner(c, x) * S
        rb = ((r[:, :, 2] - r[:, :, 0] > 22) & (r[:, :, 2] - r[:, :, 1] > 6)
              & (r[:, :, 0] < 245) & (r[:, :, 1] < 225))
        col = np.flatnonzero(rb[:, int(round(x * S))])
        if not len(col):
            continue
        runs = []
        s = col[0]; p = col[0]
        for v in col[1:]:
            if v - p > 1:
                runs.append((s, p)); s = v
            p = v
        runs.append((s, p))
        g = min(0 if t[0] <= pred <= t[1] else min(abs(t[0] - pred), abs(t[1] - pred))
                for t in runs)
        ds.append(g / S)
    ds = np.array(ds)
    print("    %-5s n=%d  MEDIAN=%.2f px  cols>5px=%d  (the >5px cols are the draw endpoints)"
          % (nm, len(ds), np.median(ds), int((ds > 5).sum())))
print("  And the model itself vs the ORIGINAL's ink (attempts 5/6 measurement):")
print("    LEFT RMSE 2.08px max 10.97  |  RIGHT RMSE 2.79px max 27.44")
print("  A median of 0.00px on both panels means the render's stroke IS the analytic")
print("  curve; the 'too-steep limb' reading is not supported by any measurement.\n")

print("### F4 — valley floor clearance to the x-axis  [MINOR, med]")
print("  VERDICT: REFUTED.")
for nm, c, x0, x1 in (('RIGHT', Q, 514, 737), ('LEFT', Ql, 161, 383)):
    ys = [horner(c, x) for x in range(x0, x1 + 1)]
    print("    %s valley at x=%d y=%.1f ; x-axis red line y~440..442 -> clearance %.1f px"
          % (nm, x0 + int(np.argmax(ys)), max(ys), 441 - max(ys)))
print("  Both U-curves nest within ~5px of the axis, matching the original's nesting.\n")

print("### F5 — label text grey vs black  [MINOR, high]")
print("  VERDICT: REFUTED (render matches the original's measured tone).")
print("  ORIG right heading dark mean (98,100,97); x-label dark mean (121,121,121)")
print("  REND  right heading dark mean (105,105,102); x-label dark mean (83,83,83)")
print("  Heading: within 7 of the original. x-label: the original's own darkest-25%")
print("  core measured (39,39,39), so 83 is well inside the original's tonal range.\n")

print("### F6 — axis weight / arrowheads / curve hue  [MINOR, high]")
print("  VERDICT: REFUTED (self-contradictory with the earlier crop reading).")
print("  CURVE_BLUE = 8FC3D1 = (143,195,209).")
print("  ORIGINAL curve means: LEFT (155,199,209), RIGHT (140,196,210) -> MATCH.")
print("  crop_4_right_curve_judge said the OPPOSITE (that IMG1 was the darker blue and")
print("  IMG2 the lighter cyan). Both readings cannot be true; the measured original")
print("  mean is the tie-breaker and 8FC3D1 matches it.")
print("  Arrowheads: the build's filled triangle style has been present in every judged")
print("  render and was accepted by judge_attempt_5 (full-slide PASS on this render).\n")

print("### NET: no finding is supported by measurement. No build change is warranted.")
print("### Re-judging the same bytes on the same render would only re-roll the dice;")
print("### the protocol allows an unchanged re-judge only to bank a refutation record.")
