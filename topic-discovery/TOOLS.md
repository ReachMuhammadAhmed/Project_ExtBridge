# Tools: stage, purpose, free terms, status

Every tool named in `methodology.md` is listed here. Free terms were checked against official pages on **2026-11-04**; terms change, so re-check before relying on a limit.

**Status values:**
- **configured:** ready in the current environment;
- **pending:** requested, not yet available;
- **to install:** you must install or set it up yourself;
- **no setup:** works in a browser or through the scripts as-is.

**Evidence of terms:**
- **official** = read on the official page;
- **official (excerpt)** = the official page blocks scripts, so it was confirmed from a search excerpt of that page.

Data *sources* (issue trackers, mailing lists, datasets) aren't tools; their licences and access are in `intersection_map.md`.

## Literature search, verification and access

| Tool | Stage(s) | Purpose | Free terms and limits | Status | Source |
|---|---|---|---|---|---|
| **Scholar Sidekick** | 0 → all (citation rule) | **Primary** citation check: `/api/verify` (verdict must be "matched") and `/api/retraction-check` before any paper enters the literature matrix; also `/api/oa-check` | Free. Anonymous: 60 requests/60 s; free key: 120 requests/60 s on the verify, retraction and open-access endpoints. Paid tiers only on RapidAPI. Official | configured (`SCHOLAR_API_KEY`) | https://scholar-sidekick.com/docs |
| `tools/verify_citation.py` | 0 → all | **Fallback** citation check (Crossref, DataCite, arXiv); `--dblp` for papers without a DOI or arXiv ID, which prints `[manual-check]` if dblp fails | Free, ours, standard library only | configured | `tools/verify_citation.py` |
| Crossref REST API | 0 (via script) | Metadata for DOIs | Free, no signup; public pool 5 req/s, "polite" pool (add `mailto`) 10 req/s. Official | no setup | https://www.crossref.org/documentation/retrieve-metadata/rest-api/access-and-authentication/ |
| DataCite REST API | 0 (via script) | Metadata for DataCite DOIs (arXiv, Zenodo) | Free reads; 500 requests/5 min per IP (1,000 with `mailto`). Official | no setup | https://support.datacite.org/docs/rate-limit |
| arXiv API | 0 (via script), 5A | Metadata and preprint search | Free; at most one request every 3 seconds, single connection. Official | no setup | https://info.arxiv.org/help/api/tou.html |
| dblp search API | 0 (citation rule, no-DOI papers), 5A | Look up papers without a DOI or arXiv ID | Free, non-profit service; metadata CC0 1.0; at most 1,000 hits per query. Official (excerpt). Blocks scripts from the research sandbox, so use it from your own machine or browser | no setup | https://dblp.org/faq/How+to+use+the+dblp+search+API.html · https://dblp.org/faq/1474677.html |
| OpenAlex API | 4, 5A | Search, citation chasing, saturation counts (also covers Semantic Scholar's role while that key is pending) | "Data is free, and so is casual use"; a free key raises the daily budget about 10×. Official | configured (`OPENALEX_API_KEY`) | https://developers.openalex.org/guides/authentication · https://developers.openalex.org/guides/pricing |
| Semantic Scholar API | 4, 5A | Search, citation graph, open-access PDF links | Free; unauthenticated calls share a pool and are often rate-limited; a free key starts at 1 request/s. Official | **pending** (key requested) | https://www.semanticscholar.org/product/api |
| CORE API | 5A | Full texts from university repositories | "Free and does not require registration, subject to our rate limits". Official | configured (used without a key) | https://core.ac.uk/services/api |
| Unpaywall API | 5A | Find legal open-access copies | Free; an email parameter is required on every call. Official (the email rule was confirmed by the API's own error) | no setup | https://unpaywall.org/products/api |
| scholar.archive.org | 5A | Full-text search of archived papers | Free, non-profit, open API, run by the Internet Archive; rate-limits heavy use. Official (excerpt) | no setup | https://blog.archive.org/2021/03/09/search-scholarly-materials-preserved-in-the-internet-archive/ |
| Google Scholar | 4, 5A | Broad recall; "Cited by" for forward snowballing | Free web search; no official API; `robots.txt` disallows `/search` and `/scholar`, so **browser only**. Official (robots.txt) | no setup (browser) | https://scholar.google.com/robots.txt |
| **Inciteful** | 5A (Pass 1 snowballing; Pass 2 neighbouring fields) | Citation-network exploration around seed papers | "100% Free to use. Our core tools are free to use and always will be." Official (rendered site; inciteful.xyz redirects to incitefulmed.com/academic) | no setup (browser) | https://incitefulmed.com/academic/ |
| **Undermind** | 5A Pass 2 step 5 only (adversarial search, top 2 candidates) | Deep search for the paper that would scoop your gap | Free plan ($0) with "standard rate limits on chats and searches". The exact monthly count isn't published, so use it sparingly. Results go through the citation rule. Official | to install (free account) | https://www.undermind.ai/pricing |
| **arXiv email alerts** | 5A onward | Daily new-paper listings for cs.SE and cs.OS | Free; no arXiv account needed (subscribe by email, as described on the help page). Official | to install (subscribe) | https://info.arxiv.org/help/subscribe.html |
| ACM Digital Library | 5A, 7 | Read ACM papers | Fully open access since 1 Jan 2026 (Basic edition). Official | no setup (browser) | https://www.acm.org/articles/bulletins/2026/january/acm-open-access |
| conf.researchr.org | 5A, 7 | Accepted-paper lists for SE conferences | Free public site (reachable from here) | no setup | https://conf.researchr.org/ |
| IEEE Computer Society Digital Library | 5A, 7 | Tables of contents and abstracts | Tables of contents and abstracts free (reachable from here); full texts often paywalled | no setup | https://www.computer.org/csdl/home |
| USENIX proceedings | 5A, 7 | Free full texts of USENIX papers | Free open-access proceedings (reachable from here) | no setup | https://www.usenix.org/publications/proceedings |
| Zotero | 0 → all | Store papers with DOIs | Free app; free sync storage 300 MB. Official | to install | https://www.zotero.org/storage |

## Data collection and analysis

| Tool | Stage(s) | Purpose | Free terms and limits | Status | Source |
|---|---|---|---|---|---|
| **lore.kernel.org git clones** | 1, 2 | Kernel mailing lists as git repositories (web pages block scripts; git works). Clone **one list, one epoch at a time**: `git clone https://lore.kernel.org/<list>/git/<N>.git` | Free public archive. Epochs on 2026-11-04: linux-ext4 0, linux-block 0, oe-lkp 0, linux-fsdevel 0–1, kvm 0–1, linux-mm 0–2, dri-devel 0–2, lkml 0–20. Even blob-free clones are about 0.3–1.1 GB per epoch. Verified by `git ls-remote` and clones | to install (git) | https://lore.kernel.org/ |
| **PyDriller** | 2 (frequency counts, filtered by subsystem path such as `fs/ext4/`), 6 (pilot) | Mine commit history from git repositories | Apache-2.0; `pip install pydriller` (v2.12 on PyPI). Official | to install | https://pypi.org/project/PyDriller/ |
| pandas, scikit-learn | 6 | Data handling and ML for the pilot | BSD-3-Clause (PyPI metadata). Official | to install | https://pypi.org/project/pandas/ · https://pypi.org/project/scikit-learn/ |
| GitHub account | 2 | Code search (needs login), higher API limits | Free account; "you must be logged in … to use code search". Official | to install (if you lack one) | https://docs.github.com/en/search-github/github-code-search/about-github-code-search |
| llama.cpp / Ollama (optional) | 0, 3 | Small local language model, only where text understanding is unavoidable | Both MIT-licensed, free local software. Official licence files | optional | https://github.com/ggml-org/llama.cpp · https://github.com/ollama/ollama |
| OSF (optional) | 6, 8 | Dated pre-registration (a dated Git commit also works) | "A free, open-source platform… register study plans". Official | optional | https://www.cos.io/products/osf |

## Venue selection (Stage 7)

| Tool | Stage | Purpose | Free terms and limits | Status | Source |
|---|---|---|---|---|---|
| **ICORE conference portal** | 7 | Venue tier lookup (current edition ICORE2026) | Free search; login optional. Official | no setup | https://portal.core.edu.au/conf-ranks/ |
| **se-deadlines** | 7 | SE conference deadlines (iCal export) | Free community site, updated by pull request. Official. **The official call for papers stays authoritative** | no setup | https://se-deadlines.github.io |
| ACM SIGSOFT Empirical Standards | 7 | Reviewer checklists per paper type | Public, CC0. Official | no setup | https://github.com/acmsigsoft/EmpiricalStandards |

## Policy reference

| Item | Stage | What it requires | Source |
|---|---|---|---|
| IEEE AI-disclosure policy | 8 (and `ai_use_log.md` throughout) | AI-generated content (text, figures, images, code) must be disclosed in the **acknowledgments section**, naming the AI system and the sections that use it, with a brief explanation of the level of use. Editing/grammar help: disclosure recommended, not required. Individual conferences may be stricter. Official | https://journals.ieeeauthorcenter.ieee.org/become-an-ieee-journal-author/publishing-ethics/guidelines-and-policies/submission-and-peer-review-policies/ |

## Deliberately not used
Papers with Code (shut down), Connected Papers, Litmaps, ResearchRabbit, Elicit, Consensus and scite are not part of this methodology.
