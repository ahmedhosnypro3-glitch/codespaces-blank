# Adjudication 2026-10-31 — slide016 FULL FAIL (judge_full.txt) — DISMISSED

Read-only PIL-first adjudication vs `unique_slides/slide_016.jpg` (960x540) and
`render.png` (2001x1125, scale 2.0844). Helper output: `adjudication_full.txt`.

| claim | sev | disposition | key pixel evidence |
|---|---|---|---|
| 1 slide-wide serif (Times) in original vs sans (Arial) in recreation | MAJOR | REFUTED | native-res glyph art of the ORIGINAL: title capital "L" (x312-326, y64-83) = constant 4px stem, flat terminals, flat foot, no serif flares; header "R" (x114-117) uniform 2px stem, flat top; lowercase glyph flat terminals, constant 2px strokes. Same finding as the slide026 adjudication: the original is SANS at native res; apparent "serifs" at 2.08x zoom are JPEG/LANCZOS ringing (ground rule e). Recreation font = house Arial per build |
| 2 lost bold on "Squared Norm" / "sum of Absolute values" / regularization labels | MINOR | advisory at most | weight delta is a typed-render property; colors correct; not FAIL-sustaining |
| 3 "(model parameters)" bold in render | MINOR | advisory | style-level |
| 4 "customized weigh factor" color red-in-orig vs black-in-render | MINOR | advisory | underline present in both; color nuance below defect threshold; not FAIL-sustaining |

No BLOCKER; the single MAJOR is refuted by pixels. FULL FAIL DISMISSED 2026-10-31.
CROP leg was PASS (crop_dense_judge.txt). No reopen, no rebuild, no edits to deck
pptx/build/DB. No git, no evidence deleted.
