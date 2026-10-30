#!/usr/bin/env bash
# Slide 019 attempt 30 — Template A + 4 crop legs on render_28 (post-a29-fix
# bytes: y170 red/green segments, header fs16 indent, continuous REDB/GREENB
# column edges, w3 0.99, x130 rule dropped). Payloads byte-exact from
# judge_protocol_03.md (A) / crop prompt with slide number substituted (B).
# Usage: dispatch_A30_B30_1200.sh [wait_max]
set -u
export TMPDIR=/home/ahmed/Projects/ai_llm_slides/scratch/tmp
cd /home/ahmed/Projects/ai_llm_slides || exit 1
VID=videos/machine-learning/03_ridger_regression_gradient_descent
Q=$VID/recreated_pptx/qa/slide019
WAIT_MAX="${1:-1800}"
LOG="$Q/legs_status_30_s4b.md"
PAYA="$Q/judgeA8_payload_20261024.txt"
PAYB="$Q/judgeB8_payload_20261024.txt"
[ -s "$PAYA" ] || { echo "FATAL: payload $PAYA missing/empty" | tee -a "$LOG"; exit 3; }
[ -s "$PAYB" ] || { echo "FATAL: payload $PAYB missing/empty" | tee -a "$LOG"; exit 3; }

ts() { date -u +%Y-%m-%dT%H:%M:%SZ; }
note() { echo "[$(ts)] A30: $*" | tee -a "$LOG"; }
q() { local n; n=$(pgrep -c -f analyze_image.py 2>/dev/null | head -n1); echo "${n:-0}"; }

wait_window() {
  local t0=$(date +%s)
  while :; do
    c=$(q)
    if [ "$c" -lt 8 ]; then return 0; fi
    el=$(( $(date +%s) - t0 ))
    if [ "$el" -ge "$WAIT_MAX" ]; then
      note "PARK $1: no window in ${el}s (pgrep=$c); honest no-verdict"
      return 42
    fi
    sleep 20
  done
}

run_leg() { # tag view capture img1 img2 payload transcript
  local tag="$1" view="$2" capture="$3" img1="$4" img2="$5" payf="$6" tr="$7"
  P="$(cat "$payf")"
  timeout 1700 bash scripts/16_vision_gate.sh python3 \
    .agents/skills/image-analysis/scripts/analyze_image.py comparison \
    "$img1" "$img2" \
    --view "$view" \
    --capture "$capture" \
    --thinking high --max-tokens 65536 --timeout 1200 --rounds 1 --tries 1 \
    --transcript "$tr" -p "$P" >> "$LOG" 2>&1
  rc=$?
  if [ -f "$tr" ] && grep -q "FINAL VERDICT:" "$tr" 2>/dev/null; then
    note "$tag: $(grep -o 'FINAL VERDICT:.*' "$tr" | tail -1 | cut -c1-60) (rc=$rc)"
  else
    note "$tag: NO VERDICT (rc=$rc) — honest no-verdict"
  fi
}

# ── Template A leg ────────────────────────────────────────────────────────────
note "payload A $(md5sum "$PAYA" | cut -d' ' -f1) len $(wc -c < "$PAYA")"
if wait_window "Template A"; then
  note "WINDOW OPEN (pgrep=$c) — DISPATCH Template A render_28 (attempt 30)"
  run_leg "Template A attempt 30" \
    "Slide 019 recreation attempt 30 - fidelity check vs original lecture frame" \
    "IMG1=150dpi PNG render of a 13.33x7.5in PPTX; IMG2=original lecture video frame" \
    "$Q/render_28.png" "$VID/unique_slides/slide_019.jpg" "$PAYA" "$Q/judge_attempt_30.txt"
else
  note "Template A not dispatched"
fi

# ── Crop legs ─────────────────────────────────────────────────────────────────
run_crop() { # slug desc
  local slug="$1" desc="$2"
  note "payload B $(md5sum "$PAYB" | cut -d' ' -f1)"
  if wait_window "crop_30 $slug"; then
    note "WINDOW OPEN (pgrep=$c) — DISPATCH crop_30 $slug"
    run_leg "crop_30 $slug" \
      "Slide 019 zoomed crop ${slug} — render vs original at matched scale (attempt 30)" \
      "IMG1=zoomed crop of a 150dpi PPTX render; IMG2=the SAME slide-space region cropped from the original lecture frame and upscaled to match IMG1's effective scale; region: ${desc}" \
      "$Q/crop_30_${slug}_render.png" "$Q/crop_30_${slug}_orig.png" \
      "$PAYB" "$Q/crop_30_${slug}_judge.txt"
  fi
}
run_crop title_bar   "top rule y170 + four column headers (fs16, indented): navy/red/green segments"
run_crop table_left  "outlier column + NO Regularizer column: headers, row groups 1-2, highlight band A"
run_crop table_right "Ridge lambda=3 + Ridge lambda=10 columns: continuous red/green rect edges, all three row groups, bottom tint strip"
run_crop noreg_rows  "NO REG W-vectors + test grids for all three row groups (x130 rule removed)"

note "attempt 30 dispatch complete"
exit 0
