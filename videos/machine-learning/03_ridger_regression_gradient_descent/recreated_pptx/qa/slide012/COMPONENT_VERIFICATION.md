# Slide 012 — producer/component verification record (2026-10-24, in-session)

This records the non-vision verification done while the full-slide judge was in
flight. It is a companion to `worker_report.md`.

## Component refresh — DONE, proven

`recreated_pptx/build/components/slide_012.js` was rewritten from the certified
`build/slide_012.js` in the house idiom (`renderBase` + `BLOCKS` + per-block draw
fns + skip/only/numeral hooks), matching the `slide_009.js` reference pattern.

Three defects were found and fixed in the first rewrite (all caught before any
vision call, by direct pptx-XML comparison):

1. **`makeTestTable` dropped cell text** — it returned bare `options` objects
   with no `text` key, so the test table rendered 12 EMPTY cells. Confirmed by
   XML diff: probe's test graphicFrame had `texts=[]` vs the deliverable's
   `['Test1','Test2','Test3','30',...]`.
2. **cell inset mismatch** — the component set `margin: 0` while the certified
   deliverable leaves pptxgenjs defaults (`marL/R=91440`, `marT/B=45720` EMU on
   all 120 cells). Removed `margin` so the two agree byte-for-byte.
3. **test-table column index off-by-one** — the component passed `ci` where the
   build passes `ci + 1` (the test table has no label column, so its data columns
   are 1-based). This had silently swapped the RED/BLUE ink alternation
   (probe: `Test1=BLUE, Test2=BLUE, Test3=RED`; deliverable: `Test1=BLUE,
   Test2=RED, Test3=BLUE`) and wrongly bolded the body-row first column.

After the fixes, `ppt/slides/slide1.xml` is **IDENTICAL** between
`slide_012_recreated.pptx` and the component build (modulo shape `id`/`name`
attributes, which carry no geometry).

## Component fidelity proof — PASS

`python3 component_fidelity.py` (re-run after the fixes):

```
== 2. pixel diff (identical command, identical raster path) ==
same geometry: True
pixels differing        : 0 of 921600
pixels differing >8     : 0
max channel delta       : 0
PIXEL-IDENTICAL: True

== 3. container member diff ==
members 39 / 39, same names: True
  differs: docProps/core.xml
container diff limited to metadata + shape ORDER: True

== 4. shape geometry multiset ==
cert   sp=24 pic=0
probe  sp=24 pic=0
same xfrm multiset (same shapes, same boxes): True
  cert xfrms=24 probe xfrms=24

== 5. skip / only / numeral hooks ==
  (full, default)            sp=24 pic=0 gf=4  OK
  only:{chrome}              sp= 6 pic=0 gf=0  OK
  skip:{title,labels}        sp=14 pic=0 gf=4  OK
  only:{chrome,trainTable}   sp= 6 pic=0 gf=1  OK
  only:{testBlock}           sp= 2 pic=0 gf=1  OK
  numeral override 42        sp=24 pic=0 gf=4  OK

COMPONENT FIDELITY: PASS
```

The first fidelity run reported FAIL on two hook checks. Cause was **stale
expectations in the checker, not a fidelity failure**: the hardcoded
`(23, 0, 4)` for the full base came from the attempt-1 deliverable; the
certified deliverable (rebuilt 23:54) draws 24 `<p:sp>` because the `labels`
block now emits 9 shapes (two-line "Perfect Data / Y follows x1" = 1 rect + 2
text runs, vs 1+1 for the single-line labels). The certified deliverable itself
measures (24, 0, 4), and the isolated per-block builds sum to exactly
(24, 0, 4). Expectations updated to (24, 0, 4).

Also confirmed: `X5 is Outlier` appears exactly **twice** in the deliverable and
exactly twice in the component build — the MAJOR label defect is closed in both.

## Deliverable status

- `recreated_pptx/slide_012_recreated.pptx` — 255,811 bytes, unchanged since the
  23:53 rebuild; contains the X5 label fix, the column ink alternation, white
  cell fills, the pale-yellow test-table y row, and the 3-column test table.
- `qa/slide012/render_2.png` — 2001x1125 RGBA, 150dpi render of that pptx.
- `qa/slide012/crop_3_*_orig.png` / `crop_3_*_render.png` — 4 crop pairs re-cut
  from `render_2.png` at matched effective scale (perfect / outlier1 / outlier2 /
  test table). Re-cut for the record; per the parent's directive the banked crop
  PASS (`crop_2_perfect_table_judge.txt`) is not re-judged.

## Vision leg status

The full-slide Template A judge was dispatched detached against
`render_2.png` + `unique_slides/slide_012.jpg` with the verified byte-for-byte
`-p` payload. It hit two internal 630s HangError aborts (gateway saturation:
~22 concurrent callers vs ~16 slots) and was then killed externally — the log
ends without an attempt-3 line and without the wrapper's `EXIT=` marker, and
`judge_attempt_3.txt` was never written. No verdict exists for attempt 3; nothing
may be inferred from the dead process.
