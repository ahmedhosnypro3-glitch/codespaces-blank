#!/bin/bash
# Lane E: fresh doc-parse crop-cascade over original frames slide_001..slide_019
# of videos/machine-learning/08_performance_measure, one cascade per frame into
# pool_run/docparse_e2/slide0NN/.
#
# Budgets per tasking: --max-crops 16 --max-parse-calls 24 --max-depth 6
# --max-retries 6 --max-parallel 2.
# One cascade at a time; 60-90s pacing between slides.
# On failure: backoff 120-300s, up to 6 attempts per slide.
# Pre-existing cascade dirs are MOVED to _archive/ (never deleted).
set -u
NS=/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure
SKILL=$HOME/.agents/skills/doc-parse
E2=$NS/pool_run/docparse_e2
LOG=$E2/run.log
cd "$NS"

log() { echo "$(date -Iseconds) $*" >> "$LOG"; }

log "laneE driver start pid=$$ slides=001-019"

FIRST=1
for N in 001 002 003 004 005 006 007 008 009 010 011 012 013 014 015 016 017 018 019; do
  OUT=$E2/slide${N}
  if [ -d "$OUT" ]; then
    TS=$(date +%Y%m%d-%H%M%S)
    mv "$OUT" "$E2/_archive/slide${N}_laneE_${TS}"
    log "archived pre-existing slide${N} -> _archive/slide${N}_laneE_${TS}"
  fi
  if [ $FIRST -eq 0 ]; then
    P=$((60 + RANDOM % 31))
    log "pacing ${P}s before slide${N}"
    sleep $P
  fi
  FIRST=0
  ATTEMPT=1
  MAX_ATTEMPTS=6
  while [ $ATTEMPT -le $MAX_ATTEMPTS ]; do
    log "=== slide${N} attempt $ATTEMPT start out=$OUT"
    python3 "$SKILL/scripts/crop_cascade.py" "unique_slides/slide_${N}.jpg" \
      --prompt-file "$SKILL/references/prompts/crop_decision.md" \
      --out "$OUT" \
      --max-crops 16 --max-parse-calls 24 --max-depth 6 \
      --max-retries 6 --max-parallel 2 \
      >> "$E2/slide${N}.cascade.log" 2>&1
    RC=$?
    log "=== slide${N} attempt $ATTEMPT rc=$RC"
    if [ $RC -eq 0 ] || [ $RC -eq 6 ]; then
      if python3 "$E2/health_check.py" "$OUT" >> "$LOG" 2>&1; then
        log "slide${N} OK on attempt $ATTEMPT"
        break
      else
        log "slide${N} attempt $ATTEMPT rc=$RC but health check FAILED"
      fi
    else
      log "slide${N} attempt $ATTEMPT rc=$RC (cascade aborted); log tail:"
      tail -3 "$E2/slide${N}.cascade.log" >> "$LOG" 2>&1
    fi
    if [ $ATTEMPT -ge $MAX_ATTEMPTS ]; then
      log "slide${N} EXHAUSTED after $MAX_ATTEMPTS attempts"
      break
    fi
    S=$((120 + RANDOM % 181))
    log "slide${N} attempt $ATTEMPT failed; backoff ${S}s"
    sleep $S
    ATTEMPT=$((ATTEMPT + 1))
  done
done

log "laneE driver done pid=$$"
