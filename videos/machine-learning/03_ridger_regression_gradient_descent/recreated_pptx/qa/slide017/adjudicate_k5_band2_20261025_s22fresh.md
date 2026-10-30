# S22 fresh carrier — K=5 band2 crop-leg adjudication (slide 017, 2026-10-25)

Leg: crop_5_band2 (transcript `crop_5_band2_judge.txt`: FINAL VERDICT FAIL,
1 MAJOR + 3 MINOR). Instrument: `adjudicate_k5_band2_20261025_s22fresh.py`
(slide-space pixel measurements on `render_5.png` + `unique_slides/slide_017.jpg`,
raw-frame ASCII bitmaps for glyph structure). Band 2 = frame y 255..395.

## MAJOR-1 "row labels: IMG1 X₁/X₂ (capital) vs IMG2 x₁/x₂ (lowercase)" — MAJOR REFUTED; delta real but settled MINOR class

New measurement (raw-frame bitmaps, th200 — stronger than the band1 crop-bbox
instrument):

| glyph (frame px) | orig t1 | orig t2 | render t2 |
|---|---|---|---|
| row-label main glyph | 169..180 = **12** | 308..318 = **11** | 306.3..319.3 = **13.4** |
| header cell X caps | 136..149 = **14–15** | 275..288 = **14** | 275.5..288.0 = **13** |
| row-1 value digits | 166..179 = **14–15** | 304..318 = **15** | 306.2..319.2 = **13.4** |

- The ORIGINAL's row-label main glyph is **x-height** (11–12 px ≈ 0.75–0.8 × its
  own cap/digit height 14–15 px), baseline-aligned, subscript dipping 1–2 px
  below. This holds on BOTH table instances.
- The RECREATION renders the labels at full cap height (13.4 = its digit
  height), wider advance (w 18.7–19.2 vs orig 13–15).
- **CORRECTION to the band1 K=5 record**: its MAJOR-2 refutation claimed
  "orig label h=27 TALLER than header caps h=25" (crop px) — a 1-frame-px
  delta inside JPEG/LANCZOS noise, and the direction is wrong. The original's
  labels are the SHORTER glyphs. The band1 record's operative outcome (finding
  = banked font-substitution MINOR, no content error) is unaffected and now
  rests on the evidence below instead.
- Why still not a MAJOR/content error: variable identity (X + subscripts 1/2,
  subscript structure) is correct in both; the delta is confined to typeface
  metrics of the label column. Certified slides **012/013** (same table
  pattern, founder-certified) carry the identical convention — 013's original
  shows the same x-height labels (169..181 vs digits 166..180) while its
  certified recreation renders cap-height labels. This is the deck's settled
  "row-label glyph width/size" font-substitution class (worker_report.md item,
  K=4 certificates for 017 full/wbox/band1/band2/band3/test all passed these
  pixels). S22 scope is delimiter work only — label-case rendering is a
  component-level convention outside this scope (re-opening it would cascade
  12→13→17→18). Classification: banked MINOR class, MAJOR severity refuted.

## MINOR-2 "superfluous underline under W" — banked item, no action

Same pixels as the K=4 wbox adjudication (worker_report.md): underline present
on BOTH sides — render 145 blue px vs orig 33 (JPEG-thinned). The K=4 wbox
judge saw it as "missing in IMG1", the K=5 band2 judge as "absent in IMG2" —
two readings of the same asymmetric stroke weight. Rule (e) medium class.
K=5 wbox crop is pixel-identical to K=4 outside the fixed lparen columns.

## MINOR-3 "norm line red in IMG1 vs blue in IMG2" — REFUTED

Norm-region ink (frame y 347..385, x 505..624): **orig blue 652 / red 248;
render blue 1444 / red 486** (the red counts are the wbox border columns
crossing the window). Blue-dominant on BOTH sides — the norm line is blue in
IMG1 exactly as in IMG2; the render's ink is simply heavier (bolder stroke).
The judge's color premise is false.

## MINOR-4 "arrows hollow in IMG1 vs solid in IMG2" — REFUTED / certified pixels

Arrow-region blue-px fill (band 2): arrow1 orig 180 vs render 147 frame-eq;
arrow2 orig 239 vs render 143 — both sides carry solid blue fill; no
hollow-vs-solid discontinuity; delta is stroke-weight/anti-aliasing (rule e).
The arrows are certified 017 component pixels, unchanged by the paren refit
(render5_vs_render4_diff.txt: diff confined to the left-paren columns);
re-litigating adjudicated pixels is barred (band1 MINOR-4 precedent).

## Conclusion

The FAIL is overturned on PIL evidence: MAJOR-1 downgraded to the settled
font-substitution MINOR class (with a measurement correction recorded against
the band1 note), MINOR-2 banked, MINOR-3/MINOR-4 refuted. No build edit → no
re-dispatch owed. The K=5 certificate set proceeds: full PASS + wbox PASS +
band1 (adjudicated clean) + band2 (adjudicated clean) + band3 pending.
