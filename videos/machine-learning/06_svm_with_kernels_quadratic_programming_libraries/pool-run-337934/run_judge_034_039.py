#!/usr/bin/env python3
# Visual judge for slides 034-039 (worker scope_034_039).
# Image order: render FIRST, original SECOND (template labels [1]=recreation, [2]=original).
# Patient timeouts: the gateway queue is deep with ~30 concurrent workers.
import subprocess, os, re, sys

BASE = "/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries"
ANALYZE = "/home/codespace/ai_llm_slides/.agents/skills/image-analysis/scripts/analyze_image.py"
TEMPLATE = open(os.path.join(BASE, "judge_template.txt")).read()

SLIDES = [int(x) for x in (sys.argv[1:] or ["34", "35", "36", "37", "38", "39"])]
ATTEMPT = int(os.environ.get("ATTEMPT", "2"))   # base attempt index for every slide
SUMMARY = []

for num in SLIDES:
    ss = f"{num:03d}"
    qadir = os.path.join(BASE, "recreated_pptx", "qa", f"slide{ss}")
    render = os.path.join(qadir, f"render_{ATTEMPT}.png")
    original = os.path.join(BASE, "unique_slides", f"slide_{ss}.jpg")
    out_file = os.path.join(qadir, f"transcript_{ss}_judge{ATTEMPT}.txt")

    if not (os.path.exists(render) and os.path.exists(original)):
        print(f"[{ss}] MISSING render {render}", flush=True)
        SUMMARY.append((ss, "MISSING")); continue

    prompt = f"""You are a visual judge comparing a RECREATED PPTX slide render against the ORIGINAL lecture frame.

VIEW: Slide {num} — SVM / kernels / QP lecture frame recreation
CAPTURE: [1] Recreated render (150dpi LibreOffice PPTX render) — file: {render}
         [2] Original lecture frame — file: {original}

IMPORTANT: image [1] is the RECREATION, image [2] is the ORIGINAL. Do not swap them.

FACTS (measured ground truth from the ORIGINAL):
- House frame: outer red frame at x=0.15, y=0.15, w=13.03, h=7.2 (0.15in inset), border C00000 width 1.5
- Badge: yellow circle at x=12.48, y=0.30, w=0.5, h=0.5, fill FFF9C4, centered bold numeral {num}, color 333333, 18pt
- Title: text box at y=0.28, x=0.6, w=12.13, centered
- These are MANDATORY house chrome and override any visual difference in the original.

{TEMPLATE}

COMPARISON TASK:
This lecture slide is primarily TEXT + EQUATIONS + BOXES. Compare:
- every text block verbatim (titles, bullets, labels, parenthetical notes);
- every equation's CONTENT and structure (symbols, subscripts/superscripts, summation limits, fractions);
- boxes/panels: presence, fill, border colors, and that enclosed content stays inside its box;
- color coding of math terms (e.g. blue variables, red coefficients/highlights, green Z) as in the original;
- overall layout order and alignment of the regions.
Ignore: house chrome differences, mouse cursors/video artifacts, letterbox bars, and the
substitution of 2D typeset equation images for inline/linear equation text.

VERDICT: PASS or FAIL for faithful usable content match

Output format:
## 1. LAYOUT MAP
[describe both images content layout]
## 2. CONTENT FIDELITY
[compare text, equations, boxes, colors]
## 3. DEFECT LIST
[list every discrepancy with severity BLOCKER/MAJOR/MINOR and confidence]
## 4. VERDICT
"""

    print(f"[{ss}] judging (attempt {ATTEMPT}) ...", flush=True)
    try:
        proc = subprocess.run(
            [ANALYZE, "comparison", render, original, "-p", prompt,
             "--timeout", "1200", "--rounds", "1", "--tries", "1"],
            cwd=BASE, capture_output=True, text=True, timeout=1800,
        )
    except subprocess.TimeoutExpired:
        print(f"[{ss}] SUBPROCESS TIMEOUT", flush=True)
        with open(out_file, "w") as fh:
            fh.write("TIMEOUT: the vision gateway did not answer within 1800s "
                     "(saturated by concurrent workers). Re-judge.\n")
        SUMMARY.append((ss, "TIMEOUT")); continue

    out = (proc.stdout or "") + (proc.stderr or "")
    with open(out_file, "w") as fh:
        fh.write(out)
    verdict = "FAIL"
    for m in re.finditer(r"^\*\*?## ?4\..*$|^## ?4\..*$", out, re.M):
        verdict = "?" ; break
    v = re.search(r"##\s*4\.?\s*VERDICT(.{0,400})", out, re.S | re.I)
    if v:
        vtext = v.group(1).upper()
        if re.search(r"\bFAIL\b", vtext):
            verdict = "FAIL"
        elif re.search(r"\bPASS\b", vtext):
            verdict = "PASS"
    print(f"[{ss}] verdict={verdict}", flush=True)
    SUMMARY.append((ss, verdict))

print("\n=== SUMMARY ===")
for ss, v in SUMMARY:
    print(f"  slide_{ss}: {v}")
