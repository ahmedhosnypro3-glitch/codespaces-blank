# slide050 FULL leg FAIL — PIL-first adjudication (2026-10-31 ~03:2x UTC, fresh worker W03)

Transcript: `judge_full.txt` (clean, no 429) — FINAL VERDICT: FAIL (3 MAJOR, 2 MINOR, no BLOCKER).
PIL diff: `adjudicate_full_fresh.txt` (`rejudge_adjudicate.py 050 --full`): 177,272 diff px
(7.88%); ink only in render 45,106 px vs only in original 70,408 px (diffuse typed-vs-handwritten).

## MAJOR #1 "Iteration 2 = plain text in original, red badge in render" — REFUTED
- Original badge zone x80-200 y278-302: 2,584 of 2,880 px reddish, mean color (204,60,67) —
  the ORIGINAL carries a solid filled red badge there. Render same zone: 11,323 of 12,500 px
  reddish, mean (206,27,31). Both images have the filled badge; claim direction reversed.

## MAJOR #2 "plot panel shifted down / shorter" and MAJOR #3 "plot frame touches panel strokes" — REFUTED
- Plot frame lines measured identical in both: horizontal y132-172, 214, 245, 276, 337, 368,
  482-520; vertical x784 and x826-900 (slide-space). Render adds two light interior gridlines
  (y397, y428) — interior, not boundary contact. Frame containment unchanged.

## MINORs #4/#5 — advisory
- "W=" label/box spacing and typed-vs-handwritten: MINOR, ground-rule class.

Disposition: FULL = PASS (dismissed). No rebuild. Crop leg verdict pending at time of writing.
