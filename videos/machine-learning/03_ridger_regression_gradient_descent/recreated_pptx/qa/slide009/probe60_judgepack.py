#!/usr/bin/env python3
"""Slide 009 — judge dispatch pack generator (attempt 1).

Extracts the Template A and Template B `-p` payloads PROGRAMMATICALLY from the
frozen deck law (shared_patterns/judge_protocol_03.md) so the bytes used at the
gate are byte-identical to the template — not retyped, where a typo would
silently change the law the judge settles. Substitutes ONLY NNN/K (and NAME plus
the one-line region description for Template B), exactly as the protocol allows.

Writes, all under qa/slide009/:
  payload_A.txt            the verbatim Template A payload
  payload_B_<name>.txt     the verbatim Template B payload per region
  judge_prompt_1.txt       the dispatch pack (sibling convention: slide038 et al.)
  judge_commands_1.sh      the exact gate commands to execute

Run: python3 probe60_judgepack.py
"""
import os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
DECK = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
PROJ = os.path.abspath(os.path.join(DECK, "..", "..", ".."))
PROTO = os.path.join(DECK, "shared_patterns", "judge_protocol_03.md")

NNN, K = "009", 1
RENDER = "videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide009/render_%d.png" % K
ORIG = "videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_%s.jpg" % NNN
PROBE_T = "videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide009/probe_%d.txt" % K
JUDGE_T = "videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide009/judge_attempt_%d.txt" % K

# Template B regions (must match probe59_crops.py exactly)
REGIONS = [
    ("eq_left",    "LEFT chart annotation box holding the black equation 50.85^2 = 2585"),
    ("eq_right",   "RIGHT chart annotation box holding the black equation 63.64^2 = 4050"),
    ("cap_left",   "LEFT chart's two caption lines: red 'Overfit' keyword + '(try to minimize the residuals ONLY)' over 'Fails to detect the Pattern'"),
    ("cap_right",  "RIGHT chart's two caption lines: red 'Generalized' keyword + '(Residuals are not minimized)' over 'Successes to detect the Pattern'"),
    ("chart_left", "LEFT scatter chart: navy border, 16x16 grid, red axes + arrowheads, blue fitted line, 12 orange points, red diagonal stroke, solid red discs incl. the large one"),
    ("chart_right", "RIGHT scatter chart: navy border, 16x16 grid, red axes + arrowheads, blue fitted line, 12 orange points, red diagonal stroke, two solid red discs"),
]

proto = open(PROTO).read()
# Scope each extraction to its OWN template section: an unscoped search for
# "GROUND RULES (founder-mandated" matches Template A's payload first and then
# runs across into Template B (that bug produced a 8978-char payload instead of
# the correct 1914).
PROTO_A = proto.split("## Template A")[1].split("## Procedure B")[0]
PROTO_B = proto.split("## Template B")[1].split("## Certificate + DB law")[0]

A = re.search(r'-p "(GROUND RULES \(founder-mandated, settle these FIRST.*?)"\n',
              PROTO_A, re.S).group(1)
B = re.search(r'-p "(GROUND RULES \(founder-mandated.*?ZOOMED CROP-PAIR.*?)"\n',
              PROTO_B, re.S).group(1)
assert len(A) == 4115, "Template A payload length drifted from the banked reference"
assert len(B) == 1914, "Template B payload length drifted from the banked reference"
assert "NNN" not in A, "Template A payload must need no substitution"
B_sub = B.replace("slide NNN", "slide %s" % NNN)
for bad in ("<NAME>", "<one-line description"):
    assert bad not in B_sub, "unreplaced placeholder %s in payload" % bad

def w(fn, s):
    p = os.path.join(HERE, fn)
    with open(p, "w") as fh:
        fh.write(s)
    return p

# Template B's payload is REGION-INDEPENDENT (NAME and the region description
# live in the --view / --capture arguments, not in the payload), so ONE payload
# file is written and shared by all six crop judges.
w("payload_A.txt", A)
w("payload_B.txt", B_sub)

# ── dispatch pack ─────────────────────────────────────────────────────────────
rel = lambda p: os.path.relpath(p, PROJ)
pack = []
pack.append("=" * 79)
pack.append("SLIDE 009 — VISUAL JUDGE DISPATCH PACK, ATTEMPT %d (w9-s009-20261021T0230, 2026-10-21)" % K)
pack.append("=" * 79)
pack.append("""Protocol law (shared_patterns/judge_protocol_03.md): the -p payloads below are
extracted PROGRAMMATICALLY from the frozen template (probe60_judgepack.py) and are
byte-for-byte identical to it except for the substitutions NNN=009, K=1 and, for
Template B, NAME + the one-line region description. Vision route: DEFAULT (no
--models flag). Thinking high, --max-tokens 65536. Outer wall: timeout 1700.
Inner --timeout 600. Never wrap analyze_image.py in another retry loop.

RENDER BEING JUDGED: %s
  (fresh 150dpi LibreOffice render of the CURRENT deliverable
   recreated_pptx/slide_009_recreated.pptx — component fidelity proven pixel-identical,
   see component_fidelity.txt; 52/52 selfcheck PASS, see selfcheck_attempt_3.txt.)

CERTIFICATION NEEDS BOTH LEGS (founder directive 2026-10-19, ALL slides zoomed):
  LEG A  Template A — full-slide comparison
  LEG B  Template B — zoomed crop-pairs, one per dense region: %s
""" % (RENDER, ", ".join(n for n, _ in REGIONS)))

pack.append("-" * 79)
pack.append("LEG A — TEMPLATE A, FULL-SLIDE COMPARISON (attempt %d)" % K)
pack.append("-" * 79)
pack.append("")
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
pack.append("COMPARISON (the real judge — execute exactly this):")
pack.append("")
pack.append("cd %s && scripts/16_vision_gate.sh timeout 1700 python3 \\" % PROJ)
pack.append("  .agents/skills/image-analysis/scripts/analyze_image.py comparison \\")
pack.append("  %s \\" % RENDER)
pack.append("  %s \\" % ORIG)
pack.append('  --view "Slide 009 recreation — fidelity check vs original lecture frame" \\')
pack.append('  --capture "IMG1=150dpi PNG render of a 13.33x7.5in PPTX; IMG2=original lecture video frame" \\')
pack.append("  --thinking high --max-tokens 65536 \\")
pack.append("  --timeout 600 --rounds 1 --tries 1 \\")
pack.append("  --transcript %s \\" % JUDGE_T)
pack.append('  -p "$(cat %s)"' % rel(os.path.join(HERE, "payload_A.txt")))
pack.append("")
for name, desc in REGIONS:
    pack.append("-" * 79)
    pack.append("LEG B — TEMPLATE B, CROP-PAIR '%s' (attempt %d)" % (name, K))
    pack.append("-" * 79)
    pack.append("region: %s" % desc)
    pack.append("")
    pack.append("cd %s && scripts/16_vision_gate.sh timeout 1700 python3 \\" % PROJ)
    pack.append("  .agents/skills/image-analysis/scripts/analyze_image.py comparison \\")
    pack.append("  videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide009/crop_%d_%s_render.png \\" % (K, name))
    pack.append("  videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide009/crop_%d_%s_orig.png \\" % (K, name))
    pack.append('  --view "Slide 009 zoomed crop %s — render vs original at matched scale (attempt %d)" \\' % (name, K))
    pack.append('  --capture "IMG1=zoomed crop of a 150dpi PPTX render; IMG2=the SAME slide-space region cropped from the original lecture frame and upscaled to match IMG1\'s effective scale; region: %s" \\' % desc)
    pack.append("  --thinking high --max-tokens 65536 \\")
    pack.append("  --timeout 600 --rounds 1 --tries 1 \\")
    pack.append("  --transcript videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide009/crop_%d_%s_judge.txt \\" % (K, name))
    pack.append('  -p "$(cat %s)"' % rel(os.path.join(HERE, "payload_B.txt")))
    pack.append("")

w("judge_prompt_1.txt", "\n".join(pack) + "\n")
print("banked judge_prompt_1.txt (%d lines)" % len(pack))
print("Template A payload: %d chars (NNN-free, verbatim)" % len(A))
print("Template B payload: %d chars (NNN=009 substituted)" % len(B_sub))
print("regions: %s" % ", ".join(n for n, _ in REGIONS))
for fn in ["payload_A.txt", "payload_B.txt"]:
    p = os.path.join(HERE, fn)
    print("  %-28s %5d bytes" % (fn, os.path.getsize(p)))
print("packet: %s" % os.path.join(HERE, "judge_prompt_1.txt"))
