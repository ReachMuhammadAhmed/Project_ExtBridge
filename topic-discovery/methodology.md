# A Research-Topic Discovery Methodology for SE × AI × OS

This methodology is for one undergraduate who wants a single-author research paper in Software Engineering (SE), using Artificial Intelligence (AI) on an Operating Systems (OS) problem. It assumes no journal access, no paid APIs and a laptop, plus an AI assistant for searching and drafting.

It takes you from no topic to one validated topic, with a written gap statement and a pilot result. Follow the stages in order. Every stage ends in a **gate** with three possible outcomes:
- **Proceed:** pass conditions met.
- **Reshape:** fixable; return to an earlier stage with a specific change.
- **Drop:** discard the candidate and record why.

Don't skip gates. Most wasted effort comes from skipping one.

**Changes to the stage structure you specified:**
- **Stage 0 added** (setup and verification toolkit). The checks against AI errors, such as invented citations and unlogged searches, only work if their tools and logs exist before the first search.
- **Stage 5 split into 5A (structured prior-work search) and 5B (gap statement and red-team).** Searching and arguing about the result are different skills. Mixing them is how students talk themselves into false gaps.
  - Stage 5A itself runs in **two passes**. Pass 1 is a lighter search across all shortlisted candidates; Pass 2 is the full protocol for the top 2 only. This keeps the reading load bounded before any candidate is cut.
- **Stage 6 (pilot) comes after gap validation but before venue matching.** There's no point matching a venue for an idea whose effect may not exist.

---

## Stage 0: Setup and verification toolkit

**Purpose.** Create the logs and checks that every later stage relies on, so that mistakes, especially the AI assistant's mistakes, are caught when they happen and not much later.

**Activities, in order**
1. Create one folder (a Git repository is ideal) with these files, using the templates at the end:
   - `problem_log.csv`
   - `idea_cards/`
   - `search_log.csv`
   - `literature_matrix.csv`
   - `claims_register.md`
   - `decisions.md`
   - `ai_use_log.md` (every use of an AI tool; needed for the IEEE AI-use disclosure in Stage 8)
2. Set up free accounts and keys (details and current status in `SETUP_KEYS.md` and `TOOLS.md`):
   - OpenAlex API key (free; without one, requests share a small daily per-IP budget);
   - Scholar Sidekick key (free; used by the citation verification rule below);
   - Semantic Scholar API key (free on application; while it is pending, OpenAlex covers search and citation chasing);
   - CORE: works without a key at a low rate limit (aggregates university repository full texts).
3. Install a reference manager (Zotero is free). Every paper you rely on goes into it with its DOI.
4. Write down the **citation verification rule** (below) and the **evidence tags** used in every document:
   - `[read-full]`: you read the full text yourself;
   - `[read-abstract]`: you read only the abstract;
   - `[secondary]`: from a blog, summary or someone else's description;
   - `[AI-unverified]`: produced by the AI assistant and not yet checked.
5. *Optional:* if you want to run a small local model, install a local runner such as llama.cpp or Ollama (both free). Check your RAM first: quantized 7B-parameter models typically need about 8 GB *(approximate; verify for your model)*.
6. Read `QUALITY_CHECKLIST.md` (15 failure patterns, each checked at a named gate) and `TOOLS.md` (every tool, its free terms and the stage that uses it).

**Citation verification rule (applies everywhere).** A reference may be used, or entered into the literature matrix, only after:
1. its DOI (or arXiv ID) resolves at doi.org, Crossref or arXiv; or, for a paper with neither, its dblp record or official proceedings page is found;
2. the title, authors, year and venue *all* match that record; and
3. it has not been retracted.

Check it in this order:
- **Primary: Scholar Sidekick.** Run its citation verification (the verdict must be "matched") and its retraction check (see `TOOLS.md`).
- **Fallback: `tools/verify_citation.py`**, when Scholar Sidekick is unavailable or its quota is used up. It checks Crossref, DataCite and arXiv; check retraction status on the publisher's page by hand.
- **No DOI or arXiv ID** (common for USENIX and some workshop papers): run `tools/verify_citation.py --dblp`, which looks the paper up on dblp and compares the fields. If dblp doesn't find it or can't be reached, tag the paper `[manual-check]` and verify it against the official proceedings page before using it.

AI-produced references stay tagged `[AI-unverified]` until these checks pass.

**Sources and tools.** OpenAlex, Scholar Sidekick, Semantic Scholar, CORE, Crossref, arXiv, dblp, Zotero, Git.

**Output artifact.** A working folder with empty logs, active keys and the verification rule written down.

**Exit criteria.**
- Every log exists.
- You verified one known paper end-to-end with the citation rule, as a test run.

**Common mistakes.**
- Keeping searches "in your head". If it isn't in `search_log.csv`, it didn't happen.
- Trusting a reference because it looks plausible.

**AI vs. you.**
- The AI can write the logs, scripts and API calls.
- You must personally run the test verification, and confirm you understand each evidence tag.

---

## Stage 1: Map the SE × AI × OS intersection

**Purpose.** Lay out the space systematically, so you choose where to look based on where real artifacts and data exist, not on what's fashionable.

**Activities, in order**
1. Build a three-axis grid:
   - **OS concern:** file systems, storage, scheduling, memory management, kernel code, drivers, virtualization/containers, systems reliability and observability, boot/firmware, configuration.
   - **SE activity:** specification and documentation, testing, debugging and diagnosis, repair, maintenance and evolution, configuration management, performance engineering, security and vulnerability management, code review, CI and release.
   - **AI method family** (laptop-feasible, no paid APIs):
     - classical ML: classification, regression, ranking;
     - anomaly detection and clustering;
     - search-based SE: genetic algorithms, hill climbing, multi-objective search;
     - Bayesian optimization;
     - classic information retrieval and NLP: TF-IDF, BM25, topic models;
     - small local language models, *only where text understanding is unavoidable*.
2. For each OS concern, list the **artifacts that exist publicly**: source code and history, bug reports, test suites, configuration files, logs and traces, crash reports, mailing-list discussions, CVE records.
3. Mark each grid cell (concern × activity) with a **data availability note**: which public artifact would let you run experiments there. Leave the AI-method axis open for now. Methods are chosen later, by the shape of the data (Stage 3).
4. Shade cells that have no public data source. They're out of scope for a laptop-only, single-author project.
5. **Score each remaining cell's data usability**, 0–2 per criterion (maximum 10):

   | Criterion | 0 | 1 | 2 |
   |---|---|---|---|
   | Unit of analysis | Unclear | Definable with extra work | Clear (e.g., one bug report, one commit, one drive-day) |
   | Labels or ground truth | None | Heuristic only (e.g., keyword matching) | Recorded in the data (e.g., fix commits, issue state, failure flags, CVE fields) |
   | History | Under 1 year | 1–3 years, or start date not verified | 3 years or more (verified start date) |
   | Licence for research use | Prohibits research use (**drop the cell**) | Terms of service only, or reuse unclear (confirm before Stage 6) | Explicit open licence, public domain, or stated research permission |
   | Mining saturation (OpenAlex count of papers naming the source) | Top third of counts (heavily mined) | Middle third | Bottom third |

6. **Short-list the 8–12 highest-scoring cells** with a score of at least 6. On ties, prefer a cell whose source is not yet on the short list, then the less-mined source (lower OpenAlex count). Count each source **at most twice**; further cells from the same source become alternates, so the short list doesn't rest on one dataset. Report the number of **distinct sources** behind the short list, not just the number of cells.

*Illustration (shape only, not a recommended topic):* the cell "file systems × testing" might list artifacts such as a kernel file-system test suite's history, public bug reports, and crash-consistency bug-fix commits.

**Sources and tools.**
- Kernel source and git history (git.kernel.org, elixir.bootlin.com);
- kernel mailing lists as **lore.kernel.org git clones**, one list at a time (see `TOOLS.md`);
- GitHub;
- public issue trackers;
- public datasets: drive-health statistics, cluster traces, I/O trace repositories. *Some trace repositories require free registration; verify each one.*

**Output artifact.** `intersection_map.md`: the grid with data-availability notes, the usability scoring table, and the short list of 8–12 cells with their distinct sources.

**Exit criteria (gate).**
- **Proceed** if at least 8 cells score at least 6 on data usability, the short list holds 8–12 of them, none scores 0 on licence, and you've opened each short-listed source at least once. State how many distinct sources the short list uses.
- **Reshape** if fewer than 8 qualify: look for better sources for the weak cells (labels, longer history), or broaden the OS concerns or SE activities.

**Common mistakes.**
- Filling the grid from what *sounds* researchable. Catch it: every cell must name a specific URL or dataset you actually opened.
- Choosing the AI method first. Catch it: the AI axis stays blank until Stage 3.
- Counting cells that only passed because a URL loaded, or many cells that all rest on one source. Catch it: the usability score and the distinct-source count.

**AI vs. you.**
- The AI can propose artifact sources per cell and draft the grid.
- You must open every data source it names. AI assistants often name datasets that don't exist, or that have moved or require payment.

---

## Stage 2: Discover real problems and gather evidence

**Purpose.** Find problems that practitioners or real systems demonstrably have, *before* reading research papers. The aim is problems that come from practice, not from papers' "future work" sections, which other researchers have already claimed.

**Ethics note (applies from this stage onward, wherever you collect data).** Mailing lists, issue trackers, Q&A sites and bug databases contain real people's names, email addresses and messages.
- Report results **in aggregate**: counts, categories, patterns. Don't single out or name individuals, and don't publish personal data in your paper or replication package.
- When quoting a message as evidence in your own logs, keep the link. In anything you publish, paraphrase or anonymize unless the quote is essential and already public in a technical context.
- Follow each platform's **terms of service, API rules and rate limits** (e.g., GitHub's API terms, Stack Exchange's licence and dump terms). Don't scrape sites that forbid automated access.
- If your venue or university requires ethics review for mining human-generated data, follow that process.

**Activities, in order**
1. For each short-listed cell (Stage 1), search **practice sources** for recurring pain points:
   - **Issue trackers:** GitHub issues in systems projects; Linux kernel Bugzilla; distribution bug trackers. Filter by labels or words such as "regression", "flaky", "data corruption", "performance", "hang", "misconfiguration".
   - **Kernel bug infrastructure:** the syzbot dashboard of automatically found kernel bugs (https://syzkaller.appspot.com/upstream, per the [official syzkaller documentation](https://github.com/google/syzkaller/blob/master/docs/syzbot.md)). Look at which bug *classes* stay open longest, or recur.
   - **Mailing lists and LWN:** threads where developers say something is hard to test, diagnose or maintain. For scripted searches and counts, clone a single list from lore.kernel.org as a git repository (one list at a time; see `TOOLS.md`). LWN's subscriber-only articles become free to everyone one week after publication (per the [LWN FAQ](https://lwn.net/op/FAQ.lwn)).
   - **CVE/NVD/OSV:** recurring weakness types in OS components.
   - **Incident postmortems:** public collections of postmortems; company engineering blogs.
   - **Developer surveys and Q&A sites:** recurring questions on Unix & Linux Stack Exchange or Server Fault *(dataset dump availability has changed recently; verify)*.
   - **Calls for papers** of relevant IEEE venues. Their "topics of interest" lists show what the community currently values. Use them as a signal, not a source of problems.
2. For every candidate problem, record a **problem log** entry (template below) with:
   - a short problem statement in practitioners' terms;
   - **≥2 independent evidence items, at least one from practice** (not a research paper), each with a link and a short verbatim quote;
   - frequency and cost indicators: number of related issues, how long they stay open, affected users, severity, developer effort mentioned. For code history, count fix commits with PyDriller, filtered to the subsystem path (e.g., `fs/ext4/`; see `TOOLS.md`);
   - who suffers: kernel developers, sysadmins, application developers, test engineers.
3. Use papers at this stage **only as background**: to understand a term or how something works. Don't harvest "limitations" sections.
4. Merge duplicates. Write each problem as a *problem*, not a solution. "Developers can't tell which X will fail" is a problem; "use ML to predict X" is a solution.

**Sources and tools.** GitHub search (free; the code-search interface needs a login), kernel Bugzilla, syzbot, lore.kernel.org (in a browser, or as git clones of single lists for scripted counts), PyDriller, LWN, NVD/CVE/OSV APIs (free), public postmortem collections, IEEE conference calls for papers.

**Output artifact.** `problem_log.csv` with about 10–25 problems, each with evidence links.

**Exit criteria (gate).** Score each problem's evidence:
- 2 points per independent practice source;
- 1 point per research source;
- +1 if recurring over more than a year;
- +1 if there's a concrete cost (data loss, downtime, developer hours).

**Proceed** with problems scoring ≥5 and at least 5 of them. **Drop** problems supported only by papers.

**Common mistakes.**
- **Counting one discussion as several sources.** Catch it: evidence must come from different projects, people or time periods.
- **The AI summarising "common problems" from memory.** Catch it: every evidence item needs a link you opened and a quote copied from that page.
- **Writing solutions instead of problems.** Catch it: if the problem statement contains "ML", "LLM" or "AI", rewrite it.

**AI vs. you.**
- The AI can generate search queries, scan exported issue lists, cluster similar complaints and draft log entries.
- You must open every link, confirm every quote and judge whether two items are truly independent.

---

## Stage 3: Turn problems into research questions and candidate topics

**Purpose.** Convert evidenced problems into **answerable research questions**, choosing the AI method by the data, not by fashion, and blocking generic "apply an LLM to X" ideas.

**Activities, in order**
1. For each problem that passed Stage 2, **write the first research question yourself, before involving the AI.** AI drafts tend to repeat the same ideas, and seeing them first anchors you. The AI then only adds variants (2–4 questions in total), using these forms:
   - **Characterize:** what are the properties, causes or patterns of X? (An empirical study.)
   - **Predict/detect:** can X be predicted or detected from data Y, and how well, compared with baseline B?
   - **Prioritize/optimize:** can search or ML choose among options for X better than current practice?
   - **Compare/explain:** why do approaches A and B differ on X?
2. Choose the AI method from the **shape of the available data**:

   | Data shape | Natural method family |
   |---|---|
   | Labelled tabular features | Classical ML (e.g., gradient-boosted trees) |
   | Unlabelled metrics, logs or traces | Anomaly detection, clustering |
   | Large discrete configuration or test space | Search-based SE, Bayesian optimization |
   | Short text (bug titles, commit messages) | Classic IR/NLP first; a small local model only if classic methods clearly fail |

3. The AI runs three **anti-generic tests** on each idea, and you check its results. Fail any one and you must reshape or drop:
   - **Engineer-substitution test:** if a careful engineer with a simple script and little effort could do the same, it's an engineering task, not research.
   - **LLM-swap test:** if the idea reads "use an LLM to do X", ask what *new knowledge* results apart from "the LLM did/didn't do X well". If none, drop it.
   - **Baseline test:** name the non-AI baseline that practitioners use today. No baseline means no measurable contribution.
4. Write one **idea card** per surviving question (template below). Choose a contribution type:
   - empirical study;
   - new technique, with evaluation;
   - dataset or benchmark, with analysis;
   - replication or extension.

*Illustration (structure only):* "Problem: certain kernel bug reports stay open for a long time. RQ: can report features available at filing time predict long-lived reports better than the triage heuristic maintainers use today?" This shows the form, not a vetted topic.

**Sources and tools.** Your problem log and data sources. Only background reading.

**Output artifact.** `idea_cards/`: about 8–15 cards.

**Exit criteria (gate).** **Proceed** with cards that name all six of these:
- research question;
- data source (already opened in Stage 1 or 2);
- baseline;
- metric;
- AI method justified by the data shape;
- contribution type.

The card must also pass `QUALITY_CHECKLIST.md` item 4 (generic or repeated ideas).

**Drop** cards that fail an anti-generic test.

**Common mistakes.**
- **Drifting toward generic LLM applications**, which happens quietly when the AI assistant drafts the ideas. Catch it: the LLM-swap test, plus a rule that small language models appear only with a written reason why classic methods won't do.
- **Research questions that can't fail.** Catch it: each question must have an outcome that would count as a negative result.

**AI vs. you.**
- The AI only adds variants to the research question you wrote, runs the three anti-generic tests, fills idea cards and proposes baselines.
- You must write the first research question for each problem yourself, check the anti-generic test results, and confirm that each baseline really reflects current practice, with evidence from Stage 2.

---

## Stage 4: Screen and shortlist

**Purpose.** Cut cheaply to 3–5 candidates before spending effort on deep searches.

**Activities, in order**
1. **Quick prior-work scan (3–5 searches per card; this is *not* gap validation).** Search across OpenAlex, Semantic Scholar and Google Scholar (in your browser). Record what you find. Drop cards that turn up an obviously matching paper.
2. **Saturation check.** For the card's core terms, use OpenAlex to count papers per year for the last 6–8 years.
   - A steep curve with many top-venue papers means a crowded area. It needs a sharply different question to continue.
   - Treat counts as a rough signal only, never as proof of a gap.
3. **Score each card with the rubric** (template below). Do it **twice, independently**:
   - you score first;
   - the AI assistant scores in a **fresh chat** that receives **only the idea card and the rubric**. Never use the chat that drafted the ideas: it is anchored on its own reasoning and can't score them independently;
   - discuss any criterion where you differ by ≥2 points, and record the resolution.

   **Cap:** "Gap strength and novelty" cannot score above 3 until Stage 5 (both 5A and 5B) is complete.
4. Keep the top 3–5 that pass all hard gates.

**Sources and tools.** OpenAlex (free key), Semantic Scholar (free key), Google Scholar (browser), arXiv.

**Output artifact.** `shortlist.md`: scored cards, quick-scan results and the reason for every drop.

**Exit criteria (gate).**
- **Proceed** with 3–5 cards that pass all hard gates and score ≥3.0 overall.
- **Reshape** if fewer than 3 survive: return to Stage 3 with the best rejected cards, or to Stage 2 for more problems.

**Common mistakes.**
- **Overrating novelty because the quick scan found nothing.** Catch it: the cap above. A quick scan can't justify a high gap score.
- **The AI inflating scores to please you.** Catch it: the fresh-chat independent double scoring, plus anchored descriptions for each score level in the rubric.

**AI vs. you.**
- The AI can run the scans and pull counts; a separate fresh chat does the independent scoring.
- You must read the titles and abstracts of every match yourself, and make the final cut.

---

## Stage 5A: Structured prior-work search (two passes)

**Purpose.** Try hard to prove each shortlisted gap **false**. A gap counts only if a structured search fails to find prior work. Two passes keep the reading load manageable: a lighter Pass 1 across all shortlisted candidates, then the full protocol only for the strongest 2.

**From this stage onward**, subscribe to the free arXiv email alerts for cs.SE and cs.OS (see `TOOLS.md`). Screen each alert for papers close to your candidates, and log matches in `search_log.csv`.

### Pass 1: all shortlisted candidates (3–5)

**Activities, in order (per candidate)**
1. **Terminology expansion.** Build a synonym table for each concept: problem, OS object, SE activity, method.
   - The AI proposes terms; you add any you've seen in Stage 2 practice sources.
   - Include older and community-specific terms (e.g., the same idea named differently by systems, SE and ML researchers).
   - Write it into `search_log.csv`.
2. **Multi-database search.** Run combined queries in OpenAlex, Semantic Scholar, arXiv, Google Scholar (browser), dblp (browser) and scholar.archive.org. Log every query: source, string, date, number of hits, number screened, number kept.
3. **One snowballing round.** Pick the 3–5 closest papers found so far. Do one round of backward snowballing (their references) and forward snowballing (papers citing them, via Semantic Scholar, OpenAlex or Google Scholar's "Cited by"). Inciteful (see `TOOLS.md`) builds the citation network around a seed paper and helps with both directions.
4. Enter the relevant papers (typically 10–15 per candidate) into the literature matrix, each only after it passes the citation verification rule (Scholar Sidekick verification and retraction check first), with evidence tags and the `overlap with my RQ` field filled from title and abstract.

**Pass 1 gate (applied to each candidate, then ranking).**
- **Drop** a candidate if any paper or tool found so far answers its research question with comparable data and method.
- **Reshape** a candidate covered only partly: narrow its question to the uncovered part and rerun Pass 1 steps 1–3 on the narrower question.
- **Rank** the surviving candidates:
  - first by the number of Pass 1 papers marked `partial` overlap, judged against the candidate's current (possibly narrowed) question (fewer is better). `full` overlaps don't appear here, because they already caused a drop;
  - ties broken by the Stage 4 rubric total. This tiebreak is fair because the gap criterion is capped at 3 for every candidate at this point.
- **Keep the top 2** for Pass 2. Record the reason each other candidate was cut in `shortlist.md`.
  - If only 1 candidate survives, take it alone into Pass 2.
  - If none survive, **Reshape**: return to Stage 4 with the next-best scored card, or to Stage 3 for new cards.

### Pass 2: top 2 candidates only (full protocol)

**Activities, in order (per candidate)**
1. **Neighboring fields.** Repeat key queries for analogous domains where the *same engineering problem* appears, e.g. database systems, distributed systems, embedded systems, compilers, networking. Inciteful's citation network around your closest papers also surfaces work from neighbouring fields that uses different terms.
2. **Citation chasing to saturation.** Continue backward and forward snowballing from the closest papers. Stop when two consecutive rounds add nothing relevant.
3. **Venue sweep.** Scan the last 3 years of tables of contents of the 3–4 most likely venues, because keyword search misses papers with unusual titles. Sources:
   - conf.researchr.org: accepted-paper lists for major SE conferences;
   - the IEEE Computer Society Digital Library (tables of contents and abstracts are free);
   - IEEE Xplore browse pages (abstracts are free in a browser);
   - USENIX proceedings (free);
   - the ACM Digital Library (open access; see below).
4. **Tool and practice search.** Check whether the problem is already *solved in practice*:
   - GitHub and package registries;
   - the kernel tree's own tools and test suites;
   - vendor documentation;
   - mailing-list threads proposing a fix.

   A practical solution with no paper still weakens a gap.
5. **Adversarial search.** Ask the AI to write the abstract of the paper that would make your gap false. Then search using *that abstract's wording*. Also run it through Undermind's free tier: use it only here, for the top 2 candidates, because the free tier is rate-limited (see `TOOLS.md`). Its results go through the citation verification rule like any other source.
6. **Complete the literature matrix** (template below) for every relevant paper. Mark each with the evidence tags. Only `[read-full]` papers can be used to support the gap.

**Free routes to IEEE papers (and ACM)**, roughly in order of reliability:
1. **ACM Digital Library.** It has been **fully open access since January 1, 2026**. The free "Basic" edition contains the PDFs of all ACM-published articles, including the older archive, so ACM papers can be read free. That includes joint ACM/IEEE conference papers published by ACM. The one exception is ACM Books. Sources: [ACM bulletin, January 2026](https://www.acm.org/articles/bulletins/2026/january/acm-open-access), [ACM DL policies](https://libraries.acm.org/digital-library/policies), [ACM rights policy](https://www.acm.org/publications/policies/publication-rights-and-licensing-policy). Read them in a browser; automated downloads may be blocked.
2. **arXiv or author preprints.** Many SE and systems papers have one.
3. **Open-access links:**
   - OpenAlex's open-access location fields;
   - Semantic Scholar's open-access PDF links;
   - Unpaywall (free API, needs only a contact email in the request).
4. **Repository aggregators:** CORE (free) and scholar.archive.org (free).
5. **IEEE's author-posting policy.** It generally lets authors post their accepted manuscript on personal or institutional sites, so check the authors' homepages *(verify the current IEEE policy wording)*.
6. **Email the author** politely, asking for a copy. This usually works.
7. **Public or national libraries and alumni access**, where available to you.

Don't use unauthorised copy sites. Their legal status is a problem, and citing from them creates risk.

**Sources and tools.** All of the above, plus Zotero for organising papers, Scholar Sidekick (citation rule), Inciteful, Undermind (Pass 2 only) and arXiv alerts. Terms and limits are in `TOOLS.md`.

**Output artifact.**
- `search_log.csv`: complete for both passes;
- `literature_matrix.csv`: Pass 1 entries for every shortlisted candidate; for the 2 Pass 2 candidates, about 20–40 papers each, with the closest 5–10 marked `[read-full]`;
- a short note per Pass 2 candidate: "closest work and how it differs".

**Pass 2 gate.** **Proceed** with a candidate only if all of these hold:
- ≥3 databases searched (Pass 1);
- a synonym table with ≥3 alternatives per concept (Pass 1);
- the neighboring-field search done;
- snowballing reached saturation;
- the venue sweep done;
- the tool search done;
- the adversarial search done;
- the closest 5 papers read in full.

**Drop** a candidate if any paper or tool answers its research question with comparable data and method. **Reshape** if prior work covers it only partly: narrow the question to the uncovered part, then rerun Pass 1 steps 1–3 and Pass 2 on the narrower question.

If a Pass 2 candidate drops, promote the next-ranked Pass 1 survivor into Pass 2. If no Pass 1 survivors remain, **Reshape**: return to Stage 4 with the next-best scored card, or to Stage 3 for new cards.

**Common mistakes.**
- **Claiming a gap because an exact-phrase search returned nothing.** Catch it: the gates require the synonym table, neighboring fields and snowballing. Zero hits for one phrase is never evidence.
- **Invented or mismatched citations from the AI.** Catch it: the citation verification rule (Stage 0) before any entry enters the literature matrix.
- **Relying on abstracts.** Catch it: only `[read-full]` papers count for the gap.
- **Missing recent preprints.** Catch it: an arXiv search sorted by date, plus forward citations of the closest papers.

**AI vs. you.**
- The AI can expand terms, run API searches, de-duplicate results, chase citations, draft matrix rows and write the adversarial abstract.
- You must:
  - verify every citation;
  - read the closest papers in full;
  - decide whether each one "answers the research question";
  - confirm the tool search yourself.

---

## Stage 5B: Gap statement and red-team

**Purpose.** Turn the search results into a precise, defensible gap statement, and attack it before reviewers do.

**Activities, in order**
1. Write the **gap statement** (template below). It must name the 3–5 closest works and state the difference from each in *kind*:
   - a new question;
   - new data;
   - a new finding;
   - a new method property.

   "Better/more/faster" is a difference in degree and doesn't count.
2. Apply the **"why does this gap exist?" test**. Real gaps have reasons, such as: data only recently became available; communities didn't overlap; prior work assumed something that practice disproves (with Stage 2 evidence). A gap with no reason often means you haven't found the prior work yet.
3. **Red-team.** Ask the AI to argue *against* the gap: find prior work, call the contribution trivial, attack its significance. Answer each point with evidence, or revise.
4. Write a **novelty calibration note**:
   - Who would cite this, and why?
   - What would a reviewer in the closest paper's community say is missing?
5. *Strongly recommended:* get an outside check by sending the gap statement to one or two people with expertise (a lecturer, or an author of a closest paper). Ask: "Do you know prior work that already does this?"
6. Update `claims_register.md` (template below): add every factual claim the gap statement makes, with its source, evidence tag and verification status. For each claim, record the page and the supporting quote, and check against the source whether it really `supports` the claim (yes / partial / no). Only claims marked `yes` may stay in the gap statement.

**Output artifact.** `gap_statement.md`, plus the red-team log.

**Exit criteria (gate).**
- **Proceed** if every red-team point has a documented answer, the "why does this gap exist?" reason is supported by evidence, the difference from each closest work is in kind, and `QUALITY_CHECKLIST.md` items 2, 5, 6 and 7 pass.
- **Reshape** if the difference is only one of degree.
- **Drop** if the red-team finds prior work you can't distinguish your idea from.

**Common mistakes.**
- **Overrating novelty.** Catch it: the difference-in-kind rule, plus the "why does this gap exist?" test.
- **Defensive red-teaming,** where weak objections get answered and strong ones skipped. Catch it: the AI must list its *three strongest* objections, ranked, and all three need answers.

**AI vs. you.**
- The AI can draft the statement and red-team it.
- You must write the final differences from the closest works yourself, in your own words. If you can't explain them, you can't defend them.

---

## Stage 6: Feasibility pilot

**Purpose.** Replace "this seems feasible" with a measured result on a small scale.

**Activities, in order**
1. **Pre-register the pilot before running anything.** Write in `pilot_plan.md`:
   - the hypothesis;
   - the dataset subset;
   - the baseline;
   - the metric;
   - the **success threshold**;
   - the **kill criterion**.

   Commit it with a date (Git, or a free OSF registration).
2. Build the **smallest experiment** that can show the effect:
   - a subset of the data (e.g., one project, one subsystem or one year). For commit history, PyDriller can extract commits filtered by subsystem path (see `TOOLS.md`);
   - the baseline from the idea card;
   - your method in its simplest form.
3. **Check for pitfalls before trusting results:**
   - data leakage (use time-based splits for anything involving history);
   - class imbalance (report precision, recall and F1 or PR-AUC, not only accuracy);
   - a trivial baseline (random, or majority class);
   - **hand-labelled agreement check** for any heuristic labels (e.g., "fix" inferred from commit-message keywords). Label a random sample of at least 50 items yourself without looking at the heuristic label, then report agreement and Cohen's κ against the heuristic. Set the minimum (e.g., κ ≥ 0.6) in the pre-registration, and fix the heuristic if it's missed;
   - **sampling-bias note**: state which projects, periods and item types your data over- or under-represents. For example, only fixed bugs have fix commits, so unfixed bugs are invisible.
4. Run the experiment, record the raw outputs, and compare against the threshold.
5. Note the **laptop cost**: runtime, memory and data size. Extrapolate to the full study.

*Illustration of a pre-registered threshold:* "Proceed if the method beats the best baseline by ≥5 F1 points on a time-based split; drop if within 2 points." The numbers are examples; set yours from the idea card.

**Sources and tools.** Python (pandas, scikit-learn), PyDriller for commit history, SQL for data handling, C/C++ where systems interaction is needed; Git for the dated pre-registration.

**Output artifact.** `pilot_report.md`: the plan, the results, raw outputs, the pitfall checks, the resource cost and the gate decision.

**Exit criteria (gate).**
- **Proceed** if the threshold is met, the pitfall checks pass, the full study fits on a laptop, and `QUALITY_CHECKLIST.md` items 8–12 pass.
- **Reshape** if the signal is weak but explicable (e.g., a better feature or data source exists): rerun once with a *new* pre-registration.
- **Drop** if the kill criterion triggers, or if the data can't support the question.

**Common mistakes.**
- **Changing the threshold after seeing results.** Catch it: the dated pre-registration.
- **Leakage producing too-good results.** Catch it: time-based splits, plus a sanity check against a trivial baseline.
- **Trusting AI-written code blindly.** Catch it: you run every script, read every metric calculation, and hand-check examples.

**AI vs. you.**
- The AI can write scripts, propose features and draft the report.
- You must run everything, inspect raw data and outputs, verify the metric code, and make the gate decision.

---

## Stage 7: IEEE publication potential and venue match

**Purpose.** Pick a realistic, legitimate IEEE venue and see the gap between your planned paper and what that venue publishes.

**Activities, in order**
1. **Find candidate venues.** Use the IEEE conference search on ieee.org (free) and the IEEE Computer Society event listings. Check each one's sponsorship.
   - **IEEE-sponsored** conferences are run by IEEE.
   - **Technically co-sponsored** ones are run by others under IEEE's technical oversight; their quality varies more.
   - Avoid events whose only credential is "proceedings in IEEE Xplore", without a credible programme committee.
   - Look up each venue's tier in the ICORE conference portal, and its upcoming deadlines on se-deadlines.github.io (see `TOOLS.md`). Both are aids only; the official call for papers is authoritative.
2. Keep venues whose **current call for papers** lists your topic. Record:
   - track types: full, short, new ideas, tool/demo, student/doctoral;
   - page limits;
   - deadlines;
   - review model.
3. **Calibration set.** For your top 2–3 venues, select 5–10 recently accepted papers closest to your topic, using the free tables-of-contents routes from Stage 5A (Pass 2, step 3). For each, record:
   - contribution type;
   - number of subjects, systems or datasets;
   - baselines;
   - metrics;
   - statistical tests;
   - artifact availability;
   - **replication package**: are code and data shared (where, and how complete)? Many SE venues now expect one, and some evaluate it;
   - length.

   This is the venue's **evidence bar**.
4. **Gap-to-bar comparison.** Compare your planned full study with that bar, and list exactly what's missing.
5. **Reviewer-objection pre-mortem.** Use the free **ACM SIGSOFT Empirical Standards** (public, CC0-licensed, at [github.com/acmsigsoft/EmpiricalStandards](https://github.com/acmsigsoft/EmpiricalStandards); one standard per paper type, e.g. Engineering Research, Repository Mining, Experiments) plus the venue's reviewer guidelines. List your top 5 likely objections, each with a mitigation. Typical ones:
   - weak novelty;
   - insufficient evaluation;
   - threats to validity;
   - non-reproducibility;
   - limited significance.
6. Place the paper on the **contribution ladder** (Tests section, after the Templates), and choose the track that matches its level.

Candidate IEEE venue *types* to check:
- software testing conferences;
- software maintenance and evolution conferences;
- software reliability conferences;
- software quality and security conferences;
- regional SE conferences;
- workshops co-located with these;
- IEEE magazines and journals in SE and reliability.

Verify each named venue's scope and sponsorship yourself.

**Output artifact.** `venue_dossier.md`: candidate venues with call-for-papers notes, calibration tables, the evidence-bar gap, the objection pre-mortem and the chosen track.

**Exit criteria (gate).**
- **Proceed** if at least one legitimate IEEE venue's scope includes the topic, the evidence bar is achievable with laptop experiments, and every top-5 objection has a mitigation.
- **Reshape** the study scope or choose a different track (e.g., short or new-ideas paper) if the bar is out of reach.

**Common mistakes.**
- **"It fits the scope, so it will be accepted."** Catch it: the calibration set; fitting a scope is not evidence of acceptance.
- **Predatory or low-credibility events.** Catch it: check sponsorship and committee, plus the venue's past proceedings.
- **Underestimating the evidence bar.** Catch it: count subjects, baselines and statistics in real accepted papers.

**AI vs. you.**
- The AI can gather calls for papers and tables of contents and draft the calibration tables.
- You must read at least 3 calibration papers in full and confirm the venue's sponsorship and legitimacy.

---

## Stage 8: Final selection and decision record

**Purpose.** Choose one topic based on evidence, and document the decision so it can be defended and revisited.

**Activities, in order**
1. Re-score the surviving candidates with the full rubric. **Cap:** "Gap strength and novelty" cannot score above 3 until Stage 5 (both 5A and 5B) is complete. Stage 5 is now complete, so this cap is lifted.
2. **Apply the contribution-level tests** (Tests section, after the Templates). Only level 3–4 candidates qualify.
3. Select **one primary and one backup**. If none qualifies, record "none qualifies" and the stage to return to. Don't force a choice.
4. Write `decisions.md` with:
   - the chosen topic;
   - the final gap statement;
   - the pilot result;
   - the venue and track;
   - the research questions;
   - the evaluation plan for the full study:
     - datasets, baselines, metrics, statistics;
     - the **replication package**: which code, scripts, data and documentation will be shared; where (e.g., a public GitHub repository plus an archived copy with a DOI on a free service such as Zenodo); and which data can't be shared and why (e.g., personal data, per the Stage 2 ethics note);
   - the main risks and mitigations;
   - the gate history of every candidate, including why each dropped one was dropped.
5. Freeze the research questions and evaluation plan with a dated commit or a free OSF pre-registration.
6. Update `claims_register.md` so every factual claim in the decision record and the planned paper has a source, an evidence tag and a verification status; resolve or remove unverified claims before writing the paper.
7. Draft the **IEEE AI-use acknowledgment** from `ai_use_log.md`. IEEE requires AI-generated content (text, figures, images, code) to be disclosed in the paper's **acknowledgments section**: name each AI system, identify the sections that use its content, and briefly explain the level of use. Check the target venue's own rules too, which may be stricter. Policy source: `TOOLS.md`.

**Output artifact.** `decisions.md`, plus the frozen evaluation plan.

**Exit criteria.**
- One topic with a written gap statement (5B), a pilot passing its pre-registered threshold (6), a venue dossier (7), and a complete decision record.
- All 15 items in `QUALITY_CHECKLIST.md` pass, and the AI-use acknowledgment is drafted.

**Common mistakes.**
- **Picking the easiest topic rather than the best-validated one.** Catch it: rank by rubric score; difficulty is recorded separately, not as a hidden weight.
- **Losing the reasons for drops.** Catch it: the gate history is mandatory.

**AI vs. you.**
- The AI can compile and format the record.
- You must make and justify the selection in your own words.

---

## Templates

### 1. Problem log (`problem_log.csv`)

| Field | Content |
|---|---|
| `id` | P-001 |
| `grid_cell` | OS concern × SE activity |
| `problem_statement` | In practitioners' terms; no solution words (ML/AI/LLM) |
| `who_suffers` | e.g., maintainers, sysadmins, test engineers |
| `evidence_1_link` / `evidence_1_quote` / `evidence_1_type` | Link, verbatim quote, and type: practice or research |
| `evidence_2_…`, `evidence_3_…` | Must be independent of each other |
| `frequency_indicator` | e.g., count of related issues, time open, recurrence period |
| `cost_indicator` | Data loss, downtime, developer hours, security impact |
| `evidence_score` | Stage 2 scoring |
| `status` | proceed / reshape / drop + reason |

### 2. Idea card (`idea_cards/I-xxx.md`)

```
ID:                     I-xxx       From problem(s): P-xxx
Research question:      (one sentence, answerable, can fail)
RQ form:                characterize / predict-detect / prioritize-optimize / compare-explain
Contribution type:      empirical study / technique+evaluation / dataset+analysis / replication-extension
Data source:            (specific, already opened; link)
Data shape:             tabular-labelled / unlabelled metrics-logs / config-test space / short text
AI method + reason:     (why this method fits the data shape)
Baseline (current practice) + evidence link:
Metric(s):              
Negative result would mean:
Anti-generic tests:     engineer-substitution [pass/fail] · LLM-swap [pass/fail] · baseline [pass/fail]
Laptop feasibility guess (to be confirmed by the pilot):
Status / gate history:
```

### 3. Scoring rubric

Score each criterion from 1 to 5. **Hard gates are pass/fail:** failing any one means drop, regardless of the score.

**Hard gates:**
- combines SE, AI and OS;
- evidence of a practice problem (Stage 2 score ≥5);
- public data or benchmark available;
- laptop-feasible;
- no paid APIs;
- passes all anti-generic tests.

| Criterion | Weight | 1 (weak) | 3 (adequate) | 5 (strong) |
|---|---|---|---|---|
| Problem significance | 20% | Rare or cosmetic | Recurring, moderate cost | Recurring, high cost, many affected |
| Gap strength and novelty (see cap below) | 35% | Obvious prior work, or a difference of degree only | Partial prior work; a narrower question differs in kind | Structured search finds none; difference in kind from every closest work; reason for the gap supported by evidence |
| Measurability | 15% | No clear metric or baseline | Metric and baseline exist | Strong baselines, clear metric, ground truth |
| Feasibility for one student | 10% | Needs heavy maths or large compute | Some learning required | Fits current skills (C/C++/Python/SQL) and a laptop |
| Long-term relevance | 10% | Tied to one tool or model version | Relevant for a few years | Durable engineering problem |
| Venue fit | 10% | No clear venue | Workshop or regional venue fit | Clear fit at a solid IEEE venue |

Weights total 100%.

**Cap:** "Gap strength and novelty" cannot score above 3 until Stage 5 (both 5A and 5B) is complete.

**Double-scoring rule:** the student and the AI score independently. The AI scores in a **fresh chat** that receives **only the idea card and the rubric**, never the chat that drafted the ideas, which is anchored on its own reasoning. Differences of ≥2 points are discussed and resolved in writing.

### 4. Literature matrix (`literature_matrix.csv`)

| Field | Content |
|---|---|
| `id`, `citation`, `DOI/arXiv`, `verified (Y/N + date)` | Must pass the citation verification rule |
| `candidate` | Idea card ID (I-xxx) this entry was found for |
| `pass` | Stage 5A Pass 1 or Pass 2 |
| `evidence_tag` | read-full / read-abstract / secondary / AI-unverified |
| `access_route` | ACM DL, arXiv, author page, CORE, scholar.archive.org, Unpaywall, emailed author, etc. |
| `problem addressed` | |
| `data / subjects` | |
| `method` | |
| `baselines` | |
| `key findings` (with page numbers) | |
| `stated limitations` | |
| `found_via` | query ID, snowball round, venue sweep, tool search |
| `overlap with my RQ` | none / partial / full |
| `difference in kind` | One sentence, or "none" |

### 5. Gap statement (`gap_statement.md`)

```
Problem (with practice evidence):        [P-xxx; links]
Research question:                       
Closest prior work (all [read-full]):
  1. <verified citation> — does: …  — does not: …  — difference in kind: …
  2. …   (3–5 entries)
Why this gap exists (with evidence):     [new data / community gap / disproved assumption / …]
Search coverage:                         databases …; synonym table [link]; neighboring fields …;
                                         snowball rounds …; venue sweep …; tool search …; adversarial search …
Contribution (one sentence, measurable): 
Who benefits and how they would adopt it:
Strongest three objections + answers:    
Pilot evidence (fill after Stage 6):     [pilot_report.md summary + threshold met?]
Residual risk (unknown or in-progress work):
```

### 6. Search log (`search_log.csv`)

| Field | Content |
|---|---|
| `query_id` | Q-001 |
| `stage` | Stage 4 / Stage 5A Pass 1 / Stage 5A Pass 2 |
| `candidate` | Idea card ID (I-xxx) |
| `source` | OpenAlex, Semantic Scholar, arXiv, Google Scholar, dblp, scholar.archive.org, venue table of contents, GitHub, etc. |
| `query_string` | The exact string or filter, copied as run |
| `synonym_set` | Which synonym-table terms this query uses |
| `date` | Date the query was run |
| `hits` | Number of results returned |
| `screened` | Number of results whose title/abstract you checked |
| `kept` | Number added to the literature matrix |
| `kept_ids` | Literature-matrix IDs of the kept papers |
| `notes` | e.g., "zero hits: rephrased as Q-014" |

### 7. Claims register (`claims_register.md`)

**Purpose:** a running list of every factual claim the paper will make, each with its source, its evidence tag, and whether it has been verified. Nothing goes into the paper unless it is in this register and verified. Every claim behind a gap statement must be checked against its source; only claims with `supports = yes` may be used.

| Field | Content |
|---|---|
| `claim_id` | C-001 |
| `claim` | The claim, worded as it will appear in the paper |
| `type` | prior work / problem evidence / data or dataset fact / tool status / number or statistic |
| `source` | Verified citation or URL |
| `page` | Page, section or line in the source |
| `quote` | The exact sentence(s) in the source that support the claim |
| `supports` | yes / partial / no: does the quoted source really support the claim as worded? |
| `evidence_tag` | read-full / read-abstract / secondary / AI-unverified |
| `verified` | Y/N, date, and how (citation verifier, full text read, URL opened) |
| `used_in` | gap statement / paper section / decision record |
| `status` | keep / revise / remove |

### 8. Decision record (`decisions.md`)

```
## Gate log (append one line after every gate)
| date | stage | candidate (I-xxx or P-xxx) | outcome (proceed/reshape/drop) | reason |

## Final decision (Stage 8)
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

### 9. AI-use log (`ai_use_log.md`)

| Field | Content |
|---|---|
| `date` | Date of use |
| `stage` | Stage number |
| `tool_model` | AI tool and model/version (e.g., the assistant's name and model ID) |
| `task` | What you asked it to do |
| `output_type` | text / code / figure / search / analysis |
| `checked_or_changed` | What you verified or rewrote yourself |
| `used_in` | Where the output ended up (file, paper section) |

---

## Tests: research contribution vs. engineering tool vs. student project

Place each candidate on this ladder honestly. Only levels 3 and 4 should be selected.

1. **Student project:** builds or reproduces something that works. Passes none of the tests below.
2. **Engineering tool:** solves a practical need. May pass test G, but fails A or B.
3. **Research contribution:** passes A–F.
4. **Contribution with realistic publication potential:** passes A–G, *and* meets the evidence bar of the venue's calibration set (Stage 7).

**The tests:**
- **A. Knowledge test.** Does the work produce a claim others could cite *without using your code*? "We found that X causes Y in Z% of cases" passes. "We built tool T" fails.
- **B. Comparison test.** Is the result compared against a current-practice baseline and at least one trivial baseline, with a metric?
- **C. Falsifiability test.** Could the experiment have come out the other way? Was a success threshold set beforehand?
- **D. Difference-in-kind test.** Does the gap statement show a new question, data, finding or method property relative to the closest verified work, not just "better"?
- **E. Generalization test.** Does the result hold beyond one example: several projects, subsystems, time periods or datasets? Are the limits stated?
- **F. Validity test.** Are threats to validity identified and addressed? These include data leakage, label quality, selection bias and reproducibility.
- **G. Adoption test.** Can a named group realistically use the result (as guidance, a dataset, a technique or a CI check), and does the paper show how?

**Quick self-check before submission.** If you remove the tool from your paper, is there still a finding? If not, you have an engineering tool, not a research paper.

---

## Notes on sources whose status is uncertain
- **Verified reachable (November 2026):** OpenAlex (free key), arXiv, Crossref, scholar.archive.org, conf.researchr.org, the IEEE Computer Society Digital Library (tables of contents and abstracts), USENIX proceedings, OpenReview, NVD/CVE/OSV.
- **Free, but rate limits or key requirements may change:** Semantic Scholar (key pending; OpenAlex covers its role meanwhile), CORE (works without a key at a low rate limit), Unpaywall (contact email in requests), Scholar Sidekick (free tier).
- **Verify the current status yourself:**
  - IEEE's author-posting policy wording;
  - Stack Exchange data-dump availability;
  - registration requirements of I/O trace repositories.
- **Browser only (blocks scripts):** Google Scholar, IEEE Xplore abstract pages, and lore.kernel.org *web pages* (for scripts, use lore git clones; see `TOOLS.md`). dblp blocks scripts from some networks, so run `tools/verify_citation.py --dblp` from your own machine. Use browser-only sources manually, and log your queries the same way.
