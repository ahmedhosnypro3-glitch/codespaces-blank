#!/usr/bin/env bash
# Slide 048 — probe + Template A full-slide judge (attempt 7, render_9).
# Payload: qa/slide048/judge_prompt_1.txt (Template A bare body, md5 8fc119623b1f020c6d135c834969bf75; -p wrapper added here).
# Walls: probe timeout 150 / --timeout 120; legA outer timeout 1700, analyzer --timeout 1200.
# Gate law: refuse to dispatch at >=8 analyze_image.py procs.
set -u
cd /home/ahmed/Projects/ai_llm_slides
DECK="videos/machine-learning/03_ridger_regression_gradient_descent"
QA="$DECK/recreated_pptx/qa/slide048"
SCRIPT=".agents/skills/image-analysis/scripts/analyze_image.py"

n=$(pgrep -c -f '[a]nalyze_image.py' || echo 0)
echo "[048] $(date -u +%H:%M:%S) procs=$n"
if [ "${n:-0}" -ge 8 ]; then echo "[048] GATE BUSY — exit 75"; exit 75; fi

if [ "${1:-probe}" = "probe" ]; then
  scripts/16_vision_gate.sh timeout 150 python3 "$SCRIPT" analysis \
    "$QA/render_10.png" \
    --view "Slide 048 recreation attempt 8 — probe" \
    --capture "150dpi PNG render of a 13.33x7.5in PPTX" \
    --timeout 120 --rounds 1 --tries 1 \
    --transcript "$QA/probe_8.txt"
  exit $?
fi

scripts/16_vision_gate.sh timeout 1700 python3 "$SCRIPT" comparison \
  "$QA/render_10.png" \
  "$DECK/unique_slides/slide_048.jpg" \
  --view "Slide 048 recreation — fidelity check vs original lecture frame" \
  --capture "IMG1=150dpi PNG render of a 13.33x7.5in PPTX; IMG2=original lecture video frame" \
  --thinking high --max-tokens 65536 \
  --timeout 1200 --rounds 1 --tries 1 \
  --transcript "$QA/judge_attempt_8.txt" \
  -p "$(cat "$QA/judge_prompt_1.txt")"
