#!/usr/bin/env bash
# Namespace-local vision concurrency gate for 10_nn_training_and_example.
# Caps THIS fleet's concurrent vision calls (the shared gateway is saturated
# fleet-wide). Same flock-slot pattern as the project-root 16_vision_gate.sh,
# but with its own lock dir inside this namespace.
#
# Usage: _pool/vision_gate.sh <command> [args...]
set -u
N="${VISION_SLOTS:-4}"
LOCKDIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/.vgate"
mkdir -p "$LOCKDIR"

for i in $(seq 0 $((N - 1))); do
    exec 9>>"$LOCKDIR/slot_$i.lock"
    if flock -n 9; then
        "$@"
        rc=$?
        flock -u 9
        exit $rc
    fi
    exec 9>&-
done

# all slots busy — block on slot 0
exec 9>>"$LOCKDIR/slot_0.lock"
flock 9
"$@"
rc=$?
flock -u 9
exit $rc
