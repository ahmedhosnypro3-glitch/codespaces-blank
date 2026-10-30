#!/usr/bin/env bash
# Slide 049 Template A full-slide judge — leg 1 (worker-fresh-049d).
# Canonical tree: /workspaces/codespaces-blank/ai_llm_slides (plural).
set -u
PROJ=/workspaces/codespaces-blank/ai_llm_slides
QA=$PROJ/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide049
VID=$PROJ/videos/machine-learning/03_ridger_regression_gradient_descent
SCRIPT=$PROJ/.agents/skills/image-analysis/scripts/analyze_image.py
export TMPDIR=$PROJ/scratch/tmp
mkdir -p "$TMPDIR"
LOG=$QA/worker_report_progress.log
WID=worker-fresh-049d
say() { echo "[$(date -u +%H:%M:%S)] $*" >> "$LOG"; }
hb() { (cd "$PROJ" && VIDEO=machine-learning/03_ridger_regression_gradient_descent python3 scripts/15_progress.py heartbeat 49 "$WID" >/dev/null 2>&1); }
wait_slot() {
  # Vision-gate law: fire only when concurrent analyze_image.py VISION CLIENTS < 8.
  # In this environment `pgrep -f analyze_image.py` over-counts ~4x because every
  # judge dispatch's bash/timeout wrappers carry the payload text in their cmdline
  # (measured 05:50: literal count 33 vs 8 real python3 clients). Count real
  # clients only: argv[0] is a python3 interpreter, argv[1] is the script.
  for round in $(seq 1 90); do
    load=$(ps -eo args= | awk '$1 ~ /python3$/ && $2 ~ /analyze_image\.py$/ {n++} END {print n+0}')
    if [ "${load:-0}" -ge 8 ]; then say "leg $1: real vision clients=$load (>=8) - heartbeat + sleep 240"; hb; sleep 240; continue; fi
    say "leg $1: slot open (real vision clients=$load)"; return 0
  done
  say "leg $1: no slot after 90 rounds - ABORT"; exit 99
}

say "=== worker-fresh-049d START: cuts verified, chrome PASS, payloads byte-verified ==="

# --- Template A probe (opens the gateway window; protocol 03) ---
wait_slot "A-probe"; hb
say "A-probe firing (load=$(pgrep -c -f analyze_image.py 2>/dev/null || echo 0))"
cd "$PROJ" && scripts/16_vision_gate.sh timeout 150 python3 "$SCRIPT" analysis \
  "$VID/recreated_pptx/qa/slide049/render_6.png" \
  --view "Slide 049 recreation attempt 6 - probe" \
  --capture "150dpi PNG render of a 13.33x7.5in PPTX" \
  --timeout 120 --rounds 1 --tries 1 \
  --transcript "$QA/probe_6.txt" > "$QA/probe_6_dispatch.log" 2>&1
rc=$?
say "A-probe rc=$rc body=$(wc -c < "$QA/probe_6.txt" 2>/dev/null || echo 0)B"
if [ $rc -ne 0 ] || [ ! -s "$QA/probe_6.txt" ]; then
  say "probe produced no body - protocol: sleep 300 and re-probe ONCE"
  hb; sleep 300; wait_slot "A-probe2"
  cd "$PROJ" && scripts/16_vision_gate.sh timeout 150 python3 "$SCRIPT" analysis \
    "$VID/recreated_pptx/qa/slide049/render_6.png" \
    --view "Slide 049 recreation attempt 6 - probe retry" \
    --capture "150dpi PNG render of a 13.33x7.5in PPTX" \
    --timeout 120 --rounds 1 --tries 1 \
    --transcript "$QA/probe_6.txt" > "$QA/probe_6_dispatch.log" 2>&1
  say "A-probe retry rc=$?"
fi

# --- Template A real judge (full-slide comparison) ---
wait_slot "A"; hb
say "A judge firing (load=$(pgrep -c -f analyze_image.py 2>/dev/null || echo 0))"
rm -f "$QA/judge_attempt_6.txt"
cd "$PROJ" && timeout 1700 bash scripts/16_vision_gate.sh python3 "$SCRIPT" comparison \
  "$QA/render_6.png" "$VID/unique_slides/slide_049.jpg" \
  --view "Slide 049 recreation - fidelity check vs original lecture frame" \
  --capture "IMG1=150dpi PNG render of a 13.33x7.5in PPTX; IMG2=original lecture video frame" \
  --thinking high --max-tokens 65536 --timeout 600 --rounds 1 --tries 1 \
  --transcript "$QA/judge_attempt_6.txt" \
  -p "$(cat "$QA/judge_prompt_6.txt")" \
  > "$QA/judge_6_dispatch.log" 2>&1
rc=$?
say "A judge rc=$rc transcript=$(wc -c < "$QA/judge_attempt_6.txt" 2>/dev/null || echo 0)B"
if [ -s "$QA/judge_attempt_6.txt" ]; then
  say "A VERDICT: $(grep -o 'FINAL VERDICT: [A-Z]*' "$QA/judge_attempt_6.txt" | tail -1)"
fi
say "=== leg A done ==="
