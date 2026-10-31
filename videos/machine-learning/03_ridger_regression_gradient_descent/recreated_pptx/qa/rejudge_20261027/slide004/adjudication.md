# Slide 004 rejudge — adjudication record (rejudge_20261027)

Scope: the missing CROP (Template B, zoomed crop-pair) leg on the POST-fix bytes. FULL=PASS was
already banked (`judge_full.txt`, 2026-10-30 23:01, v2). Render verified post-fix before dispatch:
`render.png` 2001x1125 (scale 2.0844) carries exactly 272 strict-blue px (b>=110, b>=r+50,
b>=g+50) at slide x97-122 y327-339 with core median [0,0,139] = 00008B (the Ŷ≠Y token fix), and
nothing else blue in the error-box interior (wide box x80-484 y308-363 total = 272);
`house_chrome_check.py render.png 4` = PASS rc=0 (re-run 2026-10-31 on the current bytes).
Dense region 60,232-344,440 matches result.txt; crop pair re-cut 2026-10-30 22:40
(crop_dense_render.png 592x434, crop_dense_orig.png same size, LANCZOS upscale of the frame region).

## Crop leg run

- Payload: `payload_B_004.txt` = `sed 's/slide NNN/slide 004/g' payload_B.tmpl` (0 placeholders left).
- Dispatch: `vision_leg.sh slide004/crop_dense_judge.txt 600 crop_dense_render.png
  crop_dense_orig.png "Slide 004 zoomed crop — fidelity check vs original" "IMG1=zoomed crop of
  150dpi render; IMG2=matched-scale crop of original frame" payload_B_004.txt`.
- Result: attempt 1 upstream HTTP 429 (transcript preserved); attempt 2 clean, winner `images`
  round 1 attempt 1, transcript `crop_dense_judge.txt` (2026-10-31 00:23), **FINAL VERDICT: FAIL**.

## Judge claims vs PIL-first adjudication (`rejudge_adjudicate.py 004 --crop` + targeted scans)

`rejudge_adjudicate.py 004 --crop`: diff px 48706 (18.957% of crop); densest diff cells all in the
bottom text band (slide y472-495) — typed-vs-handwritten AA; ink only in render 10090 px vs only in
original 29407 px (handwritten stroke mass, not missing content).

1. **BLOCKER/high — "missing underline under RHS Y in 'Objective is Ŷ=Y' and under Y in
   'If Ŷ≠Y'" — REFUTED.**
   - Objective box (slide x78-302 y242-301), original frame 1:1: text ink rows slide y263-285
     (descenders end y286, bottom border y299); scanning every row below the text line to the box
     bottom finds NO dark run >=8 slide-px anywhere in the box. The only sub-line marks are at
     y284 (x220-233 and x254-267, <=14 px) — inside the descender zone, i.e. handwritten glyph
     feet. The banked att8 adjudication (`qa/slide004/worker_report.md`) already refuted the
     inherited "x254 w17 y283" bar: "no isolated bar anywhere under the phrase"; real underlines
     in this deck are separate strokes >=15 px wide below the descender zone (where-block Ŷ
     x508-526, W x566-584 at y277-283, text ending ~y274). Render side: zero ink below the
     objective text line (slide y276-290 all empty). => No underline exists under Ŷ=Y in the
     original; nothing to reproduce.
   - Error box (slide x78-486 y306-365): original 00008B token Ŷ≠Y at slide x136-181 y327-342;
     crop map and 1:1 frame show rows below the token (slide y344-352) EMPTY; box-interior
     below-line scan: no run >=8 px. Render token at slide x97-122 y327-339 (post-fix 272 px,
     core [0,0,139]); rows below empty in render crop too. The horizontal runs mid-line
     (slide y333.6 and y337.6) are the ≠ sign's two bars, not an underline. => REFUTED.
2. MINOR/high — thinner recreation stroke weight: ground rule (c) typed-vs-handwritten, inherent
   medium difference. Advisory.
3. MINOR/medium — small color/contrast differences: advisory.
4. MINOR/medium — horizontal advance/placement differs at the right edge: font metrics; the
   words themselves match. Advisory.

## Disposition

CROP-leg FAIL **DISMISSED** (BLOCKER refuted by pixels; only MINOR/advisory items remain).
`result.txt`: CROP=NORESULT -> PASS. Slide 004 rejudge complete: FULL=PASS + CROP=PASS on the
post-fix bytes. Slide stays certified; DB and deck not touched; no git; no evidence deleted.
