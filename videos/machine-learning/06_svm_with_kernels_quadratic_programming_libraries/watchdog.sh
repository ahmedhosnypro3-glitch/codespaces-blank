#!/usr/bin/env bash
# Pooled-missions watchdog for the 06_svm rejudge wave.
# Observes liveness, parks dead scopes as failed, and refills emptied slots
# by writing spawn requests the main-agent loop picks up on its next turn.
set -u

DBCTL="$HOME/.agents/skills/pooled-missions/scripts/pool-db.sh"
DB="/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries/mission.db"
LOG="/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries/watchdog.log"
SPAWNQ="$HOME/.agents/scratch/06_svm_rej_spawn_queue.txt"
STALE_THRESHOLD_MIN=20
WAVE_PREFIX="scope_rej_"

ts() { date '+%F %T'; }
log() { echo "[$(ts)] $*" >> "$LOG"; }

log "=== watchdog start ==="
mkdir -p "$(dirname "$SPAWNQ")"

# Snapshot status BEFORE, so we only fail genuinely-new stalls (idempotent re-runs).
sqlite3 -cmd ".timeout 15000" "$DB" "SELECT COUNT(*) FROM scopes WHERE status='in_work';" >/dev/null 2>&1 || {
  log "DB unreachable — aborting this tick"; log "=== watchdog end ==="; exit 0;
}

UNRESOLVED=0
while IFS='|' read -r name status agent items; do
  [ "${status:-}" = "in_work" ] || continue
  updated=$(sqlite3 -cmd ".timeout 15000" "$DB" "SELECT updated_at FROM scopes WHERE name='$name';" 2>/dev/null || echo "")
  [ -n "$updated" ] || continue
  now_epoch=$(date +%s); upd_epoch=$(date -d "$updated" +%s 2>/dev/null || echo "$now_epoch")
  age_min=$(( (now_epoch - upd_epoch) / 60 ))
  if [ "$age_min" -gt "$STALE_THRESHOLD_MIN" ]; then
    # Which of this scope's slides still lack a resolved verdict?
    for it in $(echo "$items" | tr ',' ' '); do
      n=$(printf "%03d" "$it")
      if ! grep -q "\"slide\": \"$n\", \"attempt_placeholder\": null" "$SPAWNQ" 2>/dev/null; then :; fi
    done
    # Mark the scope failed so its slides become re-dispatchable, then queue a fresh worker.
    "$DBCTL" scope-fail "$DB" "$name" "watchdog: stalled ${age_min}min, parked for redispatch" >/dev/null
    "$DBCTL" event "$DB" watchdog "failed stale $name (${age_min}min) -> redispatch"
    echo "$name" >> "$SPAWNQ"
    log "STALLED $name age=${age_min}min -> failed + queued for fresh dispatch"
    UNRESOLVED=$((UNRESOLVED+1))
  else
    log "healthy $name age=${age_min}min agent=$agent"
  fi
done < <("$DBCTL" scope-list "$DB" 2>/dev/null)

done_count=$("$DBCTL" scope-list "$DB" done 2>/dev/null | grep -c 'done' || true)
log "summary total=$("$DBCTL" scope-list "$DB" 2>/dev/null | grep -c '|' ) done=$done_count parked=$UNRESOLVED"
log "=== watchdog end ==="
