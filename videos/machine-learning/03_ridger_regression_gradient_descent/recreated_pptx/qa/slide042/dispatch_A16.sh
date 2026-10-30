#!/usr/bin/env bash
# Slide 042 leg A — full-slide comparison judge (Template A), attempt 16.
# Payload byte-for-byte from shared_patterns/judge_protocol_03.md Template A
# (no NNN/K substitutions needed in that payload; BLOCKER intact).
# Walls per orchestrator override: analyzer --timeout 1200 inside `timeout 1700`.
set -u
cd /workspaces/codespaces-blank/ai_llm_slides || exit 1
GATE="scripts/16_vision_gate.sh"
PY="python3 .agents/skills/image-analysis/scripts/analyze_image.py"
QA="videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide042"

# GATE LAW: back off at >=8 concurrent analyzers (count true analyzers only,
# so shell/wrapper processes matching the pattern don't inflate the number)
n=$(pgrep -f "python3 .*analyze_image.py" | wc -l)
if [ "${n:-0}" -ge 8 ]; then
  echo "GATE BUSY: $n analyze_image.py running — sleeping 240s"
  VIDEO=machine-learning/03_ridger_regression_gradient_descent \
    python3 scripts/15_progress.py heartbeat 42 w042-finish-20261024 || true
  sleep 240
fi

$GATE timeout 1700 $PY comparison \
  videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide042/render_16.png \
  videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_042.jpg \
  --view "Slide 042 recreation attempt 16 — fidelity check vs original lecture frame" \
  --capture "IMG1=150dpi PNG render of a 13.33x7.5in PPTX; IMG2=original lecture video frame" \
  --thinking high --max-tokens 65536 --timeout 1200 --rounds 1 --tries 1 \
  --transcript videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide042/judge_attempt_16.txt \
  -p "$(cat $QA/judge_prompt_16.txt)"
echo "LEG A EXIT=$?"
