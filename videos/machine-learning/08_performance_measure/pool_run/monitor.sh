#!/usr/bin/env bash
# Monitoring script for pooled slide recreation — restart analysis or validation if down
# Runs every 15 minutes via cron

VIDEO_DIR="/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure"
LOG_FILE="$VIDEO_DIR/pool_run/monitor.log"
ANALYSIS_DIR="$VIDEO_DIR/analysis"
UNIQUE_SLIDES_DIR="$VIDEO_DIR/unique_slides"
PROJECT_ROOT="/home/codespace/ai_llm_slides"
DB="$VIDEO_DIR/pool_run/mission.db"
DBCTL="/home/codespace/.agents/skills/pooled-missions/scripts/pool-db.sh"
# cron's stripped env resolves python3 to a shim lacking the openai module;
# pin the pyenv interpreter that has it (AGENTS.md endpoint contract).
PYBIN="/home/codespace/.pyenv/versions/3.15.2/bin/python3"

mkdir -p "$(dirname "$LOG_FILE")"

{
  echo "=== Monitor run $(date) ==="
  
  # Check if analysis is running
  if ! pgrep -f "12_analyze_slides.py.*08_performance_measure" > /dev/null; then
    echo "Analysis process DOWN - restarting..."
    cd "$PROJECT_ROOT" && nohup "$PYBIN" scripts/12_analyze_slides.py "$UNIQUE_SLIDES_DIR" "$ANALYSIS_DIR" --slides 37 >> "$VIDEO_DIR/pool_run/analysis.log" 2>&1 &
    echo "Analysis restarted (PID: $!)"
  else
    echo "Analysis process RUNNING"
  fi

  # Check validation
  if ! pgrep -f "13_validate_slides.py.*08_performance_measure" > /dev/null; then
    echo "Validation process DOWN - restarting..."
    cd "$PROJECT_ROOT" && IR_MAX_TOKENS=65536 nohup "$PYBIN" scripts/13_validate_slides.py "$ANALYSIS_DIR" --slides 37 >> "$VIDEO_DIR/pool_run/validation.log" 2>&1 &
    echo "Validation restarted (PID: $!)"
  else
    echo "Validation process RUNNING"
  fi

  # Check mission DB status
  echo "--- Mission DB Status ---"
  /home/codespace/.agents/skills/pooled-missions/scripts/pool-db.sh status "$DB"

  # Progress summary
  RAW_COUNT=$(ls "$ANALYSIS_DIR"/*_raw.json 2>/dev/null | wc -l)
  FINAL_COUNT=$(ls "$ANALYSIS_DIR"/*_final.json 2>/dev/null | wc -l)
  REANA_COUNT=$(ls "$ANALYSIS_DIR/reanalysis"/*_raw.json 2>/dev/null | wc -l)
  PPTX_COUNT=$(ls "$VIDEO_DIR/recreated_pptx"/slide_*_recreated.pptx 2>/dev/null | wc -l)
  PASS_COUNT=$(grep -l "FINAL VERDICT: PASS" "$VIDEO_DIR/recreated_pptx/qa"/slide*/judge_attempt_*.txt 2>/dev/null | wc -l)
  VERIFY_COUNT=$(grep -l "FINAL VERDICT: PASS" "$VIDEO_DIR/recreated_pptx/qa"/slide*/judge_verify_*.txt 2>/dev/null | wc -l)
  echo "Progress: Raw=$RAW_COUNT/37 Final=$FINAL_COUNT/37 Reanalysis=$REANA_COUNT/37 PPTX=$PPTX_COUNT/37 PASS=$PASS_COUNT/37 Corroborated=$VERIFY_COUNT/37"

  # Orphaned build lanes (DB heartbeat is the liveness truth, never file mtime)
  echo "--- Zombie sweep ---"
  cd "$PROJECT_ROOT" && VIDEO=machine-learning/08_performance_measure "$PYBIN" scripts/15_progress.py sweep --stale-min 30 2>&1 | tail -20

  # Cross-check: a slide whose pooled-missions scope is still in_work is OWNED even when
  # the progress DB row is unclaimed (workers that skipped 15_progress.py claim).
  echo "--- True orphans (unclaimed AND scope not in_work) ---"
  ORPHANS=""
  for s in 2 5 6 18 19 20 25 26 27 28; do
    sc_state=$("$DBCTL" scope-list "$DB" 2>/dev/null | awk -F'|' -v n="slide-$s" '{gsub(/ /,"",$1); gsub(/ /,"",$2); if ($1 == n) print $2}')
    [ "$sc_state" = "in_work" ] || ORPHANS="$ORPHANS $s"
  done
  echo "orphans:${ORPHANS:- none}"

  echo "=== Verify wave (dual-read certification + re-analysis) ==="
  "$VIDEO_DIR/pool_run/verify_wave.sh" >> "$LOG_FILE" 2>&1
  echo "  verify exit=$?"

  echo "=== Monitor run complete ==="
  echo ""
} >> "$LOG_FILE" 2>&1