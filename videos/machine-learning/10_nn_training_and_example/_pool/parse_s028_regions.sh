#!/bin/bash
T=/home/codespace/.agents/skills/doc-parse/scripts/parse_document.py
C=_pool/crops028
for r in r_diagram r_header r_delta r_dw6 r_w6 r_dw7 r_w7 r_gray1 r_gray2; do
  echo "=== $r ==="
  timeout 180 python3 $T $C/$r.png -o _pool/parse028 --timeout 120 2>&1 | tail -2
done
