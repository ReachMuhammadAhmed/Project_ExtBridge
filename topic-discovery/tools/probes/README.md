# Feasibility probes (topic evaluation, 2026-11-05)

These scripts produced the numbers in `TOPIC_DECISION.md`. They read local clones and pages, keep no personal names or e-mail addresses in their output, and print only aggregates.

| Script | Input | Produces |
|---|---|---|
| `parse_lkp.py` | `git clone https://lore.kernel.org/oe-lkp/git/0.git` (full clone, ~709 MB) | one JSON line per message: subject fields, dates, robot flag, perf-report fields (metric, %change, blamed commit, Closes Message-ID, %stddev present, perf-profile count) |
| `label_perf.py` | output above + `git log --format='%x1e%H%x1f%ad%x1f%B'` of a treeless mainline clone (`git clone --bare --filter=tree:0 --shallow-since=2016-01-01 https://github.com/torvalds/linux.git`) | per-report labels: cited by a mainline commit (lore Message-ID in any tag), blamed commit reverted, blamed commit has a later `Fixes:` tag, number of human replies |
| `reply_kw.py` | oe-lkp clone + parsed messages | keyword counts (noise, alignment, cannot reproduce, …) in the un-quoted text of human replies to regression reports |
| `regzbot_parse.py` | saved regzbot pages (`/regzbot/resolved/`, `/regzbot/inconclusive/`) | per-regression rows: culprit commit known, version range, resolution kind, report channel, activity span |
| `profile_overlap.py` | oe-lkp + treeless kernel clone | sample check: do functions in a report's perf-profile lines overlap functions changed by the blamed commit (slow: lazily fetches trees) |
| `verify_batch.py` | TSV of claimed citations | Scholar Sidekick verify + retraction check per citation |
| `quotecheck.py` | TSV of URL + quote | checks each quote occurs verbatim on the page |

Raw clones and parsed files are not committed (size, and they contain names and addresses). Re-run the scripts to regenerate; outputs from the 2026-11-05 run are in `../../probes_output/`.
