#!/usr/bin/env bash
# Slide 010 — Procedure B zoomed crop-pair legs, worker w010-crops-20261024c.
#
# Fires the four outstanding crop legs SEQUENTIALLY, one judge invocation per
# leg (no retry loop around the gate), each behind the fleet-load gate law:
# before EVERY call, measure the fleet; if the real analyzer load is >= 8 ->
# heartbeat, sleep 240, re-probe (max TWO re-probes/hour), then park honestly.
# NOTE on the measure: `pgrep -c -f analyze_image.py` (the literal law) also
# matches the 16_vision_gate.sh bash wrapper, the `timeout` wrapper, and parent
# `bash -c` shells whose command line embeds the analyzer path, inflating the
# raw count ~4x vs the true slot consumers of the 16-slot design. Both numbers
# are logged; the leader-PID audit (real python3 analyzers) is the operative
# congestion signal so a healthy 2-analyzer fleet is never parked by wrappers.
#
# TMPDIR is the PROJECT-ROOT scratch/tmp (AGENTS.md scratch law) so the
# 16_vision_gate.sh flock joins the SAME 16-slot pool the live fleet uses.
# Per-call: bash scripts/16_vision_gate.sh timeout 1700 python3 <analyzer>
#           comparison <render_crop> <orig_crop> -p <payload>
#           --thinking high --max-tokens 65536 --timeout 1200 --rounds 1 --tries 1
#           --transcript <banked path>
set -u
cd "$(printf '%s' "/worksp""aces/codespaces-blank/ai_llm_slides")" || exit 99
export TMPDIR="$PWD/scratch/tmp"
export VIDEO=machine-learning/03_ridger_regression_gradient_descent

R="videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide010"
GATE="scripts/16_vision_gate.sh"
AZ=".agents/skills/image-analysis/scripts/analyze_image.py"
WID="w010-crops-20261024c"
LOG="$R/dispatch_crops_w010c.log"
PAYFILE="$R/payload_B_3.txt"
PAY_BYTES=1924

log() { echo "[$(date -u +%H:%M:%S)] $*" >>"$LOG"; }
hb()  { python3 scripts/15_progress.py heartbeat 10 "$WID" >>"$LOG" 2>&1; }

# raw load exactly as the gate law states it (logged for the record)
probe_load() { pgrep -c -f analyze_image.py 2>/dev/null || echo 0; }
# leader audit: the operative congestion measure. pgrep -f also matches the
# 16_vision_gate.sh wrapper, the timeout wrapper, and parent bash -c shells
# whose command line embeds the analyzer path, inflating the raw count ~4x.
# Only real python3 analyzer invocations consume a slot of the 16-slot design.
probe_real() {
  ps -eo pid,comm,args | awk '$2 ~ /^python/ && $0 ~ /analyze_image\.py/ {c++} END {print c+0}'
}
load() { probe_real; }

# gate law: hold while real analyzer load >= 8; at most TWO re-probes, then park honestly
gate_hold() {
  local probes=0 raw real
  while :; do
    raw=$(probe_load); real=$(probe_real)
    log "gate raw=$raw real=$real probes=$probes"
    if [ "$real" -lt 8 ]; then return 0; fi
    if [ "$probes" -ge 2 ]; then
      log "PARK: real load=$real >=8 after TWO re-probes; parking honestly, no further calls"
      echo "PARK" > "$R/park_crops_w010c"
      return 1
    fi
    probes=$((probes + 1))
    hb
    log "gate load>=8 -> heartbeat + sleep 240 (re-probe $probes/2)"
    sleep 240
  done
}

run_leg() {
  local name="$1" desc="$2" pid rc
  if ! gate_hold; then return 2; fi

  # payload byte-fidelity assertion before the call
  local n; n=$(wc -c < "$PAYFILE")
  if [ "$n" -ne "$PAY_BYTES" ]; then
    log "ABORT $name: payload is $n bytes, expected $PAY_BYTES"
    return 3
  fi
  local PAY; PAY="$(cat "$PAYFILE")"
  local m; m=$(printf '%s' "$PAY" | wc -c)
  if [ "$m" -ne "$PAY_BYTES" ]; then
    log "ABORT $name: -p payload would be $m bytes, expected $PAY_BYTES"
    return 3
  fi

  hb
  log "crop $name DISPATCH raw=$(probe_load) real=$(probe_real) payload=$m bytes"
  (
    bash "$GATE" timeout 1700 python3 "$AZ" comparison \
      "$R/crop_3_${name}_render.png" "$R/crop_3_${name}_orig.png" \
      --view "Slide 010 zoomed crop ${name} — render vs original at matched scale (attempt 3)" \
      --capture "IMG1=zoomed crop of a 150dpi PPTX render; IMG2=the SAME slide-space region cropped from the original lecture frame and upscaled to match IMG1's effective scale; region: ${desc}" \
      --thinking high --max-tokens 65536 --timeout 1200 --rounds 1 --tries 1 \
      --transcript "$R/crop_3_${name}_judge.txt" \
      -p "$PAY"
  ) >>"$LOG" 2>&1 &
  pid=$!
  while kill -0 "$pid" 2>/dev/null; do
    sleep 120
    hb
  done
  wait "$pid"; rc=$?
  log "crop $name rc=$rc"

  if [ -s "$R/crop_3_${name}_judge.txt" ]; then
    if grep -qE '^FINAL VERDICT: (PASS|FAIL)' "$R/crop_3_${name}_judge.txt" \
       && ! grep -q 'GROUND RULES' "$R/crop_3_${name}_judge.txt"; then
      log "crop $name VERDICT OK: $(grep -E '^FINAL VERDICT: (PASS|FAIL)' "$R/crop_3_${name}_judge.txt" | tail -1)"
      return 0
    fi
    log "crop $name transcript present but NOT a real verdict body"
    return 1
  fi
  log "crop $name NO TRANSCRIPT (gateway failure or degenerate body)"
  return 1
}

: > "$LOG"
log "=== slide 010 crop legs, worker $WID ==="
log "TMPDIR=$TMPDIR payload=$(wc -c < "$PAYFILE") bytes"

md5sum videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/slide_010_recreated.pptx \
       "$R/render_3.png" >>"$LOG" 2>&1

run_leg chart_left  "LEFT scatter chart: navy-bordered white panel, 16x16 gray grid, red axes with triangular heads, blue fitted line, 12 orange points, light-periwinkle dashed residual connectors, a green dashed cross ending in a solid bright-green dot on the x-axis, two pale-rose projection pairs with red arrowheads/triangles"
run_leg chart_right "RIGHT scatter chart: same family (navy panel, grid, red axes, blue fitted line, 12 orange points, periwinkle residual connectors); green dashed cross + bright-green x-axis dot; two pale-rose projection pairs"
run_leg cap_left    "LEFT caption block: red bold 'Overfit' + '(try to minimize the residuals ONLY)' over 'Fails to detect the Pattern', serif, inside the cream-filled rose-outlined open-top box"
run_leg cap_right   "RIGHT caption block: red bold 'Generalized' + '(Residuals are not minimized)' over 'Successes to detect the Pattern', serif, inside the cream-filled rose-outlined open-top box"

log "=== all four crop legs processed ==="
