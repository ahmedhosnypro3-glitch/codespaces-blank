"""probe_adj10_link1.py — SUPERSEDED, banked for the record.

First attempt to measure connector-1's path (the `dot_sequence` judge's MINOR 1). It
sampled the chain-ink mask on the AWAY side of the dot1->dot2 chord and reported the
original's link-1 ink at mean +9.58 fpx away from the chord at t=0.5. That reading was
contaminated: the away-side scan band at that station contains the dashed LEADER's
anti-aliased fringe (the leader runs vertically at frame x≈261-262), which the
lum 120..215 / spread<=16 chain-ink mask also matches. The corrected, leader-excluded census
is `probe_adj10_link1b.py` / `probe_adj10_link1b_output.txt`, which places the original's
connector-1 ink on the up-right side of the chord (mean +8.09 fpx, median ~+11.2 at the
mid bins, the black curve being only +1.29 fpx up-right at the same station).

Original command (run as a heredoc from the project root):

python3 - <<'EOF'
[same content as probe_adj10_link1b.py but with the away-side scan and the
 normal fixed to (-0.9148, +0.4039), no leader exclusion]
EOF

Banked output: probe_adj10_link1_output.txt (the superseded ORIG profile, plus one REND row
that the mask missed because the render's chain ink lies on the opposite side of the chord
from the scan direction -- the first sign the scan direction was inverted).
"""
print(__doc__)
