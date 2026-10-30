#!/usr/bin/env python3
"""Independent re-derivation of slide 045's four frozen judge payloads.

Byte-for-byte from shared_patterns/judge_protocol_03.md. Substitution law:
  NNN -> 045   (exact token)
  K   -> 1     ONLY as \\bK\\b (a naive global K->N would corrupt "BLOCKER")
  NAME / region description (Template B only, per the protocol's own text)
The BLOCKER token is asserted intact in every payload.
"""
import hashlib
import os
import re
import sys

DECK = "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
PROTO = os.path.join(DECK, "shared_patterns", "judge_protocol_03.md")
QA = os.path.join(DECK, "recreated_pptx", "qa", "slide045")
OUT = os.path.join(QA, "payload_check_worker_legs5.txt")

NNN, K = "045", "1"
REGIONS = {
    "calcs": "calculation panel: six ruled rows of dotted-product arithmetic with two bracket column vectors per row",
    "toppanel": "top worked-example panel: data table x1..x6, Initial W bracket vector, Step eta, check-classes matrix and pointer arrow",
    "augtable": "augmented vectors table with class row",
}

src = open(PROTO, encoding="utf-8").read()
blocks = re.findall(r"```\n(.*?)```", src, re.S)
lines = []
ok = True

def emit(s):
    lines.append(s)

emit("Slide 045 independent payload re-derivation")
emit("protocol: %s" % PROTO)
emit("protocol md5: %s" % hashlib.md5(open(PROTO, "rb").read()).hexdigest())
emit("fenced blocks found: %d" % len(blocks))
emit("")

def check(label, expected, path):
    global ok
    actual = open(path, encoding="utf-8").read()
    e_md5 = hashlib.md5(expected.encode("utf-8")).hexdigest()
    a_md5 = hashlib.md5(actual.encode("utf-8")).hexdigest()
    same = expected == actual
    blocker_ok = "BLOCKER" in actual and "BLONCER" not in actual and "BL1CKER" not in actual
    nn_ok = "NNN" not in actual
    status = "BYTE-EXACT" if same else "MISMATCH"
    if not same or not blocker_ok or not nn_ok:
        ok = False
    emit("%-28s %-11s expected_md5=%s actual_md5=%s len=%d" % (label, status, e_md5, a_md5, len(actual)))
    emit("%-28s BLOCKER_intact=%s no_NNN_leftover=%s" % ("", blocker_ok, nn_ok))
    if not same:
        emit("    >>> FIRST DIFF:")
        for i, (a, b) in enumerate(zip(expected, actual)):
            if a != b:
                emit("    at char %d: expected %r actual %r" % (i, expected[i:i+60], actual[i:i+60]))
                break
        else:
            emit("    length differs: expected %d actual %d" % (len(expected), len(actual)))
    emit("")

# ---- Template A -------------------------------------------------------------
a_block = blocks[2]
m = re.search(r'-p "(.*?)"\s*$', a_block, re.S)
if not m:
    emit("ERROR: Template A -p payload not found")
    ok = False
else:
    pa = m.group(1)
    emit("Template A: raw payload chars=%d  NNN_count=%d  standalone_K_count=%d"
         % (len(pa), pa.count("NNN"), len(re.findall(r"\bK\b", pa))))
    # BLOCKER guard: count standalone K tokens only; BLOCKER's K is never standalone
    pa2 = pa.replace("NNN", NNN)
    pa2 = re.sub(r"\bK\b", K, pa2)
    check("judge_prompt_1.txt", pa2, os.path.join(QA, "judge_prompt_1.txt"))

# ---- Template B -------------------------------------------------------------
b_block = blocks[3]
m = re.search(r'-p "(.*?)"\s*$', b_block, re.S)
if not m:
    emit("ERROR: Template B -p payload not found")
    ok = False
else:
    pb = m.group(1)
    emit("Template B: raw payload chars=%d  NNN_count=%d  standalone_K_count=%d  NAME_count=%d"
         % (len(pb), pb.count("NNN"), len(re.findall(r"\bK\b", pb)), pb.count("NAME")))
    for name, desc in REGIONS.items():
        p = pb.replace("NNN", NNN)
        p = re.sub(r"\bK\b", K, p)
        p = p.replace("NAME", name)
        p = p.replace("<one-line description of what the region contains>", desc)
        check("crop_prompt_1_r2_%s.txt" % name, p, os.path.join(QA, "crop_prompt_1_r2_%s.txt" % name))

# ---- explicit BLOCKER / naive-substitution guard ---------------------------
emit("Substitution guard:")
a_txt = open(os.path.join(QA, "judge_prompt_1.txt"), encoding="utf-8").read()
b_txt = open(os.path.join(QA, "crop_prompt_1_r2_calcs.txt"), encoding="utf-8").read()
for lbl, t in (("judge_prompt_1.txt", a_txt), ("crop_prompt_1_r2_calcs.txt", b_txt)):
    blk = t.count("BLOCKER")
    naive = t.count("BL1CKER") + t.count("BLONCER")
    emit("  %-28s BLOCKER_count=%d naive-corruption_count=%d" % (lbl, blk, naive))
    if blk == 0 or naive:
        ok = False
emit("")
emit("RESULT: %s" % ("ALL PAYLOADS BYTE-EXACT + BLOCKER INTACT" if ok else "FAIL"))

txt = "\n".join(lines) + "\n"
open(OUT, "w", encoding="utf-8").write(txt)
print(txt)
sys.exit(0 if ok else 1)
