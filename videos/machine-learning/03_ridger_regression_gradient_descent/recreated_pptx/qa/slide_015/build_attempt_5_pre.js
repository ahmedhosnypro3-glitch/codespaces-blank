// Build slide 015 — "Minimization of Objective function to obtain BEST model parameters"
// Deck: videos/machine-learning/03_ridger_regression_gradient_descent
// GROUND TRUTH: unique_slides/slide_015.jpg (960x540, 1 frame px = 1 pt = 1/72 in).
//
// PIL-measured geometry (qa/slide_015/{reink_015,colours_015,boxgeom via
// scratch/tmp/*}.py; every value below is measured, not assumed):
//   title          ink x129..827 y68..84, 18pt DejaVu Sans Bold (698px measured
//                  vs 696px predicted at 18pt - the sibling's verified font).
//                  Runs: "Minimization of " red | "Objective " blue |
//                        "function to obtain " red | "BEST " blue | "model parameters" red
//   cream rect A   fill FBFDE5, border C6CBC7, outer x72..892 y104..266
//   cream rect B   fill FBFDE5, border C6CBC7, outer x72..892 y344..521
//   pink box       fill F7D0D3, border C00000 (measured 142,61,84 - the deck red
//                  family), outer x73..709 y275..334
//   peach box      fill F7DCBE, NO border, outer x786..895 y275..332
//   green box      fill CFFFE3, border 499243, outer x547..885 y472..516
//
// Equations: 2D matplotlib mathtext -> 600dpi transparent PNG -> addImage at the
// exact px/600 size from eq015_table.json (built by qa/slide_015/build_eq_015.py).
// Font sizes are width-matched to the frame ink (the certified sibling
// slide_005 recipe): mathtext's \frac is taller than the original's inline ½,
// so h-ratio runs 1.0..1.3 at w-ratio ~1.0 and the ink is centred in its band.
//
// HOUSE CHROME: deck 03 — white canvas FFFFFF, gray panel E9E9E7 x54..903
// y45..540, C00000 1pt strokes LEFT x58.5 / RIGHT x901 / BOTTOM y538.5 ONLY
// (NO top stroke — a top stroke is a build defect). Badge circle d35 centered
// (876,73), fill FDFD96, purple ring 6A5ACD, bold 18pt numeral 333333 = 15.
// All of this is drawn by the shared house_chrome.js primitive.

const path = require("path");
const fs = require("fs");
const pptxgen = require("pptxgenjs");
const { drawHouseChrome } = require("../../shared_patterns/house_chrome.js");

const OUT = "videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/slide_015_recreated.pptx";
const ASSETS = path.resolve(__dirname, "assets");
const TABLE = JSON.parse(fs.readFileSync(path.join(ASSETS, "eq015_table.json"), "utf8"));

const px = (v) => v / 72; // frame px -> inches

// measured fills / borders
const CREAM = "FBFDE5"; // cream content rect fill
const CBORD = "C6CBC7"; // cream content rect border
const PINKF = "F7D0D3"; // measured (247,208,211)
const PBORD = "C00000"; // measured (142,61,84) - deck red family, founder nominal
const PEACHF = "F7DCBE"; // measured (247,220,190)
const GRING = "499243"; // measured (73,146,67)
const GFILL = "CFFFE3"; // measured (207,255,227)
const RED = "C00000";
const BLUE = "00008B"; // measured (2,0,110)
const BLACK = "000000";

const FONT = "DejaVu Sans"; // verified: 18pt bold title = 696px vs frame 698px

const pptx = new pptxgen();
pptx.layout = "LAYOUT_WIDE"; // 13.333 x 7.5 in
const slide = pptx.addSlide();

drawHouseChrome(pptx, slide, { numeral: 15 });

const rect = (x, y, w, h, fill, line = null) => {
  const opts = { x: px(x), y: px(y), w: px(w), h: px(h), fill: { color: fill } };
  if (line) opts.line = { color: line.color, width: line.width };
  return slide.addShape(pptx.ShapeType.rect, opts);
};

const textbox = (x, y, w, h, runs, align, valign, ls) => {
  const opts = { x: px(x), y: px(y), w: px(w), h: px(h), align, valign, margin: 0,
                 fontFace: FONT };
  if (ls !== null && ls !== undefined) opts.lineSpacing = ls;
  slide.addText(runs, opts);
};

// equation image: placed at its table (x_frame,y_frame) = the PNG's top-left in
// frame px, at exactly px/600 (w_in/h_in from the sidecar).  No stretching - the
// font size was chosen so the ink already matches the frame's ink width.
const eqAt = (tag) => {
  const t = TABLE[tag];
  slide.addImage({ path: path.join(ASSETS, `eq_015_${tag}.png`),
                   x: px(t.x_frame), y: px(t.y_frame),
                   w: t.w_in, h: t.h_in });
};

// ============================================================
// 1. TITLE - red/blue alternating, 18pt DejaVu Sans Bold (measured 698px ink,
//    predicted 696px at 18pt).  Ink y68..84 -> box centred on the ink band.
// ============================================================
textbox(129, 65, 700, 22, [
  { text: "Minimization of ", options: { color: RED, bold: true, fontSize: 18 } },
  { text: "Objective ", options: { color: BLUE, bold: true, fontSize: 18 } },
  { text: "function to obtain ", options: { color: RED, bold: true, fontSize: 18 } },
  { text: "BEST ", options: { color: BLUE, bold: true, fontSize: 18 } },
  { text: "model parameters", options: { color: RED, bold: true, fontSize: 18 } },
], "left", "middle", 18);

// ============================================================
// 2. CREAM CONTENT RECT A + the three J(W) lines (eq1_l1/l2/l3)
// ============================================================
rect(72, 104, 821, 163, CREAM, { color: CBORD, width: 1 });
eqAt("eq1_l1");
eqAt("eq1_l2");
eqAt("eq1_l3");

// ============================================================
// 3. PINK BOX - the ∂J/∂W = 0 identity (left) and the sentence (right)
// ============================================================
rect(73, 275, 637, 60, PINKF, { color: PBORD, width: 1.5 });
eqAt("redbox_eq");
// sentence ink x209..702 y296..315, 18pt DejaVu Sans (measured 494px, predicted
// 490px at 18pt).  Only the trailing J(W) is blue (x650..702) and its W is the
// underlined one; "Best W" is NOT underlined in the original.
textbox(208, 292, 800, 21, [
  { text: "Get Best W that minimizes the Objective Function ",
    options: { color: BLACK, fontSize: 18 } },
  { text: "J(", options: { color: BLUE, fontSize: 18 } },
  { text: "W", options: { color: BLUE, fontSize: 18, underline: {} } },
  { text: ")", options: { color: BLUE, fontSize: 18 } },
], "left", "middle", 18);

// ============================================================
// 4. PEACH BOX - "Remember" + the ∂W^TW/∂W = 2W identity (no border)
// ============================================================
rect(786, 275, 110, 58, PEACHF);
// "Remember" red bold 11pt (measured 65px wide; predicted 67px at 11pt DejaVu Bold)
textbox(790, 274, 100, 20, [
  { text: "Remember", options: { color: RED, bold: true, fontSize: 11 } },
], "left", "middle", 11);
eqAt("peach_eq");

// ============================================================
// 5. CREAM CONTENT RECT B + the two DERIV lines
// ============================================================
rect(72, 344, 821, 178, CREAM, { color: CBORD, width: 1 });
eqAt("deriv_l1");
eqAt("deriv_l2");

// ============================================================
// 6. NORMAL EQUATION (left of the green box, at the rect's lower edge)
// ============================================================
eqAt("normal");

// ============================================================
// 7. GREEN BOX - the final solution, W underlined in the mathtext
// ============================================================
rect(547, 472, 339, 45, GFILL, { color: GRING, width: 1 });
eqAt("solution");

pptx.writeFile({ fileName: OUT }).then(() => {
  console.log("WROTE " + OUT);
}).catch((err) => {
  console.error("ERROR:", err);
  process.exit(1);
});
