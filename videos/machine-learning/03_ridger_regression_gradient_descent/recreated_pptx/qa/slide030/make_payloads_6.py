#!/usr/bin/env python3
"""Extract judge payloads BYTE-FOR-BYTE from shared_patterns/judge_protocol_03.md.

Only protocol substitutions are applied:
  Template A (full slide): slideNNN -> slide030 in paths; render_K -> render_6.
  Template B (crop pairs): slideNNN -> slide030; crop_K_NAME_* -> crop_6_<name>_*;
                           transcript crop_K_NAME_judge -> crop_6_<name>_judge;
                           --view/--capture NAME -> crop slug; <region desc> -> desc.
The -p payload body is copied verbatim from the protocol (NNN->030 only) and the
result is byte-checked against the template: every difference must be a permitted
substitution token.
"""
import re

PROTO = "videos/machine-learning/03_ridger_regression_gradient_descent/shared_patterns/judge_protocol_03.md"
QA = "videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide030"
NNN, K = "030", "6"

text = open(PROTO).read()
fences = re.findall(r"```\n(.*?)```", text, re.S)
print(f"fences in protocol: {len(fences)}")

# ---- find the Template A and Template B command fences
a_cmd = b_cmd = None
for f in fences:
    if "Template A" in f or ("analysis" in f and "comparison" in f):
        pass
# simpler: locate by their distinctive markers
for f in fences:
    if "recreation attempt K — probe" in f:
        continue
    if "IMG2=original lecture video frame" in f:
        a_cmd = f
    if "matched scale (attempt K)" in f:
        b_cmd = f
assert a_cmd, "Template A command fence not found"
assert b_cmd, "Template B command fence not found"

# ---------------- Template A: substitute paths, keep -p verbatim (no NNN in body)
a_out = a_cmd.replace("slideNNN", "slide030").replace("render_K", f"render_{K}")
a_payload = re.search(r'-p "(.*)"\n?$', a_out, re.S).group(1)
a_out = a_out[: a_out.index('-p "')] + f'-p "{a_payload}"\n'
open(f"{QA}/judge_prompt_6.txt", "w").write(a_payload + "\n")
print(f"Template A payload: {len(a_payload)} bytes -> {QA}/judge_prompt_6.txt")

# ---------------- Template B: per-crop payloads
regions = {
    "iter_left":  "iteration table left half: x/f(x)/x-delta/f(x-delta) label and value cells",
    "iter_right": "iteration table right half: x+delta/f(x+delta)/slope/next x value cells",
    "formula":    "red equation box f(x)=(x-5)^2+1 plus green box X=5 and f(x) Minimum value is 1.0",
    "plot":       "graph: parabola, red dashed x=5, black secant with three dots, point and tick labels",
    "param":      "small parameter table: step/0.2, initial X/3, delta/0.1",
    "callout":    "purple filled callout: Reach Minimum after 11 Steps",
    "arrow":      "red block arrow pointing down toward the iteration table",
}
b_tmpl_payload = re.search(r'-p "(.*)"\n?$', b_cmd, re.S).group(1)
open(f"{QA}/judge_prompt_B_template.txt", "w").write(b_tmpl_payload + "\n")
print(f"Template B template payload: {len(b_tmpl_payload)} bytes")

for name, desc in regions.items():
    cmd = (b_cmd.replace("slideNNN", "slide030")
               .replace(f"crop_K_{name.upper()}_render", f"crop_{K}_{name}_render")
               .replace("crop_K_NAME_render", f"crop_{K}_{name}_render")
               .replace("crop_K_NAME_orig", f"crop_{K}_{name}_orig")
               .replace("crop_K_NAME_judge", f"crop_{K}_{name}_judge")
               .replace("Slide NNN zoomed crop NAME", f"Slide {NNN} zoomed crop {name}")
               .replace("attempt K", f"attempt {K}")
               .replace("<one-line description of what the region contains>", desc))
    payload = re.search(r'-p "(.*)"\n?$', cmd, re.S).group(1)
    # standing law substitution inside the payload body: slide NNN -> slide 030
    payload = payload.replace("slide NNN", "slide 030")
    assert "slide NNN" not in payload and "NNN" not in payload, f"unsubstituted NNN in {name}"
    open(f"{QA}/crop_prompt_6_{name}.txt", "w").write(payload + "\n")
    open(f"{QA}/crop_6_{name}_cmd.txt", "w").write(cmd)
    print(f"  crop {name:11s} payload {len(payload)} bytes -> crop_prompt_6_{name}.txt")

# ---------------- byte-verification: every diff vs the template is a permitted token
def check_diff(orig, new, allowed):
    """Assert new == orig with only <allowed> token->replacement pairs applied.

    Compares line-by-line: a changed line must be obtainable from the template line
    by applying exactly one allowed (token -> replacement) pair.
    """
    olines = orig.split("\n")
    nlines = new.split("\n")
    if len(olines) != len(nlines):
        print("    !! LINE COUNT DIFFERS")
        return False
    ok = True
    for lo, ln in zip(olines, nlines):
        if lo == ln:
            continue
        # try every combination of allowed pairs (order matters for overlapping tokens)
        cands = [lo]
        for tok, rep in allowed:
            nxt = []
            for c in cands:
                if tok in c:
                    nxt.append(c.replace(tok, rep))
                    nxt.append(c)  # keep unapplied too
                else:
                    nxt.append(c)
            cands = nxt
        if ln not in cands:
            print(f"    !! UNPERMITTED LINE CHANGE:\n       TEMPLATE: {lo!r}\n       NEW:      {ln!r}")
            ok = False
    return ok

print("\n== byte verification of substitutions ==")
checks = []
A_ALLOWED = [("slideNNN", "slide030"), ("NNN", "030"), ("render_K", f"render_{K}"), ("K", K)]
checks.append(("TemplateA paths", check_diff(a_cmd, a_out, A_ALLOWED)))
b_ref = b_cmd
for name in regions:
    cmd = open(f"{QA}/crop_6_{name}_cmd.txt").read()
B_ALLOWED = [
    ("slide NNN", "slide 030"), ("slideNNN", "slide030"), ("NNN", "030"),
    ("crop_K_NAME_render", f"crop_{K}_{name}_render"),
    ("crop_K_NAME_orig", f"crop_{K}_{name}_orig"),
    ("crop_K_NAME_judge", f"crop_{K}_{name}_judge"),
    ("NAME", name), ("K", K),
    ("<one-line description of what the region contains>", regions[name]),
]
checks.append((f"TemplateB {name}", check_diff(b_ref, cmd, B_ALLOWED)))
# payload bodies: Template A has no NNN; Template B body: slide NNN -> slide 030 only
b_ref_payload = b_tmpl_payload
for name in regions:
    p = open(f"{QA}/crop_prompt_6_{name}.txt").read().rstrip("\n")
    ok = check_diff(b_ref_payload, p, [("NNN", "030")])
    ok = ok and ("slide NNN" not in p) and ("NNN" not in p) and ("BLOCKER" in p) and ("FINAL VERDICT" in p)
    checks.append((f"payload {name}", ok))
a_ref_payload = re.search(r'-p "(.*)"\n?$', a_cmd, re.S).group(1)
ok = check_diff(a_ref_payload, a_payload, []) and ("NNN" not in a_payload) and ("BLOCKER" in a_payload) and ("FINAL VERDICT" in a_payload)
checks.append(("payload A", ok))

for name, ok in checks:
    print(f"  {'PASS' if ok else 'FAIL'}  {name}")
print("\nALL BYTE CHECKS PASS" if all(ok for _, ok in checks) else "\nBYTE CHECK FAILURES PRESENT")
