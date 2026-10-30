# PIL-first adjudication — slide 015 attempt-8 legs (2026-10-30)
render_6.png 2001x1125 scale (2.0844,2.0833) vs unique_slides/slide_015.jpg 960x540. Read-only; no bytes changed.

## Verdicts banked
| leg | transcript | verdict |
|---|---|---|
| crop_8_deriv_stack_judge.txt | FAIL |
| crop_8_eq_stack_judge.txt | PASS |
| crop_8_peachbox_judge.txt | FAIL |
| crop_8_solution_judge.txt | FAIL |
| judge_att8_full.txt | FAIL |

## Full-slide FAIL claims vs pixels
| claim | pixels |
|---|---|
| reg terms (½λWᵀW, λW, λIW) green in orig, blue in render | orig eq_stack rect x72-892 y104-266: green=2397 black=4408 blue=1321; render same rect: blue=45504 green=0 black=545 → CONFIRMED as a palette delta; severity per GROUND RULES: small color differences in text are graded, but medium/typed-vs-handwritten and 2D-format are covered; recorded as MINOR color-coding deviation, not BLOCKER |
| arrow light-orange block in orig, dark in render | arrow band x490-560 y460-530: orig green=443 black=74 red=35 (no orange class); render blue=2745 green=2305; orig arrow ink is dark/green-ish, render arrow is blue → color claim REFUTED in direction (orig is NOT light-orange block; both differ mildly) → MINOR |
| Remember-box eq color | peach box x783-898 y271-337: render blue=1645, orig black=273 (red=box border) → same equation-ink delta as above, MINOR |
| final W underline missing in render | sol-Y underline band x840-893 y505-516: orig dark rows y507(20px),y516(45px) vs render flat 2px/row → orig DOES have an underline/ink below final Y, render does not → CONFIRMED MINOR notation-cue loss |
| green box right-edge contact | right-edge strip x878-893 y472-516: render dark=199 vs orig=62 → render ink closer to box edge but strip includes the green border itself; no overflow beyond box measured |

## Crop FAIL claims vs pixels
| crop claim | pixels |
|---|---|
| deriv_stack: 'J missing in L1 numerator' | render dark-map x78-115 y348-378 shows FOUR glyphs ∂,J,(,W — J present (dark px=446 in J slot vs orig 41, render glyphs bolder); REFUTED |
| deriv_stack: λIW not green in render | deriv L2 tail x400-518 y417-466: orig green=339 black=170, render blue=2516 green=0 → CONFIRMED palette delta, MINOR |
| peachbox: W should be green | orig peach eq has NO green (black=273 only) → REFUTED |
| solution: palette black/green/red + missing Y underline | orig solution box green=13347 black=1227 red=83; render green=60538 blue=6450 → render equation is green-on-green box vs orig black/green mix; underline: see above, CONFIRMED MINOR |

## Conclusion
No BLOCKER claim survives pixel adjudication. All equation content/structure matches (full leg item 8: none).
Residual confirmed deltas are MINOR color-coding/notation-cue items (green reg-term ink, final-Y underline),
which GROUND RULES classes (typed-vs-handwritten medium, mandated 2D format, JPEG softness) place at MINOR.

## pinkbox FAIL claims vs pixels (added after leg completed 22:10)
| claim | pixels |
|---|---|
| missing underlines on W's (MAJOR) | underline band y318-334 inside pink box x73-709: orig dark col runs 15/10/2/2 vs render 16/11/10/2 — SAME underline bars present in both → REFUTED |
| missing red pointer mark between "Best" and W (MINOR) | red px x150-320 y288-322: render=22434, orig=5113 — render has MORE red ink (red W + box border), the mark is part of the red-W annotation present in both → REFUTED as missing |
| eq ink blue vs black (MINOR/low) | pinkbox census: orig black=273, render blue=1645 — same equation-ink palette delta class as full leg, MINOR |
