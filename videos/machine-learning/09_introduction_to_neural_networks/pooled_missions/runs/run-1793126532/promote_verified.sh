#!/usr/bin/env bash
# Promote build pptx -> deliverable, but ONLY when the build pptx provably
# produced the render the judge actually saw. Re-renders each build pptx and
# pixel-matches it against the judged render; promotes with cp -p so the
# mtime (and therefore verdict freshness) is preserved.
set -u
V=/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks
B=$V/recreated_pptx/build
OUT=$V/pooled_missions/runs/run-1793126532/promote_log.txt
export TMPDIR=/home/codespace/ai_llm_slides/scratch/tmp
mkdir -p "$TMPDIR"
log(){ echo "$(date +%F\ %T) $*" >> "$OUT"; }

pick_render(){
  n3="$1"
  cands=$(ls -t $B/slide_${n3}*rendered*.png 2>/dev/null | grep -v _resized)
  for c in $cands; do
    case "$c" in *_rejudge_rendered*|*_wave4_rendered*) echo "$c"; return 0;; esac
  done
  echo "$cands" | head -1
}

for n in "$@"; do
  n3=$(printf '%03d' "$((10#$n))")
  dest=$V/recreated_pptx/slide_${n3}_recreated.pptx
  src=$B/slide_${n3}_recreated.pptx
  if [ -f "$dest" ]; then log "$n3 SKIP already-promoted"; continue; fi
  if [ ! -f "$src" ]; then log "$n3 NO_BUILD_PPTX"; continue; fi
  judged=$(pick_render "$n3")
  if [ -z "$judged" ] || [ ! -s "$judged" ]; then log "$n3 NO_JUDGED_RENDER"; continue; fi
  tmp=$B/promote_${n3}_rendered
  rm -f ${tmp}*.png
  if ! bash $B/render_pdf.sh "$src" "$tmp" >> "$OUT" 2>&1; then
    log "$n3 RENDER_FAIL"; continue
  fi
  newpng=$(ls -t ${tmp}_rendered-*.png 2>/dev/null | head -1)
  if [ -z "$newpng" ]; then log "$n3 NO_NEW_PNG"; continue; fi
  res=$(python3 - "$judged" "$newpng" <<'PY'
import sys
from PIL import Image, ImageChops
a = Image.open(sys.argv[1]).convert('RGB')
b = Image.open(sys.argv[2]).convert('RGB')
if a.size != b.size:
    print(f"DIFF_DIM {a.size} vs {b.size}"); sys.exit(0)
d = ImageChops.difference(a, b)
bbox = d.getbbox()
mx = max(d.getextrema(), key=lambda t: t[1])[1]
px = sum(1 for p in d.getdata() if p != (0,0,0))
print(f"DIFF_MAXCHANNEL {mx} DIFF_PIXELS {px} BBOX {bbox}")
PY
)
  echo "$res" >> "$OUT"
  maxpx=$(echo "$res" | awk '{for(i=1;i<=NF;i++) if($i=="DIFF_MAXCHANNEL") print $(i+1)}')
  if [ -n "$maxpx" ] && [ "$maxpx" -le 2 ]; then
    cp -p "$src" "$dest"
    log "$n3 PROMOTED match(maxchannel=$maxpx) bytes=$(stat -c%s "$dest")"
  else
    log "$n3 REJECT mismatch: $res"
  fi
  rm -f ${tmp}_rendered-*.png
done
log "PROMOTE DONE"
