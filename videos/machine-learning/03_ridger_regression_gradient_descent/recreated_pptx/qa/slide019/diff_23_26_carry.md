# diff_23_26_carry.md — crop_23 certificate carry proof (S4b fresh carrier, 2026-10-26)

PIL pixel diff `render_23.png` vs `render_26.png` (both 2001x1125, 150dpi), per
region, measured with `numpy.abs(...).max(axis=2)` (int16), scale (2.08438, 2.08333):

| region (frame px) | diff px tol=0 | diff px tol=8 | verdict |
|---|---|---|---|
| table_right x400..904 y157..530 | **0** | 0 | byte-identical |
| noreg_rows x124..380 y199..485 | **0** | 0 | byte-identical |
| table_left x58..480 y157..360 | 9157 | 9157 | CHANGED (outlierArcs fix zone — must re-judge) |
| header_strip x58..60..904 y60..200 | 1540 | 1540 | CHANGED (arc tips reach y~180..193 in outlier header zone — re-judge) |
| full frame | — | 17399 (0.7729%) | consistent with the outlier-column-only fix |

Changed-ink bbox in table_left (region-rel): x16..123, y48..422 = frame x~66..117,
y~180..360 — exactly the outlier column arcs/boxes; in header_strip: x22..122,
y250..277 region-rel = frame x~68..117, y~180..193.

## Carry decisions

- **noreg_rows: crop_23 PASS CARRIES** (`crop_23_noreg_rows_judge.txt`,
  FINAL VERDICT: PASS) — region byte-identical on render_26. Protocol law: "a crop
  transcript is kept only if its region is pixel-identical across the rebuild,
  proven with a diff" — this file is that proof.
- **table_right: NO CERT EXISTS** (crop_23_table_right_judge.txt never created;
  crop_19's FAIL is from older build bytes) — judged FRESH on render_26
  (crop_26_table_right pair from cut_crops_26.py).
- **table_left + header_strip: judged FRESH** on render_26 per task #86 (regions
  changed; crop_23_table_left FAILed on the two MAJORs attempt 26 fixed).
