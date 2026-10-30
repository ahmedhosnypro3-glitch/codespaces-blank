// slide_022_v3.js — "Back Propagation Training Algorithm" (badge 22) — attempt 3
// v3 vs v2: full 3-3-3 network diagram (3 input / 3 hidden / 3 output nodes,
// 9+9 directed arrows, layer captions, weight labels, Net_j/O_j, Output/Target/
// Error labels, Neural Net caption). Step boxes + equations unchanged from v2
// (certified verbatim). House chrome per video AGENTS.md.
const pptxgen = require("pptxgenjs");
const fs = require("fs");
const path = require("path");

const FONT = "Arial";
const NUM = 22;
const TITLE = "Back Propagation Training Algorithm";

const EQ_DIR = path.join(__dirname, "eq_assets", "slide_022");
const eq = {};
for (const f of fs.readdirSync(EQ_DIR).filter(f => f.endsWith(".json"))) {
  const meta = JSON.parse(fs.readFileSync(path.join(EQ_DIR, f), "utf8"));
  eq[path.basename(f, ".json")] = meta;
  eq[path.basename(f, ".json").replace(/^eq_/, "")] = meta;
}
console.log("Loaded equations:", Object.keys(eq));

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const W = 13.33, H = 7.5;
const s = pres.addSlide();
s.background = { color: "E8E8E8" };

// ---- HOUSE CHROME ----
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: W - 0.3, h: H - 0.3,
  fill: { type: "none" }, line: { color: "C00000", width: 1.5 },
});
s.addShape(pres.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: "FFF9C4" }, line: { color: "FFF9C4", width: 0.5 },
});
s.addText(String(NUM), {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  align: "center", valign: "middle",
  fontSize: 18, bold: true, color: "333333", fontFace: FONT, margin: 0,
});
s.addText(TITLE, {
  x: 0.6, y: 0.28, w: 12.13, h: 0.55,
  align: "center", valign: "top",
  fontSize: 26, bold: true, color: "C00000", fontFace: FONT, margin: 0,
});

// ---- CONTENT GEOMETRY (measured from unique_slides/slide_022.jpg, 960x540) ----
// original px -> house inches: x_in = px*0.013885 ; y_in = 1.0 + (py-108)*0.01471
const PURPLE = "800080", GREEN = "00FF00", RED = "FF0000", BLUE = "0000FF";
const BLACK = "000000", WHITE = "FFFFFF", DKGREEN = "006100";

// diagram panel
const PANEL = { x: 0.55, y: 1.00, w: 6.30, h: 2.10 };
s.addShape(pres.shapes.RECTANGLE, {
  x: PANEL.x, y: PANEL.y, w: PANEL.w, h: PANEL.h,
  fill: { type: "none" }, line: { color: RED, width: 1 },
});

// 3 columns x 3 rows
const IN_X = 1.15, HID_X = 2.85, OUT_X = 4.55;
const ROW_YS = [1.30, 1.95, 2.60];
const IN_R = 0.055, NODE_R = 0.125;

function node(slide, x, y, r, fill, line, lineW) {
  slide.addShape(pres.shapes.OVAL, { x: x - r, y: y - r, w: 2*r, h: 2*r,
    fill: { color: fill }, line: { color: line, width: lineW } });
}
function arrow(slide, x1, y1, x2, y2) {
  slide.addShape(pres.shapes.LINE, { x: x1, y: y1, w: x2 - x1, h: y2 - y1,
    line: { color: BLACK, width: 0.75, endArrowType: "triangle" } });
}
function cap(slide, txt, x, y, w, color, size) {
  slide.addText(txt, { x, y, w, h: 0.18, align: "center", valign: "middle",
    fontSize: size, bold: true, color, fontFace: FONT, margin: 0 });
}
