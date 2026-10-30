#!/usr/bin/env bash
# verify_loop.sh — run the verify wave on a cadence while any slide is
# uncorroborated. Never exits early: zero certified slides is a valid state.
#
# Each iteration is a full verify_wave.sh run (idempotent). After a wave that
# judged at least one new slide, the spec-drift check runs against whatever
# reanalysis landed.
set -uo pipefail

VIDEO_DIR="/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure"
LOG="$VIDEO_DIR/pool_run/verify_wave.log"
DRIFT_LOG="$VIDEO_DIR/pool_run/spec_drift.md"
PYBIN="/home/codespace/.pyenv/versions/3.15.2/bin/python3"
INTERVAL="${VERIFY_INTERVAL:-600}"
MAX_ITERS="${VERIFY_MAX_ITERS:-24}"

log() { echo "[$(date '+%F %T')] LOOP: $*" >>"$LOG"; }

log "verify_loop starting (interval=${INTERVAL}s max_iters=$MAX_ITERS)"
i=0
while [ "$i" -lt "$MAX_ITERS" ]; do
  i=$((i+1))
  before_ledger=$(wc -l <"$VIDEO_DIR/pool_run/verification_ledger.md" 2>/dev/null || echo 0)
  log "iteration $i/$MAX_ITERS: running verify wave"
  timeout 1500 bash "$VIDEO_DIR/pool_run/verify_wave.sh" >>"$LOG" 2>&1
  after_ledger=$(wc -l <"$VIDEO_DIR/pool_run/verification_ledger.md" 2>/dev/null || echo 0)

  if [ "$after_ledger" -gt "$before_ledger" ]; then
    log "iteration $i: ledger grew ($before_ledger -> $after_ledger) — running spec-drift check"
    "$PYBIN" "$VIDEO_DIR/pool_run/spec_drift_check.py" \
      "$VIDEO_DIR/analysis" "$VIDEO_DIR/analysis/reanalysis" "$DRIFT_LOG" >>"$LOG" 2>&1
  fi

  if [ "$i" -lt "$MAX_ITERS" ]; then
    log "iteration $i: sleeping ${INTERVAL}s"
    sleep "$INTERVAL"
  fi
done
log "verify_loop finished after $i iterations"
