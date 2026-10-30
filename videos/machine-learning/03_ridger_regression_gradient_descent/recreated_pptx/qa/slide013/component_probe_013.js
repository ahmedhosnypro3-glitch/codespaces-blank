// Component verification probe: build slide 013 ONLY through the exported
// components/slide_013.js renderBase (no other code path), render, and compare
// against the certified deliverable's render.
const path = require("path");
const pptxgen = require("pptxgenjs");
const C = require(path.resolve(__dirname, "../../build/components/slide_013.js"));
const p = new pptxgen();
p.layout = "LAYOUT_WIDE";
const s = p.addSlide();
C.renderBase(p, s, { numeral: 13 });
p.writeFile({ fileName: path.resolve(__dirname, "component_probe_013.pptx") })
  .then((f) => console.log("wrote " + f));
