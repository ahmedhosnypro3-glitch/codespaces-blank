#!/usr/bin/env python3
"""Generate the byte-for-byte judge payloads for slide 032 attempt 10.

Payloads are EXTRACTED from the frozen fenced blocks in
shared_patterns/judge_protocol_03.md (Template A = lines 62..71, Template B =
lines 108..117) precisely as the text between `-p "` and the closing quote, so
only the GROUND RULES text is sent as the prompt. The command lines are rebuilt
explicitly with the runbook's own substitutions.

Substitutions actually needed:
  payload A : none (its GROUND RULES text carries no NNN//workspaces/codespaces-blank/ai_llm_slides placeholder)
  payload B : "slide NNN" -> "slide 032"   (the only placeholder in the text)
  commands  : slideNNN/slide_NNN -> slide032/slide_032 ; render_K -> render_10 ;
              judge_attempt_K -> judge_attempt_10 ; crop_K_NAME -> crop_10_<slug> ;
              Slide NNN [zoomed crop NAME] -> Slide 032 [...] ; (attempt /workspaces/codespaces-blank/ai_llm_slides) -> (attempt 10) ;
              <one-line description ...> -> the region text
verify_prompts_9.py re-derives the payload from the protocol and asserts equality.
"""
import difflib
import re

DECK = "/worksp" "aces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
PROTO = DECK + "/shared_patterns/judge_protocol_03.md"
QA = DECK + "/recreated_pptx/qa/slide032"
/workspaces/codespaces-blank/ai_llm_slides = 10
ROOT = "/worksp" "aces/codespaces-blank/ai_llm_slides"
REL = "videos/machine-learning/03_ridger_regression_gradient_descent"

fs = open(PROTO, encoding="utf-8").read().split("\n")
BLOCK_A = "\n".join(fs[61:71])
BLOCK_B = "\n".join(fs[107:117])


def payload_of(block):
    i = block.index('-p "') + 4
    body = block[i:]
    assert body.endswith('"'), "fenced block does not close the -p quote"
    return body[:-1]


PAY_A = payload_of(BLOCK_A)
PAY_B = payload_of(BLOCK_B)
assert PAY_A.startswith("GROUND RULES"), PAY_A[:60]
assert PAY_B.startswith("GROUND RULES"), PAY_B[:60]
print("payload A chars:", len(PAY_A), "| placeholders present:",
      {t: (t in PAY_A) for t in ("NNN", "/workspaces/codespaces-blank/ai_llm_slides", "slide_NNN")})
print("payload B chars:", len(PAY_B), "| placeholders present:",
      {t: (t in PAY_B) for t in ("NNN", "/workspaces/codespaces-blank/ai_llm_slides", "slide_NNN", "NAME")})


def show_diff(a, b, label):
    d = list(difflib.unified_diff(a.split("\n"), b.split("\n"),
                                  fromfile="protocol:" + label, tofile="generated:" + label,
                                  lineterm="", n=0))
    print("\n".join(d) if d else f"  (no diff) {label}")


# ------------------------------------------------------------------ Template A
A = PAY_A.replace("slide NNN", "slide 032")
show_diff(PAY_A, A, "Template A payload")

CMD_A = (
    f"cd {ROOT} && scripts/16_vision_gate.sh timeout 1700 python3 \\\n"
    "  .agents/skills/image-analysis/scripts/analyze_image.py comparison \\\n"
    f"  {REL}/recreated_pptx/qa/slide032/render_10.png \\\n"
    f"  {REL}/unique_slides/slide_032.jpg \\\n"
    '  --view "Slide 032 recreation — fidelity check vs original lecture frame" \\\n'
    '  --capture "IMG1=150dpi PNG render of a 13.33x7.5in PPTX; IMG2=original lecture video frame" \\\n'
    "  --thinking high --max-tokens 65536 \\\n"
    "  --timeout 600 --rounds 1 --tries 1 \\\n"
    f"  --transcript {REL}/recreated_pptx/qa/slide032/judge_attempt_10.txt \\\n"
    '  -p "' + A + '"\n'
)
assert CMD_A.count('-p "') == 1 and CMD_A.startswith("cd " + ROOT)
assert "render_10.png" in CMD_A and "slide_032.jpg" in CMD_A and "judge_attempt_10.txt" in CMD_A
open(QA + "/judge_prompt_10.txt", "w", encoding="utf-8").write(CMD_A)
print("  wrote judge_prompt_10.txt")

# ------------------------------------------------------------------ Template B
REGIONS = [
    ("title", "three-run one-line title: red 'Convex Function,' green 'Learning Rate =0.4,' blue 'Start at X=3'"),
    ("params", "parameter table: step 0.4 / initial X 3 / delta 0.1, three full-width coloured rows"),
    ("graph", "plot box of f(x)=(x-5)^2+1: blue quadratic curve, gridlines, gray axes with tick labels, red vertical at x=5, black y=10 chord, green point (5,1), red point, point labels '(2, 10)' '(7, 7)' '(5, 1)' and two segment '3' labels"),
    ("callouts", "equation callout stack: red-bordered equation box, green EFFFE2 box with 'X = 5' and 'f(x) Minimum value is 1.0', pink F7C9FB 'Reach Minimum after 6 Steps' band, white crimson-outlined down-arrow"),
    ("table", "iteration table: 5 colour bands holding 8 rows (x, f(x), x-delta, f(x-delta), x+delta, f(x+delta), slope, next x) x 6 data columns, 564BA7 outer frame"),
]

for name, desc in REGIONS:
    B = PAY_B.replace("slide NNN", "slide 032")
    show_diff(PAY_B, B, f"Template B payload ({name})")
    cmd = (
        f"cd {ROOT} && scripts/16_vision_gate.sh timeout 1700 python3 \\\n"
        "  .agents/skills/image-analysis/scripts/analyze_image.py comparison \\\n"
        f"  {REL}/recreated_pptx/qa/slide032/crop_10_{name}_render.png \\\n"
        f"  {REL}/recreated_pptx/qa/slide032/crop_10_{name}_orig.png \\\n"
        f'  --view "Slide 032 zoomed crop {name} — render vs original at matched scale (attempt 10)" \\\n'
        f'  --capture "IMG1=zoomed crop of a 150dpi PPTX render; IMG2=the SAME slide-space region cropped from the original lecture frame and upscaled to match IMG1\'s effective scale; region: {desc}" \\\n'
        "  --thinking high --max-tokens 65536 \\\n"
        "  --timeout 600 --rounds 1 --tries 1 \\\n"
        f"  --transcript {REL}/recreated_pptx/qa/slide032/crop_10_{name}_judge.txt \\\n"
        '  -p "' + B + '"\n'
    )
    assert cmd.count('-p "') == 1 and cmd.startswith("cd " + ROOT)
    assert f"crop_10_{name}_render.png" in cmd and f"crop_10_{name}_orig.png" in cmd
    open(QA + f"/crop_10_{name}_prompt.txt", "w", encoding="utf-8").write(cmd)
    print(f"  wrote crop_10_{name}_prompt.txt")
