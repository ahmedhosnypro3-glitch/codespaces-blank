#!/usr/bin/env bash
# Slide 034 — attempt-27 final judge dispatch (post plot-tick fix).
# Chained: W4 sleep 300 + ONE re-probe, then all four legs on the new render_27.png.
# Payloads banked byte-for-byte from shared_patterns/judge_protocol_03.md
#   payload_A_27.txt  = Template A (full-slide)
#   payload_B_27.txt  = Template B (crop pair; region description goes in --capture only)
set -u
cd /home/codespace/ai_llm_slides
export TMPDIR=/home/codespace/ai_llm_slides/scratch/tmp
mkdir -p "$TMPDIR"
B=videos/machine-learning/03_ridger_regression_gradient_descent
QA="$B/recreated_pptx/qa/slide034"
LOG="$TMPDIR/w034_att27_final"
mkdir -p "$LOG"

echo "=== W4: sleep 300 then ONE re-probe ===" | tee -a "$LOG/chain.log"
sleep 300
timeout 150 bash scripts/16_vision_gate.sh python3 \
  .agents/skills/image-analysis/scripts/analyze_image.py analysis \
  "$QA/render_27.png" \
  --view "Slide 034 recreation attempt 27 — probe" \
  --capture "150dpi PNG render of a 13.33x7.5in PPTX" \
  --timeout 120 --rounds 1 --tries 1 \
  --transcript "$QA/probe_27.txt" >>"$LOG/probe_27.log" 2>&1
echo "probe rc=$?" | tee -a "$LOG/chain.log"

echo "=== LEG A: full-slide Template A ===" | tee -a "$LOG/chain.log"
timeout 1700 bash scripts/16_vision_gate.sh python3 \
  .agents/skills/image-analysis/scripts/analyze_image.py comparison \
  "$QA/render_27.png" \
  "$B/unique_slides/slide_034.jpg" \
  --view "Slide 034 recreation — fidelity check vs original lecture frame" \
  --capture "IMG1=150dpi PNG render of a 13.33x7.5in PPTX; IMG2=original lecture video frame" \
  --thinking high --max-tokens 65536 \
  --timeout 600 --rounds 1 --tries 1 \
  --transcript "$QA/judge_attempt_27.txt" \
  -p "$(cat "$QA/payload_A_27.txt")" >>"$LOG/legA.log" 2>&1
echo "legA rc=$?" | tee -a "$LOG/chain.log"

crop_leg () {
  NAME="$1"; DESC="$2"; TRANSCRIPT="$3"
  echo "=== LEG crop ${NAME} ===" | tee -a "$LOG/chain.log"
  timeout 1700 bash scripts/16_vision_gate.sh python3 \
    .agents/skills/image-analysis/scripts/analyze_image.py comparison \
    "$QA/crop_27_${NAME}_render.png" \
    "$QA/crop_27_${NAME}_orig.png" \
    --view "Slide 034 zoomed crop ${NAME} — render vs original at matched scale (attempt 27)" \
    --capture "IMG1=zoomed crop of a 150dpi PPTX render; IMG2=the SAME slide-space region cropped from the original lecture frame and upscaled to match IMG1's effective scale; region: ${DESC}" \
    --thinking high --max-tokens 65536 \
    --timeout 600 --rounds 1 --tries 1 \
    --transcript "$QA/${TRANSCRIPT}" \
    -p "$(cat "$QA/payload_B_27.txt")" >>"$LOG/crop_${NAME}.log" 2>&1
  echo "crop ${NAME} rc=$?" | tee -a "$LOG/chain.log"
}

crop_leg table "the 8-row x 19-column gradient-descent table (x, f(x), x-delta, f(x-delta), x+delta, f(x+delta), slope, next x) with its coloured row fills, the green highlight cells and the highlighted x/f(x) columns" crop_27_table_judge.txt

crop_leg plot "the 2D plot of the non-convex function f(x)=(x^2 cos(x)-x)/10: teal curve, red local-max dot with dashed drop line, orange arrow annotation, green ellipse at the deepest minimum, pink 'Reach global Minima' label, black axes with tick numerals, and the red-framed plot panel" crop_27_plot_judge.txt

crop_leg leftblock "the left content block: title 'Non-Convex Function', the two subtitle lines, the 3-row parameter mini-table (step / initial X / delta), the red arrow, the white equation box holding the fraction f(x)=(x^2 cos(x)-x)/10, and the two-line callout about X and f(x) bounds" crop_27_leftblock_judge.txt

echo "=== ALL LEGS DONE ===" | tee -a "$LOG/chain.log"
