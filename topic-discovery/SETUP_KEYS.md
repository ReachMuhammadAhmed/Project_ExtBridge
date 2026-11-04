# Stage 0: accounts, API keys and the test verification

Everything here is free. You create these accounts yourself; nobody else can create them for you.

## 1. Accounts and keys to create

| # | Service | Needed for | Where to sign up | Notes |
|---|---|---|---|---|
| 1 | **OpenAlex API key** | Stage 4 saturation counts; Stage 5A searches and citation chasing | Create an account at https://openalex.org, then copy the key from https://openalex.org/settings/api | Per the [official docs](https://developers.openalex.org/api-reference/authentication), a free key gives a daily usage budget; keyless calls get a much smaller one. Pass it as `api_key=YOUR_KEY` in requests. |
| 2 | **Semantic Scholar API key** | Stage 5A searches, citation graph, open-access PDF links | Request form: https://www.semanticscholar.org/product/api#api-key-form | Free, but approval is manual and can take a while. Without a key, requests are often rate-limited (HTTP 429). |
| 3 | **CORE API key** | Stage 5A: free full texts from university repositories | https://core.ac.uk/services/api (enter your email; the key is emailed to you) | Per the official page, the API also works without a key at a low rate limit. API docs: https://api.core.ac.uk/docs/v3 |
| 4 | **Zotero** (app + optional free account for sync) | Every stage: storing papers with DOIs | App: https://www.zotero.org/download/ · Account: https://www.zotero.org/user/register | The account is only needed to sync between devices. |
| 5 | **GitHub account** | Stage 2: GitHub code search (needs login); higher API limits | https://github.com/signup | Skip if you already have one. |

**Later, not needed for Stages 0–1:**
- An **OSF account** (https://osf.io) is optional, for pre-registration in Stages 6 and 8. A dated Git commit also works.
- A **Stack Exchange account** is needed only if you later download the data dump. The Stack Exchange API works without one.

**No account needed:** Crossref, DataCite and arXiv (used by `tools/verify_citation.py`). Crossref is "polite" if you add an email via `CROSSREF_MAILTO`.

## 2. Storing the keys safely

Keep keys out of Git. In the `topic-discovery/` folder, create a file named `.env` (already listed in `.gitignore`):

```
OPENALEX_API_KEY=your-openalex-key
SEMANTIC_SCHOLAR_API_KEY=your-s2-key
CORE_API_KEY=your-core-key
CROSSREF_MAILTO=your-email@example.com
```

Load it into your shell before running scripts:

```bash
set -a; source .env; set +a
```

Quick checks once the keys exist. Each should print `200`:

```bash
curl -s -o /dev/null -w "%{http_code}\n" "https://api.openalex.org/works?search=file%20system&per-page=1&api_key=$OPENALEX_API_KEY"
```

```bash
curl -s -o /dev/null -w "%{http_code}\n" -H "x-api-key: $SEMANTIC_SCHOLAR_API_KEY" "https://api.semanticscholar.org/graph/v1/paper/search?query=file%20system&limit=1"
```

```bash
curl -s -o /dev/null -w "%{http_code}\n" -H "Authorization: Bearer $CORE_API_KEY" "https://api.core.ac.uk/v3/search/works?q=file%20system&limit=1"
```

## 3. Test verification (Stage 0 exit criterion: you must run this yourself)

Pick **one paper you already know** (from a course or reading list). From the paper itself, take its DOI or arXiv ID, exact title, first author's family name and year. Then run:

```bash
python3 tools/verify_citation.py --id <DOI-or-arXiv-ID> --title "<exact title>" --authors "<FirstAuthorFamilyName>" --year <year> --venue "<journal or conference>"
```

Then do these two checks by hand:
1. The output ends with `=> VERIFIED`.
2. Open https://doi.org/<DOI> (or the arXiv page) in your browser and confirm that the title, authors, year and venue you typed match what you see.

Then run it once more with a deliberately wrong title, and confirm it prints `=> NOT VERIFIED`. Record both runs in `decisions.md` under the gate log as "Stage 0: test verification".

**Known limits of the script:**
- It compares family names only. Compound or transliterated names (e.g., "van der Berg", Chinese names in different orders) may need a manual check.
- arXiv records report the first-submission year, which can differ from the conference year. Use the venue's DOI when one exists.
- Many USENIX papers have no DOI. Verify those by hand against the USENIX proceedings page.
