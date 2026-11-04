# Topic discovery (SE × AI × OS)

Working folder for the research-topic discovery methodology. Start with `methodology.md`.

| File | Stage | Purpose |
|---|---|---|
| `methodology.md` | all | The finalized methodology (stages, gates, templates) |
| `SETUP_KEYS.md` | 0 | Free accounts and API keys to create, key storage, test verification |
| `tools/verify_citation.py` | 0+ | Fallback for the citation verification rule (Crossref / DataCite / arXiv; `--dblp` for papers without a DOI). Scholar Sidekick is the primary check |
| `problem_log.csv` | 2 | Evidenced real-world problems |
| `idea_cards/` | 3 | One card per candidate topic (`TEMPLATE.md`) |
| `search_log.csv` | 4–5A | Every search query, logged |
| `literature_matrix.csv` | 5A | Papers found, with evidence tags |
| `claims_register.md` | 5B, 8 | Every factual claim the paper will make, with verification status |
| `decisions.md` | all | Gate log and the final decision record |
| `ai_use_log.md` | all | Every AI use, for the IEEE AI-use acknowledgment (Stage 8) |
| `QUALITY_CHECKLIST.md` | 3, 5B, 6, 8 | 15 failure patterns, checked at the named gates |
| `TOOLS.md` | all | Every tool: stage, purpose, verified free terms, status |
| `intersection_map.md` | 1 | Grid, usability scoring table and short list (generated) |
| `tools/score_stage1.py` | 1 | Regenerates `intersection_map.md` from the recorded source facts |

Status: Stage 0 (AI side) and Stage 1 re-cut complete; Stage 2 not started.
