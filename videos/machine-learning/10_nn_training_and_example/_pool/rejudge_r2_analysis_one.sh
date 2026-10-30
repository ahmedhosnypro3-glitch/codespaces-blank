#!/usr/bin/env bash
# scope_r2 fresh analysis+validation for ONE slide: storm-resilient, atomic, never aborts.
# usage: rejudge_r2_analysis_one.sh <N>
set -u
VID=/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example
P=/home/codespace/ai_llm_slides/scripts
DB=/home/codespace/.agents/skills/pooled-missions/scripts/pool-db.sh
N="$1"
PNN=$(printf "%03d" "$N")
LOG="$VID/_pool/storm_log/storm_r2_analysis_${N}.log"
mkdir -p "$VID/analysis/reanalysis" "$VID/_pool/storm_log"
log(){ printf '%s %s\n' "$(date '+%Y-%m-%d %H:%M:%S')" "$*" >> "$LOG"; }

valid_json(){ python3 - "$1" "$2" <<'EOF'
import json,sys
try:
    d=json.load(open(sys.argv[1]))
except Exception:
    sys.exit(1)
sys.exit(0 if d.get(sys.argv[2]) not in (None,"",[],{}) else 1)
EOF
}

run_step(){
  local label="$1" script="$2" out="$3" field="$4"; shift 4
  local attempt=1
  while [ "$attempt" -le 3 ]; do
    log "STEP $label slide=$N attempt=$attempt start"
    local tmp="$VID/_pool/storm_log/r2_${label}_${N}_a${attempt}.log"
    TMPDIR="$VID/_pool" timeout 2400 python3 "$script" "$@" > "$tmp" 2>&1
    local rc=$?
    if [ "$rc" -eq 0 ] && [ -f "$out" ] && valid_json "$out" "$field"; then
      log "STEP $label slide=$N attempt=$attempt OK banked=$out"
      return 0
    fi
    log "STEP $label slide=$N attempt=$attempt FAIL rc=$rc"
    grep -iE "502|504|bad gateway|gateway timeout|ServiceTimeout|Stream ended" "$tmp" | head -5 >> "$LOG"
    if [ "$attempt" -lt 3 ]; then
      log "STORM sleep 120s before retry of $label slide=$N"
      sleep 120
    fi
    attempt=$((attempt+1))
  done
  log "STEP $label slide=$N EXHAUSTED after 3 attempts"
  return 1
}

RAW="$VID/analysis/reanalysis/slide_${PNN}_raw.json"
FIN="$VID/analysis/reanalysis/slide_${PNN}_final.json"
log "=== lane slide=$N begin ==="
if [ -f "$RAW" ] && valid_json "$RAW" slide_title; then
  log "STEP analysis slide=$N SKIP: banked raw already valid"
else
  rm -f "$RAW"
  run_step analysis "$P/12_analyze_slides.py" "$RAW" slide_title \
    "$VID/unique_slides" "$VID/analysis/reanalysis" --from "$N" --to "$N" --slides 10
  if [ $? -ne 0 ]; then
    log "STEP analysis slide=$N FAILED-3X — recording task, continuing to validation/judge"
    bash "$DB" task-add "$VID/_pool/mission.db" scope_r2 "slide_${PNN}_analysis" \
      "fresh analysis exhausted 3 retries (storm clause); judge proceeds" >> "$LOG" 2>&1
  fi
fi
if [ -f "$FIN" ] && valid_json "$FIN" slide_title; then
  log "STEP validation slide=$N SKIP: banked final already valid"
else
  run_step validation "$P/13_validate_slides.py" "$FIN" slide_title \
    "$VID/analysis/reanalysis" --from "$N" --to "$N" --slides 10
  if [ $? -ne 0 ]; then
    log "STEP validation slide=$N FAILED-3X — recording task, continuing"
    bash "$DB" task-add "$VID/_pool/mission.db" scope_r2 "slide_${PNN}_validation" \
      "fresh validation exhausted 3 retries (storm clause); judge proceeds" >> "$LOG" 2>&1
  fi
fi
log "=== lane slide=$N done ==="
