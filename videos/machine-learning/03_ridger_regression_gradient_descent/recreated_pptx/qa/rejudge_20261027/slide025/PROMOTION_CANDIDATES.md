# PROMOTION_CANDIDATES — slide 025 clean PASS/PASS verdict pairs
Started 2026-10-31T08:50:38Z by promote_guard_20261031.py (promoter/guard; agent-386 owns promotion; no DB writes).
A pair qualifies when judge_full_*.txt + crop_dense_judge_*.txt share a tag, both contain a
FINAL VERDICT ... PASS line (not FAIL / not 'PASS or'), both have zero '429' lines, and the
judged render maps to a pptx md5 currently on disk.

