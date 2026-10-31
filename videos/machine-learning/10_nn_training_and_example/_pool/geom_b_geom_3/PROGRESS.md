# Lane G / scope `b_geom_3` — progress

Slides 014, 016, 017, 023, 024 in
`videos/machine-learning/10_nn_training_and_example`.

## DONE

- Scope claimed in `_pool/mission.db` (`worker_b_geom_3`, 2026-10-31 04:04:03).
- All 5 canonical deliverables rendered with LO headless, private profile
  `_pool/lo_geom_b_geom_3/`, `TMPDIR` inside the namespace, `pdftoppm -png -r 150`.
  Renders: `_pool/lo_geom_b_geom_3/out/slide_{014,016,017,023,024}_150.png`.
  All 2001x1125 (spec 2000x1125 +/-8 PASS), non-blank means 224.1..229.5 (spec 20..245 PASS).
- Measurement + report generator: `_pool/geom_b_geom_3/measure_v2.py` (masks,
  dark-ink basis, region windows, house-frame containment) and
  `_pool/geom_b_geom_3/report_gen2.py` (writes the reports).
- Reports written:
  - `qa/slide014/geom_b_geom_3.md`
  - `qa/slide016/geom_b_geom_3.md`
  - `qa/slide017/geom_b_geom_3.md`
  - `qa/slide023/geom_b_geom_3.md`
  - `qa/slide024/geom_b_geom_3.md`

## Results

| slide | TITLE | BODY | FOOTER | frame containment |
|---|---|---|---|---|
| 014 | EXCEEDS 248.72 | EXCEEDS 25.34 | NOT MEASURABLE | PASS 0 px |
| 016 | PASS 1.67 | EXCEEDS 15.75 | EXCEEDS 3.91 | PASS 0 px |
| 017 | EXCEEDS 119.52 | EXCEEDS 31.59 | EXCEEDS 57.49 | PASS 0 px |
| 023 | EXCEEDS 177.27 | EXCEEDS 180.51 | EXCEEDS 80.74 | **EXCEEDS 882 px** |
| 024 | EXCEEDS 30.40 | PASS 0.56 | PASS 0.56 | PASS 0 px |

## Method notes (settled — do not reopen)

1. **Basis = dark ink** (luminance < 150). Generic "non-background" bboxes are
   unusable: the originals carry multi-tone canvas fills, the render is flat `#E8E8E8`.
2. **Raw frame-px normalization** (render px * 960/2001, * 540/1125). A slide-rect
   normalization was tried and rejected: it is off by 282 px on 016 TITLE, whereas raw
   normalization matches 016 TITLE to 1.67 px.
3. **Chrome masked per slide**, measured not assumed:
   - render: 1px white PDF page border, house red frame (x=22..1978, y=22..1103),
     house badge disc.
   - original 014/016/017: own ring x=58/901 y=43/516, own badge, black capture bar y>=516.
   - original 023/024: own outer ring x=38/920 y=43/539; **023 also has an inner
     decorative ring** x=61/62, 862/863, y=58/523 — masking it removes a false
     ~250 px offset from every 023 band.
4. **Region comparison is box-to-box**, both sides clipped to the identical frame-px
   window. Pairing original bands to render bands by y-overlap across the two
   different pixel scales is WRONG (produced a false 351 px delta) — discarded.
5. **Regions** = the original's own chrome-masked dark-ink row bands grouped into
   TITLE / BODY / FOOTER at the two largest inter-band gaps.

## REMAINING

- Nothing outstanding. Scope closed with `scope-done`.
