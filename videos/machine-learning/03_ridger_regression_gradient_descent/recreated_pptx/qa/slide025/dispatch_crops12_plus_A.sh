#!/usr/bin/env bash
# Slide 025 attempt-12 certification legs on render_3 (current build bytes):
# 5 zoomed crop-pair legs (Template B, --timeout 600) + 1 full-slide Template A
# leg (--timeout 1200), run sequentially, each behind a pgrep<8 gate window.
# Paths adapted to this codespace; transcripts land in qa/slide025/.
set -u
ROOT="/home/codespace/ai_llm_slides"
NS="$ROOT/videos/machine-learning/03_ridger_regression_gradient_descent"
VID="videos/machine-learning/03_ridger_regression_gradient_descent"
Q="$NS/recreated_pptx/qa/slide025"
RJ="$NS/recreated_pptx/qa/rejudge_20261027"
LOG="$Q/legs_status_crops12_run1.md"
export TMPDIR="$ROOT/scratch/tmp"
cd "$ROOT" || exit 1

ts() { date -u +%Y-%m-%dT%H:%M:%SZ; }
q() { local n; n=$(pgrep -c -f analyze_image.py 2>/dev/null | head -n1); echo "${n:-0}"; }
note() { echo "[$(ts)] $*" | tee -a "$LOG"; }
WAIT_MAX=10800

wait_window() {
  local label="$1" t0=$(date +%s) c el
  while :; do
    c=$(q)
    if [ "$c" -lt 8 ]; then note "WINDOW OPEN for $label (pgrep=$c, waited $(( $(date +%s) - t0 ))s)"; return 0; fi
    el=$(( $(date +%s) - t0 ))
    if [ "$el" -ge "$WAIT_MAX" ]; then note "PARK $label: no window in ${el}s (pgrep=$c) — NOT dispatched"; return 42; fi
    sleep 20
  done
}

run_leg() {  # run_leg <img1> <img2> <view> <capture> <timeout> <transcript> <payload>
  local img1="$1" img2="$2" view="$3" cap="$4" tmo="$5" tr="$6" pay="$7"
  timeout 1700 bash scripts/16_vision_gate.sh python3 \
    .agents/skills/image-analysis/scripts/analyze_image.py comparison \
    "$img1" "$img2" \
    --view "$view" --capture "$cap" \
    --thinking high --max-tokens 65536 \
    --timeout "$tmo" --rounds 1 --tries 1 \
    --transcript "$tr" -p "$pay" >> "$LOG" 2>&1
  local rc=$?
  if [ -f "$tr" ] && grep -q "FINAL VERDICT:" "$tr" 2>/dev/null; then
    note "$(basename "$tr"): $(grep -o 'FINAL VERDICT:.*' "$tr" | tail -1 | cut -c1-60) (rc=$rc)"
  else
    note "$(basename "$tr"): NO VERDICT (rc=$rc, transcript $([ -f "$tr" ] && echo present-empty || echo MISSING))"
  fi
  return 0
}

PAYB="$Q/payload_B_025.txt"
PAYA="$RJ/payload_A.txt"
note "start attempt-12 legs on render_3; payloads B=$(md5sum "$PAYB" | cut -d' ' -f1) A=$(md5sum "$PAYA" | cut -d' ' -f1)"

for slug in tr tl bl br title; do
  desc=""
  case "$slug" in
    tr)    desc="top-right convex bowl: inverted x-axis tick order, sharper spike, dotted gridlines, floor contours" ;;
    tl)    desc="top-left concave dome with floor contour projections" ;;
    bl)    desc="bottom-left non-convex surface with extrema labels and leaders" ;;
    br)    desc="bottom-right gradient-descent path surface" ;;
    title) desc="title band text" ;;
  esac
  wait_window "crop_$slug" || continue
  run_leg "$Q/crop_12_${slug}_render.png" "$Q/crop_12_${slug}_orig.png" \
    "Slide 025 zoomed crop ${slug} — render vs original at matched scale (attempt 12)" \
    "IMG1=zoomed crop of a 150dpi PPTX render; IMG2=the SAME slide-space region cropped from the original lecture frame and upscaled to match IMG1's effective scale; region: ${desc}" \
    600 "$Q/crop_12_${slug}_judge.txt" "$(cat "$PAYB")"
done

wait_window "full_A" || exit 0
run_leg "$Q/render_3.png" "$VID/unique_slides/slide_025.jpg" \
  "Slide 025 recreation attempt 12 — fidelity check vs original lecture frame" \
  "IMG1=150dpi PNG render of a 13.33x7.5in PPTX; IMG2=original lecture video frame" \
  1200 "$Q/judge_att12_full.txt" "$(cat "$PAYA")"

note "attempt-12 leg run COMPLETE"
exit 0
