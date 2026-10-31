// slide_033.js — "Initialized weights" vs "Updated weights (after iteration # 10)" (badge 33)
// Two stacked red-bordered panels, each with the same 2-3-2 network + target matrix.
// Build: NODE_PATH=$(npm root -g) node recreated_pptx/build/slide_033.js  (from video dir)
// Geometry measured from unique_slides/slide_033.jpg (960x540 px, PX=13.33/960 in/px).
// House chrome fixed: red frame, yellow badge. No centered title (original has none).

const pptxgen = require("pptxgenjs");
const FONT = "Arial";
const NUM = 33;
const PX = 13.33 / 960;
const px = v => +(v * PX).toFixed(4);

const BG = "E8E8E8", RED = "C00000", BLACK = "000000", BLUE = "0000FF";
const PALE_YELLOW = "FFF9C4", PEACH_F = "FCE2C7", PEACH_S = "FF7A5C";
const GRAYLINE = "C9CFC9", GREEN = "008000", DARKRED = "C00000";
const CREAM = "FFFEEA";

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const W = 13.33, H = 7.5;
const s = pres.addSlide();
s.background = { color: BG };

// ========== HOUSE CHROME ==========
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: W - 0.3, h: H - 0.3,
  fill: { type: "none" }, line: { color: RED, width: 1.5 },
});
s.addShape(pres.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: "FFF9C4" }, line: { color: "FFF9C4", width: 0.5 },
});
s.addText(String(NUM), {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5, align: "center", valign: "middle",
  fontSize: 18, bold: true, color: "333333", fontFace: FONT, margin: 0,
});

// ========== HELPERS (all coords in source px) ==========
function node(cx, cy, r, fill, stroke) {
  s.addShape(pres.shapes.OVAL, {
    x: px(cx - r), y: px(cy - r), w: px(2 * r), h: px(2 * r),
    fill: { color: fill }, line: { color: stroke, width: 1 },
  });
}
function ctext(cx, cy, r, t, color, size) {
  s.addText(t, {
    x: px(cx - r), y: px(cy - r), w: px(2 * r), h: px(2 * r),
    align: "center", valign: "middle", fontSize: size || 10, bold: true,
    color: color || BLACK, fontFace: FONT, margin: 0,
  });
}
function lab(cx, cy, t, color, size, wPx, bold, italic) {
  s.addText(t, {
    x: px(cx - (wPx || 40) / 2), y: px(cy - 8), w: px(wPx || 40), h: px(16),
    align: "center", valign: "middle", fontSize: size || 10,
    bold: bold === undefined ? true : bold, italic: !!italic,
    color: color, fontFace: FONT, margin: 0,
  });
}
function conn(x1, y1, x2, y2, color) {
  s.addShape(pres.shapes.LINE, {
    x: px(x1), y: px(y1), w: px(x2 - x1), h: px(y2 - y1),
    line: { color, width: 0.75 },
  });
}
function hair(cx1, cy1, cx2, cy2) {
  conn(cx1, cy1, cx2, cy2, GRAYLINE);
}
function bracket(x, yTop, yBot) {
  s.addText("[", { x: px(x), y: px(yTop), w: px(10), h: px(yBot - yTop),
    fontSize: 15, bold: true, color: BLACK, fontFace: FONT,
    align: "center", valign: "middle", margin: 0 });
  s.addText("]", { x: px(x + 18), y: px(yTop), w: px(10), h: px(yBot - yTop),
    fontSize: 15, bold: true, color: BLACK, fontFace: FONT,
    align: "center", valign: "middle", margin: 0 });
}
