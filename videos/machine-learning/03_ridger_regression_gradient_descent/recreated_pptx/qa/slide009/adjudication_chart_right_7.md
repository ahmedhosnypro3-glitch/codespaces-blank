# Adjudication — crop_6_chart_right judge leg (attempt 7)

- transcript: qa/slide009/crop_6_chart_right_judge.txt (2181 B, gateway leg,
  `[winner] images (round 1, attempt 1)`, banked as-is)
- transcript verdict line: `FINAL VERDICT: FAIL`
- adjudication: FAIL not sustained — its single finding is DISMISSED by
  pixel measurement; zero surviving discrepancies ⇒ region reads PASS.

## The finding, and the refutation

Finding (MAJOR, high confidence): "dashed residual connector lines from
scatter points to the blue fitted line … entirely absent" in IMG1.

Refutation (PIL, render_7.png md5 84fc8bfc4d403edf248fb442ede3313a vs
unique_slides/slide_009.jpg, periwinkle-family mask
B−R∈[8,120], R−G∈[−5,6], B≥170):

1. The build draws them (slide_009.js:244-253 — one per point, point centre
   to perpendicular foot on the fitted line, CONN B4B2D2, 0.75pt, dash;
   corridors <9 px skipped).
2. Region count x478..878 y102..480 (frame px): render_7 834 px — connectors
   present; the judge's "entirely absent" is false.
3. Like-for-like corridor ink (6 drawn connectors of the RIGHT chart, boxes
   ±2.5 px in frame space, render boxes scaled ×2.0844):

   | corridor (point→foot) | original px | render_7 px |
   |---|---|---|
   | (656,327)→(660.7,336.7)   | 17 | 31 |
   | (707.5,333.5)→(694.1,320.8) | 54 | 48 |
   | (737.5,290)→(741.4,298.2) | 18 | 26 |
   | (741.5,332)→(728.8,304.2) | 56 | 75 |
   | (794,302)→(781.9,278.9)   | 75 | 67 |
   | (810,249)→(813.1,264.1)   | 30 | 39 |
   | **total**                 | **250** | **286** |

   Every corridor carries dash ink in both images; the render's crisper
   dashes carry slightly more ink than the original's faded JPEG dashes.
4. The original's much larger raw family count (6417 px) is JPEG halo:
   it tiles into navy-border anti-aliasing stripes (vertical x840..880
   ≈160 px/40px-band from y120..440; horizontal y80..120 and y440..480
   across x480..840) — chart furniture halos, not connector ink
   (ground rule (e)).

The judge's own body confirms every other clause clean (spec check ✓ per
founder directive; glyph/value audit ✓). With the single finding dismissed,
no discrepancy survives.

- leg label: single-read (gateway), finding adjudicated PIL-first per the
  deck judging law (probe71/72c precedent).
- chart_left note: the paired LEFT-chart leg degenerated 3× in the same
  gateway window (HangError@630s + 2× EmptyStreamError, no transcript) —
  solo retry dispatched; if it degenerates again, the leg moves to the
  harness reader lane (attempt-5/6 precedent) once agent-3 frees it.
