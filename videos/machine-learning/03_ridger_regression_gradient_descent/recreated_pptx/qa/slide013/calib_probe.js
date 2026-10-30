// w013 calibration probe — NOT a deliverable. Measures LO rendering of the
// chosen fonts/sizes against slide_013's measured targets.
const pptxgen = require("pptxgenjs");
const path = require("path");
const OUT = path.resolve(__dirname, "calib.pptx");
const px = (v) => v / 72;

const p = new pptxgen();
p.layout = "LAYOUT_WIDE";
const s = p.addSlide();
s.background = { color: "FFFFFF" };

// title candidates
const t = 'Effect of Overfitting on model parameter \u201cW\u201d';
[["A24", 24], ["A28", 28], ["A30", 30]].forEach(([tag, fs], i) => {
  s.addText(t, { x: px(154), y: px(40 + i * 40), w: px(700), h: px(36),
    align: "left", valign: "top", margin: 0, fontFace: "Arial", fontSize: fs, bold: true,
    color: "C00000", lineSpacing: fs + 4 });
});

// table probe at 013 geometry, 20pt Times, subscript headers
function cell(v, opts) { return { text: v, options: opts }; }
const head = [
  cell("", { bold: true, color: "0000A7", fontFace: "Times New Roman", fontSize: 20, align: "center", fill: { color: "FFFFFF" } }),
  ...[1,2,3,4,5,6,7,8].map(n => cell([
    { text: "X", options: { bold: true, color: n % 2 ? "0000A7" : "C00000", fontFace: "Times New Roman", fontSize: 20 } },
    { text: String(n), options: { bold: true, color: n % 2 ? "0000A7" : "C00000", fontFace: "Times New Roman", fontSize: 13, subscript: true } },
  ], { fill: { color: "FFFFFF" }, align: "center" }))
];
const rows = [
  [["X1", 1,2,3,4,8,9,10,11]],
  [["X1", 1,2,3,4,8,9,10,30]],
];
const body = rows.map(([row]) => row.map((v, ci) => {
  if (ci === 0) {
    return cell([
      { text: "X", options: { bold: true, color: "0000A7", fontFace: "Times New Roman", fontSize: 20 } },
      { text: String(v).slice(1), options: { bold: true, color: "0000A7", fontFace: "Times New Roman", fontSize: 13, subscript: true } },
    ], { fill: { color: "FFFFFF" }, align: "left" });
  }
  return cell(String(v), { bold: true, color: ci % 2 ? "0000A7" : "C00000", fontFace: "Times New Roman", fontSize: 20, align: "center", fill: { color: v === 30 ? "FFFF00" : "FFFFFF" } });
}));

s.addTable([head, ...body], {
  x: px(92), y: px(200), w: px(367), h: px(62),
  colW: [41,41,40,41,41,41,40,42,40].map(px),
  rowH: [31,31,31].map(px),
  fontFace: "Times New Roman", fontSize: 20,
  border: { pt: 1.5, color: "CED0CD" },
  autoFit: false,
});

// W vector text candidates
[["T20", 20], ["T22", 22], ["T24", 24]].forEach(([tag, fs], i) => {
  s.addText("0.67", { x: px(520 + i * 60), y: px(300), w: px(50), h: px(30),
    align: "center", valign: "middle", margin: 0, fontFace: "Times New Roman", fontSize: fs,
    color: "000000", lineSpacing: fs + 2 });
});
// ellipse text with superscript
s.addText([
  { text: "||W||", options: { italic: true, fontFace: "Times New Roman", fontSize: 16, color: "808000" } },
  { text: "2", options: { italic: true, fontFace: "Times New Roman", fontSize: 11, superscript: true, color: "808000" } },
  { text: " = 8.11", options: { italic: true, fontFace: "Times New Roman", fontSize: 16, color: "808000" } },
], { x: px(515), y: px(420), w: px(105), h: px(24), align: "center", valign: "middle", margin: 0 });

// label box text candidates
[["L15", 15], ["L17", 17], ["L19", 19]].forEach(([tag, fs], i) => {
  s.addShape(p.ShapeType.rect, { x: px(96 + i * 90), y: px(480), w: px(64), h: px(28), fill: { color: "0000A7" } });
  s.addText("Train", { x: px(96 + i * 90), y: px(480), w: px(64), h: px(28),
    align: "center", valign: "middle", margin: 0, fontFace: "Times New Roman", fontSize: fs,
    bold: true, italic: true, color: "FFFFFF" });
});

p.writeFile({ fileName: OUT }).then(() => console.log("wrote " + OUT));
