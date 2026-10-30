const pptxgen = require("pptxgenjs");

// ---- parameters ----
const NUM = 12;
const TITLE = "SVM Primal Problem & Quadratic Equation in \u03b1 with Constraints";
const FONT = "Arial";
const W = 13.33, H = 7.5;

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const s = pres.addSlide();
s.background = { color: "E8E8E8" };

// 1. House frame (red, 0.15in inset, 1.5pt, no fill)
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: W - 0.3, h: H - 0.3,
  fill: { type: "none" },
  line: { color: "C00000", width: 1.5 },
});

// 2. Badge (yellow oval + centered bold numeral)
s.addShape(pres.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: "FFF9C4" }, line: { color: "FFF9C4", width: 0.5 },
});
s.addText(String(NUM), {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  align: "center", valign: "middle",
  fontSize: 18, bold: true, color: "333333", fontFace: FONT, margin: 0,
});

// 3. Title box (house position: y=0.28, x=0.6, w=12.13, centered)
s.addText(TITLE, {
  x: 0.6, y: 0.28, w: 12.13, h: 0.55,
  align: "center", valign: "top",
  fontSize: 20, bold: true, color: "C00000", fontFace: FONT, margin: 0,
});

// 4. Upper panel: Primal formulation (salmon/peach background)
const primalY = 0.9;
const primalH = 2.9;
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.5, y: primalY, w: 12.3, h: primalH,
  fill: { color: "FADBD8" },
  line: { color: "E74C3C", width: 1.5 },
});

// Primal label + polynomial (verbatim from spec bullet 1)
s.addText("Minimize:", {
  x: 0.7, y: primalY + 0.1, w: 2.0, h: 0.35,
  fontSize: 16, bold: true, color: "E74C3C", fontFace: FONT, margin: 0,
});
s.addText("[ +1 \u03b1\u2081\u00b2+2 \u03b1\u2081 \u03b1\u2082-5.5 \u03b1\u2081\u03b1\u2083-6 \u03b1\u2081\u03b1\u2084 +2 \u03b1\u2082\u03b1\u2081+4 \u03b1\u2082\u00b2-11 \u03b1\u2082\u03b1\u2083-12 \u03b1\u2082\u03b1\u2084", {
  x: 0.7, y: primalY + 0.5, w: 11.8, h: 0.35,
  fontSize: 14, color: "2C3E50", fontFace: FONT, margin: 0, lineSpacing: 18,
});
s.addText("-5.5 \u03b1\u2083\u03b1\u2081-11 \u03b1\u2083\u03b1\u2082+32.5 \u03b1\u2083\u00b2+36 \u03b1\u2083\u03b1\u2084 -6 \u03b1\u2084\u03b1\u2081-12 \u03b1\u2084\u03b1\u2082+36 \u03b1\u2084\u03b1\u2083+40 \u03b1\u2084\u00b2 ]- [ \u03b1\u2081+\u03b1\u2082+\u03b1\u2083+\u03b1\u2084 ]", {
  x: 0.7, y: primalY + 0.85, w: 11.8, h: 0.35,
  fontSize: 14, color: "2C3E50", fontFace: FONT, margin: 0, lineSpacing: 18,
});

// Floating equation box: 1/2[X^T P X] + q^T X (right side of top panel)
s.addShape(pres.shapes.RECTANGLE, {
  x: 8.6, y: primalY + 0.3, w: 4.0, h: 0.9,
  fill: { color: "FFFFFF" }, line: { color: "E74C3C", width: 1 },
});
s.addText("1/2[ X\u1d40 P X ] + q\u1d40 X", {
  x: 8.7, y: primalY + 0.5, w: 3.8, h: 0.5,
  align: "center", fontSize: 15, color: "2C3E50", fontFace: FONT, margin: 0,
});

// Subject to block with checkbox-style delimiters (structured)
s.addText("Subject to:", {
  x: 0.7, y: primalY + 1.35, w: 2.0, h: 0.35,
  fontSize: 16, bold: true, color: "E74C3C", fontFace: FONT, margin: 0,
});
s.addText("\u2211 \u03b1\u1d62y\u1d62=0 \u2192 \u03b1\u2081+\u03b1\u2082-\u03b1\u2083-\u03b1\u2084=0", {
  x: 0.9, y: primalY + 1.75, w: 5.5, h: 0.35,
  fontSize: 14, color: "2C3E50", fontFace: FONT, margin: 0, lineSpacing: 18,
});
s.addText("\u03b1\u2081\u22641, \u03b1\u2082\u22641, \u03b1\u2083\u22641, \u03b1\u2084\u22641", {
  x: 0.9, y: primalY + 2.1, w: 5.5, h: 0.35,
  fontSize: 14, color: "2C3E50", fontFace: FONT, margin: 0, lineSpacing: 18,
});
s.addText("\u03b1\u1d62\u22650 \u2192 \u03b1\u2081\u22650, \u03b1\u2082\u22650, \u03b1\u2083\u22650, \u03b1\u2084\u22650", {
  x: 0.9, y: primalY + 2.45, w: 5.5, h: 0.35,
  fontSize: 14, color: "2C3E50", fontFace: FONT, margin: 0, lineSpacing: 18,
});

// Section header inside the primal panel, right side (per judge finding 5)
s.addText("Quadratic Equation in \u03b1 with constraints", {
  x: 8.6, y: primalY + 1.5, w: 4.0, h: 0.7,
  align: "center", fontSize: 13, bold: true, color: "2C3E50", fontFace: FONT, margin: 0, lineSpacing: 16,
});
