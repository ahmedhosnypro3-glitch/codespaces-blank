const pptxgen = require("pptxgenjs");

const NUM = 23;
const TITLE = "Derivatives of some Activation Functions";
const FONT = "Arial";
const BG = "E8E8E8";
const RED = "C00000";
const BLACK = "000000";
const WHITE = "FFFFFF";
const YELLOW = "FFF9C4";
const BADGE_NUM = "333333";
const PEACH = "FAE9D7";
const PEACH_BORDER = "D3B5AD";
const CREAM = "FEFFE8";
const CREAM_BORDER = "A39EBC";
const BLUE_VIOLET = "6666CC";
const RED_ACCENT = "E20A14";
const GREEN = "1E8C1E";

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const W = 13.33, H = 7.5;
const s = pres.addSlide();
s.background = { color: BG };

// HOUSE CHROME — red frame, badge, title y (all three overridden by house rule)
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: W - 0.3, h: H - 0.3,
  fill: { type: "none" }, line: { color: RED, width: 1.5 },
});
s.addShape(pres.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: YELLOW }, line: { color: YELLOW, width: 0.5 },
});
s.addText(String(NUM), {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5, align: "center", valign: "middle",
  fontSize: 18, bold: true, color: BADGE_NUM, fontFace: FONT, margin: 0,
});
s.addText(TITLE, {
  x: 0.6, y: 0.28, w: 12.13, h: 0.8, align: "center", valign: "top",
  fontSize: 28, bold: true, color: RED, fontFace: FONT, margin: 0,
});

// inner blue-violet panel (measured: y 1.51-7.07, x 1.00-11.30)
s.addShape(pres.shapes.RECTANGLE, {
  x: 1.00, y: 1.51, w: 11.30, h: 5.56,
  fill: { type: "none" }, line: { color: BLUE_VIOLET, width: 1 },
});

// --- geometry measured from unique_slides/slide_023.jpg (PIL probes) ---
const EQ = require("/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/recreated_pptx/build/eq023_manifest.json");
const BUILD_DIR = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/recreated_pptx/build/";
const LX = 1.15, RX = 8.61, RW = 3.58;
const ROWS = [
  { lY: 1.96, lH: 0.76, lW: 4.90, rY: 2.00, rH: 0.65, lEq: "eq023_L1", rEq: "eq023_R1" },
  { lY: 3.08, lH: 0.74, lW: 4.90, rY: 3.11, rH: 0.65, lEq: "eq023_L2", rEq: "eq023_R1" },
  { lY: 4.16, lH: 0.66, lW: 3.29, rY: 4.27, rH: 0.47, lEq: "eq023_L3", rEq: "eq023_R3" },
  { lY: 5.32, lH: 0.66, lW: 3.31, rY: 5.41, rH: 0.44, lEq: "eq023_L4", rEq: "eq023_R4" },
  { lY: 6.39, lH: 0.42, lW: 1.95, rY: 6.29, rH: 0.60, lEq: "eq023_L5", rEq: "eq023_R5" },
];
const INSET = 0.08;

function placeEq(key, bx, by, bw, bh) {
  const m = EQ[key];
  const aspect = m.w_px / m.h_px;
  const availW = bw - 2 * INSET, availH = bh - 2 * INSET;
  let w = availW, h = w / aspect;
  if (h > availH) { h = availH; w = h * aspect; }
  s.addImage({ path: BUILD_DIR + m.image, x: bx + (bw - w) / 2, y: by + (bh - h) / 2, w: w, h: h });
}

function connector(cx, cy, ch) {
  const top = cy + (ch - 0.56) / 2;
  s.addText("Derivative", {
    x: cx, y: top, w: 1.09, h: 0.26, align: "center", valign: "top",
    fontSize: 13, italic: true, color: RED_ACCENT, fontFace: "Times New Roman", margin: 0,
  });
  s.addText("⇒", {
    x: cx, y: top + 0.22, w: 1.09, h: 0.34, align: "center", valign: "top",
    fontSize: 24, color: RED_ACCENT, fontFace: "Times New Roman", margin: 0,
  });
}

ROWS.forEach(r => {
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
    x: LX, y: r.lY, w: r.lW, h: r.lH,
    fill: { color: PEACH }, line: { color: PEACH_BORDER, width: 0.75 },
  });
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
    x: RX, y: r.rY, w: RW, h: r.rH,
    fill: { color: CREAM }, line: { color: CREAM_BORDER, width: 0.75 },
  });
  placeEq(r.lEq, LX, r.lY, r.lW, r.lH);
  placeEq(r.rEq, RX, r.rY, RW, r.rH);
  connector(6.69, r.lY, r.lH);
});

pres.writeFile({
  fileName: BUILD_DIR + "slide_023_recreated.pptx",
}).then(() => console.log("wrote slide_023_recreated.pptx"));
