# S22 fresh carrier — K=5 band3 crop-leg adjudication (slide 017, 2026-10-25)

Leg: crop_5_band3 (transcript `crop_5_band3_judge.txt`: FINAL VERDICT FAIL,
2 MAJOR + 1 MINOR). Instrument: red-ink run-length scan of the band-3 region
(frame y 392..532) on `unique_slides/slide_017.jpg` vs `render_5.png`.

The leg's own content audit found ZERO content deltas ("No wrong digits, no
missing rows, no swapped values, no garbled glyphs, no delimiter problems —
all content matches exactly", including the refit parens: "big parens
spanning all three lines ... delimiter geometry correct").

## MAJOR-1/2 "red rectangular border around the Train/Test header rows missing in IMG1" — REFUTED

Red-ink run-length scan (count>60/row threshold, frame px):

- ORIG header band y419..426: scattered red, 65–103 px/row, x-extent
  183..863 — that is the ALTERNATING RED HEADER TEXT (X₂/X₄/X₆/X₈ cells etc.),
  not a border. No continuous red run anywhere near the ~680 px a rectangle
  edge would produce.
- ORIG verticals: only x505..507 / x621..623 (123–127 px) are real red
  verticals — the W-BOX borders. All other red verticals (26–47 px at
  x194..198, x272..279, x353..361, x432..445, x739..753, x840..855) are text
  glyph strokes at cell positions.
- RENDER: identical structure — red text rows y413..425 (73–190 px/row,
  heavier strokes = the known weight class), wbox borders y402..404/y527..528,
  no header rectangle either.

The judge's premise ("clearly present in the original") is false; its own
MINOR-3 half-concedes the mechanism ("could partly be JPEG bleed"). What it
read as a red border is the JPEG-bled alternating red header text.

## MINOR-3 "gridline tint pink (IMG2) vs gray (IMG1)" — banked item

Same finding as K=4 band2 item 1 and K=4 band3 item 2 (test-gridline color),
adjudicated rule (e) JPEG-bleed class; K=5 band3 render pixels are identical
to K=4 outside the fixed lparen columns (render5_vs_render4_diff.txt).

## Conclusion

Both MAJORs are pixel-refuted (the alleged red borders do not exist in IMG2);
MINOR is the banked gridline-tint item. FAIL overturned. No build edit → no
re-dispatch owed. 017 K=5 certificate set is COMPLETE: full PASS +
wbox PASS + band1/band2/band3 adjudicated clean (banked test certificate
carries per crop5_test_identity_proof.txt).
