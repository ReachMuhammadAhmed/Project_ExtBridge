# AI-use log

Every use of an AI tool goes here **as it happens**. Stage 8 drafts the IEEE AI-use acknowledgment from this log.

IEEE requires disclosing AI-generated content (text, figures, images and code) in the acknowledgments section. You must name the AI system, identify the sections that use AI-generated content, and briefly explain the level of use. See `TOOLS.md` for the policy source.

Fill in the exact model/version in `tool_model` from your own records (the assistant's interface shows it). `checked_or_changed` must say what **you** verified or rewrote; "pending" entries must be resolved before Stage 8.

| date | stage | tool_model | task | output_type | checked_or_changed | used_in |
|---|---|---|---|---|---|---|
| 2026-11-04 | pre-0 | Claude (Anthropic) via Claude Code | Drafted and revised the topic-discovery methodology, templates and quality checklist | text | pending student review | `methodology.md`, `QUALITY_CHECKLIST.md`, templates |
| 2026-11-04 | 0 | Claude (Anthropic) via Claude Code | Wrote the citation verifier (Crossref/DataCite/arXiv/dblp) and its tests | code | AI ran 6 tests (real, fake title, wrong author, missing DOI, arXiv, dblp fallback); student test run pending | `tools/verify_citation.py` |
| 2026-11-04 | 0 | Claude (Anthropic) via Claude Code | Drafted account/key setup instructions | text | pending student review | `SETUP_KEYS.md` |
| 2026-11-04 | 0 | Claude (Anthropic) via Claude Code (incl. subagents) | Checked free terms of research tools against official pages | search, text | pending student review of linked sources | `TOOLS.md` |
| 2026-11-04 | 1 | Claude (Anthropic) via Claude Code (incl. subagents) | Built the Stage 1 grid; checked URL reachability, licences, history spans and OpenAlex counts; wrote the scoring script | search, code, text | pending: student must open short-listed sources and review scores | `tools/score_stage1.py`, `intersection_map.md` |
| 2026-11-04 | (archived) | Claude (Anthropic) via Claude Code | Earlier exploratory pilots (ext2 reader differences, deletion artefacts), not used for topic selection | code, analysis | archived; not used | `research/` |
