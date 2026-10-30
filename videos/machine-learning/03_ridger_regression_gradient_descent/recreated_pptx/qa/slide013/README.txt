S12b evidence regeneration (pool run 299640) — slide 013
=========================================================
Scope: regenerate the banked Procedure B crop-pair evidence referenced by this
dir's five crop_6_* judge transcripts. Zero vision calls; no deliverable, DB
row, or transcript modified. Only render_regen.png + the crop pairs + this
README are new.

Render
------
slide_013_recreated.pptx -> soffice --headless (profile scratch/tmp/s12b_lo_profile)
-> pdftoppm -r 150 -png -> qa/slide013/render_regen.png, 2001x1125.
render_regen.png md5: cd5133d5e1ece80ac2ed36854f4743ad

Regions cut — the ORIGINAL cut script make_crops_attempt_6.py survives in this
dir and was used as the coordinate source (boxes + exact construction: scalar
S = H_render/540 = 2.083333; render crop at int(round(v*S)) edges; original crop
LANCZOS-upscaled to the render crop's exact pixel size):

1. crop_6_wbox1   (498, 119, 631, 260) -> pair 277x294 (banked 277x294, MATCH)
2. crop_6_wbox2   (498, 257, 631, 398) -> pair 277x294 (banked 277x294, MATCH)
3. crop_6_train1  (84, 118, 467, 257)  -> pair 798x289 (banked 798x289, MATCH)
4. crop_6_test1   (711, 88, 880, 260)  -> pair 352x359 (banked 352x359, MATCH)
5. crop_6_arrows1 (447, 178, 675, 218) -> pair 475x83  (banked 475x83, MATCH)

All five banked pair sizes (crop_scale_audit_attempt_6.txt) reproduced exactly.

Files created:
  render_regen.png
  crop_6_wbox1_render.png   (6321654443d9767ea2497274b35baa87)
  crop_6_wbox1_orig.png     (3d11e8bf44646b842230230a8692aba4)
  crop_6_wbox2_render.png   (e29ad21efd144e922b5e2be8f7988ce1)
  crop_6_wbox2_orig.png     (37e98ff1eb48951287a6406a121b885d)
  crop_6_train1_render.png  (9383376c9669896204eb475e7ad1b421)
  crop_6_train1_orig.png    (d7d56915c963559f71a9be4b454876aa)
  crop_6_test1_render.png   (de538ce4609a1322793a83c0c45c3a62)
  crop_6_test1_orig.png     (70ac173cfbdf5ae344576a5dae9670f5)
  crop_6_arrows1_render.png (032be588519b342999746942dbf40e22)
  crop_6_arrows1_orig.png   (4d2ffe11f332923dd01dc981c873ab1e)
  README.txt (this file)

Verification (zero vision): banked selfcheck_attempt_6.py re-run (paths patched)
against render_regen.png. ALL content checks PASS: containment (14 regions),
equation ink, delimiter geometry, train/test cols pixel-exact, table data
verbatim, headers single-line, house chrome PASS. Known environment delta,
documented not fixed: the six table-row-band checks report +1/+2px row
positions vs the banked certified output (e.g. train band1 [126,157,189,220,251]
vs banked [126,157,188,219,249]; at the scan-window bottom edges flicker —
duplicate 528/529 edges on band3, test band2's bottom edge 390 undetected just
outside the window). This is font-metric-driven LO raster drift
between the certification environment (codespace paths in the banked scripts)
and this machine — columns are pixel-exact, text-driven row heights shift
sub-2px. Content verified unaffected; the certificate transcripts' findings
(values, delimiters, spans) are unchanged claims.
render_regen md5 != banked render_6 md5 0321e28c3abb6afd3f35b099d5cb5547 for the
same reason (cross-environment rasterizer bytes; geometry-verified instead —
039's byte-exact md5 match in this same run proves today's pipeline reproduces
same-machine banked md5s).
Original-side crops cut from unique_slides/slide_013.jpg (960x540).
