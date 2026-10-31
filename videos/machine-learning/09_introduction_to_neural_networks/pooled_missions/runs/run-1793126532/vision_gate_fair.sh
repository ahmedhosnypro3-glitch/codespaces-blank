#!/usr/bin/env bash
# Fair-slot vision gate. Uses the SAME lock files as scripts/16_vision_gate.sh
# (so the 16-slot fleet cap is unchanged) but acquires a random free slot
# instead of convoying every blocked caller onto slot 0. Exit 75 = no slot
# acquired within GATE_WAIT seconds (retryable, no call was made).
set -u
LOCKDIR="${TMPDIR:-/tmp}"
WAIT="${GATE_WAIT:-240}"
for attempt in 1 2 3 4 5 6 7 8; do
  for j in $(seq 0 15); do
    i=$(( (RANDOM + j) % 16 ))
    exec {fd}>>"$LOCKDIR/ir_vision_gate_$i.lock"
    if flock -n $fd; then
      "$@"; rc=$?
      flock -u $fd; exec {fd}>&-
      exit $rc
    fi
    exec {fd}>&-
  done
  i=$(( RANDOM % 16 ))
  exec {fd}>>"$LOCKDIR/ir_vision_gate_$i.lock"
  if flock -w "$WAIT" $fd; then
    "$@"; rc=$?
    flock -u $fd; exec {fd}>&-
    exit $rc
  fi
  exec {fd}>&-
done
exit 75
