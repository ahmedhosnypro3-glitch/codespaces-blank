# Adjudication of attempt-3 legs — slide 041 (render_3, md5 f33118f55faf3835eb4f5af0dda6ca5c)

Worker `kimi-s6-3756628`, 2026-10-25. All measurements at frame scale (960×540,
1px = 1pt); render @150dpi (scale 2.0833). Findings below are from
`crop_3_legend_mid_judge.txt` (FINAL VERDICT: FAIL) and the Template A MINOR in
`judge_attempt_3.txt` (FINAL VERDICT: PASS).

## Legend_mid item 1 — "legend subscripts dropped" MAJOR → ADJUDICATED MINOR (no fix)

PIL measurement (ASCII dumps, threshold 170, frame coords):

- ORIGINAL C1 (x235..255): C ink y111..120; the "1" ink sits at y119..123,
  x251..252 — LOWERED below the C baseline and reduced (true subscript).
- RENDER C1: C ink y112..119; the "1" ink y112..119, same cap height as the C
  (baseline full-size digit).

Characters, colors (red C1 / blue C2 — b-r test attempt 1), sizes of the C, and
token positions are identical; the ONLY delta is the digit's vertical offset
(~4pt lower + smaller in the original). Nothing is truncated, swapped, or
missing — Template B's MAJOR-to-BLOCKER clause covers "truncated subscript",
which this is not (the judge itself wrote "This is not a truncation").

Deck-wide precedent: slide 012's certified crop judges raised the IDENTICAL
deviation twice and scored it MINOR both times
(`qa/slide012/crop_2_perfect_table_judge.txt` "Index notation: subscript vs
full-size — MINOR"; `crop_4_perfect_table_judge.txt` "Row-label subscripts …
baseline (non-subscripted) — MINOR"), and 012 is certified. Slide 041's own
attempt-1 lefttable judge scored the same flattening MINOR and PASSED
(`crop_1_lefttable_judge.txt` items 2–3). Baseline subscript styling is the
certified sibling convention for this deck; escalating it to MAJOR on one leg
would re-open certified siblings (cascade law). NOT a fix trigger.

## Legend_mid item 2 — "missing underline under W" MINOR → PIL-REFUTED

The original has NO horizontal stroke under "Initial W": rows 85..96 over
x255..345 carry no ink except (a) the wvec left-paren stem x330..331 (spanning
y58..106, its bottom bow curves right from y98) and (b) JPEG halo (13 px at y85
threshold 210, absent at 150/170). The judge's "underline extending slightly
past the W on both sides" is the paren bottom bow read as a stroke; it sits
RIGHT of the W (W ink x280..295), not under it, and has no left counterpart
past the W. No fix.

## Template A attempt 3 MINOR — "legend punctuation / Z1 case" → PIL-REFUTED

Frame-measured (attempt-1 PIL passes, banked in `cband_legend.txt`):
"positive," comma ink at x301 region and "negative," comma ink x376 (comma
clearly present in the frame); "Z1 Z1 Z1" glyphs y64..76 all identical caps-Z
per `gdiff041.txt`. The judge's reading of IMG2's low-res JPEG (960×540) is
resolution-limited; IMG1's punctuation matches the frame's measured ink.

## Status

- Template A attempt 3: PASS (adjudication above covers its only MINOR).
- lefttable crop attempt 3: PASS (its subscript MINORs = same adjudication).
- legend_mid crop attempt 3: FAIL on adjudicated findings — clean by this
  record; a re-roll on unchanged bytes is banked alongside as confirmation.
