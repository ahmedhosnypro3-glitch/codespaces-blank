#!/usr/bin/env bash
# judge_s21.sh — slide 21 original-first judge with mandated spacing + 429 retry ladder.
set -u
REPO=/home/codespace/ai_llm_slides
NS=$REPO/videos/machine-learning/08_performance_measure
PYBIN=/home/codespace/.pyenv/versions/3.15.2/bin/python3
Q=$NS/recreated_pptx/qa/slide021
ORIG=$NS/unique_slides/slide_021.jpg
RENDER=$Q/render_2.png
LOG=$Q/judge_attempt_2.log
PROMPT="$(cat $NS/pool_run/judge_prompt_template.txt)"

echo "[$(date '+%F %T')] initial spacing sleep 270s before first gateway call" >> "$LOG"
sleep 270
echo "[$(date '+%F %T')] probe --timeout 120" >> "$LOG"
timeout 200 bash $REPO/scripts/16_vision_gate.sh $PYBIN $REPO/.agents/skills/image-analysis/scripts/analyze_image.py analysis "$ORIG" -p "Reply with the single word READY" --timeout 120 > "$Q/probe_s21.txt" 2>&1
echo "[$(date '+%F %T')] probe rc=$? bytes=$(wc -c < "$Q/probe_s21.txt")" >> "$LOG"

echo "[$(date '+%F %T')] spacing 180s before judge" >> "$LOG"
sleep 180
echo "[$(date '+%F %T')] judge attempt_2 starting (original-first)" >> "$LOG"
for i in $(seq 1 8); do
  timeout 540 bash $REPO/scripts/16_vision_gate.sh $PYBIN $REPO/.agents/skills/image-analysis/scripts/analyze_image.py comparison "$ORIG" "$RENDER" \
    --thinking high --max-tokens 65536 --timeout 420 --rounds 1 --tries 1 \
    --transcript "$Q/judge_attempt_2.txt" \
    -p "$PROMPT" > "$Q/judge_attempt_2_try$i.txt" 2>&1
  rc=$?
  T="$Q/judge_attempt_2_try$i.txt"
  [ -s "$Q/judge_attempt_2.txt" ] && T="$Q/judge_attempt_2.txt"
  echo "[$(date '+%F %T')] try $i rc=$rc bytes=$(wc -c < "$T")" >> "$LOG"
  if grep -q "FINAL VERDICT" "$T" 2>/dev/null; then
    cp "$T" "$Q/judge_attempt_2.txt"
    echo "[$(date '+%F %T')] VERDICT found try $i: $($PYBIN $NS/pool_run/verdict.py "$Q/judge_attempt_2.txt")" >> "$LOG"
    exit 0
  fi
  if grep -q "429" "$T" 2>/dev/null; then
    echo "[$(date '+%F %T')] HTTP 429 -> sleep 300s" >> "$LOG"
    sleep 300
  else
    echo "[$(date '+%F %T')] no verdict -> spacing 180s" >> "$LOG"
    sleep 180
  fi
done
echo "[$(date '+%F %T')] NO VERDICT after 8 tries" >> "$LOG"
exit 1
