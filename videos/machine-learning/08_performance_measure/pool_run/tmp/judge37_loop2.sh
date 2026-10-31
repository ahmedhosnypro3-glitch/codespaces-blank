#!/usr/bin/env bash
# Judge attempt 1 for slide 37, resilient to gate queue + API hangs.
# timeout wraps ONLY the API call (inside the gate); queue wait is unbounded.
set -u
cd /home/codespace/ai_llm_slides
NS=videos/machine-learning/08_performance_measure
QA=$NS/recreated_pptx/qa/slide037
PY=/home/codespace/.pyenv/versions/3.15.2/bin/python3
RENDER=${1:-$QA/render_1.png}
TAG=${2:-1}
for MT in 65536 32768 16384; do
  OUT="$QA/judge_attempt_${TAG}_b$MT.txt"
  bash scripts/16_vision_gate.sh timeout 540 $PY .agents/skills/image-analysis/scripts/analyze_image.py \
    comparison $NS/unique_slides/slide_037.jpg "$RENDER" \
    --view "Slide 37 AUC — judge attempt $TAG (original first, render second)" \
    --capture "960x540 CSS px, 1x scale, lecture video frame" \
    --thinking high --max-tokens $MT --timeout 420 --rounds 1 --tries 1 \
    -p "$(cat $NS/pool_run/judge_prompt_template.txt)" > "$OUT" 2>&1
  rc=$?
  echo "rc=$rc (max-tokens=$MT render=$(basename $RENDER))" >> "$OUT"
  echo "=== attempt tag=$TAG mt=$MT rc=$rc size=$(wc -c < "$OUT") ==="
  if grep -q "FINAL VERDICT" "$OUT"; then
    cp "$OUT" "$QA/judge_attempt_${TAG}.txt"
    echo "VERDICT_LANDED tag=$TAG mt=$MT"
    grep "FINAL VERDICT" "$OUT" | tail -1
    exit 0
  fi
done
echo "NO_VERDICT_ALL_BUDGETS tag=$TAG"
exit 1
