# Quality checklist: 15 failure patterns

This is part of the methodology (`methodology.md`). Each item is checked at a named gate; a gate can't pass while one of its items fails.

| Gate | Items checked |
|---|---|
| Stage 3 exit | 4 |
| Stage 5B exit | 2, 5, 6, 7 |
| Stage 6 exit | 8, 9, 10, 11, 12 |
| Stage 8 exit | all 15 |

For each item: **Detect** = how you notice it · **Prevent** = what stops it happening · **Correct** = what to do when you find it.

### 1. Fabricated references
- **Detect:** the citation verification rule (Stage 0). Scholar Sidekick returns "not_found" or "mismatch", or `tools/verify_citation.py` exits non-zero.
- **Prevent:** no reference enters the literature matrix or the claims register before it passes the rule. AI-produced references stay `[AI-unverified]`.
- **Correct:** delete the reference and every claim resting on it, then find a real source or drop the claim.

### 2. A real paper cited for a claim it doesn't make
- **Detect:** the `claims_register.md` columns `page`, `quote`, `supports`. A claim without a quote, or marked `partial`/`no`, is flagged.
- **Prevent:** read the cited passage yourself (`[read-full]`) before writing the claim, and copy the exact quote into the register.
- **Correct:** reword the claim to match what the source says, find a source that does support it, or remove it.

### 3. Wrong details in real references
- **Detect:** field-by-field match (title, authors, year, venue) in Scholar Sidekick or `verify_citation.py`; `[manual-check]` for papers without a DOI.
- **Prevent:** take metadata from Crossref, arXiv or dblp records, never from memory or AI output. Store each paper in Zotero with its DOI.
- **Correct:** replace the entry with the record's metadata and rerun the check.

### 4. Generic or repeated ideas
- **Detect:** the anti-generic tests (engineer substitution, LLM swap, baseline), plus near-duplicate idea cards.
- **Prevent:** you write the first research question for each problem before any AI involvement (Stage 3), and choose the AI method by data shape.
- **Correct:** merge duplicate cards, and reshape or drop cards that fail a test.

### 5. Novelty that collapses when executed
- **Detect:** the difference from each closest work is only one of degree, or the pilot (Stage 6) can't show the effect.
- **Prevent:** apply the difference-in-kind rule and the "why does this gap exist?" test in 5B, and set a pre-registered pilot threshold.
- **Correct:** narrow the question to what is genuinely new, or drop the candidate and promote the next one.

### 6. A gap supported only by a keyword search
- **Detect:** `search_log.csv` shows only exact-phrase queries, with no synonyms, no snowballing, no venue sweep and no adversarial search.
- **Prevent:** run both Stage 5A passes in full. Zero hits for one phrase is never evidence.
- **Correct:** finish the missing search steps before stating any gap.

### 7. Thin or stale literature
- **Detect:** fewer than 5 closest papers read in full; no papers from the last 2–3 years; snowballing never reached saturation.
- **Prevent:** Pass 2 saturation rule, arXiv alerts from Stage 5 onward, and forward citations of the closest papers.
- **Correct:** extend the search: forward citations, recent venue tables of contents, arXiv sorted by date.

### 8. No baseline, metric or success threshold
- **Detect:** the idea card or `pilot_plan.md` lacks a current-practice baseline, a trivial baseline, a metric, or a threshold.
- **Prevent:** the Stage 3 gate requires baseline and metric; the Stage 6 pre-registration requires threshold and kill criterion.
- **Correct:** add them and re-register before running anything. Never set them after seeing results.

### 9. Leakage from splits that ignore time order
- **Detect:** random train/test splits on historical data; results suspiciously better than baselines; future information among the features.
- **Prevent:** time-based splits for anything with history; use only features available at prediction time.
- **Correct:** redo the split by time and rerun. Report the change in `pilot_report.md`.

### 10. Unchecked heuristic labels
- **Detect:** labels from keywords or rules with no agreement measurement.
- **Prevent:** the hand-labelled agreement check (Stage 6): ≥ 50 random items, agreement and Cohen's κ against a pre-set minimum. Also write the sampling-bias note.
- **Correct:** fix the heuristic or label by hand until the minimum is met. State the remaining label noise as a threat to validity.

### 11. LLM threats, if any LLM is used
- **Detect:** closed or unversioned models, possible training-data leakage (the model may have seen your benchmark), results that can't be rerun.
- **Prevent:** prefer classical methods. If an LLM is needed, use a local open model with a pinned version, fixed prompts and seeds, and data created after the model's cutoff where possible.
- **Correct:** add a leakage check (e.g., post-cutoff data), report the model version and prompts, or replace the LLM with a non-LLM baseline.

### 12. Numbers with no script output behind them
- **Detect:** a number in a document or the paper that no committed script or raw output reproduces.
- **Prevent:** every number comes from a committed script plus raw output (e.g., `tools/score_stage1.py` produces the Stage 1 table).
- **Correct:** regenerate the number from a script, or remove it.

### 13. Repetitive or overclaiming prose
- **Detect:** the same phrases repeated; words like "first", "novel", "significantly" without evidence; claims broader than the data.
- **Prevent:** write the paper text yourself. Every claim must be in `claims_register.md` with `supports = yes`, and "significant" is only used with a statistical test.
- **Correct:** cut repetition, scope claims to the data studied, and add "to our knowledge, after a search of …" where a novelty claim is kept.

### 14. Poor fit with the SE/OS domain
- **Detect:** the problem has no practice evidence from OS/systems projects, or the venue calibration set has no similar paper.
- **Prevent:** Stage 1 usability scoring, Stage 2 practice evidence (≥ 2 sources), and the Stage 7 calibration set.
- **Correct:** reframe around the evidenced systems problem, or change venue or track.

### 15. Undisclosed AI use
- **Detect:** AI-produced text, code, figures or searches that don't appear in `ai_use_log.md` or in the paper's acknowledgments.
- **Prevent:** log every AI use as it happens (`ai_use_log.md`), and draft the IEEE acknowledgment from the log in Stage 8.
- **Correct:** add the missing log entries and update the acknowledgment, naming each AI system, the sections and the level of use, before submission.
