#!/usr/bin/env bash
# Slide 018 judge dispatch, attempt K=5 paren-refit re-cert (S22 fresh carrier, 2026-10-25).
#
# Corrected copy of qa/slide018/judge_commands_kimi_5.sh: that staged script
# carried slide 017's IMG2 (unique_slides/slide_017.jpg) and --view label from a
# copy-paste; the Template A full-slide judge for 018 must compare 018's render
# against 018's original frame. Payload source, all other judge parameters and
# the walls are unchanged from the staged script (byte-identical frozen Template
# A; --thinking high --max-tokens 65536; --timeout 1200 inside timeout 1700).
#
# dispatching nothing: the gate law requires pgrep < 8 before the call, so this
# script must be launched only after that check passes.
set -u
export TMPDIR=/home/ahmed/Projects/ai_llm_slides/scratch/tmp
cd /home/ahmed/Projects/ai_llm_slides
QA=videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide018

# gate law: pgrep < 8 required before the call.
COUNT=$(pgrep -c -f analyze_image.py || true)
if [ "${COUNT:-99}" -ge 8 ]; then
  echo "=== GATE BUSY (analyze_image.py count=${COUNT}) — not dispatching ==="
  exit 75
fi

scripts/16_vision_gate.sh timeout 1700 python3 \
  .agents/skills/image-analysis/scripts/analyze_image.py comparison \
  $QA/render_5.png \
  videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_018.jpg \
  --view "Slide 018 recreation — fidelity check vs original lecture frame" \
  --capture "IMG1=150dpi PNG render of a 13.33x7.5in PPTX; IMG2=original lecture video frame" \
  --thinking high --max-tokens 65536 \
  --timeout 1200 --rounds 1 --tries 1 \
  --transcript $QA/judge_attempt_5.txt \
  -p "$(cat $QA/judge_prompt_5.txt)"
