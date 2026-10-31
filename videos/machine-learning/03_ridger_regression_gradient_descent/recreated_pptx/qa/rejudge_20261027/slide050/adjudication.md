# slide050 — FULL-leg FAIL adjudication (2026-10-31, fresh worker W01, PIL-first)

Transcript: `judge_full.txt` (clean, no 429) — FINAL VERDICT: FAIL.
Claims: MAJOR #1 "Iteration 2" is plain red text in orig vs white-on-red badge in
recreation; MAJOR #2 plot panel shifted down/compressed; MAJOR #3 plot frame touches
panel right/bottom strokes; MINORs #4/#5 (W= label proximity, typed-vs-handwritten).

Evidence (read-only PIL, slide space 960x540; render 2001x1125 scale 2.0844;
`adjudicate_w01_full.txt` = `rejudge_adjudicate.py 050 --full`: 177,272 diff px
(7.875%) spread across glyph bands; `adjudicate_w01_full_pil.txt`):

- #1 REFUTED: orig red-box zone x84-214 y277-305 is 92.7% red-filled (3,373/3,640 px),
  render 92.9% (14,600/15,718) — the ORIGINAL has the solid red box with white text;
  extents orig y277-305 x84-214 vs render y277.8-305.1 x83.5-213.0 (<=1.1 px). Build
  `build/slide_050.js:35` records the same measured box. Judge inverted the direction.
- #2 REFUTED: plot frame orig x313-824 y174-481 (w511 h307) vs render x310-825
  y171-482 (w~514 h~311) — within 3 slide px; not compressed or shifted.
- #3 REFUTED: house panel strokes orig x900-902 / y538-539 = render x900-900.5 /
  y538.1-538.6; plot right edge orig x824 vs render x825, bottom orig y481 vs render
  y482 — ~59 px clear of the right stroke and ~56 px above the bottom stroke in both.
- #4/#5 MINOR/advisory (typed-vs-handwritten, label proximity).

Disposition: all 3 MAJORs REFUTED by pixels. FULL = PASS (FAIL dismissed). Slide stays
certified; no build/pptx/DB change; no git; no evidence deleted.
