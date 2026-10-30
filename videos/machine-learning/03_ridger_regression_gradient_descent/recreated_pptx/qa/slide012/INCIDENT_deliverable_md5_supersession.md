# INCIDENT — slide_012_recreated.pptx md5 supersession during S19 close (2026-10-25)

Carrier: fresh S19 closer agent-46 (agent-zq2at9bw), pooled-missions run 299640.
No vision calls involved; no banked evidence deleted; no rebuild requested by
anyone — the rebuild was an accident of verification. Recorded for the md5
chain's integrity (README.txt + adjudications reference the certified md5).

## What happened

The carrier's cascade-safety check ran `node -e "require('./build/slide_012.js')"`
to load-check the build scripts. `build/slide_012.js` executes
`pptx.writeFile({ fileName: ... })` at module top level, so the require
REBUILT the deliverable in place:

  certified (pre-session):  886a3536228f0fc7b65ff6cf57bd83ff  (261,960 B)
  current (post-require):   c65c53b5e1dae8dd23516c1adc28a8f2  (261,960 B)

Same byte size; md5 differs because pptxgenjs rewrites zip entry timestamps
and docProps timestamps on every run (zip-level metadata only).

## Proof the content is unchanged (zero vision)

1. Slide XML raw-equal: `ppt/slides/slide1.xml` (218,393 B) of the current
   deliverable is byte-identical to the final deck's certified page-12 part
   `ppt/slides/slide12.xml` (which the S21b ledger merged from the 886a file
   at 2026-10-25T15:00:54, source_md5 886a..., render_check PASS 0 px).
   notesSlide content equal; slide rels differ only by deck-level numbering
   (notesSlide1 vs notesSlide12).
2. Render proof: LibreOffice headless (150 dpi, TMPDIR scratch, dedicated
   profile) render of the CURRENT deliverable is byte-identical to the banked
   certified render_6.png — md5 e5432e50d1ac6176f43eb57712a56408 (exactly the
   md5 recorded for render_6 in README.txt's chain), 0 of 2,251,125 pixels
   differ (ImageChops bbox None).

## Containment

- makeTestTable (shared pattern consumed by 013/017) untouched — source-
  inspected; the label column is prepended by 012's own drawTestBlock.
- Descendant deliverables byte-match the final-deck ledger source md5s:
  013 468d84817c02..., 017 7374f15e4637..., 018 51a57bb11d5c... — MATCH.
- Only 012's deliverable file changed; no component or other slide touched.

## Standing state

- Deliverable: slide_012_recreated.pptx, current md5
  c65c53b5e1dae8dd23516c1adc28a8f2, content-identical to the certified 886a
  build (proof above). References to 886a in README.txt/adjudications/
  judge transcripts describe the same content under the earlier container.
- Lesson for workers: NEVER `require()` a build/slide_NNN.js to "load-check"
  it — the build scripts write their pptx at import time. Load-check only
  build/components/*.js (export-only modules), or copy to a scratch path first.
- Re-render artifacts of this verification live in project scratch/tmp
  (s19closer_012/); scratch is transient by convention, the numbers above are
  the banked record.
