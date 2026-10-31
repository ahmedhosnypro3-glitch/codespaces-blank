#!/bin/bash
# Fresh corroboration read for slide 37 (verify-wing). Uncapped; up to 8 attempts.
cd /home/codespace/ai_llm_slides || exit 1
NS=videos/machine-learning/08_performance_measure
QADIR=$NS/recreated_pptx/qa/slide037
RENDER=$QADIR/render.png
TS=$(date +%s)
PRIMARY=$QADIR/judge_verify_v2_${TS}_37.txt
for attempt in $(seq 1 8); do
  OUT=$PRIMARY
  if [ "$attempt" -gt 1 ]; then OUT=$QADIR/judge_verify_v2_${TS}_37_attempt${attempt}.txt; fi
  echo "[verify37] attempt $attempt/8 -> $OUT $(date)" >> $QADIR/judge_verify_v2_${TS}_37_retries.log
  python3 .agents/skills/image-analysis/scripts/analyze_image.py comparison \
    $NS/unique_slides/slide_037.jpg \
    $RENDER \
    --thinking high --max-tokens 65536 --timeout 600 --rounds 1 --tries 1 \
    -p "$(cat $NS/pool_run/judge_prompt_template.txt)" \
    > "$OUT" 2>&1
  rc=$?
  echo "[verify37] attempt $attempt rc=$rc $(date)" >> $QADIR/judge_verify_v2_${TS}_37_retries.log
  if grep -q "FINAL VERDICT" "$OUT"; then
    echo "[verify37] verdict found on attempt $attempt: $(grep 'FINAL VERDICT' "$OUT" | tail -1)" >> $QADIR/judge_verify_v2_${TS}_37_retries.log
    echo "$OUT" > $QADIR/judge_verify_v2_${TS}_37_final_path.txt
    exit 0
  fi
  echo "[verify37] no verdict (429/HangError/empty); sleeping 300s" >> $QADIR/judge_verify_v2_${TS}_37_retries.log
  sleep 300
done
echo "[verify37] exhausted 8 attempts, no verdict" >> $QADIR/judge_verify_v2_${TS}_37_retries.log
exit 1
