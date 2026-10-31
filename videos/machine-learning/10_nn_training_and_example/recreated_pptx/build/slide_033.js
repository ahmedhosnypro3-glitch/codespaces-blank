// slide_033.js — "Initialized weights" / "Updated weights (after iteration # 10)" (badge 33)
// Two stacked red-bordered white panels, each a 2-3-2 feed-forward net with target block.
// Geometry measured from unique_slides/slide_033.jpg (960x540 px, PX=13.33/960 in/px).
// House chrome: gray bg, red frame 0.15in inset, yellow badge. No centered title (none in original).
const pptxgen = require("pptxgenjs");
const VID = "/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example";
const PX = 13.33 / 960;
const px = v => +(v * PX).toFixed(4);
const FONT = "Arial";
const BLACK = "000000", BLUE = "0000FF", RED = "C00000", GREEN = "008000";
const MAGENTA = "A000A0", YELLOW = "FFFF99", PEACH = "FBD08A", LBLUE = "9DC3E6";
const CREAM = "FFFDE7", GRAYCONN = "BFBFBF", NAVY = "000080";

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const W = 13.33, H = 7.5;
const s = pres.addSlide();
s.background = { color: "E8E8E8" };

// ========== HOUSE CHROME ==========
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: W - 0.3, h: H - 0.3,
  fill: { type: "none" }, line: { color: RED, width: 1.5 },
});
s.addShape(pres.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: "FFF9C4" }, line: { color: "FFF9C4", width: 0.5 },
});
s.addText("33", {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5, align: "center", valign: "middle",
  fontSize: 18, bold: true, color: "333333", fontFace: FONT, margin: 0,
});

// ========== HELPERS ==========
function txt(str, x, y, w, h, size, color, bold, align, italic) {
  s.addText(str, {
    x: px(x), y: px(y), w: px(w), h: px(h), align: align || "left",
    valign: "middle", fontSize: size, bold: !!bold, italic: !!italic,
    color, fontFace: FONT, margin: 0,
  });
}
function node(cx, cy, r, fill, stroke) {
  s.addShape(pres.shapes.OVAL, {
    x: px(cx - r), y: px(cy - r), w: px(2 * r), h: px(2 * r),
    fill: { color: fill }, line: { color: stroke, width: 1 },
  });
}
function conn(x1, y1, x2, y2, color) {
  s.addShape(pres.shapes.LINE, {
    x: px(x1), y: px(y1), w: px(x2 - x1), h: px(y2 - y1),
    line: { color, width: 0.75 },
  });
}
// near-straight bracket stroke: two segments with slight mid bulge, 3px ink width
function bracket(cx, yTop, yBot) {
  conn(cx + 2.5, yTop, cx - 0.5, (yTop + yBot) / 2, BLACK);
  conn(cx - 0.5, (yTop + yBot) / 2, cx + 2.5, yBot, BLACK);
}
function vrule(x, yTop, yBot) {
  conn(x, yTop, x, yBot, BLACK);
}
function wlab(cx, cy, t, color, size) {
  txt(t, cx - 20, cy - 7, 40, 14, size || 7, color, true, "center", true);
}
