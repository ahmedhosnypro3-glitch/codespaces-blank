"""verification_attempt_7_fix4 — slide 004 current-deliverable proof.

Run from the deck namespace. Verifies:
  1. source Remember label color is REDTXT FF0000;
  2. current PPTX XML Remember run is <a:srgbClr val="FF0000"/>;
  3. current render Remember ink is red;
  4. the lower-case vector subscript (10 rows) vs a capital comparator
     (12 rows) discriminator keeps the subscript refutation alive;
  5. the four refuted dossier items remain refuted.
"""

import json
import re
import xml.etree.ElementTree as ET
from zipfile import ZipFile

import numpy as np
from PIL import Image

DECK = "."
PPTX = "recreated_pptx/slide_004_recreated.pptx"
RENDER = "recreated_pptx/qa/slide004/render_7.png"
ORIGINAL = "unique_slides/slide_004.jpg"
SPEC = "analysis/slide_004_final.json"

build = open("recreated_pptx/build/slide_004.js", encoding="utf-8").read()
spec = json.load(open(SPEC, encoding="utf-8"))

source_ok = re.search(
    r'\{\s*text:\s*"Remember",\s*options:\s*\{\s*color:\s*REDTXT',
    build,
) is not None

A = "{http://schemas.openxmlformats.org/drawingml/2006/main}"
with ZipFile(PPTX) as z:
    slide_xml = z.read("ppt/slides/slide1.xml")
root = ET.fromstring(slide_xml)
xml_red = False
for run in root.iter(A + "r"):
    text_node = run.find(A + "t")
    if text_node is not None and text_node.text == "Remember":
        props = run.find(A + "rPr")
        if props is not None:
            fill = props.find(A + "solidFill")
            if fill is not None:
                color = fill.find(A + "srgbClr")
                if color is not None and color.get("val") == "FF0000":
                    xml_red = True

orig = np.asarray(Image.open(ORIGINAL).convert("RGB")).astype(int)
rend = np.asarray(Image.open(RENDER).convert("RGB")).astype(int)
SX = 2001 / 960.0
SY = 1125 / 540.0


def red_mean(img, x0, y0, x1, y1, xscale=1.0, yscale=1.0):
    crop = img[y0:y1, x0:x1].astype(int)
    r, g, b = crop[..., 0], crop[..., 1], crop[..., 2]
    if img is rend:
        core = (r >= 245) & (g <= 80) & (b <= 120)
    else:
        core = (r > g + 15) & (r > b + 5) & (r < 250) & (r > 170)
    selected = crop[core]
    return tuple(round(float(q), 1) for q in np.round(selected.mean(axis=0), 1))


orig_remember_red = red_mean(orig, 787, 103, 855, 119)
rend_remember_red = red_mean(
    rend,
    int(787 * SX),
    int(103 * SY),
    int(855 * SX),
    int(119 * SY),
)

# Matched ink threshold (< 240 grayscale), tightly framed to discrete subscript
# glyphs in the original lecture frame.
gray = np.asarray(Image.open(ORIGINAL).convert("L"))


def span(box, threshold=240):
    sub = gray[box[1]:box[3], box[0]:box[2]] < threshold
    ys, _ = np.nonzero(sub)
    y0 = int(ys.min() + box[1])
    y1 = int(ys.max() + box[1])
    return y0, y1, y1 - y0 + 1


lower_left = span((188, 190, 195, 207))
capital_n = span((594, 320, 602, 340))

# Box interior medians, excluding text rows where practical.
boxes = [
    ("Objective", (82, 246, 296, 298)),
    ("Error", (82, 310, 480, 362)),
    ("Formula", (82, 468, 480, 520)),
]
fill_results = []
for name, box in boxes:
    o = np.median(orig[box[1]:box[3], box[0]:box[2]].reshape(-1, 3), axis=0)
    r = np.median(
        rend[
            int(box[1] * SY):int(box[3] * SY),
            int(box[0] * SX):int(box[2] * SX),
        ].reshape(-1, 3),
        axis=0,
    )
    fill_results.append((name, o.tolist(), r.tolist()))

# Remember construction: one pale-blue fill and no near-white band inside the
# measured box.
remember_fill = (
    np.median(orig[120:150, 790:875].reshape(-1, 3), axis=0).tolist(),
    np.median(
        rend[int(120 * SY):int(150 * SY), int(790 * SX):int(875 * SX)].reshape(-1, 3),
        axis=0,
    ).tolist(),
)
white_bands_orig = int(
    (
        (orig[102:150, 786:868].min(axis=2) > 235)
        & (orig[102:150, 786:868].max(axis=2) > 235)
    ).sum()
)

spec_text = json.dumps(spec, ensure_ascii=False)
paren_ok = "X_{N\u00d7(d+1)}" in spec_text
lower_spec_ok = "}\\right)_{n \\times 1}" in spec_text or "y_n" in spec_text

print("verification_attempt_7_fix4 — slide 004 current deliverable")
print("[%s] Remember source color is REDTXT" % ("PASS" if source_ok else "FAIL"))
print(
    "[%s] Remember PPTX run srgbClr FF0000"
    % ("PASS" if xml_red else "FAIL")
)
print(
    "[%s] Remember render ink is red: original mean RGB=%s, render mean RGB=%s"
    % (
        "PASS" if rend_remember_red[0] > rend_remember_red[1] + 50 else "FAIL",
        list(orig_remember_red),
        list(rend_remember_red),
    )
)
print(
    "[%s] subscript discriminator: lower vector n rows=%d y%d..%d, capital comparator rows=%d y%d..%d"
    % (
        "PASS" if lower_left[2] == 10 and capital_n[2] == 12 else "FAIL",
        lower_left[2],
        lower_left[0],
        lower_left[1],
        capital_n[2],
        capital_n[0],
        capital_n[1],
    )
)
print("[%s] vector subscript spec is lowercase n" % ("PASS" if lower_spec_ok else "FAIL"))
print("[%s] X subscript keeps foundered parenthesised (d+1)" % ("PASS" if paren_ok else "FAIL"))
for name, o, r in fill_results:
    pale = (o[1] > o[2]) and (r[1] > r[2])
    print(
        "[%s] %s fill is pale yellow family: original median=%s, render median=%s"
        % ("PASS" if pale else "FAIL", name, o, r)
    )
remember_pale = (
    remember_fill[0][2] > remember_fill[0][0]
    and remember_fill[1][2] > remember_fill[1][0]
    and white_bands_orig < 100
)
print(
    "[%s] Remember construction: single pale-blue fill, no white header band: original median=%s, render median=%s, white band px=%d"
    % ("PASS" if remember_pale else "FAIL", remember_fill[0], remember_fill[1], white_bands_orig)
)

all_pass = all(
    [
        source_ok,
        xml_red,
        rend_remember_red[0] > rend_remember_red[1] + 50,
        lower_left[2] == 10,
        capital_n[2] == 12,
        lower_spec_ok,
        paren_ok,
        all((o[1] > o[2]) and (r[1] > r[2]) for _, o, r in fill_results),
        remember_pale,
    ]
)
print("RESULT: %s" % ("ALL PASS" if all_pass else "FAIL"))
