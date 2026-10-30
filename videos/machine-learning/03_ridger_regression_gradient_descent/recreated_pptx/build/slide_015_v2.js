// Build slide 015 v2 — colored equations + arrow fix + title fix + Remember italic
// Deck: videos/machine-learning/03_ridger_regression_gradient_descent

const path = require("path");
const fs = require("fs");
const pptxgen = require("pptxgenjs");
const { drawHouseChrome } = require("../../shared_patterns/house_chrome.js");

const OUT = "videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/slide_015_recreated_v3.pptx";
const ASSETS = path.resolve(__dirname, "assets");
const TABLE = JSON.parse(fs.readFileSync(path.join(ASSETS, "eq015_table_c.json"), "utf8"));

const px = (v) => v / 72; // frame px -> inches

// measured fills / borders (from original frame PIL measurement)
const CREAM = "FBFDE5"; // cream content rect fill
const CBORD = "C6CBC7"; // cream content rect border
const PINKF = "F7D0D3"; // pink box fill
const PBORD = "C00000"; // pink box border (deck red family)
const PEACHF = "F7DCBE"; // peach box fill
const GRING = "499243"; // green box border
const GFILL = "CFFFE3"; // green box fill
const RED = "C00000";
const BLUE = "00008B";
const BLACK = "000000";
const PALE_PINK = "FFB6C1"; // for hollow arrow
const GREEN_HL = "2E9B57";  // green highlight

const FONT = "DejaVu Sans";

const pptx = new pptxgen();
pptx.layout = "LAYOUT_WIDE";
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

const eqAt = (tag) => {
  const t = TABLE[tag];
  slide.addImage({ path: path.join(ASSETS, `eq_015_${tag}_c.png`),
                   x: px(t.x_frame), y: px(t.y_frame),
                   w: t.w_in, h: t.h_in });
};

// ============================================================
// 1. TITLE - red/blue alternating: "Minimization of " red | "Objective " blue |
//    "function to obtain " red | "BEST " blue | "model parameters" red
//    (adjudication: "Objective" was red, should be blue like "BEST")
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
//    Now rendered black with green lambda highlights
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
// sentence: "Get Best W that minimizes the Objective Function J(W)"
// "Get Best W" black; "Objective Function" blue; "J(W)" blue + W underlined
textbox(208, 292, 800, 21, [
  { text: "Get Best ", options: { color: BLACK, fontSize: 18 } },
  { text: "W", options: { color: RED, fontSize: 18 } },
  { text: " that minimizes the Objective Function ",
    options: { color: BLACK, fontSize: 18 } },
  { text: "J(", options: { color: BLUE, fontSize: 18 } },
  { text: "W", options: { color: BLUE, fontSize: 18, underline: {} } },
  { text: ")", options: { color: BLUE, fontSize: 18 } },
], "left", "middle", 18);

// ============================================================
// 4. PEACH BOX - "Remember" + the ∂W^TW/∂W = 2W identity (no border)
//    "Remember" label: red, bold, ITALIC (adjudication finding)
// ============================================================
rect(786, 275, 110, 58, PEACHF);
textbox(790, 274, 100, 20, [
  { text: "Remember", options: { color: RED, bold: true, fontSize: 11, italic: true } },
], "left", "middle", 11);
eqAt("peach_eq");

// ============================================================
// 5. CREAM CONTENT RECT B + the two DERIV lines (deriv_l1, deriv_l2)
//    deriv_l2 now includes "+ λ I W"
// ============================================================
rect(72, 344, 821, 178, CREAM, { color: CBORD, width: 1 });
eqAt("deriv_l1");
eqAt("deriv_l2");

// ============================================================
// 6. NORMAL EQUATION (left of green box, at rect's lower edge)
// ============================================================
eqAt("normal");

// ============================================================
// 6b. RIGHT ARROW between normal equation and green box
// Original: small hollow/outlined pale-pink arrow
// Render as hollow red arrow with no fill (pptxgenjs supports line-only)
// ============================================================
// normal ends at x_frame ~229+266=495; green box starts at 553; gap ~58px
// vertical center with normal eq (y_frame 467, height ~53pt)
slide.addShape(pptx.ShapeType.rightArrow, {
  x: px(500), y: px(470), w: px(45), h: px(20),
  fill: { color: "FFFFFF", transparency: 100 }, // no fill
  line: { color: PALE_PINK, width: 1.5 }
});

// ============================================================
// 7. GREEN BOX - final solution, W underlined in mathtext
// ============================================================
rect(547, 472, 339, 45, GFILL, { color: GRING, width: 1 });
eqAt("solution");

pptx.writeFile({ fileName: OUT }).then(() => {
  console.log("WROTE " + OUT);
}).catch((err) => {
  console.error("ERROR:", err);
  process.exit(1);
});
