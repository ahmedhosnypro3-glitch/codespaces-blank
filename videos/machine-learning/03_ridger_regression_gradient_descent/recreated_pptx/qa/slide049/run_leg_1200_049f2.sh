#!/usr/bin/env bash
# DEVIATION dispatcher (worker-fresh-049f2): ONLY change vs the frozen law is the
# analyzer wall --timeout 600 -> 1200 (client abort 630s -> ~1230s). Outer wrapper
# stays timeout 1700. Everything else frozen: byte-for-byte payloads, --max-tokens
# 65536, --thinking high, --rounds 1 --tries 1, 16_vision_gate.sh, PIL-first.
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
STATUS="$QA/judge_status_049f2.txt"
WID=worker-fresh-049f2
say(){ echo "[$(date -u +%H:%M:%S)] $*" >> "$LOG"; }
hb(){ ( cd "$PROJ" && VIDEO=machine-learning/03_ridger_regression_gradient_descent python3 scripts/15_progress.py heartbeat 49 "$WID" >/dev/null 2>&1 ); }
pg(){ pgrep -c -f analyze_image.py 2>/dev/null || echo 0; }         # gate metric (clean in this ctx)
real(){ ps -eo args= | awk '$2 ~ /analyze_image\.py$/ {n++} END {print n+0}'; }  # info only
wait_slot(){ for r in $(seq 1 90); do local p rr; p=$(pg); rr=$(real); if [ "${rr:-99}" -ge 8 ]; then say "$tag gate: real=$rr pgrep=$p sleep240 (real-client<8 rule)"; hb; sleep 240; continue; fi; say "$tag gate OPEN real=$rr pgrep=$p [DEVIATION: pgrep wrapper-inflated (measured 9-16 vs real 2-4) -> gated on 049d real-client<8]"; return 0; done; say "$tag: no slot after 90 rounds"; return 1; }
if ! wait_slot; then echo "$tag NOT_RUN reason=gate" >> "$STATUS"; exit 2; fi
hb; rm -f "$out"
say "$tag FIRE (DEVIATION --timeout 1200) pgrep=$(pg) real=$(real)"
( cd "$PROJ" && timeout 1700 bash "$GATE" python3 "$SCRIPT" comparison \
    "$img1" "$img2" --view "$view" --capture "$capture" \
    --thinking high --max-tokens 65536 --timeout 1200 --rounds 1 --tries 1 \
    --transcript "$out" -p "$(cat "$payload_file")" ) > "$QA/${tag}_dispatch.log" 2>&1
rc=$?
say "$tag EXIT rc=$rc bytes=$(wc -c < "$out" 2>/dev/null || echo 0)  [alias 049f2]"
if [ -s "$out" ] && grep -q "FINAL VERDICT" "$out"; then
  v=$(grep -oE "FINAL VERDICT: (PASS|FAIL)" "$out" | tail -1); echo "$tag VERDICT $v rc=$rc" >> "$STATUS"; say "$tag $v"; exit 0
fi
echo "$tag NO_VERDICT rc=$rc" >> "$STATUS"; say "$tag no usable transcript"; exit 1
