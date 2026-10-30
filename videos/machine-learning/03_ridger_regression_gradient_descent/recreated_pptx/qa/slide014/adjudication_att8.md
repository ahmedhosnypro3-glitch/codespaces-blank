# Slide 014 — attempt-8 adjudication record

Worker: s26-1415-worker-1793022298 (pool scope S26_014_015, run 299640).
Attempt 8 is the orchestrator-authorized certification roll for the parked
attempt-7 slide (wave brief S26: "att8 cycle: rebuild → render_8 → chrome check →
Template A judge + owed zoomed crops → adjudicate → certify").

## Carry-over from attempt 7 (settled — NOT re-litigated)

`adjudicate_attempt_7.md` (banked) disposed of every att7 claim with measurements:

| # | att7 claim | Disposition (settled) |
|---|---|---|
| 1 | Right-box text collision "Predicted Labels" × "from Model" | REFUTED (doc-parse: two clean lines) |
| 2 | Missing X in "from Model Ŷ = X̲W̲" | REAL → FIXED (bold underlined X restored) |
| 3 | Left box 3-line wrap | REAL → FIXED (labels 18→14pt per measured glyph height) |
| 4 | Delimiter geometry/style + ŷₙ proximity | style-level, medium conf — recorded, not an error |
| 5 | Missing wide inter-phrase gaps in band 1 | MINOR accepted |
| 6 | Missing underlines on bold Ŷ/Y in Define-Loss | REAL → FIXED (underline:true) |
| 7 | λW spacing in final equation PNG | MINOR accepted (mathtext standard) |
| — | ⋮ vs … row-3 ellipsis | MINOR accepted (entry-form variance) |

## Attempt-8 build currency (measured, not assumed)

- `build/slide_014.js` unchanged since the att7 fixes (mtime Oct 25 07:08; the
  three fixes verified present in source: 14pt label runs, bold underlined X at
  line 96, underlined Ŷ/Y at lines 151/153).
- PPTX rebuilt from that script 2026-10-26 → fresh render `render_8.png`
  (2001×1125 @150dpi, md5 496917e3f9021024573088c958eaca84).
- render_8 vs banked render_7c (md5 8f36444418649096095e3d438c3066f2): 14,385 of
  2,251,125 pixels differ at luma>8 (0.64%), confined to a 1px sub-pixel
  rasterization shift of the left/right red strokes (right stroke x1877-78 →
  x1876-77; left x120-123 shifted likewise) plus badge AA. Zero glyph/content
  pixels differ. Content-identical to the render that carries the verified att7
  fixes (render_7c doc-parse: left box 2 lines, right box "Ŷ = X W").

## House chrome (render_8)

`HOUSE CHROME CHECK: PASS (panel x 112-1882, y 94-bottom; strokes L/R/bottom
present, top bare; badge center (1824,152) d=68; all within tol 8)`

## Owed Procedure B crops (cut fresh from render_8, create_crops_8.py)

| region | frame bbox | out px | eff. scale |
|---|---|---|---|
| vectors | x48..910, y50..240 | 1797×396 | 2.0847/2.0842 |
| bands | x48..910, y242..347 | 1797×219 | 2.0847/2.0857 |
| final | x48..910, y462..532 | 1797×145 | 2.0847/2.0714 |

These are the three dense regions staged at att7 (payload_B_7_* banked,
byte-verified = frozen Template B, md5 978be75de7b83501d09f8f0c5576cbee) but
never dispatched. Dispatchers written fresh: `dispatch_judge_8.sh` (Template A)
and `dispatch_8_crop.sh <vectors|bands|final>` (Template B).

## Attempt-8 judge findings (filled when judge_attempt_8.txt lands)

PENDING
