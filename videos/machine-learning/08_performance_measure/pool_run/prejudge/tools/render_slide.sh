#!/usr/bin/env bash
# Render a single-slide pptx to a 150dpi PNG with a project-scratch LibreOffice
# profile (never /tmp). Read-only on the pptx.
#
# Usage: render_slide.sh <pptx> <outdir> <png_basename>
set -euo pipefail
PPTX="$1"; OUTDIR="$2"; NAME="$3"
NS=/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure
SCRATCH="$NS/pool_run/prejudge/scratch"
mkdir -p "$OUTDIR" "$SCRATCH/lo/${NAME}_profile" "$SCRATCH/lo/${NAME}_work"
soffice --headless \
  -env:UserInstallation="file://$SCRATCH/lo/${NAME}_profile" \
  --convert-to pdf --outdir "$SCRATCH/lo/${NAME}_work" "$PPTX" >/dev/null 2>&1
PDF="$SCRATCH/lo/${NAME}_work/$(basename "${PPTX%.pptx}").pdf"
pdftoppm -png -r 150 "$PDF" "$SCRATCH/lo/${NAME}_work/page"
SRC="$SCRATCH/lo/${NAME}_work/page-1.png"
cp "$SRC" "$OUTDIR/$NAME.png"
echo "$OUTDIR/$NAME.png"
