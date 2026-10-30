# Slide 016 — attempt-8 adjudication (all legs: legA, last_bullet, full_body)

## Verdicts
- legA (`judge_attempt_8.txt`): **PASS**, zero discrepancies.
- crop last_bullet (`crop_8_last_bullet_judge.txt`): **PASS** (underlines, (N)/(d) red, wrap all match).
- crop full_body (`crop_8_full_body_judge.txt`): FAIL on 1 MAJOR + 4 minors — adjudicated below.

## full_body claims

| # | Claim | Evidence | Ruling |
|---|---|---|---|
| 1 | "(model parameters)" black in render, blue in original (MAJOR, high) | PIL column census of the ORIGINAL heading line (rows 122..152): blue ink spans cols 147..358 only ("Penalize large values of W"); "(model parameters)" occupies cols 366..513 with dark ink mean RGB (85,87,84) — BLACK, zero blue pixels. Render: dark extent 364..520, no blue in that span — IDENTICAL structure. Judge misread IMG2. | **REFUTED** |
| 2 | Lost bold/weight contrast inside red phrases (MINOR, med-high) | Weight-level judgment; verbatim text + color family correct | MINOR, accepted |
| 3 | "customized weigh factor" hue/underline tone (MINOR, low-med) | Judge itself flagged possible zoom artifact | MINOR, accepted |
| 4 | "(N)"/"(d)" weight regular vs bold (MINOR, medium) | legA + last_bullet legs read the same tokens as matching; low impact | MINOR, accepted |
| 5 | Right-edge crop offset (MINOR, high) | Judge marked non-content (crop alignment) | N/A |

## Outcome
All three attempt-8 legs clean after adjudication (no refuted-claim-driven re-roll needed;
attempt 8 was the sanctioned 7th and final roll). **visual_check = PASS**,
gen_status = passed. Deliverable: `slide_016_recreated.pptx`, render_8.png
(md5 7d4fdd31019f2bac6082be1b2d3eb9dc), legA transcript + 2 crop transcripts +
this file = evidence chain.
