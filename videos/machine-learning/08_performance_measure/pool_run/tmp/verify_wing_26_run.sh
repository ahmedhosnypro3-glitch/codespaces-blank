#!/bin/bash
# verify-wing 026: on trigger flag, run corroboration judge, then dual-PASS bookkeeping.
set -u
REPO=/home/codespace/ai_llm_slides
NS=$REPO/videos/machine-learning/08_performance_measure
QA=$NS/recreated_pptx/qa/slide026
FLAG=$NS/pool_run/tmp/verify_wing_26_trigger.txt
LOG=$NS/pool_run/tmp/verify_wing_26_run.log

# wait for trigger
while [ ! -f "$FLAG" ]; do sleep 15; done
trigger=$(cat "$FLAG")
echo "$(date -Is) trigger: $trigger" >> "$LOG"
case "$trigger" in STANDDOWN*) echo "$trigger" >> "$LOG"; exit 0;; esac

attempt=$(echo "$trigger" | sed 's/.*attempt=\([^ ]*\).*/\1/')
render=$(echo "$trigger" | sed 's/.*render=\([^ ]*\).*/\1/')
render_base=$(basename "$render")

# next verify K
nextK=$(ls "$QA"/judge_verify_*.txt 2>/dev/null | sed 's/.*judge_verify_\([0-9a-z_]*\)\.txt/\1/' | sort -V | tail -1)
case "$nextK" in ''|*[!0-9]*) nextK=0;; esac
nextK=$((nextK+1))
out="$QA/judge_verify_${nextK}.txt"
echo "$(date -Is) corroboration -> $out vs $render_base (attempt=$attempt)" >> "$LOG"

# sleep 180-240s before the heavy call
sleep $((180 + RANDOM % 61))

cd "$REPO"
tries=0
while [ $tries -lt 8 ]; do
  tries=$((tries+1))
  timeout 540 python3 .agents/skills/image-analysis/scripts/analyze_image.py comparison \
    videos/machine-learning/08_performance_measure/unique_slides/slide_026.jpg \
    "videos/machine-learning/08_performance_measure/recreated_pptx/qa/slide026/$render_base" \
    --thinking high --max-tokens 65536 --timeout 420 --rounds 1 --tries 1 > "$out" 2>&1
  rc=$?
  echo "$(date -Is) verify try=$tries rc=$rc" >> "$LOG"
  if grep -q "FINAL VERDICT: PASS" "$out" 2>/dev/null; then
    echo "$(date -Is) verify PASS on try=$tries" >> "$LOG"
    break
  fi
  if grep -qiE "429|HangError|rate.?limit" "$out" 2>/dev/null; then
    echo "$(date -Is) 429/Hang -> sleep 300" >> "$LOG"
    sleep 300
  else
    sleep 60
  fi
done

verdict=$(grep -o "FINAL VERDICT: [A-Z]*" "$out" 2>/dev/null | tail -1)
echo "$(date -Is) final verify verdict: ${verdict:-NONE}" >> "$LOG"
if [ "$verdict" = "FINAL VERDICT: PASS" ]; then
  row="| 26 | \`recreated_pptx/qa/slide026/$(basename "$attempt")\` ($render_base) | \`recreated_pptx/qa/slide026/judge_verify_${nextK}.txt\` ($render_base) | PASS / PASS (original-first dual-read, backup verify-wing) |  | yes |"
  flock "$NS/pool_run/verification_ledger.md" -c "printf '%s\n' '$row' >> '$NS/pool_run/verification_ledger.md'"
  cd "$NS"
  python3 pool_run/merge_final_deck.py update 26 recreated_pptx/slide_026_recreated.pptx 08-performance_final.pptx >> "$LOG" 2>&1
  echo "$(date -Is) merge rc=$?" >> "$LOG"
  sqlite3 pool_run/mission.db "UPDATE scopes SET status='done' WHERE name='slide-26';"
  echo "$(date -Is) db updated" >> "$LOG"
  echo "DUAL_PASS_DONE" >> "$LOG"
else
  echo "VERIFY_NOT_PASS" >> "$LOG"
fi
