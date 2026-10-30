// Pattern: house-chrome (machine-learning family, measured from slide 3 reference)
// LAWS: Slide LAYOUT_WIDE 13.33x7.5in, background E8E8E8; red frame 0.15in inset; yellow badge; title at y=0.28
// Slide 27 specific: background #E8E4D8 (per original); dense NN diagram + calc boxes

const pptxgen = require("pptxgenjs");

const NUM = 27;
const TITLE = "Example";
const FONT = "Arial";  // Sans-serif per analysis

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const W = 13.33, H = 7.5;
const s = pres.addSlide();
s.background = { color: "E8E4D8" };  // Match original beige-gray

// 1. Outer red house frame (0.15in inset from every edge)
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: W - 0.3, h: H - 0.3,
  fill: { type: "none" },
  line: { color: "C00000", width: 1.5 },
});

// 2. Slide-number badge (yellow oval + centered bold numeral) - HOUSE CHROME
s.addShape(pres.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: "FFF9C4" }, line: { color: "FFF9C4", width: 0.5 },
});
s.addText(String(NUM), {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  align: "center", valign: "middle",
  fontSize: 18, bold: true, color: "333333", fontFace: FONT, margin: 0,
});

// 3. Title box (house position, top-left, red)
s.addText(TITLE, {
  x: 0.6, y: 0.28, w: 12.13, h: 0.55,
  align: "left", valign: "top",
  fontSize: 36, bold: true, color: "C00000", fontFace: FONT, margin: 0,
});

// 4. Neural network diagram: red-bordered rectangle
// Measured: y=58-255px -> 0.81-3.54in; x=173-864px -> 2.41-12.00in
const D_X = 2.41, D_Y = 0.81, D_W = 9.59, D_H = 2.73;
s.addShape(pres.shapes.RECTANGLE, {
  x: D_X, y: D_Y, w: D_W, h: D_H,
  fill: { type: "none" },
  line: { color: "C00000", width: 2 },
});

// Diagram layer labels (measured: y=72-88px -> ~1.0in, above the diagram)
s.addText("Input",  { x: 2.55, y: 0.95, w: 1.0, h: 0.3, fontSize: 13, bold: true, color: "0000FF", fontFace: FONT, margin: 0 });
s.addText("Output", { x: 6.6,  y: 0.95, w: 1.5, h: 0.3, fontSize: 13, bold: true, color: "0000FF", fontFace: FONT, margin: 0 });
s.addText("Target", { x: 8.6,  y: 0.95, w: 1.2, h: 0.3, fontSize: 13, bold: true, color: "0000FF", fontFace: FONT, margin: 0 });

// Input nodes (x1, x2, Bias) — measured x≈223-236px -> 3.10-3.28in
const IX = 3.10, IY = 1.35, IR = 0.33, ISPC = 0.72;
const inodes = [
  { label: "x₁", val: "(1)", fill: "FFFFFF", vc: "000000" },
  { label: "x₂", val: "(5)", fill: "FFFFFF", vc: "000000" },
  { label: "Bias", val: "(1)", fill: "0000FF", vc: "FFFFFF" },
];
inodes.forEach((n, i) => {
  const y = IY + i * ISPC;
  s.addShape(pres.shapes.OVAL, { x: IX, y, w: IR, h: IR, fill: { color: n.fill }, line: { color: "000000", width: 1.5 } });
  s.addText(n.label, { x: IX, y, w: IR, h: IR, align: "center", valign: "middle", fontSize: 11, bold: true, color: n.vc, fontFace: FONT, margin: 0 });
  s.addText(n.val, { x: IX - 0.25, y: y + 0.36, w: IR + 0.5, h: 0.25, align: "center", valign: "top", fontSize: 10, color: "000000", fontFace: FONT, margin: 0 });
});

// Hidden nodes (3,4,5 yellow) — measured x≈554-566px -> 7.7-7.86in
const HX = 7.7, HY = 1.2, HR = 0.42, HSPC = 0.85;
for (let i = 0; i < 3; i++) {
  const y = HY + i * HSPC;
  s.addShape(pres.shapes.OVAL, { x: HX, y, w: HR, h: HR, fill: { color: "FFF2CC" }, line: { color: "000000", width: 1.5 } });
  s.addText(String(i + 3), { x: HX, y, w: HR, h: HR, align: "center", valign: "middle", fontSize: 15, bold: true, color: "000000", fontFace: FONT, margin: 0 });
  s.addText("O" + String.fromCharCode(8323 + i), { x: HX - 0.55, y: y + 0.12, w: 0.5, h: 0.3, align: "right", valign: "middle", fontSize: 12, color: "000000", fontFace: FONT, margin: 0 });
}

// Output nodes (6,7 orange) — measured x≈850-860px -> 11.8-11.95in
const OX = 11.8, OY = 1.45, ORAD = 0.42, OSPC = 0.85;
for (let i = 0; i < 2; i++) {
  const y = OY + i * OSPC;
  s.addShape(pres.shapes.OVAL, { x: OX, y, w: ORAD, h: ORAD, fill: { color: "FCE4D6" }, line: { color: "000000", width: 1.5 } });
  s.addText(String(i + 6), { x: OX, y, w: ORAD, h: ORAD, align: "center", valign: "middle", fontSize: 15, bold: true, color: "000000", fontFace: FONT, margin: 0 });
  s.addText("O" + String.fromCharCode(8315 + i), { x: OX + ORAD + 0.08, y: y + 0.05, w: 0.4, h: 0.3, align: "left", valign: "middle", fontSize: 12, color: "000000", fontFace: FONT, margin: 0 });
}
// Target values
s.addText("t₆ = (0)", { x: OX + ORAD + 0.55, y: OY + 0.05, w: 1.0, h: 0.3, fontSize: 12, color: "000000", fontFace: FONT, margin: 0 });
s.addText("t₇ = (1)", { x: OX + ORAD + 0.55, y: OY + OSPC + 0.05, w: 1.0, h: 0.3, fontSize: 12, color: "000000", fontFace: FONT, margin: 0 });

// η=5 label inside diagram bottom-right (measured y≈238-250px -> ~3.36in)
s.addText("η=5", { x: D_X + D_W - 0.9, y: D_Y + D_H - 0.38, w: 0.8, h: 0.3, align: "right", valign: "bottom", fontSize: 13, bold: true, color: "C00000", fontFace: FONT, margin: 0 });

// 5. "Forward" header (measured: y=250-266px -> 3.47-3.69in, x=51-146px -> 0.71-2.03in)
s.addText("Forward", { x: 0.71, y: 3.47, w: 1.32, h: 0.22, fontSize: 16, bold: true, color: "0000FF", fontFace: FONT, margin: 0 });

// 6. Left calc box 1 (measured: y=276-422px -> 3.83-5.86in, x=52-368px -> 0.72-5.11in)
const L1_X = 0.72, L1_Y = 3.83, L1_W = 4.39, L1_H = 2.03;
s.addShape(pres.shapes.RECTANGLE, { x: L1_X, y: L1_Y, w: L1_W, h: L1_H, fill: { color: "FFFFFF" }, line: { color: "000000", width: 1 } });
const netEqs = [
  "Net₃ = 1*0.1+5*0.4+1*0.1 = 2.2",
  "Net₄ = 1*0.2+5*0.5+1*0.1 = 2.8",
  "Net₅ = 1*0.3+5*0.6+1*0.1 = 3.4",
  "Net₆ = 0.9*0.3+0.943*0.4+0.968*0.5+1*0.2 = 1.3312",
  "Net₇ = 0.9*0.3+0.943*0.4+0.968*0.5+1*0.2 = 1.3312",
];
netEqs.forEach((e, i) => {
  s.addText(e, { x: L1_X + 0.15, y: L1_Y + 0.1 + i * 0.38, w: L1_W - 0.3, h: 0.35, fontSize: 13, color: "C00000", fontFace: FONT, margin: 0 });
});

// 7. Left calc box 2 (measured: y=434-529px -> 6.03-7.35in, x=53-608px -> 0.74-8.44in)
const L2_X = 0.74, L2_Y = 6.03, L2_W = 7.7, L2_H = 1.32;
s.addShape(pres.shapes.RECTANGLE, { x: L2_X, y: L2_Y, w: L2_W, h: L2_H, fill: { color: "FFFFFF" }, line: { color: "000000", width: 1 } });
s.addText("Net₆ = 0.9*0.3+0.943*0.4+0.968*0.5+1*0.2 = 1.3312", {
  x: L2_X + 0.15, y: L2_Y + 0.12, w: L2_W - 0.3, h: 0.4, fontSize: 14, color: "C00000", fontFace: FONT, margin: 0 });
s.addText("Net₇ = 0.9*0.3+0.943*0.4+0.968*0.5+1*0.2 = 1.3312", {
  x: L2_X + 0.15, y: L2_Y + 0.62, w: L2_W - 0.3, h: 0.4, fontSize: 14, color: "C00000", fontFace: FONT, margin: 0 });

// 8. Green formula box A (measured: y=276-425px -> 3.83-5.90in, x=646-896px -> 8.97-12.44in)
const G_X = 8.97, G_Y = 3.83, G_W = 3.47, G_H = 2.07;
s.addShape(pres.shapes.RECTANGLE, { x: G_X, y: G_Y, w: G_W, h: G_H, fill: { color: "D9EAD3" }, line: { color: "006100", width: 1.5 } });
const sigEqsA = [
  "O₃ = 1/(1+e⁻²·²) = 0.9",
  "O₄ = 1/(1+e⁻²·⁸) = 0.943",
  "O₅ = 1/(1+e⁻³·⁴) = 0.968",
];
sigEqsA.forEach((e, i) => {
  s.addText(e, { x: G_X + 0.15, y: G_Y + 0.12 + i * 0.62, w: G_W - 0.3, h: 0.5, fontSize: 13, color: "000000", fontFace: FONT, margin: 0 });
});

// 9. Green formula box B (measured: y=432-528px -> 6.0-7.33in, x=646-896px -> 8.97-12.44in)
const G2_Y = 6.0, G2_H = 1.33;
s.addShape(pres.shapes.RECTANGLE, { x: G_X, y: G2_Y, w: G_W, h: G2_H, fill: { color: "D9EAD3" }, line: { color: "006100", width: 1.5 } });
const sigEqsB = [
  "O₆ = 1/(1+e⁻¹·³³¹²) = 0.791",
  "O₇ = 1/(1+e⁻¹·³³¹²) = 0.791",
];
sigEqsB.forEach((e, i) => {
  s.addText(e, { x: G_X + 0.15, y: G2_Y + 0.12 + i * 0.58, w: G_W - 0.3, h: 0.5, fontSize: 13, color: "000000", fontFace: FONT, margin: 0 });
});

pres.writeFile({ fileName: "slide_027_recreated.pptx" }).then(() => console.log("wrote slide_027_recreated.pptx"));