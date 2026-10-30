#!/usr/bin/env bash
# Slide 001 full-slide judge RE-DISPATCH (2026-10-20, worker w4-s001-20261020T1900).
# Rationale: the attempt-1 dispatch died BODYLESS at the frozen outer wall 1700s
# (two 630s HangError aborts, killed 440s into client attempt 3; the client's own
# 3-attempt abort ladder needs up to 3x630=1890s > 1700s). A bodyless death
# consumes no attempt (outage ruling + verdict law). This re-dispatch keeps EVERY
# judge parameter byte-identical to the frozen Template A of
# shared_patterns/judge_protocol_03.md and only sizes the outer wrapper (2000s)
# to the client's measured ladder, per the walls law ("outer wrapper > gate
# internal ladder > per-call --timeout").
set -u
export TMPDIR=/home/ahmed/Projects/ai_llm_slides/scratch/tmp
cd /home/ahmed/Projects/ai_llm_slides
QA=videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide001

scripts/16_vision_gate.sh timeout 2000 python3 \
  .agents/skills/image-analysis/scripts/analyze_image.py comparison \
  $QA/render_1.png \
  videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_001.jpg \
  --view "Slide 001 recreation — fidelity check vs original lecture frame" \
  --capture "IMG1=150dpi PNG render of a 13.33x7.5in PPTX; IMG2=original lecture frame" \
  --thinking high --max-tokens 65536 \
  --timeout 600 --rounds 1 --tries 1 \
  --transcript $QA/judge_attempt_1.txt \
  -p "$(cat $QA/judge_prompt_1.txt)"
