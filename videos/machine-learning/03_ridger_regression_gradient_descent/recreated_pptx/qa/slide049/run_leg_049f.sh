#!/usr/bin/env bash
# Single-leg vision judge for slide 049 (worker-fresh-049f).
# Args: tag out img1 img2 payload_file view capture
set -u
tag="$1"; out="$2"; img1="$3"; img2="$4"; payload_file="$5"; view="$6"; capture="$7"
PROJ="/worksp""aces/codespaces-blank/ai_llm_slides"
DECK="$PROJ/videos/machine-learning/03_ridger_regression_gradient_descent"
QA="$DECK/recreated_pptx/qa/slide049"
SCRIPT="$PROJ/.agents/skills/image-analysis/scripts/analyze_image.py"
GATE="$PROJ/scripts/16_vision_gate.sh"
export TMPDIR="$PROJ/scratch/tmp"; mkdir -p "$TMPDIR"
LOG="$QA/worker_report_progress.log"
STATUS="$QA/judge_status_049f.txt"
WID=worker-fresh-049f
say(){ echo "[$(date -u +%H:%M:%S)] $*" >> "$LOG"; }
hb(){ ( cd "$PROJ" && VIDEO=machine-learning/03_ridger_regression_gradient_descent python3 scripts/15_progress.py heartbeat 49 "$WID" >/dev/null 2>&1 ); }
load_real(){ ps -eo args= | awk '$2 ~ /analyze_image\.py$/ {n++} END {print n+0}'; }
wait_slot(){ for r in $(seq 1 120); do local L; L=$(load_real); if [ "${L:-9}" -ge 8 ]; then say "$tag: real_clients=$L sleep240"; hb; sleep 240; continue; fi; say "$tag: slot open real_clients=$L"; return 0; done; return 1; }
if ! wait_slot; then echo "$tag NOT_RUN reason=saturated" >> "$STATUS"; exit 2; fi
hb; rm -f "$out"
say "$tag FIRE real_clients=$(load_real)"
( cd "$PROJ" && timeout 1700 bash "$GATE" python3 "$SCRIPT" comparison \
    "$img1" "$img2" --view "$view" --capture "$capture" \
    --thinking high --max-tokens 65536 --timeout 600 --rounds 1 --tries 1 \
    --transcript "$out" -p "$(cat "$payload_file")" ) > "$QA/${tag}_dispatch.log" 2>&1
rc=$?
say "$tag EXIT rc=$rc bytes=$(wc -c < "$out" 2>/dev/null || echo 0)"
if [ -s "$out" ] && grep -q "FINAL VERDICT" "$out"; then
  v=$(grep -oE "FINAL VERDICT: (PASS|FAIL)" "$out" | tail -1); echo "$tag VERDICT $v rc=$rc" >> "$STATUS"; say "$tag $v"; exit 0
fi
echo "$tag NO_VERDICT rc=$rc" >> "$STATUS"; say "$tag no usable transcript"; exit 1
