# S23 paren sweep — slide 017 (2026-10-26, s23-paren-worker)

## Census (certified render_5.png)
- Band 1 (render y283-448): `(` x1162 (delta −2.90) / `)` x1255 (+3.32). Correct.
- Band 2 (y560-735): `(` x1144 (−6.26) / `)` x1245 (+2.92). Correct.
- Band 3 (y858-1015): `(` x1162-1169 (−2.93) detected; the RP component
  (x1244-1264, w20 h157) MERGED with neighboring content ink in the flattened
  render, so the auto-census dropped it below the curved threshold.

## Adjudication (PIL-first)
- Asset truth: `build/assets/wbox017_band{1,2,3}.png` measured directly (RGBA
  alpha): band1 LP −11.57 "(" / RP +13.45 ")"; band2 LP −24.62 / RP +10.45;
  band3 LP −11.71 / RP +1.70 (RP merged with matrix bars inside the asset —
  ASCII of the asset's RP region shows a clean ")" belly-right at x~800-838
  with the horizontal matrix bars touching it). All three bands: "(" left,
  ")" right — matches the S22 refit evidence (paren_refit_20261025, k5).
- ASCII of the render's band-3 RP (x1240-1268): vertical belly at x1258-1262,
  tips spreading left at top+bottom — true ")".
- S22 precedent: slide 017 was the origin of the defect class; fixed by
  `fix_wbox017_parens_dir_20261025.py`, certified att5 (k5 crops). Positive
  evidence referenced read-only.

## Verdict
NO mirrored delimiter. CLEAN — no rebuild.
