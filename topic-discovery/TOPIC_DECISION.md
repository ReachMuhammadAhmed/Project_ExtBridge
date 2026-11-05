# Topic decision

Written 2026-11-05 (UTC) for Ahmed.
- Every fact here comes from a source that was opened, or from a script committed in `tools/probes/` (outputs in `probes_output/`).
- Quotes are verbatim, hedges included. Anything not checked is marked as such.
- Supporting records: `problem_log.csv`, `claims_register.md` (C-001 to C-018), `literature_matrix.csv` (L-001 to L-034), `search_log.csv` (Q-001 to Q-231), `decisions.md`, `idea_cards/`.

**Decision: option A, I-001, reshaped after the red-team.**
- It ranked first in both independent scorings (4.00 of 5 from this session and 4.00 from a fresh reviewer; 3.65 with the gap criterion capped).
- No paper or tool answering its questions was found in either search pass or by the red-team reviewer.
- **Fallback:** option C, I-003, on unresolved kernel regressions in regzbot data.

---

## 1. The chosen topic

**Working title:** *When nobody triages the robot: an empirical study of what happens to the Linux kernel test robot's performance-regression reports*

### The problem, in practitioners' words

Intel's kernel test robot (0-day CI / LKP) runs benchmarks on kernel trees. When a result changes, it bisects to a culprit commit and e-mails the patch author a report, for example "stress-ng.signest.ops_per_sec 4.1% regression". Developers repeatedly say that many of these reports are noise, or blame a commit that has nothing to do with the benchmark:

| Year | Who | Quote | Link |
|---|---|---|---|
| 2021 | robot team, LPC talk | "0day bot has reported many strange kernel performance changes that the bisected culprit commits have nothing to do with the benchmark, which make patch authors confused or even annoyed." | https://lpc.events/event/11/contributions/895/ |
| 2021 | patch author replying to a report | "the data is very noisy, so I'm not sure I can confirm it." | https://lkml.iu.edu/hypermail/linux/kernel/2105.1/03332.html |
| 2024 | developer replying to a report | "This _looks_ like noise to me. Some benchmarks went up, some went down." | https://lkml.iu.edu/hypermail/linux/kernel/2403.0/03148.html |
| 2017 | robot operator | "A great portion of them may also be random noises (eg. performance fluctuations)." | https://lkml.iu.edu/hypermail/linux/kernel/1703.1/00436.html |

Nobody triages between the robot and the author. The robot's FAQ says "you are not obliged to respond to a robot" (lkp-tests `doc/faq.md`). By contrast, Mozilla and MongoDB, where performance-alert triage has been studied, run alerts through an in-house triage workflow.

### What the public archive shows

All of this is script output in `probes_output/`.

- **Coverage:** the archive holds 979 robot performance-regression reports from 2016 to 2026.
- **Acted on:** only 73 (7.5%) are cited by a mainline fix or revert commit.
- **No reply:** 569 (58%) got no human reply.
- **Analysis window (2020 onward):** 626 reports, 68 cited by a fix or revert, and 292 threads with human replies.
- **Report contents:**
  - 1,664 of 1,728 performance reports name a blamed commit.
  - 1,674 include a %stddev table.
  - 1,398 include perf-profile lines.

### Research questions (reshaped)

RQ1 and RQ2 are the core; RQ3 is secondary.

| | Research question | Form |
|---|---|---|
| **RQ1** | In 2020–2026, what share of the robot's performance-regression reports are: acted on (fixed, reverted, or the blamed patch changed or dropped); disputed (noise, misattribution, accepted trade-off); acknowledged without action; or ignored? How does this compare with the published alert outcomes of a triaged setting (Mozilla: 56.3% true, 12.5% false, 31.2% uncertain alert summaries, Besbes et al.)? | characterise / compare |
| **RQ2** | Which evidence available when a report is sent goes with each outcome? Candidates: the change relative to its %stddev; the number of benchmarks and metrics affected; the benchmark family; the tested branch; whether the perf profile names functions the blamed commit changed. Do the reasons developers give for disputing a report (noise, alignment, an unrelated commit) match that evidence? | explain |
| **RQ3** (secondary, pre-registered) | Does an interpretable classical ranker over that evidence put acted-on reports first, compared with these baselines: the robot's own gates and order; \|%change\|; %change ÷ %stddev; a Mozilla-style feature set (after Hmissa et al. 2026)? | prioritise (replication-extension) |

### Data

- The oe-lkp public-inbox archive (`git clone https://lore.kernel.org/oe-lkp/git/0.git`): 709 MB, 20,537 messages.
- Mainline kernel and linux-next history, cloned from git.kernel.org. This keeps GitHub's research-use clause off the data path; see `decisions.md`, open constraints.
- All free, and it fits on a laptop.

### Labels

Two independent routes, so that the red-team's label-bias objection can be measured:
1. **Tag-based:** a mainline commit cites the report's Message-ID in `Closes:`/`Link:`, or reverts the blamed commit. So far 68 reports in 2020+ (a lower bound).
2. **Code-based:** a later commit changes the hunks the blamed commit touched, or the blamed development-branch patch never reaches mainline or reaches it in a changed version. A first probe found 43 of 168 parsed development-branch reports whose patch never reached mainline; each needs a manual check.

Then:
- You hand-code the reply threads with a written codebook: acted-on, disputed (noise / misattribution / trade-off), acknowledged, no response.
- A stratified hand-check of "ignored" reports estimates how many of those labels are wrong.
- The keyword probe shows dispute wording in a minority of threads: noise 5%, alignment 4%, "cannot reproduce" 4%.

### Method

1. Parse every report into a table.
2. Link reports to commits by Message-ID, by revert, and by patch identity.
3. Code the threads.
4. Analyse:
   - RQ1: proportions with 95% CIs, and a comparison with the Mozilla shares.
   - RQ2: effect sizes (odds ratios, Mann–Whitney r) and logistic regression.
   - RQ3: logistic regression and gradient-boosted trees, explained with coefficients or SHAP. Train on reports up to mid-2024 and test on later ones; the test set has 24 positives.

No LLM is used. The data is labelled numeric tables, so classical ML is the fitting family.

### Baselines

1. The robot's own gates and order. Its `lib/stats.rb` only mails changes that pass fixed checks, such as `return true unless ratio > 1.01` and `return true unless ratio > 1.05 || perf_metric?(k)`.
2. Rank by \|%change\|.
3. Rank by %change ÷ %stddev.
4. The rule "the perf profile names a function the commit changed".
5. A Mozilla-style feature set.

### Metrics

- RQ1: shares with CIs.
- RQ2: effect sizes with CIs.
- RQ3: AUC-PR and recall@k pooled over the test period, with bootstrap CIs against each baseline, plus a power estimate written before running.

### Contribution, ladder placement and topic fit

**Contribution type:**
- An empirical repository-mining study with a new outcome-labelled dataset (RQ1, RQ2).
- A small replication-extension of performance-alert triage (RQ3).

**Ladder placement:** a research contribution. It passes the knowledge test, because RQ1 and RQ2 give citable findings with no tool involved. Whether it meets an IEEE venue's evidence bar is checked in Phase 6. The red-team's warning: with the ranker as the headline, the paper would be closer to a student project. That is why RQ3 is secondary.

**How it combines SE, AI and OS:**
- **OS:** kernel performance across scheduler, memory, file-system and locking benchmarks.
- **SE:** continuous-integration regression triage and repository mining.
- **AI:** a classical ML ranker, chosen to fit the shape of the data.

---

## 2. Gap statement and red-team

### Closest works and the difference from each

About 230 queries were logged across Pass 1, Pass 2 and the red-team.

| # | Closest work (evidence tag) | What it does | Difference in kind |
|---|---|---|---|
| 1 | Hmissa et al., *Performance Alert Triage with Time-Aware Learning and Multi-Scale Time-Series Features*, ICPE 2026 Companion, doi:10.1145/3777911.3800694 [read-abstract] | Predicts "whether an aggregated Mozilla performance alert summary is associated with a reported bug"; test AUPRC 0.851 | **New setting and data:** e-mailed reports with one bisected culprit, sent straight to the author, with no triage step. **New outcomes:** acted-on, disputed, ignored, patch changed or dropped, where Mozilla has only "bug filed". **New evidence:** overlap between the culprit and the perf profile. RQ3 transfers this idea and is claimed only as replication-extension. |
| 2 | Chen et al., ICPE 2022 Companion, doi:10.1145/3491204.3527487, and SCP 2024, doi:10.1016/j.scico.2023.103068; Bauer et al., ICPE 2022 Companion, doi:10.1145/3491204.3527486 [read-abstract] | Classify MongoDB change points as real or spurious before triage | They detect before any report exists. **New question:** what happens after a report reaches developers. |
| 3 | Besbes et al., Mozilla alert dataset, arXiv:2503.16332, and change-point study, arXiv:2606.18377 [read-full by a helper] | 3,912 alert summaries; compare change-point detectors | They don't explain or predict action on alerts, and don't cover the kernel. Their shares are used as RQ1's contrast. |
| 4 | Tian et al., *Characterizing and Mitigating False-Positive Bug Reports in the Linux Kernel*, FSE 2026, doi:10.1145/3797082 [read-full by a helper] | 2,006 Bugzilla and syzbot reports; LLM detection of false positives | **Different report type** (no performance reports), **evidence** (no numeric effect sizes or profiles) and **outcome** |
| 5 | Bursey et al., *SyzRetrospector*, RAID 2025, doi:10.1109/RAID67961.2025.00033; Ding & Le Goues, *An Empirical Study of OSS-Fuzz Bugs*, MSR 2021, doi:10.1109/MSR52588.2021.00026 [secondary / title-level] | Outcomes of bug reports filed by bots (fuzzers) | They cover crash bugs held in trackers, not statistical performance changes mailed to authors. **New evidence type** (noisy measurements) and **new outcome** (disputed as noise). |

Also screened, with no overlap on the research questions: Daly et al. ICPE 2020 (change-point detection in MongoDB CI); Ruohonen & Alami 2024 (regzbot fixing times); Asthana et al. FSE 2023 (developer perceptions of bots).

**Unread residual risk:** Huang et al., *Demystifying performance bugs in large-scale infrastructure software … in the Linux kernel*, JSS 2026, doi:10.1016/j.jss.2026.112996. No abstract or PDF was reachable. The title suggests a study of bugs and patches rather than robot reports, but this is unverified.

### Why the gap exists

1. **The outcome labels only recently became observable.** Mainline commits that credit the robot carry a lore `Link:`/`Closes:` tag in 0 of 17 cases in 2016, 237 of 589 in 2020, and 442 of 457 in 2026 (`probes_output/A_robot_tags.txt`).
2. **The communities don't overlap.** Performance-alert triage is studied at ICPE on industrial CI (Mozilla, MongoDB). Kernel repository mining studies bug reports, syzbot and regzbot. OpenAlex returned no paper that names LKP or will-it-scale.

### Search coverage

| Step | What was done |
|---|---|
| Databases | OpenAlex, arXiv, Crossref, Semantic Scholar, Undermind (search only). Scholar Feed returned HTTP 503 throughout. |
| Terminology | Synonym sets |
| Neighbouring fields | Browsers, databases, compilers, JVM, cloud |
| Snowballing | Forward, two rounds, until saturation |
| Venue sweep | ICPE, MSR, ICSME, ISSRE 2023–2026, via OpenAlex source filters |
| Tool search | lkp-tests, KernelCI |
| Adversarial search | An adversarial abstract, searched in its own wording |

### 2a. Red-team result

Done by a fresh reviewer (Opus, high effort) that saw only the card and this gap statement. **Verdict: "reshape, then proceed"**; none of the objections is fatal.

| # | Objection (as ranked by the reviewer) | Status | Answer |
|---|---|---|---|
| O1 | The "acted-on" label is a lower bound whose recall changes with the year, because tagging went from 0/17 to 442/457. Trends and time-varying features could reflect tagging habits rather than developers' choices. | fixed in the design | The main window is now 2020+. A second, code-based outcome route is added. A stratified hand-check of "ignored" reports measures label error. A second coder codes about 20% of threads, and Cohen's κ is reported. |
| O2 | The novelty is a new setting, which a reviewer may call a difference of degree; bot-report outcome studies exist (syzbot, OSS-Fuzz). | answered by reframing | The claim is now explicitly a contrast: evidence about what happens to performance reports when no triage role exists. Mozilla shares are compared directly (RQ1), and syzbot and OSS-Fuzz are positioned in row 5 of the table above. |
| O3 | RQ3 has too few positives (24 in the test period) and the AI part is thin. | accepted as a limitation | RQ3 is now secondary and pre-registered, with a power estimate. Metrics are pooled over the test period, not taken per month. |

**Missed prior work:** the reviewer found no paper on outcomes of 0-day/LKP performance reports. It added SyzRetrospector, OSS-Fuzz (MSR 2021) and developer bots (FSE 2023); all three are now in the matrix as L-026, L-033 and L-034 and verified with Scholar Sidekick.

**Novelty calibration:**
- Kernel CI and test-robot maintainers would cite this paper, as would performance-triage researchers at ICPE and MSR who need a non-industrial, no-triage contrast.
- A Mozilla-triage reviewer would ask for a direct comparison of outcome shares, which RQ1 now includes.

---

## 3. All options compared

The scores are weighted rubric totals from two independent scorings: this session, and a fresh reviewer who saw only the cards and the rubric. No criterion differed by more than 1 point between the two.

| Option | Practice evidence (Stage 2 score) | Data and labels (probe) | Closest prior work | Score: this session / independent (independent with gap capped at 3) | Ladder | Outcome and reason |
|---|---|---|---|---|---|---|
| **A, I-001: robot performance reports** | 4 independent items 2017–2024 plus the robot FAQ (10): P-001 | 979 regression reports (626 since 2020); 68–73 tag-linked; 292–410 threads to code | Hmissa ICPE'26, Chen and Bauer ICPE'22, Tian FSE'26 (all partial) | **4.00 / 4.00 (3.65)** | research contribution | **Chosen.** Strongest and most independent practice evidence; unique data; a difference in kind for RQ1 and RQ2 |
| C, I-003: unresolved regressions in regzbot | 3 items, all from one person (5): P-003 | 2,186 resolved and 287 inconclusive regressions; the outcome is recorded by the tracker | Ruohonen & Alami 2024 ("Only resolved regression bugs were included in the dataset."); Xiao TR 2020; Gu FSE-C 2024 | 3.65 / 3.70 (3.35) | research contribution | **Fallback.** Real gap, but practice evidence only at the threshold, a thin AI part, and dependence on one tracker run by one person whose funding is uncertain (https://lwn.net/Articles/990599/) |
| D, I-004: missing links from regression reports to fixes | 2 items (6): P-004 | About 490 automatic links versus about 1,562 manual "fix:" commands (heuristic) | Mature issue-commit link-recovery field: Bachmann FSE'10, DeepLink SANER'19, EALink ASE'23, PaStA ICSE'19 | 2.90 / 2.90 | engineering tool | **Not pursued.** Known technique on a new dataset (difference in degree); fails the engineer-substitution test |
| B, I-002: duplicate robot reports | 3 items, two about syzbot (7): P-002 | Only 226 of 6,517 blamed commits got more than one report; no duplicate labels | Mu et al. NDSS 2022 (kernel duplicates) | 2.50 / 2.20 | engineering tool | **Dropped.** Fails the engineer-substitution test, because the robot already groups tests per commit; difference in degree |

The full per-criterion scores are in `decisions.md` (Stage 4 double scoring) and in each card's file.

---

## 4. Top risks, kill criteria and fallbacks

| # | Risk | Kill or reshape criterion (checked at) | Fallback |
|---|---|---|---|
| R1 | **Labels too sparse or unreliable.** Silent fixes, and a single coder. | After Phase 2: fewer than 60 reports in 2020+ have a definite acted-on outcome from either route, **or** Cohen's κ < 0.6 after one revision of the codebook. | If κ is fine but positives are few: drop RQ3 and publish RQ1 and RQ2 as a short paper. If κ < 0.6: switch to **I-003**. |
| R2 | **Scooped.** Huang JSS 2026, or a new paper, already studies the outcomes of 0-day/LKP reports. | Phase 0: read Huang et al. and rerun the adversarial query. Kill if a paper reports outcome shares for robot performance reports. | Narrow to RQ2's kernel-specific evidence (profile overlap, misattribution), or switch to **I-003**. |
| R3 | **RQ3 shows nothing.** | Pre-registered: the ranker must beat the best baseline on pooled test AUC-PR by ≥ 0.05, with a 95% bootstrap CI excluding 0. | Not a kill. Report a negative result; the paper stands on RQ1 and RQ2. |
| R4 | **The archive is incomplete.** Private reports exist ("a private report or tree", robot FAQ); some reports may only be on LKML. | Phase 1: spot-check 30 robot reports found in an LKML clone. If more than 20% of 2020+ performance reports are missing from oe-lkp, add LKML epochs as a second source. | Add the LKML clone (about 1 GB per epoch) and state the selection bias. |
| R5 | **Terms of use.** lore.kernel.org states no reuse licence; the regzbot fallback has none either. | Kill only if a stated term forbids research mining. | Publish only aggregates, Message-IDs and numeric fields, never names or e-mails. |
| R6 | **The profile-overlap feature is infeasible.** It was not demonstrated here: lazy tree fetch took more than 300 s per commit. | Phase 1: if fewer than 70% of blamed commits can be resolved to a diff locally. | Drop that feature; it is one feature, not the study. |

---

## 5. How to proceed

There is no timeline constraint. The venue dates are real, though.

**Primary target: IEEE ICSME 2027.** Research track paper deadline Fri 5 Mar 2027 (https://conf.researchr.org/home/icsme-2027). Its Visions and Emerging Results track was 5 + 1 pages, double-anonymous, in 2026 (https://conf.researchr.org/track/icsme-2026/icsme-2026-nier); the 2027 date is not yet published.

**Secondary target: MSR 2028.** The MSR 2027 deadline (23 Oct 2026) has passed. Its call allows arXiv preprints under a different title (https://conf.researchr.org/track/msr-2027/msr-2027-technical-papers).

Check sponsorship on the official pages before choosing.

**Model abbreviations used in the table:**
- **Opus-H** = Claude Opus 5.5 at high effort (design, statistics review, critique).
- **Sonnet-M** = Claude Sonnet 5.5 at medium effort (scripts, parsing, data plumbing).
- **You** = steps that are your measurement or your judgement.

| Phase | Deliverable | Done when | Who / model |
|---|---|---|---|
| **0. Pre-registration and final prior-work check** | `preregistration.md` holding the RQs, label definitions, codebook v1, time split, RQ3 threshold and power estimate, and kill criteria R1–R6, committed with a date. Huang JSS 2026 requested from its authors and read. | The commit exists before any labelling. Huang et al. has been read, or 4 weeks have passed with no reply (then logged). | Opus-H drafts; **you** approve and send the e-mail |
| **1. Dataset build** | Parser covering every report format 2016–2026, including the 644 development-branch subjects not yet parsed. Linker: Message-ID tags, reverts, patch-id / subject match against mainline and linux-next, later commits touching the blamed hunks. Feature table. Archive-coverage spot-check (R4). | At least 95% of 2020+ reports parsed. A manual check of 50 random reports shows the parsed fields correct. The R4 and R6 checks are logged. | Sonnet-M writes the code, Opus-H reviews it; **you** do the 50-report check |
| **2. Labelling** | Codebook. All 292 post-2020 threads (410 overall) coded. 60 threads re-coded at least 2 weeks later. A classmate codes 60 threads. A stratified hand-check of 50 "ignored" reports. | κ ≥ 0.6, or the R1 decision is logged | **You.** AI may only build the coding spreadsheet; no AI labels |
| **3. RQ1 and RQ2 analysis** | Committed scripts and tables: outcome shares with CIs, the Mozilla contrast, effect sizes, logistic regression, the dispute-reason analysis | Every number in the draft comes from a committed script (checklist item 12) | Sonnet-M scripts; Opus-H statistics review; **you** run them |
| **4. RQ3 pilot (Stage 6)** | `pilot_report.md`: baselines, ranker, pooled time-split results, leakage checks (features available at report time only) | Pre-registered threshold met or not met, recorded as either | Sonnet-M; Opus-H reviews for leakage; **you** run |
| **5. Validity and generalisation** | Results by subsystem, benchmark family and year. Sensitivity to the two label routes. Threats-to-validity section. | Every threat in R1–R6 has a measured answer or is stated as a limitation | Opus-H drafts; **you** decide |
| **6. Venue dossier (Stage 7)** | `venue_dossier.md`: 5–10 calibration papers from ICSME/MSR 2023–2026, the ACM SIGSOFT Empirical Standards Repository Mining checklist, the top 5 reviewer objections | Gap-to-bar list closed or the track adjusted | Sonnet-M gathers; Opus-H analyses; **you** read 3 calibration papers |
| **7. Writing and replication package** | Paper draft; Zenodo archive with a DOI containing the scripts and derived dataset (Message-IDs, numbers, labels; no names or e-mails); IEEE AI-use acknowledgement drafted from `ai_use_log.md` | Claims register fully "supports = yes"; all 15 checklist items pass | **You** write the text; Opus-H critiques |
| **8. Submit** | ICSME 2027 submission (or MSR 2028) | Submitted | **You** |

---

## 6. What you must do yourself

Only the steps that can't be delegated:
1. **Accept this decision** or name the fallback, in one line in `decisions.md`.
2. **Send one e-mail** asking Huang et al. for the JSS 2026 PDF. Also read Hmissa et al. in full in your browser (ACM DL is open access).
3. **Code the reply threads** using the codebook: 292 threads, about 15–25 hours. Re-code 60 of them two weeks later, and ask one classmate to code 60. This is the study's measurement, so an AI must not do it; letting an AI label them would also turn this into an LLM study.
4. **Run the committed scripts once on your laptop**, so you can vouch for every number (methodology Stage 6, "AI vs. you"). Check the 50-report parse sample.
5. **Confirm the venue on its official page in a browser:** ICSME 2027 sponsorship, the call for papers, and the track. Then choose the track.
6. **Write the paper text yourself**, approve the AI-use acknowledgement, and submit.

Everything else can run on the models named in §5.
