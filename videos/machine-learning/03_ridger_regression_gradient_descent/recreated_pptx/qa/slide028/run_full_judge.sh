#!/usr/bin/env bash
# Template A full-slide comparison — slide 028, render_4 (attempt 2).
# Payload sourced verbatim from shared_patterns/judge_protocol_03.md Template A.
# Patient storm retry: up to ATTEMPTS tries with 60-120s spacing; stops as soon as a
# transcript banks a FINAL VERDICT line.
set -u
ROOT=/workspaces/codespaces-blank/ai_llm_slides
export TMPDIR=/workspaces/codespaces-blank/ai_llm_slides/scratch/tmp
QA=$ROOT/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide028
ATTEMPTS="${1:-3}"
TS="$QA/judge_attempt_2.txt"
LOG="$QA/judge_retry_4.log"
PAYLOAD=$(cat "$QA/payload_template_A.txt")

echo "=== Template A judge: slide 028 render_4  attempts=$ATTEMPTS  start $(date +%T) ===" | tee -a "$LOG"

for a in $(seq 1 "$ATTEMPTS"); do
  echo "--- attempt $a  $(date +%T) ---" | tee -a "$LOG"
  cd "$ROOT" && scripts/16_vision_gate.sh timeout 1700 python3 \
    .agents/skills/image-analysis/scripts/analyze_image.py comparison \
    "$QA/render_4.png" \
    "$ROOT/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_028.jpg" \
    --view "Slide 028 recreation — fidelity check vs original lecture frame" \
    --capture "IMG1=150dpi PNG render of a 13.33x7.5in PPTX; IMG2=original lecture video frame" \
    --thinking high --max-tokens 65536 \
    --timeout 600 --rounds 1 --tries 1 \
    --transcript "$TS" \
    -p "$PAYLOAD" 2>&1 | tail -12 | tee -a "$LOG"
  if grep -q "FINAL VERDICT" "$TS" 2>/dev/null; then
    echo "==> VERDICT BANKED on attempt $a" | tee -a "$LOG"
    tail -2 "$TS" | tee -a "$LOG"
    exit 0
  fi
  echo "==> no verdict yet (attempt $a)" | tee -a "$LOG"
  if [ "$a" -lt "$ATTEMPTS" ]; then
    s=$((60 + RANDOM % 61)); echo "    storm pacing: sleep ${s}s" | tee -a "$LOG"; sleep "$s"
  fi
done
echo "=== EXHAUSTED $ATTEMPTS attempts without a verdict ===" | tee -a "$LOG"
exit 1
