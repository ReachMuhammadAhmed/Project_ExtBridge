# Decision record

## Gate log (append one line after every gate)

| date | stage | candidate (I-xxx or P-xxx) | outcome (proceed/reshape/drop) | reason |
|---|---|---|---|---|
| 2026-11-04 | Stage 0 | — | pending (student) | Logs, templates and tools/verify_citation.py created; AI test runs passed (real DOI and arXiv verified; fake title, wrong first author and nonexistent DOI rejected). Exit still needs the student's own test verification (SETUP_KEYS.md §3). |
| 2026-11-04 | Stage 1 | — | proceed (AI side) | 81/100 cells have a confirmed public source (34 direct fetch, 47 GitHub API) ≥ 8. Final once the student has opened the sources for the cells they pursue. |

## Final decision (Stage 8)

```
Chosen topic (primary):
Backup topic:
Final gap statement:                     [link to gap_statement.md]
Pilot result:                            [link to pilot_report.md; threshold met?]
Venue and track:                         [link to venue_dossier.md]
Research questions:
Evaluation plan:
  - datasets, baselines, metrics, statistics:
  - replication package (what is shared, where, what cannot be shared and why):
Main risks and mitigations:
Why each other candidate was dropped:    [see gate log]
Frozen on (commit hash or OSF link):
```
