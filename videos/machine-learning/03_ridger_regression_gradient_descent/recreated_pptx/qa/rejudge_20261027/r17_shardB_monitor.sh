#!/usr/bin/env bash
# r17_shardB_monitor.sh — idempotent harvest loop for shard B r17 legs.
# For each slide 018-034 (skip 025/033): when judge_full_r17.txt / crop_dense_judge_r17.txt
# is clean (FINAL VERDICT, no 429) and result.txt lacks the R17_ key, append:
#   PASS -> R17_FULL=PASS (+ transcript + verdict ts)
#   FAIL -> R17_FULL=FAIL + PIL census banked via rejudge_adjudicate.py (classification by orchestrator)
# Never rewrites existing result.txt lines; appends only. No git; no deletes.
set -u
ROOT=/home/codespace/ai_llm_slides
NS=$ROOT/videos/machine-learning/03_ridger_regression_gradient_descent
RJ=$NS/recreated_pptx/qa/rejudge_20261027
LOG=$RJ/r17_shardB_harvest.log
SCOPE="018 019 020 021 022 023 024 026 027 028 029 030 031 032 034"

clean() { [ -f "$1" ] && grep -q 'FINAL VERDICT' "$1" 2>/dev/null && ! grep -qi '429' "$1" 2>/dev/null; }
verdict() { grep -oE 'FINAL VERDICT: *\*{0,2} *(PASS|FAIL)' "$1" | tail -1 | grep -oE 'PASS|FAIL'; }
has_key() { grep -q "^$2=" "$RJ/slide$1/result.txt" 2>/dev/null; }
ts_of() { stat -c %y "$1" | cut -d. -f1 | sed 's/ /_/'; }
log() { echo "$(date -u +%FT%TZ) r17B $*" >> "$LOG"; }

harvest_leg() { # N full|crop target adjudicate_mode
  local N=$1 leg=$2 T=$3 mode=$4 D=$RJ/slide$N KEY
  KEY=$(echo "$leg" | tr a-z A-Z)  # FULL or CROP
  local V=$(verdict "$T")
  local line="R17_${KEY}=${V}"
  [ "$V" = PASS ] || line="$line (PIL census banked: slide$N/adjudicate_r17_${leg}.txt — classification by orchestrator)"
  {
    echo "$line"
    echo "R17_${KEY}_TRANSCRIPT=$T"
    echo "R17_${KEY}_VERDICT_TS=$(ts_of "$T") UTC (clean, no 429)"
    echo "R17_${KEY}_WRITTEN=$(date -u +%FT%TZ) r17 shard B harvest"
  } >> "$D/result.txt"
  if [ "$V" = FAIL ]; then
    python3 "$RJ/rejudge_adjudicate.py" "$N" "$mode" > "$D/adjudicate_r17_${leg}.txt" 2>&1
  fi
  log "HARVEST $N $leg=$V from $(basename "$T")"
}

log "monitor start pid=$$"
while true; do
  done_count=0
  for N in $SCOPE; do
    D=$RJ/slide$N
    [ -f "$D/result.txt" ] || continue
    if ! has_key "$N" R17_FULL; then
      T=$D/judge_full_r17.txt
      if clean "$T"; then harvest_leg "$N" full "$T" --full; else log "wait $N full (no clean r17 yet)"; fi
    fi
    if ! has_key "$N" R17_CROP; then
      T=$D/crop_dense_judge_r17.txt
      if clean "$T"; then harvest_leg "$N" crop "$T" --crop; else log "wait $N crop (no clean r17 yet)"; fi
    fi
    has_key "$N" R17_FULL && has_key "$N" R17_CROP && done_count=$((done_count+1))
  done
  log "pass: $done_count/15 slides fully harvested"
  [ "$done_count" -eq 15 ] && { log "ALL_DONE"; break; }
  sleep 60
done
