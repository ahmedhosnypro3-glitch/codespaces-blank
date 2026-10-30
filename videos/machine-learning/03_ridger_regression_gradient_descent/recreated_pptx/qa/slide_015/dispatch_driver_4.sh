#!/usr/bin/env bash
# Staged dispatch driver for slide 015, attempt 4 (render_4.png).
#
# Gate law (non-negotiable): before EACH vision call, read
#   pgrep -c -f analyze_image.py
# and dispatch ONLY if it is < 8.  While it is >= 8, heartbeat the DB row, sleep
# 240s, and re-probe.  Never retry-loop a single leg: one hard-wall retry max,
# and a degenerate/garbage winner body is a FAIL that must be retried at a new
# attempt count (3 garbage retries max).
#
# Usage:
#   ./dispatch_driver_4.sh              # runs the full leg sequence
#   ./dispatch_driver_4.sh probe        # only the probe
#   ./dispatch_driver_4.sh judgeA       # only the full-slide judge
#   ./dispatch_driver_4.sh crop SLUG    # only one crop pair
#
# Everything is run from the repo root, which is derived so the driver is not
# tied to one checkout path.
set -u
REPO=$(git rev-parse --show-toplevel) || exit 1
cd "$REPO" || exit 1

VIDEO=machine-learning/03_ridger_regression_gradient_descent
WORKER=w015-buildfirst-20261024
SLIDE=15
QA=videos/$VIDEO/recreated_pptx/qa/slide_015
GATE=scripts/16_vision_gate.sh
ANALYZE=.agents/skills/image-analysis/scripts/analyze_image.py

hb() { VIDEO=$VIDEO python3 scripts/15_progress.py heartbeat $SLIDE $WORKER >/dev/null 2>&1; }

load() { pgrep -c -f analyze_image.py 2>/dev/null || echo 0; }

# wait_for_gate <max_minutes> -> 0 if drained, 1 if still congested
wait_for_gate() {
  local cap=${1:-60} i=0 n
  while [ $i -lt $((cap * 60 / 240)) ]; do
    n=$(load)
    if [ "$n" -lt 8 ]; then
      echo "gate drained: ${n} concurrent analyze_image.py"
      return 0
    fi
    echo "gate congested: ${n} concurrent analyze_image.py - heartbeat, sleep 240"
    hb
    sleep 240
    i=$((i + 1))
  done
  echo "gate still congested after ${cap} min - PARKED"
  return 1
}

run() {  # run <dispatch file> <log file>
  local f=$1 log=$2 n
  n=$(load)
  if [ "$n" -ge 8 ]; then
    echo "REFUSED $f: gate at ${n} (>= 8). Not dispatched."
    return 2
  fi
  echo "dispatching $f (gate ${n})"
  bash "$f" > "$log" 2>&1
  echo "exit=$? log=$log"
}

do_probe() {
  wait_for_gate 60 || return 1
  run "$QA/dispatch_4_probe.txt" "$QA/probe_4_run.log"
  # a valid body opens the window; a hang means sleep 300 and re-probe ONCE
  if [ ! -s "$QA/probe_4.txt" ]; then
    echo "probe produced no transcript - one re-probe after sleep 300"
    hb; sleep 300
    run "$QA/dispatch_4_probe.txt" "$QA/probe_4_run2.log"
  fi
}

do_judgeA() {
  wait_for_gate 60 || return 1
  run "$QA/dispatch_4_judgeA.txt" "$QA/judge_4_run.log"
}

do_crop() {
  local slug=$1
  wait_for_gate 60 || return 1
  run "$QA/dispatch_4_crop_${slug}.txt" "$QA/crop_4_${slug}_run.log"
}

case "${1:-all}" in
  probe)   do_probe ;;
  judgeA)  do_judgeA ;;
  crop)    do_crop "$2" ;;
  all)
    do_probe || { echo "probe blocked - stopping"; exit 1; }
    do_judgeA || echo "judgeA blocked"
    for s in eq_stack pinkbox peachbox deriv_stack solution; do
      do_crop "$s" || echo "crop $s blocked"
    done
    ;;
  *) echo "usage: $0 [probe|judgeA|crop SLUG|all]"; exit 2 ;;
esac
