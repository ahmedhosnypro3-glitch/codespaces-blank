#!/bin/bash
# Backup verify wing (agent-B) for slide 6, 08_performance_measure.
# Runs the corroboration judge as an uncapped background job; ends in wait.
NS=/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure
QA=$NS/recreated_pptx/qa/slide006
REPO=/home/codespace/ai_llm_slides
LOG=$NS/pool_run/verify_wing_b_slide6.log
cd "$REPO" || exit 2

{
  RENDER=$(ls -t "$QA"/render_*.png | head -1)
  RENDER_REL=videos/machine-learning/08_performance_measure/recreated_pptx/qa/slide006/$(basename "$RENDER")
  K=1
  while [ -e "$QA/judge_verify_$K.txt" ]; do K=$((K+1)); done
  OUT=$QA/judge_verify_$K.txt
  echo "$(date -u +%FT%TZ) wing-B slide6: newest render=$(basename "$RENDER") bank=$OUT"
  sleep $((90 + RANDOM % 61))
  for i in $(seq 1 8); do
    echo "$(date -u +%FT%TZ) attempt $i/8 -> $OUT.tmp"
    python3 .agents/skills/image-analysis/scripts/analyze_image.py comparison \
      videos/machine-learning/08_performance_measure/unique_slides/slide_006.jpg \
      "$RENDER_REL" \
      --thinking high --max-tokens 65536 --timeout 600 --rounds 1 --tries 1 \
      -p "$(cat videos/machine-learning/08_performance_measure/pool_run/judge_prompt_template.txt)" \
      > "$OUT.tmp" 2>&1
    rc=$?
    echo "$(date -u +%FT%TZ) attempt $i rc=$rc bytes=$(stat -c%s "$OUT.tmp" 2>/dev/null)"
    if grep -q "FINAL VERDICT:" "$OUT.tmp" 2>/dev/null; then
      mv "$OUT.tmp" "$OUT"
      echo "$(date -u +%FT%TZ) VERDICT BANKED: $OUT"
      grep "FINAL VERDICT:" "$OUT"
      exit 0
    fi
    if [ ! -s "$OUT.tmp" ] || grep -qiE "429|HangError|empty|rate.?limit|ServiceTimeout" "$OUT.tmp"; then
      echo "$(date -u +%FT%TZ) transient (429/empty/HangError) — sleep 300"
    else
      echo "$(date -u +%FT%TZ) no verdict, rc=$rc — sleep 300 and retry"
    fi
    sleep 300
  done
  [ -s "$OUT.tmp" ] && mv "$OUT.tmp" "$OUT"
  echo "$(date -u +%FT%TZ) NO VERDICT after 8 attempts; raw banked at $OUT"
  exit 1
} > "$LOG" 2>&1 &
wait
