#!/usr/bin/env python3
"""Decisive word-level adjudication of judge_attempt_4's MAJOR.

Claim (A): the render's "and model" (end of b2a) vs the original's "and".
Claim (B): the render's "the regularization term" (in b2b) vs the original's
           "the generalization term".

Method — per-word ink width measured in BOTH images at 1px=1pt, then compared
against Liberation Sans metrics for the candidate words. Calibration: measure a
word that both images agree on ("customized" in b2c, "generalization" at the
start of b2b) to pin the ORIGINAL's effective font size, then test whether the
original's disputed word width fits "model"/"and" and "regularization"/
"generalization".
"""
import numpy as np
from PIL import Image, ImageFont

QA = ("/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/"
      "03_ridger_regression_gradient_descent/recreated_pptx/qa/slide016")
ORIG = ("/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/"
        "03_ridger_regression_gradient_descent/unique_slides/slide_016.jpg")
LIN = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"

oa = np.asarray(Image.open(ORIG).convert("RGB")).astype(int)
im = Image.open(f"{QA}/render_4.png").convert("RGB")
fa = np.asarray(im).astype(int)
S = fa.shape[0] / 540


def ink(a):
    return a.min(axis=2) < 160


def words(mask, base_x, ss, gap=5):
    """Column runs -> words (runs separated by >= `gap` px are word spaces)."""
    cols = np.where(mask.any(axis=0))[0]
    if not len(cols):
        return []
    runs, start, prev = [], cols[0], cols[0]
    for c in cols[1:]:
        if c != prev + 1:
            runs.append((start, prev))
            start = c
        prev = c
    runs.append((start, prev))
    out, cur = [], [runs[0]]
    for r in runs[1:]:
        if r[0] - cur[-1][1] - 1 >= gap:
            out.append((cur[0][0], cur[-1][1]))
            cur = [r]
        else:
            cur.append(r)
    out.append((cur[0][0], cur[-1][1]))
    return [((a / ss) + base_x, (b / ss) + base_x) for a, b in out]


def w_of(txt, pt):
    f = ImageFont.truetype(LIN, int(round(pt)))
    return f.getlength(txt)


print("=" * 78)
print("CALIBRATION — words both images agree on")
print("=" * 78)
# b2c line y281..298: "customized weigh factor (do regularization to what extent)"
om = ink(oa[281:299, 84:830])
fm = ink(fa[int(281 * S):int(299 * S), int(84 * S):int(830 * S)])
ow = words(om, 84, 1.0)
rw = words(fm, 84, S)
print("b2c original words: " + " ".join(f"[{a:.0f}-{b:.0f} w{b-a+1:.0f}]" for a, b in ow))
print("b2c render   words: " + " ".join(f"[{a:.0f}-{b:.0f} w{b-a+1:.0f}]" for a, b in rw))
# first word of b2c is "customized"
o_first = ow[0][1] - ow[0][0] + 1
r_first = rw[0][1] - rw[0][0] + 1
print(f"\n'customized' width: original {o_first:.0f}px, render {r_first:.0f}px")
# infer the original's font size from that word
for pt in range(11, 20):
    if abs(w_of("customized", pt) - o_first) < 4:
        print(f"  -> original effective size ~{pt}pt (Liberation metric "
              f"{w_of('customized', pt):.0f}px)")
        OPT = pt
        break
else:
    OPT = 14
    print(f"  -> assuming ~{OPT}pt")
print(f"  -> render effective size ~{r_first / w_of('customized', 18) * 18:.1f}pt "
      f"(build uses 18pt)")

print()
print("=" * 78)
print("CLAIM (A) — does the original's b2a end with 'and' or 'and model'?")
print("=" * 78)
om2 = ink(oa[228:250, 84:830])
fm2 = ink(fa[int(228 * S):int(250 * S), int(84 * S):int(830 * S)])
ow2 = words(om2, 84, 1.0)
rw2 = words(fm2, 84, S)
print("b2a ORIGINAL last 3 words: " +
      " ".join(f"[x{a:.0f}-{b:.0f} w{b-a+1:.0f}]" for a, b in ow2[-3:]))
print("b2a RENDER   last 3 words: " +
      " ".join(f"[x{a:.0f}-{b:.0f} w{b-a+1:.0f}]" for a, b in rw2[-3:]))
print()
print("  candidate widths at the original's inferred size:")
for cand in ["and", "and model", "model"]:
    print(f"    {cand!r:12s} ~{w_of(cand, OPT):.0f}px")
o_last = ow2[-1][1] - ow2[-1][0] + 1
r_last = rw2[-1][1] - rw2[-1][0] + 1
print(f"  measured last-word width: original {o_last:.0f}px, render {r_last:.0f}px")
print(f"  original line ends x{ow2[-1][1]:.0f}; render line ends x{rw2[-1][1]:.0f}")

print()
print("=" * 78)
print("CLAIM (B) — 'regularization term' vs 'generalization term' in b2b")
print("=" * 78)
om3 = ink(oa[254:276, 84:830])
fm3 = ink(fa[int(254 * S):int(276 * S), int(84 * S):int(830 * S)])
ow3 = words(om3, 84, 1.0)
rw3 = words(fm3, 84, S)
print("b2b ORIGINAL words: " +
      " ".join(f"[x{a:.0f}-{b:.0f} w{b-a+1:.0f}]" for a, b in ow3))
print()
print("b2b RENDER   words: " +
      " ".join(f"[x{a:.0f}-{b:.0f} w{b-a+1:.0f}]" for a, b in rw3))
print()
print("  candidate word widths at the original's inferred size:")
for cand in ["regularization", "generalization"]:
    print(f"    {cand!r:16s} ~{w_of(cand, OPT):.0f}px")
print("  candidate phrase widths:")
for cand in ["regularization term", "generalization term"]:
    print(f"    {cand!r:24s} ~{w_of(cand, OPT):.0f}px")
