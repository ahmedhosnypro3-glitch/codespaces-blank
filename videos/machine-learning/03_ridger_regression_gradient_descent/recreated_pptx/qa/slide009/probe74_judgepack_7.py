#!/usr/bin/env python3
"""probe74 — judge dispatch pack generator, slide 009 attempt 7 (crop set 6).

Same frozen-law mechanism as probe60_judgepack.py: the Template A and Template B
`-p` payloads are extracted PROGRAMMATICALLY from
shared_patterns/judge_protocol_03.md (byte-for-byte, length-asserted), with only
NNN substituted. The frozen template is NOT edited.

What differs from attempt 1:
  - K=7 render (render_7.png), crop set 6 (crop_6_* cut by probe73_crops_6.py)
  - LEG B covers the regions whose pixels CHANGED vs the certified attempt-5
    (eq_left, eq_right, chart_left, chart_right — proven by probe72/probe72c)
    plus the two annotation corridors that ARE the subject of the founder's
    2026-10-25 directive. cap_left/cap_right are 0-changed-px (probe72), so
    their attempt-5 certificates remain valid under the protocol's
    "a crop transcript is kept only if its region is pixel-identical" rule.
  - the founder's 2026-10-25 annotation facts travel in the --view CONTEXT line
    (owner feedback overrides the frame there); the frozen payload is untouched.

Writes: payload_A_7.txt, payload_B_7.txt, judge_prompt_7.txt
Run: python3 probe74_judgepack_7.py
"""
import os, re

HERE = os.path.dirname(os.path.abspath(__file__))
DECK = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
PROJ = os.path.abspath(os.path.join(DECK, "..", "..", ".."))
PROTO = os.path.join(DECK, "shared_patterns", "judge_protocol_03.md")

NNN, K, CK = "009", 7, 6
SL = "videos/machine-learning/03_ridger_regression_gradient_descent"
RENDER = "%s/recreated_pptx/qa/slide009/render_%d.png" % (SL, K)
ORIG = "%s/unique_slides/slide_%s.jpg" % (SL, NNN)
PROBE_T = "%s/recreated_pptx/qa/slide009/probe_%d.txt" % (SL, K)
JUDGE_T = "%s/recreated_pptx/qa/slide009/judge_attempt_%d.txt" % (SL, K)

FOUNDER = ("FOUNDER DIRECTIVE 2026-10-25 (owner feedback overrides the frame here): "
           "the red mm-annotation on both charts is INTENTIONALLY rebuilt in this attempt — "
           "the dimension arrow is ORTHOGONAL to the blue fitted line with its foot ON that line "
           "and an arrowhead at BOTH ends (upper + lower), the '50.85 mm' / '63.64 mm' label runs "
           "ALONG that arrow, and the short leader beside the outlier is RED, exactly PARALLEL to the "
           "blue line, and carries NO arrowhead. The original frame's faded pale-rose sloped dimension "
           "line, its detached single arrowhead and the label's old orientation are INTENTIONALLY "
           "corrected — they are NOT discrepancies; judge the rebuilt construction against this spec.")

REGIONS = [
    ("eq_left",    208,   140,   325,   183,
     "LEFT chart annotation box holding the black equation 50.85^2 = 2585; the founder-corrected red dimension shaft clips this box's lower-left corner"),
    ("eq_right",   625,   140,   742,   183,
     "RIGHT chart annotation box holding the black equation 63.64^2 = 4050; the founder-corrected red dimension shaft clips this box's lower-left corner"),
    ("chart_left",  87,   102,   473,   480,
     "LEFT scatter chart: navy border, 16x16 grid, red axes + arrowheads, blue fitted line, orange points, and the rebuilt red mm-annotation (double-headed arrow orthogonal to the blue line, label along the arrow, plain parallel leader beside the outlier)"),
    ("chart_right", 478,  102,   878,   480,
     "RIGHT scatter chart: navy border, 16x16 grid, red axes + arrowheads, blue fitted line, orange points, and the rebuilt red mm-annotation (double-headed arrow orthogonal to the blue line, label along the arrow, plain parallel leader beside the outlier)"),
    ("annotation_left", 150, 125, 340, 330,
     "LEFT chart mm-annotation corridor: the red dimension arrow (orthogonal to the blue fitted line, foot ON the line, arrowheads at BOTH ends), the '50.85 mm' label running ALONG that arrow, the plain parallel red leader through the outlier (NO arrowhead), and the orange outlier point"),
    ("annotation_right", 555, 125, 765, 390,
     "RIGHT chart mm-annotation corridor: the red dimension arrow (orthogonal to the blue fitted line, foot ON the line, arrowheads at BOTH ends), the '63.64 mm' label running ALONG that arrow, the plain parallel red leader through the outlier (NO arrowhead), and the orange outlier point"),
]

proto = open(PROTO).read()
PROTO_A = proto.split("## Template A")[1].split("## Procedure B")[0]
PROTO_B = proto.split("## Template B")[1].split("## Certificate + DB law")[0]

A = re.search(r'-p "(GROUND RULES \(founder-mandated, settle these FIRST.*?)"\n', PROTO_A, re.S).group(1)
B = re.search(r'-p "(GROUND RULES \(founder-mandated.*?ZOOMED CROP-PAIR.*?)"\n', PROTO_B, re.S).group(1)
assert len(A) == 4115, "Template A payload length drifted from the banked reference"
assert len(B) == 1914, "Template B payload length drifted from the banked reference"
assert "NNN" not in A, "Template A payload must need no substitution"
B_sub = B.replace("slide NNN", "slide %s" % NNN)
assert "<NAME>" not in B_sub and "<one-line description" not in B_sub

def w(fn, s):
    p = os.path.join(HERE, fn)
    with open(p, "w") as fh:
        fh.write(s)
    return p

w("payload_A_7.txt", A)
w("payload_B_7.txt", B_sub)

rel = lambda p: os.path.relpath(p, PROJ)
pack = []
pack.append("=" * 79)
pack.append("SLIDE 009 — VISUAL JUDGE DISPATCH PACK, ATTEMPT %d (crop set %d), 2026-10-25" % (K, CK))
pack.append("=" * 79)
pack.append("""Frozen-law payloads extracted PROGRAMMATICALLY from shared_patterns/judge_protocol_03.md
(probe74_judgepack_7.py) — byte-for-byte, length-asserted; only NNN=009 substituted in
Template B. Vision route: DEFAULT (no --models flag). Thinking high, --max-tokens 65536.
Outer wall timeout 1700, inner --timeout 600. Never wrap analyze_image.py in a retry loop.

RENDER BEING JUDGED: %s
  (attempt 7 = founder-annotation fix + house-chrome module restored to the pre-drift,
   AGENTS.md-conformant version; probe71 PASS, house_chrome_7 PASS, probe72/72c region diff
   PASS — every eq-region delta is annotation mechanics, equation glyphs unchanged.)

CERTIFICATION NEEDS BOTH LEGS (founder directive 2026-10-19, ALL slides zoomed):
  LEG A  Template A — full-slide comparison
  LEG B  Template B — zoomed crop-pairs: %s
cap_left/cap_right are NOT re-judged: probe72 measured 0 changed px vs the certified
attempt-5 pixels, so their attempt-5 crop certificates remain valid under the
protocol's pixel-identical rule.
""" % (RENDER, ", ".join(n for n, *_ in REGIONS)))

pack.append("-" * 79)
pack.append("PROBE FIRST (opens the gateway window; a valid body opens it, a hang means")
pack.append("sleep 300 and re-probe ONCE — a probe is NOT a judge attempt):")
pack.append("")
pack.append("cd %s && scripts/16_vision_gate.sh timeout 150 python3 \\" % PROJ)
pack.append("  .agents/skills/image-analysis/scripts/analyze_image.py analysis \\")
pack.append("  %s \\" % RENDER)
pack.append('  --view "Slide 009 recreation attempt %d — probe" \\' % K)
pack.append('  --capture "150dpi PNG render of a 13.33x7.5in PPTX" \\')
pack.append("  --timeout 120 --rounds 1 --tries 1 \\")
pack.append("  --transcript %s" % PROBE_T)
pack.append("")
pack.append("LEG A — TEMPLATE A, FULL-SLIDE COMPARISON (attempt %d)" % K)
pack.append("")
pack.append("cd %s && scripts/16_vision_gate.sh timeout 1700 python3 \\" % PROJ)
pack.append("  .agents/skills/image-analysis/scripts/analyze_image.py comparison \\")
pack.append("  %s \\" % RENDER)
pack.append("  %s \\" % ORIG)
pack.append('  --view "Slide 009 recreation — fidelity check vs original lecture frame. %s" \\' % FOUNDER)
pack.append('  --capture "IMG1=150dpi PNG render of a 13.33x7.5in PPTX; IMG2=original lecture video frame" \\')
pack.append("  --thinking high --max-tokens 65536 \\")
pack.append("  --timeout 600 --rounds 1 --tries 1 \\")
pack.append("  --transcript %s \\" % JUDGE_T)
pack.append('  -p "$(cat %s)"' % rel(os.path.join(HERE, "payload_A_7.txt")))
pack.append("")
for name, x0, y0, x1, y1, desc in REGIONS:
    pack.append("-" * 79)
    pack.append("LEG B — TEMPLATE B, CROP-PAIR '%s' (crop set %d, render attempt %d)" % (name, CK, K))
    pack.append("-" * 79)
    pack.append("region (frame px): x%d..%d y%d..%d  — %s" % (x0, x1, y0, y1, desc))
    pack.append("")
    pack.append("cd %s && scripts/16_vision_gate.sh timeout 1700 python3 \\" % PROJ)
    pack.append("  .agents/skills/image-analysis/scripts/analyze_image.py comparison \\")
    pack.append("  %s/recreated_pptx/qa/slide009/crop_%d_%s_render.png \\" % (SL, CK, name))
    pack.append("  %s/recreated_pptx/qa/slide009/crop_%d_%s_orig.png \\" % (SL, CK, name))
    pack.append('  --view "Slide 009 zoomed crop %s — render vs original at matched scale (crop set %d, render attempt %d). %s" \\' % (name, CK, K, FOUNDER))
    pack.append('  --capture "IMG1=zoomed crop of a 150dpi PPTX render; IMG2=the SAME slide-space region cropped from the original lecture frame and upscaled to match IMG1\'s effective scale; region: %s" \\' % desc)
    pack.append("  --thinking high --max-tokens 65536 \\")
    pack.append("  --timeout 600 --rounds 1 --tries 1 \\")
    pack.append("  --transcript %s/recreated_pptx/qa/slide009/crop_%d_%s_judge.txt \\" % (SL, CK, name))
    pack.append('  -p "$(cat %s)"' % rel(os.path.join(HERE, "payload_B_7.txt")))
    pack.append("")

w("judge_prompt_7.txt", "\n".join(pack) + "\n")
print("banked judge_prompt_7.txt (%d lines)" % len(pack))
print("Template A payload: %d chars (NNN-free, verbatim)" % len(A))
print("Template B payload: %d chars (NNN=009 substituted)" % len(B_sub))
print("crop legs: %s" % ", ".join(n for n, *_ in REGIONS))
for fn in ["payload_A_7.txt", "payload_B_7.txt", "judge_prompt_7.txt"]:
    p = os.path.join(HERE, fn)
    print("  %-24s %6d bytes" % (fn, os.path.getsize(p)))
