#!/usr/bin/env bash
# r20 shard A harvest — append-only. For each in-scope slide (001-013, 015-018):
#  clean r20 transcript (FINAL VERDICT present, no 429):
#    PASS  -> update canonical FULL=/CROP= line in result.txt (backup .preR20.bak first)
#             + append R20_* fields + transcript pointers
#    FAIL  -> append R20_FULL=FAIL / R20_CROP=FAIL + run rejudge_adjudicate.py into
#             slideNNN/adjudicate_r20_{full,crop}.txt (adjudication disposition by human/agent)
#  missing/no-verdict leg -> nothing (wrapper may still be in flight).
# Idempotent: skips legs already harvested (R20_FULL=/R20_CROP= line present).
set -u
ROOT=/home/codespace/ai_llm_slides
NS=$ROOT/videos/machine-learning/03_ridger_regression_gradient_descent
RJ=$NS/recreated_pptx/qa/rejudge_20261027
LOG=$RJ/r20_shardA_harvest.log
: > "$LOG"

clean() { [ -f "$1" ] && grep -q 'FINAL VERDICT' "$1" 2>/dev/null && ! grep -qi '429' "$1" 2>/dev/null; }
verdict() { grep -oE 'FINAL VERDICT: *\*{0,2} *(PASS|FAIL)' "$1" | tail -1 | grep -oE 'PASS|FAIL'; }
ts() { stat -c %y "$1" | cut -d. -f1 | sed 's/ /_/'; }

for N in 001 002 003 004 005 006 007 008 009 010 011 012 013 015 016 017 018; do
  D=$RJ/slide$N; NN=$((10#$N)); R=$D/result.txt
  [ -f "$R" ] || { echo "$N: no result.txt, skip" >> "$LOG"; continue; }

  for leg in full crop; do
    if [ "$leg" = full ]; then T=$D/judge_full_r20.txt; FIELD=R20_FULL; CANON=FULL; ADJ=full
    else T=$D/crop_dense_judge_r20.txt; FIELD=R20_CROP; CANON=CROP; ADJ=crop; fi
    grep -q "^${FIELD}=" "$R" && { echo "$N $leg: already harvested" >> "$LOG"; continue; }
    clean "$T" || { echo "$N $leg: no clean r20 transcript yet" >> "$LOG"; continue; }
    V=$(verdict "$T")
    [ -f "$R.preR20.bak" ] || cp "$R" "$R.preR20.bak"
    if [ "$V" = PASS ]; then
      sed -i "s|^${CANON}=.*|${CANON}=PASS|" "$R"
      sed -i "s|^${CANON}_TRANSCRIPT=.*|${CANON}_TRANSCRIPT=$T|" "$R"
      { echo "${FIELD}=PASS"
        echo "${FIELD}_TRANSCRIPT=$T"
        echo "${FIELD}_TS=$(ts "$T") UTC r20 clean no-429, harvested $(date -u +%FT%TZ)"
      } >> "$R"
      echo "$N $leg: r20 PASS -> result.txt ${CANON}=PASS" >> "$LOG"
    else
      { echo "${FIELD}=FAIL"
        echo "${FIELD}_TRANSCRIPT=$T"
        echo "${FIELD}_TS=$(ts "$T") UTC r20 clean FAIL, harvested $(date -u +%FT%TZ)"
      } >> "$R"
      if [ "$ADJ" = full ]; then python3 "$RJ/rejudge_adjudicate.py" "$N" --full > "$D/adjudicate_r20_full.txt" 2>&1
      else python3 "$RJ/rejudge_adjudicate.py" "$N" --crop > "$D/adjudicate_r20_crop.txt" 2>&1; fi
      echo "$N $leg: r20 FAIL -> appended + adjudicate_r20_$ADJ.txt banked (disposition pending)" >> "$LOG"
    fi
  done
done
echo "HARVEST_PASS_DONE $(date -u +%FT%TZ)" >> "$LOG"
cat "$LOG"
