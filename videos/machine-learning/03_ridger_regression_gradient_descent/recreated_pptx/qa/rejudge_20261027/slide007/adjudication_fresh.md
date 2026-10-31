# slide007 crop-leg FAIL adjudication (2026-10-31 ~03:1x, fresh worker, PIL-first)

Fresh leg: `crop_dense_judge_fresh.txt` (vision_leg.sh attempt=1 rc=0, no 429, t=600,
payload_B_007.txt, crop pair region 60,184-344,392) — **FINAL VERDICT: FAIL**.
Prior FAIL `crop_dense_judge.txt` (02:44) adjudicated earlier today
(`adjudicate_fresh_crop.txt`): 24.6% diffuse diff, densest cells 230-264 px in 24px cells
across text bands, no localized block. Banked `crop_dense_judge_retry.txt` (2026-10-30) = PASS.

Census (`rejudge_adjudicate.py 007 --crop`, banked): render 592x434 vs orig 592x434,
diff 63,267 px (24.6%); ink-only-render 21,152 vs ink-only-orig 28,107 (original-heavy =
handwriting heavier than typed text).

## Claim 1 (MAJOR: render heading reads "Linear regression model ha…", orig ends clean before right edge) — REFUTED

Ground truth: `build/slide_007.js:94` heading = "Linear regression model has FOUR
problems:" — the string genuinely continues past "model"; the crop right edge (slide x344)
cuts the heading in BOTH images. Pixel proof, top heading line (crop cols; render line
y31-62, orig line y38-79):

- orig heading ink run is one continuous handwritten cluster cols 62-591 (to the crop
  right edge), ink 12,389 px; render clusters end (557,591), ink 6,686 px.
- right-edge strip cols 540-591 of the heading line: orig 1,396 ink px vs render 527 px —
  the ORIGINAL is inked at the right edge at least as much as the render. No render-only
  trailing glyph exists; the typed "has" corresponds to handwritten ink in the original.
- underline: render y66-68 run cols 58-591 (to edge); orig underline sits inside the
  handwriting band (y80-120 shows only cols 43-272 = descenders/pen marks) — the judge's
  "underline terminates early in IMG2" reading is a handwriting-vs-typed artifact
  (ground rule d), not a content difference.

## Claim 2 (MAJOR: 4th bullet completes inside region in render but clipped mid-word in orig; recreation "collapsed" the two Matrix Inversion bullets) — REFUTED

- Bottom visible line (render y337-371, orig y348-383): BOTH end at crop col 591 —
  render clusters [..., (462,591)], orig [..., (459,591)]. Both are clipped at the crop
  edge; the render does NOT complete with clearance. (The line is
  "➢Matrix Inversion Problem [2] (Large Matrix dimension)" — long in both.)
- The two "Matrix Inversion" bullets are NOT collapsed in the build:
  `build/slide_007.js:111` = "[1] (Singular Matrix)", `:123` = "[2] (Large Matrix
  dimension)", matching `analysis/slide_007_final.json` verbatim bullets exactly.

## Claim 3 (MINOR bullet glyph weight) — advisory, ground-rule (d).

Disposition: fresh crop FAIL **DISMISSED** — both MAJORs refuted by pixels; no
BLOCKER/MAJOR survives. CROP = PASS (dismissed), consistent with the banked 2026-10-30
crop PASS. FULL = PASS (`judge_full.txt` 2026-10-27, clean, MINOR advisory only).
Slide 007 rejudge complete; certification stands; no build/pptx/DB changes; no git;
no evidence deleted (both FAIL transcripts remain banked).
