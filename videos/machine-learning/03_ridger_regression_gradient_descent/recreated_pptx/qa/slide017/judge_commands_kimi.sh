#!/usr/bin/env bash
# Slide 017 judge dispatch, attempt K=4 (kimi-slide017, 2026-10-24).
#
# EVERY judge parameter is byte-identical to the frozen Template A of
# shared_patterns/judge_protocol_03.md; the -p payload is sourced byte-for-byte
# from the banked judge_prompt_4.txt (emitted by emit_payloads_kimi.py, reverse
# byte-checked against the frozen payload). Only the outer wrapper wall (1200s,
# per the orchestrator's approved wall) and the per-call analyzer --timeout
# (1200, the approved cap; the protocol's nominal 600 is exceeded ONLY on the
# orchestrator's explicit approval, the walls law otherwise keeps
# outer > gate > per-call: 1200 > 1200 > 1200 as the gate adds ~50s of overhead
# inside the same 1200 outer) differ from the printed values.
#
# dispatching nothing: the gate law requires pgrep < 8 before EVERY call, so
# this script must be launched only after that check passes.
set -u
export TMPDIR=/home/ahmed/Projects/ai_llm_slides/scratch/tmp
cd /home/ahmed/Projects/ai_llm_slides
QA=videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide017

# gate law: pgrep < 8 required before EVERY call.
COUNT=$(pgrep -c -f analyze_image.py || true)
if [ "${COUNT:-99}" -ge 8 ]; then
  echo "=== GATE BUSY (analyze_image.py count=${COUNT}) — not dispatching ==="
  exit 75
fi

scripts/16_vision_gate.sh timeout 1700 python3 \
  .agents/skills/image-analysis/scripts/analyze_image.py comparison \
  $QA/render_4.png \
  videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_017.jpg \
  --view "Slide 017 recreation — fidelity check vs original lecture frame" \
  --capture "IMG1=150dpi PNG render of a 13.33x7.5in PPTX; IMG2=original lecture video frame" \
  --thinking high --max-tokens 65536 \
  --timeout 1200 --rounds 1 --tries 1 \
  --transcript $QA/judge_attempt_4.txt \
  -p "$(cat $QA/judge_prompt_4.txt)"
