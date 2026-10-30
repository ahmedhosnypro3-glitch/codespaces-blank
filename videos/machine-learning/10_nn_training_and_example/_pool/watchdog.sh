#!/usr/bin/env bash
# Watchdog for pooled mission - runs every 15 minutes via cron
# Detects zombie workers (stale heartbeat >= 120 min) and respawns them
# Uses file activity as additional liveness signal for agent workers

set -euo pipefail

VIDEO_DIR="/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example"
POOL_DIR="$VIDEO_DIR/_pool"
DB="$POOL_DIR/mission.db"
LOG="$POOL_DIR/watchdog.log"
STALE_MIN="${STALE_MIN:-120}"  # long judge/measurement phases need time
ACTIVE_MIN="${ACTIVE_MIN:-90}"  # recent file activity window for the liveness escape
PIN="$POOL_DIR/pinned_scopes"   # scopes owned by a live worker: never zombie them

mkdir -p "$POOL_DIR"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" | tee -a "$LOG"
}

if ! command -v sqlite3 >/dev/null 2>&1; then
    log "sqlite3 not found, exiting"
    exit 1
fi

if [[ ! -f "$DB" ]]; then
    log "DB not found at $DB, exiting"
    exit 1
fi

log "=== Watchdog sweep started ==="

# Get scopes with in_work status and their updated_at
zombies=$(sqlite3 "$DB" "SELECT name, COALESCE(agent, ''), updated_at FROM scopes WHERE status = 'in_work';")

while IFS='|' read -r scope_name agent_name updated_at; do
    if [[ -z "$scope_name" ]]; then continue; fi
    # Compute minutes since last DB update
    last_epoch=$(date -d "$updated_at" +%s 2>/dev/null || echo 0)
    now_epoch=$(date +%s)
    age_min=$(( (now_epoch - last_epoch) / 60 ))
    
    if [[ $age_min -ge $STALE_MIN ]]; then
        if [[ -f "$PIN" ]] && grep -qxF "$scope_name" "$PIN"; then
            log "Scope $scope_name: DB stale (${age_min}min) but PINNED (live worker) — skipping"
            continue
        fi
        # Additional check: file activity in slide dirs for this scope
        # Get slide numbers from scope items
        items=$(sqlite3 "$DB" "SELECT items FROM scopes WHERE name='$scope_name';")
        has_activity=0
        for slide in $(echo "$items" | tr ',' ' '); do
            # Match slide_010, slide_10, and qa/slide003 naming variants
            pat="slide_0*${slide}[_.]"
            if find "$VIDEO_DIR/analysis" "$VIDEO_DIR/analysis/parse" "$VIDEO_DIR/analysis/reanalysis" \
                     "$VIDEO_DIR/recreated_pptx/build" "$VIDEO_DIR/qa" "$VIDEO_DIR/_pool" \
                     -maxdepth 2 -regextype posix-extended \
                     -regex ".*(${pat}|qa/slide[0]?${slide}(/|_)|rejudge/.*${slide}).*" \
                     -mmin -"$ACTIVE_MIN" 2>/dev/null | grep -q .; then
                has_activity=1
                break
            fi
        done
        
        if [[ $has_activity -eq 1 ]]; then
            log "Scope $scope_name: DB stale (${age_min}min) but file activity detected — NOT a zombie, skipping"
            continue
        fi
        
        log "ZOMBIE detected: scope=$scope_name agent=$agent_name age=${age_min}min last_update=$updated_at (no file activity)"
        # Fail the scope (releases claim)
        /home/codespace/.agents/skills/pooled-missions/scripts/pool-db.sh scope-fail "$DB" "$scope_name" "zombie: heartbeat stale ${age_min}min" >>"$LOG" 2>&1
        # Log respawn event
        log "Respawning worker for scope $scope_name"
        /home/codespace/.agents/skills/pooled-missions/scripts/pool-db.sh event "$DB" watchdog-respawn "scope=$scope_name agent=$agent_name age=${age_min}min" >>"$LOG" 2>&1
    fi
done <<< "$zombies"

log "=== Watchdog sweep complete ==="