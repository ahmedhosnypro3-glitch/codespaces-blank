#!/usr/bin/env bash
# RE-JUDGE every CERTIFIED slide against its ORIGINAL frame.
# Phase 1 (gateway-free): re-render the CURRENT canonical deliverable via LO headless.
# Phase 2 (gateway): comparison judge, IMG1=render, IMG2=original, frozen template.
# Background task (NOT a subagent). Banked evidence is never overwritten: each slide
# writes into qa/slideNNN/rejudge_r2/.
set -u
NS=/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example
cd "$NS"
SKILL=/home/codespace/ai_llm_slides/.agents/skills/image-analysis
LOG=$NS/_pool/rejudge_certified.log
CERT="001 004 005 006 007 008 009 010 012 013 014 016 017 023 024 025 026 027 029 032"
LOGDIR=$NS/_pool/lo_r2
mkdir -p "$LOGDIR"
: > "$LOG"
log(){ echo "$(date +%F\ %T) $*" >> "$LOG"; }
# Each parallel worker holds ONE gate slot: xargs -P2 == 2 concurrent vision calls.
export VISION_SLOTS=1

render_one(){
  local n="$1"
  local src="recreated_pptx/slide_${n}_recreated.pptx"
  local out="qa/slide${n}/rejudge_r2"
  if [ ! -f "$src" ]; then log "RENDER-SKIP $n no canonical deliverable"; return 1; fi
  mkdir -p "$out"
  local work="$LOGDIR/w_${n}"
  rm -rf "$work"; mkdir -p "$work"
  cp -p "$src" "$work/slide_${n}.pptx"
  local md5
  md5=$(md5sum "$work/slide_${n}.pptx" | cut -d' ' -f1)
  log "RENDER $n src_md5=$md5"
  soffice --headless -env:UserInstallation=file://"$LOGDIR/profile" \
    --convert-to pdf --outdir "$work" "$work/slide_${n}.pptx" >> "$LOG" 2>&1
  if [ ! -f "$work/slide_${n}.pdf" ]; then log "RENDER-FAIL $n no pdf"; return 1; fi
  pdftoppm -png -r 150 "$work/slide_${n}.pdf" "$out/render" 2>> "$LOG"
  local png
  png=$(ls "$out"/render-*.png 2>/dev/null | head -1)
  if [ -z "$png" ]; then log "RENDER-FAIL $n no png"; return 1; fi
  python3 - "$png" "$md5" "$out" <<'PY'
import sys
from PIL import Image
p, md5, out = sys.argv[1], sys.argv[2], sys.argv[3]
im = Image.open(p).convert("RGB")
px = list(im.getdata())
mean = sum(sum(c) for c in px) / (len(px) * 3)
print(f"{p} size={im.size} mean={mean:.2f}")
assert im.size[0] >= 1900 and im.size[1] >= 1080, "render too small"
assert 20 < mean < 245, "render blank/suspect"
open(f"{out}/render_meta.txt", "w").write(f"png={p}\nsize={im.size}\nmean={mean:.4f}\nsrc_md5={md5}\n")
PY
  log "RENDER-OK $n png=$png"
  return 0
}

judge_one(){
  local n="$1"
  local out="qa/slide${n}/rejudge_r2"
  local png
  png=$(ls "$out"/render-*.png 2>/dev/null | head -1)
  [ -z "$png" ] && { log "JUDGE-SKIP $n no render"; return 0; }
  local i=1
  while [ $i -le 4 ]; do
    log "JUDGE $n attempt $i"
    bash _pool/vision_gate.sh python3 -u "$SKILL/scripts/analyze_image.py" comparison \
      "$png" "unique_slides/slide_${n}.jpg" \
      --view "Slide $n recreation render vs original lecture frame" \
      --capture "IMG1=150dpi PNG render of 13.33x7.5in PPTX; IMG2=original 960x540 lecture frame" \
      --max-tokens 24000 --timeout 780 --rounds 1 --tries 1 \
      -p "$(cat judge_template.txt)" > "${out}/judge_attempt_${i}.txt" 2>&1
    local rc=$? sz w v
    sz=$(wc -c < "${out}/judge_attempt_${i}.txt" 2>/dev/null || echo 0)
    w=$(grep -c '\[winner\]' "${out}/judge_attempt_${i}.txt" 2>/dev/null || echo 0)
    v=$(grep -o 'FINAL VERDICT: [A-Z]*' "${out}/judge_attempt_${i}.txt" 2>/dev/null | tail -1)
    log "JUDGE-END $n attempt $i rc=$rc bytes=$sz winner=$w verdict='${v:-NONE}'"
    if [ -n "$v" ]; then log "VERDICT $n $v"; return 0; fi
    i=$((i+1))
    if [ $i -le 4 ]; then sleep 90; else mv "${out}/judge_attempt_${i-1}.txt" "${out}/judge_attempt_dead.txt" 2>/dev/null; fi
  done
  log "JUDGE-DEBT $n no terminal verdict after 4 attempts"
  return 0
}
export -f render_one judge_one
export NS SKILL LOG LOGDIR
log "=== rejudge_certified driver start ==="
for n in $CERT; do echo "$n"; done | xargs -P 1 -I{} bash -c 'render_one "$@"' _ {}
log "=== renders done, judging ==="
for n in $CERT; do echo "$n"; done | xargs -P "${VISION_SLOTS:-2}" -I{} bash -c 'judge_one "$@"' _ {}
log "=== rejudge_certified driver end ==="
