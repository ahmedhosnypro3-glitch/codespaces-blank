# Slide 050 — attempt-8 adjudication record (w7, worker w050-fixjudge-20261024-114323)

Method: independent PIL re-measurement of `unique_slides/slide_050.jpg` (960x540,
1px=1pt) against a FRESH 150dpi render of the CURRENT pptx (`render_7.png`,
2001x1125, scale 2.0833).  `render_7.png` is byte-identical to the banked
`render_6.png` (0 differing pixels) — the prior lane's build was deterministic.

## TRIAGE of the trail

### judge_attempt_2.txt — Finding 1 (BLOCKER, omitted L4 caption) → CONFIRMED FIXED (prior lane)
Prior lane added the caption at x240..106 w280/20 (13pt, C1 red / C2 blue /
Zero green / rest black). Independently re-measured on render_7/8:
- orig L4 band x240..510 y110..124 ink present, word colours verified:
  C1 red 46px, C2 blue 26px, Zero green 167px, tail black 257px
- render L4 band x230..539 y109..130 ink present, same four colour families
  (red 211 / blue 208 / green 375 px @150dpi)
The element is present with matching colour semantics. CLOSED.

### judge_attempt_5.txt — Finding 1 (BLOCKER, "W vector truncated") → REFUTED; PRIOR LANE'S FIX WAS WRONG; REVERTED
The prior lane read the original's pink-box construct as THREE components
(5 / −1 / −1) and rebuilt `eq_050_finalW.png` as 3 components.  That is a
**misreading of the frame** — it invented content the original does not show.

Independent PIL proof (`w7_pinkbox_ascii.txt`, full-res ASCII of the original's
pink box, x743..827 y57..135, lum<205, 1 char = 1 frame px):
- exactly TWO digit rows exist in the construct:
    "5"   rows y68..83
    "−1"  rows y119..133
- exactly ONE fraction bar (y106, 19 cols wide)
- parens: left x745..746, right x786..787, both spanning y61..134
- the right ink column at x786..787 is the construct's own RIGHT PAREN, not a
  third component; x820..827 is the pink box's own right border
- the band y118..133 which the prior lane read as a "third digit" is in fact
  the −1 denominator row plus the right paren; there is no third stacked entry
The only coherent reading of the frame is `underline{W} = ( 5 / −1 )` — the same
two-component stacked-vector format as the Initial-W block, exactly as the
judge itself originally demanded ("W = (5, −1)" — the judge's OWN field reading).

Therefore: the original shows TWO components; the prior 3-component build was an
over-fix that DREW a defect the original lacks (standing law: "never draw a
defect the original lacks").  Action: reverted.

REVERT executed (copy-then-modify ledger):
- `eq_050_finalW.png` re-rendered as `\underline{W}=\left(\substack{5\\-1}\right)`,
  13pt black, 557x215px @600dpi; sidecar `eq_050_finalW.json` written explicitly
  to disk (render_eq.py only PRINTS sidecars — the prior lane's stale-sidecar
  bug is a real trap).
- Prior 3-component assets preserved: `eq_050_finalW.png.pre_w7_3comp`,
  `eq_050_finalW.json.pre_w7_3comp`.
- `recreated_pptx/build/slide_050.js` pre-revert copy banked at
  `qa/slide050/build_attempt_7_pre_finalW_revert.js`; no build-script edit was
  needed (the sidecar drives the geometry).
- pptx rebuilt → `recreated_pptx/slide_050_recreated.pptx` (12:19).
- `render_8.png` (11:52 -> rebuilt 12:20) confirmed: construct ink x745..810,
  y70..105, reading w_ = ( 5 / −1 ); the 7-vs-8 pixel diff is confined to
  x745..815 y70..105 (2240 px) — i.e. ONLY the pink construct changed.
- house_chrome_8: PASS.

### judge_attempt_5.txt — Finding 2 (BLOCKER, "η = 1" missing) → REFUTED (own PIL, decisive)
The prior lane refuted this; I re-verified independently because the banked
`orig_mathzoneL12_transcript.txt` vision read DID transcribe "REPEAT using Step η = 1".
My own measurement (`w7_eta2.py`), original frame, band y58..84:
- red ink runs (REPEAT using Step): x426..458 / 462..487 / 497..504 / 511..518 / 526..530
  → the red phrase TERMINATES at x530.
- ink in the "eta zone" x530..700: 167 px total, of which 166 px are BLACK and
  sit at x643..650 / 666..676 / 688..699 — those are the Z₁/Z₂/Z₃ label glyphs
  at y71..81 (the "Z" letters), i.e. the next element of the slide.
- between x531 and x642, y58..84: ZERO ink at lum<210, <200, <190, <175, <160.
- blue count in that zone = 0.  green = 0.  red = 1 stray px.
The zone right of "REPEAT using Step" is uniform cream (measured samples
(251,255,228) / (254,255,232) / (253,255,234)). There is NO η = 1 in the original.
Both vision reads were phrase-completion hallucinations. The prior lane's blue
"η" PNG (colour also wrong — matplotlib parses "C00000" as cycle index C0+0000 →
tab:blue) was correctly REMOVED. CLOSED — nothing to fix.

### judge_attempt_5.txt — Finding 3 (MINOR, six vs five class labels) → REFUTED (own PIL)
Class rows in the original carry six C-label clusters at 22.6px pitch
(x90..101 / 113..124 / 135..146 / 157..169 / 180..192 / 203..214) in BOTH the
top data table and the augmented-vectors table — the tables have six columns
x1..x6. The render matches. CLOSED.

### judge_attempt_5.txt — Finding 4 (MINOR, cursor "+" reproduced) → CONFIRMED FIXED (prior lane)
Original cursor "+" at x233..241 y414..419 (6 px ink at lum<210, isolated in the
left margin with no semantic role). On render_8 that box (x215..260 y405..425)
contains ZERO ink at lum<210/200/190. CLOSED.

## Containment / house chrome
- house_chrome_8: PASS (panel x112-1882 y94-bottom; strokes L/R/bottom present,
  top bare; badge centre (1824,152) d=68, tol 8).
- No render ink at all outside the gray panel (0 px, lum<210).
- No content ink crosses the C00000 left/right/bottom stroke lines beyond the
  strokes themselves.
