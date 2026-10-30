#!/usr/bin/env python3
"""Decisive glyph-level adjudication of claim (B).

Width cannot separate "regularization" from "generalization" (both ~106px here),
so compare the actual INK: the original's disputed word (b2b x257..363, y254..276)
is normalized and matched against (i) the render's own "regularization" glyphs and
(ii) Liberation Sans renderings of both candidate words at the original's
effective size. Lowest pixel difference wins.

Also re-confirms claim (A)'s last word of b2a the same way ("model" vs "and").
"""
import numpy as np
from PIL import Image, ImageFont, ImageDraw

QA = ("/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/"
      "03_ridger_regression_gradient_descent/recreated_pptx/qa/slide016")
ORIG = ("/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/"
        "03_ridger_regression_gradient_descent/unique_slides/slide_016.jpg")
LIN = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"

oa = Image.open(ORIG).convert("RGB")
im = Image.open(f"{QA}/render_4.png").convert("RGB")
S = im.size[1] / 540


def bin_crop(img, x0, x1, y0, y1):
    # PIL crop wants (left, upper, right, lower)
    if img is im:
        box = (int(round(x0 * S)), int(round(y0 * S)),
               int(round(x1 * S)), int(round(y1 * S)))
    else:
        box = (x0, y0, x1, y1)
    a = np.asarray(img.crop(box).convert("L"))
    return (a < 160).astype(np.uint8)


def norm(mask, H=34):
    im2 = Image.fromarray((mask * 255).astype(np.uint8))
    w = max(1, round(im2.size[0] * H / im2.size[1]))
    return np.asarray(im2.resize((w, H), Image.BILINEAR)).astype(float) / 255.0


def synth(txt, pt, H=34):
    f = ImageFont.truetype(LIN, int(round(pt)))
    W = int(f.getlength(txt)) + 8
    im2 = Image.new("L", (W, int(pt * 1.6)), 255)
    d = ImageDraw.Draw(im2)
    d.text((4, int(pt * 0.45)), txt, font=f, fill=0)
    a = np.asarray(im2)
    ys, xs = np.where(a < 160)
    if not len(ys):
        return None
    a = a[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
    return norm((a < 160).astype(np.uint8), H)


def diff(a, b):
    """Resize b to a's width and compute mean abs difference."""
    H = a.shape[0]
    W = a.shape[1]
    bb = np.asarray(Image.fromarray((b * 255).astype(np.uint8)).resize(
        (W, H), Image.BILINEAR)).astype(float) / 255.0
    return float(np.abs(a - bb).mean())


# ---- effective size: calibrate on b2c's 'customized', identical in both -------
cal_o = bin_crop(oa, 110, 297, 281, 299)
cal_r = bin_crop(im, 110, 302, 281, 299)
best = min(range(13, 21),
           key=lambda p: abs(norm(cal_o).shape[1] - norm(synth("customized", p)).shape[1]))
PT = best
cw = norm(synth("customized", PT)).shape[1]
print(f"original effective size calibrated ~{PT}pt "
      f"('customized' ink w={norm(cal_o).shape[1]} at H=34; "
      f"Liberation {PT}pt -> {cw})")

print("\n== CLAIM (B): the disputed word in b2b ==")
o_word = norm(bin_crop(oa, 257, 363, 254, 276))
r_word = norm(bin_crop(im, 263, 368, 254, 276))
s_reg = synth("regularization", PT)
s_gen = synth("generalization", PT)
print(f"  original disputed word ink w={o_word.shape[1]} @H34")
print(f"  render  'regularization' ink w={r_word.shape[1]} @H34")
print(f"  synth   'regularization' ink w={s_reg.shape[1]} @H34")
print(f"  synth   'generalization' ink w={s_gen.shape[1]} @H34")
print(f"  |orig - render'regularization'| = {diff(o_word, r_word):.4f}")
print(f"  |orig - synth'regularization'|  = {diff(o_word, s_reg):.4f}")
print(f"  |orig - synth'generalization'|  = {diff(o_word, s_gen):.4f}")
print(f"  (render'regularization' vs synth'regularization' sanity = "
      f"{diff(r_word, s_reg):.4f}; vs synth'generalization' = {diff(r_word, s_gen):.4f})")

print("\n== CLAIM (A): last word of b2a (control: 'model' vs 'and') ==")
oa_w = norm(bin_crop(oa, 738, 783, 228, 250))
ra_w = norm(bin_crop(im, 757, 803, 228, 250))
print(f"  original last-word ink w={oa_w.shape[1]} @H34; render last-word w={ra_w.shape[1]} @H34")
sm, sa = synth("model", PT), synth("and", PT)
print(f"  synth 'model' w={sm.shape[1]}, 'and' w={sa.shape[1]}")
print(f"  |orig - synth'model'| = {diff(oa_w, sm):.4f}")
print(f"  |orig - synth'and'|   = {diff(oa_w, sa):.4f}")
print(f"  |render - synth'model'| = {diff(ra_w, sm):.4f}")

print("\n== CONTROL: a word both images definitely agree on ('the' in b2b) ==")
oc = norm(bin_crop(oa, 229, 250, 254, 276))
st = synth("the", PT)
print(f"  original 'the' ink w={oc.shape[1]} @H34; synth 'the' w={st.shape[1]}; "
      f"diff={diff(oc, st):.4f}")
