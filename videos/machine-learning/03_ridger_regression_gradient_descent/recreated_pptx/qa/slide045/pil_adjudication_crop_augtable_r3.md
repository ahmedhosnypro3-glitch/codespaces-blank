# Slide 045 — crop leg augtable (r3) PIL adjudication (2026-10-25, s7-judge-1024)

Transcript: crop_1_r3_augtable_judge.txt — FINAL VERDICT: FAIL (2 MAJOR).

## D1 "x1..x6 header labels absent in IMG1" — REFUTED

ASCII ink map of the region (frame px):
- ORIG label marks at y166..174 (x~96,126,148,172,194,214)
- RENDER label marks at y204 (x~96..102,122..126,148,172..178,200..206,216..220)
Six subscript labels present in BOTH; render's panel content sits ~30px lower
(spacing-rhythm MINOR, accepted — same class as the toppanel leg's M4).

## D2 "IMG2 has tall spanning parens per column; IMG1 loose scalars" — REFUTED

ASCII map of the original data rows (y184..222, x88..230) shows every value flanked by
SHORT paren strokes (~6-8 rows tall), one pair per scalar cell — there are NO tall
spanning enclosures in the original. The render (y190..222) has the same short-paren
per-cell structure. The judge inverted the two images' geometry claim; the mandated
"delimiter spans its lines" clause cannot fire when the original itself uses per-cell
short parens. Values match row-by-row (judge's own note).

## Conclusion

FAIL rests on two refuted findings. No build edit. Leg evidence: transcript + this record.
