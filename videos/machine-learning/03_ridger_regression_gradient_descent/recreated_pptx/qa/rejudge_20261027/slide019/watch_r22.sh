#!/usr/bin/env bash
# watch_r22.sh — FRESH background monitor (round r22) for slide 019 k17 fix artifacts.
# Polls every ~180s for up to 2h (40 rounds). Logs to watch_r22.log.
# Detection: a judge_full_k17*.txt with a FINAL VERDICT line and 0 "429" occurrences
# whose verdict is PASS, on a k17 render that also has a pil_k17*.txt with OVERALL: PASS.
# On detection: logs CLEAN_FULL_PASS <variant> and exits 0 (promotion is done by the
# orchestrating agent, not by this script). Exit 1 on timeout.
RJ=/home/codespace/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/rejudge_20261027
D=$RJ/slide019
LOG=$D/watch_r22.log
NS=/home/codespace/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent
B=$NS/recreated_pptx/build

echo "watch_r22 start $(date -u +%FT%TZ) pid=$$ rounds=40 interval=180s" >> "$LOG"
python3 - "$NS/slides_progress.db" >> "$LOG" 2>&1 <<'PY'
import sqlite3, sys, datetime
c = sqlite3.connect(sys.argv[1])
row = c.execute("select slide_id, gen_status, visual_check, pptx_path, build_script from slides where slide_id=19").fetchone()
print(f"{datetime.datetime.utcnow().isoformat()}Z DB row 19: {row}")
PY

for i in $(seq 1 40); do
  TS=$(date -u +%FT%TZ)
  JS=$(ls $B/slide_019_k17*.js 2>/dev/null | xargs -r -n1 basename | tr '\n' ' ')
  RN=$(ls $D/render_k17*.png 2>/dev/null | xargs -r -n1 basename | tr '\n' ' ')
  PL=$(ls $D/pil_k17*.txt 2>/dev/null | xargs -r -n1 basename | tr '\n' ' ')
  echo "$TS round=$i js=[$JS] render=[$RN] pil=[$PL]" >> "$LOG"
  for jf in $D/judge_full_k17*.txt; do
    [ -f "$jf" ] || continue
    [ -s "$jf" ] || { echo "$TS $(basename $jf) exists but empty (leg in flight)" >> "$LOG"; continue; }
    N429=$(grep -c '429' "$jf")
    V=$(grep -i 'FINAL VERDICT' "$jf" | tail -1 | sed 's/^ *//')
    echo "$TS $(basename $jf) mtime=$(stat -c %y "$jf" | cut -c1-19) 429count=$N429 verdict=[$V]" >> "$LOG"
    if [ "$N429" = "0" ] && echo "$V" | grep -qi 'PASS'; then
      VAR=$(basename "$jf" | sed 's/judge_full_//; s/\.txt//')
      PIL="$D/pil_${VAR}.txt"
      if [ -f "$PIL" ] && grep -q 'OVERALL: PASS' "$PIL"; then
        echo "$TS CLEAN_FULL_PASS variant=$VAR transcript=$jf pil=$PIL verdict=[$V] 429=0" >> "$LOG"
        echo "$TS PROMOTE_READY variant=$VAR" >> "$LOG"
        exit 0
      else
        echo "$TS clean PASS verdict on $VAR but pil_${VAR}.txt missing or not OVERALL PASS (pil=[$(ls $D/pil_${VAR}.txt 2>/dev/null)]) — waiting" >> "$LOG"
      fi
    fi
  done
  sleep 180
done
echo "$(date -u +%FT%TZ) WATCH_TIMEOUT after 40 rounds (~2h), no clean k17 FULL PASS" >> "$LOG"
exit 1
