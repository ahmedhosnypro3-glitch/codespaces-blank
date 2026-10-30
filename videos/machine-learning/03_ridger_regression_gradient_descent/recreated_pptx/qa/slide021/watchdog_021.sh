#!/usr/bin/env bash
# slide 021 — crop-leg supervisor (NO vision dispatch of its own).
#
# Watches the four outstanding Procedure B crop legs and guarantees each one gets an
# attempt, without ever calling analyze_image.py itself:
#   - a leg counts as DONE only when its transcript has a REAL verdict body
#     (line-anchored "FINAL VERDICT: PASS|FAIL"), never an echoed payload line;
#   - while any dispatcher is alive, the supervisor does nothing;
#   - when no dispatcher is alive and legs are still missing, it relaunches the
#     existing dispatcher script for exactly those legs (the dispatcher owns the
#     gate check, the payload, and the single dispatch per leg).
# Any no-verdict transcript is archived (never deleted) before a relaunch so banked
# evidence is preserved.
set -u
ROOT="/worksp""aces/codespaces-blank/ai_llm_slides"
V="machine-learning/03_ridger_regression_gradient_descent"
QADIR="$ROOT/videos/$V/recreated_pptx/qa/slide021"
DISPATCH="$QADIR/dispatch_leg2_crops_fresh.sh"
LOG="$QADIR/watchdog_021.log"
WID="${WID:-w021-legs-20261024}"
POLL_EVERY="${POLL_EVERY:-60}"
POLL_MAX="${POLL_MAX:-21600}"
MAX_LAUNCHES="${MAX_LAUNCHES:-40}"
SLUGS="top_chain mid_table_eq mid_chain bot_eq_table"

ts() { date -u +%Y-%m-%dT%H:%M:%SZ; }
note() { echo "[$(ts)] $*" >> "$LOG"; }

cd "$ROOT"
note "watchdog started (WID=$WID, poll ${POLL_EVERY}s, cap ${POLL_MAX}s, max launches ${MAX_LAUNCHES})"

t0=$(date +%s)
launches=0
while :; do
  el=$(( $(date +%s) - t0 ))
  if [ "$el" -ge "$POLL_MAX" ]; then
    note "POLL CAP ${el}s reached — honest park, no leg fabricated, no vision dispatched"
    exit 42
  fi

  missing=""
  for s in $SLUGS; do
    f="$QADIR/crop_10_${s}_judge.txt"
    if [ ! -f "$f" ] || ! grep -qE '^FINAL VERDICT: (PASS|FAIL)\b' "$f" 2>/dev/null; then
      missing="$missing $s"
    fi
  done

  if [ -z "$missing" ]; then
    note "all four outstanding legs carry a real verdict body — watchdog done"
    exit 0
  fi

  running="$(pgrep -f "dispatch_leg2_crops_fresh.sh" | tr '\n' ' ')"
  if [ -n "$running" ]; then
    sleep "$POLL_EVERY"
    continue
  fi

  if [ "$launches" -ge "$MAX_LAUNCHES" ]; then
    note "MAX_LAUNCHES ${MAX_LAUNCHES} reached — honest park, still missing:${missing}"
    exit 43
  fi

  for s in $missing; do
    f="$QADIR/crop_10_${s}_judge.txt"
    if [ -f "$f" ]; then
      mv "$f" "$QADIR/crop_10_${s}_judge.noverdict.$(date -u +%Y%m%dT%H%M%SZ).bak"
      note "archived no-verdict transcript for $s (evidence preserved, not deleted)"
    fi
  done

  launches=$(( launches + 1 ))
  note "no dispatcher alive; relaunching for:${missing} (launch ${launches}/${MAX_LAUNCHES})"
  setsid env WID="$WID" SLUGS="${missing# }" POLL_MAX=21600 POLL_EVERY=240 \
    bash "$DISPATCH" >> "$QADIR/legs2_fresh_resume.log" 2>&1 < /dev/null &
  disown
  sleep "$POLL_EVERY"
done
