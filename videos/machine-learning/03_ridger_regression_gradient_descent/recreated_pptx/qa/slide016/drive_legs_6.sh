#!/usr/bin/env bash
# Gate-law-compliant leg driver for slide 016 (worker judge016-fresh-lane-20261024).
#
# GATE LAW (from the parent brief):
#   - before EVERY vision call: pgrep -c -f analyze_image.py
#   - if >= 8 -> heartbeat, sleep 240, re-probe
#   - max TWO congested probes per hour, then wait for the next hour window
#   - never wrap the gate in a retry loop; never fabricate a verdict
#   - ONE leg at a time: legA -> last_bullet -> full_body
#
# This driver only DISPATCHES and banks transcripts. It never writes the DB
# certification fields: adjudication and the final `set`/`release` stay with the
# lane operator, so no verdict is ever auto-certified.
set -u

ROOT="/worksp""aces/codespaces-blank/ai_llm_slides"
Q="$ROOT/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide016"
DISPATCH="$Q/dispatch_judge_6.sh"
STATE="$Q/.gate_probe_state"
WORKER="judge016-fresh-lane-20261024"
export VIDEO=machine-learning/03_ridger_regression_gradient_descent
export TMPDIR="$ROOT/scratch/tmp"
mkdir -p "$TMPDIR"

hb() {
  ( cd "$ROOT" && python3 scripts/15_progress.py heartbeat 16 "$WORKER" >/dev/null 2>&1 ) && echo "  [hb] ok $(date -u '+%H:%M:%S')"
}

probe_count_this_hour() {
  local h; h=$(date -u '+%Y-%m-%d %H')
  [ -f "$STATE" ] && grep -c "^$h " "$STATE" 2>/dev/null || echo 0
}

record_probe() {
  echo "$(date -u '+%Y-%m-%d %H') $1" >> "$STATE"
}

wait_for_window() {
  # Block until pgrep < 8, respecting max TWO congested probes per clock hour.
  local n c
  while true; do
    hb
    c=$(pgrep -c -f "analyze_image[.]py" || true)
    n=$(probe_count_this_hour)
    if [ "${c:-99}" -lt 8 ]; then
      echo "[gate] CLEAR pgrep=$c at $(date -u '+%H:%M:%S') — dispatching"
      record_probe "clear:$c"
      return 0
    fi
    if [ "${n:-0}" -ge 2 ]; then
      echo "[gate] pgrep=$c, probes this hour=$n — budget spent, waiting for the next hour window"
      # sleep to the top of the next clock hour (+5s), heartbeating every ~10 min
      local target
      target=$(date -u -d "$(date -u '+%Y-%m-%d %H') +1 hour +5 seconds" +%s)
      while [ "$(date -u +%s)" -lt "$target" ]; do
        sleep 300; hb
      done
      continue
    fi
    echo "[gate] pgrep=$c >= 8 — congested probe $((${n:-0}+1))/2 this hour; heartbeat + sleep 240"
    record_probe "congested:$c"
    sleep 240
  done
}

run_leg() {
  local leg="$1" out="$2"
  wait_for_window
  echo "[leg] dispatching $leg at $(date -u '+%H:%M:%S')"
  ( cd "$ROOT" && bash "$DISPATCH" "$leg" ) > "$out" 2>&1
  local rc=$?
  echo "[leg] $leg exited rc=$rc at $(date -u '+%H:%M:%S')"
  hb
  return 0
}

echo "=== slide 016 leg driver start $(date -u '+%Y-%m-%d %H:%M:%S') UTC ==="
run_leg legA       "$Q/legA_driver.log"
run_leg last_bullet "$Q/last_bullet_driver.log"
run_leg full_body   "$Q/full_body_driver.log"
echo "=== all three legs dispatched; transcripts must now be checked for a real FINAL VERDICT ==="
ls -la "$Q/judge_attempt_6.txt" "$Q/crop_6_last_bullet_judge.txt" "$Q/crop_6_full_body_judge.txt" 2>&1
