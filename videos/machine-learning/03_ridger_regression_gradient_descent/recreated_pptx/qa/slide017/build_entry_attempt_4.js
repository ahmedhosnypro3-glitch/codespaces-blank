// Build slide 017 — "Adding Ridge Regularizer to the model λ=3"
// Deck: videos/machine-learning/03_ridger_regression_gradient_descent
//
// CHILD of slide 013 (dependency edge 17 > 13). The composition lives in the
// shared component components/slide_017.js, which IMPORTS the certified parent
// component (table PATTERN) and redraws it at 017's own PIL-measured geometry
// with 017's own values. This script is only the writer.
//
// Run: cd <project root> && NODE_PATH=$(npm root -g) node <this file>
const path = require("path");
const pptxgen = require("pptxgenjs");
const C = require(path.resolve(__dirname, "./components/slide_017.js"));

const OUT = path.resolve(__dirname, "../slide_017_recreated.pptx");

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const slide = pres.addSlide();

C.renderBase(pres, slide, { numeral: 17 });

pres.writeFile({ fileName: OUT })
  .then((f) => console.log("wrote " + f))
  .catch((e) => { console.error(e); process.exit(1); });
