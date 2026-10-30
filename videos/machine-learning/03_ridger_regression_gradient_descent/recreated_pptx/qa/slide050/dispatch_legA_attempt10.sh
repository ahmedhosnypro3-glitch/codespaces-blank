#!/usr/bin/env bash
# Slide 050 — probe + Template A full-slide judge (attempt 10, render_12).
# render_12 = current pptx (c3441077588d779ecb0bb32df233c0ee) after the
# attempt-9 fix set: finalW construct + stop-text (renders 10/11) and the
# origin wedge + blue-square (1,2) fixes (render_12).
# Payload: qa/slide050/judge_payload_8.txt (Template A verbatim, md5 9387f5fbb94ef05a31db19f1e018dde1).
# Walls: probe timeout 150 / --timeout 120; legA outer timeout 1700, analyzer --timeout 1200.
set -u
cd /home/ahmed/Projects/ai_llm_slides
DECK="videos/machine-learning/03_ridger_regression_gradient_descent"
QA="$DECK/recreated_pptx/qa/slide050"
SCRIPT=".agents/skills/image-analysis/scripts/analyze_image.py"

n=$(pgrep -c -f '[a]nalyze_image.py' || echo 0)
echo "[050] $(date -u +%H:%M:%S) procs=$n"
if [ "${n:-0}" -ge 8 ]; then echo "[050] GATE BUSY — exit 75"; exit 75; fi

if [ "${1:-probe}" = "probe" ]; then
  scripts/16_vision_gate.sh timeout 150 python3 "$SCRIPT" analysis \
    "$QA/render_12.png" \
    --view "Slide 050 recreation attempt 10 — probe" \
    --capture "150dpi PNG render of a 13.33x7.5in PPTX" \
    --timeout 120 --rounds 1 --tries 1 \
    --transcript "$QA/probe_10.txt"
  exit $?
fi

scripts/16_vision_gate.sh timeout 1700 python3 "$SCRIPT" comparison \
  "$QA/render_12.png" \
  "$DECK/unique_slides/slide_050.jpg" \
  --view "Slide 050 recreation — fidelity check vs original lecture frame" \
  --capture "IMG1=150dpi PNG render of a 13.33x7.5in PPTX; IMG2=original lecture video frame" \
  --thinking high --max-tokens 65536 \
  --timeout 1200 --rounds 1 --tries 1 \
  --transcript "$QA/judge_attempt_10.txt" \
  -p "$(cat "$QA/judge_payload_8.txt")"
