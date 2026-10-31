#!/usr/bin/env bash
# Judge retry driver for slide 15 (queue-tolerant under a saturated fleet vision gate).
# Each round re-rolls for a free vision-gate slot; a round that reaches the model and
# returns a verdict ends the loop. Rounds that die in the gate queue are banked as
# timeout evidence and do NOT consume a judge attempt.
set -u
cd /home/codespace/ai_llm_slides
NS=videos/machine-learning/08_performance_measure
QA=$NS/recreated_pptx/qa/slide015
OUT=$QA/judge_attempt_3.txt
LOG=$QA/judge_attempt_3_queue.log
PY=/home/codespace/.pyenv/versions/3.15.2/bin/python3
PROMPT=$(cat $NS/pool_run/judge_prompt_template.txt)

for round in $(seq 1 15); do
  timeout 1400 bash scripts/16_vision_gate.sh "$PY" .agents/skills/image-analysis/scripts/analyze_image.py \
    comparison $NS/unique_slides/slide_015.jpg $NS/recreated_pptx/qa/slide015/render_3.png \
    --thinking high --max-tokens 65536 --timeout 420 --rounds 1 --tries 1 -p "$PROMPT" > "$OUT" 2>&1
  rc=$?
  if grep -qa "FINAL VERDICT" "$OUT"; then
    echo "round $round rc=$rc verdict=$(grep -a 'FINAL VERDICT' "$OUT" | tail -1)" >> "$LOG"
    echo "VERDICT_READY"
    exit 0
  fi
  size=$(wc -c < "$OUT")
  echo "round $round rc=$rc bytes=$size (no verdict)" >> "$LOG"
  cp "$OUT" "$QA/judge_attempt_3_timeout_r${round}.txt"
  : > "$OUT"
  sleep 15
done
echo "NO_VERDICT_AFTER_15_ROUNDS"
exit 1
