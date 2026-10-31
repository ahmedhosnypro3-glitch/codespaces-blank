"""Per-region driver notes for the Lane G b_geom_2 reports, grounded in the
measured boxes and in the 60x15 slide-inch structure maps built from the same
chrome-free content masks."""

NOTES = {
    ("008", "title"): [
        "Driver: the original's upper block (the neural-network diagram inside its beige box, "
        "plus the red 'Error' bar) starts 0.22 in higher and 1.33 in further left than the "
        "render's. The 008 frame has NO title, so this band is pure slide content - the "
        "deviation is a content geometry finding, not chrome.",
        "Robustness: under a more sensitive ink threshold (lum<205, chroma>30, 1px dilation) "
        "the left delta grows to +277 px; the verdict is unchanged.",
    ],
    ("008", "body"): [
        "Driver: the render's diagram block is 0.36 in NARROWER (7.27 in vs 8.26 in) and 0.39 in "
        "TALLER than the original's, and its right edge sits 0.63 in left of the original - the "
        "original's far-right 'dE/dw_ij' + question-mark run reaches x 12.96 in while the render "
        "stops at 12.33 in.",
        "Robustness: unchanged under the sensitive threshold (right -97 px, bottom +50 px).",
    ],
    ("008", "footer"): [
        "Driver: the build's black bottom bar is y 7.45..7.50 (h 0.05 in, build/slide_008.js:40) "
        "while the original's black band starts at 7.39 in - top-edge delta +12 px @150dpi. Small "
        "but over the 4 px tolerance; it is a bar-thickness difference, not a misplacement.",
    ],
    ("009", "title"): [
        "Chrome-attributable part (NOT a finding): the render's title text is centred in the "
        "house title box (measured title ink x 5.1..8.9 in) while the original's is left-aligned "
        "at x 0.44..2.22 in. That is the house title box (x=0.6, w=12.13, centered) overriding "
        "the original's alignment.",
        "Content part: the top-right neural-network diagram - original right edge 12.34 in vs "
        "render 11.73 in, so the render's diagram is 0.61 in narrower.",
    ],
    ("009", "body"): [
        "Driver: render left edge 0.90 in vs original 0.56 in (+0.34 in - the update-equation "
        "box's left edge) and render bottom 6.76 in vs original 6.63 in (+0.13 in). Right edge "
        "agrees to +12 px.",
        "Robustness: unchanged under the sensitive threshold (left +53 px).",
    ],
    ("010", "title"): [
        "Same split as 009: the horizontal difference is house-chrome title centring (render "
        "title x 5.1..8.9 in centred, original x 0.44..2.22 in left-aligned) - not a finding.",
        "Content part: the top-right diagram, original right edge 12.00 in vs render 11.03 in, "
        "so the render's diagram is 0.97 in narrower.",
    ],
    ("010", "body"): [
        "Driver: render left edge 0.90 in vs original 0.34 in (+0.56 in) - the original's "
        "lower-left chain-rule box starts 0.56 in further left - and render bottom 6.74 in vs "
        "original 6.90 in (-0.11 in).",
    ],
    ("012", "title"): [
        "Chrome-attributable part (NOT a finding): the build's title box is y 0.28..0.83 "
        "(build/slide_012.js:41), the house position, so the title ink sits at y 0.38..0.68 in "
        "against the original's 0.53..0.90 in.",
        "Content part: the render's title is 0.39 in narrower (2.49 in vs 2.95 in) - a glyph "
        "width / font-size difference.",
    ],
    ("012", "body"): [
        "Driver: the render's main content block is x 1.49..11.51 / y 1.69..6.00 against the "
        "original's x 0.37..10.43 / y 1.29..6.90 - shifted 1.12 in right, 0.40 in down, 1.24 in "
        "narrower and 0.90 in shorter.",
        "The structure maps show the original keeps a lower-left text block (rows 5.5..6.9) "
        "that the render replaces with a full-width block at rows 4.5..5.5, i.e. a re-layout "
        "rather than a pure offset.",
        "Robustness: unchanged under the sensitive threshold (left +169 px, top +61 px, "
        "right +156 px, bottom -133 px).",
    ],
    ("012", "footer"): [
        "FINDING (missing element): the render's footer band is empty - build/slide_012.js has "
        "no black bottom bar - while the original has one at y 7.37..7.50. Slides 008/009/010 "
        "all carry 'x:0, y:H-0.05, w:W, h:0.05' black fill.",
    ],
    ("013", "title"): [
        "Chrome-attributable (NOT a finding): the 013 frame has no content at all in y 0.15..1.10 "
        "- its only content is a centred red title plus blue subtitle at y 2.67..4.86 - so the "
        "render's title ink at y 0.58..1.10 comes from the house title box (build at y 0.45..1.45, "
        "build/slide_013.js:37).",
        "Also flagged: that build title box is y=0.45, not the house-rule y=0.28 - a house-rule "
        "deviation for the parent, still not a geometry finding.",
    ],
    ("013", "body"): [
        "Driver: the render's two text boxes (y 0.58..1.90) against the original's title+subtitle "
        "block (y 2.67..4.86, x 2.57..11.08). All four edges exceed tolerance by 236..446 px, but "
        "the entire difference is the title block's vertical placement, which the house title box "
        "governs.",
        "Verdict: EXCEEDS-TOLERANCE numerically, chrome-attributable - NOT a geometry finding.",
    ],
    ("013", "footer"): [
        "FINDING (missing element): identical to 012 - no black bottom bar in the render "
        "(build/slide_013.js has none); the original has one at y 7.37..7.50.",
    ],
}

# content  -> region deviation is slide-specific content geometry (a FINDING)
# chrome   -> deviation is entirely house-chrome governed (NOT a finding)
# mixed    -> region mixes chrome-governed and content-driven edges
CLASS = {
    ("008", "title"): "content", ("008", "body"): "content", ("008", "footer"): "content",
    ("009", "title"): "mixed", ("009", "body"): "content", ("009", "footer"): "content",
    ("010", "title"): "mixed", ("010", "body"): "content", ("010", "footer"): "pass",
    ("012", "title"): "mixed", ("012", "body"): "content", ("012", "footer"): "content",
    ("013", "title"): "chrome", ("013", "body"): "chrome", ("013", "footer"): "content",
}

# The content edge of a mixed region (the chrome edges are the title placement).
MIXED_CONTENT = {
    ("009", "title"): "the top-right neural-network diagram is 0.61 in narrower in the render "
                      "(right edge -93.2 px @150dpi); the left edge +58.3 px is house-chrome "
                      "title centring and is excluded",
    ("010", "title"): "the top-right neural-network diagram is 0.97 in narrower in the render "
                      "(right edge -146.1 px @150dpi); the left edge +58.3 px is house-chrome "
                      "title centring and is excluded",
    ("012", "title"): "the title renders 0.39 in narrower and 0.15 in taller than the original "
                      "(right -58.2 px, bottom -32.0 px @150dpi); the top edge -22.3 px is the "
                      "house title box at y=0.28 and is excluded",
}
