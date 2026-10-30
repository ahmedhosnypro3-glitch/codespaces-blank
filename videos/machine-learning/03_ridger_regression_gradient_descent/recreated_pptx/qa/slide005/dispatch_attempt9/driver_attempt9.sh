#!/usr/bin/env bash
# Slide 005 attempt-9 judge driver.
#
# Protocol (as assigned):
#   * fire ONE leg at a time: Template A full-slide first, then the four
#     Procedure B crop-pair legs;
#   * before EVERY leg, re-check the fleet occupancy meter; if it reads >= 8,
#     sleep 600 s and re-check rather than dumping into congestion;
#   * heartbeat the DB on every poll cycle (VIDEO-prefixed, always);
#   * never retry a leg in a loop — one dispatch per leg, and a leg whose
#     transcript already carries a real FINAL VERDICT is skipped;
#   * stop after the last leg.
#
# Legs are dispatched through the staged scripts, which already carry the
# approved walls: --thinking high --max-tokens 65536 --timeout 1200 inside
# `timeout 1700`, via scripts/16_vision_gate.sh.
set -u
ROOT="/home/ahmed/Projects/ai_llm_slides"
cd "$ROOT" || exit 9
export TMPDIR="$ROOT/scratch/tmp"
VIDEO_NS="machine-learning/03_ridger_regression_gradient_descent"
Q="$ROOT/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide005"
WID="${WID:-slide005-judge9-1024192313}"
LOG="$Q/measure_attempt9/driver_leg_log.txt"

hb() {
  VIDEO="$VIDEO_NS" python3 scripts/15_progress.py heartbeat 005 "$WID" >/dev/null 2>&1
  echo "$(date -u +%Y-%m-%dT%H:%M:%SZ) $*" | tee -a "$LOG"
}

# wait for the gate meter to read < 8; one check per 600 s
await_gate() {
  while :; do
    C=$(pgrep -c -f analyze_image.py 2>/dev/null || echo 0)
    A=$(ps -eo args | grep -c "^/.*python3 .*analyze_image.py" 2>/dev/null || echo 0)
    hb "gate_check gate_count=$C analyzer_procs=$A"
    if [ "$C" -lt 8 ]; then
      echo "$(date -u +%Y-%m-%dT%H:%M:%SZ) GATE OPEN ($C < 8) — dispatching $1" | tee -a "$LOG"
      return 0
    fi
    hb "gate closed ($C >= 8) — sleep 600 before re-probe"
    sleep 600
  done
}

run_leg() {
  local script="$1" transcript="$2"
  if python3 "$Q/dispatch_attempt9/check_transcript.py" "$transcript" >/dev/null 2>&1; then
    hb "SKIP $script — $transcript already carries a real FINAL VERDICT"
    return 0
  fi
  await_gate "$(basename "$script")"
  hb "dispatch $script"
  bash "$script" >>"$LOG" 2>&1
  local rc=$?
  hb "leg finished $script rc=$rc"
  python3 "$Q/dispatch_attempt9/check_transcript.py" "$transcript" >>"$LOG" 2>&1
  return 0
}

run_leg "$Q/dispatch_attempt9/leg_A_full_slide.sh"      "$Q/judge_attempt_9.txt"
run_leg "$Q/dispatch_attempt9/leg_B_eq_stack.sh"        "$Q/crop_9_eq_stack_judge.txt"
run_leg "$Q/dispatch_attempt9/leg_B_blue_upper.sh"      "$Q/crop_9_blue_upper_judge.txt"
run_leg "$Q/dispatch_attempt9/leg_B_pink_band.sh"       "$Q/crop_9_pink_band_judge.txt"
run_leg "$Q/dispatch_attempt9/leg_B_lower_eqs.sh"       "$Q/crop_9_lower_eqs_judge.txt"
hb "ALL LEGS DISPATCHED — verify transcripts, adjudicate, certify"
