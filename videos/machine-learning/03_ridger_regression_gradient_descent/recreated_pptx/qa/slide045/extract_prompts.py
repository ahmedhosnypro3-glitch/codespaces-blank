#!/usr/bin/env python3
"""Extract Template A / B -p payloads from the frozen protocol and bank them for slide 045.

Substitutes ONLY NNN and K (and NAME / region description for B). Everything else
is byte-for-byte from shared_patterns/judge_protocol_03.md.
"""
import re

PROTO = "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/shared_patterns/judge_protocol_03.md"
QA = "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide045"

src = open(PROTO, encoding="utf-8").read()

# fenced code blocks
blocks = re.findall(r"```\n(.*?)```", src, re.S)
print("fenced blocks: %d" % len(blocks))

NNN, K = "045", "1"

# Template A payload = the -p "..." inside the comparison block (block index 2)
a_block = blocks[2]
m = re.search(r'-p "(.*?)"\s*$', a_block, re.S)
assert m, "Template A -p payload not found"
payload_a = m.group(1)
ncount = payload_a.count("NNN")
kcount = len(re.findall(r"\bK\b", payload_a))
print("Template A raw: %d chars, NNN=%d, K tokens=%d" % (len(payload_a), ncount, kcount))
if ncount:
    payload_a = payload_a.replace("NNN", NNN)
if kcount:
    payload_a = re.sub(r"\bK\b", K, payload_a)
open(QA + "/judge_prompt_1.txt", "w", encoding="utf-8").write(payload_a)
print("judge_prompt_1.txt: %d chars (NNN->%s x%d, K->%s x%d)" % (len(payload_a), NNN, ncount, K, kcount))

# Template B payload = block index 4
b_block = blocks[3]
m = re.search(r'-p "(.*?)"\s*$', b_block, re.S)
assert m, "Template B -p payload not found"
payload_b = m.group(1)
assert payload_b.count("NNN") == 1

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
    open(QA + "/crop_prompt_1_%s.txt" % name, "w", encoding="utf-8").write(p)
    print("crop_prompt_1_%s.txt: %d chars" % (name, len(p)))

# verify no placeholders remain
for f in ["judge_prompt_1.txt"] + ["crop_prompt_1_%s.txt" % n for n in REGIONS]:
    t = open(QA + "/" + f, encoding="utf-8").read()
    leftovers = [tok for tok in ("NNN", "NAME", "<one-line") if tok in t]
    print("  %-26s leftover placeholders: %s" % (f, leftovers or "none"))
