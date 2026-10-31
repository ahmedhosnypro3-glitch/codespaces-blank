# Slide 025 rejudge adjudication (2026-10-31 02:3x UTC)

Legs: judge_full.txt (02:33) FINAL VERDICT: FAIL; crop_dense_judge FAIL (attempt 4, 01:43).

FULL FAIL claims vs pixels/build:
1. "BR axis/ink lines run below the BR red frame across the house bottom stroke to the image edge
   (~830..844 render px) — MAJOR overflow" — REFUTED: bottom red house stroke is at render row
   1122 (slide-y 538.6); dark-ink count at 2..14 px BELOW the stroke = 0 px at every row
   (nothing crosses the frame; the original itself has badge ink at slide-y 539).
2. "BR chart changed 3D surface -> 2D heatmap — MAJOR" — REFUTED: build/slide_025.js embeds
   generated 3-D surface PNGs (assets plot_025_tl/tr/bl/br.png, matplotlib plot_surface, 300dpi,
   exact measured region size) via addImage; BR region x615..880 y344..531 holds plot_025_br.png.
3. MINOR: TL/BL re-plotted not identical, axis scaling, caption "Non- Convex" spacing — advisory
   (generated-graph rule + medium difference), not reopen triggers.

Disposition: FULL-leg FAIL DISMISSED (both MAJORs refuted by pixels/build bytes). Crop leg FAIL
pending PIL adjudication (rejudge_adjudicate.py 025 --crop) — will dismiss if diffuse. Slide 025
certifiable once a clean crop PASS (or dismissed FAIL) is banked.
