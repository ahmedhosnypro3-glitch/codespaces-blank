#!/usr/bin/env bash
# Slide 030 judge dispatch v2 (worker w030-finish-20261024).
# Leg A already fired at 11:37 under the ORPHANED v1 wrapper (killed by the
# harness 600s background ceiling; its python client 574060 was reparented to
# init and still owns the leg-A transcript path). v2 therefore:
#   1. waits for that orphan to exit (or the 1700s wrapper wall) — no duplicate
#      leg-A firing;
#   2. if it left no verdict, re-fires leg A ONCE at the ratified provisional
#      W4 wall (--timeout 1200; payload byte-for-byte unchanged);
#   3. then fires the 7 Procedure B crop legs, also at 1200.
# Gate law: fire only when concurrent REAL python3 analyze_image.py clients < 8.
set -u
ROOT="/worksp""aces/codespaces-blank/ai_llm_slides"
DECK="$ROOT/videos/machine-learning/03_ridger_regression_gradient_descent"
QA="$DECK/recreated_pptx/qa/slide030"
export TMPDIR="$ROOT/scratch/tmp"
mkdir -p "$TMPDIR" "$QA"
LOG="$QA/worker_report_progress.log"
WID=w030-finish-20261024

say() { echo "[$(date -u +%H:%M:%S)] $*" >> "$LOG"; }
hb() { (cd "$ROOT" && VIDEO=machine-learning/03_ridger_regression_gradient_descent \
        python3 scripts/15_progress.py heartbeat 30 "$WID" >/dev/null 2>&1); }
real_clients() { ps -eo args= | awk '$1 ~ /python3$/ && $2 ~ /analyze_image\.py$/ {n++} END {print n+0}'; }

wait_slot() {
  for round in $(seq 1 120); do
    load=$(real_clients)
    if [ "${load:-0}" -lt 8 ]; then
      say "$1: slot open (real clients=$load, pgrep -f=$(pgrep -c -f analyze_image.py 2>/dev/null || echo 0))"
      return 0
    fi
    say "$1: real clients=$load (>=8) - heartbeat + sleep 240"; hb; sleep 240
  done
  say "$1: no slot after 120 rounds - PARK"; exit 99
}

run_leg() {  # run_leg <label> <img1> <img2> <view> <capture> <transcript> <payloadfile> <timeout>
  local label="$1" img1="$2" img2="$3" view="$4" cap="$5" tr="$6" pf="$7" to="$8"
  local payload; payload=$(cat "$pf")
  wait_slot "$label"; hb
  say "$label firing (tmo=$to)"
  ( cd "$ROOT" && bash scripts/16_vision_gate.sh timeout 1700 python3 \
      .agents/skills/image-analysis/scripts/analyze_image.py comparison \
      "$img1" "$img2" \
      --view "$view" --capture "$cap" \
      --thinking high --max-tokens 65536 \
      --timeout "$to" --rounds 1 --tries 1 \
      --transcript "$tr" \
      -p "$payload" ) > "$QA/${label}_dispatch.log" 2>&1
  local rc=$?
  say "$label rc=$rc"
  if grep -q "FINAL VERDICT:" "$tr" 2>/dev/null; then
    say "$label VERDICT: $(grep -o 'FINAL VERDICT: [A-Z]*' "$tr" | tail -1)"
  else
    say "$label NO VERDICT LINE (rc=$rc)"
  fi
  return $rc
}

desc_of() { python3 -c "
import json
print(json.load(open('$QA/crop_6_scale_audit.json'))['$1']['desc'])"; }

say "=== dispatch v2 START ==="
hb

# ---------- 1. Leg A: wait for the orphaned v1 client (pid arg or autodetect) ----
LEGA_TR="$QA/judge_attempt_6.txt"
if grep -q "FINAL VERDICT:" "$LEGA_TR" 2>/dev/null; then
  say "legA_full: orphan ALREADY landed a verdict - $(grep -o 'FINAL VERDICT: [A-Z]*' "$LEGA_TR" | tail -1)"
else
  # wait for any live analyze_image client writing to this transcript
  for i in $(seq 1 120); do
    alive=$(ps -eo args= | grep -c "transcript .*slide030/judge_attempt_6.txt" || true)
    if [ "${alive:-0}" -eq 0 ]; then
      say "legA_full: orphan gone after $i polls"
      break
    fi
    if [ $((i % 5)) -eq 0 ]; then say "legA_full: orphan still alive (poll $i, real clients=$(real_clients))"; hb; fi
    sleep 60
  done
  if grep -q "FINAL VERDICT:" "$LEGA_TR" 2>/dev/null; then
    say "legA_full: ORPHAN LANDED - $(grep -o 'FINAL VERDICT: [A-Z]*' "$LEGA_TR" | tail -1)"
  else
    say "legA_full: orphan left NO verdict - re-firing ONCE at W4 wall 1200"
    run_leg "legA_full" \
      "$QA/render_6.png" "$DECK/unique_slides/slide_030.jpg" \
      "Slide 030 recreation — fidelity check vs original lecture frame" \
      "IMG1=150dpi PNG render of a 13.33x7.5in PPTX; IMG2=original lecture video frame" \
      "$LEGA_TR" "$QA/judge_prompt_6.txt" 1200
  fi
fi
hb

# ---------- 2. Legs B: crop pairs ----------
for name in param formula plot iter_left iter_right callout arrow; do
  if grep -q "FINAL VERDICT:" "$QA/crop_6_${name}_judge.txt" 2>/dev/null; then
    say "legB_${name}: already has verdict - skip"
    continue
  fi
  desc=$(desc_of "$name")
  run_leg "legB_${name}" \
    "$QA/crop_6_${name}_render.png" "$QA/crop_6_${name}_orig.png" \
    "Slide 030 zoomed crop ${name} — render vs original at matched scale (attempt 6)" \
    "IMG1=zoomed crop of a 150dpi PPTX render; IMG2=the SAME slide-space region cropped from the original lecture frame and upscaled to match IMG1's effective scale; region: ${desc}" \
    "$QA/crop_6_${name}_judge.txt" "$QA/crop_prompt_6_${name}.txt" 1200
  hb
done

say "=== dispatch v2 COMPLETE ==="
hb
echo "V2-DONE"
for f in "$QA"/judge_attempt_6.txt "$QA"/crop_6_*_judge.txt; do
  [ -f "$f" ] || continue
  printf "%-46s %s\n" "$(basename "$f")" "$(grep -o 'FINAL VERDICT: [A-Z]*' "$f" | tail -1 || echo 'NO VERDICT')"
done
