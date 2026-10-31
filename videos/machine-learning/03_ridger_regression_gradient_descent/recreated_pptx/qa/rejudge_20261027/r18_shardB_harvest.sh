#!/usr/bin/env bash
# r18 shard B harvest — one pass, idempotent. For each in-scope slide leg with a clean
# (FINAL VERDICT, no 429) r18 transcript not yet marked done in r18_shardB_harvest_done.txt:
#   PASS -> append r18 PASS record to slideNNN/result.txt (R18_* fields) + marker
#   FAIL -> run rejudge_adjudicate.py NNN [--crop] -> slideNNN/adjudicate_r18_<leg>.txt,
#           append r18 FAIL record to result.txt + marker (diffuse/localized disposition
#           applied by the r18 shard B spawn after reading the adjudication output)
set -u
ROOT=/home/codespace/ai_llm_slides
NS=$ROOT/videos/machine-learning/03_ridger_regression_gradient_descent
RJ=$NS/recreated_pptx/qa/rejudge_20261027
DONE=$RJ/r18_shardB_harvest_done.txt
LOG=$RJ/r18_shardB_harvest.log
touch "$DONE"

clean() { [ -f "$1" ] && grep -q 'FINAL VERDICT' "$1" 2>/dev/null && ! grep -qi '429' "$1" 2>/dev/null; }
verdict() { grep -oE 'FINAL VERDICT: *\*{0,2} *(PASS|FAIL)' "$1" | tail -1 | grep -oE 'PASS|FAIL'; }

for N in 018 019 020 021 022 023 024 026 027 028 029 030 031 032 034; do
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
