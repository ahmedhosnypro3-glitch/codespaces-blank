#!/usr/bin/env bash
# Slide 030 retry dispatcher v4 (worker w030-finish-20261024b) — 2026-10-24 15:2x UTC.
# Re-fires the legs that returned no verdict in v3 (upstream 504 / internal 1230s
# HangError). Legs already carrying a real FINAL VERDICT are skipped.
#   - payload bytes unchanged (banked, byte-verified by make_payloads_6.py)
#   - --timeout 1200 (approved wall) inside timeout 1700, --thinking high
#     --max-tokens 65536
#   - gate law: real python3 analyze clients < 8 (049 metric); pgrep -f logged.
#     Two probes max per hour, then sleep 240, then continue waiting.
#   - sequential, one leg at a time (the gateway cannot take parallel heavy legs).
set -u
ROOT="/worksp""aces/codespaces-blank/ai_llm_slides"
DECK="$ROOT/videos/machine-learning/03_ridger_regression_gradient_descent"
QA="$DECK/recreated_pptx/qa/slide030"
export TMPDIR="$ROOT/scratch/tmp"
LOG="$QA/worker_report_progress.log"
WID=w030-finish-20261024b

say() { echo "[$(date -u +%H:%M:%S)] $*" >> "$LOG"; }
hb() { (cd "$ROOT" && VIDEO=machine-learning/03_ridger_regression_gradient_descent \
        python3 scripts/15_progress.py heartbeat 30 "$WID" >/dev/null 2>&1); }
real_clients() { ps -eo args= | awk '$1 ~ /python3$/ && $2 ~ /analyze_image\.py$/ {n++} END {print n+0}'; }

wait_slot() {
  local probes=0
  for round in $(seq 1 200); do
    load=$(real_clients)
    pg=$(pgrep -c -f analyze_image.py 2>/dev/null || echo 0)
    if [ "${load:-0}" -lt 8 ]; then
      say "$1: slot open (real clients=$load, pgrep -f=$pg)"
      return 0
    fi
    probes=$((probes+1))
    say "$1: real clients=$load (probe $probes) - sleep 240"; hb; sleep 240
    if [ "$probes" -ge 2 ]; then say "$1: 2 probes this hour - continuing to wait"; fi
  done
  say "$1: no slot after 200 rounds - PARK"; exit 99
}

run_leg() {  # run_leg <label> <img1> <img2> <view> <capture> <transcript> <payloadfile>
  local label="$1" img1="$2" img2="$3" view="$4" cap="$5" tr="$6" pf="$7"
  local payload; payload=$(cat "$pf")
  wait_slot "$label"; hb
  say "$label firing (tmo=1200)"
  ( cd "$ROOT" && bash scripts/16_vision_gate.sh timeout 1700 python3 \
      .agents/skills/image-analysis/scripts/analyze_image.py comparison \
      "$img1" "$img2" \
      --view "$view" --capture "$cap" \
      --thinking high --max-tokens 65536 \
      --timeout 1200 --rounds 1 --tries 1 \
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

fire_crop() {  # fire_crop <name>
  local name="$1" desc
  desc=$(desc_of "$name")
  run_leg "legB_${name}" \
    "$QA/crop_6_${name}_render.png" "$QA/crop_6_${name}_orig.png" \
    "Slide 030 zoomed crop ${name} — render vs original at matched scale (attempt 6)" \
    "IMG1=zoomed crop of a 150dpi PPTX render; IMG2=the SAME slide-space region cropped from the original lecture frame and upscaled to match IMG1's effective scale; region: ${desc}" \
    "$QA/crop_6_${name}_judge.txt" "$QA/crop_prompt_6_${name}.txt"
}

say "=== dispatch v4 START (retry legs missing verdicts) ==="
hb

# ---- Leg A: full-slide (still missing) ----
LEGA_TR="$QA/judge_attempt_6.txt"
if ! grep -q "FINAL VERDICT:" "$LEGA_TR" 2>/dev/null; then
  run_leg "legA_full" \
    "$QA/render_6.png" "$DECK/unique_slides/slide_030.jpg" \
    "Slide 030 recreation — fidelity check vs original lecture frame" \
    "IMG1=150dpi PNG render of a 13.33x7.5in PPTX; IMG2=original lecture video frame" \
    "$LEGA_TR" "$QA/judge_prompt_6.txt"
else
  say "legA_full: verdict already present - skip"
fi
hb

# ---- crops missing verdicts (formula already PASS) ----
for name in plot iter_left iter_right param callout arrow; do
  if grep -q "FINAL VERDICT:" "$QA/crop_6_${name}_judge.txt" 2>/dev/null; then
    say "legB_${name}: verdict already present - skip"
    continue
  fi
  fire_crop "$name"
  hb
done

say "=== dispatch v4 COMPLETE ==="
hb
echo "V4-DONE"
for f in "$QA"/judge_attempt_6.txt "$QA"/crop_6_*_judge.txt; do
  [ -f "$f" ] || continue
  printf "%-40s %s\n" "$(basename "$f")" "$(grep -o 'FINAL VERDICT: [A-Z]*' "$f" | tail -1 || echo 'NO VERDICT')"
done
