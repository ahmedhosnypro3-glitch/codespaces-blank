#!/usr/bin/env bash
# Slide 030 judge dispatch (worker w030-finish-20261024, attempt 6).
# Legs: Template A full-slide comparison + 7 Procedure B crop pairs.
#   - payloads read from the BYTE-VERIFIED banked payload files (judge_prompt_6.txt,
#     crop_prompt_6_<name>.txt) — regenerated from shared_patterns/judge_protocol_03.md
#     with ONLY slide_NNN -> slide030 and K -> 6 substitutions (make_payloads_6.py).
#   - gate law: fire only when concurrent REAL python3 analyze_image.py clients < 8
#     (049's measurement: `pgrep -f` over-counts ~4x because every judge dispatch's
#     bash/timeout wrappers carry the payload text in their cmdline — logged here).
#   - walls: timeout 1700 wrapper, --timeout 600 per call (protocol 03 default).
#     Provisional W4 extension to --timeout 1200 only if a leg aborts at the 630s
#     client wall; max one hard-wall retry per leg; never retry-loop.
set -u
ROOT="/worksp""aces/codespaces-blank/ai_llm_slides"
DECK="$ROOT/videos/machine-learning/03_ridger_regression_gradient_descent"
QA="$DECK/recreated_pptx/qa/slide030"
SCRIPT="$ROOT/.agents/skills/image-analysis/scripts/analyze_image.py"
export TMPDIR="$ROOT/scratch/tmp"
mkdir -p "$TMPDIR" "$QA"
LOG="$QA/worker_report_progress.log"
WID=w030-finish-20261024

say() { echo "[$(date -u +%H:%M:%S)] $*" >> "$LOG"; }
hb() { (cd "$ROOT" && VIDEO=machine-learning/03_ridger_regression_gradient_descent \
        python3 scripts/15_progress.py heartbeat 30 "$WID" >/dev/null 2>&1); }

real_clients() {
  ps -eo args= | awk '$1 ~ /python3$/ && $2 ~ /analyze_image\.py$/ {n++} END {print n+0}'
}
wait_slot() {
  for round in $(seq 1 90); do
    load=$(real_clients)
    pg=$(pgrep -c -f analyze_image.py 2>/dev/null || echo 0)
    if [ "${load:-0}" -ge 8 ]; then
      say "$1: real clients=$load (>=8) pgrep=$pg - heartbeat + sleep 240"
      hb; sleep 240; continue
    fi
    say "$1: slot open (real clients=$load, pgrep -f count=$pg)"
    return 0
  done
  say "$1: no slot after 90 rounds - PARK"; exit 99
}

fire() {  # fire <label> <mode> <img1> <img2> <view> <capture> <transcript> <payloadfile> [timeout]
  local label="$1" mode="$2" img1="$3" img2="$4" view="$5" cap="$6" tr="$7" pf="$8" to="${9:-600}"
  local payload
  payload=$(cat "$pf")
  wait_slot "$label"; hb
  say "$label firing (mode=$mode tmo=$to)"
  ( cd "$ROOT" && bash scripts/16_vision_gate.sh timeout 1700 python3 "$SCRIPT" "$mode" \
      "$img1" "$img2" \
      --view "$view" \
      --capture "$cap" \
      --thinking high --max-tokens 65536 \
      --timeout "$to" --rounds 1 --tries 1 \
      --transcript "$tr" \
      -p "$payload" ) > "$QA/${label}_dispatch.log" 2>&1
  local rc=$?
  say "$label done rc=$rc"
  if grep -q "FINAL VERDICT:" "$tr" 2>/dev/null; then
    say "$label VERDICT: $(grep -o 'FINAL VERDICT: [A-Z]*' "$tr" | tail -1)"
  else
    say "$label NO VERDICT LINE (rc=$rc)"
  fi
  return $rc
}

say "=== w030-finish ATTEMPT 6 dispatch START (build current, chrome PASS, PIL clean, crops cut at matched scale) ==="
hb

# ---- 0. Template A probe (opens the gateway window) ----
wait_slot "probe"; hb
( cd "$ROOT" && bash scripts/16_vision_gate.sh timeout 150 python3 "$SCRIPT" analysis \
    "$QA/render_6.png" \
    --view "Slide 030 recreation attempt 6 - probe" \
    --capture "150dpi PNG render of a 13.33x7.5in PPTX" \
    --timeout 120 --rounds 1 --tries 1 \
    --transcript "$QA/probe_6.txt" ) > "$QA/probe_6_dispatch.log" 2>&1
say "probe rc=$? verdict=$(grep -c 'FINAL VERDICT' "$QA/probe_6.txt" 2>/dev/null || echo 0)"
hb

# ---- 1. Leg A: full-slide comparison (Template A) ----
fire "legA_full" comparison \
  "$QA/render_6.png" "$DECK/unique_slides/slide_030.jpg" \
  "Slide 030 recreation — fidelity check vs original lecture frame" \
  "IMG1=150dpi PNG render of a 13.33x7.5in PPTX; IMG2=original lecture video frame" \
  "$QA/judge_attempt_6.txt" "$QA/judge_prompt_6.txt"
hb

# ---- 2. Legs B: crop pairs (Procedure B), in region order ----
for name in param formula plot iter_left iter_right callout arrow; do
  desc=$(python3 -c "
import json,sys
a=json.load(open('$QA/crop_6_scale_audit.json'))
print(a['$name']['desc'])")
  fire "legB_${name}" comparison \
    "$QA/crop_6_${name}_render.png" "$QA/crop_6_${name}_orig.png" \
    "Slide 030 zoomed crop ${name} — render vs original at matched scale (attempt 6)" \
    "IMG1=zoomed crop of a 150dpi PPTX render; IMG2=the SAME slide-space region cropped from the original lecture frame and upscaled to match IMG1's effective scale; region: ${desc}" \
    "$QA/crop_6_${name}_judge.txt" "$QA/crop_prompt_6_${name}.txt"
  hb
done

say "=== dispatch sequence COMPLETE ==="
hb
echo "DONE"
grep -c "VERDICT" "$LOG" 2>/dev/null | sed 's/^/verdict lines logged: /'
for f in "$QA"/judge_attempt_6.txt "$QA"/crop_6_*_judge.txt; do
  [ -f "$f" ] || continue
  printf "%-52s %s\n" "$(basename "$f")" "$(grep -o 'FINAL VERDICT: [A-Z]*' "$f" | tail -1 || echo 'NO VERDICT')"
done
