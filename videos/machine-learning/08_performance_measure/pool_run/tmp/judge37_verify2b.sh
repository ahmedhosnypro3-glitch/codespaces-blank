#!/usr/bin/env bash
# Persistent corroboration read for slide 37 (dual-read law): retry until a
# FINAL VERDICT lands. Infra failures (hang / 429 / upstream timeout) are not verdicts.
set -u
cd /home/codespace/ai_llm_slides
NS=videos/machine-learning/08_performance_measure
QA=$NS/recreated_pptx/qa/slide037
PY=/home/codespace/.pyenv/versions/3.15.2/bin/python3
RENDER=$QA/render_2.png
i=0
for MT in 32768 65536 32768 16384 32768 65536 32768 16384 32768 65536 32768 16384; do
  i=$((i+1))
  OUT="$QA/judge_verify_2_r${i}_b$MT.txt"
  bash scripts/16_vision_gate.sh timeout 500 $PY .agents/skills/image-analysis/scripts/analyze_image.py \
    comparison $NS/unique_slides/slide_037.jpg "$RENDER" \
    --view "Slide 37 AUC — corroboration read (original first, render second)" \
    --capture "960x540 CSS px, 1x scale, lecture video frame" \
    --thinking high --max-tokens $MT --timeout 380 --rounds 2 --tries 2 \
    -p "$(cat $NS/pool_run/judge_prompt_template.txt)" > "$OUT" 2>&1
  rc=$?
  echo "rc=$rc (round=$i max-tokens=$MT)" >> "$OUT"
  echo "=== verify round=$i mt=$MT rc=$rc size=$(wc -c < "$OUT") ==="
  if grep -q "FINAL VERDICT" "$OUT"; then
    cp "$OUT" "$QA/judge_verify_2.txt"
    echo "VERIFY_LANDED round=$i mt=$MT"
    grep "FINAL VERDICT" "$OUT" | tail -1
    exit 0
  fi
  sleep 20
done
echo "NO_VERDICT_AFTER_ALL_ROUNDS"
exit 1
