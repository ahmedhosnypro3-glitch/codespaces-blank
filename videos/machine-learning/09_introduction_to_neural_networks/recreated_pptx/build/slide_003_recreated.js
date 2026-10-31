// Pattern: house-chrome + slide 003 content (corrected from judge feedback v2)
// Colors/bold/underline spec verified pixel-by-pixel against unique_slides/slide_003.jpg.
// Build: NODE_PATH=$(npm root -g) node slide_003_recreated.js
const pptxgen = require("pptxgenjs");

const NUM = 3;
const TITLE = "Problem Formulation";
const FONT = "Times New Roman";
const W = 13.33, H = 7.5;

// palette measured from the original frame
const RED = "C00000";   // title red
const BLUE = "0000CC";  // "class I" / "Class II" emphasis (pixel-confirmed)
const GREEN = "008000"; // d(X), W^T X, delta_i, standalone X
const BLACK = "000000";
const BORDERC = "9E1B1B";
const FILLC = "F0F0F0";

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const s = pres.addSlide();
s.background = { color: FILLC };

// 1. outer red house frame (0.15in inset from every edge)
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: W - 0.3, h: H - 0.3,
  fill: { type: "none" },
  line: { color: RED, width: 1.5 },
});

// 2. slide-number badge (house oval + centered bold numeral)
s.addShape(pres.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: "FFF9C4" }, line: { color: "FFF9C4", width: 0.5 },
});
s.addText(String(NUM), {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  align: "center", valign: "middle",
  fontSize: 18, bold: true, color: "333333", fontFace: FONT, margin: 0,
});

// 3. title box
s.addText(TITLE, {
  x: 0.6, y: 0.28, w: 12.13, h: 0.55,
  align: "center", valign: "top",
  fontSize: 32, bold: true, color: RED, fontFace: FONT, margin: 0,
});

// 4. panels. Original: borders y=90,203,217,301,315,404,419,516 of 540,
// fills span the full inner height, last panel ends at 95.6%.
const boxX = 0.67;
const boxW = 12.0;
const topY = 1.15;          // just below the title box
const gapY = 0.017 * 7.5;   // ~2px of 540 scaled
const heights = [1.575, 0.781, 0.829, 1.005]; // px-ratio panel heights (of 540)
let boxY = topY;

function panel(h) {
  s.addShape(pres.shapes.RECTANGLE, {
    x: boxX, y: boxY, w: boxW, h: h,
    fill: { color: FILLC },
    line: { color: BORDERC, width: 1 },
  });
}

function line(y, parts, opts) {
  const runs = parts.map((p) => ({ text: p[0], options: Object.assign({}, opts, p[1]) }));
  s.addText(runs, {
    x: boxX + 0.25, y: boxY + y, w: boxW - 0.5, h: 0.30,
    align: "left", valign: "top", margin: 0,
  });
}

// ---- Panel 1 : Define two classes ----
panel(heights[0]);
line(0.10, [["Define two classes: ", {}], ["class I", { color: RED, italic: true, bold: true }], [" and ", {}], ["Class II", { color: BLUE, italic: true, bold: true }]], { fontSize: 20, color: BLACK, fontFace: FONT });
line(0.42, [["let ", {}], ["d(X)", { color: GREEN, bold: true }], [" be a discriminent function = ", {}], ["W", { bold: true }], ["T", { superscript: true }], [" X", { color: GREEN, bold: true }]], { fontSize: 20, color: BLACK, fontFace: FONT });
line(0.74, [["if ", {}], ["X", { bold: true, underline: true }], [" ", {}], ["\u2208 ", {}], ["class I", { color: BLUE, italic: true }], [" then ", {}], ["d(X)", { color: GREEN, bold: true }], [" ", {}], ["> 0", { color: RED }]], { fontSize: 20, color: BLACK, fontFace: FONT });
line(1.06, [["if ", {}], ["X", { bold: true, underline: true }], [" ", {}], ["\u2208 ", {}], ["class II", { color: BLUE, italic: true }], [" then ", {}], ["d(X)", { color: GREEN, bold: true }], [" ", {}], ["< 0", { color: BLUE }]], { fontSize: 20, color: BLACK, fontFace: FONT });
boxY += heights[0] + gapY;

// ---- Panel 2 : For misclassified X ----
panel(heights[1]);
line(0.10, [["For misclassified ", { color: BLUE, italic: true }], ["X", { color: GREEN, bold: true }], [" :", {}]], { fontSize: 20, color: BLACK, fontFace: FONT });
line(0.42, [["If ", {}], ["X", { bold: true, underline: true }], [" ", {}], ["\u2208 ", {}], ["class I", { color: BLUE, italic: true }], [" and ", {}], ["misclassified", { color: RED, italic: true }], [" as ", {}], ["Class II", { color: BLUE, italic: true }], [" then ", {}], ["d(X)", { color: GREEN, bold: true }], [" will be ", {}], ["<0", { color: RED }]], { fontSize: 20, color: BLACK, fontFace: FONT });
line(0.74, [["If ", {}], ["X", { bold: true, underline: true }], [" ", {}], ["\u2208 ", {}], ["class II", { color: BLUE, italic: true }], [" and ", {}], ["misclassified", { color: RED, italic: true }], [" as ", {}], ["class I", { color: BLUE, italic: true }], [" then ", {}], ["d(X)", { color: GREEN, bold: true }], [" will be ", {}], [">0", { color: BLUE }]], { fontSize: 20, color: BLACK, fontFace: FONT });
boxY += heights[1] + gapY;

// ---- Panel 3 : Define Error function as ----
panel(heights[2]);
line(0.08, [["Define Error function as:", { bold: true, underline: true }]], { fontSize: 20, color: BLACK, fontFace: FONT });
s.addImage({
  path: "assets/eq_error.png",
  x: boxX + 0.25,
  y: boxY + 0.40,
  w: 11.5,
  h: 11.5 / 17.6119,
});
s.addText("X", {
  x: boxX + 11.05, y: boxY + 0.42, w: 1.0, h: 0.3,
  align: "left", valign: "top",
  fontSize: 20, bold: true, color: RED, fontFace: FONT, margin: 0,
});
boxY += heights[2] + gapY;

// ---- Panel 4 : Define delta_i ----
panel(heights[3]);
line(0.08, [["Define ", { bold: true, underline: true }], ["\u03b4", { color: GREEN, bold: true }], ["i", { color: GREEN, bold: true, subscript: true }], [" as :", { bold: true, underline: true }]], { fontSize: 20, color: BLACK, fontFace: FONT });
line(0.40, [["If ", {}], ["X", { bold: true, underline: true }], [" ", {}], ["\u2208 ", {}], ["class I", { color: BLUE, italic: true }], [" and ", {}], ["misclassified", { color: RED, italic: true }], [" as ", {}], ["Class II", { color: BLUE, italic: true }], [" then ", {}], ["d(X)", { color: GREEN, bold: true }], [" will be ", {}], ["<0", { color: RED }], [" \u21d2 ", {}], ["\u03b4", { color: GREEN, bold: true }], ["i", { color: GREEN, bold: true, subscript: true }], [" = -1 \u21d2 ", {}], ["d(X)", { color: GREEN, bold: true }], [" ", {}], ["\u03b4", { color: GREEN, bold: true }], ["i", { color: GREEN, bold: true, subscript: true }], [" >0", {}]], { fontSize: 20, color: BLACK, fontFace: FONT });
line(0.72, [["If ", {}], ["X", { bold: true, underline: true }], [" ", {}], ["\u2208 ", {}], ["class II", { color: BLUE, italic: true }], [" and ", {}], ["misclassified", { color: RED, italic: true }], [" as ", {}], ["class I", { color: BLUE, italic: true }], [" then ", {}], ["d(X)", { color: GREEN, bold: true }], [" will be ", {}], [">0", { color: BLUE }], [" \u21d2 ", {}], ["\u03b4", { color: GREEN, bold: true }], ["i", { color: GREEN, bold: true, subscript: true }], [" = +1 \u21d2 ", {}], ["d(X)", { color: GREEN, bold: true }], [" ", {}], ["\u03b4", { color: GREEN, bold: true }], ["i", { color: GREEN, bold: true, subscript: true }], [" >0", {}]], { fontSize: 20, color: BLACK, fontFace: FONT });

pres.writeFile({ fileName: "slide_003_recreated.pptx" }).then(() => console.log("wrote slide_003_recreated.pptx"));
