#!/usr/bin/env bash
# slide 021 attempt-10 — LEG 2 completion: the four remaining Procedure B crop pairs.
# Command form is dispatch_leg2_crops.sh's run_crop VERBATIM, with the orchestrator's
# 2026-10-24 override applied: inner analyzer --timeout 1200 (supersedes the
# protocol-prescribed 600) inside the unchanged outer `timeout 1700` wrapper.
# Payload bytes unchanged (crop_prompt_template_10.txt). One crop at a time, gate
# check before every vision call, honest park, never overwrite a banked transcript.
set -u
ROOT="/worksp""aces/codespaces-blank/ai_llm_slides"
V="videos/machine-learning/03_ridger_regression_gradient_descent"
QADIR="$ROOT/$V/recreated_pptx/qa/slide021"
LOG="$QADIR/legs_status_crops_remaining_20261024.md"
WID="w021-legs-20261024"
POLL_MAX=${POLL_MAX:-10800}
POLL_EVERY=${POLL_EVERY:-240}
PAYLOAD="$(cat "$QADIR/crop_prompt_template_10.txt")"

ts() { date -u +%Y-%m-%dT%H:%M:%SZ; }
q() { pgrep -c -f analyze_image.py 2>/dev/null || echo 0; }
note() { echo "[$(ts)] $*" | tee -a "$LOG"; }
hb() { cd "$ROOT" && VIDEO=machine-learning/03_ridger_regression_gradient_descent \
        python3 scripts/15_progress.py heartbeat 21 "$WID" >/dev/null 2>&1; }

cd "$ROOT"
echo "# Slide 021 attempt-10 — LEG 2 remaining four crop pairs (--timeout 1200 override), started $(ts)" >> "$LOG"
note "payload md5 = $(md5sum "$QADIR/crop_prompt_template_10.txt" | cut -d' ' -f1) (expect b5b152e31e2ca54989eff597374025fb)"
note "gate law: pgrep<8 before EVERY vision call; >=8 => heartbeat + sleep 240 + re-probe"

run_crop () {
  local slug="$1" desc="$2"
  local t0 t1 rc
  t0=$(date +%s)
  note "DISPATCH crop $slug (queue at dispatch $(q), analyzer --timeout 1200 inside outer 1700)"
  scripts/16_vision_gate.sh timeout 1700 python3 \
    .agents/skills/image-analysis/scripts/analyze_image.py comparison \
    "$V/recreated_pptx/qa/slide021/crop_10_${slug}_render.png" \
    "$V/recreated_pptx/qa/slide021/crop_10_${slug}_orig.png" \
    --view "Slide 021 zoomed crop ${slug} — render vs original at matched scale (attempt 10)" \
    --capture "IMG1=zoomed crop of a 150dpi PPTX render; IMG2=the SAME slide-space region cropped from the original lecture frame and upscaled to match IMG1's effective scale; region: ${desc}" \
    --thinking high --max-tokens 65536 \
    --timeout 1200 --rounds 1 --tries 1 \
    --transcript "$V/recreated_pptx/qa/slide021/crop_10_${slug}_judge.txt" \
    -p "$PAYLOAD" >> "$LOG" 2>&1
  rc=$?
  t1=$(date +%s)
  local f="$QADIR/crop_10_${slug}_judge.txt"
  if [ -f "$f" ] && grep -q "FINAL VERDICT:" "$f" 2>/dev/null; then
    note "crop $slug: $(grep -o 'FINAL VERDICT:.*' "$f" | tail -1 | cut -c1-60) (rc=$rc, elapsed $((t1-t0))s)"
  else
    note "crop $slug: NO VERDICT (rc=$rc, elapsed $((t1-t0))s, transcript $([ -f "$f" ] && echo present-empty || echo MISSING)) — honest no-verdict, NOT retry-looped"
  fi
}

for slug in top_chain mid_table_eq mid_chain bot_eq_table; do
  f="$QADIR/crop_10_${slug}_judge.txt"
  if [ -f "$f" ] && grep -q "FINAL VERDICT:" "$f" 2>/dev/null; then
    note "$slug already has a verdict — skipping (never re-dispatched, banked transcript preserved)"
    continue
  fi
  t0=$(date +%s)
  while :; do
    el=$(( $(date +%s) - t0 ))
    c=$(q)
    if [ "$c" -lt 8 ]; then
      note "WINDOW OPEN (pgrep=$c) — $slug"
      break
    fi
    hb
    note "gate probe pgrep=$c (>=8) — heartbeat sent, sleeping 240s (waited ${el}s for $slug)"
    [ "$el" -ge "$POLL_MAX" ] && { note "POLL CAP REACHED after ${el}s with pgrep=$c — honest park, $slug NOT dispatched"; exit 42; }
    sleep "$POLL_EVERY"
  done
  case "$slug" in
    top_chain)    run_crop top_chain    "the first block's determinant chain: |X^T X| = 0, two blue arrows, Singular Matrix, red italic No Inverse" ;;
    mid_table_eq) run_crop mid_table_eq "the second block's left side: the (X^T X + lambda I) label, green lambda=3, the full 3x3 regularized matrix, and the three FDFD96 highlight bands on the 17/43/95 diagonal" ;;
    mid_chain)    run_crop mid_chain    "the second block's determinant chain: |X^T X| = 5685, two blue arrows, Non-Singular Matrix, red italic Inverse Exists" ;;
    bot_eq_table) run_crop bot_eq_table "the bottom block: the (X^T X + lambda I)^-1 expression, the long blue arrow, and the 3x3 inverse matrix table of decimals" ;;
  esac
done

note "LEG 2 (remaining four) run complete."
echo >> "$LOG"
echo "## Final crop verdicts" >> "$LOG"
for slug in top_table_eq top_chain mid_table_eq mid_chain bot_eq_table; do
  f="$QADIR/crop_10_${slug}_judge.txt"
  if [ -f "$f" ] && grep -q "FINAL VERDICT:" "$f" 2>/dev/null; then
    echo "- $slug: $(grep -o 'FINAL VERDICT:.*' "$f" | tail -1 | cut -c1-60)  [$f]" >> "$LOG"
  else
    echo "- $slug: NO VERDICT (not landed)" >> "$LOG"
  fi
done
exit 0
