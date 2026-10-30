# INCIDENT — stray unprefixed 15_progress.py writes (w4-s038, 2026-10-20T19:19Z)

## What happened
While setting DB milestones I invoked `scripts/15_progress.py` FIVE times without the
mandatory `VIDEO=machine-learning/03_ridger_regression_gradient_descent` prefix:

```
python3 scripts/15_progress.py set 38 gen_status building
python3 scripts/15_progress.py set 38 build_script videos/.../03_ridger.../build/slide_038.js
python3 scripts/15_progress.py set 38 pptx_path videos/.../03_ridger.../slide_038_recreated.pptx
python3 scripts/15_progress.py set 38 visual_attempts 0
python3 scripts/15_progress.py set 38 last_error ""
```

The unprefixed default target is the CLOSED ml-intro deck
(`videos/machine-learning/01_ml-intro/slides_progress.db`), so those five writes landed
on ml-intro row 38 — exactly the incident class the dispatch brief warns about.

## Damage (measured by a full row-by-row diff, live DB vs `git show HEAD:` of the same file)
Confined to `videos/machine-learning/01_ml-intro/slides_progress.db`, table `slides`,
`slide_id = 38` ("How Training Takes Place to learn the model ?"):

| field | pristine (git HEAD) | corrupted (my write) |
|---|---|---|
| gen_status | `passed` | `building` |
| pptx_path | `videos/ml-intro/recreated_pptx/slide_038_recreated.pptx` | `videos/.../03_ridger.../slide_038_recreated.pptx` |
| build_script | `videos/ml-intro/recreated_pptx/build/slide_038.js` | `videos/.../03_ridger.../build/slide_038.js` |
| visual_attempts | `1` | `0` |
| last_error | `NULL` | `''` |
| updated_at | `2026-10-10T06:03:55` | `2026-10-20T19:19:14` |

64 rows, same set live and in HEAD; `founder_issues` count identical (14/14).
No other row changed. `visual_check=PASS` and `visual_transcript` were untouched.
`worker_id` / `worker_heartbeat_at` on ml-intro row 38 are NULL both before and after
(my `claim` DID carry the VIDEO prefix and went to the 03 deck correctly).

## Repair performed
1. Backed up the corrupted file to
   `scratch/tmp/slide038/ml-intro-CORRUPTED-BY-W4-STRAY-SET.db.bak`.
2. Restored row 38's five damaged fields + `updated_at` to the git-HEAD values (direct
   sqlite update, restore-by-value not restore-by-file — see note below).
3. Re-verified: row 38 is now field-for-field identical to git HEAD; the only remaining
   live-vs-HEAD diff anywhere in the file is row 35's `updated_at`
   (`2026-10-19T15:27:34` live vs `2026-10-10T06:03:55` HEAD), which predates this
   session and was not written by me — left alone deliberately (a timestamp from prior
   legitimate activity; reverting it would erase real history).

## Note on why restore-by-file was NOT used
The live ml-intro DB carries four columns absent from git HEAD
(`pattern_group`, `pattern_seq`, `worker_id`, `worker_heartbeat_at`) — the schema was
migrated after the HEAD commit. Restoring the HEAD file byte-for-byte would have
DROPPED those columns and any data in them, breaking the script for every worker. A
field-level restore of the single damaged row is the correct minimal repair.

## Process fix adopted for the rest of this run
Every subsequent `15_progress.py` invocation is written as one command with the
`VIDEO=` prefix in the same statement, and each write is read back with a `get`.
