# Slide 025 fresh-leg pair FINAL adjudication (2026-10-31 ~07:25 UTC)

Both fresh transcripts have now landed clean (zero 429):
- `judge_full_fresh.txt` 04:33:05Z FINAL VERDICT: FAIL (judged k14 render bytes, 03:37).
- `crop_dense_judge_fresh.txt` 07:22Z FINAL VERDICT: FAIL (judged current crop pair;
  crop_dense_render.png 06:21, derived from promoted render.png md5 2ab860b7...).

Censuses vs the NEW render (render.png 2ab860b7, mtime 06:21) banked:
`adjudicate_freshfinal_full_20261031_0725.txt` (19.375% frame diff, orig-heavy 122234 vs
85407, densest cells uniform edge bands) and `adjudicate_freshfinal_crop_20261031_0725.txt`
(30.025% crop diff, orig-heavy 19716 vs 17755, densest 24px cells 288px spread across
label bands — same diffuse class as the dismissed 02:45 att5 census).

Fresh FULL FAIL (k14 bytes) claim-by-claim: see `adjudication_fresh_20261031.md` — claims
1/2/4/5/6 pixel-refuted or generated-graph MINOR; claim 3 (BL label swap) not
pixel-confirmed by profile NCC (same-pos 0.489 vs crossed -0.273) but k15 swapped labels
per the fix worker's glyph-template probe; superseded by later builds anyway.

Fresh CROP FAIL (current k15b-promoted bytes) claims vs pixels (`probe_fresh025_k15claims.out`
on render.png 2ab860b7):
1. BLOCKER "3D bowl flattened, z-stack absent" — z-axis substance PARTIALLY SUPPORTED:
   TR z-tick strip ink render=136 vs orig=470; x10^4 corner render=1 vs orig=83 (effectively
   absent). NOT refuted.
2. MAJOR left-axis tick order reversed — not pixel-refuted (build uses invert_xaxis; judge
   reads opposite at crop scale). Stands registered.
3. MAJOR z labels 1.5/1/0.5/0 missing/collapsed — SUPPORTED (same strips as #1).
4. MAJOR extra detached diagonal + upper red line geometry — SUPPORTED per the fix worker's
   banked probe (register ~06:55 entry: render carries long shallow stroke A at 7.5% where
   orig has 0%; orig steep diagonal missing in render).
5. MINOR fill emphasis — MINOR class.

Disposition: FAIL branch executed per dispatch — rejudge_adjudicate.py 025 [--crop] run vs
the NEW render and banked; MAJORs are NOT all pixel-refuted (crop claims 1/3/4 have pixel
support), so slide 025 is NOT certified by this worker. No DB write (row 25 stays
building/''), no final_deck_tool.py update, no render_check_pages.py run, no result.txt
rewrite, no register certification entry. Fix loop (k16/k17 legs + watch_k15.sh/watch_k17)
owns the next iteration. No git; no evidence deleted.
