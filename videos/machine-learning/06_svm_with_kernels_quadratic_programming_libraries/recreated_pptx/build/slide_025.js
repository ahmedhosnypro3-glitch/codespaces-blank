// slide_025.js — FRESH rebuild from qa/reanalysis2/slide_025_analysis.txt (rebuild wave 3)
// Run: cd recreated_pptx/build && NODE_PATH=$(npm root -g) node slide_025.js
const pptxgen = require("pptxgenjs");
const path = require("path");

const NUM = 25;
const TITLE = "Quadratic Kernel Mapping and Kernel Trick";
const W = 13.33, H = 7.5;
const NS = "/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries";
const EQDIR = path.join(NS, "recreated_pptx/build/eq_025");
const manifest = require(path.join(EQDIR, "manifest_rb4.json"));

// normalized spec coords [x0,y0,x1,y1] -> inches
const X = v => v * 13.33, Y = v => v * 7.5;
const box = r => ({ x: X(r[0]), y: Y(r[1]), w: (r[2] - r[0]) * 13.33, h: (r[3] - r[1]) * 7.5 });

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const s = pres.addSlide();
s.background = { color: "E8E8E8" };

// House chrome (overrides spec frame/badge/title/letterbox)
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
  fontSize: 18, bold: true, color: "333333", fontFace: "Arial", margin: 0,
});
s.addText(TITLE, {
  x: 0.6, y: 0.28, w: 12.13, h: 0.55,
  align: "center", valign: "top",
  fontSize: 24, bold: true, color: "C00000", fontFace: "Arial", margin: 0,
});

function rect(r, fill, lineColor, lineW, rounded) {
  const b = box(r);
  s.addShape(rounded ? pres.shapes.ROUNDED_RECTANGLE : pres.shapes.RECTANGLE, {
    x: b.x, y: b.y, w: b.w, h: b.h,
    fill: fill ? { color: fill } : { type: "none" },
    line: { color: lineColor, width: lineW },
  });
}
// math PNG at natural size (w = px/600), left-aligned at box x, v-centered
function eq(name, r) {
  const b = box(r), m = manifest[name];
  s.addImage({
    path: m.path,
    x: b.x, y: b.y + (b.h - m.h_in) / 2,
    w: m.w_in, h: m.h_in,
  });
}

// Cream content panel, blue stroke (spec LAYOUT / VISUAL_ELEMENTS)
rect([0.065, 0.144, 0.833, 0.569], "FFFBF0", "3333CC", 1.0);
// Highlight rounded boxes (spec VISUAL_ELEMENTS)
rect([0.069, 0.159, 0.126, 0.243], "F7E3CE", "F7E3CE", 0.5, true); // peach, behind "a = (a1 a2)"
rect([0.069, 0.265, 0.117, 0.320], "FDE2DE", "FDE2DE", 0.5, true); // pink, behind "a^T b"
rect([0.069, 0.420, 0.108, 0.480], "FDE2DE", "FDE2DE", 0.5, true); // pink, behind "[a^T b]"

// Equations E1-E5 (spec section 8), placed at their measured spec boxes.
// e1 is left-aligned in its box (asset is taller than the box is wide);
// e5 is centered on the original caption position (x ~ 0.722 norm).
{
  const b = box([0.071, 0.161, 0.198, 0.243]), m = manifest.e1;
  s.addImage({ path: m.path, x: b.x, y: b.y + (b.h - m.h_in) / 2, w: m.w_in, h: m.h_in });
}
{
  const b = box([0.069, 0.259, 0.521, 0.363]), m = manifest.e2;
  s.addImage({ path: m.path, x: b.x, y: b.y + (b.h - m.h_in) / 2, w: m.w_in, h: m.h_in });
}
eq("e3", [0.069, 0.380, 0.458, 0.541]);
eq("e4", [0.513, 0.374, 0.783, 0.520]);
{
  const m = manifest.e5, cx = 0.722 * 13.33, cy = (0.520 + 0.550) / 2 * 7.5;
  s.addImage({ path: m.path, x: cx - m.w_in / 2, y: cy - m.h_in / 2, w: m.w_in, h: m.h_in });
}

// Mouse-pointer glyph (spec IMAGERY): small black arrow with white outline
const pb = box([0.308, 0.770, 0.329, 0.804]);
s.addShape(pres.shapes.ISOSCELES_TRIANGLE, {
  x: pb.x, y: pb.y, w: pb.w, h: pb.h, rotate: 315,
  fill: { color: "000000" }, line: { color: "FFFFFF", width: 1.0 },
});

pres.writeFile({ fileName: path.join(NS, "recreated_pptx/slide_025_recreated.pptx") })
  .then(() => console.log("wrote slide_025_recreated.pptx"))
  .catch(e => console.error(e));
