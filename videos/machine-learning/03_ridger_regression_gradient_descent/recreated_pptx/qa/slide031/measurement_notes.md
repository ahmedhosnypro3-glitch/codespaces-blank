# Slide 031 — measurement record + adjudication (attempt 1, worker-kimi-031-r2)

Source frame: `unique_slides/slide_031.jpg` (960x540, 1px = 1pt = 1/72in).
Method: PIL + NumPy scans (non-white / colour-channel masks / connected components),
cross-checked against `analysis/slide_031_final.json`.

## Measured elements (frame px)

| Element | Measured | Data | Note |
|---|---|---|---|
| plot box | x 573..809, y 66..267 | — | RED `C00000` border (JPEG-darkened (117,50,57)), 1pt, white fill |
| x tick grid | 573 / 630 / 687 / 745 / 801 | x = -5 / 0 / 5 / 10 / 15 | 11.4 px/unit, x=0 at 630 |
| y tick grid | 87 / 146 / 206 / 265 | y = 15 / 10 / 5 / 0 | 11.87 px/unit, y=0 at 265 (= box bottom edge) |
| parabola | vertex frame (688, 253) | (5, 1) | f(x)=(x-5)^2+1, blue; arms reach frame y 70 at x 733 and 644 |
| black chord | frame y 143..150, x 650..725 | y = 10, x 1.75..8.33 | 3 short vertical ticks below it at frame x 653 / 691 / 733 (data x ≈ 2, 5.4, 9) |
| green blob | frame x 678..699, y 248..256 | ≈ (5, 1) | the (5,1) minimum marker |
| red dot | frame x 657..665, y 179..186 | ≈ (2.7, 6.9) | inside plot, above the chord |
| "(5,1)" label | frame x 526..558, y 249..261 | — | left of plot box, green |
| y tick labels | frame x 530..560 | — | above y=87 → "15", above y=265 → "0" (partial rows captured) |
| house chrome | panel x54..903 y45..540; C00000 left x58.5 / right x901 / bottom y538.5; **NO top stroke**; badge d35 at (876,73) FDFD96 ring 6A5ACD | | per deck AGENTS.md |

## Adjudication of spec-vs-frame (frame wins)

The analysis JSON said the graph had `x ~ 600-920, y ~ 50-250` with tick labels
"-5,0,5,10,15 on both x and y" and a "black horizontal segment from (3,9) to (7,9)".
The frame disproves part of that:
1. The plot box is **x 573..809, y 66..267** — not 600..920 / 50..250. The old
   geometry put the white plot rect on top of the badge (chrome check FAIL:
   badge center 21 render-px high, lower half covered).
2. The **y axis runs 0..15**, not -5..15. The four y grid lines are at frames
   87/146/206/265, i.e. 11.87 px/unit with y=0 at the box bottom (265). The old
   `yMax=15` squash put grid lines at 10 px/unit, which the frame disproves.
3. The black chord sits on the **y=10** grid line (frame 146), spanning data
   x ≈ 1.75..8.33 — NOT (3,9)-(7,9). It is drawn as data-y 10.
4. The chord's three ticks sit at data x ≈ 2, 5.4, 9 (frame 65/691/733), i.e.
   3px outside each end of the chord and one near the middle.
5. The plot border is **red C00000**, not black.

## Curve fidelity (second-difference ripple check)

f(x) = (x-5)^2 + 1 sampled densely over its visible span (data x 1.025..8.975):

| N | max abs 2nd difference | in frame px |
|---|---|---|
| 100 | 1.264e-02 | 0.150 |
| 200 | 3.160e-03 | 0.0375 |
| 400 | 7.900e-04 | 0.0094 |

The quadratic is analytic (exactly constant second derivative), so the ripple is
pure discretisation error and falls as 1/N^2. **N=200 gives < 0.04 frame-px
ripple** — invisible at 150 dpi (where 1 frame px ≈ 2.083 render px).

## Verdict history

*No banked judge transcripts exist for slide 031* (qa/slide031/ holds only
render_1.png; qa/slide_031/ holds an unrelated old dispatch brief).
This is the first judge attempt (K=1).
