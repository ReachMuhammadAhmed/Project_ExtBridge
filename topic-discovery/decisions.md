# Decision record

## Gate log (append one line after every gate)

| date | stage | candidate (I-xxx or P-xxx) | outcome (proceed/reshape/drop) | reason |
|---|---|---|---|---|
| 2026-11-04 | Stage 0 | — | pending (student) | Logs, templates and tools/verify_citation.py created; AI test runs passed (real DOI and arXiv verified; fake title, wrong first author and nonexistent DOI rejected). Exit still needs the student's own test verification (SETUP_KEYS.md §3). |
| 2026-11-04 | Stage 1 | — | superseded | 81/100 cells had a reachable source, but reachability alone isn't usability; re-cut below. |
| 2026-11-04 | Stage 1 (re-cut) | — | proceed (AI side) | Usability scoring (`tools/score_stage1.py`): 85 reachable cells scored, 73 score ≥ 6; short list of 12 cells from 11 distinct sources (max 2 per source). Final once the student has opened every short-listed source; licence scores of 1 to be confirmed before Stage 6. |
| 2026-11-04 | Stage 1 (fact fix) | — | proceed (AI side); short list changed | History inputs in `tools/score_stage1.py` corrected from the fact-finding check: L-lkp 2022→2013 (message dates in epoch 0), F4 2011→2019 (oldest GitHub issue), R3 unverified→2004 (oldest Launchpad task). Regenerated `intersection_map.md`: still 85 cells / 73 ≥ 6 / 12 short-listed, now **10** distinct sources. R3 now scores 9 in two cells (Drivers × Debugging, Reliability & observability × Repair); K13 (Kernel code × Repair) fell off the list; list numbering changed. Student's short-list decision still pending. |

## Decisions outside gates (UTC dates)

| date | decision | by | reason |
|---|---|---|---|
| 2026-11-04 | `research/` pilots (Direction A: ext readers disagree on logical contents; Direction B: ext2 deletion artefacts vs. kernel driver) **rejected**; do not revive | student | Rejected on the merits of the idea, not only because an AI proposed them. Files stay in `research/` as history only. |

## Open constraints

| opened | constraint | affects | resolve at | status |
|---|---|---|---|---|
| 2026-11-04 | GitHub Acceptable Use Policies §7: "Researchers may use public, non-personal information from the Service for research purposes, only if any publications resulting from that research are open access." (https://docs.github.com/en/site-policy/acceptable-use-policies/github-acceptable-use-policies, opened 2026-11-04). Publications from GitHub-sourced data must be open access, and only non-personal information may be used. | Every GitHub-hosted source, including F4 (e2fsprogs), S5 (blktests), F7 (libfuse), S9 (nvme-cli) | Stage 7 (venue and track: open-access route); Stage 2 onward: report in aggregate, no personal data (ethics note) | open |

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
