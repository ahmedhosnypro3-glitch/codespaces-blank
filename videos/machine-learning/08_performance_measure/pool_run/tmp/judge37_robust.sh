#!/usr/bin/env bash
# Robust judge runner: RENDER TAG OUTBASE
# - sleeps before each gateway-bound call
# - on 429 / hang / no-verdict: sleep 240s, retry up to 5 times
set -u
cd /home/codespace/ai_llm_slides
NS=videos/machine-learning/08_performance_measure
QA=$NS/recreated_pptx/qa/slide037
PY=/home/codespace/.pyenv/versions/3.15.2/bin/python3
RENDER=$1
TAG=$2
for attempt in 1 2 3 4 5; do
  sleep 70
  MT=32768
  OUT="$QA/${TAG}_r${attempt}.txt"
  bash scripts/16_vision_gate.sh timeout 500 $PY .agents/skills/image-analysis/scripts/analyze_image.py \
    comparison $NS/unique_slides/slide_037.jpg "$RENDER" \
    --view "Slide 37 AUC — $TAG attempt $attempt (original first, render second)" \
    --capture "960x540 CSS px, 1x scale, lecture video frame" \
    --thinking high --max-tokens $MT --timeout 380 --rounds 2 --tries 2 \
    -p "$(cat $NS/pool_run/judge_prompt_template.txt)" > "$OUT" 2>&1
  rc=$?
  echo "rc=$rc (attempt=$attempt)" >> "$OUT"
  echo "=== $TAG attempt=$attempt rc=$rc size=$(wc -c < "$OUT") ==="
  if grep -q "FINAL VERDICT" "$OUT"; then
    cp "$OUT" "$QA/${TAG}.txt"
    echo "VERDICT_LANDED $TAG attempt=$attempt"
    grep "FINAL VERDICT" "$OUT" | tail -1
    exit 0
  fi
  echo "no verdict (rc=$rc); sleeping 240 before retry"
  sleep 240
done
echo "NO_VERDICT $TAG"
exit 1
