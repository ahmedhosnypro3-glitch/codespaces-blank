// slide_016.js — REBUILD from qa/reanalysis2/slide_016_analysis.txt (fix round 2).
// Spec coords normalized [x0,y0,x1,y1] -> inches: x*13.33, y*7.5.
// Build from project root: node <NS>/recreated_pptx/build/slide_016.js
const pptxgen = require("pptxgenjs");
const fs = require("fs");
const path = require("path");

const NS = "/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries";
const EQ = path.join(NS, "recreated_pptx/build/eq_016");
const man = JSON.parse(fs.readFileSync(path.join(EQ, "manifest.json"), "utf8"));
const W = 13.33, H = 7.5, FONT = "Arial", SERIF = "Times New Roman";
const box = r => ({ x: r[0] * W, y: r[1] * H, w: (r[2] - r[0]) * W, h: (r[3] - r[1]) * H });

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const s = pres.addSlide();
s.background = { color: "E8E8E8" };

// House chrome (mandatory, overrides spec): red frame, badge, title
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: W - 0.3, h: H - 0.3,
  fill: { type: "none" }, line: { color: "C00000", width: 1.5 },
});
s.addShape(pres.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: "FFF9C4" }, line: { color: "FFF9C4", width: 0.5 },
});
s.addText("16", {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  align: "center", valign: "middle",
  fontSize: 18, bold: true, color: "333333", fontFace: FONT, margin: 0,
});
s.addText("Non-Linearly Separable Data", {
  x: 0.6, y: 0.28, w: 12.13, h: 0.55,
  align: "center", valign: "top",
  fontSize: 26, bold: true, color: "C00000", fontFace: FONT, margin: 0,
});

// Inner red plot frame around the whole diagram region
const pf = box([0.025, 0.150, 0.890, 0.790]);
s.addShape(pres.shapes.RECTANGLE, {
  x: pf.x, y: pf.y, w: pf.w, h: pf.h,
  fill: { type: "none" }, line: { color: "C00000", width: 1 },
});

// Beige "Mapping" box, peach fill, blue italic serif header
const mb = box([0.060, 0.205, 0.275, 0.315]);
s.addShape(pres.shapes.RECTANGLE, {
  x: mb.x, y: mb.y, w: mb.w, h: mb.h,
  fill: { color: "F6D9A8" }, line: { color: "C8A96A", width: 1.25 },
});
s.addText("Mapping", {
  x: mb.x, y: mb.y + 0.015, w: mb.w, h: 0.16,
  align: "center", valign: "middle",
  fontSize: 12, italic: true, color: "1F49C7", fontFace: SERIF, margin: 0,
});
// Equation image x => phi(x) = [ x ; x^2 ] (true 2-D column, blue serif)
const eb = box([0.075, 0.240, 0.260, 0.312]);
const em = man.eq_map;
s.addImage({
  path: path.join(EQ, em.file), w: em.w_in,
  x: eb.x + (eb.w - em.w_in) / 2, y: eb.y + (eb.h - em.h_in) / 2,
});

// Right-upper note in a red-bordered box, both lines red, first line bold italic
const nb = box([0.685, 0.225, 0.905, 0.350]);
s.addShape(pres.shapes.RECTANGLE, {
  x: nb.x, y: nb.y, w: nb.w, h: nb.h,
  fill: { type: "none" }, line: { color: "C00000", width: 1 },
});
const t1 = box([0.690, 0.235, 0.900, 0.285]);
s.addText("Data is linearly separable", {
  x: t1.x, y: t1.y, w: t1.w, h: t1.h,
  align: "left", valign: "middle",
  fontSize: 14, bold: true, italic: true, color: "C00000", fontFace: FONT, margin: 0,
});
const t2 = box([0.695, 0.300, 0.900, 0.340]);
s.addText("In the new representation", {
  x: t2.x, y: t2.y, w: t2.w, h: t2.h,
  align: "left", valign: "middle",
  fontSize: 14, italic: true, color: "C00000", fontFace: FONT, margin: 0,
});

// "Linear Decision Boundary" callout: three-line bold-italic blue label inside a
// bordered box beside the right end of the boundary, thin leader to the line end
const bl = box([0.740, 0.395, 0.900, 0.495]);
s.addShape(pres.shapes.RECTANGLE, {
  x: bl.x, y: bl.y, w: bl.w, h: bl.h,
  fill: { color: "F6D9A8" }, line: { color: "1F49C7", width: 1 },
});
s.addText("Linear\nDecision\nBoundary", {
  x: bl.x, y: bl.y, w: bl.w, h: bl.h,
  align: "left", valign: "middle",
  fontSize: 13, bold: true, italic: true, color: "1F49C7", fontFace: SERIF, margin: 0,
});
s.addShape(pres.shapes.LINE, {
  x: 0.715 * W, y: 0.488 * H, w: (0.748 - 0.715) * W, h: (0.508 - 0.488) * H,
  line: { color: "1F49C7", width: 1 },
});

// Red axes with arrowheads. Vertical x^2 axis at PANEL CENTRE (points straddle it);
// horizontal x axis along the zero line. Axis labels as crisp text runs.
const AX = 0.455;
s.addShape(pres.shapes.LINE, {
  x: AX * W, y: 0.185 * H, w: 0, h: (0.780 - 0.185) * H,
  line: { color: "C00000", width: 2, beginArrowType: "triangle" },
});
s.addShape(pres.shapes.LINE, {
  x: 0.025 * W, y: 0.780 * H, w: (0.885 - 0.025) * W, h: 0,
  line: { color: "C00000", width: 2, endArrowType: "triangle" },
});
s.addText([
  { text: "x", options: { fontSize: 18, italic: true, color: "C00000", fontFace: SERIF } },
  { text: "2", options: { fontSize: 12, italic: true, color: "C00000", fontFace: SERIF, superscript: true } },
], { x: AX * W + 0.09, y: 0.150 * H, w: 0.5, h: 0.3, margin: 0 });
s.addText("x", {
  x: 0.890 * W, y: 0.725 * H, w: 0.3, h: 0.3, margin: 0,
  fontSize: 18, italic: true, color: "C00000", fontFace: SERIF,
});

// Blue horizontal linear decision boundary, stopping short of the callout
s.addShape(pres.shapes.LINE, {
  x: 0.300 * W, y: 0.505 * H, w: (0.715 - 0.300) * W, h: 0,
  line: { color: "1F49C7", width: 2.25 },
});

// Cyan class: symmetric parabola arms about the axis, height increasing outward.
// Red class: tight inverted-arc cluster, top pair just below the boundary.
const cyan = [[0.425, 0.455], [0.385, 0.360], [0.345, 0.250],
              [0.485, 0.455], [0.525, 0.360], [0.565, 0.250]];
const red = [[0.440, 0.545], [0.470, 0.545], [0.400, 0.600],
             [0.510, 0.600], [0.360, 0.660], [0.550, 0.660]];
function dots(list, color) {
  list.forEach(p => {
    const cx = p[0] * W, cy = p[1] * H, r = 0.085;
    s.addShape(pres.shapes.OVAL, {
      x: cx - r, y: cy - r, w: 2 * r, h: 2 * r,
      fill: { color }, line: { color, width: 0 },
    });
  });
}
dots(cyan, "17BECF");
dots(red, "DD2C2C");

// Original 1-D data: 12 open circles on the x-axis, grouped 3 blue / 6 red / 3 blue
const seq = ["0033CC", "0033CC", "0033CC", "CC0000", "CC0000", "CC0000",
             "CC0000", "CC0000", "CC0000", "0033CC", "0033CC", "0033CC"];
for (let i = 0; i < 12; i++) {
  const cx = (0.335 + (0.240 * i) / 11) * W, cy = 0.780 * H, r = 0.07;
  s.addShape(pres.shapes.OVAL, {
    x: cx - r, y: cy - r, w: 2 * r, h: 2 * r,
    fill: { type: "none" },
    line: { color: seq[i], width: 1.5 },
  });
}

pres.writeFile({ fileName: path.join(NS, "recreated_pptx/slide_016_recreated.pptx") })
  .then(() => console.log("wrote slide_016_recreated.pptx"))
  .catch(err => { console.error(err); process.exit(1); });
