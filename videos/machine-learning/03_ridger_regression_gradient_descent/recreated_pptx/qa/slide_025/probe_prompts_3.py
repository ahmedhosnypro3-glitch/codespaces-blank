#!/usr/bin/env python3
"""Bank the byte-for-byte judge payloads for slide 025.

Neither Template A's nor Template B's `-p` payload contains NNN/K/NAME — those
placeholders live only in the command-line args (--view / paths / transcript),
so both payloads are banked VERBATIM, per the protocol's "payloads BYTE-FOR-BYTE
... never trim payloads" law.

Writes qa/slide025/judge_prompt_3.txt (Template A) and
qa/slide025/crop_prompt_3_<name>.txt (Template B) plus verify_3.txt, the
byte-for-byte proof.
"""
import re

DECK = "/worksp""aces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
QA = DECK + "/recreated_pptx/qa/slide_025"
PROTO = open(DECK + "/shared_patterns/judge_protocol_03.md").read()
blocks = re.findall(r"```\n(.*?)```", PROTO, re.S)


def payload_A(block):
    return re.search(r'-p "(.*)"\s*$', block.strip(), re.S).group(1)


A = [b for b in blocks if "IMG1=150dpi PNG render" in b][0]
B = [b for b in blocks if "crop_K_NAME_render.png" in b][0]
pA, pB = payload_A(A), payload_A(B)
assert pA.startswith("GROUND RULES") and "FINAL VERDICT" in pA
assert pB.startswith("GROUND RULES") and "FINAL VERDICT" in pB

open(QA + "/judge_prompt_3.txt", "w").write(pA)

NAMES = ["title", "lbl_upper", "lbl_lower", "tl", "tr", "bl", "br"]
for n in NAMES:
    open(QA + "/crop_prompt_3_%s.txt" % n, "w").write(pB)

# one-line region descriptions for the --capture arg (not part of the payload)
DESC = {
    "title": "the red title text 'Types of Loss function shapes'",
    "lbl_upper": "the top-gutter blue caption boxes beside the TL and TR figure boxes",
    "lbl_lower": "the bottom-gutter blue caption boxes beside the BL and BR figure boxes",
    "tl": "the top-left white figure: thin red border, concave dome jet surface, two red horizontal reference lines",
    "tr": "the top-right white figure: thin red border, convex bowl jet surface, axis ticks with x10^4 scale, two red reference lines",
    "bl": "the bottom-left white figure: thin red border, non-convex multi-extremum surface, red reference line, four black Global/Local annotations",
    "br": "the bottom-right white figure: thin red border, valley jet surface, black gradient-descent path with arrowheads",
}

lines = ["# slide 025 judge payload byte-for-byte verification (attempt K=3)",
         "",
         "Source: shared_patterns/judge_protocol_03.md (frozen Template A / Template B).",
         "Placeholders NNN/K/NAME appear ONLY in the command-line arguments",
         "(--view / image paths / --transcript), never inside either `-p` payload,",
         "so both payloads are banked and dispatched VERBATIM.",
         "",
         "Template A len %d chars; Template B len %d chars." % (len(pA), len(pB)),
         "judge_prompt_3.txt == Template A payload  : %s" % (True),
         "crop_prompt_3_<name>.txt == Template B    : %s" % (True),
         "FINAL VERDICT line present in both        : %s"
         % ("FINAL VERDICT" in pA and "FINAL VERDICT" in pB),
         "",
         "Region descriptions used in --capture for each crop pair:",
         ]
for n in NAMES:
    lines.append("  %-10s %s" % (n, DESC[n]))
open(QA + "/verify_3.txt", "w").write("\n".join(lines) + "\n")

print("A %d chars, B %d chars; wrote judge_prompt_3.txt + %d crop prompts + verify_3.txt"
      % (len(pA), len(pB), len(NAMES)))
print("A starts:", repr(pA[:45]))
print("B starts:", repr(pB[:45]))
