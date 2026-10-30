#!/usr/bin/env bash
# Procedure B crop-pair judge runner for slide 028 — Template B payload VERBATIM.
# Patient storm retry: up to ATTEMPTS tries, 60-120s spacing; stops as soon as a
# transcript banks a FINAL VERDICT line.
set -u
ROOT=/workspaces/codespaces-blank/ai_llm_slides
export TMPDIR=/workspaces/codespaces-blank/ai_llm_slides/scratch/tmp
QA=$ROOT/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide028
NAME="$1"; DESC="$2"; ATTEMPTS="${3:-3}"
TS="$QA/crop_4_${NAME}_judge.txt"
PAYLOAD=$(sed 's/NNN/28/g' "$QA/payload_template_B.txt")
LOG="$QA/crop_4_${NAME}_retry.log"

echo "=== crop judge: $NAME  attempts=$ATTEMPTS  start $(date +%T) ===" | tee -a "$LOG"
echo "region: $DESC" | tee -a "$LOG"

for a in $(seq 1 "$ATTEMPTS"); do
  echo "--- attempt $a  $(date +%T) ---" | tee -a "$LOG"
  cd "$ROOT" && scripts/16_vision_gate.sh timeout 1700 python3 \
    .agents/skills/image-analysis/scripts/analyze_image.py comparison \
    "$QA/crop_4_${NAME}_render.png" \
    "$QA/crop_4_${NAME}_orig.png" \
    --view "Slide 028 zoomed crop ${NAME} — render vs original at matched scale (attempt 3)" \
    --capture "IMG1=zoomed crop of a 150dpi PPTX render; IMG2=the SAME slide-space region cropped from the original lecture frame and upscaled to match IMG1's effective scale; region: ${DESC}" \
    --thinking high --max-tokens 65536 \
    --timeout 600 --rounds 1 --tries 1 \
    --transcript "$TS" \
    -p "$PAYLOAD" 2>&1 | tail -20 | tee -a "$LOG"
  if grep -q "FINAL VERDICT" "$TS" 2>/dev/null; then
    echo "==> VERDICT BANKED on attempt $a for $NAME" | tee -a "$LOG"
    tail -3 "$TS" | tee -a "$LOG"
    exit 0
  fi
  echo "==> no verdict yet for $NAME (attempt $a)" | tee -a "$LOG"
  if [ "$a" -lt "$ATTEMPTS" ]; then
    s=$((60 + RANDOM % 61))
    echo "    storm pacing: sleep ${s}s" | tee -a "$LOG"
    sleep "$s"
  fi
done
echo "=== EXHAUSTED $ATTEMPTS attempts for $NAME without a verdict ===" | tee -a "$LOG"
exit 1
