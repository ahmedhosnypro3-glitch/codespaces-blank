// Slide 003 "Problem Formulation" — house-chrome template + original-frame geometry.
//
// Every coordinate was measured with PIL on
// videos/machine-learning/09_introduction_to_neural_networks/unique_slides/slide_003.jpg
// (960x540 frame, so 1 frame px = 1pt = 1/72in).
//   panel borders   x 67..871, rows 89-91 / 203-205 / 216-218 / 300-302 /
//                   314-316 / 403-405 / 418-419 / 502-504
//   text left edge  x 80;  body cap height 14px (=> 21pt, rendered at 22pt)
//   line baselines  p1 111/138/165/193  p2 235/263/290
//                   p3 header 338 (fully underlined, rule at y 340 x 79-304)
//                   p4 437/464/489
//   colors          "class I" red, "Class II"/"Class II" blue, "misclassified" black,
//                   d(X)/X_i/delta green, ">0" red in p1c but blue in p2c/p4c,
//                   "<0" blue in p1d but red in p2b/p4b; the sigma-limit word
//                   "misclassified" and "(i)" red; the trailing X mark red.
//   equation strip  ink x 84-733, y 354-396 (sigma x 219-240 y 354-380, limits
//                   band x 162-298 y 384-396); trailing red X ink x 762-786.
// Build: cd <this dir> && node slide_003.js
const pptxgen = require("pptxgenjs");

const NUM = 3;
const TITLE = "Problem Formulation";
const FONT = "Times New Roman";
const W = 13.33, H = 7.5;

const px = (v) => +(v / 72).toFixed(4);

const RED = "C00000";    // title / class I / <0 (p1c) / trailing X
const BLUE = "0000CC";   // class II / >0
const GREEN = "008000";  // d(X), X_i, delta_i
const BLACK = "000000";
const BORDERC = "9E1B1B";
const FILLC = "E8E8E8";

const BODY = 22;
const INK_OFF = 0.34 * BODY; // LibreOffice cap-top offset below the text box top, in px

const PLACE = require("./assets/eq_error_place.json");

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const s = pres.addSlide();
s.background = { color: FILLC };

// 1. outer red house frame (house rule: 0.15in inset from every edge)
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: W - 0.3, h: H - 0.3,
  fill: { type: "none" },
  line: { color: RED, width: 1.5 },
});

// 2. slide-number badge (house rule; numeral = the number printed on the original)
s.addShape(pres.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: "FFF9C4" }, line: { color: "FFF9C4", width: 0.5 },
});
s.addText(String(NUM), {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  align: "center", valign: "middle",
  fontSize: 18, bold: true, color: "333333", fontFace: FONT, margin: 0,
});

// 3. title box (house rule: y=0.28, x=0.6, w=12.13, centered)
s.addText(TITLE, {
  x: 0.6, y: 0.28, w: 12.13, h: 0.55,
  align: "center", valign: "top",
  fontSize: 30, bold: true, color: RED, fontFace: FONT, margin: 0,
});

// 4. the four content panels
const BOX_X = px(67);
const BOX_W = px(805);
const TEXT_X = px(80);
const TEXT_W = px(790);
const PANELS = [
  { top: 89, h: 117 },
  { top: 216, h: 87 },
  { top: 314, h: 92 },
  { top: 418, h: 87 },
];

function panel(p) {
  s.addShape(pres.shapes.RECTANGLE, {
    x: BOX_X, y: px(p.top), w: BOX_W, h: px(p.h),
    fill: { color: FILLC },
    line: { color: BORDERC, width: 1 },
  });
}

function line(p, baseline, parts, opts) {
  const runs = parts.map((q) => ({ text: q[0], options: Object.assign({}, opts, q[1]) }));
  s.addText(runs, {
    x: TEXT_X, y: px(p.top + baseline - INK_OFF - 14), w: TEXT_W, h: 0.36,
    align: "left", valign: "top", margin: 0,
  });
}

const B = { fontSize: BODY, color: BLACK, fontFace: FONT };
const REDT = { color: RED, italic: true };
const BLUET = { color: BLUE, italic: true };
const GRNB = { color: GREEN, bold: true };
const UNDER = { bold: true, underline: true };
const XCOND = { bold: true, underline: true };

// ---- Panel 1 : Define two classes ----------------------------------------
const p1 = PANELS[0];
panel(p1);
line(p1, 111, [
  ["Define two classes: ", {}],
  ["class I", REDT],
  [" and ", {}],
  ["Class II", BLUET],
], B);
line(p1, 138, [
  ["let ", { italic: true }],
  ["d(X)", GRNB],
  [" be a discriminent function = ", {}],
  ["W", { bold: true }],
  ["T", { bold: true, superscript: true }],
  [" X", GRNB],
], B);
line(p1, 165, [
  ["if ", {}],
  ["X", XCOND],
  [" \u2208 ", {}],
  ["class I", REDT],
  [" then ", {}],
  ["d(X)", GRNB],
  [" ", {}],
  ["> 0", { color: RED, bold: true }],
], B);
line(p1, 193, [
  ["if ", {}],
  ["X", XCOND],
  [" \u2208 ", {}],
  ["class II", BLUET],
  [" then ", {}],
  ["d(X)", GRNB],
  [" ", {}],
  ["< 0", { color: BLUE, bold: true }],
], B);

// ---- Panel 2 : For misclassified X ---------------------------------------
const p2 = PANELS[1];
panel(p2);
line(p2, 235, [
  ["For ", {}],
  ["misclassified", { bold: true }],
  [" ", {}],
  ["X", GRNB],
  [" :", {}],
], B);
line(p2, 263, [
  ["If ", {}],
  ["X", XCOND],
  [" \u2208 ", {}],
  ["class I", REDT],
  [" and ", {}],
  ["misclassified", { italic: true }],
  [" as ", {}],
  ["Class II", BLUET],
  [" then ", {}],
  ["d(X)", GRNB],
  [" will be ", {}],
  ["<0", { color: RED, bold: true }],
], B);
line(p2, 290, [
  ["If ", {}],
  ["X", XCOND],
  [" \u2208 ", {}],
  ["class II", BLUET],
  [" and ", {}],
  ["misclassified", { italic: true }],
  [" as ", {}],
  ["class I", REDT],
  [" then ", {}],
  ["d(X)", GRNB],
  [" will be ", {}],
  [">0", { color: BLUE, bold: true }],
], B);

// ---- Panel 3 : Define Error function as ----------------------------------
const p3 = PANELS[2];
panel(p3);
line(p3, 338, [
  ["Define Error function as:", UNDER],
], B);
// 2D mathtext strips (600 dpi PNGs, never hand-written OMML): placements come
// from assets/eq_error_place.json, measured against the original frame.
for (const p of PLACE) {
  s.addImage({
    path: p.image,
    x: p.x, y: p.y, w: p.w, h: p.h,
  });
}

// ---- Panel 4 : Define delta_i --------------------------------------------
const p4 = PANELS[3];
panel(p4);
line(p4, 437, [
  ["Define ", UNDER],
  ["\u03b4", GRNB],
  ["i", { color: GREEN, bold: true, subscript: true }],
  [" as :", {}],
], B);
line(p4, 464, [
  ["If ", {}],
  ["X", XCOND],
  [" \u2208 ", {}],
  ["class I", REDT],
  [" and ", {}],
  ["misclassified", { italic: true }],
  [" as ", {}],
  ["Class II", BLUET],
  [" then ", {}],
  ["d(X)", GRNB],
  [" will be ", {}],
  ["<0", { color: RED, bold: true }],
  [" \u21d2 ", {}],
  ["\u03b4", GRNB],
  ["i", { color: GREEN, bold: true, subscript: true }],
  [" = -1 \u21d2 ", {}],
  ["d(X)", GRNB],
  [" ", {}],
  ["\u03b4", GRNB],
  ["i", { color: GREEN, bold: true, subscript: true }],
  [" >0", {}],
], B);
line(p4, 489, [
  ["If ", {}],
  ["X", XCOND],
  [" \u2208 ", {}],
  ["class II", BLUET],
  [" and ", {}],
  ["misclassified", { italic: true }],
  [" as ", {}],
  ["class I", REDT],
  [" then ", {}],
  ["d(X)", GRNB],
  [" will be ", {}],
  [">0", { color: BLUE, bold: true }],
  [" \u21d2 ", {}],
  ["\u03b4", GRNB],
  ["i", { color: GREEN, bold: true, subscript: true }],
  [" = +1 \u21d2 ", {}],
  ["d(X)", GRNB],
  [" ", {}],
  ["\u03b4", GRNB],
  ["i", { color: GREEN, bold: true, subscript: true }],
  [" >0", {}],
], B);

pres.writeFile({ fileName: "slide_003_recreated.pptx" }).then(() => console.log("wrote slide_003_recreated.pptx"));
