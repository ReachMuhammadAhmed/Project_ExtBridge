# Decision record

## Gate log (append one line after every gate)

| date | stage | candidate (I-xxx or P-xxx) | outcome (proceed/reshape/drop) | reason |
|---|---|---|---|---|
| 2026-11-04 | Stage 0 | — | pending (student) | Logs, templates and tools/verify_citation.py created; AI test runs passed (real DOI and arXiv verified; fake title, wrong first author and nonexistent DOI rejected). Exit still needs the student's own test verification (SETUP_KEYS.md §3). |
| 2026-11-04 | Stage 1 | — | superseded | 81/100 cells had a reachable source, but reachability alone isn't usability; re-cut below. |
| 2026-11-04 | Stage 1 (re-cut) | — | proceed (AI side) | Usability scoring (`tools/score_stage1.py`): 85 reachable cells scored, 73 score ≥ 6; short list of 12 cells from 11 distinct sources (max 2 per source). Final once the student has opened every short-listed source; licence scores of 1 to be confirmed before Stage 6. |
| 2026-11-04 | Stage 1 (fact fix) | — | proceed (AI side); short list changed | History inputs in `tools/score_stage1.py` corrected from the fact-finding check: L-lkp 2022→2013 (message dates in epoch 0), F4 2011→2019 (oldest GitHub issue), R3 unverified→2004 (oldest Launchpad task). Regenerated `intersection_map.md`: still 85 cells / 73 ≥ 6 / 12 short-listed, now **10** distinct sources. R3 now scores 9 in two cells (Drivers × Debugging, Reliability & observability × Repair); K13 (Kernel code × Repair) fell off the list; list numbering changed. Student's short-list decision still pending. |
| 2026-11-05 | Stage 0: test verification | — | proceed | **AI-run** at 2026-11-05T00:15Z UTC on doi:10.1109/TSE.2019.2952614 (PatchNet): Scholar Sidekick verify = `matched` (high, no mismatches); retraction-check `isRetracted:false`, no corrections or concerns; `tools/verify_citation.py` with the correct title → `=> VERIFIED` (exit 0); with a wrong title → `=> NOT VERIFIED` (exit 1, title similarity 0.38). The student **waived** their personal run (methodology Stage 0 "AI vs. you") to avoid blocking on a gate; recorded as a deviation, not as a student check. |
| 2026-11-05 | Stage 1 | — | superseded | Student decision: new short-list cell #7 (Reliability & observability × Repair, R3) is dropped, and the Stage 1 short list is superseded by the direct topic evaluation in `TOPIC_DECISION.md` (options A–C from the student plus up to 2 found in the measured sources). The student has not personally opened the sources; this is recorded as a deviation from the Stage 1 exit criterion. |
| 2026-11-05 | Stage 2 (evidence) | P-001..P-004 | proceed P-001 (10), P-002 (7), P-004 (6), P-003 (5) | Evidence scores per methodology (2/practice source, +1 recurring, +1 cost). P-003's three items all trace to one person, counted as 2 independent by time period. All quotes re-checked verbatim by `tools/probes/quotecheck.py`; subagent paraphrases replaced by exact text. |
| 2026-11-05 | Stage 5A Pass 1 | I-001..I-004 | proceed I-001, I-003 to Pass 2; drop I-002; stop I-004 | No full-overlap paper for any card. I-002 dropped: fails engineer-substitution (robot already groups tests per commit; 226 of 6,517 blamed commits got >1 report) and Mu et al. NDSS 2022 covers duplicate kernel reports (difference in degree). I-004 not taken further: issue-commit link recovery is a mature field (Bachmann FSE 2010, DeepLink SANER 2019, EALink ASE 2023, PaStA ICSE 2019) → difference in degree. Ranking by partial overlaps put I-003 (fewest) and I-001 (tie-broken by rubric) into Pass 2. |
| 2026-11-05 | Stage 5A Pass 2 | I-001, I-003 | proceed both | Gap not falsified for either (98 and 46 Pass 2 queries; snowballing to saturation; venue sweep; tool search; adversarial abstracts incl. Undermind). I-001 reshaped: Hmissa et al. ICPE 2026 predicts Mozilla alerts linked to bugs, so RQ3 is framed as replication-extension; novelty rests on RQ1/RQ2 and the dataset. |
| 2026-11-05 | Stage 4 (double scoring) | I-001..I-004 | I-001 4.00 / I-003 3.65 (AI) vs 4.00 / 3.70 (independent) | Main session and a fresh independent scorer (cards + rubric only). No criterion differed by more than 1 point; ranking identical with or without the gap cap (I-001 3.65 capped vs I-003 3.35). |
| 2026-11-05 | Stage 5B red-team | I-001 | reshape → proceed | Fresh Opus reviewer (card + gap statement only): O1 label recall drifts with tagging adoption → main window 2020+, code-based outcome route, stratified check of 'ignored', second coder + κ; O2 novelty is a setting → reframed as explicit contrast with triaged Mozilla alerts (Besbes shares) and bot-report studies (SyzRetrospector, OSS-Fuzz); O3 RQ3 underpowered (24 test positives) → secondary, pre-registered, pooled metrics. No missed paper on 0-day/LKP report outcomes. |
| 2026-11-05 | Selection (TOPIC_DECISION.md) | I-001 | chosen; I-003 fallback | Highest score in both scorings (4.00/4.00; 3.65 capped), strongest practice evidence (P-001 = 10), gap not falsified in Pass 1, Pass 2 or red-team. I-003 fallback (3.65/3.70). I-002 dropped, I-004 not pursued (see Pass 1 row). Awaiting the student's one-line acceptance. |

## Decisions outside gates (UTC dates)

| date | decision | by | reason |
|---|---|---|---|
| 2026-11-04 | `research/` pilots (Direction A: ext readers disagree on logical contents; Direction B: ext2 deletion artefacts vs. kernel driver) **rejected**; do not revive | student | Rejected on the merits of the idea, not only because an AI proposed them. Files stay in `research/` as history only. |


## Assumptions logged during the topic evaluation (2026-11-05)

| # | assumption | reason |
|---|---|---|
| A1 | "Acted-on" = a mainline commit cites the report's Message-ID (any lore list path) or reverts the blamed commit; this is a lower bound. | Fixes without tags are invisible to scripts; manual coding is planned to measure the gap. |
| A2 | Replies from senders other than the robot count as "human replies" (includes robot staff follow-ups). | Names are not kept; only the robot's From line is matched. |
| A3 | The oe-lkp archive is treated as the public record of robot performance reports; private reports exist (robot FAQ mentions "a private report or tree"). | Selection-bias threat, stated in the plan. |
| A4 | The mainline history in the probes came from the GitHub mirror (commit metadata only); the study plan uses git.kernel.org clones so GitHub's research-use clause does not apply to the chosen topic's data. | Keeps the open-access constraint off the main data path. |
| A5 | Scholar Feed returned HTTP 503 throughout; OpenAlex, arXiv, Crossref, Semantic Scholar and Undermind (search only) were used instead. | Host unavailable; logged in search_log.csv. |
| A6 | The venue sweep used OpenAlex source filters, not per-proceedings browsing. | conf.researchr.org lists were not crawled; residual risk for very recent papers. |
| A7 | Huang et al., JSS 2026 (kernel performance bugs) could not be read (no abstract, ScienceDirect 403) and is a residual risk. | Student to request the PDF from the authors. |
| A8 | The student's "Yang et al., arXiv 2605.07678" is recorded as Tian et al., FSE 2026 (Scholar Sidekick and arXiv record). | Record metadata wins. |
| A9 | ICSE 2027 SRC (deadline 13 Nov 2026) is not the primary target. | Too soon for results; participation needs registration (cost not checked). |
| A10 | Subagent errors corrected before logging: first authors "Yang"→Yedida (TSE 2023) and "Xia"→Xiao (TR 2020); a wrong arXiv ID (2504.18806, "Pope et al.") and a placeholder ID discarded; two quotes re-copied. | Citation rule and verbatim-quote rule. |

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
