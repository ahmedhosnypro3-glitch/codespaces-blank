#!/usr/bin/env bash
# Spin-acquire vision gate slot: all 4 slots are tried non-blocking in a loop so
# a waiter can grab ANY slot that frees (the stock gate blocks on slot_0 only and
# starves under fleet-wide saturation). Usage: vg_spin.sh <cmd...>
set -u
VGATE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/.vgate"
mkdir -p "$VGATE"
N="${VISION_SLOTS:-4}"
for attempt in $(seq 1 600); do
  for i in $(seq 0 $((N - 1))); do
    exec 9>>"$VGATE/slot_$i.lock"
    if flock -n 9; then
      "$@"
      rc=$?
      flock -u 9
      exec 9>&-
      exit $rc
    fi
    exec 9>&-
  done
  sleep 5
done
echo "vg_spin: no slot acquired after 600 attempts" >&2
exit 7
