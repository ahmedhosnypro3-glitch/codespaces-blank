#!/usr/bin/env python3
"""Bank attempt-1 judge payloads extracted PROGRAMMATICALLY from the frozen deck
protocol (byte-for-byte; only NNN/K/NAME/region substitutions). 2026-10-20."""
import re

PROTO = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/shared_patterns/judge_protocol_03.md"
QA = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide001"

text = open(PROTO, encoding="utf-8").read()

# --- Template A payload: the -p line inside the fenced block after the marker ---
mA = text.split("Comparison (the real judge; `-p` payload VERBATIM below, NNN/K substituted):")[1]
blockA = mA.split("```")[1]
payloadA = next(line for line in blockA.splitlines() if line.strip().startswith('-p "'))
payloadA = payloadA.strip()[len('-p "'):-1]  # strip -p " ... trailing "
assert payloadA.startswith("GROUND RULES"), payloadA[:60]

# --- Template B payload ---
mB = text.split("## Template B — crop-pair judge")[1]
blockB = mB.split("```")[1]
payloadB = next(line for line in blockB.splitlines() if line.strip().startswith('-p "'))
payloadB = payloadB.strip()[len('-p "'):-1]
assert payloadB.startswith("GROUND RULES"), payloadB[:60]

# substitutions: NNN -> 001, K -> 1 (byte-for-byte from the frozen template)
pA = payloadA.replace("NNN", "001").replace("attempt K", "attempt 1")
pB = payloadB.replace("NNN", "001").replace("attempt K", "attempt 1")

open(f"{QA}/judge_prompt_1.txt", "w", encoding="utf-8").write(pA + "\n")
print(f"banked judge_prompt_1.txt ({len(pA)} chars, sha-check later)")

REGIONS = {
    "title":       "three-line red title block (large bold red text)",
    "preparedby":  "subtitle + Prepared By attribution block (small blue text)",
    "instructors": "Instructors header + two name/email entries (left-aligned small text)",
    "logo":        "institutional Zewail City logo (teal panel + tiny Arabic/English text)",
}
for name, desc in REGIONS.items():
    p = pB.replace("NAME", name).replace("<one-line description of what the region contains>", desc)
    open(f"{QA}/crop_prompt_1_{name}.txt", "w", encoding="utf-8").write(p + "\n")
    print(f"banked crop_prompt_1_{name}.txt ({len(p)} chars)")

# also record the frozen-template provenance hashes for the report
import hashlib
print("payloadA sha256:", hashlib.sha256(payloadA.encode()).hexdigest()[:16])
print("payloadB sha256:", hashlib.sha256(payloadB.encode()).hexdigest()[:16])
