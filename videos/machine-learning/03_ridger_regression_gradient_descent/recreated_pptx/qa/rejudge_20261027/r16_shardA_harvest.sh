#!/usr/bin/env bash
# r16 shard A harvest — one pass, idempotent. For each in-scope slide leg with a clean
# (FINAL VERDICT, no 429) r16 transcript not yet marked done in r16_harvest_done.txt:
#   PASS -> append r16 PASS record to slideNNN/result.txt (r16 fields) + marker
#   FAIL -> run rejudge_adjudicate.py NNN [--crop] -> slideNNN/adjudicate_r16_<leg>.txt,
#           append r16 FAIL record to result.txt + marker (disposition decided by orchestrator)
set -u
ROOT=/home/codespace/ai_llm_slides
NS=$ROOT/videos/machine-learning/03_ridger_regression_gradient_descent
RJ=$NS/recreated_pptx/qa/rejudge_20261027
DONE=$RJ/r16_harvest_done.txt
LOG=$RJ/r16_shardA_harvest.log
touch "$DONE"

clean() { [ -f "$1" ] && grep -q 'FINAL VERDICT' "$1" 2>/dev/null && ! grep -qi '429' "$1" 2>/dev/null; }
verdict() { grep -oE 'FINAL VERDICT: *\*{0,2} *(PASS|FAIL)' "$1" | tail -1 | grep -oE 'PASS|FAIL'; }

for N in 001 002 003 004 005 006 007 008 009 010 011 012 013 015 016 017; do
  D=$RJ/slide$N
  for leg in full crop; do
    f=$D/judge_full_r16.txt; [ $leg = crop ] && f=$D/crop_dense_judge_r16.txt
    key="${N}_${leg}_r16"
    grep -q "^$key " "$DONE" && continue
    clean "$f" || continue
    v=$(verdict "$f"); ts=$(stat -c %y "$f" | cut -d. -f1)
    echo "$key $v $ts $(date -u +%FT%TZ)" >> "$DONE"
    {
      echo "R16_${leg^^}=$v (r16 transcript $(basename $f), $ts UTC, clean no 429, harvested $(date -u +%FT%TZ))"
      echo "R16_${leg^^}_TRANSCRIPT=$f"
    } >> "$D/result.txt"
    if [ "$v" = FAIL ]; then
      mode="--full"; [ $leg = crop ] && mode="--crop"
      (cd "$ROOT" && python3 "$RJ/rejudge_adjudicate.py" "$N" $mode) > "$D/adjudicate_r16_${leg}.txt" 2>&1
      echo "$key FAIL adjudicated -> $D/adjudicate_r16_${leg}.txt $(date -u +%FT%TZ)" >> "$LOG"
    else
      echo "$key PASS $ts $(date -u +%FT%TZ)" >> "$LOG"
    fi
  done
done
echo "pass done $(date -u +%FT%TZ)" >> "$LOG"
