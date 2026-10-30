#!/usr/bin/env python3
"""Slide 045: extract Procedure B -p payloads for the _r2 crop pairs.

Byte-for-byte from shared_patterns/judge_protocol_03.md Template B, substituting
ONLY NNN, K, NAME and the region description. Never re-typed or edited.
The old crop_prompt_1_*.txt (used by the stale attempt-1 pairs) stay banked.
"""
import re

PROTO = "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/shared_patterns/judge_protocol_03.md"
QA = "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide045"

src = open(PROTO, encoding="utf-8").read()
blocks = re.findall(r"```\n(.*?)```", src, re.S)
print("fenced blocks: %d" % len(blocks))

NNN, K = "045", "1"

b_block = blocks[3]
m = re.search(r'-p "(.*?)"\s*$', b_block, re.S)
assert m, "Template B -p payload not found"
payload_b = m.group(1)
assert payload_b.count("NNN") == 1, payload_b.count("NNN")

REGIONS = {
    "calcs": "calculation panel: six ruled rows of dotted-product arithmetic with two bracket column vectors per row",
    "toppanel": "top worked-example panel: data table x1..x6, Initial W bracket vector, Step eta, check-classes matrix and pointer arrow",
    "augtable": "augmented vectors table with class row",
}
for name, desc in REGIONS.items():
    p = payload_b.replace("NNN", NNN)
    p = re.sub(r"\bK\b", K, p)
    p = p.replace("NAME", name)
    p = p.replace("<one-line description of what the region contains>", desc)
    open(QA + "/crop_prompt_1%s_%s.txt" % ("_r2", name), "w", encoding="utf-8").write(p)
    print("crop_prompt_1_r2_%s.txt: %d chars" % (name, len(p)))

for name in REGIONS:
    t = open(QA + "/crop_prompt_1_r2_%s.txt" % name, encoding="utf-8").read()
    leftovers = [tok for tok in ("NNN", "NAME", "<one-line") if tok in t]
    print("  %-26s leftover placeholders: %s" % (name, leftovers or "none"))
