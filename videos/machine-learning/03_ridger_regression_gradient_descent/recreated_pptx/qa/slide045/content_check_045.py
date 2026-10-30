#!/usr/bin/env python3
"""Slide 045: content-fidelity check that does NOT need the vision gate.

Extracts every text run from the shipped pptx and matches it against the
verbatim_text / equations in analysis/slide_045_final.json. This is objective
evidence for the next judge leg: it proves the render carries the required
strings, so any vision finding of "missing element" can be checked against this.

Note: this is a screening aid, NOT a substitute for the two judge legs.
"""
import json
import re
import zipfile

NS = "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
PPTX = NS + "/recreated_pptx/slide_045_recreated.pptx"
ANALYSIS = NS + "/analysis/slide_045_final.json"

z = zipfile.ZipFile(PPTX)
slide = z.read("ppt/slides/slide1.xml").decode("utf-8")

# collect text runs
runs = re.findall(r"<a:t>(.*?)</a:t>", slide, re.S)
joined = " ".join(t.strip() for t in runs if t.strip())

spec = json.load(open(ANALYSIS, encoding="utf-8"))
vt = spec.get("verbatim_text", {})

n = 0


def norm(s):
    return re.sub(r"\s+", " ", s).strip()


def check(label, s):
    global n
    n += 1
    t = norm(s)
    # compare on a punctuation/space-insensitive basis: the render uses typed
    # glyphs for subscripts (x1 not x₁), so strip sub/superscript codepoints.
    def loose(x):
        x = x.replace("\u2081", "1").replace("\u2082", "2").replace("\u2083", "3")
        x = x.replace("\u2084", "4").replace("\u2085", "5").replace("\u2086", "6")
        x = x.replace("\u03b7", "eta")
        return re.sub(r"[^0-9a-z]", "", x.lower())

    ok = loose(t) in loose(joined)
    print("[%s] %-34s %r" % ("FOUND" if ok else "MISSING", label, t))


print("=== pptx text runs (%d) ===" % len(runs))
print(joined[:1500])
print()
print("=== spec match (loose: subscript/glyph-insensitive) ===")
for k in ("bullets", "labels", "equations"):
    print("-- %s --" % k)
    for item in vt.get(k, []):
        check(k, item)
print()
print("%d strings checked" % n)
