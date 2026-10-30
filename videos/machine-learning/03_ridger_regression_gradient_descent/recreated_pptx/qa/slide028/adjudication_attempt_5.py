# Robust curve adjudication for slide 028 — both images compared to the SAME
# reference, the analytic quartic model, using straddle-aware nearest-run logic.
#
# A run that straddles the model prediction counts as a perfect match (this is
# what the dot markers do: they sit ON the curve and are fatter than the stroke).
# This avoids the earlier artefact where a fat valley dot was filtered out and the
# picker then latched onto a staircase connector line 74px away.
import sys
import numpy as np
from PIL import Image

QA = '/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide028/'
ORIG = '/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_028.jpg'
RENDER = QA + (sys.argv[1] if len(sys.argv) > 1 else 'render_5.png')

o = np.asarray(Image.open(ORIG).convert('RGB')).astype(int)
r = np.asarray(Image.open(RENDER).convert('RGB')).astype(int)
S = r.shape[0] / 540.0
print("render %dx%d scale=%.4f  original %dx%d" % (r.shape[1], r.shape[0], S, o.shape[1], o.shape[0]))

orr, ogg, obb = o[:, :, 0], o[:, :, 1], o[:, :, 2]
oblue = (obb - orr > 35) & (obb - ogg > 12) & (orr < 220)
of = np.zeros_like(oblue)
of[125:134, :] = True; of[504:513, :] = True
of[:, 85:95] = True; of[:, 854:864] = True
oblue &= ~of

rr, gg, bb = r[:, :, 0], r[:, :, 1], r[:, :, 2]
rblue = (np.abs(rr - 46) < 60) & (np.abs(gg - 117) < 60) & (np.abs(bb - 182) < 60)
rf = np.zeros_like(rblue)
rf[int(505 * S):int(512 * S), :] = True
rf[int(125 * S):int(133 * S), :] = True
rf[:, int(85 * S):int(95 * S)] = True
rf[:, int(854 * S):int(864 * S)] = True
rblue &= ~rf

QUARTIC = {
    'LEFT': (1.257813992130e-06, -1.380428744223e-03, 5.367079591099e-01,
             -8.662429049860e+01, 5.186743353907e+03),
    'RIGHT': (1.280248111588e-06, -3.212513553308e-03, 2.991242381533e+00,
              -1.224430887994e+03, 1.862054178402e+05),
}
OLD = {'LEFT': (-0.017594, 9.6960, -917.61), 'RIGHT': (-0.017881, 22.4690, -6641.32)}
SPAN = {'LEFT': (161, 383), 'RIGHT': (514, 737)}


def horner(c, x):
    y = 0.0
    for v in c:
        y = y * x + v
    return y


def runs_of(mask, ci):
    col = np.flatnonzero(mask[:, ci])
    if not len(col):
        return []
    out, s, p = [], col[0], col[0]
    for y in col[1:]:
        if y - p > 1:
            out.append((s, p)); s = y
        p = y
    out.append((s, p))
    return out


def nearest(mask, ci, pred_px):
    """Distance from pred_px to the nearest edge of any blue run; 0 if straddled."""
    runs = runs_of(mask, ci)
    if not runs:
        return None
    best = None
    for t in runs:
        if t[0] <= pred_px <= t[1]:
            return 0.0
        d = min(abs(t[0] - pred_px), abs(t[1] - pred_px))
        if best is None or d < best:
            best = d
    return float(best)


for nm, (x0, x1) in SPAN.items():
    c, old = QUARTIC[nm], OLD[nm]
    rows = []
    for x in range(x0, x1 + 1):
        yfit = horner(c, x)
        dorig = nearest(oblue, x, yfit)                        # original, frame px
        drend = nearest(rblue, int(round(x * S)), yfit * S)   # render, render px
        rows.append((x, dorig, None if drend is None else drend / S))
    oo = np.array([t[1] for t in rows if t[1] is not None])
    nn = np.array([t[2] for t in rows if t[2] is not None])
    # old quadratic's gap to the same ink, for contrast
    ogap, ngap = [], []
    for x in range(x0, x1 + 1):
        yo = old[0] * x * x + old[1] * x + old[2]
        a = nearest(oblue, x, yo)
        b = nearest(rblue, int(round(x * S)), yo * S)
        if a is not None:
            ogap.append(a)
        if b is not None:
            ngap.append(b / S)
    ogap = np.array(ogap); ngap = np.array(ngap)
    print("\n%s panel: orig-cols=%d render-cols=%d" % (nm, len(oo), len(nn)))
    print("  ORIGINAL ink vs NEW quartic : RMSE=%5.2f max=%5.2f  cols>5px %d/%d  median=%.2f"
          % (np.sqrt((oo ** 2).mean()), oo.max(), int((oo > 5).sum()), len(oo), np.median(oo)))
    print("  RENDER   ink vs NEW quartic : RMSE=%5.2f max=%5.2f  cols>5px %d/%d  median=%.2f"
          % (np.sqrt((nn ** 2).mean()), nn.max(), int((nn > 5).sum()), len(nn), np.median(nn)))
    print("  (contrast) ORIGINAL vs OLD quadratic: RMSE=%5.2f max=%5.2f cols>5px %d/%d"
          % (np.sqrt((ogap ** 2).mean()), ogap.max(), int((ogap > 5).sum()), len(ogap)))
    print("  (contrast) RENDER   vs OLD quadratic: RMSE=%5.2f max=%5.2f cols>5px %d/%d"
          % (np.sqrt((ngap ** 2).mean()), ngap.max(), int((ngap > 5).sum()), len(ngap)))
    print("  valley: old quad x=%.0f y=%.0f | new quartic x=%.0f y=%.0f"
          % (-old[1] / (2 * old[0]),
             old[0] * (-old[1] / (2 * old[0])) ** 2 + old[1] * (-old[1] / (2 * old[0])) + old[2],
             x0 + int(np.argmax([horner(c, xx) for xx in range(x0, x1 + 1)])),
             max(horner(c, xx) for xx in range(x0, x1 + 1))))
