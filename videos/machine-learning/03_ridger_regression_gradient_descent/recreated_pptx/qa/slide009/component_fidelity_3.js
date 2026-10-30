// Slide 009 — component fidelity probe (attempt 5, 2026-10-24, worker w009).
// Builds the CURRENT certified component (build/components/slide_009.js) into a
// standalone pptx and exercises the hook API (numeral / skip / only), so the
// render of the component can be diffed pixel-by-pixel against render_5.png.
// Outputs: qa/slide009/component_probe_attempt5.pptx  (+ shape-count log)
const path = require("path");
const pptxgen = require("pptxgenjs");
const COMP = path.resolve(__dirname, "..", "..", "build", "components", "slide_009.js");
const comp = require(COMP);

function newPptx() {
  const p = new pptxgen();
  p.layout = "LAYOUT_WIDE";
  return p;
}

// 1) full composition (must be pixel-identical to slide_009_recreated.pptx)
{
  const p = newPptx(); const s = p.addSlide();
  comp.renderBase(p, s, { numeral: 9 });
  p.writeFile({ fileName: path.join(__dirname, "component_probe_attempt5.pptx") })
    .then(() => console.log("wrote component_probe_attempt5.pptx shapes=" + s._slideObjects.length));
}
// 2) hook variants (shape-count gates)
const variants = [
  ["only-chrome", { only: { chrome: true } }, 6],
  ["skip-captions", { skip: { captions: true } }, 151],
  ["only-chrome-panels-axes", { only: { chrome: true, panels: true, axes: true } }, 102],
  ["numeral-42", { numeral: 42 }, 155],
];
(async () => {
  for (const [name, opts, want] of variants) {
    const p = newPptx(); const s = p.addSlide();
    comp.renderBase(p, s, opts);
    const n = s._slideObjects.length;
    console.log(`${name}: shapes=${n} (want ${want}) ${n === want ? "OK" : "DIFF"}`);
    await p.writeFile({ fileName: path.join(__dirname, `component_probe_attempt5_${name}.pptx`) });
  }
})();
