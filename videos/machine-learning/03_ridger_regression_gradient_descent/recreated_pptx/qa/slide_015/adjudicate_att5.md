# Slide 015 — attempt-5 legA adjudication (fresh-eyes re-dispatch on unchanged bytes)

Worker: s26-1415-worker-1793022298 (pool scope S26_014_015, run 299640), 2026-10-26.
Context: att4 parked after 3 legA FAILs on unchanged bytes (render_4, md5
0019627f1ec094510c369801269762d3, re-verified current at resume), all refuted by
pixel evidence (`adjudicate_attempt_4.md`). The orchestrator's wave brief ordered
a fresh-eyes legA re-dispatch. Dispatch: `dispatch_5_judgeA.sh` (probe + Template A,
payload md5 9387f5fbb94ef05a31db19f1e018dde1 = frozen template). Transcript:
`judge_attempt_5.txt` (att4's transcripts banked, untouched).

Verdict: **FAIL** — 5 MAJOR + 2 MINOR claims. Adjudicated PIL-first below
(`adjudicate_att5.out.txt`, `adjudicate_att5_r2.out.txt`, `adjudicate_att5_r3.out.txt`,
`adjudicate_att5_r4.out.txt` + doc-parse transcripts `scratch/tmp/att5_docparse/`).

| # | Claim (sev) | Measurement | Ruling |
|---|---|---|---|
| 1 | Eq1 second factor: original "(X−XW)" vs render "(Y−XW)" (MAJOR) | Independent doc-parse of the original's L1-right crop (4× LANCZOS, `att5_L1r_orig.png`) reads `½(Y−XW)^T(Y−XW)+½λW^TW` — Y, not X. The analysis raw transcription (vision, 2026-10-20) reads the same. The render's own crop parses identically. Three independent reads agree on Y−XW. | **REFUTED** — judge misread the handwritten Y |
| 2 | Inline λ-terms recolored black; green duplicates float as extra lines (MAJOR) | Green row-census in the cream box: render green bands at y131..154 / 189..213 / 242..266 (2412/1272/1270 px) = INSIDE the three dark line bands (105..154 / 164..213 / 217..266); zero green rows outside them. Original green bands y109..152 / 168..210 / 222..264 — same structure. Line-band census: 3 dark bands in BOTH (orig 109..151, 168..210, 222..263; render 105..154, 164..213, 217..266). | **REFUTED** — inline green present; no floating rows; matches settled att4 MAJOR-1 refutation |
| 3 | Spurious J(W) annotation tags colliding with equations (MAJOR) | Same census as #2: exactly 3 line bands in both images, no extra annotation rows. Settled att4 park note measured 1 J(W) cluster/line (unchanged bytes). | **REFUTED** — repeats the settled refutation |
| 4 | Omitted ⇒ arrow before green box (MAJOR) | Gap x503..545, y468..519: original 12 ink px (the settled closing-paren/ Y-stroke tails at the window's left edge), render 0. Settled twice (`adjudicate_arrow.txt`, att4 MAJOR-2). | **REFUTED** — settled; no arrow exists in the original |
| 5 | Stray λI annotations under final equation / inside green box (MAJOR) | Green census x500..900, y420..535: original 3058 px ALL inside the green box interior (the boxed formula's own ink); render 3714 px likewise. Zero green (or other) ink under the final equation in either image. Box centering (claim 7's basis): formula ink margins top/bottom = orig 4.0/5.0 px, render 3.4/4.0 px. | **REFUTED** — the "λI" the judge saw is the boxed formula's own content |
| 6 | "Best W" — W not red (MINOR) | Original: red glyph burst x291..310, y297..311 (214 red px, core RGB ≈ (180,6,29) = C00000 family) inside the sentence line, at the W's measured position (render W cluster x291.9..308.2). Render: 0 red px in the pink box interior. Build drew the whole sentence black. | **REAL → FIXED**: "W" run recolored RED (C00000) in build/slide_015.js; re-rendered as render_6 (att6) |
| 7 | Result formula not vertically centered in green box (MINOR-to-MAJOR) | Formula ink margins top/bottom: orig 4.0/5.0 px, render 3.4/4.0 px (box h 53) — render is if anything 0.8px more balanced. | **REFUTED** |

## Disposition

One REAL finding (claim 6, minor severity) — fixed as the smallest correct change
(single text-run recolor; pre-change build banked as `build_attempt_5_pre.js`).
The rebuilt pptx re-renders as **render_6.png**; word positions verified unchanged
(sentence ink x208.8..709.5 in both R4 and R6; per-word clusters within ±0.5 px;
the run split only flipped sub-pixel AA along the line). House chrome PASS on
render_6; containment 0 spills. Attempt 6 = re-run BOTH legs from render_6
(Template A + 5 re-cut crop pairs, `cut_crops_6.py`/`crops_6.json`).

Per the protocol, an att6 judge verdict on the new bytes supersedes att5's
refuted mass; att5 counts as the spent attempt (5 of 6 → att6 = 6 of 6).
