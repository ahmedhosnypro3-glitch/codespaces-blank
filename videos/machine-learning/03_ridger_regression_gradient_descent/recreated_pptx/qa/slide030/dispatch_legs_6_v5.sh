#!/usr/bin/env bash
# Slide 030 retry dispatcher v5 (worker w030-finish-20261024b).
# The image/vision upstream (Nvidia via IronRouter) is currently returning
# HTTP 504 upstream_timeout on EVERY call, heavy or light (verified 16:2x with a
# 90s analysis probe). The 03:14-03:41 UTC window earlier today DID work
# (crop_6_formula landed PASS), so the outage is transient.
#
# Strategy: poll the lane with a LIGHT probe (analysis, --timeout 120) every
# PROBE_EVERY seconds. When a probe returns a real body, fire the missing legs
# back-to-back at --timeout 1200 (approved wall). Cap = MAX_WAIT_MIN minutes,
# then park honestly with evidence.
#
# Payload bytes unchanged; gate law respected (real python3 clients < 8).
set -u
ROOT="/worksp""aces/codespaces-blank/ai_llm_slides"
DECK="$ROOT/videos/machine-learning/03_ridger_regression_gradient_descent"
QA="$DECK/recreated_pptx/qa/slide030"
SCRIPT="$ROOT/.agents/skills/image-analysis/scripts/analyze_image.py"
export TMPDIR="$ROOT/scratch/tmp"
LOG="$QA/worker_report_progress.log"
WID=w030-finish-20261024b
PROBE_EVERY=300
MAX_WAIT_MIN=100

say() { echo "[$(date -u +%H:%M:%S)] $*" >> "$LOG"; }
hb() { (cd "$ROOT" && VIDEO=machine-learning/03_ridger_regression_gradient_descent \
        python3 scripts/15_progress.py heartbeat 30 "$WID" >/dev/null 2>&1); }
real_clients() { ps -eo args= | awk '$1 ~ /python3$/ && $2 ~ /analyze_image\.py$/ {n++} END {print n+0}'; }

start_ts=$(date +%s)
probe_no=0

while :; do
  now=$(date +%s); waited=$(( (now - start_ts) / 60 ))
  if [ "$waited" -ge "$MAX_WAIT_MIN" ]; then
    say "upstream: still 504 after ${waited}min - PARK (resume later)"; hb; exit 98
  fi
  load=$(real_clients)
  if [ "${load:-0}" -ge 8 ]; then
    say "probe: real clients=$load (>=8) - heartbeat + sleep 240"
    hb; sleep 240; continue
  fi
  probe_no=$((probe_no+1))
  say "probe #${probe_no}: gateway health (waited ${waited}min, real clients=$load, pgrep -f=$(pgrep -c -f analyze_image.py 2>/dev/null || echo 0))"
  hb
  ( cd "$ROOT" && bash scripts/16_vision_gate.sh timeout 300 python3 "$SCRIPT" analysis \
      "$QA/render_6.png" \
      --view "slide030 gateway health probe" \
      --capture "150dpi PNG render of a 13.33x7.5in PPTX" \
      --timeout 200 --rounds 1 --tries 1 \
      --transcript "$QA/probe_health_${probe_no}.txt" ) > "$QA/probe_health_dispatch.log" 2>&1
  if [ -s "$QA/probe_health_${probe_no}.txt" ] && grep -q "[A-Za-z]" "$QA/probe_health_${probe_no}.txt"; then
    if grep -qi "FINAL VERDICT\|verdict" "$QA/probe_health_${probe_no}.txt" 2>/dev/null; then :; fi
    if grep -q "504\|upstream_timeout" "$QA/probe_health_dispatch.log"; then
      say "probe #${probe_no}: still upstream_timeout - sleep ${PROBE_EVERY}"
      sleep "$PROBE_EVERY"; continue
    fi
    say "probe #${probe_no}: gateway ANSWERED - firing missing legs"
    break
  else
    say "probe #${probe_no}: no usable body (rc from dispatch log) - sleep ${PROBE_EVERY}"
    if grep -q "504\|upstream_timeout" "$QA/probe_health_dispatch.log"; then
      sleep "$PROBE_EVERY"; continue
    fi
    # probe body empty but not a 504: still worth attempting the real legs
    say "probe #${probe_no}: empty but not 504 - attempting legs"
    break
  fi
done

# ---------------- fire missing legs ----------------
fire_leg() {  # fire_leg <label> <img1> <img2> <view> <capture> <transcript> <payloadfile>
  local label="$1" img1="$2" img2="$3" view="$4" cap="$5" tr="$6" pf="$7"
  local payload; payload=$(cat "$pf")
  local round=0
  while [ "$round" -lt 6 ]; do
    load=$(real_clients)
    if [ "${load:-0}" -ge 8 ]; then say "$label: congested ($load) - sleep 240"; hb; sleep 240; continue; fi
    round=$((round+1))
    say "$label firing (round $round, tmo=1200)"; hb
    ( cd "$ROOT" && bash scripts/16_vision_gate.sh timeout 1700 python3 "$SCRIPT" comparison \
        "$img1" "$img2" --view "$view" --capture "$cap" \
        --thinking high --max-tokens 65536 \
        --timeout 1200 --rounds 1 --tries 1 \
        --transcript "$tr" -p "$payload" ) > "$QA/${label}_dispatch.log" 2>&1
    local rc=$?
    if grep -q "FINAL VERDICT:" "$tr" 2>/dev/null; then
      say "$label VERDICT: $(grep -o 'FINAL VERDICT: [A-Z]*' "$tr" | tail -1)"; return 0
    fi
    if grep -q "upstream_timeout\|HTTP 504" "$QA/${label}_dispatch.log"; then
      say "$label rc=$rc upstream_timeout - retry after probe window"; return 1
    fi
    say "$label rc=$rc non-504 failure - retry once after 240"; sleep 240
  done
  say "$label: no verdict after 6 rounds"; return 1
}

desc_of() { python3 -c "
import json
print(json.load(open('$QA/crop_6_scale_audit.json'))['$1']['desc'])"; }

# Leg A first (highest value: full-slide)
if ! grep -q "FINAL VERDICT:" "$QA/judge_attempt_6.txt" 2>/dev/null; then
  fire_leg "legA_full" \
    "$QA/render_6.png" "$DECK/unique_slides/slide_030.jpg" \
    "Slide 030 recreation — fidelity check vs original lecture frame" \
    "IMG1=150dpi PNG render of a 13.33x7.5in PPTX; IMG2=original lecture video frame" \
    "$QA/judge_attempt_6.txt" "$QA/judge_prompt_6.txt"
fi
hb

for name in plot iter_left iter_right param callout arrow; do
  grep -q "FINAL VERDICT:" "$QA/crop_6_${name}_judge.txt" 2>/dev/null && { say "legB_${name}: verdict present - skip"; continue; }
  desc=$(desc_of "$name")
  fire_leg "legB_${name}" \
    "$QA/crop_6_${name}_render.png" "$QA/crop_6_${name}_orig.png" \
    "Slide 030 zoomed crop ${name} — render vs original at matched scale (attempt 6)" \
    "IMG1=zoomed crop of a 150dpi PPTX render; IMG2=the SAME slide-space region cropped from the original lecture frame and upscaled to match IMG1's effective scale; region: ${desc}" \
    "$QA/crop_6_${name}_judge.txt" "$QA/crop_prompt_6_${name}.txt"
  hb
done

say "=== dispatch v5 COMPLETE ==="
hb
echo "V5-DONE"
for f in "$QA"/judge_attempt_6.txt "$QA"/crop_6_*_judge.txt; do
  [ -f "$f" ] || continue
  printf "%-40s %s\n" "$(basename "$f")" "$(grep -o 'FINAL VERDICT: [A-Z]*' "$f" | tail -1 || echo 'NO VERDICT')"
done
