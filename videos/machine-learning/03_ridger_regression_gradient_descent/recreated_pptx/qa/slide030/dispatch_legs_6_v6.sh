#!/usr/bin/env bash
# Slide 030 dispatcher v6 (worker w030-finish-20261024c).
# v5 burned legA_full on a fast 504 and never revisits it, so v6 re-checks
# EVERY leg each outer round and fires only the ones with no verdict yet.
# A leg that returns a fast 504 is skipped (not blocking) so the healthy
# legs keep flowing; the outer loop retries whatever is still missing.
#
# Payload bytes unchanged; approved wall = --timeout 1200 inside timeout 1700.
set -u
ROOT="/worksp""aces/codespaces-blank/ai_llm_slides"
DECK="$ROOT/videos/machine-learning/03_ridger_regression_gradient_descent"
QA="$DECK/recreated_pptx/qa/slide030"
SCRIPT="$ROOT/.agents/skills/image-analysis/scripts/analyze_image.py"
export TMPDIR="$ROOT/scratch/tmp"
LOG="$QA/worker_report_progress.log"
WID=w030-finish-20261024c
OUTER_ROUNDS=10

say() { echo "[$(date -u +%H:%M:%S)] v6 $*" >> "$LOG"; }
hb() { (cd "$ROOT" && VIDEO=machine-learning/03_ridger_regression_gradient_descent \
        python3 scripts/15_progress.py heartbeat 30 "$WID" >/dev/null 2>&1); }
real_clients() { ps -eo args= | awk '$1 ~ /python3$/ && $2 ~ /analyze_image\.py$/ {n++} END {print n+0}'; }

desc_of() { python3 -c "
import json
print(json.load(open('$QA/crop_6_scale_audit.json'))['$1']['desc'])"; }

fire_leg() {  # fire_leg <label> <img1> <img2> <view> <capture> <transcript> <payloadfile>
  local label="$1" img1="$2" img2="$3" view="$4" cap="$5" tr="$6" pf="$7"
  local payload; payload=$(cat "$pf")
  say "$label firing"
  hb
  ( cd "$ROOT" && bash scripts/16_vision_gate.sh timeout 1700 python3 "$SCRIPT" comparison \
      "$img1" "$img2" --view "$view" --capture "$cap" \
      --thinking high --max-tokens 65536 \
      --timeout 1200 --rounds 1 --tries 1 \
      --transcript "$tr" -p "$payload" ) > "$QA/${label}_dispatch.log" 2>&1
  local rc=$?
  if grep -q "FINAL VERDICT:" "$tr" 2>/dev/null; then
    say "$label VERDICT: $(grep -o 'FINAL VERDICT: [A-Z]*' "$tr" | tail -1) (rc=$rc)"
    return 0
  fi
  if grep -q "upstream_timeout\|HTTP 504" "$QA/${label}_dispatch.log"; then
    say "$label rc=$rc upstream_timeout - skip to next leg"
    return 1
  fi
  say "$label rc=$rc non-504 failure - no verdict"
  return 1
}

legA_done() { grep -q "FINAL VERDICT:" "$QA/judge_attempt_6.txt" 2>/dev/null; }
crop_done() { grep -q "FINAL VERDICT:" "$QA/crop_6_${1}_judge.txt" 2>/dev/null; }

for outer in $(seq 1 "$OUTER_ROUNDS"); do
  missing=0
  for name in plot iter_left iter_right param callout arrow; do
    crop_done "$name" || missing=1
  done
  legA_done || missing=1
  [ "$missing" -eq 0 ] && { say "all legs have verdicts - done"; break; }

  load=$(real_clients)
  if [ "${load:-0}" -ge 8 ]; then
    say "outer $outer: congested ($load) - heartbeat + sleep 240"
    hb; sleep 240; continue
  fi

  if ! legA_done; then
    fire_leg "legA_full" \
      "$QA/render_6.png" "$DECK/unique_slides/slide_030.jpg" \
      "Slide 030 recreation — fidelity check vs original lecture frame" \
      "IMG1=150dpi PNG render of a 13.33x7.5in PPTX; IMG2=original lecture video frame" \
      "$QA/judge_attempt_6.txt" "$QA/judge_prompt_6.txt"
  fi

  for name in plot iter_left iter_right param callout arrow; do
    crop_done "$name" && { say "legB_${name}: verdict present - skip"; continue; }
    desc=$(desc_of "$name")
    fire_leg "legB_${name}" \
      "$QA/crop_6_${name}_render.png" "$QA/crop_6_${name}_orig.png" \
      "Slide 030 zoomed crop ${name} — render vs original at matched scale (attempt 6)" \
      "IMG1=zoomed crop of a 150dpi PPTX render; IMG2=the SAME slide-space region cropped from the original lecture frame and upscaled to match IMG1's effective scale; region: ${desc}" \
      "$QA/crop_6_${name}_judge.txt" "$QA/crop_prompt_6_${name}.txt"
    hb
  done

  say "outer $outer complete; re-checking missing legs"
  sleep 120
done

say "=== dispatch v6 COMPLETE ==="
hb
for f in "$QA"/judge_attempt_6.txt "$QA"/crop_6_*_judge.txt; do
  [ -f "$f" ] || continue
  printf "%-40s %s\n" "$(basename "$f")" "$(grep -o 'FINAL VERDICT: [A-Z]*' "$f" | tail -1 || echo 'NO VERDICT')"
done
