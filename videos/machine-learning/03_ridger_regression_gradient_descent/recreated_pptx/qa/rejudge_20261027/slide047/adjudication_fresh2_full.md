# slide047 FULL fresh2 adjudication (2026-10-31, this worker, PIL-first, read-only)

Leg: `judge_full_fresh2.txt` (2026-10-31 03:37:08 UTC, clean transcript, no 429, fresh2 pid 836634):
FINAL VERDICT FAIL. Claims:

| # | claim | sev | disposition | evidence |
|---|---|---|---|---|
| 1 | heading "Ugmented" vs orig "Augmented" (missing A) | MAJOR | REFUTED | original slide_047.jpg heading strip (x78-240 y144-163) is pixel-identical (IoU 0.985) to the same handwritten heading on 045/048/049/051 — the ORIGINAL omits the "A" on every perceptron-iteration frame; build `slide_047.js:155` and analysis verbatim both "Ugmented Vectors ( from Top )" (sic). 043/045 typo law: frame text wins, recreation matches |
| 2 | "( from Top )" vs "( from Top)" spacing | MINOR | REFUTED as defect | build + analysis verbatim carry the spaced parens "( from Top )" exactly as extracted from the frame |
| 3 | "C₂negative" run-on in top-box caption | MINOR | advisory | typed-vs-handwritten advance difference; no ink collision measurable (subscript glyph and "negative" do not overlap in render) |

Sweep: `adjudicate_fresh2_full.txt` — 145,400 diff px (6.46%), densest cells all in the top-band
text rows y112-135 (typed-vs-handwritten AA), no localized missing block; ink-only-in-original
heavier than render (handwriting vs typed), consistent with every dismissed FAIL this wave.

Disposition: FULL-leg FAIL **DISMISSED** — the only MAJOR is refuted by the sibling-frame pixel proof +
verbatim records; MINORs advisory. FULL=PASS (dismissed). CROP=PASS (crop_dense_judge_fresh2.txt,
clean 03:2x). `slide047/result.txt` written. Slide stays certified; no build/pptx/DB changes.
No git; no evidence deleted.
