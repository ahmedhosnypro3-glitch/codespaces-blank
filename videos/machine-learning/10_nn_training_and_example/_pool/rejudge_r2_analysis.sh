#!/usr/bin/env bash
# scope_r2 fresh-analysis runner: storm-resilient, atomic banking, never aborts.
set -u
VID=/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example
P=/home/codespace/ai_llm_slides/scripts
LOG="$VID/_pool/storm_log/storm_r2_analysis.log"
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

run_step(){ # label script outfile field slide [args...]
  local label="$1" script="$2" out="$3" field="$4" n="$5"; shift 5
  local attempt=1
  while [ "$attempt" -le 3 ]; do
    log "STEP $label slide=$n attempt=$attempt start"
    local tmp="$VID/_pool/storm_log/r2_${label}_${n}_a${attempt}.log"
    TMPDIR="$VID/_pool" timeout 900 python3 "$script" "$@" > "$tmp" 2>&1
    local rc=$?
    if [ "$rc" -eq 0 ] && [ -f "$out" ] && valid_json "$out" "$field"; then
      log "STEP $label slide=$n attempt=$attempt OK rc=$rc banked=$out"
      return 0
    fi
    log "STEP $label slide=$n attempt=$attempt FAIL rc=$rc out_exists=$([ -f "$out" ] && echo yes || echo no)"
    grep -iE "502|504|bad gateway|gateway timeout|ServiceTimeout|error" "$tmp" | head -5 >> "$LOG"
    if [ "$attempt" -lt 3 ]; then
      log "STORM sleep 120s before retry of $label slide=$n"
      sleep 120
    fi
    attempt=$((attempt+1))
  done
  log "STEP $label slide=$n EXHAUSTED after 3 attempts"
  return 1
}

for N in 4 5 6; do
  PNN=$(printf "%03d" "$N")
  rm -f "$VID/analysis/reanalysis/slide_${PNN}_raw.json"
  run_step analysis "$P/12_analyze_slides.py" \
    "$VID/analysis/reanalysis/slide_${PNN}_raw.json" slide_title "$N" \
    "$VID/unique_slides" "$VID/analysis/reanalysis" --from "$N" --to "$N" --slides 10
  rc_a=$?
  if [ "$rc_a" -ne 0 ]; then
    log "STEP analysis slide=$N FAILED-3X — recording task, continuing to validation/judge"
    bash /home/codespace/.agents/skills/pooled-missions/scripts/pool-db.sh task-add \
      "$VID/_pool/mission.db" scope_r2 "slide_${PNN}_analysis" \
      "fresh analysis exhausted 3 retries (storm clause); judge proceeds without fresh analysis" >> "$LOG" 2>&1
  fi
  run_step validation "$P/13_validate_slides.py" \
    "$VID/analysis/reanalysis/slide_${PNN}_final.json" slide_title "$N" \
    "$VID/analysis/reanalysis" --from "$N" --to "$N" --slides 10
  rc_v=$?
  if [ "$rc_v" -ne 0 ]; then
    log "STEP validation slide=$N FAILED-3X — recording task, continuing"
    bash /home/codespace/.agents/skills/pooled-missions/scripts/pool-db.sh task-add \
      "$VID/_pool/mission.db" scope_r2 "slide_${PNN}_validation" \
      "fresh validation exhausted 3 retries (storm clause); judge proceeds" >> "$LOG" 2>&1
  fi
done
log "ALL STEPS COMPLETE"
