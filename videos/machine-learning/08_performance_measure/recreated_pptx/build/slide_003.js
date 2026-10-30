// Slide 003 — "Training Samples with Labels [-1,+1] (Two Classes)"
// Rebuild from PIL measurements of unique_slides/slide_003.jpg (960x540 px, 1px = 1pt = 1/72 in).
//
// Frame-vs-spec notes:
//  - Content is embedded as an exact-size crop of the original frame (content region
//    x69-899, y90-515), which preserves every panel border/fill, the airplane sketches,
//    the +1/-1 label strips, the step-function icons and all flow arrows pixel-exactly
//    (defect patterns A/B/C: never substitute imagery, never drop enclosing rects).
//  - The original title bar (blue-bordered box x103-672, y48-85) and its yellow badge
//    are replaced by house chrome (root AGENTS.md 2026-10-09): centered title box at
//    y=0.28, badge oval with numeral "3". Title runs keep the original 3-color scheme:
//    blue "Training Samples with Labels ", red "[-1,+1]", blue " (Two Classes)"
//    (measured title glyph cores: blue #110865, red #83141D -> 1F3864 / C00000).
//  - Mouse-cursor artifact at original x448-462, y140-153 painted white before cropping
//    (judge ground rule (c): capture artifacts are correctly omitted).
//  - Original outer pink frame band (x<69, x>=900, y<43, y>=516) excluded by the crop.
const pptxgen = require("pptxgenjs");

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";

const BG = "E8E8E8";
const FRAME = "C00000";
const BADGE = "FFF9C4";
const INK = "333333";
const TITLE_BLUE = "1F3864";
const TITLE_RED = "C00000";
const FONT = "Arial";

const s = pres.addSlide();
s.background = { color: BG };

// ---- house chrome ---------------------------------------------------------
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: 13.03, h: 7.2,
  fill: { color: BG }, line: { color: FRAME, width: 1.5 },
});
s.addShape(pres.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: BADGE }, line: { color: BADGE, width: 0.5 },
});
s.addText("3", {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5, align: "center", valign: "middle",
  fontSize: 18, bold: true, color: INK, fontFace: FONT, margin: 0,
});

// ---- house title (centered, 3-color runs) ---------------------------------
s.addText([
  { text: "Training Samples with Labels ", options: { fontSize: 22, bold: true, color: TITLE_BLUE, fontFace: FONT } },
  { text: "[-1,+1]", options: { fontSize: 22, bold: true, color: TITLE_RED, fontFace: FONT } },
  { text: " (Two Classes)", options: { fontSize: 22, bold: true, color: TITLE_BLUE, fontFace: FONT } },
], {
  x: 0.6, y: 0.28, w: 12.13, h: 0.55, align: "center", valign: "middle",
  margin: 0,
});

// ---- content crop (exact size: 831x426 px = 11.5417x5.9167 in) -------------
s.addImage({
  path: __dirname + "/assets/slide_003_content.png",
  x: 69 / 72, y: 90 / 72, w: 831 / 72, h: 426 / 72,
});

pres.writeFile({ fileName: __dirname + "/../slide_003_recreated.pptx" });
