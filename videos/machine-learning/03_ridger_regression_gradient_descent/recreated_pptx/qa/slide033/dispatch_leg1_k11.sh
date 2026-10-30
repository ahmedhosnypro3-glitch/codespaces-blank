#!/bin/bash
# Leg 1 — Template A full-slide judge, slide 033, attempt 11 (render_11).
# Payload: judge_payload_A_k9.txt — byte-for-byte from
#   shared_patterns/judge_protocol_03.md Template A (protocol line 71);
#   md5 9387f5fbb94ef05a31db19f1e018dde1, len 4139 (unchanged; attempt
#   numbering lives only in filenames/transcript paths/--view).
# Lane wall (orchestrator directive 2026-10-24, supersedes the protocol's 600):
#   analyzer --timeout 1200, inside `timeout 1700`, --rounds 1 --tries 1,
#   --thinking high --max-tokens 65536. No retry loops around this gate.
set -u
cd /workspaces/codespaces-blank/ai_llm_slides || exit 1
Q=videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide033
V=videos/machine-learning/03_ridger_regression_gradient_descent

bash scripts/16_vision_gate.sh timeout 1700 python3 \
  .agents/skills/image-analysis/scripts/analyze_image.py comparison \
  $Q/render_11.png $V/unique_slides/slide_033.jpg \
  --view "Slide 33 recreation — fidelity check vs original lecture frame" \
  --capture "IMG1=150dpi PNG render of a 13.33x7.5in PPTX; IMG2=original lecture video frame" \
  --thinking high --max-tokens 65536 \
  --timeout 1200 --rounds 1 --tries 1 \
  --transcript $Q/judge_attempt_11.txt \
  -p "$(cat $Q/judge_payload_A_k9.txt)"
echo "LEG1_GATE_EXIT=$?"
