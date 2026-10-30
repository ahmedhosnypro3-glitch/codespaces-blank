# S23 paren sweep — slide 018 (2026-10-26, s23-paren-worker)

## Census (certified render_5.png)
- Band 1 (y270-450): `(` x1162 (−2.59) / `)` x1257 (+2.47). Correct.
- Band 2 (y570): `(` x1142 (−12.27) / `)` x1267 (+2.61). Correct.
- Band 3 (y840): `(` x1162 (−2.60) / `)` x1257 (+2.47). Correct.

## Asset truth
`build/assets/wbox018_band{1,2,3}.png` measured (alpha): band1 LP −10.20 / RP
+10.20; band2 LP −47.64 / RP +10.22; band3 LP −10.18 / RP +10.19 — all "("
left, ")" right. Matches the S22 refit (both sides fixed there; this slide had
both sides mirrored originally) and the att5 k5 certification.

## Verdict
NO mirrored delimiter. CLEAN — no rebuild.
