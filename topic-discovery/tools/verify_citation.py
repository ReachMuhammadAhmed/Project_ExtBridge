#!/usr/bin/env python3
"""Apply the methodology's citation verification rule (Stage 0).

A reference may be used only after:
  1. its DOI (or arXiv ID) resolves (Crossref, DataCite or arXiv) -- or, for a paper with neither,
     its dblp record (--dblp) or official proceedings page is found;
  2. the title, authors, year and venue ALL match that record; and
  3. it has not been retracted (check with Scholar Sidekick, the primary tool; this script is the fallback).

This script checks title, authors and year automatically, and venue when you
pass --venue. It uses only the Python standard library and free APIs:
  - Crossref   https://api.crossref.org/works/{doi}        (most journal/conference DOIs)
  - DataCite   https://api.datacite.org/dois/{doi}          (arXiv DOIs 10.48550/..., Zenodo, etc.)
  - arXiv      https://export.arxiv.org/api/query?id_list=  (arXiv IDs)

Usage examples:
  python3 verify_citation.py --id 10.1038/nphys1170 --title "Measured measurement" \
      --authors "Aspelmeyer" --year 2009
  python3 verify_citation.py --id arXiv:2409.04109 \
      --title "Can LLMs Generate Novel Research Ideas?" --authors "Si; Yang; Hashimoto" --year 2024

--authors takes family names separated by ';' (first author first). You may list
only some authors (e.g., the first one), but every name you list must appear in
the record, and the first name you list must be the record's first author.

Optional: set CROSSREF_MAILTO=<your email> to use Crossref's "polite" pool.
Papers with no DOI or arXiv ID: use --dblp (title search on dblp). If dblp has no match or is
unreachable, the script prints [manual-check]: verify against the official proceedings page.

Exit code: 0 = VERIFIED, 1 = NOT VERIFIED, 2 = record not found / error, 3 = [manual-check] needed.
"""
import argparse
import difflib
import json
import os
import re
import sys
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

TITLE_THRESHOLD = 0.90  # similarity needed after normalisation (handles punctuation/case)
UA = "citation-verifier/1.0 (student research tool; stdlib urllib)"


def norm(text):
    text = unicodedata.normalize("NFKD", text or "")
    text = "".join(c for c in text if not unicodedata.combining(c))
    text = re.sub(r"<[^>]+>", " ", text)          # strip markup (Crossref titles may contain <i> etc.)
    text = re.sub(r"[^a-z0-9]+", " ", text.lower())
    return " ".join(text.split())


def fetch(url, accept="application/json"):
    headers = {"User-Agent": UA, "Accept": accept}
    with urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=30) as r:
        return r.read()


def classify_id(raw):
    s = raw.strip()
    s = re.sub(r"^(https?://)?(dx\.)?doi\.org/", "", s, flags=re.I)
    s = re.sub(r"^doi:\s*", "", s, flags=re.I)
    s = re.sub(r"^(https?://)?arxiv\.org/(abs|pdf)/", "", s, flags=re.I)
    s = re.sub(r"\.pdf$", "", s, flags=re.I)
    s = re.sub(r"^arxiv:\s*", "", s, flags=re.I)
    m = re.match(r"^10\.48550/arxiv\.(.+)$", s, flags=re.I)
    if m:
        return "arxiv", m.group(1)
    if re.match(r"^\d{4}\.\d{4,5}(v\d+)?$", s) or re.match(r"^[a-z\-]+(\.[A-Z]{2})?/\d{7}(v\d+)?$", s):
        return "arxiv", s
    if s.startswith("10."):
        return "doi", s
    raise ValueError(f"Not a recognisable DOI or arXiv ID: {raw!r}")


def record_from_crossref(doi):
    url = "https://api.crossref.org/works/" + urllib.parse.quote(doi)
    mailto = os.environ.get("CROSSREF_MAILTO")
    if mailto:
        url += "?mailto=" + urllib.parse.quote(mailto)
    msg = json.loads(fetch(url))["message"]
    years = set()
    for key in ("published-print", "published-online", "issued", "published"):
        parts = (msg.get(key) or {}).get("date-parts") or []
        if parts and parts[0] and parts[0][0]:
            years.add(int(parts[0][0]))
    return {
        "source": "Crossref",
        "title": " ".join(msg.get("title") or []),
        "authors": [a.get("family") or a.get("name") or "" for a in msg.get("author", [])],
        "years": years,
        "venue": " | ".join(v for v in (msg.get("container-title") or []) + [(msg.get("event") or {}).get("name", "")] if v),
    }


def record_from_datacite(doi):
    data = json.loads(fetch("https://api.datacite.org/dois/" + urllib.parse.quote(doi)))["data"]["attributes"]
    return {
        "source": "DataCite",
        "title": " ".join(t.get("title", "") for t in data.get("titles", [])[:1]),
        "authors": [c.get("familyName") or c.get("name", "").split(",")[0] for c in data.get("creators", [])],
        "years": {int(data["publicationYear"])} if data.get("publicationYear") else set(),
        "venue": data.get("publisher") if isinstance(data.get("publisher"), str) else (data.get("publisher") or {}).get("name", ""),
    }


def record_from_arxiv(aid):
    xml = fetch("https://export.arxiv.org/api/query?id_list=" + urllib.parse.quote(aid), accept="application/atom+xml")
    ns = {"a": "http://www.w3.org/2005/Atom", "arxiv": "http://arxiv.org/schemas/atom"}
    entry = ET.fromstring(xml).find("a:entry", ns)
    if entry is None or entry.find("a:title", ns) is None or (entry.find("a:id", ns).text or "").endswith("/api/errors"):
        raise LookupError("arXiv returned no entry for this ID")
    names = [a.find("a:name", ns).text for a in entry.findall("a:author", ns)]
    journal = entry.find("arxiv:journal_ref", ns)
    return {
        "source": "arXiv",
        "title": entry.find("a:title", ns).text,
        "authors": [n.split()[-1] for n in names],  # family name = last token (check manually for compound names)
        "years": {int(entry.find("a:published", ns).text[:4])},
        "venue": "arXiv" + (f" | journal_ref: {journal.text}" if journal is not None else ""),
    }


def record_from_dblp(title):
    """Search dblp by title (for papers with no DOI or arXiv ID). Returns the best-matching record."""
    url = "https://dblp.org/search/publ/api?" + urllib.parse.urlencode({"q": title, "format": "json", "h": 10})
    data = json.loads(fetch(url))  # raises ValueError (JSONDecodeError) if dblp returns an anti-bot HTML page
    hits = ((data.get("result") or {}).get("hits") or {}).get("hit") or []
    if not hits:
        raise LookupError("dblp returned no match for this title")
    best = max(hits, key=lambda h: difflib.SequenceMatcher(None, norm(title), norm(h["info"].get("title", ""))).ratio())
    info = best["info"]
    authors = (info.get("authors") or {}).get("author") or []
    if isinstance(authors, dict):
        authors = [authors]
    names = [re.sub(r"\s+\d{4}$", "", a.get("text", "")) for a in authors]  # dblp disambiguation suffix, e.g. "Jane Doe 0001"
    return {
        "source": "dblp",
        "title": info.get("title", ""),
        "authors": [n.split()[-1] for n in names if n],
        "years": {int(info["year"])} if info.get("year") else set(),
        "venue": info.get("venue", "") if isinstance(info.get("venue"), str) else " | ".join(info.get("venue") or []),
    }


def lookup(raw_id):
    kind, ident = classify_id(raw_id)
    if kind == "arxiv":
        return record_from_arxiv(ident)
    try:
        return record_from_crossref(ident)
    except urllib.error.HTTPError as e:
        if e.code != 404:
            raise
    return record_from_datacite(ident)  # DOIs not registered with Crossref (e.g., Zenodo)


def check(rec, title, authors, year, venue):
    results = {}
    sim = difflib.SequenceMatcher(None, norm(title), norm(rec["title"])).ratio()
    results["title"] = (sim >= TITLE_THRESHOLD, f"similarity {sim:.2f} (need {TITLE_THRESHOLD})")

    claimed = [norm(a) for a in authors.split(";") if a.strip()]
    record = [norm(a) for a in rec["authors"]]
    missing = [a for a in claimed if not any(a == r or a in r.split() or r in a.split() for r in record)]
    first_ok = bool(claimed) and bool(record) and (claimed[0] == record[0] or claimed[0] in record[0].split())
    results["authors"] = (not missing and first_ok,
                          f"missing: {missing or 'none'}; first author matches: {first_ok}")

    results["year"] = (year in rec["years"], f"claimed {year}; record {sorted(rec['years']) or 'none'}")

    if venue:
        vsim = max([difflib.SequenceMatcher(None, norm(venue), norm(v)).ratio() for v in rec["venue"].split("|")] + [0])
        contained = norm(venue) in norm(rec["venue"])
        results["venue"] = (contained or vsim >= 0.8, f"record venue: {rec['venue'] or 'none'}")
    return results


def main():
    ap = argparse.ArgumentParser(description="Citation verification rule (methodology Stage 0).")
    ap.add_argument("--id", help="DOI or arXiv ID (URLs and prefixes accepted). Omit it and use --dblp for papers without one.")
    ap.add_argument("--title", required=True)
    ap.add_argument("--authors", required=True, help="family names separated by ';', first author first")
    ap.add_argument("--year", required=True, type=int)
    ap.add_argument("--venue", help="claimed venue (journal/conference). If omitted, check venue manually.")
    ap.add_argument("--json", action="store_true", help="print machine-readable result")
    ap.add_argument("--dblp", action="store_true",
                    help="paper has no DOI/arXiv ID: look it up on dblp by title; if not found or unreachable, flag [manual-check]")
    a = ap.parse_args()
    if not a.id and not a.dblp:
        ap.error("give --id, or --dblp for a paper without a DOI or arXiv ID")

    if a.dblp and not a.id:
        try:
            rec = record_from_dblp(a.title)
        except (urllib.error.URLError, LookupError, ValueError, KeyError) as e:
            print(f"dblp lookup failed: {e}\n"
                  "=> [manual-check]: verify title, authors, year and venue against the official proceedings page "
                  "before using this paper, and record the result in the literature matrix.")
            sys.exit(3)
        a.id = "dblp:" + rec["title"][:60]
    else:
      try:
        rec = lookup(a.id)
      except (urllib.error.URLError, LookupError, ValueError, KeyError, ET.ParseError) as e:
        print(f"RECORD NOT FOUND / ERROR for {a.id}: {e}\n"
              "=> NOT VERIFIED. Keep the tag [AI-unverified]; check the ID at https://doi.org or https://arxiv.org.")
        sys.exit(2)

    res = check(rec, a.title, a.authors, a.year, a.venue)
    ok = all(v[0] for v in res.values())
    if a.json:
        print(json.dumps({"id": a.id, "verified": ok, "venue_checked": bool(a.venue),
                          "record": {**rec, "years": sorted(rec["years"])},
                          "checks": {k: {"pass": v[0], "detail": v[1]} for k, v in res.items()}}, indent=2))
    else:
        print(f"Record ({rec['source']}): {rec['title']!r}")
        print(f"  authors: {', '.join(rec['authors'][:8])}{' …' if len(rec['authors']) > 8 else ''}")
        print(f"  years: {sorted(rec['years'])}   venue: {rec['venue'] or '-'}")
        for k, (passed, detail) in res.items():
            print(f"  [{'PASS' if passed else 'FAIL'}] {k}: {detail}")
        if not a.venue:
            print("  [NOTE] venue not checked: the rule requires it — compare the record venue above by hand.")
        print("=> VERIFIED" if ok else "=> NOT VERIFIED (do not use this reference; keep [AI-unverified])")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
