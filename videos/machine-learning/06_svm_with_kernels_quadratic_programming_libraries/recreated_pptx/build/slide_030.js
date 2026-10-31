// slide_030.js — RBF Kernel (matches reanalysis spec layout; eq PNGs from eq_030/)
const pptxgen = require("pptxgenjs");
const fs = require("fs");
const path = require("path");

const NS = "/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries";
const EQ = NS + "/recreated_pptx/build/eq_030/";
const NUM = 30;
const TITLE = "Radial Basis Function (RBF) Kernel";
const FONT = "Arial";

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const W = 13.33, H = 7.5;
const s = pres.addSlide();
s.background = { color: "E8E8E8" };

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
  fontSize: 24, bold: true, color: "C00000", fontFace: FONT, margin: 0,
});

function eq(name, x, y) {
  const m = JSON.parse(fs.readFileSync(EQ + name + ".png.json"));
  s.addImage({ path: EQ + name + ".png", x, y, w: m.w_in, h: m.h_in });
  return m;
}

// Left derivation panel (blue border)
const lx = 0.29, ly = 1.24, lw = 8.84, lh = 6.0;
s.addShape(pres.shapes.RECTANGLE, {
  x: lx, y: ly, w: lw, h: lh,
  fill: { color: "FFFFFF" }, line: { color: "20457A", width: 1.5 },
});

// E1 row with peach highlight behind the first term
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.77, y: 1.54, w: 2.43, h: 0.71,
  fill: { color: "FBE3C4" }, line: { color: "FBE3C4", width: 0.5 },
});
const e1a = eq("e1a", 0.85, 1.62);
eq("e1b", 0.85 + e1a.w_in + 0.15, 1.64);

// E2 row vector
eq("e2", 0.83, 2.74);

// phi(a)^T outlined label box under the row vector
const paX = 1.93, paY = 4.09, paW = 1.47, paH = 0.75;
s.addShape(pres.shapes.RECTANGLE, {
  x: paX, y: paY, w: paW, h: paH,
  fill: { color: "FFFFFF" }, line: { color: "333333", width: 1 },
});
const phia = JSON.parse(fs.readFileSync(EQ + "phia.png.json"));
s.addImage({ path: EQ + "phia.png", x: paX + (paW - phia.w_in) / 2, y: paY + (paH - phia.h_in) / 2, w: phia.w_in, h: phia.h_in });

// phi(b) outlined label box and e^{-b^2/2} label, left of the column bracket
const pbX = 4.60, pbY = 4.50, pbW = 1.87, pbH = 0.83;
s.addShape(pres.shapes.RECTANGLE, {
  x: pbX, y: pbY, w: pbW, h: pbH,
  fill: { color: "FFFFFF" }, line: { color: "333333", width: 1 },
});
const phib = JSON.parse(fs.readFileSync(EQ + "phib.png.json"));
s.addImage({ path: EQ + "phib.png", x: pbX + (pbW - phib.w_in) / 2, y: pbY + (pbH - phib.h_in) / 2, w: phib.w_in, h: phib.h_in });
eq("eb2", 6.33, 4.62);

// tall column bracket of the b series
eq("colb", 7.27, 2.74);

// Right panel
const rx = 9.01, ry = 1.80, rw = 4.16, rh = 5.44;
s.addShape(pres.shapes.RECTANGLE, {
  x: rx, y: ry, w: rw, h: rh,
  fill: { color: "FFFFFF" }, line: { color: "20457A", width: 1.5 },
});
s.addText("RBF Kernel", {
  x: rx + 0.32, y: ry + 0.26, w: rw - 0.64, h: 0.41,
  align: "center", fontSize: 18, bold: true, color: "9E1B1B", fontFace: FONT, margin: 0,
});
const bx = 9.49, by = 5.29, bw = 3.28, bh = 0.94;
s.addShape(pres.shapes.RECTANGLE, {
  x: bx, y: by, w: bw, h: bh,
  fill: { color: "FFFFFF" }, line: { color: "333333", width: 1 },
});
const rbf = JSON.parse(fs.readFileSync(EQ + "rbf.png.json"));
s.addImage({ path: EQ + "rbf.png", x: bx + (bw - rbf.w_in) / 2, y: by + (bh - rbf.h_in) / 2, w: rbf.w_in, h: rbf.h_in });

pres.writeFile({ fileName: path.join(NS, "recreated_pptx/slide_030_recreated.pptx") })
  .then(() => console.log("wrote slide_030_recreated.pptx"))
  .catch(e => console.error(e));
