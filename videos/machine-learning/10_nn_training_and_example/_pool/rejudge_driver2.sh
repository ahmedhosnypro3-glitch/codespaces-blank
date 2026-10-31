#!/usr/bin/env bash
# Parallel RE-JUDGE of every CERTIFIED slide against its original (background task).
# Per-slide flock; skips slides that already hold a terminal verdict in rejudge_r2.
# Renders the CURRENT canonical deliverable, so a verdict is bound to current bytes.
set -u
NS=/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example
cd "$NS"
LOG=$NS/_pool/rejudge2.log
LOGDIR=$NS/_pool/lo_r2b
CERT="001 004 005 006 007 008 009 010 012 013 014 016 017 023 024 025 026 027 029 032"
LOCKDIR=$NS/qa/.rejudge2_locks
mkdir -p "$LOGDIR" "$LOCKDIR"
log(){ echo "$(date +%F\ %T) $*" >> "$LOG"; }
export -f log

has_verdict(){ ls "qa/slide${1}/rejudge_r2"/judge_attempt_*.txt 2>/dev/null | xargs grep -l 'FINAL VERDICT: \(PASS\|FAIL\)' 2>/dev/null | grep -q .; }

render_one(){
  n="$1"; src="recreated_pptx/slide_${n}_recreated.pptx"
  [ -f "$src" ] || { log "RENDER-SKIP $n no canonical deliverable"; return 1; }
  out="qa/slide${n}/rejudge_r2"; mkdir -p "$out"
  [ -s "$out/render-r2.png" ] && { log "RENDER-SKIP $n render already built"; return 0; }
  work="$LOGDIR/w_${n}"; rm -rf "$work"; mkdir -p "$work"
  cp -p "$src" "$work/slide_${n}.pptx"
  soffice -env:UserInstallation=file:///tmp/lo_r2_${n} --headless --convert-to pdf \
    --outdir "$work" "$work/slide_${n}.pptx" >> "$out/render.log" 2>&1
  pdf="$work/slide_${n}.pdf"
  [ -f "$pdf" ] || { log "RENDER-FAIL $n no pdf"; return 1; }
  pdftoppm -png -r 150 "$pdf" "$work/p" >> "$out/render.log" 2>&1
  first=$(ls "$work"/p-*.png 2>/dev/null | head -1)
  [ -n "$first" ] || { log "RENDER-FAIL $n no png"; return 1; }
  cp -p "$first" "$out/render-r2.png"
  md5=$(md5sum "$work/slide_${n}.pptx" | cut -d' ' -f1)
  echo "$md5" > "$out/render-r2.md5"
  log "RENDERED $n $out/render-r2.png (src md5 ${md5:0:8})"
  return 0
}

judge_one(){
  n="$1"; out="qa/slide${n}/rejudge_r2"
  render_one "$n" || return 0
  if has_verdict "$n"; then log "JUDGE-SKIP $n terminal verdict already banked"; return 0; fi
  exec 9>>"$LOCKDIR/slide_${n}.lock"; flock -n 9 || return 0
  if has_verdict "$n"; then log "JUDGE-SKIP $n verdict landed while locking"; return 0; fi
  log "JUDGE-START $n"
  nohup bash _pool/judge_one_slide.sh "$n" "$out/render-r2.png" "$out" 8 \
    >> "$out/judge_runner2.log" 2>&1 &
  log "JUDGE-LAUNCH $n detached"
  return 0
}
export -f render_one judge_one has_verdict
export NS LOG LOGDIR CERT LOCKDIR
log "=== rejudge2 driver start (certified slides, parallel) ==="
for n in $CERT; do echo "$n"; done | xargs -P "${RJ_PAR:-3}" -I{} bash -c 'judge_one "$@"' _ {}
log "=== rejudge2 driver end ==="
