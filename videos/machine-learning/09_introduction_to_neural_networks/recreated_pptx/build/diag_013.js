const pptxgen = require("pptxgenjs");
const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const s = pres.addSlide();
s.addText("T", { x: 1, y: 1, w: 1, h: 1, fontSize: 24, color: "B22222", fontFace: "Times New Roman" });
pres.writeFile({ fileName: "diag_013.pptx" }).then(() => console.log("ok"));
