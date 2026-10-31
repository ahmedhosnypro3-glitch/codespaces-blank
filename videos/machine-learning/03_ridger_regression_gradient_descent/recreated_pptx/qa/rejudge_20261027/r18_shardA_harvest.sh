#!/usr/bin/env bash
# r18 shard A harvest — idempotent pass. For each in-scope slide leg with a clean
# (FINAL VERDICT, no 429) r18 transcript not yet marked done in r18_shardA_harvest_done.txt:
#   PASS -> append R18_<LEG> PASS record to slideNNN/result.txt + marker
#   FAIL -> run rejudge_adjudicate.py NNN [--full|--crop] -> slideNNN/adjudicate_r18_<leg>.txt,
#           append R18_<LEG> FAIL record + marker (diffuse/localized classification by
#           this worker from the banked census, recorded in the register)
set -u
ROOT=/home/codespace/ai_llm_slides
NS=$ROOT/videos/machine-learning/03_ridger_regression_gradient_descent
RJ=$NS/recreated_pptx/qa/rejudge_20261027
DONE=$RJ/r18_shardA_harvest_done.txt
LOG=$RJ/r18_shardA_harvest.log
touch "$DONE"

clean() { [ -f "$1" ] && grep -q 'FINAL VERDICT' "$1" 2>/dev/null && ! grep -qi '429' "$1" 2>/dev/null; }
verdict() { grep -oE 'FINAL VERDICT: *\*{0,2} *(PASS|FAIL)' "$1" | tail -1 | grep -oE 'PASS|FAIL'; }

for N in 001 002 003 004 005 006 007 008 009 010 011 012 013 015 016 017; do
  D=$RJ/slide$N
  for leg in full crop; do
    f=$D/judge_full_r18.txt; [ $leg = crop ] && f=$D/crop_dense_judge_r18.txt
    key="${N}_${leg}_r18"
    grep -q "^$key " "$DONE" && continue
    clean "$f" || continue
    v=$(verdict "$f"); ts=$(stat -c %y "$f" | cut -d. -f1)
    echo "$key $v $ts $(date -u +%FT%TZ)" >> "$DONE"
    {
      echo "R18_${leg^^}=$v (r18 transcript $(basename $f), $ts UTC, clean no 429, harvested $(date -u +%FT%TZ))"
      echo "R18_${leg^^}_TRANSCRIPT=$f"
      echo "R18_${leg^^}_VERDICT_TS=$ts UTC (clean, no 429)"
    } >> "$D/result.txt"
    if [ "$v" = FAIL ]; then
      mode="--full"; [ $leg = crop ] && mode="--crop"
      (cd "$ROOT" && python3 "$RJ/rejudge_adjudicate.py" "$N" $mode) > "$D/adjudicate_r18_${leg}.txt" 2>&1
      echo "$key FAIL adjudicated -> $D/adjudicate_r18_${leg}.txt $(date -u +%FT%TZ)" >> "$LOG"
    else
      echo "$key PASS $ts $(date -u +%FT%TZ)" >> "$LOG"
    fi
  done
done
echo "pass done $(date -u +%FT%TZ)" >> "$LOG"
