#!/bin/bash
# Render PDF and PNG for a given slide PDF using LibreOffice + pdftoppm
# Usage: bash render_pdf.sh <pptx_path> <output_prefix>

set -euo pipefail

PPTX_PATH="$1"
OUT_PREFIX="$2"

# Convert PPTX to PDF using LibreOffice headless
TMPDIR_R=$(mktemp -d)
trap 'rm -rf "$TMPDIR_R"' EXIT

libreoffice --headless --convert-to pdf --outdir "$TMPDIR_R" "$PPTX_PATH" 2>&1

# Find the generated PDF
PDF_FILE=$(find "$TMPDIR_R" -name '*.pdf' | head -n 1)
if [ -z "$PDF_FILE" ]; then
    echo "ERROR: LibreOffice produced no PDF for $PPTX_PATH"
    exit 1
fi

# Convert PDF to PNG at 150dpi
pdftoppm -r 150 -png "$PDF_FILE" "${OUT_PREFIX}_rendered"

echo "Rendered: ${OUT_PREFIX}_rendered-*.png"