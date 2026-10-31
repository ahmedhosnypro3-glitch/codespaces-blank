#!/usr/bin/env bash
# W5: launch slide015 FULL fresh leg only if result.txt FULL != PASS and no live
# vision_leg.sh wrapper is writing a judge_full transcript for slide015.
set -u
ROOT=/home/codespace/ai_llm_slides
NS=videos/machine-learning/03_ridger_regression_gradient_descent
RJ=$NS/recreated_pptx/qa/rejudge_20261027
D=$RJ/slide015
mkdir -p "$RJ/legs_20261031.pids"

have=$(grep -oE '^FULL=[A-Z]+' "$D/result.txt" 2>/dev/null | cut -d= -f2)
[ "$have" = PASS ] && { echo "SKIP 015 full already PASS"; exit 0; }

live_full() {
  for p in $(pgrep -f 'vision_leg[.]sh'); do
    [ "$p" = "$$" ] && continue
    args=$(tr '\0' ' ' < /proc/$p/cmdline 2>/dev/null) || continue
    case "$args" in
      *"slide015/"*judge_full*) return 0;;
    esac
  done
  return 1
}
if live_full; then echo "SKIP 015 full live wrapper on same leg"; exit 0; fi

setsid nohup bash "$ROOT/$RJ/vision_leg.sh" "$D/judge_full_fresh5.txt" 1200 \
  "$D/render.png" "$ROOT/$NS/unique_slides/slide_015.jpg" \
  "Slide 15 recreation — fidelity check vs original lecture frame" \
  "IMG1=150dpi PNG render of 13.33x7.5in PPTX; IMG2=original 960x540 lecture frame" \
  "$ROOT/$RJ/payload_A.txt" > "$D/judge_full_fresh5.wrapper.out" 2>&1 &
echo $! > "$RJ/legs_20261031.pids/015_full_fresh5.pid"
echo "LAUNCH 015 full fresh5 pid $! -> judge_full_fresh5.txt t=1200 payload_A.txt"
