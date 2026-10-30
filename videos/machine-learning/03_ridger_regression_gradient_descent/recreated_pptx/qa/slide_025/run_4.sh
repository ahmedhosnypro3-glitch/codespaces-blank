#!/bin/bash
# Slide 025 K=4 judge runner: full-slide leg A + remaining Procedure B crop legs.
# Detached (setsid) so it survives session loss. Payloads are the byte-frozen
# crop_prompt_4_*.txt / judge_prompt_4.txt; analyzer --timeout 600 inside timeout 1700.
export TMPDIR=/workspaces/codespaces-blank/ai_llm_slides/scratch/tmp
cd /workspaces/codespaces-blank/ai_llm_slides || exit 1
QA=videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide_025
RUNLOG=$QA/scratch/run_4.log
runcrop() {
  local NAME="$1" DESC="$2"
  if [ -s "$QA/crop_4_${NAME}_judge.txt" ] && grep -q "FINAL VERDICT:" "$QA/crop_4_${NAME}_judge.txt"; then
    echo "[$(date -u +%H:%M:%SZ)] SKIP crop $NAME (verdict already banked)" >> "$RUNLOG"; return 0
  fi
  local P; P="$(cat $QA/crop_prompt_4_$NAME.txt)"
  echo "[$(date -u +%H:%M:%SZ)] dispatch crop $NAME" >> "$RUNLOG"
  timeout 1700 bash scripts/16_vision_gate.sh python3 \
    .agents/skills/image-analysis/scripts/analyze_image.py comparison \
    $QA/crop_4_${NAME}_render.png $QA/crop_4_${NAME}_orig.png \
    --view "Slide 025 zoomed crop $NAME — render vs original at matched scale (attempt 4)" \
    --capture "IMG1=zoomed crop of a 150dpi PPTX render; IMG2=the SAME slide-space region cropped from the original lecture frame and upscaled to match IMG1's effective scale; region: $DESC" \
    --thinking high --max-tokens 65536 \
    --timeout 600 --rounds 1 --tries 1 \
    --transcript $QA/crop_4_${NAME}_judge.txt \
    -p "$P" >> "$QA/scratch/run_crop_$NAME.log" 2>&1
  echo "[$(date -u +%H:%M:%SZ)] crop $NAME rc=$?" >> "$RUNLOG"
}
echo "[$(date -u +%H:%M:%SZ)] runner start" >> "$RUNLOG"
if [ ! -s "$QA/judge_attempt_4.txt" ] || ! grep -q "FINAL VERDICT:" "$QA/judge_attempt_4.txt"; then
  echo "[$(date -u +%H:%M:%SZ)] dispatch leg A full-slide" >> "$RUNLOG"
  PA="$(cat $QA/judge_prompt_4.txt)"
  timeout 1700 bash scripts/16_vision_gate.sh python3 \
    .agents/skills/image-analysis/scripts/analyze_image.py comparison \
    $QA/render_4.png videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_025.jpg \
    --view "Slide 025 recreation attempt 4 — fidelity check vs original lecture frame" \
    --capture "IMG1=150dpi PNG render of a 13.33x7.5in PPTX; IMG2=original lecture video frame" \
    --thinking high --max-tokens 65536 \
    --timeout 600 --rounds 1 --tries 1 \
    --transcript $QA/judge_attempt_4.txt \
    -p "$PA" >> "$QA/scratch/run_A_4.log" 2>&1
  echo "[$(date -u +%H:%M:%SZ)] leg A rc=$?" >> "$RUNLOG"
else
  echo "[$(date -u +%H:%M:%SZ)] leg A already banked" >> "$RUNLOG"
fi
runcrop lbl_upper "the top-gutter blue caption boxes beside the TL and TR figure boxes"
runcrop lbl_lower "the bottom-gutter blue caption boxes beside the BL and BR figure boxes"
runcrop tl "the top-left white figure: thin red border, concave dome jet surface, two red horizontal reference lines"
runcrop tr "the top-right white figure: thin red border, convex bowl jet surface, axis ticks with x10^4 scale, two red reference lines"
runcrop bl "the bottom-left white figure: thin red border, non-convex multi-extremum surface, red reference line, two red annotation arrows, four black Global/Local annotations"
runcrop br "the bottom-right white figure: thin red border, valley jet surface, black gradient-descent path with arrowheads"
echo "[$(date -u +%H:%M:%SZ)] RUNNER COMPLETE" >> "$RUNLOG"
