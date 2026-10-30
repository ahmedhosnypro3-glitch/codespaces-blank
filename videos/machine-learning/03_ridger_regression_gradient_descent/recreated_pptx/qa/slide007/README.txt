S12b evidence regeneration (pool run 299640) — slide 007
=========================================================
Scope: regenerate the banked Procedure B crop-pair evidence referenced by this
dir's judge transcripts. Zero vision calls; no deliverable, DB row, or
transcript modified. Only render_regen.png + the crop pairs + this README are new.

Render
------
slide_007_recreated.pptx -> soffice --headless (profile scratch/tmp/s12b_lo_profile)
-> pdftoppm -r 150 -png -> qa/slide007/render_regen.png, 2001x1125.
render_regen.png md5: 2f5d80ddb765fb66f32470cbcd6db307

Regions cut — COORDINATES DERIVED (this is the one slide in the scope with no
banked crop boxes anywhere: crop_prompt_1_*.txt hold only the frozen judge
payload, selfcheck_attempt_1.py has no crop section, no scale audit or make_crops
script exists in the dir). Boxes were derived from the transcripts' own region
descriptions plus the selfcheck's banked ink anchors, per Procedure B step 1
(dense region + ~8px padding). No guess-box: every edge is pinned to a banked
constant. Construction: render crop at (round(x0*2001/960), round(y0*1125/540))..
(round(x1*..), round(y1*..)); original crop LANCZOS-upscaled to the render crop's
exact pixel size — matched effective scale by construction.

1. crop_1_title (54, 0, 903, 126) -> pair 1769x262
   derivation: transcript crop_1_title_judge.txt describes "top band from the
   very top edge down to the blue content-frame top edge near the bottom of both
   crops; title centered ...; yellow badge at top-right (~x 0.92-1.00)".
   Banked constants: blue content box outer top y120 (selfcheckAttempt1 header),
   badge left edge ~858 -> (858-54)/849 = 0.947 inside the stated 0.92-1.00 band.
   Panel x54..903 (house chrome), top edge y0, blue-box top y120 + 6px.
2. crop_1_body (84, 146, 866, 438) -> pair 1630x609
   derivation: transcript crop_1_body_judge.txt covers intro + underlined header
   + the four arrow bullets. Banked ink anchors (selfcheck header): intro y154
   x90..807; header y202 (underline y220-221); bullets y249/294/348/397, bullet4
   x92..858; "nothing below y~430 in the box". Box = ink extents + ~8px padding
   (146 = 154-8; 438 = last-ink bottom ~426 + 12; 84/866 = 92/858 +-8).

No banked pair sizes exist for this slide, so no size match was assertable; both
pairs are at matched effective scale by construction (2.0836/2.0794 and
2.0844/2.0856 px per frame px).

Files created:
  render_regen.png
  crop_1_title_render.png (0fd1e30c11d1816a3996ede49fd1092f)
  crop_1_title_orig.png   (c3079d4d4e12caeb2d48a9db6a66a7c4)
  crop_1_body_render.png  (9544030dd67877e21ad94002177be0bd)
  crop_1_body_orig.png    (b1347663026bbcb16c94aefc8b7ef455)
  README.txt (this file)

Verification (zero vision): banked selfcheck_attempt_1.py re-run (paths patched)
against render_regen.png -> SELFCHECK PASS (body ink strictly inside the blue
box, ink presence in all bands, bullet arrowheads at banked positions, no ink
below y430). Original-side crops cut from unique_slides/slide_007.jpg (960x540).
