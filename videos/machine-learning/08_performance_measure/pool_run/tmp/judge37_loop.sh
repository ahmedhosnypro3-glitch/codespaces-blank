#!/usr/bin/env bash
# Retry judge attempt 1 for slide 37 until a FINAL VERDICT lands (infra hangs are not verdicts).
# Token-budget ladder: 65536 (prescribed) -> 32768 -> 16384.
set -u
cd /home/codespace/ai_llm_slides
NS=videos/machine-learning/08_performance_measure
QA=$NS/recreated_pptx/qa/slide037
PY=/home/codespace/.pyenv/versions/3.15.2/bin/python3
for MT in 65536 32768 16384; do
  OUT="$QA/judge_attempt_1_b$MT.txt"
  timeout 540 bash scripts/16_vision_gate.sh $PY .agents/skills/image-analysis/scripts/analyze_image.py \
    comparison $NS/unique_slides/slide_037.jpg $QA/render_1.png \
    --view "Slide 37 AUC — judge attempt 1 (original first, render second)" \
    --capture "960x540 CSS px, 1x scale, lecture video frame" \
    --thinking high --max-tokens $MT --timeout 420 --rounds 1 --tries 1 \
    -p "$(cat $NS/pool_run/judge_prompt_template.txt)" > "$OUT" 2>&1
  echo "rc=$? (max-tokens=$MT)" >> "$OUT"
  echo "=== done max-tokens=$MT rc=$? size=$(wc -c < "$OUT") ==="
  if grep -q "FINAL VERDICT" "$OUT"; then
    cp "$OUT" "$QA/judge_attempt_1.txt"
    echo "VERDICT_LANDED in $OUT"
    grep "FINAL VERDICT" "$OUT" | tail -1
    exit 0
  fi
done
echo "NO_VERDICT_ALL_BUDGETS"
exit 1
