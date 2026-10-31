#!/usr/bin/env bash
# Corroboration read for slide 37 (dual-read law), per parent instruction:
#   - ORIGINAL first, newest render second, frozen judge template
#   - sleep 150s before the first heavy call, 90-150s between calls
#   - on 429 / HangError: sleep 300s, retry up to 8x
set -u
cd /home/codespace/ai_llm_slides
NS=videos/machine-learning/08_performance_measure
QA=$NS/recreated_pptx/qa/slide037
PY=/home/codespace/.pyenv/versions/3.15.2/bin/python3
RENDER=$QA/render_8.png
OUT=$QA/judge_verify_8.txt
sleep 150
for attempt in 1 2 3 4 5 6 7 8; do
  timeout 540 $PY .agents/skills/image-analysis/scripts/analyze_image.py \
    comparison $NS/unique_slides/slide_037.jpg "$RENDER" \
    --view "Slide 37 AUC — corroboration read $attempt (original first, render second)" \
    --capture "960x540 CSS px, 1x scale, lecture video frame" \
    --thinking high --max-tokens 65536 --timeout 420 --rounds 1 --tries 1 \
    -p "$(cat $NS/pool_run/judge_prompt_template.txt)" > "$OUT" 2>&1
  rc=$?
  echo "rc=$rc (attempt=$attempt)" >> "$OUT"
  echo "=== verify attempt=$attempt rc=$rc size=$(wc -c < "$OUT") ==="
  if grep -q "FINAL VERDICT" "$OUT"; then
    grep "FINAL VERDICT" "$OUT" | tail -1
    exit 0
  fi
  echo "no verdict (rc=$rc); sleeping 300 before retry"
  sleep 300
done
echo "NO_VERDICT_AFTER_8_ATTEMPTS"
exit 1
