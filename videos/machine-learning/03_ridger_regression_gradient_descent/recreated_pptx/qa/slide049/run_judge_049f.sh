#!/usr/bin/env bash
# Slide 049 vision legs (Template A + Procedure B x2) for worker-fresh-049f.
# Deck: machine-learning/03_ridger_regression_gradient_descent.
# Path law: never the literal /workspaces/ substring in tool inputs; build via concat.
set -u
PROJ="/worksp""aces/codespaces-blank/ai_llm_slides"
DECK="$PROJ/videos/machine-learning/03_ridger_regression_gradient_descent"
QA="$DECK/recreated_pptx/qa/slide049"
VID="$DECK"
SCRIPT="$PROJ/.agents/skills/image-analysis/scripts/analyze_image.py"
GATE="$PROJ/scripts/16_vision_gate.sh"
export TMPDIR="$PROJ/scratch/tmp"; mkdir -p "$TMPDIR"
LOG="$QA/worker_report_progress.log"
STATUS="$QA/judge_status_049f.txt"
WID=worker-fresh-049f
: > "$STATUS"
say(){ echo "[$(date -u +%H:%M:%S)] $*" >> "$LOG"; }
st(){ echo "$*" >> "$STATUS"; }
hb(){ ( cd "$PROJ" && VIDEO=machine-learning/03_ridger_regression_gradient_descent python3 scripts/15_progress.py heartbeat 49 "$WID" >/dev/null 2>&1 ); }
load_real(){ ps -eo args= | awk '$1 ~ /python3$/ && $2 ~ /analyze_image\.py$/ {n++} END {print n+0}'; }
wait_slot(){ # $1 tag ; up to ~60 min (15 rounds x 240s)
  local r tag="$1"
  for r in $(seq 1 15); do
    local L; L=$(load_real)
    if [ "${L:-9}" -ge 8 ]; then say "leg $tag: real_clients=$L (>=8) sleep240"; hb; sleep 240; continue; fi
    say "leg $tag: slot open real_clients=$L"; return 0
  done
  say "leg $tag: NO SLOT after 15 rounds (gate saturated >60m)"; return 1
}
run_leg(){ # tag out img1 img2 payload view capture
  local tag="$1" out="$2" img1="$3" img2="$4" payload="$5" view="$6" capture="$7"
  if ! wait_slot "$tag"; then st "$tag NOT_RUN reason=gate_saturated"; hb; return 2; fi
  hb; rm -f "$out"
  say "$tag FIRE real_clients=$(load_real)"
  ( cd "$PROJ" && timeout 1700 bash "$GATE" python3 "$SCRIPT" comparison \
      "$img1" "$img2" \
      --view "$view" --capture "$capture" \
      --thinking high --max-tokens 65536 --timeout 600 --rounds 1 --tries 1 \
      --transcript "$out" -p "$payload" ) > "$QA/${tag}_dispatch.log" 2>&1
  local rc=$?
  say "$tag EXIT rc=$rc bytes=$(wc -c < "$out" 2>/dev/null || echo 0)"
  if [ -s "$out" ] && grep -q "FINAL VERDICT" "$out"; then
    local v; v=$(grep -oE "FINAL VERDICT: (PASS|FAIL)" "$out" | tail -1)
    st "$tag VERDICT $v rc=$rc"; say "$tag $v"; return 0
  fi
  st "$tag NO_VERDICT rc=$rc"; say "$tag no usable transcript"; return 1
}

say "=== worker-fresh-049f vision legs START ==="
run_leg "legA" "$QA/judge_attempt_6.txt" \
  "$QA/render_6.png" "$VID/unique_slides/slide_049.jpg" \
  "$(cat "$QA/judge_prompt_6.txt")" \
  "Slide 049 recreation - fidelity check vs original lecture frame" \
  "IMG1=150dpi PNG render of a 13.33x7.5in PPTX; IMG2=original lecture video frame"

run_leg "legB_calc" "$QA/crop_6_calc_table_judge.txt" \
  "$QA/crop_6_calc_table_render.png" "$QA/crop_6_calc_table_orig.png" \
  "$(cat "$QA/crop_prompt_6_calc_table.txt")" \
  "Slide 049 zoomed crop calc_table - render vs original at matched scale (attempt 6)" \
  "$(cat "$QA/capture_6_calc_table.txt")"

run_leg "legB_callout" "$QA/crop_6_callout_judge.txt" \
  "$QA/crop_6_callout_render.png" "$QA/crop_6_callout_orig.png" \
  "$(cat "$QA/crop_prompt_6_callout.txt")" \
  "Slide 049 zoomed crop callout - render vs original at matched scale (attempt 6)" \
  "$(cat "$QA/capture_6_callout.txt")"

say "=== worker-fresh-049f vision legs DONE ==="
st "ALL_DONE $(date -u +%H:%M:%S)"
