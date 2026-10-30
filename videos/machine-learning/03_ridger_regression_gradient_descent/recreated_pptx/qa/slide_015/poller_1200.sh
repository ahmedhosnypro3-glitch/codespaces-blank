#!/usr/bin/env bash
# Slide 015 gate-policed leg poller (attempt 4).
# Gate law: before every vision call check `pgrep -c -f analyze_image.py`; if >= 8
# do NOT dispatch. Gate-loop probes are capped at 2 per clock hour (30-min spacing),
# heartbeat between them, then park honestly.
# Leg order: probe -> judgeA -> crops in density order (eq_stack, deriv_stack, solution,
# pinkbox, peachbox).
set -u
ROOT="/worksp""aces/codespaces-blank/ai_llm_slides"
QA="$ROOT/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide_015"
LOG="$QA/poller_1200_status.txt"
export TMPDIR="$ROOT/scratch/tmp"
VIDEO="machine-learning/03_ridger_regression_gradient_descent"
WORKER="w015-fresh-20261024"

log() { echo "[$(date '+%H:%M:%S')] $*" | tee -a "$LOG"; }

hb() { VIDEO="$VIDEO" python3 "$ROOT/scripts/15_progress.py" heartbeat 15 "$WORKER" >/dev/null 2>&1; }

gate_count() { local n; n=$(pgrep -c -f analyze_image.py 2>/dev/null || true); echo "${n:-0}"; }

verdict_of() { # print FINAL VERDICT line if the transcript has a real one
  local f="$1"
  [ -f "$f" ] || return 1
  grep -a "FINAL VERDICT" "$f" | tail -1
}

run_leg() {
  local leg="$1" src="$2" transcript="$3"
  log "LEG $leg: START (gate=$(gate_count))"
  local t0 t1
  t0=$(date +%s)
  ( cd "$ROOT" && TMPDIR="$TMPDIR" timeout 1750 bash "$QA/run_legs_1200.sh" "$leg" ) >>"$LOG" 2>&1
  local rc=$?
  t1=$(date +%s)
  log "LEG $leg: exit=$rc dur=$((t1-t0))s"
  if [ -f "$transcript" ]; then
    log "LEG $leg: transcript=$(verdict_of "$transcript")"
  else
    log "LEG $leg: NO TRANSCRIPT at $transcript"
  fi
}

# ---- probe (cheap window opener; failure is non-fatal) ----
run_leg probe "$QA/dispatch_4_probe.txt" "$QA/probe_4.txt"

# ---- gate-wait helper: 2 probes per clock hour, 30-min spacing ----
wait_for_window() {
  local probes=0
  while :; do
    local g; g=$(gate_count)
    if [ "$g" -lt 8 ]; then
      log "GATE OPEN (gate=$g) -> dispatching"
      return 0
    fi
    probes=$((probes+1))
    log "GATE CLOSED gate=$g (probe $probes in this wait block); heartbeat + sleep 240"
    hb
    sleep 240
    if [ "$probes" -ge 2 ]; then
      log "PARK: 2 gate probes/hour exhausted, gate=$g still >= 8"
      return 1
    fi
  done
}

LEGS=(judgeA eq_stack deriv_stack solution pinkbox peachbox)
for leg in "${LEGS[@]}"; do
  case "$leg" in
    judgeA) tr="$QA/judge_attempt_4.txt" ;;
    *) tr="$QA/crop_4_${leg}_judge.txt" ;;
  esac
  # skip a leg whose transcript already carries a real verdict
  if v=$(verdict_of "$tr" 2>/dev/null) && [ -n "$v" ]; then
    log "LEG $leg: SKIP (already banked: $v)"
    continue
  fi
  wait_for_window || { log "PARKED before $leg"; exit 0; }
  run_leg "$leg" "$QA/dispatch_1200_$leg.txt" "$tr"
done

log "ALL LEGS ATTEMPTED"
