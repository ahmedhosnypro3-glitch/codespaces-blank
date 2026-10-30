#!/usr/bin/env python3
"""Bank slide 038's attempt-1 judge prompts by extracting the -p payloads
BYTE-FOR-BYTE from the frozen shared_patterns/judge_protocol_03.md, then
substituting only NNN=038, K=1, NAME and the region description.

Also writes the exact Bash commands to run, so what is dispatched is provably
what was banked (no hand-typed payloads anywhere).
"""
import re, pathlib

ROOT = pathlib.Path("/home/ahmed/Projects/ai_llm_slides")
PROTO = (ROOT / "videos/machine-learning/03_ridger_regression_gradient_descent"
              / "shared_patterns/judge_protocol_03.md").read_text()
QA = ROOT / "videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide038"

blocks = re.findall(r"```\n(.*?)\n```", PROTO, re.S)
tplA, tplB = blocks[2], blocks[3]          # comparison blocks (A and B)
N, K = "038", 1
RENDER = "render_3.png"                     # the current, verified post-fix render

# ---- Template A ------------------------------------------------------------------
a = tplA.replace("slideNNN", "slide038").replace("render_K.png", RENDER)
a = a.replace("judge_attempt_K.txt", "judge_attempt_1.txt")
assert "slideNNN" not in a and "render_K" not in a and "_K.txt" not in a

# ---- Template B, per crop region -------------------------------------------------
REGIONS = {
    "title_l1l2": ("crop_1_title_l1l2_render.png", "crop_1_title_l1l2_orig.png",
                   "lines 1 and 2 of the three-line title block: 'Gradient Descent' in "
                   "dark red followed by '(GD)' in blue, and the 'vs' line in dark red below"),
    "title_l3": ("crop_1_title_l3_render.png", "crop_1_title_l3_orig.png",
                 "line 3 of the title block: 'Stochastic' and 'Gradient Descent' in dark red "
                 "followed by '(SGD)' in blue"),
    "badge": ("crop_1_badge_render.png", "crop_1_badge_orig.png",
              "the yellow slide-number badge circle with its purple ring and the bold numeral '38'"),
}

HEAD = f"""================================================================================
SLIDE 038 — VISUAL JUDGE DISPATCH PACK, ATTEMPT {K} (w4-s038, 2026-10-20)
================================================================================
Protocol law (shared_patterns/judge_protocol_03.md): the -p payload below is
extracted programmatically from the frozen template and byte-for-byte identical
to it except for the substitutions NNN=038, K={K}, NAME and the one-line region
description. Vision route: DEFAULT (no --models flag). Thinking high,
--max-tokens 65536. Outer wall: timeout 1700. Inner --timeout 600.

ATTEMPT LEDGER (no judge evidence existed before this dispatch):
  judge attempts used before this pack: 0  (selfcheck/crop/geometry work only)
  this dispatch = judge attempt {K}

RENDER BEING JUDGED: {QA}/{RENDER}
  (byte-identical, md5 412885247ca5e60a7e4eb0b447d3ad5f, to render_2.png; verified on
  2026-10-20 as a fresh LibreOffice re-render of the CURRENT deliverable
   slide_038_recreated.pptx — the rebuild is pixel-identical: 0/2251125 px differ.)
  render_1.png is the PRE-FIX render (attempt-1 build, failed selfcheck) and is kept
  as lineage evidence; it is NOT judged here.

CERTIFICATION NEEDS BOTH LEGS (founder directive 2026-10-19, ALL slides zoomed):
  LEG A  Template A — full-slide comparison
  LEG B  Template B — zoomed crop-pairs, one per dense region: title_l1l2, title_l3, badge

--------------------------------------------------------------------------------
LEG A — TEMPLATE A, FULL-SLIDE COMPARISON (attempt 1)
--------------------------------------------------------------------------------

PROBE FIRST (opens the gateway window; a valid body opens it, a hang means sleep 300
and re-probe ONCE — this is a probe, NOT a judge attempt):

cd /home/ahmed/Projects/ai_llm_slides && scripts/16_vision_gate.sh timeout 150 python3 \\
  .agents/skills/image-analysis/scripts/analyze_image.py analysis \\
  videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide038/{RENDER} \\
  --view "Slide 038 recreation attempt 1 — probe" \\
  --capture "150dpi PNG render of a 13.33x7.5in PPTX" \\
  --timeout 120 --rounds 1 --tries 1 \\
  --transcript videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide038/probe_1.txt

COMPARISON (the real judge — execute exactly this):

{a}

"""

out = [HEAD]
# ---- LEG B blocks ----------------------------------------------------------------
b_head = []
for i, (name, (rp, op, desc)) in enumerate(REGIONS.items()):
    b = tplB.replace("slideNNN", "slide038")
    b = b.replace("crop_K_NAME_render.png", rp).replace("crop_K_NAME_orig.png", op)
    b = b.replace("crop_K_NAME_judge.txt", f"crop_1_{name}_judge.txt")
    b = b.replace("attempt K", "attempt 1")
    b = b.replace("<one-line description of what the region contains>", desc)
    assert "slideNNN" not in b and "crop_K" not in b and "attempt K" not in b and "<one-line" not in b, name
    b_head.append(f"""--------------------------------------------------------------------------------
LEG B.{i+1} — TEMPLATE B, ZOOMED CROP-PAIR '{name}' (attempt 1)
--------------------------------------------------------------------------------

{b}

""")
out.append("""--------------------------------------------------------------------------------
LEG B — TEMPLATE B, ZOOMED CROP-PAIR CERTIFICATES (attempt 1)
--------------------------------------------------------------------------------
Procedure B compliance (judge_protocol_03.md):
  * regions picked from the ORIGINAL frame (960x540): the slide's dense regions are the
    three-line title block (its only content) split into title_l1l2 + title_l3, plus the
    badge small-text cluster. Minimum one per dense region: satisfied.
  * both images cropped at the SAME slide-space region; original upscaled LANCZOS to the
    render crop's EXACT pixel size, so output_px/frame_px is identical on BOTH axes
    (verified in cut_crops_1.out: 1667x306 / 1667x134 / 88x88, MATCH=OK on every region).
  * banked as crop_1_<name>_render.png + crop_1_<name>_orig.png under qa/slide038/.
  * title_l3's bottom edge is frame y=378 — it stops at L3's ink bottom (y1=376) so the
    mouse-cursor video artifact at x687..698, y378..388 in the original is not presented
    as a recreation difference (founder law: cursors are correctly omitted).
  * findings map back to slide space via crop-relative coords x crop scale before any edit.

""")
out.extend(b_head)
(QA / "judge_prompt_1.txt").write_text("".join(out))
print(f"judge_prompt_1.txt written: {len(''.join(out))} bytes")
# sanity: payload uniqueness / no leftover placeholders
tail = "".join(out)
for ph in ["slideNNN", "render_K", "crop_K", "attempt K", "<one-line", "_K.txt"]:
    print(f"  leftover '{ph}': {tail.count(ph)}")
