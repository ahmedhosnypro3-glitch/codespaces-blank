#!/usr/bin/env python3
"""Bank the judge dispatch commands for slide 024 attempt 1, sourcing the `-p`
payloads BYTE-FOR-BYTE from shared_patterns/judge_protocol_03.md (substitute only
024 / K=1 / NAME / the region description) — the deck's frozen-template law.

Writes:
  qa/slide024/judge_prompt_1.txt              full-slide (Template A) comparison command
  qa/slide024/probe_prompt_1.txt              full-slide probe command
  qa/slide024/crop_prompt_1_<NAME>.txt        crop-pair (Template B) commands
Also prints each for a manual byte-check.
"""
import re

ROOT = "/home/ahmed/Projects/ai_llm_slides"
VDIR = f"{ROOT}/videos/machine-learning/03_ridger_regression_gradient_descent"
PROTO = f"{VDIR}/shared_patterns/judge_protocol_03.md"
QA = f"{VDIR}/recreated_pptx/qa/slide024"

NNN, K = "024", "1"

src = open(PROTO).read()
blocks = re.findall(r"```\n(.*?)```", src, re.S)
print(f"protocol fenced blocks: {len(blocks)}")


def find(pred):
    for b in blocks:
        if pred(b):
            return b.strip("\n")
    raise SystemExit("block not found")


probe = find(lambda b: "— probe" in b and "analysis" in b)
tmplA = find(lambda b: "fidelity check vs original lecture frame" in b and "comparison" in b)
tmplB = find(lambda b: "zoomed crop NAME" in b)
assert "--thinking high --max-tokens 65536" in tmplA and "--thinking high --max-tokens 65536" in tmplB


def sub(text, name=None, desc=None):
    # ONLY the protocol's declared placeholders are substituted: NNN, K, NAME,
    # and the crop-region description. Everything else stays byte-identical.
    t = text.replace("judge_attempt_K", "judge_attempt_1")
    t = t.replace("probe_K", "probe_1").replace("render_K", "render_1")
    t = t.replace("crop_K", f"crop_{K}")
    t = t.replace("attempt K", f"attempt {K}")
    t = t.replace("NNN", NNN)
    if name:
        t = t.replace("NAME", name)
    if desc:
        t = t.replace("<one-line description of what the region contains>", desc)
    return t


REGIONS = [
    ("title", "the title band: bold red 45pt 'Gradient Descent (GD)' incl. its two parentheses"),
    ("subtitles", "the two-line subtitle stack: 'and' (34pt) over 'How to apply to minimize Loss function' (30pt)"),
    ("icon", "the tiny bottom-center dark pen glyph (~16x17 frame px)"),
]

out = {
    f"{QA}/probe_prompt_1.txt": sub(probe),
    f"{QA}/judge_prompt_1.txt": sub(tmplA),
}
for name, desc in REGIONS:
    out[f"{QA}/crop_prompt_1_{name}.txt"] = sub(tmplB, name, desc)

for path, body in out.items():
    with open(path, "w") as f:
        f.write(body + "\n")
    print(f"\n=== {path.split('/')[-1]} ===")
    print(body)

# sanity: the -p payloads are present verbatim (a substitution only swapped the
# declared placeholders); assert no residual placeholder text survives.
for path, body in out.items():
    for bad in ("NNN", "crop_K", "NAME", "<one-line description"):
        if bad in body:
            raise SystemExit(f"{path}: residual placeholder '{bad}'")
print("\nall banked commands substituted; no residual placeholders")
