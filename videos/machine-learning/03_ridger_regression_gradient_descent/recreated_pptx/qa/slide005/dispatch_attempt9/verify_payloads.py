#!/usr/bin/env python3
"""Byte-fidelity check: attempt-9 banked judge payloads vs judge_protocol_03.md.

The deck's dispatch law requires every -p payload to be sourced byte-for-byte
from the frozen templates (only NNN/K/region-description substituted).
Copy-only: this script reads files and compares, it never rewrites payloads.
"""
import sys

VIDEO_DIR = ("/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/"
             "03_ridger_regression_gradient_descent")
Q = f"{VIDEO_DIR}/recreated_pptx/qa/slide005"
MD = f"{VIDEO_DIR}/shared_patterns/judge_protocol_03.md"

lines = open(MD, encoding="utf-8").read().split("\n")
A_line = B_line = None
for ln in lines:
    if ln.startswith('  -p "GROUND RULES') and "ZOOMED" not in ln:
        A_line = ln
    elif "ZOOMED CROP-PAIR" in ln and ln.lstrip().startswith('-p "'):
        B_line = ln
if A_line is None or B_line is None:
    sys.exit(f"template lines not found: A={A_line is not None} B={B_line is not None}")


def payload(line):
    assert line.startswith('  -p "') and line.endswith('"'), line[:40]
    return line[len('  -p "'):-1]


def norm(s):
    return s.rstrip("\n")


A_pay, B_pay = payload(A_line), payload(B_line)

fails = 0

got = open(f"{Q}/judge_prompt_9.txt", encoding="utf-8").read()
exp = A_pay.replace("slide NNN", "slide 005").replace("render_K", "render_9")
ok = norm(got) == norm(exp)
fails += not ok
print(f"[A] judge_prompt_9.txt          bytes_match={ok}  got={len(norm(got))}B exp={len(norm(exp))}B")
if not ok:
    for i, (x, y) in enumerate(zip(norm(got), norm(exp))):
        if x != y:
            print(f"    first diff @{i}: got={norm(got)[i-50:i+50]!r} exp={norm(exp)[i-50:i+50]!r}")
            break

for name in ("blue_upper", "eq_stack", "lower_eqs", "pink_band"):
    got = open(f"{Q}/crop_prompt_9_{name}.txt", encoding="utf-8").read()
    desc = norm(open(f"{Q}/crop_9_{name}_desc.txt", encoding="utf-8").read())
    exp = B_pay.replace("slide NNN", "slide 005").replace(
        "<one-line description of what the region contains>", desc)
    ok = norm(got) == norm(exp)
    fails += not ok
    print(f"[B] crop_prompt_9_{name:<10} bytes_match={ok}  got={len(norm(got))}B exp={len(norm(exp))}B")
    if not ok:
        a, b = norm(got), norm(exp)
        for i in range(min(len(a), len(b))):
            if a[i] != b[i]:
                print(f"    first diff @{i}: got={a[i-50:i+50]!r} exp={b[i-50:i+50]!r}")
                break
        else:
            print(f"    common prefix; length delta={len(a)-len(b)} tail={a[len(b):] or b[len(a):]!r}")

print("RESULT:", "ALL PAYLOADS BYTE-FAITHFUL" if fails == 0 else f"{fails} MISMATCH(ES)")
sys.exit(1 if fails else 0)
