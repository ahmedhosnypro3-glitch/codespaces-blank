#!/bin/bash
# VERIFY-WING corroboration judge, slide 18, namespace 08_performance_measure.
# Original-first order: IMG1=original frame, IMG2=newest render.
cd /home/codespace/ai_llm_slides || exit 1
NS=videos/machine-learning/08_performance_measure
PY=/home/codespace/.pyenv/versions/3.15.2/bin/python3
RENDER=$NS/recreated_pptx/qa/slide018/render.png
OUT=$NS/recreated_pptx/qa/slide018/judge_verify_v2_$(date +%s)_18.txt
echo "start $(date -u +%FT%TZ) render=$RENDER" > "$OUT"
S=$((RANDOM % 61 + 90))
echo "pre-call pacing sleep ${S}s" >> "$OUT"
sleep "$S"
i=0
while [ $i -lt 8 ]; do
  i=$((i+1))
  TMP=$(mktemp /tmp/verify18_XXXX.txt)
  "$PY" .agents/skills/image-analysis/scripts/analyze_image.py comparison \
    "$NS/unique_slides/slide_018.jpg" "$RENDER" \
    --thinking high --max-tokens 65536 --timeout 600 --rounds 1 --tries 1 \
    -p "$(cat $NS/pool_run/judge_prompt_template.txt)" > "$TMP" 2>&1
  rc=$?
  cat "$TMP" >> "$OUT"
  if grep -q "FINAL VERDICT" "$TMP"; then
    echo "[attempt $i rc=$rc] FINAL VERDICT present: $(grep 'FINAL VERDICT' "$TMP" | tail -1)" >> "$OUT"
    rm -f "$TMP"
    break
  fi
  if grep -qiE "429|HangError|Too Many Requests|rate.?limit|ServiceTimeout" "$TMP"; then
    echo "[attempt $i rc=$rc] infra failure (429/hang/timeout) — sleep 300" >> "$OUT"
  else
    echo "[attempt $i rc=$rc] empty/no-verdict output — sleep 300" >> "$OUT"
  fi
  rm -f "$TMP"
  sleep 300
done
echo "DONE attempts=$i $(date -u +%FT%TZ)" >> "$OUT"
